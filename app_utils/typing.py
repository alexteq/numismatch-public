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
from typing import (
    Literal,
)

from pydantic import (
    BaseModel,
    Field,
)


class Feedback(BaseModel):
    """Represents feedback for a conversation."""

    score: int | float
    text: str | None = ""
    invocation_id: str
    log_type: Literal["feedback"] = "feedback"
    service_name: Literal["capstoneproject"] = "capstoneproject"
    user_id: str = ""


class TriageResponse(BaseModel):
    """
    Structured response from the root triage agent when NOT delegating to pipeline.
    
    This schema ensures guaranteed JSON output when the agent determines
    the input is not Roman coin data or has insufficient information.
    """

    is_roman: bool = Field(
        description="Boolean indicating whether the data relates to a Roman coin. "
        "Should be False when returning this response (True cases delegate to pipeline)."
    )
    response: str = Field(
        description="Brief explanation to the user. Should indicate why the data "
        "was classified as non-Roman (e.g., 'appears to be Greek', 'Byzantine era', "
        "'insufficient information provided')."
    )
    is_finished: bool = Field(
        default=True,
        description="Indicates the workflow is complete. Always True for non-Roman responses."
    )


class Inscriptions(BaseModel):
    """Coin inscriptions on obverse and reverse."""
    
    obverse: str = Field(
        description="Inscription on the obverse (front) of the coin. "
        "Use 'Not fully legible' if unclear."
    )
    reverse: str = Field(
        description="Inscription on the reverse (back) of the coin. "
        "Use 'Not fully legible' if unclear."
    )


class CatalogNumber(BaseModel):
    """Catalog reference for the coin."""
    
    catalog_type: str = Field(
        description="Type of catalog (e.g., RIC, RSC, Sear, Cohen, BMCRE)"
    )
    number: str = Field(
        description="The full catalog number/reference"
    )
    source: str = Field(
        description="How this catalog number was identified (e.g., 'Internet search', 'Database match')"
    )


class HistoricalSale(BaseModel):
    """Individual historical sale record."""
    
    no: int = Field(
        description="Sale number/index in the list (1, 2, 3, etc.)"
    )
    price: str = Field(
        description="Sale price with currency symbol (e.g., '$450', '€320', '£280')"
    )
    date: str = Field(
        description="Date of the sale (e.g., '2023-05-15', 'May 2023', '2023')"
    )
    condition: str = Field(
        description="Condition grade or description (e.g., 'VF', 'XF', 'Good', 'About VF')"
    )
    link: str | None = Field(
        default=None,
        description="URL to the auction listing or sale record. None if not available."
    )
    image_url: str | None = Field(
        default=None,
        description="URL to the coin image from the sale. None if not available."
    )
    notes: str | None = Field(
        default=None,
        description="Additional notes about the sale (e.g., 'Dealer listing - asking price', 'Auction realized price')"
    )


class CoinDetails(BaseModel):
    """Detailed information about the identified coin."""
    
    emperor: str = Field(
        description="Name of the emperor or ruler (e.g., 'Augustus', 'Trajan', 'Hadrian')"
    )
    denomination: str = Field(
        description="Type of coin (e.g., 'Denarius', 'Aureus', 'Sestertius', 'As')"
    )
    metal: str = Field(
        description="Metal composition (e.g., 'Silver', 'Gold', 'Bronze', 'Copper')"
    )
    period: str = Field(
        description="Date range or period (e.g., '27 BC - 14 AD', 'c. 100-110 AD')"
    )
    mint: str = Field(
        description="Mint location (e.g., 'Rome', 'Alexandria', 'Unknown')"
    )
    inscriptions: Inscriptions = Field(
        description="Obverse and reverse inscriptions"
    )
    catalog_numbers: list[CatalogNumber] = Field(
        description="List of catalog references found for this coin. "
        "Multiple references strengthen identification accuracy."
    )


class MarketStatistics(BaseModel):
    """Market analysis statistics."""
    
    total_sales: int = Field(
        description="Total number of historical sales found"
    )
    average_price: str | None = Field(
        default=None,
        description="Average sale price with currency (e.g., '$425'). None if insufficient data."
    )
    price_range: str | None = Field(
        default=None,
        description="Price range (e.g., '$200 - $650'). None if insufficient data."
    )


class IdentificationSummary(BaseModel):
    """Summary of the identification process and confidence."""
    
    overall_confidence: str = Field(
        description="Confidence level (e.g., 'High', 'Medium', 'Low', 'Very High')"
    )
    catalog_status: str = Field(
        description="Status of catalog identification (e.g., 'Multiple catalogs found', 'Single catalog match')"
    )
    price_research_status: str = Field(
        description="Status and limitations of price research (e.g., 'Multiple verified sales found', 'Limited data available')"
    )
    validation_status: str = Field(
        description="Validation status (e.g., 'All checks passed', 'Issues encountered')"
    )
    validation_notes: list[str] = Field(
        default_factory=list,
        description="Important notes from validation process"
    )
    issues: list[str] = Field(
        default_factory=list,
        description="Any issues encountered during the analysis"
    )


class CoinIdentificationReport(BaseModel):
    """
    Complete structured report for Roman coin identification and pricing.
    
    This schema ensures guaranteed JSON output from the summarizer agent
    with all identification, catalog, and historical sales data.
    """
    
    is_finished: bool = Field(
        default=True,
        description="Indicates the agentic workflow is complete. Always True for final reports."
    )
    coin_details: CoinDetails = Field(
        description="Comprehensive details about the identified coin"
    )
    historical_sales_data: list[HistoricalSale] = Field(
        description="List of historical sales with prices, dates, conditions, and links. "
        "Empty list if no sales data found."
    )
    market_statistics: MarketStatistics | None = Field(
        default=None,
        description="Market analysis statistics. None if insufficient sales data."
    )
    identification_summary: IdentificationSummary = Field(
        description="Summary of identification confidence and any issues"
    )
