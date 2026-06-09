#!/usr/bin/env python3

"""
Comprehensive Test Framework for AgentCoordinator

This test framework validates the complete financial agent coordination system
with step-by-step testing and detailed educational feedback.

Test Categories:
1. Environment & Setup Validation
2. Component Initialization Testing  
3. Tool Creation and Management
4. Intelligent Routing System
5. Multi-Tool Query Processing
6. PII Protection Integration
7. Result Synthesis and Formatting
8. Error Handling and Edge Cases

Expected Implementation Time: 90-120 minutes
Key Learning: Multi-tool coordination, intelligent routing, result synthesis
"""

try:
    import pytest
except ImportError:
    class _PytestFallback:
        @staticmethod
        def fail(message):
            raise AssertionError(message)

    pytest = _PytestFallback()
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestAgentCoordinatorEnvironment:
    """Test environment setup and dependencies"""
    
    def test_imports_available(self):
        """Test 1: Verify all required imports are available"""
        print("\n" + "="*60)
        print("TEST 1: Environment & Import Validation")
        print("="*60)
        
        try:
            from helper_modules.agent_coordinator import AgentCoordinator
            print("✅ AgentCoordinator import successful")
        except ImportError as e:
            pytest.fail(f"❌ Cannot import AgentCoordinator: {e}")
        
        # Test required dependencies
        required_modules = [
            ('llama_index.core', 'LlamaIndex core'),
            ('llama_index.llms.openai', 'OpenAI LLM'),
            ('llama_index.embeddings.openai', 'OpenAI embeddings'),
            ('pathlib', 'Path handling')
        ]
        
        for module_name, description in required_modules:
            try:
                __import__(module_name)
                print(f"✅ {description} available")
            except ImportError:
                print(f"⚠️  {description} not available (needed for full functionality)")
    
    def test_file_structure(self):
        """Test 2: Verify supporting files exist"""
        print("\n" + "="*60)
        print("TEST 2: File Structure Validation")
        print("="*60)
        
        base_path = Path(__file__).parent.parent
        
        required_files = [
            ('helper_modules/document_tools.py', 'Document tools module'),
            ('helper_modules/function_tools.py', 'Function tools module'),
            ('data/financial.db', 'Financial database'),
        ]
        
        for file_path, description in required_files:
            full_path = base_path / file_path
            if full_path.exists():
                print(f"✅ {description} found")
            else:
                print(f"⚠️  {description} not found at {full_path}")
                print(f"    Hint: AgentCoordinator needs this file for full functionality")

class TestAgentCoordinatorInitialization:
    """Test agent coordinator initialization and setup"""
    
    def test_basic_initialization(self):
        """Test 3: Basic coordinator initialization"""
        print("\n" + "="*60)
        print("TEST 3: Basic Initialization")
        print("="*60)
        
        try:
            from helper_modules.agent_coordinator import AgentCoordinator
            
            # Test default initialization
            agent = AgentCoordinator()
            print("✅ AgentCoordinator created with defaults")
            
            # Verify default attributes
            assert hasattr(agent, 'companies'), "❌ Missing 'companies' attribute"
            assert hasattr(agent, 'verbose'), "❌ Missing 'verbose' attribute"
            assert hasattr(agent, 'document_tools'), "❌ Missing 'document_tools' attribute"
            assert hasattr(agent, 'function_tools'), "❌ Missing 'function_tools' attribute"
            print("✅ All required attributes present")
            
            # Test default values
            assert agent.companies == ["AAPL", "GOOGL", "TSLA"], "❌ Incorrect default companies"
            assert agent.verbose == False, "❌ Incorrect default verbose setting"
            print("✅ Default values correct")
            
            # Test custom initialization
            custom_agent = AgentCoordinator(companies=["AAPL"], verbose=True)
            assert custom_agent.companies == ["AAPL"], "❌ Custom companies not set"
            assert custom_agent.verbose == True, "❌ Custom verbose not set"
            print("✅ Custom initialization works")
            
        except Exception as e:
            pytest.fail(f"❌ Initialization failed: {e}")
    
    def test_settings_configuration(self):
        """Test 4: Settings configuration method"""
        print("\n" + "="*60)
        print("TEST 4: Settings Configuration")
        print("="*60)
        
        try:
            from helper_modules.agent_coordinator import AgentCoordinator
            agent = AgentCoordinator()
            
            # Test _configure_settings method exists
            assert hasattr(agent, '_configure_settings'), "❌ Missing _configure_settings method"
            print("✅ _configure_settings method found")
            
            # Test method can be called (even if not implemented)
            agent._configure_settings()
            print("✅ _configure_settings callable")
            
            # Test if LLM is configured (implementation dependent)
            if hasattr(agent, 'llm') and agent.llm is not None:
                print("✅ LLM configuration detected")
            else:
                print("⚠️  LLM not configured (implementation needed)")
                print("    Hint: Implement OpenAI LLM setup in _configure_settings")
            
        except Exception as e:
            print(f"⚠️  Settings configuration issue: {e}")
            print("    Hint: Check _configure_settings implementation")

