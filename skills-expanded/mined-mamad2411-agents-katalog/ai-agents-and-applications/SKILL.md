---
name: ai-agents-and-applications
description: "Knowledge base from \"AI Agents and Applications With LangChain, LangGraph, and MCP\" by Roberto Infante. Use when applying the author's frameworks for LangChain, LangGraph, RAG, prompt engineering, multi-agent systems, or MCP servers, studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# AI Agents and Applications With LangChain, LangGraph, and MCP
**Author**: Roberto Infante | **Pages**: ~410 | **Chapters**: 14 (+ 5 appendices) | **Generated**: 2026-09-17

## How to Use This Skill

- **Without arguments** — load core frameworks for reference
- **With a topic** — ask about `RAG`, `tool calling`, `MCP`, or another indexed topic; I find and read the relevant chapter
- **With chapter** — ask for `ch11`, or `appendix c`; I load that specific file
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read
the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**Engines vs. chatbots vs. agents** — the book's foundational taxonomy. An *engine* is invoked, produces output, and stops (summarization, search). A *chatbot* maintains conversational context but doesn't act. An *agent* loops (observe → decide → act → observe), coordinates tools, and adapts based on intermediate results. Use this to size the right architecture before reaching for an agent framework.

**Adaptation ladder** — prompt engineering → RAG → fine-tuning, in that order of cost/complexity. Exhaust prompt engineering first, add RAG when you need grounding in data the model wasn't trained on, and only fine-tune when neither is enough.

**LCEL (LangChain Expression Language)** — compose `Runnable` steps with `|` into chains; `RunnableParallel`/`.map()` fan out work concurrently. This is the backbone of every chain in the book — summarization, RAG, research engines. Prefer LCEL composition over hand-rolled sequential Python once a pipeline stabilizes.

**Summarization: MapReduce vs. Refine** — MapReduce splits → summarizes each chunk in parallel → reduces to one summary (fast, loses cross-chunk nuance). Refine folds each document into a running summary sequentially (preserves fidelity, slower, more tokens). Use MapReduce when speed/cost matters and chunks are independent; use Refine when narrative continuity across documents matters.

**RAG design pattern** — two-stage architecture: (1) ingestion/indexing (load → split → embed → store), (2) retrieval-and-generation (embed query → retrieve → prompt with context → generate). Always instruct the model to answer only from retrieved context and say "I don't know" otherwise — the single highest-leverage hallucination guard in the book.

**Vector library vs. vector database** — libraries (FAISS-style) are fast and read-optimized but immutable once built; databases (Chroma/Pinecone-style) support full CRUD and metadata filtering. Pick a database when your corpus changes after ingestion or you need metadata filters.

**Advanced indexing (when plain RAG retrieves the wrong chunks)** — ParentDocumentRetriever (embed small child chunks, return the larger parent for context), MultiVectorRetriever (embed a summary or LLM-generated hypothetical questions instead of the raw chunk), granular chunk expansion (index small, stitch neighbors at retrieval time). Use these when relevant content is being missed or context is too fragmented, not as a default.

