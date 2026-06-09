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

Implementation status: complete.

Key Concepts:
1. FunctionTool Creation: Wrap Python functions as LlamaIndex tools
2. SQL Generation: Use LLM to generate SQL from natural language
3. Database Operations: Execute SQL queries and format results  
4. API Integration: Fetch real-time market data from external APIs
5. PII Protection: Automatically mask sensitive information
"""

import logging
import ast
import os
import re
import sqlite3
import random
import requests
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
        api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

        self.llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_base=api_base,
        )
        Settings.llm = self.llm
        Settings.embed_model = OpenAIEmbedding(
            model="text-embedding-ada-002",
            api_base=api_base,
        )
    
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
        
        # Create the three main function tools and wrap them with FunctionTool:
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
                # Build a schema-grounded prompt, then clean common LLM formatting.
                error_instruction = ""
                if error_context:
                    error_instruction = (
                        f"\nThe previous SQL failed with this error: {error_context}\n"
                        "Correct the SQL while preserving the user's intent.\n"
                    )

                prompt = f"""
You are a careful SQLite query generator for a financial services database.
Convert the user's question into one valid SQLite SELECT statement.

Rules:
- Return only SQL, with no Markdown, commentary, or explanation.
- Use only SELECT statements.
- Use table and column names exactly as shown in the schema.
- Prefer explicit JOINs when a question spans customers, holdings, companies, or market data.
- Limit broad result sets to 20 rows unless the user asks for an aggregate count or summary.