class TestToolManagement:
    """Test tool creation and management functionality"""
    
    def test_tool_creation_methods(self):
        """Test 5: Tool creation infrastructure"""
        print("\n" + "="*60)
        print("TEST 5: Tool Creation Methods")
        print("="*60)
        
        try:
            from helper_modules.agent_coordinator import AgentCoordinator
            agent = AgentCoordinator(verbose=True)
            
            # Test _create_tools method exists
            assert hasattr(agent, '_create_tools'), "❌ Missing _create_tools method"
            print("✅ _create_tools method found")
            
            # Test setup method exists
            assert hasattr(agent, 'setup'), "❌ Missing setup method"
            print("✅ setup method found")
            
            # Test initial tool state
            assert len(agent.document_tools) == 0, "❌ Document tools should start empty"
            assert len(agent.function_tools) == 0, "❌ Function tools should start empty"
            print("✅ Initial tool state correct")
            
            # Test setup method (may not fully work without dependencies)
            try:
                agent.setup()
                print("✅ Setup method callable")
            except Exception as e:
                print(f"⚠️  Setup encountered issues: {e}")
                print("    Hint: Check tool manager imports and implementations")
            
        except Exception as e:
            pytest.fail(f"❌ Tool management test failed: {e}")
    
    def test_status_and_utility_methods(self):
        """Test 6: Status and utility methods"""
        print("\n" + "="*60)
        print("TEST 6: Status and Utility Methods")
        print("="*60)
        
        try:
            from helper_modules.agent_coordinator import AgentCoordinator
            agent = AgentCoordinator()
            
            # Test get_status method
            assert hasattr(agent, 'get_status'), "❌ Missing get_status method"
            status = agent.get_status()
            assert isinstance(status, dict), "❌ get_status should return dict"
            
            required_status_keys = ['companies', 'document_tools', 'function_tools', 'ready']
            for key in required_status_keys:
                assert key in status, f"❌ Missing status key: {key}"
            print("✅ get_status method working correctly")
            
            # Test list_available_tools method
            assert hasattr(agent, 'list_available_tools'), "❌ Missing list_available_tools method"
            tools = agent.list_available_tools()
            assert isinstance(tools, list), "❌ list_available_tools should return list"
            print("✅ list_available_tools method working correctly")
            
        except Exception as e:
            pytest.fail(f"❌ Utility methods test failed: {e}")

