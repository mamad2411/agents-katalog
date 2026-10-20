---
name: llm-app-deployer
description: >-
  Take an LLM application from prototype to production. Use when the user says
  "deploy my LLM app", "dockerize my RAG service", "ship the chatbot to AWS",
  "my LLM prototype needs to go live", "production container for AI app",
  "containerize my FastAPI LLM service", "push my chatbot image to a registry",
  "run my assistant on EC2", or "vector DB production tuning". Covers
  extracting a notebook/CLI prototype into a REST microservice, moving local
  state (vector store, chat history, tracing) to managed cloud services,
  building a lean multi-stage production Docker image (uv, non-root,
  Gunicorn+Uvicorn, runtime secrets), IAM/budget hygiene, registry push and
  compute rollout, a scaling ladder from single VM to orchestrated containers,
  and vector-store tuning (precision@k benchmarking, HNSW hnsw_ef sweeps,
  quantization with rescoring). Also triggers on "image too big", "secrets in
  Docker image", "Qdrant slow in prod", or "when do I need Kubernetes for my
  LLM app".
---

# LLM App Deployer

## Purpose

Promote a working LLM prototype — notebook, CLI loop, or dev script — into a production service: an API microservice in a container, backed by managed stateful services, running on cloud compute, with its vector store tuned against a measured accuracy baseline. The skill encodes a 4-step promotion (API-ify → externalize state → containerize → deploy) plus the tuning and scaling decisions that follow.

Use it when the request is about *shipping* an LLM app, not building one. Concrete tools below (FastAPI, uv, Gunicorn, AWS ECR/EC2, Qdrant, Redis) are worked examples — substitute the user's actual framework, registry, compute, and stores in each slot.

## Core model

**The assistant is a microservice.** In production, the LLM app is one decoupled service in a larger system, spoken to only via REST. Identity comes from the caller: `user_id` and `session_id` arrive in the request from the main backend (which owns accounts and may provision per-user LLM budgets, e.g. LiteLLM virtual keys at signup) — never generated inside the LLM service. Prototype-era interactivity (input loops, goodbye/exit handling) is deleted, not ported.

**State lives outside the container.** Containers are disposable; anything that must survive a restart moves to a managed service. The standard slots:

| Slot | Local prototype | Managed example |
|---|---|---|
| Vector store | local Qdrant / in-memory | Qdrant Cloud (URL + API key) |
| History / cache | local Redis | Redis Cloud (`redis://user:pass@host:port/0`) |
| Tracing / prompts | self-hosted Langfuse | Langfuse Cloud (`LANGFUSE_HOST`) |
| LLM gateway | local LiteLLM proxy | self-run on its own VM or a PaaS |

The IaaS-vs-SaaS framing: IaaS gives maximum control at maximum ops burden; SaaS/managed tiers hand scaling and patching to the provider at the cost of control — a real concern for data-sensitive workloads, so choose explicitly per slot. Connection changes stay *localized*: swapping local for managed touches only the client-construction call (URL + key from env), nothing downstream.

**Secrets are runtime inputs.** Keys never appear in code, in the image, or in git. `.env` is templated (`.env.template` committed, `.env` ignored and dockerignored), injected with `docker run --env-file`, and read via `os.environ`. The gateway pattern from the same family: point the OpenAI-compatible client's `base_url` at your LLM proxy endpoint so the provider is swappable by env alone.

