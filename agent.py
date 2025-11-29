"""
Numismatch - Roman Coin Identification and Price search

Simplified Architecture:
- Root Agent (LlmAgent): Does quick triage check with images
  * If NOT Roman → Returns JSON immediately (guaranteed structure via output_schema)
  * If Roman → Delegates to pipeline
- Roman Coin Pipeline (SequentialAgent): Full analysis (steps 1-4)
  * Identification → Price Research → Validation → Summary

No separate triage agent needed - root does it directly!
"""

from pathlib import Path
from google.adk.agents import Agent, SequentialAgent
from numismatch.app_utils.typing import TriageResponse
from numismatch.pipeline_agents import (
    coin_identifier,
    price_researcher,
    validator_agent,
    summarizer_agent,
)


def load_prompt(filename: str) -> str:
    """Load prompt from the prompts folder."""
    prompt_path = Path(__file__).parent / "prompts" / filename
    with open(prompt_path, "r") as f:
        return f.read()


# Roman Coin Pipeline (SequentialAgent)
# Steps 1-4: Full analysis pipeline (only runs if root confirms Roman)
roman_coin_pipeline = SequentialAgent(
    name='roman_coin_pipeline',
    description=(
        'Performs complete Roman coin analysis. '
        'Identifies catalog numbers, researches historical prices, '
        'validates data, and generates a comprehensive report.'
    ),
    sub_agents=[
        coin_identifier,    # Step 1: Identify + catalog search
        price_researcher,   # Step 2: Historical price research
        validator_agent,    # Step 3: Validate and clean data
        summarizer_agent,   # Step 4: Generate final report
    ],
)


# Root Agent
# Does quick triage check with images, then either responds or delegates
root_agent = Agent(
    model='gemini-2.5-flash',  # Fast, lightweight model for triage
    name='numismatch_root',
    description=(
        'Roman coin identification system. '
        'Quickly checks if data is Roman coin related. '
        'If Roman, delegates to pipeline for full analysis. '
        'If not Roman, returns negative result to the user.'
    ),
    instruction=load_prompt("0_root_agent_prompt.txt"),
    output_schema=TriageResponse,  # Ensures guaranteed JSON structure when NOT delegating
    sub_agents=[
        roman_coin_pipeline,  # Delegates here if Roman coin detected
    ],
)
