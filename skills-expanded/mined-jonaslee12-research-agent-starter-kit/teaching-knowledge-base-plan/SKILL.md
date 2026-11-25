---
name: teaching-knowledge-base-plan
description: Plan a teaching knowledge base for AI-agent support, including source types, metadata, RAG architecture, privacy boundaries, content governance, evaluation, and teacher-facing use cases.
---

# Teaching Knowledge Base Plan

Use when the user asks to build a teaching knowledge base, RAG system, course knowledge base, AI tutor memory, or repository of active learning resources.

## Scope

This skill plans the knowledge base. It does not install dependencies or implement a full system unless the user explicitly asks.

Use `dissertation-knowledge-ops` instead when the task is syncing, deduplicating, indexing, or deciding the source of record across `research-wiki`, `knowledge-base`, and Obsidian.

## Source Types

Consider:

- active learning literature notes
- teaching strategy guides
- course outlines
- lesson plans
- assessment rubrics
- workshop outputs
- anonymized teacher concerns and needs
- institutional guidance
- AI-agent design requirements
- prototype evaluation notes

## Workflow

1. Define users:
   - researcher
   - university teacher
   - AI agent
   - supervisor/examiner
2. Define use cases:
   - answer questions about active learning
   - suggest teaching activities
   - retrieve evidence for dissertation writing
   - support AI agent design decisions
   - compare adoption concerns across teachers
3. Specify information architecture:
   - documents
   - metadata
   - tags
   - evidence tables
   - concept pages
   - decision logs
4. Decide retrieval strategy:
   - simple Markdown wiki first
   - local search
   - vector search/RAG later
   - citations/source links required
5. Define privacy boundaries:
   - public teaching resources
   - restricted research notes
   - sensitive participant data
6. Define evaluation:
   - source citation accuracy
   - retrieval relevance
   - usefulness for teachers
   - hallucination rate
   - privacy compliance

## Output

Create or update:

- `knowledge-base/KB_PLAN.md`
- `knowledge-base/SOURCE_REGISTER.md`
- `knowledge-base/METADATA_SCHEMA.md`
- `knowledge-base/RAG_EVALUATION_PLAN.md`

## Starter Architecture

For a research-agent starter project, prefer:

1. Markdown knowledge base first.
2. Clear metadata and source registers.
3. Manual citation audit.
4. Local/private RAG only after the structure is stable.

## Guardrails

Do not mix raw participant data with general teaching resources.
Do not recommend uploading sensitive data to external services without explicit confirmation.
