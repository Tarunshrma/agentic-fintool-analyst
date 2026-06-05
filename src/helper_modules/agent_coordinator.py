"""
Agent Coordinator Module - Complete Financial Agent with Modular Architecture

This module provides the complete financial agent functionality with intelligent routing,
tool coordination, and backward compatibility. It replaces both modern_financial_agent.py
and financial_agent.py by providing all functionality in a single coordinated system.

Learning Objectives:
- Understand multi-tool coordination and intelligent routing
- Implement LLM-based decision making for tool selection
- Learn result synthesis from multiple data sources
- Build modular agent architecture
- Master PII protection in agent workflows

Your Task: Complete the missing implementations marked with YOUR CODE HERE

Key Features:
- Multi-tool coordination with intelligent routing
- Document analysis (10-K filings) for Apple, Google, Tesla
- Database queries with SQL auto-generation and PII protection
- Real-time market data from Yahoo Finance
- Complete backward compatibility for existing notebooks
- Modular architecture using helper modules
"""

import os
import logging
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path

# LlamaIndex imports
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Environment setup
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class AgentCoordinator:
    """
    Complete Financial Agent with Dynamic Multi-Tool Coordination
    
    This class combines the functionality of the original modern_financial_agent.py
    and financial_agent.py into a single coordinated system using modular architecture.
    
    Architecture:
    - Document Tools (3): Individual SEC 10-K filing analysis for Apple, Google, Tesla
    - Function Tools (3): Database SQL queries, real-time market data, PII protection
    - Intelligent Routing: LLM-based tool selection and result synthesis
    - Backward Compatibility: Works with existing notebooks and code
    """
    
    def __init__(self, companies: List[str] = None, verbose: bool = False):
        """
        Initialize the complete financial agent with modular architecture.
        
        Args:
            companies: List of company symbols (default: ["AAPL", "GOOGL", "TSLA"])
            verbose: Whether to show detailed operation information
        """
        self.companies = companies if companies is not None else ["AAPL", "GOOGL", "TSLA"]
        self.verbose = verbose
        self.project_root = Path.cwd()  # Use current working directory
        
        # Company metadata
        self.company_info = {
            "AAPL": {"name": "Apple Inc.", "sector": "Technology"},
            "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology"},
            "TSLA": {"name": "Tesla Inc.", "sector": "Automotive"}
        }
        
        # Storage for tools and engines
        self.document_tools = []
        self.function_tools = []
        self.llm = None
    
        
        self._configure_settings()
        
        # Don't auto-initialize tools - create them lazily when first needed
        self._tools_initialized = False
        
        if self.verbose:
            print("✅ Financial Agent Coordinator Initialized")
            print(f"   Companies: {self.companies}")
            print(f"   Tools will be created automatically when first query is made")
    
  
    def _configure_settings(self):
        """Configure LlamaIndex settings with Vocareum API compatibility
        
        TODO: Set up the LLM and embedding model for intelligent routing
        
        Requirements:
        - Create OpenAI LLM with "gpt-3.5-turbo" model and temperature=0
        - Create OpenAIEmbedding with "text-embedding-ada-002" model
        - Use api_base parameter for Vocareum API compatibility (both models)
        - Set Settings.llm and Settings.embed_model
        - Store LLM reference in self.llm for routing decisions
        
        IMPORTANT NOTE FOR VOCAREUM:
        LlamaIndex requires the api_base parameter to work with Vocareum's OpenAI endpoint.
        Get the base URL from environment: os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")
        Pass it as api_base parameter to both OpenAI() and OpenAIEmbedding() constructors.
        """
        # YOUR CODE HERE
        pass
    
    
    def setup(self, document_tools: List = None, function_tools: List = None):
        """
        Setup all components using the modular architecture.
        
        Args:
            document_tools: Optional pre-created document tools
            function_tools: Optional pre-created function tools
            
        This method initializes all tools and sets up the routing system.
        If tools are not provided, they will be created automatically.
        """
        if self.verbose:
            print("🔧 Setting up Advanced Financial Agent (Modular Architecture)...")
        
        try:
            if document_tools is not None and function_tools is not None:
                # Use provided tools
                self.document_tools = document_tools
                self.function_tools = function_tools
            else:
                # Create tools automatically
                self._create_tools()
            
            if self.verbose:
                status = self.get_status()
                print(f"✅ Setup complete: {status['document_tools']} document tools, {status['function_tools']} function tools")
                print(f"🎯 System ready: {'✅' if status['ready'] else '❌'}")
                
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            if self.verbose:
                print(f"❌ Setup failed: {e}")
    
    def _create_tools(self):
        """Create all tools automatically using helper modules
        
        TODO: Import and use the DocumentToolsManager and FunctionToolsManager
        to create all necessary tools for the coordinator.
        
        Steps:
        1. Import DocumentToolsManager from .document_tools
        2. Import FunctionToolsManager from .function_tools
        3. Create instances and call their build methods
        4. Store results in self.document_tools and self.function_tools
        """
        # YOUR CODE HERE
        pass
    
    def _check_and_apply_pii_protection(self, tool_name: str, result: str) -> str:
        """Check if database results need PII protection and apply it automatically
        
        This method automatically detects when database queries return sensitive information
        and applies appropriate PII protection using the PII protection tool from function_tools.
        
        Args:
            tool_name: Name of the tool that generated the result
            result: Raw result string from the tool
            
        Returns:
            Protected result string with PII masked if necessary
        """
        
        # Only apply to database query results
        if "database_query_tool" not in tool_name:
            return result
        
        # Check if result contains column information
        if "COLUMNS:" not in result:
            return result
        
        # TODO: Extract column names from result
        # Detect PII fields using _detect_pii_fields()
        # If PII detected, find and use the pii_protection_tool
        # Apply protection and return masked result
        # YOUR CODE HERE
        
        return result  # Placeholder
    
    def _detect_pii_fields(self, field_names: list) -> set:
        """Detect which fields contain PII based on field names
        
        This method identifies potentially sensitive database fields that need protection.
        
        Args:
            field_names: List of database column names
            
        Returns:
            Set of field names that contain PII
        """
        # TODO: Define PII field patterns (email, phone, names, address, ssn, etc.)
        # Check each field name against patterns
        # Return set of detected PII field names
        # YOUR CODE HERE
        
        return set()  # Placeholder
    

    def _route_query(self, query: str) -> List[Tuple[str, str, Any]]:
        """Use LLM to intelligently route query to appropriate tools
        
        This method analyzes the user's query and determines which tools are needed
        to provide a complete answer, then executes those tools and returns results.
        
        Args:
            query: User's natural language query
            
        Returns:
            List of tuples: (tool_name, tool_description, result)
        """
        
        # TODO: Build routing logic
        # 1. Create descriptions of all available tools
        # 2. Build LLM prompt with query and tool options
        # 3. Include routing guidelines (database for customers, market for prices, etc.)
        # 4. Parse LLM response to get tool indices
        # 5. Execute selected tools and collect results
        # 6. Apply PII protection to database results
        # YOUR CODE HERE
        
        return []  # Placeholder
    
    def query(self, question: str, verbose: bool = None) -> str:
        """Process query with dynamic tool routing and result synthesis
        
        This is the main entry point for the financial agent. It handles:
        1. Tool routing and selection using LLM
        2. Multi-tool execution 
        3. Result synthesis for comprehensive answers
        4. Automatic PII protection
        
        Args:
            question: User's financial question
            verbose: Whether to show detailed processing info
            
        Returns:
            Comprehensive answer synthesized from relevant tools
        """
        
        # Use instance verbose if parameter not provided
        if verbose is None:
            verbose = self.verbose
        
        # Ensure tools are initialized
        if not self._tools_initialized:
            self.setup()
            self._tools_initialized = True
        
        if verbose:
            print(f"🎯 Query: {question}")
        
        # TODO: Implement query processing workflow
        # 1. Route query to appropriate tools using _route_query()
        # 2. Display tool selection info if verbose
        # 3. If single tool result, return it directly
        # 4. If multiple tool results, synthesize using LLM
        # 5. Return comprehensive answer
        # YOUR CODE HERE
        
        return "Query method not implemented yet - complete the YOUR CODE HERE sections"
    
    def get_available_tools(self) -> Dict[str, Any]:
        """
        Get information about available tools with full compatibility.
        
        Returns:
            Dictionary with comprehensive tool information
        """
        return {
            "document_tools": ["apple", "google", "tesla"] if len(self.document_tools) >= 3 else [],
            "function_tools": ["sql", "market", "pii"] if len(self.function_tools) >= 3 else [],
            "total_tools": len(self.document_tools) + len(self.function_tools),
            "document_tool_count": len(self.document_tools),
            "function_tool_count": len(self.function_tools)
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive agent status with full compatibility.
        
        Returns:
            Dictionary with detailed status information
        """
        tool_count = len(self.document_tools) + len(self.function_tools)
        system_ready = len(self.document_tools) >= 3 and len(self.function_tools) >= 3
        
        return {
            "companies": self.companies,
            "document_tools": len(self.document_tools),
            "function_tools": len(self.function_tools),
            "total_tools": tool_count,
            "ready": system_ready,
            "architecture": "modular",
            "coordinator_ready": system_ready,
            "available_companies": ['AAPL', 'GOOGL', 'TSLA'],
            "capabilities": [
                "Document analysis (10-K filings)",
                "Database queries (customer portfolios)",
                "Real-time market data",
                "PII protection",
                "Multi-tool coordination",
                "Intelligent routing"
            ],
            "system_ready": system_ready
        }
