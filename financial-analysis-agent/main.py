import streamlit as st
import logging
import os
from datetime import datetime
import sys
import traceback
import json

# Import our custom modules
from src.query_processor import QueryProcessor

# Configure logging
def setup_logging():
    """Setup logging configuration with both file and console handlers"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

# Initialize logger
logger = setup_logging()

# Initialize components
@st.cache_resource
def get_query_processor():
    """Get cached query processor instance."""
    try:
        return QueryProcessor()
    except Exception as e:
        logger.error(f"Failed to initialize QueryProcessor: {e}")
        st.error(f"Failed to initialize the system: {e}")
        return None

def display_query_analysis(parsed_query):
    """Display the parsed query information."""
    st.subheader("📊 Query Analysis")
    
    # Display category and analysis type
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Category", parsed_query.category.replace("_", " ").title())
    with col2:
        st.metric("Analysis Type", parsed_query.analysis_type.replace("_", " ").title())
    
    # Display entities
    st.subheader("🔍 Extracted Entities")
    
    # Symbols
    if parsed_query.entities.symbols:
        st.write("**Symbols:**", ", ".join(parsed_query.entities.symbols))
    
    # Time period
    if parsed_query.entities.time_period:
        st.write("**Time Period:**", parsed_query.entities.time_period)
    
    # Events
    if parsed_query.entities.events:
        st.write("**Events/Regimes:**", ", ".join(parsed_query.entities.events))
    
    # Metrics
    if parsed_query.entities.metrics:
        st.write("**Metrics:**", ", ".join(parsed_query.entities.metrics))

def main():
    """Main Streamlit application"""
    # Page configuration
    st.set_page_config(
        page_title="Financial Analysis Agent",
        page_icon="📊",
        layout="wide"
    )
    
    # Log app startup
    logger.info("Streamlit app started")
    
    # Header
    st.title("📊 Financial Analysis Agent")
    st.markdown("Ask me anything about financial analysis, statistical tests, or market data!")
    
    # Initialize components
    query_processor = get_query_processor()
    
    if query_processor is None:
        st.error("System initialization failed. Please check your API keys and try again.")
        return
    
    # Main text input
    user_input = st.text_area(
        "Enter your analysis query:",
        placeholder="e.g., 'Is SPY's average daily return significantly different from zero?' or 'Are FAANG stocks becoming more correlated?'",
        height=100,
        help="Ask about statistical analysis, correlations, risk measurements, or market patterns."
    )
    
    # Submit button
    if st.button("Analyze Query", type="primary"):
        if user_input.strip():
            logger.info(f"User submitted query: {user_input}")
            
            # Show processing indicator
            with st.spinner("Analyzing your query..."):
                try:
                    # Process the query
                    parsed_query = query_processor.process_query(user_input)
                    
                    if parsed_query:
                        # Display results
                        st.success("Query analyzed successfully!")
                        
                        # Show the original query
                        st.write("**Your query:**", user_input)
                        st.divider()
                        
                        # Display the parsed information
                        display_query_analysis(parsed_query)
                        
                        # Show raw model response (for debugging)
                        with st.expander("🔧 Raw Model Response"):
                            st.json(parsed_query.model_dump())
                        
                        # Show what we can do with this analysis
                        st.subheader("🎯 Analysis Plan")
                        
                        if parsed_query.category == "single_stock_analysis":
                            st.info("This is a single stock analysis. We can perform statistical tests, volatility analysis, or return analysis.")
                        elif parsed_query.category == "event_regime":
                            st.info("This is an event/regime analysis. We can study seasonal patterns, event effects, or market regimes.")
                        elif parsed_query.category == "cross_asset_correlation":
                            st.info("This is a cross-asset correlation analysis. We can compare multiple assets, find similarities, or analyze correlations.")
                        elif parsed_query.category == "risk_stress_testing":
                            st.info("This is a risk/stress testing analysis. We can measure risk metrics, perform stress tests, or analyze volatility clustering.")
                        
                        st.write("**Next steps:** Implement the specific analysis based on the extracted information.")
                        
                    else:
                        st.error("Failed to analyze the query. Please try rephrasing your question.")
                    
                except Exception as e:
                    logger.error(f"Error processing query: {e}")
                    logger.error(traceback.format_exc())
                    st.error(f"An error occurred while analyzing your query: {str(e)}")
                    st.info("Please try rephrasing your question or check if the stock symbols are correct.")
            
        else:
            logger.warning("User attempted to submit empty query")
            st.warning("Please enter some text before submitting.")
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        logger.error(traceback.format_exc())
        st.error(f"Application error: {e}")
