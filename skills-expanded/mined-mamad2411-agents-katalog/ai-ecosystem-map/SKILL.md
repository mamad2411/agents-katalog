---
name: ai-ecosystem-map
description: Reference directory of the modern AI tooling ecosystem — organized by layer (LLM, Agentic AI, RAG, Embedding, MCP, AI Security, Observability, Memory, AI Agent, Automation, Vector Database) with the key tools in each category. Use when the user is choosing tools for an AI project, wants to understand what exists in a specific layer, or needs to know which tools compete/complement each other. Source: @rathanuday "The Modern AI Ecosystem - Tools" (2026).
---

# Modern AI Ecosystem — Tool Reference Map

Source: @rathanuday "The Modern AI Ecosystem - Tools" (2026 edition).

> The full stack of tools for building AI systems, organized by layer.

## The layers

---

### LLM — Foundation Models

The models that do the thinking.

| Provider | Model family |
|---|---|
| OpenAI | GPT series |
| Anthropic | Claude (Haiku, Sonnet, Opus, Fable) |
| Google | Gemini |
| Meta | Llama (open-weight) |
| Mistral AI | Mistral, Mixtral |
| Cohere | Command series |
| Hugging Face | Model hub (hosts all open-weight models) |
| Ollama | Local LLM runtime (run any open-weight model locally) |
| vLLM | High-throughput LLM serving (self-hosted) |

---

### Agentic AI — Multi-Agent Frameworks

Orchestrate multiple LLMs or tool-using agents working together.

| Tool | What it does |
|---|---|
| LangGraph | Stateful multi-agent graphs; cycles and branches |
| CrewAI | Role-based agent teams with task delegation |
| Microsoft AutoGen | Conversational multi-agent framework |
| Microsoft Agent Framework | Enterprise agent orchestration |
| LlamaIndex Workflows | Event-driven agent pipelines |
| AWS Strands Agents | AWS-native agentic SDK |
| CAMEL | Communicative agent framework for roleplay/research |
| Agno | Lightweight agent framework |

---

### RAG — Retrieval-Augmented Generation

Ground LLM outputs in your own data.

| Tool | What it does |
|---|---|
| LangChain | Most popular RAG pipeline framework |
| LlamaIndex | Document ingestion and retrieval pipelines |
| Haystack | Production RAG with evaluation built in |
| DSPy | Programmatic prompt optimization for RAG |
| RAGFlow | Open-source RAG with document parsing |
| GraphRAG | Knowledge graph-based RAG (Microsoft) |
| Unstructured | Document parsing and chunking |
| EmbedChain | Simple RAG on top of any data source |

---

### Embedding — Vector Representations

Turn text into vectors for semantic search and retrieval.

| Tool | What it does |
|---|---|
| OpenAI Embeddings | text-embedding-3-small / large |
| Cohere Embed | Multilingual embedding models |
| Voyage AI | High-quality retrieval-optimized embeddings |
| Sentence Transformers | Open-source, local embedding models |
| BGE | BAAI general embedding models (open-source) |
| Google Vertex AI Embeddings | GCP-native embedding API |
| Azure OpenAI Embeddings | Azure-hosted OpenAI embedding models |

---

### MCP — Model Context Protocol

