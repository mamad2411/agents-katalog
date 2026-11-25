---
name: 250-open-source-agents
description: Curated map of 250+ open-source AI agents organised by category — coding, research, web browsing, data, DevOps, finance, and more. Use when scoping which agent framework or reference implementation to study before building a new autonomous agent, or to discover existing agents that already solve the problem at hand. Source: @theromanknox.
---

# 250 Open Source Agents — Category Map

A community-curated reference of 250+ open-source AI agents, grouped by domain.

## Why this matters

Before building a new agent, check whether an open-source version already exists. Most capability categories have at least one battle-tested implementation worth forking or studying.

---

## Category Overview

### Coding Agents
Agents that write, review, debug, or execute code autonomously.
- **SWE-agent** — automated software engineering on real GitHub issues
- **Aider** — AI pair programmer that edits files directly via git
- **OpenHands** (OpenDevin) — full software development environment in a sandbox
- **GPT-Engineer** — scaffolds entire codebases from a spec
- **Cursor Agent** — IDE-native coding agent

### Research Agents
Agents that search, read, synthesise, and produce reports.
- **GPT-Researcher** — autonomous deep research with web search + synthesis
- **Open Deep Research** — multi-step research pipelines
- **Perplexica** — self-hosted Perplexity-style search agent

### Web Browsing Agents
Agents that navigate the web, fill forms, and extract data.
- **Browser-use** — LLM-controlled browser automation
- **Playwright Agent** — structured web task execution
- **Skyvern** — AI-driven browser automation for repetitive web tasks

### Data & Analysis Agents
Agents that query databases, analyse datasets, and produce insights.
- **Pandas AI** — natural-language DataFrame queries
- **Vanna** — natural language to SQL
- **LlamaIndex Agents** — RAG-powered Q&A over structured and unstructured data

### DevOps / Infrastructure Agents
Agents that manage deployments, monitor systems, and run ops tasks.
- **k8s-agent** — Kubernetes cluster management via natural language
- **Ansible Agent** — infrastructure automation with LLM planning

### Finance Agents
Agents that analyse markets, summarise filings, and model portfolios.
- **FinGPT** — open-source financial LLM + agent stack
- **TradingGPT** — market analysis and strategy generation

### Personal Assistants
General-purpose agents for scheduling, email, and task management.
- **AutoGPT** — one of the first autonomous agent frameworks
- **AgentGPT** — browser-based agent with persistent memory
- **Mem0** — persistent memory layer for AI assistants

### Multi-Agent Orchestration
Frameworks for coordinating multiple specialised agents.
- **CrewAI** — role-based multi-agent teams
- **AutoGen** — Microsoft's conversational multi-agent framework
- **LangGraph** — stateful agent graphs with cycles

---

## How to use this map

1. **Identify your task category** (coding, research, browsing, etc.)
2. **Check existing agents in that category** — are they a fit to fork or extend?
3. **Review the framework** — does it use the same orchestration layer (LangChain, LlamaIndex, DSPy, raw API) as your stack?
4. **Clone and run the demo** before committing to a build from scratch

Source: @theromanknox