**Query transformation (when the user's question is the problem, not the index)** — Rewrite-Retrieve-Read (clean up a poorly-phrased query), Step-back prompting (retrieve broader context alongside the specific one), HyDE (embed a hypothetical answer instead of the question to close the semantic gap), multi-query/RRF (generate several query phrasings, fuse results), decomposition (break a compound question into sub-questions). Diagnose which failure mode you have before picking a technique — see cheatsheet.md's failure-mode table.

**LangGraph StateGraph** — model an agent as a typed state object, node functions (each returns a partial state update), and edges (linear or conditional) between an entry point and END. Use LangGraph instead of a linear LCEL chain once you need loops, conditional branching, or persistent state across steps.

**ReAct tool-calling agent** — the LLM reasons, selects a tool, observes the result, and repeats until it can answer. Prefer LangGraph's prebuilt `create_react_agent` over hand-wiring the graph once the pattern is understood — it's less code for the same behavior and keeps LangSmith tracing intact.

**Router vs. Supervisor multi-agent pattern** — Router: LLM classifies a query once and dispatches to a single specialist agent ("one-way ticket") — cheap, simple, good for clearly-separable domains. Supervisor: a coordinating agent wraps each specialist as a callable tool and can invoke several, repeatedly, within one session ("return ticket") — needed for multi-step, multi-domain requests. Give the Supervisor a stronger LLM than its specialists.

**MCP (Model Context Protocol)** — a standard host/client/server architecture so tool integrations are built once (as an MCP server) and consumed by any agent (as an MCP client), instead of every team wrapping the same API as a bespoke local tool. Reach for MCP when a capability will be reused across agents/teams; keep it a local tool when it's single-use.

**Memory & guardrails for production** — use a LangGraph checkpointer (thread_id + a saver) for resumable short-term memory and state rewinding. Layer guardrails: a cheap router-level relevance check plus a stricter agent-level `pre_model_hook`, because an agent invoked directly (bypassing the router) loses the router's protection.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction-to-ai-agents-and-applications.md) | Introduction to AI agents and applications | Engines/chatbots/agents taxonomy, LangChain architecture, adaptation ladder |
| [ch02](chapters/ch02-executing-prompts-programmatically.md) | Executing prompts programmatically | PromptTemplate, FewShotPromptTemplate, in-context learning ladder |
| [ch03](chapters/ch03-summarizing-text-using-langchain.md) | Summarizing text using LangChain | MapReduce chain, Refine strategy |
| [ch04](chapters/ch04-building-a-research-summarization-engine.md) | Building a research summarization engine | LCEL chain composition, query rewriting |
| [ch05](chapters/ch05-agentic-workflows-with-langgraph.md) | Agentic workflows with LangGraph | StateGraph, agentic workflow vs. agent |
| [ch06](chapters/ch06-rag-fundamentals-with-chromadb.md) | RAG fundamentals with ChromaDB | RAG design pattern, vector library vs. database |
| [ch07](chapters/ch07-qa-chatbots-with-langchain-and-langsmith.md) | Q&A chatbots with LangChain and LangSmith | Ingestion/retrieval-generation stages, conversational memory |
| [ch08](chapters/ch08-advanced-indexing.md) | Advanced indexing | ParentDocumentRetriever, MultiVectorRetriever |
| [ch09](chapters/ch09-question-transformations.md) | Question transformations | Rewrite-Retrieve-Read, step-back, HyDE |
| [ch10](chapters/ch10-query-generation-routing-and-retrieval-postprocessing.md) | Query generation, routing, and retrieval postprocessing | Self-querying, text-to-SQL, chain routing |
| [ch11](chapters/ch11-building-tool-based-agents-with-langgraph.md) | Building tool-based agents with LangGraph | ReAct pattern, tool calling, prebuilt agent |
| [ch12](chapters/ch12-multi-agent-systems.md) | Multi-agent systems | Router pattern, Supervisor pattern |
| [ch13](chapters/ch13-building-and-consuming-mcp-servers.md) | Building and consuming MCP servers | MCP host/client/server, FastMCP 2 |
| [ch14](chapters/ch14-productionizing-ai-agents.md) | Productionizing AI agents: Memory, guardrails, and beyond | Checkpointer, layered guardrails |
| [appA](chapters/ch15-appendix-a-trying-out-langchain.md) | Appendix A: Trying out LangChain | Environment/API-key setup |
| [appB](chapters/ch16-appendix-b-setting-up-a-jupyter-notebook-environment.md) | Appendix B: Setting up a Jupyter Notebook environment | Jupyter setup |
| [appC](chapters/ch17-appendix-c-choosing-an-llm.md) | Appendix C: Choosing an LLM | Nine-factor LLM selection checklist |
| [appD](chapters/ch18-appendix-d-installing-sqlite-on-windows.md) | Appendix D: Installing SQLite on Windows | SQLite setup |
| [appE](chapters/ch19-appendix-e-open-source-llms.md) | Appendix E: Open source LLMs | Open-source models, quantization, local inference engines |

## Topic Index

- **Advanced indexing** → ch08
- **Agentic workflows** → ch05
- **Anti-hallucination prompting** → ch06
- **Chain routing** → ch10
- **Checkpointer (LangGraph)** → ch14
- **ChromaDB** → ch06
- **Decomposition (query)** → ch09
- **FastMCP** → ch13
- **Few-shot / one-shot prompting** → ch02
- **Guardrails** → ch14
- **HyDE (Hypothetical Document Embeddings)** → ch09
- **LangGraph (StateGraph)** → ch05, ch11, ch14
- **LangSmith tracing** → ch07, ch11
- **LCEL (LangChain Expression Language)** → ch03, ch04, ch07
- **MapReduce summarization** → ch03
- **MCP (Model Context Protocol)** → ch13
- **Memory (chatbot / agent)** → ch07, ch14
- **Metadata enrichment / self-querying** → ch10
- **Multi-agent systems** → ch12
- **Multi-query retrieval** → ch09
- **ParentDocumentRetriever** → ch08
- **Prompt engineering** → ch02, ch04
- **Prompt templates** → ch02
- **Query transformations** → ch09
- **RAG (Retrieval-Augmented Generation)** → ch06, ch08, ch09, ch10
- **ReAct agent pattern** → ch11
- **Refine (summarization)** → ch03
- **Research summarization engine** → ch04
- **Router agent** → ch12
- **Selecting an LLM** → appC
- **Semantic SQL / text-to-SQL** → ch10
- **Step-back prompting** → ch09
- **Supervisor agent** → ch12
- **Tool calling** → ch11
- **Vector stores** → ch06
- **Weather MCP server** → ch13

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — quick reference tables and decision guides

---

## Scope & Limits

This skill covers the book content only. For hands-on implementation in your codebase,
combine with project-specific tools. For topics beyond this book, check related skills
or ask the agent directly.
