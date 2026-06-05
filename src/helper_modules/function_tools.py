"""
Function Tools Module - Database queries, market data, and PII protection

This module provides function-based tools for SQL generation, market data retrieval,
and PII protection. These are the core business logic tools that enable the agent
to access database information and current market data.

Learning Objectives:
- Understand function tool creation with LlamaIndex
- Implement database querying with SQL generation
- Create market data retrieval tools
- Build PII protection mechanisms
- Learn about real-time API integration

Your Task: Complete the missing implementations marked with YOUR CODE HERE

Key Concepts:
1. FunctionTool Creation: Wrap Python functions as LlamaIndex tools
2. SQL Generation: Use LLM to generate SQL from natural language
3. Database Operations: Execute SQL queries and format results  
4. API Integration: Fetch real-time market data from external APIs
5. PII Protection: Automatically mask sensitive information
"""

import logging
import sqlite3
import random
from pathlib import Path
from typing import List, Tuple

# LlamaIndex imports
from llama_index.core import Settings
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Environment setup
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class FunctionToolsManager:
    """Manager for all function tools - Database, market data, and PII protection"""
    
    def __init__(self, verbose: bool = False):
        """Initialize function tools manager
        
        Args:
            verbose: Whether to print detailed progress information
        """
        self.verbose = verbose
        self.project_root = Path.cwd()
        self.db_path = self.project_root / "data" / "financial.db"
        
        # Database schema for SQL generation
        self.db_schema = self._get_database_schema()
        
        # Storage for tools
        self.function_tools = []
        
        self._configure_settings()
        
        if self.verbose:
            print("✅ Function Tools Manager Initialized")
    
    def _configure_settings(self):
        """Configure LlamaIndex settings
        
        TODO: Set up the LLM for SQL generation and other AI tasks
        
        Requirements:
        - Create OpenAI LLM with "gpt-3.5-turbo" model and temperature=0
        - Set Settings.llm and Settings.embed_model
        - Store LLM reference in self.llm for use in tools
        
        IMPORTANT NOTE FOR VOCAREUM:
        LlamaIndex requires the api_base parameter to work with Vocareum's OpenAI endpoint.
        Get the base URL from environment: os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")
        Pass it as api_base parameter to both OpenAI() and OpenAIEmbedding() constructors.
        
        Hint: This is similar to document_tools configuration
        """
        # YOUR CODE HERE
        pass
    
    def _get_database_schema(self) -> str:
        """Get enhanced database schema with relationships for SQL generation
        
        This method reads the database structure and returns a comprehensive
        schema description that helps the LLM generate better SQL queries.
        
        Returns:
            String containing detailed database schema with table relationships
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get table names to verify database connection
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            # Return comprehensive schema for SQL generation
            schema_info = """Enhanced Database Schema with Relationships:

TABLE: customers (Customer Information)
- id (PRIMARY KEY, INTEGER) - Unique customer identifier
- first_name (TEXT) - Customer first name
- last_name (TEXT) - Customer last name  
- email (TEXT) - Customer email address
- phone (TEXT) - Customer phone number
- investment_profile (TEXT) - conservative/moderate/aggressive
- risk_tolerance (TEXT) - low/medium/high

TABLE: portfolio_holdings (Customer Stock Holdings)
- id (PRIMARY KEY, INTEGER) - Unique holding record
- customer_id (FOREIGN KEY → customers.id) - Links to customer
- symbol (TEXT) - Stock symbol like 'AAPL', 'TSLA', 'MSFT', 'GOOGL'
- shares (REAL) - Number of shares owned
- purchase_price (REAL) - Price when purchased
- current_value (REAL) - Current total value of holding

TABLE: companies (Company Master Data)
- id (PRIMARY KEY, INTEGER) - Unique company identifier
- symbol (TEXT) - Stock symbol like 'AAPL', 'TSLA', 'MSFT', 'GOOGL'
- name (TEXT) - Company name like 'Apple Inc', 'Tesla Inc'
- sector (TEXT) - Business sector (technology, automotive, etc.)
- market_cap (REAL) - Market capitalization

