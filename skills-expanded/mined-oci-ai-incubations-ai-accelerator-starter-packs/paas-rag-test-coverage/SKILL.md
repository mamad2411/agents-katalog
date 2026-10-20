---
name: paas-rag-test-coverage
description: Authoritative test specification for the Managed Enterprise Chat Agent (paas_rag) starter pack. Documents API endpoints, UI interactions, document management, RAG chat flows, and infrastructure. Split into phase-specific files.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, WebFetch, Write, Edit
argument-hint: [section] (optional — "api", "ui", "infra", or omit to run all three)
---

# Managed Enterprise Chat Agent — Test Coverage Specification

Source of truth for what to test on a deployed PaaS RAG stack. Covers the OracleNet frontend (React SPA), the LlamaStack backend, Oracle 26ai vector database, OCI Object Storage, and OCI infrastructure.

**Frontend repo:** `oci-ai-incubations/oraclenet-frontend` (React 19, Vite 6, TanStack Query, Zustand, Tailwind, Framer Motion)
**Backend:** LlamaStack — OpenAI-compatible API with vector store support, chat completions, and file management
**Database:** Oracle Autonomous Database 26ai — vector storage for RAG embeddings
**Object Storage:** OCI Object Storage (S3-compatible) — document file storage
**Deployment:** Terraform → OKE → Corrino Blueprint (2-service deployment group: llamastack + frontend)

**Note:** PaaS RAG is CPU-only — no GPU workers. Uses OCI GenAI service models (not local NIM).

---

## Test Files

Each file is **self-contained** — it has everything needed to execute its tests without reading any other file. Load only the file for the phase you're executing.

| File | Tests | Count | Executor |
|---|---|---|---|
| `api-tests.md` | PA-1 through PA-10 | 10 | Main agent via `curl` |
| `ui-tests.md` | PU-1 through PU-18 | 18 | agent-browser |
| `infra-tests.md` | PI-1 through PI-5 | 5 | Main agent via `kubectl` / OCI CLI |

**Total: 33 tests** (10 API + 18 UI + 5 Infra)

---

## Invocation Behavior

- **`/paas-rag-test-coverage infra`** — Read and execute `infra-tests.md` only.
- **`/paas-rag-test-coverage api`** — Read and execute `api-tests.md` only.
- **`/paas-rag-test-coverage ui`** — Read and execute `ui-tests.md` only.
- **`/paas-rag-test-coverage`** (no argument) — Execute ALL three in order: `infra-tests.md`, then `api-tests.md`, then `ui-tests.md`.

---

## Environment Variables for Testing

| Variable | Required | Description |
|---|---|---|
| `STARTER_PACK_URL` | Yes | Base URL of the deployed OracleNet frontend (e.g. `https://frontend-paas.1-2-3-4.nip.io`) |

**Note:** No authentication required. The OracleNet frontend has no login.

---

## Architecture Components

| Component | Port | Purpose |
|---|---|---|
| OracleNet Frontend (React SPA) | 3000 | 2-page app — Chat (collections, messages, citations) + Settings |
| LlamaStack Backend | 8321 | OpenAI-compatible API — vector stores, files, models, chat responses (SSE) |
| Oracle 26ai Database | 1522 | Autonomous Database for vector embeddings and collection storage |
| OCI Object Storage (S3) | — | Document file storage via S3-compatible API |

**Ingress route mapping (via Corrino blueprint):**
- `/` → frontend (port 3000)
- `/v1/*` → llamastack (port 8321) — models, health, responses, vector_stores, files

**Pages:** `/` (Chat with collections sidebar), `/settings` (Model + RAG configuration)

**Key user flows:**
1. Create a collection (vector store) with embedding model selection
2. Upload documents (.txt, .pdf, .doc, .docx, .md) — async indexing with status polling
3. Select collection(s) in sidebar → chat with RAG retrieval
4. View inline citations with footnote references and file downloads
5. Configure model, temperature, and system instructions in Settings

---

## Known Issues & Stability Notes

| Issue | Impact | Mitigation |
|---|---|---|
| LlamaStack startup 2-5 min | API returns 502 until pod is ready | Wait for health endpoint to respond |
| Oracle 26ai provisioning 10-20 min | Vector store operations fail until DB is ready | Check health endpoint dependency status |
| Embedding model availability | Collection creation fails if no embedding models loaded | Verify `/v1/models` returns embedding models first |
| SSE streaming for chat | Connection may drop on long responses | Verify streaming works end-to-end |
| File indexing async | Upload returns immediately; indexing takes seconds to minutes | Poll file status until `completed` |
| System collections hidden | `metadata_schema` and `meta` collections filtered from UI | Expected behavior — don't test for them |
| No GPU required | PaaS RAG is CPU-only; uses OCI GenAI service | No GPU allocation tests needed |

---

## Maintenance

- Re-run this skill when `blueprint_files.tf` paas_rag sections change or frontend image version updates
- Update API inventory if `oraclenet-frontend` image version changes
- IDs (PA-*, PU-*, PI-*) are stable — never renumber, only append
- If an endpoint is removed, mark `DEPRECATED` — do not delete from this spec