{self.db_schema}
{error_instruction}
User question: {query_text}
SQL:
"""
                response = self.llm.complete(prompt)
                sql_query = str(response).strip()

                sql_query = re.sub(r"^```(?:sql)?\s*", "", sql_query, flags=re.IGNORECASE)
                sql_query = re.sub(r"\s*```$", "", sql_query)
                sql_query = sql_query.strip()

                statements = [stmt.strip() for stmt in sql_query.split(";") if stmt.strip()]
                sql_query = statements[0] if statements else ""

                if not sql_query.lower().startswith("select"):
                    raise ValueError(f"Generated SQL must be a SELECT statement. Got: {sql_query}")

                return sql_query
            
            def execute_sql(sql_query: str) -> Tuple[bool, list, list, str]:
                """Execute SQL and return (success, results, column_names, error)"""
                # Return tuple: (success_flag, results_list, column_names_list, error_message).
                try:
                    if not sql_query.strip().lower().startswith("select"):
                        return False, None, None, "Only SELECT queries are allowed"

                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute(sql_query)
                    results = cursor.fetchall()
                    column_names = (
                        [description[0] for description in cursor.description]
                        if cursor.description
                        else []
                    )
                    conn.close()
                    return True, results, column_names, ""
                except Exception as e:
                    return False, None, None, str(e)
            
            try:
                # Generate SQL, execute it, retry once on failure, then format rows.
                sql_query = generate_sql(query)
                success, results, column_names, error = execute_sql(sql_query)

                if not success:
                    sql_query = generate_sql(query, error_context=error)
                    success, results, column_names, error = execute_sql(sql_query)

                if not success:
                    return (
                        "Database query failed after retry.\n"
                        f"SQL Query: {sql_query}\n"
                        f"Error: {error}"
                    )

                formatted_rows = []
                for row in results:
                    formatted_rows.append(dict(zip(column_names, row)))

                if not formatted_rows:
                    result_text = "No matching rows found."
                else:
                    result_text = "\n".join(str(row) for row in formatted_rows)

                return (
                    f"SQL Query: {sql_query}\n\n"
                    f"COLUMNS: {column_names}\n\n"
                    f"Database Results:\n{result_text}"
                )
                        
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
                def get_cached_stock_data(error_message: str) -> dict:
                    """Fetch latest stored market data when live Yahoo data is unavailable"""
                    try:
                        conn = sqlite3.connect(self.db_path)
                        cursor = conn.cursor()
                        cursor.execute(
                            """
                            SELECT close_price, volume, market_cap, date
                            FROM market_data
                            WHERE symbol = ?
                            ORDER BY date DESC
                            LIMIT 2
                            """,
                            (symbol,),
                        )
                        rows = cursor.fetchall()
                        conn.close()

                        if not rows:
                            return {
                                "success": False,
                                "symbol": symbol,
                                "error": error_message,
                            }

                        current_price, volume, market_cap, date = rows[0]
                        previous_close = rows[1][0] if len(rows) > 1 else current_price
                        change = current_price - previous_close
                        change_percent = (change / previous_close) * 100 if previous_close else 0

                        return {
                            "success": True,
                            "symbol": symbol,
                            "current_price": current_price,
                            "previous_close": previous_close,
                            "change": change,
                            "change_percent": change_percent,
                            "volume": volume,
                            "market_cap": market_cap,
                            "source": f"cached market_data table ({date})",
                            "live_error": error_message,
                        }
                    except Exception as cache_error:
                        return {
                            "success": False,
                            "symbol": symbol,
                            "error": f"{error_message}; cache fallback failed: {cache_error}",
                        }

                # Make API call to Yahoo Finance.
                # URL: https://query1.finance.yahoo.com/v8/finance/chart/{symbol}
                # Extract: current price, previous close, volume, market cap
                # Calculate: price change and change percentage
                # Return: Dictionary with stock data and success flag
                try:
                    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    data = response.json()

                    result = data.get("chart", {}).get("result", [])
                    if not result:
                        return get_cached_stock_data("No market data returned from Yahoo Finance")

                    meta = result[0].get("meta", {})
                    current_price = meta.get("regularMarketPrice")
                    previous_close = meta.get("chartPreviousClose") or meta.get("previousClose")
                    volume = meta.get("regularMarketVolume")
                    market_cap = meta.get("marketCap")

                    if current_price is None or previous_close is None:
                        return get_cached_stock_data("Yahoo Finance response missing price data")

                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100 if previous_close else 0

                    return {
                        "success": True,
                        "symbol": symbol,
                        "current_price": current_price,
                        "previous_close": previous_close,
                        "change": change,
                        "change_percent": change_percent,
                        "volume": volume,
                        "market_cap": market_cap,
                        "source": "Yahoo Finance",
                    }
                except Exception as e:
                    return get_cached_stock_data(str(e))
            
            try:
                # Map company names/symbols to ticker symbols (AAPL, TSLA, GOOGL).
                query_lower = query.lower()
                symbol_map = {
                    "AAPL": ["aapl", "apple"],
                    "GOOGL": ["googl", "google", "alphabet"],
                    "TSLA": ["tsla", "tesla"],
                }

                requested_symbols = [
                    symbol
                    for symbol, aliases in symbol_map.items()
                    if any(alias in query_lower for alias in aliases)
                ]

                if not requested_symbols:
                    requested_symbols = list(symbol_map.keys())
                
                # Fetch stock data for each identified company
                stock_results = [get_real_stock_data(symbol) for symbol in requested_symbols]
                
                # Format results with price, change, volume
                formatted_results = []
                for stock_data in stock_results:
                    symbol = stock_data.get("symbol", "UNKNOWN")
                    if not stock_data.get("success"):
                        formatted_results.append(
                            f"{symbol}: Market data unavailable ({stock_data.get('error', 'unknown error')})"
                        )
                        continue

                    market_cap = stock_data.get("market_cap")
                    market_cap_text = f"${market_cap:,.0f}" if market_cap else "Not available"
                    volume = stock_data.get("volume")
                    volume_text = f"{volume:,}" if volume else "Not available"

                    formatted_results.append(
                        f"{symbol} Market Data:\n"
                        f"- Current Price: ${stock_data['current_price']:.2f}\n"
                        f"- Previous Close: ${stock_data['previous_close']:.2f}\n"
                        f"- Change: ${stock_data['change']:.2f} "
                        f"({stock_data['change_percent']:.2f}%)\n"
                        f"- Volume: {volume_text}\n"
                        f"- Market Cap: {market_cap_text}\n"
                        f"- Source: {stock_data.get('source', 'Unknown')}"
                    )
                
                # API failures are handled inside get_real_stock_data using cached data.
                return "\n\n".join(formatted_results)
                    
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
                # Check field names against common PII patterns.
                pii_patterns = [
                    "name",
                    "email",
                    "phone",
                    "address",
                    "ssn",
                    "social_security",
                    "date_of_birth",
                    "dob",
                ]

                pii_fields = set()
                for field_name in field_names:
                    normalized_name = str(field_name).lower()
                    if any(pattern in normalized_name for pattern in pii_patterns):
                        pii_fields.add(field_name)

                return pii_fields
            
            def mask_field_value(field_name: str, value: str) -> str:
                """Apply appropriate masking based on field type"""
                # Apply field-specific masking strategies.
                # Examples: abc@gmail.com -> ***@gmail.com
                #          123-456-7890 -> ***-***-7890
                #          John -> ****
                value_str = str(value)
                normalized_name = field_name.lower()

                if value_str in {"", "None", "NULL"}:
                    return value_str

                if "email" in normalized_name and "@" in value_str:
                    _, domain = value_str.split("@", 1)
                    return f"***@{domain}"

                if "phone" in normalized_name:
                    digits = re.sub(r"\D", "", value_str)
                    if len(digits) >= 4:
                        return f"***-***-{digits[-4:]}"
                    return "***"

                if "name" in normalized_name:
                    return "*" * len(value_str)

                return "***"
            
            # Parse column names, mask PII fields row by row, and add a notice.
            try:
                parsed_columns = ast.literal_eval(column_names)
                if not isinstance(parsed_columns, list):
                    parsed_columns = [str(parsed_columns)]
            except Exception:
                parsed_columns = [
                    column.strip().strip("'\"")
                    for column in column_names.strip("[]").split(",")
                    if column.strip()
                ]

            pii_fields = detect_pii_fields(parsed_columns)
            if not pii_fields:
                return database_results

            protected_lines = []
            for line in database_results.splitlines():
                stripped_line = line.strip()
                if stripped_line.startswith("{") and stripped_line.endswith("}"):
                    try:
                        row = ast.literal_eval(stripped_line)
                        if isinstance(row, dict):
                            protected_row = {}
                            for field_name, value in row.items():
                                if field_name in pii_fields:
                                    protected_row[field_name] = mask_field_value(field_name, value)
                                else:
                                    protected_row[field_name] = value
                            protected_lines.append(str(protected_row))
                            continue
                    except Exception:
                        protected_lines.append(line)
                        continue

                protected_lines.append(line)

            masked_fields = ", ".join(sorted(pii_fields))
            return (
                f"PII protection applied. Masked fields: {masked_fields}\n\n"
                + "\n".join(protected_lines)
            )
        
        # Wrap functions as agent-usable tools with descriptive routing metadata.
        self.function_tools = [
            FunctionTool.from_defaults(
                fn=database_query_tool,
                name="database_query_tool",
                description=(
                    "Use this tool to answer questions about customers, portfolio holdings, "
                    "companies, financial metrics, and stored market data in the SQLite database. "
                    "It converts natural language questions into SQL and returns tabular results."
                ),
            ),
            FunctionTool.from_defaults(
                fn=finance_market_search_tool,
                name="finance_market_search_tool",
                description=(
                    "Use this tool to retrieve current market information for supported stocks "
                    "including Apple (AAPL), Alphabet/Google (GOOGL), and Tesla (TSLA). "
                    "It is best for current prices, price changes, trading volume, and market data."
                ),
            ),
            FunctionTool.from_defaults(
                fn=pii_protection_tool,
                name="pii_protection_tool",
                description=(
                    "Use this tool to mask personally identifiable information from database "
                    "results, including names, email addresses, phone numbers, and other sensitive "
                    "customer fields while preserving non-sensitive financial data."
                ),
            ),
        ]

        for tool in self.function_tools:
            original_fn = tool.fn

            def call_as_string(*args, _original_fn=original_fn, **kwargs):
                return str(_original_fn(*args, **kwargs))

            tool.call = call_as_string
        
        if self.verbose:
            print("   ✅ Function tools created")
        
        return self.function_tools
    
    def get_tools(self):
        """Get all function tools
        
        Returns:
            List of FunctionTool objects
        """
        return self.function_tools
