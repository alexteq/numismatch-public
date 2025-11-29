# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# mypy: disable-error-code="attr-defined,arg-type"
import logging
import os
from typing import Any

import google.auth
import vertexai
from google.adk.artifacts import GcsArtifactService, InMemoryArtifactService
from google.cloud import logging as google_cloud_logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, export
from vertexai.agent_engines.templates.adk import AdkApp

from numismatch.agent import root_agent
from numismatch.app_utils.tracing import CloudTraceLoggingSpanExporter
from numismatch.app_utils.typing import Feedback

class AgentEngineApp(AdkApp):
    def set_up(self) -> None:
        """Set up logging and tracing for the agent engine app."""
        super().set_up()
        logging.basicConfig(level=logging.INFO)
        logging_client = google_cloud_logging.Client()
        self.logger = logging_client.logger(__name__)
        provider = TracerProvider()
        processor = export.BatchSpanProcessor(
            CloudTraceLoggingSpanExporter(
                project_id=os.environ.get("GOOGLE_CLOUD_PROJECT")
            )
        )
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)

    async def query(
        self,
        message: str | dict[str, Any],
        user_id: str | None = None,
        session_id: str | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """
        Minimal query wrapper that uses ADK's built-in session management.
        This method is exposed as a REST endpoint for external clients.
        
        Note: Vertex AI Agent Engine REST API spreads the 'input' dict as kwargs,
        so message, user_id, session_id come in as separate parameters.
        """
        # If message is a dict with user_id/session_id keys (legacy format), extract them
        # Otherwise, message is already the Content dict (role, parts) from the REST API
        if isinstance(message, dict) and ("user_id" in message or "session_id" in message):
            user_id = message.get("user_id") or user_id
            session_id = message.get("session_id") or session_id
            message = message.get("message", message.get("input", ""))
        
        # Ensure we have a user_id
        if not user_id:
            user_id = f"user-{id(self)}"
        
        logging.info(
            "Query: user_id=%s, session_id=%s",
            user_id,
            session_id,
        )
        
        # Call parent's async_stream_query (which handles sessions automatically)
        full_text = ""
        
        async for event in self.async_stream_query(
            message=message,
            user_id=user_id,
            session_id=session_id,
            **kwargs
        ):
            # Extract text from event
            if isinstance(event, dict) and "content" in event:
                content = event["content"]
                if isinstance(content, dict) and "parts" in content:
                    for part in content["parts"]:
                        if isinstance(part, dict) and "text" in part:
                            full_text += part["text"]
        
        # Return response with just output (session_id not available here)
        response = {"output": full_text or "No response generated"}
        return response

    def register_feedback(self, feedback: dict[str, Any]) -> None:
        """Collect and log feedback."""
        feedback_obj = Feedback.model_validate(feedback)
        self.logger.log_struct(feedback_obj.model_dump(), severity="INFO")

    def register_operations(self) -> dict[str, list[str]]:
        """Register custom operations for Agent Engine."""
        operations = super().register_operations()
        # Register our minimal query wrapper and feedback as custom operations
        operations["async"] = operations.get("async", []) + ["query"]
        operations[""] = operations.get("", []) + ["register_feedback"]
        return operations



_, project_id = google.auth.default()
vertexai.init(project=project_id, location="us-central1")
artifacts_bucket_name = os.environ.get("ARTIFACTS_BUCKET_NAME")
agent_engine = AgentEngineApp(
    agent=root_agent,
    artifact_service_builder=lambda: GcsArtifactService(
        bucket_name=artifacts_bucket_name
    )
    if artifacts_bucket_name
    else InMemoryArtifactService(),
)