**Tune the query side before the index side.** For vector stores, the exact k-NN search is ground truth and ANN is the production approximation. Search-time parameters (Qdrant's `hnsw_ef`, quantization rescoring) can be moved in production with no reindex; build-time parameters (`m`, `ef_construct`) require a rebuild and are a separate, heavier lever. Every tuning change is judged against a precision@k benchmark, never by vibes.

**Climb the scaling ladder only on evidence.** Single VM → load balancer + replicas → serverless adapter → orchestrated containers. Each rung adds ops surface; climb when the current rung measurably fails (step 9), not preemptively.

## Workflow

Work the steps in order; each has a verifiable exit condition.

### 1. Extract the service API

- Define the request schema with caller-supplied identity:

  ```python
  class QueryRequest(BaseModel):
      user_input: str
      user_id: str      # supplied by the main backend
      session_id: str   # drives history retrieval + usage attribution
  ```

- Expose one endpoint (e.g. `POST /ask`) that runs guardrails/input validation *before* any chain call, then the chain, then returns the answer.
- Delete CLI-era code paths (exit chains, interactive prompts). Keep tools (e.g. a retrieval tool) and build heavy resources like the vector store lazily on first use.
- Dev run: `uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)`.
- Preserve tracing across the move: the observability decorators, parent span, and `session_id`/`user_id` attribute propagation from the eval phase must still fire in the service — see `llm-evals-engineer`.
- **Exit:** local `POST /ask` with a real `user_id`/`session_id` returns an answer and produces a trace.

### 2. Externalize state to managed services

- For each slot in the Core-model table, create the managed instance ([vector store cloud cluster], [managed cache/history DB], [hosted tracing project]) and record URL + credentials in `.env`.
- Migrate vector data by re-embedding on first run or by snapshot upload from the local instance.
- Change only the connection call, e.g.:

  ```python
  QdrantVectorStore.from_existing_collection(
      url=os.environ["QDRANT_URL"], api_key=os.environ["QDRANT_API_KEY"],
      embedding=embeddings_model, collection_name=collection_name)
  ```

- The LLM gateway/proxy typically stays self-run (own VM or PaaS); apps point at it via `base_url` env.
- **Exit:** app runs locally with *zero* local stateful dependencies.

### 3. Build the production container

- `.dockerignore` first: `.git`, `__pycache__`, `.venv`, `.env` / `*.env`, IDE dirs, logs, build artifacts. Smaller context, and secrets can never enter the image.
- Modern packaging with a lockfile (uv shown). Split dependency install from source copy so the deps layer rebuilds only when the lockfile changes:

  ```dockerfile
  FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
  ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
  WORKDIR /app
  COPY pyproject.toml uv.lock ./
  RUN --mount=type=cache,target=/root/.cache/uv \
      uv sync --frozen --no-install-project --no-dev
  COPY . /app
  RUN --mount=type=cache,target=/root/.cache/uv \
      uv sync --frozen --no-dev

  FROM python:3.13-slim
  RUN useradd --create-home appuser
  COPY --from=builder --chown=appuser /app /app
  USER appuser
  WORKDIR /app
  ENV PATH="/app/.venv/bin:$PATH"
  CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", \
       "--bind", "0.0.0.0:8000", "--workers", "2", "--preload", "main:app"]
  ```

  Why each piece: multi-stage keeps build toolchain out of the runtime image (only the venv and app cross over); `UV_COMPILE_BYTECODE=1` precompiles for faster cold starts; `UV_LINK_MODE=copy` makes linking behave across container filesystems; non-root user limits blast radius; Gunicorn is the process manager over async Uvicorn workers (`--preload` loads app code before forking) — never bare dev-server in prod.
- Size check: for this stack expect roughly **600–700 MB**. Meaningfully larger usually means a fat base image, dev dependencies, or build-context leaks — and it matters: private-registry free tiers cap image size (e.g. private ECR at 500 MB) and big images slow every pull.
- **Exit:** `docker run --env-file .env -p 8000:8000 [image:tag]` serves correct answers locally; `docker images` confirms size.

### 4. Cloud account hygiene (before anything runs)

- Zero-spend (or low-threshold) budget alarm first.
- Never operate as the root account: MFA on root, create an IAM admin user and work as it; least-privilege users for narrow tasks; access keys only for the CLI user.
- **Exit:** billing alarm active; root untouched since setup.

### 5. Push to a registry

- Choose deliberately: public repo (e.g. public ECR — free, no size cap concern) vs private (access control, but e.g. 500 MB free-tier cap) vs Docker Hub.
- Flow: `docker login` → `docker tag <image> [registry]/<image>:<tag>` → `docker push` (managed registries display their exact per-repo commands).
- **Exit:** image pullable from a clean machine.

### 6. Provision compute and deploy

- Smallest viable VM (e.g. free-tier `t2.micro`/`t3.micro`, Ubuntu/Debian AMI), SSH key pair, security group allowing SSH + HTTP(S). Note: the public IP changes across restarts unless you attach a static one.
- Install Docker **Engine** (not Desktop); add your user to the `docker` group to drop sudo.
- Recreate `.env` by hand on the box — it was never in the image or the repo.
- Run:

  ```bash
  docker run -d -p 80:8000 --name [service-name] --restart always \
      --env-file ./.env [registry-image]
  ```

  `--restart always` survives crashes and daemon restarts; host port 80 exposes the API publicly.
- If self-running the LLM proxy, give it its own VM and point apps at `http://<proxy-ip>:4000` via env.
- **Exit:** `http://<vm-ip>/docs` loads from the public internet.

### 7. Smoke test end to end

- Real request with real `user_id`/`session_id` from outside the cloud network; verify the answer, the trace in the hosted tracing project, history persistence in the managed store, and guardrail rejection of a known-bad input.
- **Exit:** all four observed, not assumed.

### 8. Tune the vector store against a benchmark

- Build the harness: for each of [~100 test queries] with precomputed embeddings, run ANN (`limit=10`) and exact search (`SearchParams(exact=True)`); `precision@10 = |ANN ∩ exact| / 10`; record mean precision and per-query latency. Exact search is too slow to serve but is the accuracy ground truth.
- **Query-side knob (no reindex):** sweep `hnsw_ef` over `[10, 20, 50, 100, 200]` via `SearchParams(hnsw_ef=...)`. Larger ef → wider candidate queue → higher precision, higher latency. Pick the smallest value meeting your precision target.
- **Build-time knobs (reindex required):** `m` and `ef_construct` shape the graph itself — a separate, heavier lever; changing them rebuilds the index, so exhaust query-side tuning first.
- **Quantization** (quantized vectors stored alongside originals): scalar int8 is the accuracy-safe default (~2× speed, ~4× storage); product compresses hardest but can cost real accuracy; binary is extreme and model-dependent (validated mainly for ada-002 / Cohere) — benchmark before adopting. Apply live:

  ```python
  client.update_collection(collection_name=...,
      optimizer_config=models.OptimizersConfigDiff(),
      quantization_config=models.ScalarQuantization(
          scalar=models.ScalarQuantizationConfig(
              type=models.ScalarType.INT8, quantile=0.99, always_ram=False)))
  ```

  `quantile=0.99` clips outliers so they don't stretch the int8 range; `always_ram=False` lets quantized vectors page from disk. At query time, `QuantizationSearchParams(ignore=True)` keeps ground-truth runs honest; `rescore=True, oversampling=2.0` fetches 2× candidates via quantized vectors then re-ranks with originals — benchmark rescore on vs off.
- **Exit:** a table of (config, precision@10, latency) and a chosen config with rationale.

### 9. Set scaling-ladder triggers

Write down, now, the conditions that justify each climb:

1. **Load balancer + VM replicas** — when a single VM saturates CPU/memory at peak, or uptime requires surviving one instance loss. Buys HA, horizontal scale, managed TLS.
2. **Serverless adapter** (e.g. Lambda + API Gateway via Mangum) — when traffic is spiky or low and paying for an idle VM is the dominant cost. Buys zero server ops, pay-per-use; watch cold starts.
3. **Orchestrated containers** (e.g. ECS/EKS, Fargate to skip node management) — when you run multiple microservices, need automated deploys/scaling/service discovery/health management, or sustain high traffic. Most robust, most ops surface.

**Exit:** triggers documented next to the deployment; no preemptive climbing.

## Guardrails

- **Never bake secrets.** No keys in code, Dockerfile, image layers, or git history. `.env` in `.dockerignore` *and* `.gitignore`; inject via `--env-file` or the platform's secret store. If a key ever entered a layer or commit, rotate it — deleting the file later does not remove it from history.
- **No root — container or cloud.** Containers run as a dedicated non-root user; cloud work happens as an IAM user with MFA-protected root left idle. Budget alarm before the first billable resource.
- **Identity comes from the caller.** The service must not mint `user_id`/`session_id`; accepting them from the request is what makes history, personalization, and cost attribution correct.
- **Guardrails before the chain.** Input validation/rails run before any model or tool call in the endpoint — moving to a service must not reorder this.
- **Evals gate the deploy.** Do not promote a build whose eval suite (see `llm-evals-engineer`) hasn't passed, and verify tracing survived the migration — a service that went dark observationally is not deployed, it's abandoned.
- **Benchmark before believing.** No vector-store parameter change ships without a before/after precision@k + latency measurement. Distinguish clearly for the user which knobs are query-time (`hnsw_ef`, rescoring) and which force a reindex (`m`, `ef_construct`, re-embedding).
- **Dev servers are not prod servers.** Bare `uvicorn --reload` (or any framework dev server) never reaches production; use a process manager with multiple workers.
- **Flag the size regression.** If the image lands far above the ~600–700 MB expectation for a Python LLM stack, diagnose (base image, dev deps, context leaks) before pushing.
- **Escalate org-level concerns.** SSO, org-wide IAM policy, network segmentation, compliance for data-sensitive workloads are beyond this skill — hand off to `platform-security-playbook` when the deployment goes enterprise.

## Suggested effort

- **Typical engagement** (prototype → live on one VM, steps 1–7): a focused multi-session effort; budget most of it on steps 2–3, where connection refactors and Dockerfile iteration dominate.
- **Vector tuning** (step 8): a self-contained session once a test-query set with embeddings exists; building that set is the long pole, the sweeps are quick.
- **Fast path:** if the app is already a containerized API, start at step 4 and compress 4–7 into one session.
- **Stop and ask** when: the workload is data-sensitive and the SaaS-vs-IaaS choice isn't yours to make; monthly cloud spend beyond free tier is implied; or the user asks for rung 2–3 of the scaling ladder without evidence rung 1 has failed.
