"""
Custom tools for Numismatch agents.
"""

import os
from openai import OpenAI


def perplexity_search(query: str) -> str:
    """
    Search the web using Perplexity AI for Roman coin price information.
    
    This tool uses Perplexity's advanced search and reasoning capabilities
    to find auction results, dealer listings, and historical sales data
    for Roman coins.
    
    Args:
        query: The search query (e.g., "RIC II.1 123 Vespasian denarius auction sold prices")
    
    Returns:
        Search results from Perplexity including sources and citations
    """
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return "Error: PERPLEXITY_API_KEY environment variable not set. Please configure your API key."
    
    try:
        # Perplexity uses OpenAI-compatible API
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        
        # Use Perplexity's search-optimized model
        response = client.chat.completions.create(
            model="sonar",  # Perplexity's search model
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a specialized search assistant for Roman coin price research. "
                        "Find auction results, dealer listings, and historical sales data. "
                        "Provide your results as a list of objects with the following keys: source, url, coin image-url, date, price, condition, notes. "
                        "Always include source URLs, price, image URLs and dates when available. "
                        "Focus on reputable sources like Heritage Auctions, CNG, Roma Numismatics, "
                        "Stack's Bowers, Gorny & Mosch, NAC."
                        "Use also sites like Biddr, Numista, vcoins, coinarchives, ma-shops.de, ebay and others"
                    )
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            temperature=0.15,  # Lower temperature for more factual results
            max_tokens=4000,
        )
        
        result = response.choices[0].message.content
        
        # Add citation information if available
        if hasattr(response, 'citations') and response.citations:
            result += "\n\nSources:\n"
            for i, citation in enumerate(response.citations, 1):
                result += f"{i}. {citation}\n"
        
        return result
        
    except Exception as e:
        return f"Error calling Perplexity API: {str(e)}"

