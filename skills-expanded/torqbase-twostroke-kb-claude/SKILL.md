# CLAUDE.md — TwoStrokeGPT

Guidance for Claude Code working in this repo. Read this first; keep it updated as the project evolves.

## What this is

An AI-powered knowledge platform for **two-stroke engines** (Hirth Engines hackathon challenge). Users upload technical documents in any format; the system ingests them into a searchable knowledge base and answers questions with an agentic RAG pipeline that **cites its sources and checks its own answers**.

- **Knowledge source:** ONLY user-uploaded documents (no web scraping in this phase).
- **Languages:** English and German (corpus is German-first).
- **Primary risk to design against:** the corpus is quantitative (specs, fuel data, FAR limits). **Never let the model invent a number.** Every numeric claim must trace to a source.

## Tech stack

- **Backend / API:** Python 3.11+, FastAPI, Uvicorn.
- **Frontend:** FastAPI serves a minimal HTML/JS page from `api/static/` (no JS build step).
- **Agent orchestration:** LangGraph (ingestion pipeline = one graph; ReAct agent = another).
- **Vector store + DB:** PostgreSQL + pgvector (one DB for vectors, relational data, graph tables).
- **Embeddings:** multilingual model (see `EMBEDDING_MODEL` in `.env`).
- **LLM:** hosted API (OpenAI/Anthropic) or local Ollama — controlled by `LLM_PROVIDER`.
- **Retrieval:** hybrid (BM25 + dense) → cross-encoder re-rank.
- **Dep management:** pip + venv (`requirements.txt`).
- **LLM access:** ALL model calls go through `llm.py` (`chat`, `chat_json`). Do not call OpenAI/Anthropic/Ollama SDKs directly elsewhere.

## Design docs (read these for context)

- `docs/ARCHITECTURE.md` — full system diagram (Mermaid) + how each format is handled.
- `docs/PLAN.md` — rationale, memory model, multilingual handling, X-factor, build order, evidence.
- `docs/architecture.mermaid` — the raw diagram source.

## Repo layout

```
twostroke-kb/
├── CLAUDE.md                  # this file
├── README.md                  # human setup guide
├── requirements.txt
├── .env.example               # copy to .env and fill in
├── .gitignore
├── docker-compose.yml         # postgres + pgvector
├── Makefile                   # common commands
├── pyproject.toml             # pytest pythonpath + ruff config
├── config.py                  # settings (pydantic-settings, reads .env)
├── llm.py                     # unified LLM client (openai/anthropic/ollama)
├── docs/                      # ARCHITECTURE.md, PLAN.md, architecture.mermaid
├── db/
│   └── schema.sql             # tables: documents, chunks, structured_facts, graph_*, feedback, gaps, memory
├── api/
│   ├── main.py                # FastAPI app: /upload /ask /feedback + static
│   └── static/index.html      # minimal upload + chat UI
├── ingestion/                 # GRAPH 1 — turns uploads into knowledge
│   ├── orchestrator.py        # LangGraph ingestion pipeline
│   ├── format_router.py       # detect type + language, dispatch to a parser
│   ├── parsers/
│   │   ├── pdf_parser.py      # digital PDF (PyMuPDF)
│   │   ├── ocr.py             # scanned PDF / images (Tesseract de+en)
│   │   ├── docx_parser.py     # .docx
│   │   ├── doc_convert.py     # legacy .doc -> convert then parse
│   │   ├── sheet_parser.py    # .xlsx/.csv TABLE-AWARE -> structured facts
│   │   ├── pptx_parser.py     # .pptx
│   │   ├── link_handler.py    # .url shortcut -> store link only, no fetch
│   │   └── figure_handler.py  # STRETCH: extract figures, vision-caption, OCR callouts
│   ├── corpus_builder.py      # normalize -> clean text + tables + metadata
│   ├── chunker.py             # chunk prose, keep tables intact
│   ├── domain_enricher.py     # extract tags + entities (de/en) via LLM
│   ├── graph_builder.py       # extract Engine->Part->Symptom->Cause->Fix relations
│   ├── knowledge_base.py      # embed + write to pgvector
│   └── dedup.py               # cosine>0.98 -> skip vector, MERGE provenance
├── agent/                     # GRAPH 2 — answers questions
│   ├── graph.py               # LangGraph ReAct graph wiring
│   ├── nodes.py               # reason / choose_tool / act / observe / draft / verify
│   ├── tools.py               # hybrid_search, graph_lookup, spec_lookup, conflict_check, unit_convert, diagnostic_tree, source_viewer
│   ├── retriever_hybrid.py    # BM25 + dense fusion
│   ├── reranker.py            # cross-encoder, top-20 -> top-5
│   ├── recommender.py         # related questions + graph neighbours
│   └── verifier.py            # grounding check + gap detection
├── memory/
│   └── store.py               # conversation, user profile, feedback/corrections
└── tests/
    └── test_smoke.py
```

