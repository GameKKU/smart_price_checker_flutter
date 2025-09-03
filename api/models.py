from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ItemInfo(BaseModel):
    name: str
    series: str
    year: str
    condition: str

class PriceRange(BaseModel):
    min: float
    max: float
    currency: str
    suggested: float

class MarketResult(BaseModel):
    title: str
    price: str
    source: str
    url: Optional[str] = None

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    estimated_time: int

class AnalysisResult(BaseModel):
    analysis_id: str
    status: str
    item_info: Optional[ItemInfo] = None
    price_range: Optional[PriceRange] = None
    confidence: Optional[float] = None
    market_data: List[MarketResult] = []
    created_at: str
    completed_at: Optional[str] = None
    error_message: Optional[str] = None

class UserHistoryResponse(BaseModel):
    analyses: List[AnalysisResult]
    total_count: int
    page: int
    limit: int