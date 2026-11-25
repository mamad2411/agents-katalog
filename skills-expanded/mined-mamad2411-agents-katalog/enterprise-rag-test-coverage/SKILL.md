---
name: enterprise-rag-test-coverage
description: Authoritative test specification for the Self-Hosted Enterprise Chat Agent (enterprise_rag) starter pack. Documents API endpoints, UI interactions, document ingestion, RAG chat flows, and infrastructure. Split into phase-specific files.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, WebFetch, Write, Edit
argument-hint: [section] (optional — "api", "ui", "infra", or omit to run all three)
---

# Self-Hosted Enterprise Chat Agent — Test Coverage Specification

Source of truth for what to test on a deployed Enterprise RAG stack. Covers the Enterprise RAG frontend (React SPA), the RAG server, ingestor server, NIM models, Milvus vector DB, and OCI infrastructure.

**Frontend repo:** `oci-ai-incubations/enterprise-rag-frontend` (React 19, Vite, MUI/KUI, Tailwind, Zustand, TanStack Query)
**RAG Server:** NVIDIA Blueprint RAG Server 2.3.0 — LLM chat with retrieval augmentation
**Ingestor:** NVIDIA Blueprint Ingestor Server 2.3.0 — document processing via NV-Ingest
**LLM:** Llama 3.3 Nemotron Super 49B v1.5 (via NIM)
**Embedding:** Llama 3.2 NV-embedqa 1B (via NIM)
**Reranker:** Llama 3.2 NV-rerankqa 1B (via NIM)
**Vector DB:** Milvus (port 19530, GPU_CAGRA index)
**Deployment:** Terraform → OKE → Helm chart (NOT Corrino blueprint) in `rag` namespace

**Note:** This spec covers `enterprise_rag`. The `enterprise_rag_aiq` category deploys the same RAG stack plus an additional AIQ namespace with a separate frontend — that would need its own test coverage spec.

---

## Test Files

Each file is **self-contained** — it has everything needed to execute its tests without reading any other file.

| File | Tests | Count | Executor |
|---|---|---|---|
| `api-tests.md` | EA-1 through EA-10 | 10 | Main agent via `curl` |
| `ui-tests.md` | EU-1 through EU-18 | 18 | agent-browser |
| `infra-tests.md` | EI-1 through EI-10 | 10 | Main agent via `kubectl` / OCI CLI |

**Total: 38 tests** (10 API + 18 UI + 10 Infra)

---

## Invocation Behavior

- **`/enterprise-rag-test-coverage infra`** — Read and execute `infra-tests.md` only.
- **`/enterprise-rag-test-coverage api`** — Read and execute `api-tests.md` only.
- **`/enterprise-rag-test-coverage ui`** — Read and execute `ui-tests.md` only.
- **`/enterprise-rag-test-coverage`** (no argument) — Execute ALL three in order: `infra-tests.md`, then `api-tests.md`, then `ui-tests.md`.

---

## Environment Variables for Testing

| Variable | Required | Description |
|---|---|---|
| `STARTER_PACK_URL` | Yes | Base URL of the deployed RAG frontend (e.g. `https://frontend-erag.1-2-3-4.nip.io`) |

**Note:** No authentication required. The Enterprise RAG frontend has no login.

---

## Architecture Components

| Component | Port | Namespace | Purpose |
|---|---|---|---|
| RAG Frontend (React) | 3000 | rag | SPA — chat, collections, settings, citations |
| RAG Server | 8081 | rag | Chat/generate endpoint with RAG retrieval |
| Ingestor Server | 8082 | rag | Document upload, processing, collection management |
| NIM LLM (Nemotron 49B) | 8000 | rag | Large language model inference |
| NIM Embedding (embedqa 1B) | 8000 | rag | Document embedding generation |
| NIM Ranking (rerankqa 1B) | 8000 | rag | Reranking search results |
| Milvus | 19530 | rag | Vector database for embeddings |
| MinIO | 9000 | rag | In-cluster object storage for multimodal content |
| Redis | 6379 | rag | Cache for ingestor batch coordination |
| NV-Ingest | 7670 | rag | Document processing pipeline (text/table/chart extraction) |

**Frontend API proxy mapping (via ingress):**
- `/api/generate` → RAG Server (8081) — chat/RAG queries (SSE streaming)
- `/api/collections` → Ingestor Server (8082) — list/create/delete collections
- `/api/documents` → Ingestor Server (8082) — upload/list/delete documents
- `/api/status` → Ingestor Server (8082) — poll ingestion task status
- `/api/health` → Ingestor Server (8082) — health check with dependency status

**Pages:** `/` (Chat), `/collections/new` (New Collection), `/settings` (Settings)

---

## Known Issues & Stability Notes

| Issue | Impact | Mitigation |
|---|---|---|
| NIM LLM startup 15-30 min | Chat fails until model loaded | Wait for nim-llm pod Running + `/v1/models` returns models |
| Embedding NIM startup 10-15 min | Document ingestion fails | Wait for nemoretriever-embedding pod Running |
| Ingestor 90-min Helm timeout | Large Helm release may take long to deploy | Monitor `helm list -n rag` for status |
| Milvus cold start | Collection creation may fail initially | Verify Milvus pod Running before collection tests |
| MinIO credentials | Randomly generated per deploy | Check rag-minio secret exists |
| Large file upload (400MB max) | Ingestion may timeout for very large files | Test with moderate file sizes (<50MB) |
| SSE streaming for chat | Connection may drop on long responses | Verify streaming works end-to-end |
| GPU_CAGRA index | Requires GPU nodes for vector search | Verify GPU allocation on worker nodes |

---

## Maintenance

- Re-run this skill when `helm.tf` RAG sections or `helm-values/enterprise-rag-values.yaml` change
- Update API inventory if `enterprise-rag-frontend` image version changes
- IDs (EA-*, EU-*, EI-*) are stable — never renumber, only append
- If an endpoint is removed, mark `DEPRECATED` — do not delete from this spec
