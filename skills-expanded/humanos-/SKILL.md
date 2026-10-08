# HumanOS Core Engine Rules & Context Gate

You are working on **HumanOS** - the core psychological and pedagogical engine powering the CHISG ecosystem.

## 0. DOCUMENTATION SEARCH (Weaviate Knowledge Base)
*   **CAPABILITY**: All project documentation, CVs, job applications, and corporate docs are indexed in Weaviate.
*   **HOW TO SEARCH**: Run from `/Users/michaelstewart/Coding/humanOS/scripts/`:
    ```bash
    source .venv/bin/activate && python search_docs.py "your query" -c
    ```
*   **INTERACTIVE MODE**: `python search_docs.py -i` for continuous searching
*   **FILTER BY PROJECT**: `python search_docs.py "query" -p humanOS`
*   **DATABASE**: Weaviate on localhost:8081, class `Documentation`
*   **RE-INGEST**: Run `python ingest_docs.py` to refresh after adding new docs

## 1. Project Identity (Safe Hands)
- **Primary Goal**: Core ETP (Emotional Trigger Point) framework and CHISG knowledge graph engine.
- **Key Audience**: Internal services (LAOMobile, Skills Map, Coach).
- **Core Technology**: Go (API), Weaviate (Vector DB), React (Frontend).
- **Relationship**: Provides the "Smart Minds" reasoning layer for all other projects.

## 2. Core Concepts
- **ETP Framework**: Emotional Trigger Points define the "terrain" of learning barriers.
- **CHISG**: Curriculum Intelligence graph for knowledge claims and semantic links.
- **Recursive Mastery**: Stimulus → ETP → Skill → Behaviour logic chain.

## 3. Strict Logical Boundaries
- **NO CURRICULUM CONTENT**: Actual lessons/content belong in LAOMobile or assist.
- **NO STUDENT-FACING UI**: This is the engine, not the front-end product.
- **SHARED LOGIC ONLY**: Focus on reusable psychological/pedagogical frameworks.

## 4. Architectural Standards
- **Safe Hands**: Deterministic APIs, type safety, validated data.
- **Smart Minds**: LLM integration, semantic search, knowledge graph queries.
- All code must be idiomatic Go for the backend.
