---
name: complete-ai-agent-stack-deployment-self-hosted-from-scratch
description: >
  Sequences a complete, end-to-end, fully self-hosted AI agent stack
  deployment from scratch — GPU procurement/sizing for open-weight model
  serving, self-hosted LLM serving (vLLM/TGI), agent control-flow
  architecture, a self-hosted vector database for RAG, self-hosted MCP
  servers for tool access, and an evaluation/guardrails harness — with no
  managed LLM API or managed vector database anywhere in the stack. An
  integration/orchestration skill that sequences existing tool-specific
  skills in the right order and flags handoff points, explicit about the
  added GPU-procurement and operational burden versus a cloud-managed
  agent stack. Use when a user asks to "build a self-hosted AI agent stack
  with open-weight models," "run our agent on our own GPUs with no managed
  LLM API," "stand up a self-hosted vector database and MCP servers for an
  agent platform," or "give me the end-to-end sequence for a fully
  self-hosted agent deployment from GPU procurement to production."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# Complete AI Agent Stack Deployment (Self-Hosted) From Scratch

## Purpose

The cloud-managed AI agent path in this skill family leans on managed LLM
provider APIs and a managed vector database, trading infrastructure
ownership for per-token pricing and someone else's on-call rotation. This
skill is the opposite path: serving an open-weight model on GPU
infrastructure the team itself procures and operates, paired with a
self-hosted vector database and self-hosted MCP servers, with no managed
LLM API or managed vector database anywhere in the stack. The tradeoff is
real, and the sequencing risk is sharper than on the managed path: GPU
capacity has to be sized and provisioned *before* the agent's latency
budget is even meaningfully designable (unlike a managed API, where
provider-side scaling is someone else's problem), and every durability
concern a managed vector database absorbs — replication, backup, upgrade
— becomes this team's responsibility from day one. This skill sequences
that whole path — GPU procurement through evaluation — and is explicit
throughout about where the self-hosted burden actually lands.

## When to use

- Standing up a production AI agent with a hard requirement of no managed
  LLM API or managed vector database — data residency, air-gapped
  deployment, fixed-cost GPU amortization, or model-customization reasons
  all commonly drive this.
- Deciding whether a team genuinely has the GPU procurement and
  operational capacity to self-host an agent stack, versus one of the
  cloud-managed alternatives in this skill family.
- Auditing an existing self-hosted agent deployment for a skipped or
  out-of-order phase (e.g. an agent's latency budget designed before real
  serving latency was measured on actual hardware, or a self-hosted
  vector database with no replication running in production for months).
- Rebuilding a reference self-hosted agent architecture for a second team
  or environment that should follow the same proven sequence as a
  known-good first deployment.
- Honestly comparing the total cost and operational burden of this path
  against the cloud-managed alternative before committing to it.

## Prerequisites & environment

- GPU infrastructure already provisioned or provisionable — on
  Kubernetes, this means the NVIDIA GPU Operator and dedicated
  serving-shaped GPU node pools per
  [gpu-accelerator-infrastructure-for-ml-training](../../../mlops/skills/gpu-accelerator-infrastructure-for-ml-training/SKILL.md)
  (that skill's title says "for ML training" but its GPU Operator/MIG/
  node-pool guidance applies identically to inference-serving GPU
  capacity). Whether this capacity is on-prem, colocated, or
  cloud-rented-as-raw-compute, this team owns its procurement lead time
  and scaling — there is no managed API absorbing a traffic spike on its
  own.
- A self-hosting-capable serving runtime (vLLM or TGI) and the open-weight
  model checkpoint(s) already selected and downloaded, with a plan for
  where model weights are versioned and stored (not just "a directory on
  the serving node").
- A self-hosted vector database deployment target (Weaviate or Milvus,
  self-managed on Kubernetes) and its own dedicated compute/storage —
  distinct from the GPU serving nodes, since vector search is typically
  CPU/memory-bound, not GPU-bound.
- `kubectl`/`helm` if deploying on Kubernetes, and a realistic estimate of
  expected concurrent request volume and sequence length before sizing
  either the GPU serving fleet or the vector database cluster — sizing
  either without real numbers produces guesses that fail under real load.
- A decision, made deliberately and with realistic staffing in mind, about
  whether this team can actually operate GPU capacity planning, model
  serving upgrades, and vector database durability long-term — see the
  honest tradeoff called out in Common pitfalls.

## Step-by-step guidance

This is the phase sequence. Each phase links to the skill that covers its
full depth; the text here covers only the self-hosted-specific sequencing
and the operational burden each phase adds versus a managed alternative.

1. **Phase 1 — GPU infrastructure procurement and sizing.** Before
   anything else, size and provision the GPU capacity this stack will
   run on, per
   [gpu-accelerator-infrastructure-for-ml-training](../../../mlops/skills/gpu-accelerator-infrastructure-for-ml-training/SKILL.md):
   install the NVIDIA GPU Operator, and design a dedicated serving GPU
   node pool (separate from any training capacity that may share the
   cluster) sized to the model's memory footprint plus KV-cache headroom
   at expected concurrency:
   ```bash
   helm install gpu-operator nvidia/gpu-operator \
     --namespace gpu-operator --create-namespace --set mig.strategy=mixed
   kubectl taint nodes -l gpu-pool=agent-serving workload=serving:NoSchedule
   ```
   This has no equivalent phase at all on the cloud-managed path — a
   managed LLM API absorbs this entirely. Treat GPU procurement lead time
   (physical hardware or committed cloud GPU capacity) as a hard blocking
   dependency for every phase that follows, not something to start in
   parallel with agent-architecture work.

2. **Phase 2 — self-hosted LLM serving.** Deploy the chosen open-weight
   model with vLLM or TGI on the Phase 1 GPU pool, applying the
   batching-aware LLM serving guidance from
   [model-serving-and-scaling](../../../mlops/skills/model-serving-and-scaling/SKILL.md)
   (that skill's LLM-specific guidance on continuous batching and
   KV-cache sizing applies directly here, even though it lives in the
   MLOps domain):
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata: { name: agent-llm-server }
   spec:
     template:
       spec:
         nodeSelector: { gpu-pool: agent-serving }
         containers:
           - name: vllm
             image: vllm/vllm-openai:latest
             args: ["--model", "<OPEN_WEIGHT_MODEL_ID>", "--tensor-parallel-size", "1"]
             resources: { limits: { nvidia.com/gpu: 1 } }
   ```
   **Measure real serving latency on this actual hardware before Phase 3
   finalizes the agent's iteration cap and per-step timeout** — a latency
   budget designed against an assumed number, rather than the real
   measured p95 on the Phase 1 hardware, is the most common self-hosted-
   specific design error in this sequence (see Common pitfalls).

3. **Phase 3 — agent architecture design.** Design the control loop,
   termination condition, iteration cap, wall-clock timeout, and tool-
   boundary classification per
   [agent-architecture-design](../agent-architecture-design/SKILL.md),
   using the Phase 2 measured latency (not an assumed managed-API
   latency figure) to set realistic per-call timeouts and the overall
   loop's wall-clock budget.

4. **Phase 4 — self-hosted vector database and RAG pipeline.** Design
   the chunking/embedding/retrieval pattern per
   [rag-pipeline-design](../rag-pipeline-design/SKILL.md), then deploy a
   self-hosted Weaviate or Milvus cluster per
   [vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md)'s
   self-hosted guidance — sized, sharded, and **replicated** from the
   start:
   ```python
   # Milvus collection replication (self-hosted — no managed-service
   # durability behind this unless explicitly configured)
   collection: agent_knowledge_base
   replica_number: 2   # survives one query-node loss without downtime
   ```
   Unlike a managed vector database, replication, backup, and capacity
   planning here are entirely this team's responsibility — a
   single-replica self-hosted index has no vendor SLA behind it at all.

5. **Phase 5 — self-hosted MCP servers.** Build and deploy MCP servers
   for tool access per
   [mcp-server-development](../mcp-server-development/SKILL.md), on
   network infrastructure segmented from the Phase 1/2 GPU serving
   cluster's internal network — an MCP server sharing an unsegmented
   network with the model-serving control plane gives a compromised tool
   call a much larger blast radius than the tool's documented scope
   suggests. Scope each server's backend credential to least privilege,
   independent of any broad credential the GPU cluster's own service
   accounts might otherwise have.

6. **Phase 6 — evaluation harness and guardrails.** Build the offline
   eval set and runtime guardrail layer per
   [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md)
   before Phase 2–5's full stack serves real traffic, including
   adversarial cases for RAG-content injection (Phase 4) and MCP-tool-
   output injection (Phase 5), exactly as on the cloud-managed path — the
   injection risk itself doesn't change because the model is self-hosted.

7. **Phase 7 — cost and utilization monitoring.** Unlike the cloud-
   managed path's per-token provider billing, self-hosted cost is
   dominated by GPU capital/amortized cost and utilization, not per-call
   spend — apply the structural levers from
   [llm-cost-and-latency-optimization](../../../ai-agent/skills/llm-cost-and-latency-optimization/SKILL.md)
   (context trimming, batching, right-sized models per step) alongside
   GPU utilization monitoring (`DCGM_FI_DEV_GPU_UTIL`) from the Phase 1
   GPU infrastructure layer. A self-hosted GPU fleet sitting at 15%
   utilization between bursty agent traffic can easily cost more in
   amortized terms than the managed-API alternative would have — this
   is a real total-cost-of-ownership comparison to make explicitly, not
   an assumption that self-hosting is automatically cheaper.

## Best practices

- Treat GPU procurement (Phase 1) as the hard, lead-time-bound
  prerequisite it is — every other phase's design decisions (Phase 3's
  latency budget especially) depend on real measured numbers from this
  phase, not estimates made in parallel with it.
- Measure real serving latency and throughput on the actual Phase 1/2
  hardware before finalizing any agent-loop timeout in Phase 3 — a
  self-hosted serving stack's latency characteristics differ enough from
  a managed API's that assumptions carried over from the managed path
  are unreliable here.
- Set a replication factor of at least 2 on the self-hosted vector
  database (Phase 4) from the start — there is no managed-service
  failover behind a self-hosted single-replica index, and this is a
  cheap decision to make before go-live versus after a first outage.
- Segment MCP servers' (Phase 5) network access from the GPU
  serving/training cluster's internal network deliberately — don't treat
  "it's all internal infrastructure" as equivalent to "it's all one
  trust boundary."
- Model the total cost of the self-hosted stack (Phase 7) including GPU
  idle time between bursts, not just a per-token comparison against the
  managed-API alternative — the honest comparison is total cost of
  ownership, not sticker price per call.
- Version model checkpoints, vLLM/TGI server configuration, and vector
  database schema/replication settings in one repository, exactly as
  rigorously as a registered model artifact would be versioned on the
  MLOps side of this repo — a self-hosted stack has no vendor console
  showing "what's currently deployed."

## Common pitfalls

- **Symptom:** The agent's control loop (Phase 3) frequently times out
  mid-task, even though the same design worked fine when prototyped
  against a managed LLM API.
  **Fix:** The per-call timeout and iteration cap were carried over from
  assumptions valid for a managed API's latency profile, not the actually
  measured p95 latency of the Phase 2 self-hosted serving stack on the
  Phase 1 hardware — re-measure real serving latency under realistic
  concurrency and re-tune Phase 3's budget against those numbers.

- **Symptom:** A routine node restart or upgrade on the self-hosted
  vector database causes a multi-minute outage for every agent query
  that needs retrieval.
  **Fix:** Phase 4's vector database was deployed with no replication
  (or a replication factor of 1), unlike a managed vector database which
  handles this transparently. Set a replication factor of at least 2
  before cutover, not after the first maintenance-window outage.

- **Symptom:** A compromised or manipulated MCP tool call reaches
  infrastructure far beyond its documented tool surface, including
  parts of the model-serving control plane.
  **Fix:** Phase 5's MCP servers were deployed on the same unsegmented
  network as the Phase 1/2 GPU serving cluster, with no network policy
  isolating them. Segment MCP server network access independently of the
  ML infrastructure's internal network, regardless of how convenient
  sharing it was during initial setup.

- **Symptom:** Total infrastructure spend for the self-hosted stack ends
  up higher than the cloud-managed alternative would have cost for the
  same traffic volume, contrary to the assumption that self-hosting is
  always cheaper.
  **Fix:** Phase 7's cost model only compared a rough per-token estimate
  against managed-API pricing, without accounting for GPU idle time
  between bursty agent traffic. Model utilization explicitly — a GPU
  fleet provisioned for peak load but averaging low utilization between
  bursts often costs more in amortized terms than metered managed-API
  usage would have for the same real traffic pattern.

- **Symptom:** An eval suite that passed cleanly before launch fails to
  catch a real regression introduced when the open-weight model
  checkpoint was updated in place.
  **Fix:** The self-hosted model checkpoint was swapped without version
  pinning or re-running the Phase 6 eval suite against the new
  checkpoint — treat every checkpoint change exactly like a registered
  model version change on the MLOps side of this repo: pin it, and
  re-run the full eval suite before it replaces the serving deployment.

## Worked example

**Scenario:** A defense-adjacent company must run its internal
engineering-assistant agent entirely on-premises with no managed LLM API
or managed vector database, using an open-weight model on their own GPU
cluster.

```bash
# Phase 1 — GPU procurement: 4x A100-80GB nodes provisioned on-prem,
# GPU Operator installed, dedicated agent-serving node pool tainted
helm install gpu-operator nvidia/gpu-operator --namespace gpu-operator --create-namespace
kubectl taint nodes gpu-node-01 gpu-node-02 workload=serving:NoSchedule

# Phase 2 — vLLM serving the chosen open-weight model on the serving pool
kubectl apply -f agent-llm-vllm-deployment.yaml
# real p95 measured under expected concurrency: 2.8s per generation step

# Phase 3 — ReAct-style agent loop, iteration cap and per-call timeout
# tuned against the Phase 2 measured 2.8s p95 (not an assumed managed-API number)
MAX_ITERATIONS = 10
PER_CALL_TIMEOUT_SECONDS = 8   # real p95 + margin, not a guess

# Phase 4 — self-hosted Milvus, replica_number=2, RAG design decided first
collection: engineering_docs
replica_number: 2

# Phase 5 — self-hosted MCP servers on a segmented network, separate from
# the GPU cluster's internal network, least-privilege backend credentials

# Phase 6 — 50-case eval suite including RAG-injection and MCP-tool-output
# injection adversarial cases, passing before wide internal rollout

# Phase 7 — GPU utilization dashboard (DCGM) alongside token-cost tracking;
# utilization holds at ~55% average across business hours, confirmed as a
# reasonable total-cost-of-ownership tradeoff versus the managed-API
# alternative that was priced out before committing to this path
```

Two months in, a scheduled node maintenance window restarts one Milvus
node; because Phase 4's replication factor was set to 2 from the start,
agent queries continue serving without interruption from the remaining
replica — the exact failure mode this skill's Common pitfalls section
flags as catastrophic on a single-replica self-hosted deployment.

## Cross-references

- [gpu-accelerator-infrastructure-for-ml-training](../../../mlops/skills/gpu-accelerator-infrastructure-for-ml-training/SKILL.md) — Phase 1's GPU Operator install and serving node pool design (its guidance applies to inference-serving capacity, not only training).
- [model-serving-and-scaling](../../../mlops/skills/model-serving-and-scaling/SKILL.md) — Phase 2's vLLM/TGI batching-aware LLM serving mechanics.
- [agent-architecture-design](../agent-architecture-design/SKILL.md) — Phase 3's control-loop, termination, and tool-boundary design.
- [rag-pipeline-design](../rag-pipeline-design/SKILL.md) — Phase 4's chunking/embedding/retrieval design.
- [vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md) — Phase 4's self-hosted Weaviate/Milvus sizing, sharding, and replication.
- [mcp-server-development](../mcp-server-development/SKILL.md) — Phase 5's tool-server build, network segmentation, and credential scoping.
- [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md) — Phase 6's offline eval harness and runtime guardrails.
- [llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md) — Phase 7's structural cost/latency levers, applied alongside GPU utilization monitoring.
- [complete-ai-agent-stack-deployment-cloud-managed-from-scratch](../complete-ai-agent-stack-deployment-cloud-managed-from-scratch/SKILL.md) — the managed-service alternative to this entire path, for comparing total cost and operational burden before choosing between them.
