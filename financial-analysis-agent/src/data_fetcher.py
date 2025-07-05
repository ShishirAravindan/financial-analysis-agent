"""
Data fetcher module using yfinance.
"""

import yfinance as yf
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
import pandas as pd

from .data_models import StockPrice, HistoricalData, StockInfo

logger = logging.getLogger(__name__)


class DataFetcher:
    """Wrapper around yfinance for fetching financial data."""
    
    def __init__(self):
        self.logger = logger
    
    def get_current_price(self, symbol: str) -> Optional[StockPrice]:
        """Get current price for a stock symbol."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get current price
            current_price = info.get('regularMarketPrice')
            if current_price is None:
                self.logger.warning(f"Could not get current price for {symbol}")
                return None
            
            # Get additional info
            currency = info.get('currency', 'USD')
            timestamp = datetime.now()
            
            # Get change info if available
            previous_close = info.get('regularMarketPreviousClose')
            change = None
            change_percent = None
            
            if previous_close:
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100
            
            return StockPrice(
                symbol=symbol,
                price=current_price,
                currency=currency,
                timestamp=timestamp,
                change=change,
                change_percent=change_percent
            )
            
        except Exception as e:
            self.logger.error(f"Error fetching current price for {symbol}: {e}")
            return None
    
    def get_historical_data(self, symbol: str, period: str = "1mo") -> Optional[HistoricalData]:
        """Get historical data for a stock symbol."""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                self.logger.warning(f"No historical data found for {symbol}")
                return None
            
            # Convert DataFrame to dict for easier handling
            data_dict = hist.to_dict('index')
            
            # Get start and end dates
            start_date = hist.index[0].to_pydatetime()
            end_date = hist.index[-1].to_pydatetime()
            
            return HistoricalData(
                symbol=symbol,
                data=data_dict,
                period=period,
                start_date=start_date,
                end_date=end_date
            )
            
        except Exception as e:
            self.logger.error(f"Error fetching historical data for {symbol}: {e}")
            return None
    
    def get_stock_info(self, symbol: str) -> Optional[StockInfo]:
        """Get general stock information."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return StockInfo(
                symbol=symbol,
                company_name=info.get('longName', symbol),
                sector=info.get('sector'),
                market_cap=info.get('marketCap'),
                pe_ratio=info.get('trailingPE'),
                dividend_yield=info.get('dividendYield'),
                volume=info.get('volume')
            )
            
        except Exception as e:
            self.logger.error(f"Error fetching stock info for {symbol}: {e}")
            return None
    
    def get_multiple_prices(self, symbols: List[str]) -> Dict[str, StockPrice]:
        """Get current prices for multiple symbols."""
        results = {}
        for symbol in symbols:
            price_data = self.get_current_price(symbol)
            if price_data:
                results[symbol] = price_data
        return results
    
    def validate_symbol(self, symbol: str) -> bool:
        """Check if a symbol is valid by attempting to get basic info."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info.get('regularMarketPrice') is not None
        except:
            return False 