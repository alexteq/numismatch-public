# Numismatch

![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)

**Numismatch** is an AI-powered Roman coin identification and valuation agent built with Google Vertex AI and Google ADK (Agent Development Kit). It specializes in analyzing Roman coins from images and descriptions, providing coin identification and market price estimates.

## What the agent does

Numismatch is designed to recognize Roman coins by examining both images and textual descriptions. It identifies emperors, coin denominations, minting periods, and other relevant coin data. It also offers market value estimates, taking into account the coin's condition and rarity, and researches historical sale prices as well as broader trends in the coin market. This app utilizes the multimodal capabilities of Gemini models and the ADK agentic architecture to enable comprehensive, intelligent analysis.

## Key features

- **Multi-Agent Architecture**: Uses specialized sub-agents for identification, price estimation, quality assessment, and data validation
- **Multimodal Input**: Accepts both coin images and text descriptions
- **Tool Integration**: Incorporates external services such as Perplexity and Tavily as ADK agent tools
- **Production Ready**: Deployable on Vertex AI Agent Engine
- **Cloud-Native Deployment**: Live at https://numismatch.app, fully hosted on Google Cloud, with Vertex AI Agent Engine running the agent, and BigQuery used for logging and analyzing user-provided quality assessments

## How to Start

### Prerequisites

- Python 3.10-3.12
- Google Cloud Project with Vertex AI enabled
- Google Cloud SDK installed and configured

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd numismatch
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud authentication**:
   ```bash
   gcloud auth application-default login
   ```

4. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

### Local Testing

Run the agent locally with ADK web interface:

```bash
adk web --module numismatch.agent --object root_agent
```

Open http://localhost:8000 in your browser to use ADK Web interface, choose 'numismatch' agent and start sending images or/and textual coin descriptions!

**Sample Test Images**: The `sample_images/` folder contains test images you can use:
- `sample_images/RomanCoins/` - 5 sets of authentic Roman coin photos for testing identification
- `sample_images/NonRomanOrNotCoins/` - Non-Roman images for testing triage logic

### Example Queries

**Basic Identification**:
```
I have a silver coin about 19mm with "IMP CAESAR TRAIAN" and a portrait. 
The reverse shows a standing figure.
```

**With Image**:
Upload an image of your Roman coin (try images from `sample_images/RomanCoins/`) and ask:
```
Can you identify this coin and estimate its value?
```

**Detailed Description**:
```
Silver denarius, Emperor Augustus, obverse legend "CAESAR AVGVSTVS", 
reverse shows Capricorn, approximately 19mm diameter, 3.8 grams, 
good condition with clear details.
```

## 📁 Project Structure

```
numismatch/
├── agent.py                 # Main agent definition (root/triage agent)
├── agent_engine_app.py      # AgentEngine app wrapper for deployment using Vertex AI
├── pipeline_agents.py       # Pipeline sub-agents (identifier, researcher, validator and summarizer.)
├── tools.py                 # Custom tools and functions
├── __init__.py
├── requirements.txt         # Python dependencies
├── LICENSE                  # Apache 2.0 License
├── CONTRIBUTING.md          # Contribution guidelines
├── prompts/                 # Agent prompt files
│   ├── 0_root_agent_prompt.txt
│   ├── 1_coin_identifier_prompt.txt
│   ├── 2_price_researcher_prompt.txt
│   ├── 3_validator_prompt.txt
│   └── 4_summarizer_prompt.txt
└── sample_images/           # Test images for local development
    ├── RomanCoins/          # Sample Roman coin photos (5 sets)
    └── NonRomanOrNotCoins/  # Non-Roman test images
```

## Architecture

Numismatch uses a **multi-agent pipeline architecture**:

1. **Root Agent**: Fast triage to determine if input is related to a Roman coin
2. **Coin Identifier**: Analyzes images and text to identify the coin
3. **Price Researcher**: Searches for historical sales data and market values
4. **Validator**: Verifies identification accuracy and data quality
5. **Summarizer**: Compiles comprehensive JSON report with all findings


## API Usage

Once deployed, the agent exposes these operations:

### Query Endpoint (Async)

**Request**:
```json
{
  "message": "I have a silver denarius with Trajan",
  "user_id": "user-123",
  "session_id": "session-456"
}
```

**Response**:
```json
{
  "output": {
    "is_finished": true,
    "coin_details": {
      "emperor": "Trajan",
      "denomination": "Denarius",
      "period": "98-117 AD",
      ...
    },
    "historical_sales_data": [...],
    "market_statistics": {...}
  },
  "session_id": "session-456"
}
```


## Environment Variables

Configure these environment variables (see `.env.example`):

- `GOOGLE_CLOUD_PROJECT`: Your GCP project ID
- `GOOGLE_API_KEY`: API key for Gemini models to use
- `NUM_WORKERS`: Number of worker processes (default: 1)
- `PERPLEXITY_API_KEY`: API key for Perplexity price research
- `GOOGLE_GENAI_USE_VERTEXAI =1`: Use of Vertex AI


## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas where we'd love help:
- Additional coin identification tools
- Improved image preprocessing
- Market data integration
- Existing price search tools improvement or new tools development
- Documentation and examples

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

```
Copyright 2025

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
```

## Acknowledgments

Built with:
- [Google Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agents)
- [Google ADK (Agent Development Kit)](https://cloud.google.com/vertex-ai/docs/adk)
- [Gemini Models](https://deepmind.google/technologies/gemini/)

## 📞 Support

- **Questions**: Open a GitHub Discussion
- **Bug Reports**: Open a GitHub Issue

---

**Happy coin hunting!** 
