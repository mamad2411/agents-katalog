---
name: agent-observability-test-coverage
description: Authoritative test specification for the Agent Observability (Langfuse) starter pack. Documents the Langfuse dashboard UI, the Langfuse public API + LlamaStack OpenAI-compatible API (incl. the OCI GenAI DAC model), and infrastructure (HA ClickHouse, managed Postgres/Redis/Object Storage, GenAI endpoint). Split into phase-specific files.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, WebFetch, Write, Edit
argument-hint: [section] (optional — "api", "ui", "infra", or omit to run all three)
---

# Agent Observability (Langfuse) — Test Coverage Specification

Source of truth for what to test on a deployed `agent_observability` stack. Covers the **Langfuse** web app (traces/evals/prompts/dashboards), the **LlamaStack** OpenAI-compatible gateway fronting the **OCI GenAI Dedicated AI Cluster (DAC)** model, and the managed/in-cluster backing services.

**Frontend/UI:** Langfuse v3 web app (`langfuse/langfuse:3`) — its own dashboard; no custom frontend.
**Inference gateway:** LlamaStack (`…/llama-stack-oci:pr-d74b10d`) — OpenAI-compatible API; serves the OCI GenAI catalog **and** the dedicated DAC model.
**Transactional DB:** OCI Database with PostgreSQL (managed, HA).
**Cache/queue:** OCI Cache (managed Redis, TLS).
**Blob storage:** OCI Object Storage (S3-compatible) — Langfuse events/media.
**OLAP:** ClickHouse via the Altinity clickhouse-operator — 1 shard × 2 replicas + 3-node Keeper.
**Agentic model:** OCI GenAI endpoint — `existing` (bring an endpoint OCID) or `create` (DAC + HF import, default `Qwen/Qwen3.6-35B-A3B` on `H100_X2`).
**Deployment:** Terraform → OKE (CPU-only) → Corrino blueprint deployment-group (`langfuse-web`, `langfuse-worker`, `llamastack`) + managed OCI services provisioned in TF.

**Note:** Agent Observability is CPU-only on OKE — the GPU lives in the managed OCI GenAI DAC, not on the cluster.

---

## Test Files

Each file is **self-contained** — it has everything needed to execute its tests without reading any other file. Load only the file for the phase you're executing.

| File | Tests | Count | Executor |
|---|---|---|---|
| `infra-tests.md` | AOI-1 through AOI-12 | 12 | Main agent via `kubectl` / OCI CLI |
| `api-tests.md` | AOA-1 through AOA-10 | 10 | Main agent via `curl` |
| `ui-tests.md` | AOU-1 through AOU-14 | 14 | agent-browser |

**Total: 36 tests** (12 Infra + 10 API + 14 UI)

---

## Invocation Behavior

- **`/agent-observability-test-coverage infra`** — Read and execute `infra-tests.md` only.
- **`/agent-observability-test-coverage api`** — Read and execute `api-tests.md` only.
- **`/agent-observability-test-coverage ui`** — Read and execute `ui-tests.md` only.
- **`/agent-observability-test-coverage`** (no argument) — Execute ALL three in order: `infra-tests.md`, then `api-tests.md`, then `ui-tests.md`.

---

## Environment Variables for Testing

| Variable | Required | Description |
|---|---|---|
| `STARTER_PACK_URL` | Yes (api/ui) | Langfuse UI base URL, from the `starter_pack_url` output (e.g. `https://langfuse.1-2-3-4.nip.io`). |
| `LLAMASTACK_URL` | Yes (api) | LlamaStack base URL **without** `/v1` (e.g. `https://llamastack.1-2-3-4.nip.io`). Same `<fqdn>` as `STARTER_PACK_URL`, `llamastack` subdomain. |
| `LANGFUSE_PUBLIC_KEY` | Yes (api) | From the `langfuse_project_public_key` output (`pk-lf-…`). |
| `LANGFUSE_SECRET_KEY` | Yes (api) | From the `langfuse_project_secret_key` output (`sk-lf-…`, sensitive). |
| `ADMIN_EMAIL` | Yes (ui) | `corrino_admin_email` — bootstrapped Langfuse admin login. |
| `ADMIN_PASSWORD` | Yes (ui) | `corrino_admin_password` — bootstrapped Langfuse admin login. |
| `KUBECONFIG` | Yes (infra) | kubeconfig for the OKE cluster (`oci ce cluster create-kubeconfig … --kube-endpoint PUBLIC_ENDPOINT`). |
| `OCI_CLI_PROFILE` | Yes (infra) | OCI CLI profile for the deploy tenancy/region. |

