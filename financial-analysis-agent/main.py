import streamlit as st
import logging
import os
from datetime import datetime
import sys

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
    st.markdown("Enter your query below and the system will process it.")
    
    # Main text input
    user_input = st.text_area(
        "Enter your query:",
        placeholder="Type your financial analysis query here...",
        height=200,
        help="Enter any text related to financial analysis, stock queries, or market data requests."
    )
    
    # Submit button
    if st.button("Submit Query", type="primary"):
        if user_input.strip():
            logger.info(f"User submitted query: {user_input}")
            st.success("Query submitted successfully!")
            st.write("**Your query:**", user_input)
            
            # TODO: Add your API calls here
            # Example:
            # result = process_query(user_input)
            # st.write("**Result:**", result)
            
        else:
            logger.warning("User attempted to submit empty query")
            st.warning("Please enter some text before submitting.")
    
    # Display recent activity
    if st.checkbox("Show recent queries"):
        st.subheader("Recent Activity")
        # TODO: Add logic to display recent queries from logs or database
        st.info("Recent queries will be displayed here.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"Application error: {e}")
