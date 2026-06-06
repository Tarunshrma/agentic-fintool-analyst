# Udacity FinTool Analyst Rubric Notes

Source captured from the user's Udacity screenshots in `mics/1.png` through `mics/5.png`.

## Project Goal

Build a modular financial agent system that routes user questions across document RAG, database querying, live market data, and privacy protection, then synthesizes a coherent answer.

## Required Deliverables

- `src/helper_modules/document_tools.py`
  - Complete `DocumentToolsManager`.
  - Configure LlamaIndex OpenAI LLM and embeddings with Vocareum `api_base`.
  - Build one `QueryEngineTool` per 10-K: AAPL, GOOGL, TSLA.
  - Use clear tool names and descriptions.

- `src/helper_modules/function_tools.py`
  - Complete `FunctionToolsManager`.
  - Build `database_query_tool` for natural language to SQL and SQLite execution.
  - Build `finance_market_search_tool` for Yahoo Finance market data.
  - Build `pii_protection_tool` for automatic sensitive field masking.

- `src/helper_modules/agent_coordinator.py`
  - Complete `AgentCoordinator`.
  - Initialize document and function tools from helper modules.
  - Route queries with LLM-guided decision making.
  - Apply automatic PII protection for database results with sensitive fields.
  - Synthesize multi-tool results into a comprehensive answer.

- `src/financial_agent_walkthrough.ipynb`
  - Run end to end without errors.
  - Demonstrate document analysis, database queries, market data, PII protection, and multi-tool coordination.

## Tests Mentioned By Udacity

- `python tests/test_vocareum_setup_for_llama_index.py`
- `python tests/test_document_tools.py`
- `python tests/test_function_tools.py`
- `python tests/test_agent_coordinator.py`
- Run the full notebook: `jupyter notebook financial_agent_walkthrough.ipynb`

## Rubric Highlights

- No placeholder code remains: no `YOUR CODE HERE`, `pass`, or "not implemented" behavior in required paths.
- LlamaIndex setup uses:
  - LLM model: `gpt-3.5-turbo`
  - Embedding model: `text-embedding-ada-002`
  - `api_base=os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")`
- Document tools must load all three PDF filings, create indexes, expose query engines, and answer company-specific questions.
- Database tool must generate valid single-statement `SELECT` SQL, execute safely, include column names, handle joins, and retry or explain failures.
- Market tool must retrieve AAPL, GOOGL, and TSLA data and degrade gracefully if live API access fails.
- PII tool must mask names, emails, phone numbers, and other sensitive fields while leaving non-PII readable.
- Coordinator must select single or multiple tools depending on query needs, avoid unnecessary PII processing, and synthesize results from documents, database, and market data.
- Code should remain modular, maintainable, documented where helpful, and robust to errors.

## TradeFi Reuse Lens

The transferable architecture for `tradefi.network` is:

- Document RAG: issuer memos, offering docs, regulatory filings, pool documents.
- Database tool: issuer, asset, pool, investor, transaction, NAV, subscription, redemption, and compliance tables.
- Market/API tool: TradeFi issuer APIs, XDC on-chain data, FX, benchmark rates, tokenized fund data.
- PII protection: investor/KYC fields, subscription records, wallet mappings, emails, phone numbers, account identifiers.
- Coordinator: routes questions across disclosure documents, internal databases, and live APIs while protecting sensitive data.