Auth keys are auto-provisioned at deploy — read them from stack outputs rather than the UI:
`oci resource-manager job get-job-logs-content --job-id <apply-job> | grep langfuse_project_`.

---

## Architecture Components

| Component | Port | Purpose |
|---|---|---|
| Langfuse web (`langfuse/langfuse:3`) | 3000 | Dashboard + public ingestion/API. Subdomain `langfuse`. N replicas. |
| Langfuse worker (`langfuse/langfuse-worker:3`) | 3030 | Async event processing. No ingress. |
| LlamaStack (`…/llama-stack-oci:pr-d74b10d`) | 8321 | OpenAI-compatible API (`/v1`). Subdomain `llamastack`. Serves the DAC model. |
| ClickHouse (Altinity operator) | 8123/9000 | OLAP store. Service `clickhouse-langfuse.clickhouse.svc`. 1 shard × 2 replicas. |
| ClickHouse Keeper | 2181 | Replication coordination. Service `keeper-langfuse.clickhouse.svc`. 3 nodes. |
| OCI Database with PostgreSQL | 5432 | Langfuse transactional store (managed, HA). |
| OCI Cache (Redis, TLS) | 6379 | Event queue (`rediss://`). |
| OCI Object Storage (S3) | — | Langfuse `events/` + `media/` blobs (versioning enabled). |
| OCI GenAI endpoint | 443 | Agentic model inference (DAC or existing). |

**Ingress routes:** `/` (on `langfuse.<fqdn>`) → langfuse-web:3000; `/v1/*` (on `llamastack.<fqdn>`) → llamastack:8321. TLS via cert-manager + LetsEncrypt.

**Key flows:** (1) instrument an agent with the Langfuse SDK → traces land; (2) agent calls a model via LlamaStack (DAC or catalog) → captured as generations; (3) view traces/dashboards in the Langfuse UI; (4) optional OIDC SSO login.

---

## Known Issues & Stability Notes

| Issue | Impact | Mitigation |
|---|---|---|
| **Reasoning model token cap** | A small `max_tokens`/`max_completion_tokens` on the default `Qwen3.6-35B-A3B` truncates mid-reasoning → DAC returns **HTTP 500** | Omit the cap or set ≥ ~4096. `max_tokens` is deprecated → use `max_completion_tokens`. |
| OpenAI-compat path | `/v1/openai/v1/...` returns Not Found | Use `/v1/chat/completions`. |
| DAC model id is dynamic | Derived from the endpoint display name + deploy id (`Qwen3-6-35B-A3B-endpoint-<hex>`) | Discover from `/v1/models` (the entry whose `provider_resource_id` contains `generativeaiendpoint`); don't hard-code. |
| Langfuse startup | `/api/public/health` 502 until web migrates Postgres + ClickHouse | Wait for health OK (can be several min after pods Running). |
| Managed PSQL/Redis provisioning | 10-20 min; `langfuse-secrets` not created until their FQDNs resolve | Blueprint deploy waits on the secret (ordering fix). |
| ClickHouse HA needs Keeper 25.8 | Keeper 24.8 crashes (`use_xid_64`); replicated tables need Keeper quorum | Server+keeper pinned to 25.8. |
| Object Storage versioning | Bucket fills with versioned trace blobs | Teardown must force-empty (see BUG-040). |

---

## Maintenance

- Re-run this skill when `agent_observability_blueprint.tf`, `langfuse_*.tf`, or the image versions change.
- IDs (AOA-*, AOU-*, AOI-*) are stable — never renumber, only append. Mark removed checks `DEPRECATED`, don't delete.
- Cross-references: pack overview `docs/packs/agent_observability.md`; agent how-to `docs/packs/agent_observability/connect-an-agent.md`; teardown gaps `BUGS.md` BUG-040.
