---
name: okf
description: >
  Work with Open Knowledge Format (OKF) bundles in this repository. Use when
  the user mentions OKF, Open Knowledge Format, knowledge bundle, OKF bundle,
  agent-readable knowledge, LLM wiki, concepts, frontmatter, validation,
  indexing, graph generation, search, RAG, reading, writing, or editing OKF
  concepts. Prefer the MCP server named simple-okf from .mcp.json for OKF
  content operations.
metadata:
  version: "3.0"
  scope: simple-okf-local
---

# Open Knowledge Format (OKF)

Use this skill for OKF content, OKF tooling, and OKF-aware RAG work in this
repository.

OKF is a portable knowledge format based on:

```text
Markdown + YAML frontmatter + directories + Markdown links
```

This repository is standardized on:

```text
okf/                    # default OKF bundle
okf_mcp/                    # MCP server, OKF library, CLI fallback, OKF RAG
.env            # local-only RAG environment file, never commit
artifacts/              # generated graph, 7D dashboard, and RAG artifacts
.agents/skills/okf/     # this skill, templates, references
```

Do not create alternate local tooling packages or a top-level `rag/` directory.

## Authority and source of truth

For this project:

1. `README.md` is the human quick-start.
2. `SPEC.md` is the repository/tooling contract.
3. `AGENTS.md` is the repository-local agent policy.
4. `okf/` is the default knowledge bundle.
5. `okf_mcp/okf.py` is the shared OKF filesystem implementation.
6. `okf_mcp/server.py` is the MCP tool surface.
7. `okf_mcp/rag/` is tooling over OKF concepts, not canonical knowledge.

When files disagree, update the canonical owner instead of duplicating the same
rule in another file.

## MCP entrypoint

Primary MCP server name:

```text
simple-okf
```

`simple-okf` is configured in `.mcp.json` and runs `python -m okf_mcp server`
against the `okf/` bundle.

Preferred MCP tools for OKF work:

```text
simple-okf.bundle_info()
simple-okf.read_support_file(path="index.md")
simple-okf.list_directory(directory="")
simple-okf.list_concepts(...)
simple-okf.search_concepts(query, limit)
simple-okf.read_concept(concept_id, include_body=true)
simple-okf.read_existing_doc(concept_id)
simple-okf.read_concept_raw(concept_id)
simple-okf.write_concept_doc(concept_id, frontmatter, body, ...)
simple-okf.validate_bundle()
simple-okf.generate_indexes()
simple-okf.export_source_documents(source="system", force=false)
simple-okf.build_graph(write=true, out_path="artifacts/okf/graph.json", html=true, html_out_path="artifacts/okf/graph.html")
```

OKF-aware RAG MCP tools:

```text
simple-okf.rag_inspect_corpus(...)
simple-okf.rag_parse_chunks()
simple-okf.rag_refresh_index()
simple-okf.rag_retrieve(query, limit, type_filter, tag)
simple-okf.rag_answer(question, limit)
simple-okf.rag_get_source(concept_id, line_start, line_end)
simple-okf.rag_concept_relationships(concept_id, depth)
simple-okf.rag_local_readiness(correlation_id)
simple-okf.rag_infra_readiness(timeout_seconds, correlation_id)
simple-okf.rag_index_freshness()
simple-okf.rag_quality_summary(limit)
simple-okf.rag_recent_failures(limit)
simple-okf.rag_event_lookup(event_id, correlation_id, limit)
```

If `simple-okf` is unavailable during an OKF content task, report that MCP is
unavailable. Use local CLI fallback only when the user asks to work on this
repository/tooling or explicitly accepts fallback behavior.

## CLI fallback

CLI fallback commands live in the `okf_mcp` multi-app CLI and call shared implementation code.
Do not duplicate OKF logic in CLI handlers.

```sh
python3 -m okf_mcp validate okf
python3 -m okf_mcp indexes okf
python3 -m okf_mcp export system --out okf
python3 -m okf_mcp graph okf --out artifacts/okf/graph.json --html-out artifacts/okf/graph.html
python3 -m okf_mcp rag inspect --pretty
python3 -m okf_mcp rag refresh --pretty
python3 -m okf_mcp rag retrieve "query" --pretty
python3 -m okf_mcp rag retrieve "query" --answer --pretty
python3 -m okf_mcp rag local-readiness --pretty      # exits non-zero when not ready; add --no-fail for informational use
python3 -m okf_mcp rag infra-readiness --pretty      # exits non-zero when required/configured infra is not ready; add --no-fail for informational use
python3 -m okf_mcp rag index-freshness --pretty      # exits non-zero when stale/missing; add --no-fail for informational use
python3 -m okf_mcp rag quality-summary --pretty
python3 -m okf_mcp rag recent-failures --pretty
python3 -m okf_mcp rag event-lookup --event-id EVENT_ID --pretty
```