TABLE: financial_metrics (Company Financial Data)
- id (PRIMARY KEY, INTEGER) - Unique metrics record
- symbol (FOREIGN KEY → companies.symbol) - Stock symbol
- revenue (REAL) - Company revenue
- net_income (REAL) - Net income
- eps (REAL) - Earnings per share
- pe_ratio (REAL) - Price to earnings ratio
- debt_to_equity (REAL) - Debt to equity ratio
- roe (REAL) - Return on equity

TABLE: market_data (Current Market Information)
- id (PRIMARY KEY, INTEGER) - Unique market record
- symbol (FOREIGN KEY → companies.symbol) - Stock symbol
- close_price (REAL) - Latest closing price
- volume (INTEGER) - Trading volume
- market_cap (REAL) - Current market cap
- date (TEXT) - Date of data

COMMON QUERY PATTERNS & JOINS:

1. Customer holdings with names:
   SELECT c.first_name, c.last_name, ph.symbol, ph.shares, ph.current_value
   FROM customers c 
   JOIN portfolio_holdings ph ON c.id = ph.customer_id

2. Holdings with company information:
   SELECT ph.symbol, co.name, ph.shares, ph.current_value, co.sector
   FROM portfolio_holdings ph
   JOIN companies co ON ph.symbol = co.symbol

3. Holdings with current market prices:
   SELECT ph.symbol, ph.shares, ph.current_value, md.close_price
   FROM portfolio_holdings ph
   JOIN market_data md ON ph.symbol = md.symbol

4. Complete customer portfolio view:
   SELECT c.first_name, c.last_name, co.name, ph.shares, 
          ph.current_value, md.close_price, co.sector
   FROM customers c
   JOIN portfolio_holdings ph ON c.id = ph.customer_id
   JOIN companies co ON ph.symbol = co.symbol
   JOIN market_data md ON ph.symbol = md.symbol

