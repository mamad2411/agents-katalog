---
name: dox-pack-test-coverage
description: Authoritative test specification for the Document Extractor starter pack. Documents API endpoints, UI interactions, extraction pipeline, RAG chat flows, and infrastructure. Split into phase-specific files.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, WebFetch, Write, Edit
argument-hint: [section] (optional — "api", "ui", "infra", or omit to run all three)
---

# Document Extractor — Test Coverage Specification

Source of truth for what to test on a deployed dox_pack stack. Covers the dox-frontend (Next.js), the dox-backend (FastAPI extraction + RAG chat), LlamaStack (OpenAI-compatible inference), OCI GenAI Dedicated AI Cluster (Qwen3-VL-235B), Oracle 26ai database, and OCI infrastructure.

**Frontend:** Next.js UI — contract upload, extraction progress, CSV/JSON download, RAG chat, history, prompt config
**Backend:** dox-backend (FastAPI, port 8000) — 3-pass extraction pipeline (Qwen3-VL vision OCR, Maverick text expansion, validation) + RAG chat
**Inference:** LlamaStack (port 8321) — OpenAI-compatible API with Maverick LLM + Cohere embeddings; OCI GenAI DAC — Qwen3-VL-235B for vision OCR
**Database:** Oracle Autonomous Database 26ai — extraction history + vector storage for RAG
**Object Storage:** OCI Object Storage (S3-compatible) — document file storage
**Deployment:** Terraform -> OKE -> Corrino Blueprint (3-service deployment group: llamastack + dox-backend + dox-frontend)

**Note:** Document Extractor is CPU-only on the OKE cluster. GPU inference runs on the OCI GenAI Dedicated AI Cluster (DAC), which is a managed OCI service outside the Kubernetes cluster.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│              dox-frontend (Next.js, port 80)                │
│  Exposed via ingress at dox-frontend.<fqdn>                 │
│                                                                  │
│  Upload PDF ─────────> dox-backend /api/extract             │
│  Poll status ────────> dox-backend /api/jobs/{id}           │
│  Download CSV ───────> dox-backend /api/jobs/{id}/download  │
│  Download JSON ──────> dox-backend /api/jobs/{id}/download/json │
│  List contracts ─────> dox-backend /api/contracts           │
│  Chat ───────────────> dox-backend /api/chat                │
│  Prompt config ──────> dox-backend /api/config/prompt       │
│  History ────────────> dox-backend /api/history             │
│                                                                  │
│  Pages: / (Upload + Extraction), /history, /chat, /settings      │
└──────────────────────┬───────────────────────────────────────────┘
                       │ BACKEND_SVC
           ┌───────────▼───────────┐
           │  dox-backend     │
           │  (FastAPI, port 8000) │
           │                       │
           │  3-pass extraction:   │
           │    Pass 1: Qwen3-VL   │──────────┐
           │    Pass 2: Maverick   │───┐      │
           │    Pass 3: Validation │   │      │
           │                       │   │      │
           │  RAG chat ────────────│───┤      │
           └───────┬───────────────┘   │      │
                   │                   │      │
           ┌───────▼──────┐   ┌────────▼──┐  │
           │  Oracle 26ai │   │ LlamaStack│  │
           │  (ORACLE_DSN)│   │ :8321     │  │
           │  history +   │   │ Maverick  │  │
           │  vectors     │   │ + Cohere  │  │
           └──────────────┘   │ embeddings│  │
                              └───────────┘  │
                                     ┌───────▼──────────┐
                                     │ OCI GenAI DAC    │
                                     │ Qwen3-VL-235B    │
                                     │ (QWEN_URL)       │
                                     │ Vision OCR       │
                                     └──────────────────┘
```

---

## Invocation Behavior

- **`/dox-pack-test-coverage infra`** — Read and execute `infra-tests.md` only.
- **`/dox-pack-test-coverage api`** — Read and execute `api-tests.md` only.
- **`/dox-pack-test-coverage ui`** — Read and execute `ui-tests.md` only.
- **`/dox-pack-test-coverage`** (no argument) — Execute ALL three in order: `infra-tests.md`, then `api-tests.md`, then `ui-tests.md`.

---

## Test Files

Each file is **self-contained** — it has everything needed to execute its tests without reading any other file. Load only the file for the phase you are executing.

| File | Tests | Count | Executor |
|---|---|---|---|
| `infra-tests.md` | CI-1 through CI-7 | 7 | Main agent via `kubectl` / OCI CLI |
| `api-tests.md` | CA-1 through CA-10 | 10 | Main agent via `curl` |
| `ui-tests.md` | CU-1 through CU-9 | 9 | agent-browser |

**Total: 26 tests** (7 Infra + 10 API + 9 UI)

---

## Environment Variables for Testing

| Variable | Required | Description |
|---|---|---|
| `STARTER_PACK_URL` | Yes | Base URL of the deployed dox-frontend (e.g. `https://dox-frontend.1-2-3-4.nip.io`) |
| `TEST_PDF_PATH` | For extraction tests | Path to a test PDF contract file for upload |

**Note:** No authentication required. The dox-frontend has no login.

---

## Known Issues & Stability Notes

| Issue | Impact | Mitigation |
|---|---|---|
| Qwen3-VL extraction 10-15 min | Extraction jobs take significant time due to per-page vision OCR | Use generous polling timeouts (15+ min) |
| LlamaStack startup 2-5 min | API returns 502 until pod is ready | Wait for health endpoint to respond |
| Oracle 26ai provisioning 10-20 min | Database operations fail until DB is ready | Check health endpoint after deploy |
| DAC cold start | First extraction may take longer if DAC is scaling | Allow extra time on first extraction |
| PDF page count affects duration | Large contracts (50+ pages) take proportionally longer | Use small test PDFs (5-10 pages) for smoke tests |
| No GPU on cluster | All GPU inference is on the DAC — no local NIM pods to check | Verify DAC endpoint reachability instead |

---

## Maintenance

- Re-run this skill when `blueprint_files.tf` dox_pack sections change or image versions update
- Update API inventory if dox-backend or dox-frontend images change
- IDs (CA-*, CU-*, CI-*) are stable — never renumber, only append
- If an endpoint is removed, mark `DEPRECATED` — do not delete from this spec