RAG fallback reads environment from `.env` by default. If the file is
missing, use `--env /path/to/file` for smoke tests or report that RAG runtime
validation was skipped.

## Core terminology

- **Bundle** — a directory tree of Markdown files; unit of distribution.
- **Concept** — one Markdown file representing one unit of knowledge.
- **Concept ID** — bundle-relative path without the `.md` suffix.
- **Frontmatter** — YAML mapping at the top of a concept file.
- **Body** — Markdown content after frontmatter.
- **Support file** — navigation/history file, not a concept.
- **Link** — Markdown link expressing a relationship between concepts.
- **Citation** — link or source reference backing a claim.
- **Derived output** — generated indexes, graph reports, or RAG artifacts.

Example concept ID:

```text
requirements/functions/FUNC-001
```

## Reserved files

| File | Purpose | Concept? |
|---|---|---|
| `index.md` | Directory navigation / progressive disclosure | No |
| `log.md` | Bundle-local change history | No |

Never treat `index.md` or `log.md` as normal concepts. RAG tools must exclude
them from the corpus.

## Frontmatter rules

Minimum conformant concept:

```md
---
type: Reference
status: draft
---

Concept body.
```

Recommended project frontmatter:

```yaml
---
type: API Operation
status: draft
title: API-042 — Create project
description: Operation contract for project creation.
resource: system/API.md#api-042
tags: [api, operation, project]
timestamp: 2026-06-25T00:00:00Z
requirement_id: API-042
source_path: system/API.md
owner_document: API.md
---
```

Rules:

1. `type` is required and must be mapped in the 7D type registry.
2. `status` is required. Allowed values are exactly `draft`, `to-review`,
   `not-valid`, `valid`, `rejected`, and `accepted`.
3. `status` is document/artifact state, not implementation progress. Status
   transitions are recommended only, not validation gates: `draft` ->
   `to-review` -> (`valid` or `not-valid`), then optionally `accepted` or
   `rejected`.
4. `title`, `description`, and `timestamp` are recommended.
5. Unknown frontmatter keys are allowed.
6. Preserve unknown frontmatter keys when editing existing concepts.
7. Do not invent fields, citations, source paths, schema details, or
   requirement IDs.
8. Use `tags` as a list when possible.

## Common concept types

Use these unless the user or existing bundle taxonomy indicates another type:

```yaml
type: Source Document
type: Requirement
type: Function Requirement
type: User Flow
type: Business Rule
type: Access Rule
type: Data Entity
type: API Operation
type: UX Screen
type: UI Component
type: Architecture Decision
type: Deployment Requirement
type: Traceability Row
type: Gap
type: Glossary Term
type: Reference
```

Type values are controlled by the 7D registry in `SPEC.md` and
`okf_mcp/okf.py`. Do not create an unmapped type silently; if no existing mapped
value fits, report the mapping gap instead of inventing a new taxonomy value.

## Links as graph

Relationships are normal Markdown links:

```md
This operation creates [Project](../../data/entities/project.md)
and is governed by [ACCESS-005](../../requirements/access/ACCESS-005.md).
```

The relationship type is expressed by surrounding prose. Prefer relative links
for internal OKF links because validation and graph generation resolve them
reliably.

Do not replace a missing exact target with a broad link just to satisfy
validation. If the correct target is unknown, report the gap.

## Workflow: inspect existing bundle

1. Call `simple-okf.read_support_file(path="index.md")`.
2. Call `simple-okf.list_directory(directory="")`.
3. Use `simple-okf.list_concepts(...)` or `simple-okf.search_concepts(...)` for
   discovery.
4. Open only needed concepts with `simple-okf.read_concept(...)` or
   `simple-okf.read_concept_raw(...)`.
5. Follow Markdown links through `simple-okf.read_concept(...)` when
   relationships matter.
6. Use `simple-okf.rag_retrieve(...)` or `simple-okf.rag_answer(...)` for
   broader semantic discovery when RAG is configured.

## Workflow: create a concept

1. Discover the right location with `list_directory` and `list_concepts`.
2. Choose a stable concept ID.
3. Use frontmatter with at least mapped `type` and allowed `status`; prefer
   `title`, `description`, `timestamp`, `tags`, and source fields when supported
   by evidence.
