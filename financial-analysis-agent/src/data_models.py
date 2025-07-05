"""
Data models for the financial analysis agent.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class StockPrice(BaseModel):
    """Current stock price data."""
    symbol: str
    price: float
    currency: str
    timestamp: datetime
    change: Optional[float] = None
    change_percent: Optional[float] = None


class HistoricalData(BaseModel):
    """Historical stock data."""
    symbol: str
    data: dict  # DataFrame-like data from yfinance
    period: str
    start_date: datetime
    end_date: datetime


class StockInfo(BaseModel):
    """General stock information."""
    symbol: str
    company_name: str
    sector: Optional[str] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    volume: Optional[int] = None

class QueryEntities(BaseModel):
    """Entities extracted from a user query."""
    symbols: List[str]
    time_period: str
    events: List[str]
    metrics: List[str]
    
class QueryResponse(BaseModel):
    """Response from a query."""
    category: str
    entities: QueryEntities

