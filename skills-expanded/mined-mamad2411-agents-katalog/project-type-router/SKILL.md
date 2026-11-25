---
name: project-type-router
description: Routes any project description to the correct technology stack and skill chain
---

# Project Type Router

## Project Types

### Type 1: Web Application (Full-Stack)
Stack: Next.js 15 + FastAPI/tRPC + Supabase + TypeScript strict
Chain: brainstorming → ultrathinking → ultraplanning → architect → project-bootstrap → tdd → e2e-runner → security-reviewer → deployment

### Type 2: REST API / Backend Service
Stack: FastAPI (Python) or Hono (TypeScript) + PostgreSQL/Supabase
Chain: api-design → ultraplanning → architect → project-bootstrap → tdd → database-reviewer → security-reviewer → deployment

### Type 3: AI / LLM System
Stack: Python + FastAPI + LiteLLM + LangGraph/CrewAI + pgvector + Langfuse
Chain: ultrathinking → ai-engineering → prompt-engineering → architect → project-bootstrap → tdd → write-tests (eval suite) → security-reviewer → deployment

### Type 4: CLI Tool
Stack: Python + Typer OR TypeScript + Commander.js
Chain: brainstorming → writing-plans → project-bootstrap → tdd → code-reviewer → deployment

### Type 5: Mobile App
Stack: React Native Expo (cross-platform) or Flutter
Chain: ultraplanning → architect → project-bootstrap → tdd → e2e-runner → security-reviewer → deployment

### Type 6: Data Pipeline / ETL
Stack: Python + Airflow/Prefect + dbt + PostgreSQL
Chain: ultrathinking → architect → database-reviewer → project-bootstrap → tdd → deployment

## Router Decision Tree
```
Primary output?
├── UI for users → Type 1
├── API endpoints → Type 2
├── AI/LLM features → Type 3 (can combine)
├── Terminal command → Type 4
├── iOS/Android → Type 5
├── Process/transform data → Type 6
└── Code for developers → Type 8 (Library)
```