4. Write concise Markdown body sections.
5. Add relative links to related concepts only when there is evidence.
6. Add citations only when there is a real source.
7. Write via `simple-okf.write_concept_doc(...)`.
8. Run `simple-okf.generate_indexes()`.
9. Run `simple-okf.build_graph(write=true, out_path="artifacts/okf/graph.json", html=true,
   html_out_path="artifacts/okf/graph.html")` when relationships changed.
10. Run `simple-okf.validate_bundle()`.

## Workflow: edit a concept

1. Read the existing concept first.
2. Preserve unknown frontmatter fields.
3. Preserve stable concept IDs unless the user approves a rename.
4. Update links if concept IDs move.
5. Do not delete citations, schema details, or source fields unless they are
   incorrect or obsolete.
6. Write via `simple-okf.write_concept_doc(...)`.
7. Regenerate derived outputs as needed.
8. Validate the bundle.

## Workflow: export canonical Markdown docs

Convert source Markdown documents into `Source Document` concepts:

```text
simple-okf.export_source_documents(source="system", force=false)
simple-okf.generate_indexes()
simple-okf.validate_bundle()
```

Do not treat generated OKF output as more canonical than its source unless the
user explicitly changes the ownership model.

## Workflow: generate graph

Build graph JSON and optional HTML report from concept links:

```text
simple-okf.build_graph(write=true, out_path="artifacts/okf/graph.json", html=true, html_out_path="artifacts/okf/graph.html")
```

`artifacts/okf/graph.json` and `artifacts/okf/graph.html` are derived outputs and may be
regenerated.

## Workflow: use OKF RAG

Use RAG for discovery and question answering over OKF concepts, not as a
replacement for reading/editing source concepts.

RAG configuration:

```text
.env              # local-only, ignored
.env.example      # committed template
artifacts/rag/            # generated RAG artifacts
```

Default useful variables:

```dotenv
RAG_BUNDLE_DIR=okf
RAG_ARTIFACTS_DIR=artifacts/rag
RAG_RETRIEVAL_RESULT_LIMIT=10
RAG_ANSWER_EVIDENCE_LIMIT=5
```

RAG rules:

1. RAG corpus is OKF concepts only; exclude `index.md` and `log.md`.
2. RAG chunks must preserve frontmatter context.
3. RAG answers must cite `concept_id`, path, and line ranges when evidence is
   available.
4. RAG artifacts are derived outputs, not canonical knowledge.
5. Never commit `.env`.
6. Keep `RAG_PROFILE=local` infrastructure-free; use `quality` only for gated
   Compose-backed checks and `production` only with explicit infra readiness.
7. For profile-specific Compose guidance, backup/restore, index rollback/swap,
   security/MCP exposure, 7D release checklist artifacts, and CI matrix details,
   see `docs/operations/rag_production_hardening.md`.

## Validation expectations

Before finishing OKF content work, run through MCP when available:

```text
simple-okf.validate_bundle()
```

When adding/removing/renaming concepts, also run:

```text
simple-okf.generate_indexes()
simple-okf.build_graph(write=true, out_path="artifacts/okf/graph.json", html=true, html_out_path="artifacts/okf/graph.html")
simple-okf.validate_bundle()
```

For repository/tooling changes, use local checks as appropriate:

```sh
python3 -m py_compile okf_mcp/*.py okf_mcp/rag/*.py okf_mcp/rag/ingestion/*.py okf_mcp/rag/retrieval/*.py
python3 -m okf_mcp validate okf
python3 -m okf_mcp graph okf --out artifacts/okf/graph.json --html-out artifacts/okf/graph.html
git diff --check
git status --short
git diff --stat
```

Report which MCP tools or fallback commands were run and their results.

## Guardrails

1. Never invent domain facts.
2. Preserve unknown fields.
3. Keep stable IDs and links stable unless the user asks for a rename/move.
4. Prefer minimal accurate concepts over padded concepts.
5. Do not impose a rigid taxonomy beyond project conventions.
6. Ask before broad directory, ownership, or bundle-structure changes.
7. Do not commit local secrets or `.env`.
8. Do not create alternate local tooling packages or top-level `rag/` directories.
9. Treat graph and RAG artifacts as derived outputs.
10. Report unresolved missing knowledge as gaps or open questions.

## Output format

When presenting OKF changes, summarize:

1. files changed;
2. concepts added/edited/moved/deleted;
3. derived outputs regenerated, if any;
4. validation commands/MCP tools and results;
5. remaining gaps or open questions.