KEY TIPS:
- Use LIKE '%Tesla%' or LIKE '%Apple%' for company name searches
- Use symbol = 'TSLA', 'AAPL', 'MSFT', 'GOOGL' for exact stock matches
- JOIN portfolio_holdings with customers to get customer names
- JOIN with companies to get full company names and sectors
- JOIN with market_data to get current prices and volumes
"""
            
            conn.close()
            return schema_info
            
        except Exception as e:
            return f"Schema error: {e}\n\nFallback basic schema available."
    
    def create_function_tools(self):
        """Create function tools for database, market data, and PII protection
        
        This method creates three main function tools:
        1. Database Query Tool - Generates and executes SQL queries
        2. Market Search Tool - Fetches real-time stock data
        3. PII Protection Tool - Masks sensitive information
        
        Returns:
            List of FunctionTool objects
        """
        if self.verbose:
            print("🛠️ Creating function tools...")
        
        # Clear existing tools
        self.function_tools = []
        
        # TODO: Create the three main function tools
        # Implement these three nested functions and wrap them with FunctionTool:
        # 1. database_query_tool - Natural language to SQL conversion and execution
        # 2. finance_market_search_tool - Real-time Yahoo Finance API integration
        # 3. pii_protection_tool - Automatic PII detection and masking
        
        # 1. DATABASE QUERY TOOL
        def database_query_tool(query: str) -> str:
            """Generate and execute SQL queries for customer/portfolio database
            
            This tool takes a natural language query, converts it to SQL using
            the LLM, executes it against the database, and returns formatted results.
            
            Args:
                query: Natural language question about the database
                
            Returns:
                String containing SQL query and formatted results
            """
            
            def generate_sql(query_text: str, error_context: str = None) -> str:
                """Generate SQL query from natural language using LLM"""
                # TODO: Build prompt that includes database schema and query
                # Handle error_context for retry logic if previous query failed
                # Use self.llm.complete() to generate SQL
                # Clean up response (remove markdown, handle multiple statements)
                # YOUR CODE HERE
                
                return "SELECT 1"  # Placeholder - replace with your implementation
            
            def execute_sql(sql_query: str) -> Tuple[bool, list, list, str]:
                """Execute SQL and return (success, results, column_names, error)"""
                # TODO: Connect to database, execute query, extract results and column names
                # Return tuple: (success_flag, results_list, column_names_list, error_message)
                # YOUR CODE HERE
                
                return False, None, None, "Not implemented"
            
            try:
                # TODO: Implement the main database query logic
                # 1. Generate SQL from natural language query
                # 2. Execute the SQL and get results
                # 3. Format results with column names
                # 4. If execution fails, retry with error context
                # YOUR CODE HERE
                
                return "Database query not implemented yet"
                        
            except Exception as e:
                return f"Database system error: {e}"
        
        # 2. MARKET DATA TOOL
        def finance_market_search_tool(query: str) -> str:
            """Get real current stock prices and market information
            
            This tool fetches real-time stock data from Yahoo Finance API
            for Apple (AAPL), Tesla (TSLA), and Google (GOOGL).
            
            Args:
                query: Natural language query mentioning companies
                
            Returns:
                String containing current market data
            """
            
            def get_real_stock_data(symbol: str) -> dict:
                """Fetch real stock data from Yahoo Finance API"""
                # TODO: Make API call to Yahoo Finance
                # URL: https://query1.finance.yahoo.com/v8/finance/chart/{symbol}
                # Extract: current price, previous close, volume, market cap
                # Calculate: price change and change percentage
                # Return: Dictionary with stock data and success flag
                # YOUR CODE HERE
                
                return {'success': False, 'error': 'Not implemented'}
            
            try:
                # TODO: Identify companies mentioned in the query
                # Map company names/symbols to ticker symbols (AAPL, TSLA, GOOGL)
                # Fetch stock data for each identified company
                # Format results with price, change, volume
                # Handle API failures with appropriate fallbacks
                # YOUR CODE HERE
                
                return "Market data tool not implemented yet"
                    
            except Exception as e:
                return f"Market data error: {e}"
        
        # 3. PII PROTECTION TOOL
        def pii_protection_tool(database_results: str, column_names: str) -> str:
            """Automatically mask PII fields in database results
            
            This tool identifies and masks personally identifiable information
            in database query results based on column names and content patterns.
            
            Args:
                database_results: Raw database results as string
                column_names: List of column names (as string)
                
            Returns:
                String with PII fields masked for privacy protection
            """
            
            def detect_pii_fields(field_names: list) -> set:
                """Detect which fields contain PII based on field names"""
                # TODO: Create patterns for common PII field names
                # Check field names against patterns (email, phone, names, address, ssn, etc.)
                # Return set of detected PII field names
                # YOUR CODE HERE
                
                return set()  # Placeholder
            
            def mask_field_value(field_name: str, value: str) -> str:
                """Apply appropriate masking based on field type"""
                # TODO: Implement field-specific masking strategies
                # Examples: abc@gmail.com -> ***@gmail.com
                #          123-456-7890 -> ***-***-7890
                #          John -> ****
                # YOUR CODE HERE
                
                return str(value)  # Placeholder
            
            # TODO: Parse column names and detect PII fields
            # Parse database results line by line
            # For each line with PII fields, apply masking
            # Add notice about which fields were masked
            # YOUR CODE HERE
            
            return database_results  # Placeholder - no masking implemented
        
        # TODO: Create FunctionTool objects for each function
        # Wrap each function with FunctionTool.from_defaults()
        # Provide descriptive names and descriptions for agent routing
        # Add all tools to self.function_tools list
        # YOUR CODE HERE
        
        if self.verbose:
            print("   ✅ Function tools created")
        
        return self.function_tools
    
    def get_tools(self):
        """Get all function tools
        
        Returns:
            List of FunctionTool objects
        """
        return self.function_tools

