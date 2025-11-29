"""
Numismatch Pipeline Agents

Individual agents for the Roman coin identification and pricing pipeline.
These run sequentially only if the root agent determines the coin is Roman.

Pipeline steps:
1. Coin Identifier - Identifies catalog numbers with search
2. Price Researcher - Finds historical sales data with Perplexity AI
3. Validator - Validates and cleans results with search
4. Summarizer - Generates final structured JSON report
"""

from pathlib import Path
from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool
from numismatch.app_utils.typing import CoinIdentificationReport
from numismatch.tools import perplexity_search


def load_prompt(filename: str) -> str:
    """Load prompt from the prompts directory."""
    prompt_path = Path(__file__).parent / "prompts" / filename
    with open(prompt_path, "r") as f:
        return f.read()


# Step 1: Coin Identifier (Heavy Model with Search)
coin_identifier = Agent(
    model='gemini-2.5-pro',
    name='coin_identifier',
    description='Identifies Roman coins and finds catalog numbers using image analysis and internet search',
    instruction=load_prompt("1_coin_identifier_prompt.txt"),
    output_key='coin_data',
)

# Step 2: Price Researcher (with Search)
price_researcher = Agent(
    model='gemini-2.5-flash',
    name='price_researcher',
    description='Searches for historical sales data using Perplexity AI for comprehensive price research',
    instruction=load_prompt("2_price_researcher_prompt.txt"),
    output_key='price_data',
    tools=[perplexity_search, GoogleSearchTool(bypass_multi_tools_limit=True)],
)

# Step 3: Validator (Fast Model with Search)
validator_agent = Agent(
    model='gemini-2.5-flash',
    name='validator',
    description='Validates catalog numbers and price data, removes duplicates and inconsistencies',
    instruction=load_prompt("3_validator_prompt.txt"),
    output_key='validated_results',
    tools=[GoogleSearchTool(bypass_multi_tools_limit=True)],
)

# Step 4: Summarizer (Final Report Generator)
summarizer_agent = Agent(
    model='gemini-2.5-flash',
    name='summarizer',
    description='Creates comprehensive final structured JSON report with all identification and pricing data',
    instruction=load_prompt("4_summarizer_prompt.txt"),
    output_key='final_report',
    output_schema=CoinIdentificationReport,  # Ensures guaranteed JSON structure
    tools=[],
)

