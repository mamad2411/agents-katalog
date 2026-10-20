## Purpose
Be concise: this file tells an AI coding agent how this repository is organized, where to find the important artifacts, and which patterns to follow when editing or adding content.

## Big picture (what this repo is)
- This is primarily a job-application / project documentation workspace (resumes, application trackers, playbooks, and agent prompts), not a single runnable product.
- Common architecture patterns referenced across the repo: LangChain-based agent orchestration, RAG pipelines (embeddings + FAISS), MCP (Model Context Protocol) for agent-to-agent communication, FastAPI backends, and Streamlit experiment UIs. Look for examples under `applications/` (e.g. `applications/ai-engineer-agents/`, `applications/shipt/`, `applications/meta-reality-labs-ai-engineer/`).

## What to read first (high-value files)
- `README.md` (repo root) — overview and master tracker note.
- `RESUME_APPLICATION_WORKFLOW.md` — operational workflows and references to tools (MCP generator, standalone scripts like `generate-resume-standalone.mjs`).
- `applications/README.md` — master tracker for each company entry.
- `applications/_resources/OPTIMIZATION_SUMMARY.md` and `applications/_resources/role-based-context-loading.md` — contains optimized prompts and where agent prompt files are expected (e.g. `.claude/agents/resume-agent.md`).
- `context/` — canonical system/context prompts and short architecture notes (see `interview_qa_bank.md` which documents the GridCOP SQL-generation pattern and sensitive-data handling).

## Project-specific conventions and patterns
- Each job entry lives in `applications/<company>/` and typically includes `resume-data.json`, `job-posting.md`, `resume-draft*.md` and an optional `README.md` describing the per-application workflow.
- Use `_template/` and `_template-ai-engineer/` when creating new application folders — copy naming and metadata patterns (date-prefixed resume drafts like `YYYYMMDD-...` are common).
- Prompts/configs are referenced but not always committed: look for `.claude/` references in `_resources/*`. If you need agent configs, search for `.claude` references and ask the maintainer when they are missing.
- RAG and agent examples: inspect `applications/ai-engineer-agents/` and `applications/shipt/` for LangChain + FAISS + MCP examples and naming conventions.

## Integration points and external dependencies
- LLMs: Anthropic Claude is the primary commercial model referenced. OpenAI, Ollama, and local LLMs are mentioned across examples.
- Retrieval: FAISS (vector DB) and Pinecone are commonly referenced for embedding + RAG patterns.
- Backends & UIs: FastAPI and Streamlit are the typical runtime components for serving agents/experiments.
- Web search tool: DuckDuckGo Search API used in several examples for live retrieval.

## Safe editing rules for AI agents
- Never send raw sensitive data to external APIs. The documented pattern (see `context/interview_qa_bank.md`): LLMs generate SQL or analysis locally; execute on local DB and send only sanitized aggregates back to the model.
- If a file references `.claude/...` or other agent configs that are not present, do not invent secrets or keys — ask the user for missing configs.

## Developer workflows (what an AI assistant should do)
- For content edits (resume text, application templates): follow the templates in `applications/_template*` and update `applications/README.md` master tracker when you apply a resume.
- For prompt/agent iteration: prefer small, local experiments with Streamlit or a FastAPI dev server if examples exist; otherwise draft prompts under `applications/_resources/` and request human review before calling real APIs.
- For running the resume generator: see `RESUME_APPLICATION_WORKFLOW.md` for the MCP generator and `generate-resume-standalone.mjs` fallback.

## Concrete examples to reference
- GridCOP pattern (LangChain → LLM generates SQL → local validation → execute → sanitize): `context/interview_qa_bank.md`.
- Multi-agent + RAG example traces: `applications/ai-engineer-agents/20251031-1826-ai-engineer-resume-draft.md` and `applications/shipt/*` (mentions LangGraph/MCP/FAISS/FastAPI).

## If you're unsure
- Read `RESUME_APPLICATION_WORKFLOW.md` and `applications/README.md` first.
- Search for the pattern or file name under `applications/` before creating new conventions.
- When missing runtime scripts, configs, or secrets (e.g. `.claude/*`, API keys), stop and ask — do not fabricate values.

---
If you'd like, I can: (A) expand this into more prescriptive editing templates, (B) add a short CONTRIBUTING.md, or (C) scan and list candidate files that look like runnable code (FastAPI/Streamlit) we could add small run scripts for. Which would you prefer next?
