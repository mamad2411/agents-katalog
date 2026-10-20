<!--
  Summarized AGENTS.md for Sentra Brain

  This file contains the essential guidance for coding agents working on
  the Sentra Brain monorepo.  It focuses on useful information: the
  overall architecture, key verticals, monorepo structure, build
  commands, code style guidelines, testing practices, pull request
  conventions and high-level automation considerations.  Extraneous
  commentary and deep implementation details have been removed.

  See the full AGENTS.md for more context and examples.
-->

# Sentra Brain – Essential Agent Guide

## Overview

Sentra Brain is a **private, modular AI server** for SMEs requiring
full control over their data and AI infrastructure.
It combines a local LLM serving engine (llama.cpp or vLLM), a private
RAG engine (ChromaDB/Qdrant), an MCP integration layer and web UIs for
administration and chat.  Data and computation
remain on‑premises to meet GDPR, HIPAA and similar regulations.

### Supported sectors and use cases

| Sector                  | Key uses:contentReference[oaicite:3]{index=3}:contentReference[oaicite:4]{index=4} |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Accounting & Admin     | Automate tax filings (303, 111, 130, 190), payroll drafts, invoice extraction, form pre‑fill and agency communications with on‑prem control:contentReference[oaicite:5]{index=5}. |
| Law Firms             | Compare and draft legal documents, find similar contracts, search jurisprudence and local folders, summarise case files:contentReference[oaicite:6]{index=6}. |
| Financial Agencies     | Analyse financial reports, create incorporation checklists, fetch client data from platforms like Holded, summarise invoices, draft employment contracts and lookup aids, regulations and social security procedures:contentReference[oaicite:7]{index=7}. |
| Industrial SMEs        | Customer‑support FAQ assistant and search of local technical manuals:contentReference[oaicite:8]{index=8}. |
| Healthcare             | Fill medical certificates, check medication interactions, answer patient FAQs and summarise medical reports:contentReference[oaicite:9]{index=9}:contentReference[oaicite:10]{index=10}. |
| Public sector & other  | Automate requests, generate meeting summaries and verify documents with vendor‑independent, on‑prem AI (detailed in internal docs). |

## Monorepo structure (high‑level)

| Directory/Service         | Purpose |
|--------------------------|---------|
| `core/sentra-core`       | Domain entities, repositories and services for core data (users, conversations, documents). |
| `core/sentra-engine`     | Adapters and orchestrators for LLM serving, planning and context management. |
| `core/sentra-rag`        | RAG base library: embeddings, vector store abstractions and RAG service. |
| `services/sentra-api`    | Main API gateway exposing REST endpoints; orchestrates core calls; integrates with Postgres, MongoDB, RabbitMQ and the vector DB. |
| `services/sentra-mcp`    | Model Context Protocol server; centralises access to external tools and long‑running operations. |
| `services/sentra-rag-*`  | Microservices for vector search (`server`) and document ingestion (`worker`). |
| `frontends/sentra-admin` | React/TypeScript admin panel: dashboards, settings, logs and dataset management. |
| `frontends/sentra-web`   | End‑user chat interface with multiple modes and context selection. |
| `deploy`                 | Docker compose files and monitoring config. |
| `docs` / `dev-docs`      | Technical documentation, ADRs and internal guides. |

## Setup and development

1. **Clone and prepare**
   ```bash
   git clone git@github.com:jgccon/sentra-brain.git
   cd sentra-brain
