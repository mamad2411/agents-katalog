---
name: cuopt-test-coverage
description: Authoritative test specification for the cuOpt (Vehicle Delivery Route Optimizer) starter pack. Documents API endpoints, UI interactions, chat flows, and infrastructure components. Split into phase-specific files.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, WebFetch, Write, Edit
argument-hint: [section] (optional — "api", "ui", "infra", or omit to run all three)
---

# Vehicle Delivery Route Optimizer — Test Coverage Specification

Source of truth for what to test on a deployed cuOpt stack. Covers the cuOpt interactive frontend (React SPA), the NVIDIA cuOpt solver backend, LlamaStack LLM service, and OCI infrastructure.

**Frontend repo:** `oci-ai-incubations/vehicle_route_optimizer_frontend` (React 18, Vite 7, MUI 5, Leaflet, Axios)
**Backend:** NVIDIA cuOpt 25.10.0 — vehicle routing optimization solver (GPU-accelerated)
**LLM:** LlamaStack — OpenAI-compatible chat completions with function calling
**Deployment:** Terraform → OKE → Corrino Blueprint (3-service deployment group: cuopt + llamastack + demo frontend)

---

## Test Files

Each file is **self-contained** — it has everything needed to execute its tests without reading any other file. Load only the file for the phase you're executing.

| File | Tests | Count | Executor |
|---|---|---|---|
| `api-tests.md` | CA-1 through CA-7 | 7 | Main agent via `curl` |
| `ui-tests.md` | CU-1 through CU-20 | 18 | agent-browser |
| `infra-tests.md` | CI-1 through CI-7 | 7 | Main agent via `kubectl` / OCI CLI |

**Total: 32 tests** (7 API + 18 UI + 7 Infra)

---

## Invocation Behavior

- **`/cuopt-test-coverage infra`** — Read and execute `infra-tests.md` only.
- **`/cuopt-test-coverage api`** — Read and execute `api-tests.md` only.
- **`/cuopt-test-coverage ui`** — Read and execute `ui-tests.md` only.
- **`/cuopt-test-coverage`** (no argument) — Execute ALL three in order: `infra-tests.md`, then `api-tests.md`, then `ui-tests.md`.

---

## Environment Variables for Testing

| Variable | Required | Description |
|---|---|---|
| `STARTER_PACK_URL` | Yes | Base URL of the deployed cuOpt frontend (e.g. `https://demo-cuopt.1-2-3-4.nip.io`) |

**Note:** No authentication is required. The cuOpt frontend has no login.

---

## Architecture Components

| Component | Port | Purpose |
|---|---|---|
| cuOpt Frontend (React SPA) | 3000 | Single-page app — problem config, map, chat, results |
| cuOpt Solver (NVIDIA) | 5000 | GPU-accelerated vehicle routing optimizer — `/cuopt/request`, `/cuopt/solution/{id}` |
| LlamaStack (LLM) | 8321 | OpenAI-compatible chat completions with function calling — `/v1/chat/completions`, `/v1/models` |

**Ingress route mapping (via Corrino blueprint):**
- `/` → demo frontend (port 3000)
- `/cuopt/*` → cuOpt solver (port 5000)
- `/v1/*` → LlamaStack (port 8321)

**Frontend is a SPA** — single page at `/` with three tabs: Problem, Map, Settings. No client-side routing.

**Key user flows:**
1. View default problem (6 deliveries, 2 vehicles in Austin TX)
2. Click "Find Optimal Routes" → solver returns vehicle routes + dropped tasks
3. Chat with AI to modify problem (add vehicles, add stops, change capacities)
4. AI auto-solves after modifications
5. View results: route segments, capacity utilization, dropped task explanations

---

## Known Issues & Stability Notes

| Issue | Impact | Mitigation |
|---|---|---|
| cuOpt solver cold start on GPU | First solve after deploy may be slow (30-60s) | Allow extra time on first solve |
| LlamaStack model loading | `/v1/models` returns empty until model is ready | Wait for model list to populate before chat tests |
| Function calling fallback | LLM may not support tools → falls back to prompt-based | Both paths should work; test with tool_choice=auto first |
| Map "COMING SOON" overlay | Map tab has a banner overlay — map is still interactive underneath | Expected behavior, not a bug |
| NIM pod startup 15-30 min | GPU pods need time to load models | Wait for all blueprint pods Running before testing |
| Solver timeout 5 minutes | Polling `/cuopt/solution/{id}` up to 300 attempts (1/sec) | Set test timeouts accordingly |

---

## Maintenance

- Re-run this skill when `blueprint_files.tf` cuopt sections change or frontend image version updates
- IDs (CA-*, CU-*, CI-*) are stable — never renumber, only append
- If an endpoint is removed, mark `DEPRECATED` — do not delete from this spec