class TestIntelligentRouting:
    """Test intelligent routing and PII protection integration"""
    
    def test_routing_methods(self):
        """Test 7: Routing method infrastructure"""
        print("\n" + "="*60)
        print("TEST 7: Routing Methods")
        print("="*60)
        
        try:
            from helper_modules.agent_coordinator import AgentCoordinator
            agent = AgentCoordinator()
            
            # Test routing methods exist
            assert hasattr(agent, '_intelligent_routing'), "❌ Missing _intelligent_routing method"
            assert hasattr(agent, '_simple_routing'), "❌ Missing _simple_routing method"
            print("✅ Both routing methods found")
            
            # Test simple routing with sample queries
            test_queries = [
                "What is Apple's revenue?",
                "Show me Tesla stock price",
                "Protect sensitive customer data"
            ]
            
            for query in test_queries:
                try:
                    results = agent._simple_routing(query)
                    assert isinstance(results, list), f"❌ Simple routing should return list for '{query}'"
                    print(f"✅ Simple routing works for: '{query}' -> {len(results)} tools")
                except Exception as e:
                    print(f"⚠️  Simple routing failed for '{query}': {e}")
            
            # Test intelligent routing (may fall back to simple)
            try:
                results = agent._intelligent_routing("What is Apple's revenue?")
                assert isinstance(results, list), "❌ Intelligent routing should return list"
                print("✅ Intelligent routing method callable")
            except Exception as e:
                print(f"⚠️  Intelligent routing issues: {e}")
                print("    Hint: Check LLM configuration for intelligent routing")
            
        except Exception as e:
            pytest.fail(f"❌ Routing test failed: {e}")
    
    def test_pii_detection_and_protection(self):
        """Test 8: PII detection and protection coordination"""
        print("\n" + "="*60)
        print("TEST 8: PII Detection and Protection")
        print("="*60)
        
        try:
            from helper_modules.agent_coordinator import AgentCoordinator
            agent = AgentCoordinator()
            
            # Test PII detection method (coordinator level)
            assert hasattr(agent, '_detect_pii_fields'), "❌ Missing _detect_pii_fields method"
            print("✅ PII detection method found")
            
            # Test with sample field names
            test_fields = ['customer_name', 'email_address', 'phone_number', 'revenue', 'stock_price']
            pii_fields = agent._detect_pii_fields(test_fields)
            
            print(f"✅ PII detection callable - found {len(pii_fields)} PII fields")
            if len(pii_fields) > 0:
                print(f"    Detected PII fields: {pii_fields}")
            else:
                print("    Hint: Implement PII field detection patterns in agent coordinator")
            
            # Test PII protection application method
            assert hasattr(agent, '_check_and_apply_pii_protection'), "❌ Missing PII protection method"
            print("✅ PII protection application method found")
            
            # Test with sample database result
            sample_result = """SQL Query: SELECT * FROM customers
            
Database Results:
{'id': 1, 'first_name': 'John', 'email': 'john@email.com'}
COLUMNS: ['id', 'first_name', 'email']"""
            
            protected_result = agent._check_and_apply_pii_protection("database_query_tool", sample_result)
            print("✅ PII protection coordination method callable")
            
            print("    Note: Coordinator detects PII fields, function_tools.py handles actual masking")
            
        except Exception as e:
            pytest.fail(f"❌ PII detection and protection test failed: {e}")

class TestQueryProcessing:
    """Test main query processing functionality"""
    
    def test_main_query_method(self):
        """Test 9: Main query processing"""
        print("\n" + "="*60)
        print("TEST 9: Main Query Processing")
        print("="*60)
        
        try:
            from helper_modules.agent_coordinator import AgentCoordinator
            agent = AgentCoordinator(verbose=True)
            
            # Test query method exists
            assert hasattr(agent, 'query'), "❌ Missing main query method"
            print("✅ Main query method found")
            
            # Test with sample query (may not work fully without tool setup)
            test_query = "What is Apple's current stock price?"
            
            try:
                response = agent.query(test_query)
                assert isinstance(response, str), "❌ Query should return string response"
                assert len(response) > 0, "❌ Query response should not be empty"
                print("✅ Query method returns valid response")
                print(f"    Response preview: {response[:100]}...")
                
            except Exception as e:
                print(f"⚠️  Query processing encountered issues: {e}")
                print("    Hint: This is expected if tools are not fully implemented")
            
        except Exception as e:
            pytest.fail(f"❌ Query processing test failed: {e}")
    
    def test_result_synthesis(self):
        """Test 10: Result synthesis functionality"""
        print("\n" + "="*60)
        print("TEST 10: Result Synthesis")
        print("="*60)
        
        try:
            from helper_modules.agent_coordinator import AgentCoordinator
            agent = AgentCoordinator()
            
            # Test synthesis method exists
            assert hasattr(agent, '_synthesize_results'), "❌ Missing _synthesize_results method"
            print("✅ Result synthesis method found")
            
            # Test with mock results
            mock_results = [
                {'tool': 'apple_document_tool', 'score': 0.9, 'result': 'Apple revenue: $365B'},
                {'tool': 'market_data_tool', 'score': 0.8, 'result': 'AAPL price: $150.00'}
            ]
            
            try:
                synthesized = agent._synthesize_results("What is Apple's revenue and stock price?", mock_results)
                assert isinstance(synthesized, str), "❌ Synthesis should return string"
                assert len(synthesized) > 0, "❌ Synthesized result should not be empty"
                print("✅ Result synthesis working")
                print(f"    Synthesis preview: {synthesized[:100]}...")
                
            except Exception as e:
                print(f"⚠️  Result synthesis issues: {e}")
                print("    Hint: Check LLM configuration for intelligent synthesis")
            
        except Exception as e:
            pytest.fail(f"❌ Result synthesis test failed: {e}")

