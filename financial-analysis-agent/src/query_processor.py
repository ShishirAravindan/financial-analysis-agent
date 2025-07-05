"""
Query processor that combines LLM parsing with intent handling.
"""

import json
import logging
from google import genai
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

from .data_models import QueryResponse
from .data_fetcher import DataFetcher
from config.prompts import QUERY_CATEGORIZATION_PROMPT

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class QueryProcessor:
    """Combined LLM query parser and intent handler."""
    
    def __init__(self):
        self.logger = logger
        self.data_fetcher = DataFetcher()
        
        # Initialize Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.logger.info("Gemini model initialized")
    
    def parse_query(self, query: str) -> Optional[QueryResponse]:
        """Use Gemini to parse the user query and extract intent and entities."""
        try:
            # Format the prompt with the user query
            prompt = QUERY_CATEGORIZATION_PROMPT.format(query=query)
            
            # Get response from Gemini
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            response_text = response.text.strip()

            # Try to parse JSON response
            try:
                parsed_data = json.loads(response_text)
                
                # Validate and create QueryResponse object
                parsed_query = QueryResponse(**parsed_data)
                
                self.logger.info(f"Successfully parsed query: {parsed_query}")
                return parsed_query
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response: {e}")
                self.logger.debug(f"Raw response: {response_text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error parsing query with Gemini: {e}")
            return None
     
    def process_query(self, query: str) -> QueryResponse:
        """Main method to process a user query."""
        try:
            # Parse the query
            parsed_query = self.parse_query(query)
            if not parsed_query:
                self.logger.error(f"Failed to parse query: {query}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return None