## Commands

```bash
make setup        # create venv + install requirements + system-dep reminders
make db           # docker compose up postgres+pgvector, apply db/schema.sql
make run          # uvicorn api.main:app --reload
make test         # pytest
```

Or manually:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d
psql "$DATABASE_URL" -f db/schema.sql
uvicorn api.main:app --reload
```

## System dependencies (NOT pip)

These must be installed on the machine for some parsers to work:
- **Tesseract OCR** + German data: `tesseract-ocr tesseract-ocr-deu` (for `ocr.py`).
- **Poppler** (`pdf2image` backend): `poppler-utils`.
- **LibreOffice** or **antiword** (for legacy `.doc` in `doc_convert.py`).

## Critical design rules (do not violate)

1. **Ground every claim, especially numbers.** Answers must cite the chunk/cell/clause they came from. The `verifier` node rejects unsupported numeric claims and loops back. Never synthesize a spec value.
2. **Dedup MERGES provenance, never deletes a source.** In `dedup.py`, when cosine > 0.98, keep one vector but append the new source reference. `conflict_check` and citations depend on seeing every source. Blind deletion is a bug.
3. **Upload-only scope.** Do not add web/forum scraping. `.url` files store the link as a reference; they are NOT fetched.
4. **Multilingual, not per-language indexes.** One multilingual embedding space. Detect language, answer in the user's language, cite the original (even if cross-language).
5. **Spreadsheets are first-class.** `.xlsx/.csv` go through `sheet_parser.py` into the `structured_facts` table with units preserved; `spec_lookup` reads exact values from there.
6. **Plain RAG must work before the agent.** Keep a path that does retrieve→answer without the full ReAct loop, so the demo has a fallback if the agent misbehaves.

## MVP cut line (build in this order)

1. Upload → `format_router` → PDF/docx/txt parse → chunk → embed → pgvector. Plain retrieve→answer with citations.
2. Add OCR (scanned PDF) + `sheet_parser` (xlsx) + legacy `.doc`.
3. Wrap retrieval in the ReAct agent + grounding `verifier` (self-correction).
4. Re-ranker, then recommendation system (a challenge requirement).
5. Feedback loop + dedup-with-provenance + gap detector.
6. Knowledge graph view, beginner/expert mode.
7. STRETCH only: figure/diagram intelligence, document versioning, streaming/progress polish.

If short on time, stop adding features and make the cited-answer demo flawless.

## Conventions

- Type hints everywhere; small pure functions; docstrings state inputs/outputs/side-effects.
- All DB access goes through helpers in `config.py`/`memory/store.py` — no scattered connection strings.
- Secrets only in `.env` (never commit). Read via `config.py`.
- Each parser returns the SAME normalized shape: `{text, tables, metadata, source_ref}` so `corpus_builder` is parser-agnostic.
- Tests: at minimum a smoke test per parser against a tiny sample file in `tests/fixtures/`.

## Glossary

- **chunk** — a passage of text + metadata that gets embedded.
- **structured fact** — a row/value extracted from a spreadsheet/table, stored separately for exact lookup.
- **grounding** — verifying a draft answer is supported by retrieved sources before returning it.
- **gap** — a question that retrieved no good evidence; logged for an expert to fill.