Connect AI models to external tools and data sources via a standard protocol (Anthropic's "USB-C for AI").

| Tool | What it does |
|---|---|
| MCP SDK | Official SDK for building MCP servers |
| FastMCP | Fast MCP server framework |
| MCP Registry | Directory of available MCP servers |
| GitHub MCP Server | Connect Claude to GitHub repos |
| Slack MCP Server | Connect Claude to Slack workspaces |
| PostgreSQL MCP Server | Connect Claude to Postgres databases |
| Google Drive MCP Server | Connect Claude to Google Drive |
| Filesystem MCP Server | Connect Claude to local/remote filesystems |

---

### AI Security — Guardrails & Safety

Control what AI models can say and do.

| Tool | What it does |
|---|---|
| NVIDIA NeMo Guardrails | Topical, safety, and dialog rails |
| Guardrails AI | Input/output validation for LLMs |
| Microsoft Presidio | PII detection and anonymization |
| Lakera Guard | Real-time prompt injection detection |
| Prompt Security | Enterprise prompt firewall |
| Protect AI | AI security platform (model scanning) |
| Azure Content Safety | Microsoft's content moderation API |
| AWS Bedrock Guardrails | AWS-native LLM safety controls |

---

### Observability — Monitoring & Tracing

See what your AI is doing and why.

| Tool | What it does |
|---|---|
| LangSmith | LangChain-native tracing and evaluation |
| Langfuse | Open-source LLM observability |
| Arize Phoenix | ML observability with LLM support |
| Weights & Biases (Weave) | Experiment tracking + LLM tracing |
| TruLens | RAG evaluation and tracing |
| Ragas | RAG evaluation framework |
| Promptfoo | Prompt testing and red-teaming |
| Helicone | LLM API proxy with logging |

---

### Memory — Persistent State for Agents

Give AI systems the ability to remember across sessions.

| Tool | What it does |
|---|---|
| Mem0 | Personal AI memory layer |
| Zep | Long-term memory for AI assistants |
| Letta | Stateful AI agents with memory |
| LangGraph Memory | Memory module for LangGraph agents |
| Redis | In-memory key-value store (fast session memory) |
| PostgreSQL | Relational memory with complex queries |
| Neo4j | Graph database for knowledge-graph memory |
| Chroma | Lightweight vector DB (also used for memory) |

---

### AI Agent — Agent SDKs & Frameworks

Build individual AI agents with tool use and reasoning.

| Tool | What it does |
|---|---|
| OpenAI Agents SDK | OpenAI's official agent framework |
| LangChain Agents | ReAct and tool-using agents via LangChain |
| PydanticAI | Type-safe agent framework (Python) |
| Semantic Kernel | Microsoft's AI orchestration SDK (.NET/Python) |
| Google ADK | Google's Agent Development Kit |
| AWS Bedrock Agents | Managed agents on AWS Bedrock |
| Azure AI Foundry Agent Service | Azure-hosted managed agents |

---

### Automation — Workflow Orchestration

Trigger AI tasks and connect them to business systems.

| Tool | What it does |
|---|---|
| n8n | Open-source workflow automation (self-hostable) |
| Zapier | No-code automation, 7,000+ app integrations |
| Make (formerly Integromat) | Visual workflow automation |
| Microsoft Power Automate | Enterprise automation in the Microsoft stack |
| Temporal | Durable workflow orchestration for developers |
| Apache Airflow | Python-based DAG orchestration |
| Prefect | Modern Python workflow orchestration |
| Kestra | Declarative workflow orchestration (YAML) |
| Pipedream | Code-first automation platform |

---

### Vector Database — Semantic Storage

Store and query vector embeddings at scale.

| Tool | What it does |
|---|---|
| Pinecone | Managed vector DB, production-scale |
| Weaviate | Open-source vector DB with GraphQL |
| Qdrant | High-performance open-source vector DB |
| Milvus | Distributed open-source vector DB |
| Chroma | Lightweight local/hosted vector DB |
| pgvector | Vector search extension for PostgreSQL |
| Elasticsearch | Search engine with vector search support |
| Redis (vector) | Vector search via RediSearch module |
| MongoDB Atlas Vector Search | Vector search in MongoDB |

---

## Choosing tools by use case

| If you're building… | Start with |
|---|---|
| A chatbot on your docs | LlamaIndex + Chroma + Claude |
| A multi-step AI agent | LangGraph or CrewAI + any LLM |
| A local AI app (no cloud) | Ollama + Chroma + n8n |
| A production RAG pipeline | LangChain + Pinecone + LangSmith |
| An MCP server | MCP SDK + FastMCP |
| An enterprise AI system | Azure/AWS managed services tier |
| A SaaS MVP (fast) | Supabase + Next.js + Claude API (see `saas-mvp-24h`) |

## Related skills

- **saas-mvp-24h**: Build stack for a 24-hour SaaS MVP — draws from the Automation and Agent layers
- **n8n-agent-builder**: Deep dive into n8n specifically
- **open-source-devtools-2026**: Developer tooling layer (database workspaces, API testing, etc.)
- **mcp-builder**: Build your own MCP server (if that skill exists)
- **claude-api**: Claude API reference for building on the Anthropic layer