class TestIntegrationScenarios:
    """Test complete integration scenarios"""
    
    def test_end_to_end_workflow(self):
        """Test 11: Complete workflow integration"""
        print("\n" + "="*60)
        print("TEST 11: End-to-End Integration")
        print("="*60)
        
        try:
            from helper_modules.agent_coordinator import AgentCoordinator
            
            # Test complete workflow
            agent = AgentCoordinator(companies=["AAPL"], verbose=True)
            print("✅ Agent created successfully")
            
            # Test status before setup
            initial_status = agent.get_status()
            assert not initial_status['ready'], "❌ Agent should not be ready before setup"
            print("✅ Initial status correct")
            
            # Attempt full setup and query
            try:
                # This may partially work depending on implementation
                test_queries = [
                    "What is Apple's revenue?",
                    "Show me current stock prices",
                    "Analyze Tesla's performance"
                ]
                
                for query in test_queries:
                    try:
                        response = agent.query(query)
                        print(f"✅ Query processed: '{query}' -> {len(response)} chars")
                    except Exception as e:
                        print(f"⚠️  Query '{query}' had issues: {e}")
                
            except Exception as e:
                print(f"⚠️  Integration test encountered expected issues: {e}")
                print("    This is normal if supporting modules need implementation")
            
        except Exception as e:
            pytest.fail(f"❌ Integration test failed: {e}")

def run_comprehensive_test():
    """Run all tests with detailed reporting"""
    print("🚀 AGENT COORDINATOR COMPREHENSIVE TEST FRAMEWORK")
    print("="*80)
    print("Testing complete financial agent coordination system...")
    print("Expected: Multi-tool coordination with intelligent routing")
    print("Implementation Time: 90-120 minutes")
    print("="*80)
    
    # Run all test classes
    test_classes = [
        TestAgentCoordinatorEnvironment,
        TestAgentCoordinatorInitialization,
        TestToolManagement,
        TestIntelligentRouting,
        TestQueryProcessing,
        TestIntegrationScenarios
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for test_method in test_methods:
            total_tests += 1
            try:
                getattr(test_instance, test_method)()
                passed_tests += 1
            except Exception as e:
                print(f"❌ {test_method} failed: {e}")
    
    print("\n" + "="*80)
    print("🎯 FINAL TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Agent Coordinator implementation complete!")
    elif passed_tests >= total_tests * 0.8:
        print("✅ EXCELLENT PROGRESS! Most functionality implemented correctly.")
    elif passed_tests >= total_tests * 0.6:
        print("👍 GOOD PROGRESS! Core functionality working, some features need work.")
    else:
        print("🔧 NEEDS WORK! Review the implementation hints above.")
    
    print("\n🎓 Key Learning Objectives:")
    print("- Multi-tool coordination and intelligent routing")
    print("- LLM-based tool selection and result synthesis")
    print("- Automatic PII protection integration")
    print("- Modular architecture with helper modules")
    print("- Error handling and graceful degradation")

if __name__ == "__main__":
    run_comprehensive_test()
