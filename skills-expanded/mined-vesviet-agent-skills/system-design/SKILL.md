---
name: system-design
description: Design, specify, and document complex system architectures covering compute, network, storage, middleware, and AI inference layers. Translate NFRs into measurable infrastructure targets and produce capacity models. Use when designing or reviewing system topology, sizing infrastructure, planning capacity, or specifying AI infrastructure (GPU, inference servers, vector databases).
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# System Design

Use this skill when designing system topology for a new service or infrastructure layer, translating non-functional requirements into engineering specifications, planning capacity for growth, or architecting AI inference infrastructure.

## When to Use

- a new system, environment, or service needs infrastructure topology specified before implementation
- non-functional requirements (latency, throughput, availability, scalability) need translating into measurable engineering targets
- capacity planning is needed for known or forecast growth
- AI inference infrastructure (GPU allocation, inference server, vector database) needs to be designed or selected
- an existing system needs a performance or capacity review
- infrastructure decisions require documented trade-off analysis

## Core Rules

- every design decision must trace to a measurable NFR or explicit business requirement — "best practice" alone is not a rationale
- do not accept vague NFRs (e.g., "the system should be fast"); return unmeasurable NFRs for clarification before producing a design
- all infrastructure changes must be committed to IaC (Terraform, Ansible, Kubernetes manifests) — manual-only changes are invisible drift
- analyze cross-layer impact for every proposed change; a change at one layer creates second-order effects at adjacent layers
- capacity planning is proactive — produce a capacity model before production, not after the first resource incident
- **CELLULAR-SHUFFLE-SHARDING**: Partition systems targeting $\ge 99.95\%$ availability into shared-nothing cells; assign tenants via Highest Random Weight (HRW) shuffle sharding ($P(\text{Collision}) = 1/\binom{N}{K} \le 0.005\%$) with monotonic epoch fencing tokens to eliminate split-brain mutations.
- **LITTLES-LAW-BULKHEAD**: Dimension worker pools and PgBouncer connection pools via Little's Law ($L = \lambda \times W$) with a $2.5\times$ burst multiplier; never allow unbounded concurrency.
- **GPU-VRAM-FORMULA**: Sizing must follow $VRAM_{total} = VRAM_{weights} + VRAM_{KV} + VRAM_{activation} + VRAM_{overhead}$ with $\ge 15\%$ safety headroom; running below 10% headroom causes OOM-kill under burst traffic.
- **INFERENCE-SERVER-SELECTION**: vLLM for high-throughput LLM serving with continuous batching and chunked prefill; TensorRT-LLM for lowest-latency serving; Triton for multi-model ensembles; Ollama for local dev; vLLM Automatic Prefix Caching (APC) with static system prompts first.
- **LLM-SLOS & TOKEN-ECONOMICS**: Set measurable LLM SLOs ($TTFT_{P95} \le 800\text{ms}$, $TBT_{P95} \le 25\text{ms}$, throughput $> 40$ tokens/s per user); compute Cost-Per-Token ($CPT$) and enforce Value-Per-Token ($VPT \ge 4 \times CPT$) viability before sizing clusters.
- **VECTOR-DB-TUNING**: Explicitly specify HNSW $m$ (connectivity), $ef\_construction$ (build quality), and query-time $ef$ (recall-latency trade-off).
- **EMBEDDING-CACHE**: Always design an embedding cache layer; repeated embedding of identical content is the most common preventable AI cost spike.
- **KV-CACHE-TIERING (2026)**: For agentic and long-context workloads, evaluate KV-cache offloading tiers (GPU → CPU RAM → storage; vLLM/SGLang offloading, NVIDIA ICMS) before scaling GPU count; record the tiering decision in `ai_infrastructure.kv_cache_tiering` — idle GPU VRAM used as a KV warehouse is the most expensive storage in the stack.
- **SPECULATIVE-DECODING-DECISION (2026)**: Evaluate EAGLE-3/MTP speculative decoding as a capacity lever for decode-bound workloads (up to 6.5x throughput on supported stacks); gate the decision on measured draft acceptance rate (net loss below ~70%) and record it in `ai_infrastructure.speculative_decoding`.
- **DRA-GPU-ALLOCATION (2026)**: On Kubernetes v1.34+, allocate accelerators via DRA ResourceClaims (GA; admin-access and extended-resource support GA in v1.36/v1.37) with structured VRAM requests instead of opaque integer `nvidia.com/gpu` counts; combine with MIG partitioning for multi-tenant isolation.
- See [`references/cellular-topology-and-capacity-sizing.md`](references/cellular-topology-and-capacity-sizing.md) for combinatorial proofs, Go HRW router code, and worked GPU sizing examples.

## Suggested Process

### Step 1: Collect Inputs

Before designing, gather:

- NFRs from Technical Architect (ADRs) or Product Manager (feature briefs)
- traffic and load projections (current and forecast)
- service topology (what services exist and how they communicate)
- security requirements and data residency constraints
- cost envelope and budget constraints
- AI model specifications if inference infrastructure is in scope: model name/version, parameter count, quantization target, expected QPS, P99 latency target, context window length

### Step 2: Translate NFRs Into Measurable Targets

For each NFR, produce a specific, measurable engineering target:

| NFR (vague) | Engineering target (specific) |
|-------------|-------------------------------|
| "High availability" | 99.9% availability = max 8.7h downtime/year; RTO < 15min; RPO < 5min |
| "Fast response" | P99 API latency < 200ms at 1000 req/s peak load |
| "Handle growth" | Scale to 10x current traffic without design changes; scale to 100x with horizontal sharding |
| "Low cost AI inference" | < $0.005 per LLM request; token budget: 2K input + 500 output average |

Return NFRs to their source if a measurable target cannot be derived from available information.

### Step 3: Design System Topology

Specify each layer of the system:

**Compute layer:**
- instance types and sizing rationale
- replica count and autoscaling policy (scale-out trigger, scale-in threshold)
- placement strategy (availability zones, regions)

**Network layer:**
- VLAN/subnet segmentation
- load balancer type and configuration (L4 vs L7, health check intervals, session persistence)
- DNS strategy (TTL, health-check-aware failover)
- service mesh or direct connection decision

**Storage layer:**
- database type selection and sizing
- storage tier hierarchy (hot/warm/cold)
- replication and backup strategy
- retention policy

**Middleware layer:**
- message queue topology (Kafka partition strategy, consumer group design; or Redis Streams; or cloud-native alternatives)
- cache hierarchy (L1 in-process, L2 Redis/Memcached, L3 CDN)
- API gateway or service mesh configuration

**AI inference layer (when in scope):**
- GPU type, count, and allocation plan
- inference serving stack selection with configuration
- vector database selection and index parameters
- embedding pipeline design

### Step 4: Build Capacity Model

Produce a capacity model for every primary resource:

```
| Resource     | Current  | P95 (3mo) | P95 (12mo) | Headroom | Action trigger |
|--------------|----------|-----------|------------|----------|----------------|
| CPU (avg)    | 35%      | 52%       | 78%        | 22%      | Scale at 70%   |
| Memory       | 12 GB    | 18 GB     | 28 GB      | 4 GB     | Scale at 80%   |
| Storage      | 500 GB   | 750 GB    | 1.2 TB     | 300 GB   | Expand at 80%  |
| GPU VRAM     | 18 GB    | 22 GB     | 30 GB      | 10 GB    | Upgrade at 85% |
| Network egr. | 50 GB/d  | 75 GB/d   | 120 GB/d   | —        | Review at 2x   |
```

Derive forecasts from: current usage × growth rate (from traffic projections or business targets).

### Step 5: Document Trade-offs

For every significant design decision, record:

- what was chosen and why
- what alternatives were considered and rejected
- what trade-off was accepted (e.g., higher cost for lower latency; lower availability for simpler design)

### Step 6: Analyze Cross-Layer Impact

Before finalizing:

- trace each infrastructure decision to its second-order effects: "changing connection pool max from 50 to 200 enables higher concurrency but increases database memory pressure by ~4 GB"
- identify changes that affect multiple layers simultaneously
- flag any changes that require coordination with adjacent roles (DevOps for pipeline, SRE for SLO alignment, Security Engineer for security review)

### Step 7: Produce IaC and Deliverable

- author or update Terraform modules, Ansible playbooks, or Kubernetes manifests for all infrastructure changes
- produce `contracts/schemas/system-design-spec.json` for machine-readable handoff when downstream roles need to consume the design
- produce a human-readable System Design Brief using the Output Template in `system-engineer.md`

## Checklist

- [ ] all NFRs have specific, measurable targets with measurement methods
- [ ] system topology covers all in-scope layers with cellular partition and shuffle sharding rationale (if $\ge 99.95\%$ availability)
- [ ] capacity model produced for all primary resources (compute, memory, network, storage, GPU if applicable) via Little's Law
- [ ] 3-month and 12-month capacity forecasts present with burst safety multipliers
- [ ] action triggers defined (when to scale, when to upgrade)
- [ ] cost vs. performance trade-off surfaced to stakeholders with Token Economics (CPT/VPT)
- [ ] cross-layer impact analysis complete with zero cross-cell synchronous RPC chains
- [ ] all infrastructure changes represented in IaC — no manual-only configuration
- [ ] trade-offs documented: what was chosen, what was rejected, and why
- [ ] AI infrastructure specified (when in scope): GPU allocation, inference server config, vector DB, embedding pipeline
- [ ] KV-cache tiering decision recorded for agentic/long-context workloads (when AI in scope)
- [ ] speculative decoding decision recorded with draft acceptance basis (when AI in scope)
- [ ] GPU allocation via DRA ResourceClaims on K8s v1.34+ (no opaque integer GPU counts)
- [ ] system-design-spec.json produced when structured downstream handoff required
- [ ] open questions, accepted risks, and escalation items documented

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- `contracts/schemas/system-design-spec.json` — Required fields: topology, nfr_targets, capacity_model, rollback_plan, and trade_offs. Set produced_by_role to System Engineer or Technical Architect.

Skip emission for solo refactor work where no downstream handoff is expected.

## Failure Modes

- **Vague NFR accepted**: a design proceeds with "the system should be fast". Mitigation: return unmeasurable NFRs to the source for clarification before producing a design.
- **VRAM under-provisioned**: GPU memory is sized without accounting for KV cache, activation, or safety headroom. Mitigation: enforce the GPU-VRAM formula; require ≥ 15% headroom.
- **Default vector index deployed**: a vector database ships with default HNSW parameters. Mitigation: explicitly set `m`, `ef_construction`, and query-time `ef`; document the recall-latency trade-off.
- **Embedding re-computed**: the same content is re-embedded on every request, driving unnecessary GPU cost. Mitigation: design an embedding cache layer; verify cache hit rate in production.
- **LLM SLO missing**: GPU infrastructure is sized without TTFT, TBT, or throughput targets. Mitigation: define measurable SLOs (TTFT p95 < 800ms, TBT p95 < 25ms) before sizing.
- **Capacity model stale**: the capacity model was produced once and never updated. Mitigation: re-validate the capacity model quarterly or after every 2x growth event.
- **Cross-layer impact missed**: a connection pool change breaks an adjacent layer. Mitigation: trace second-order effects for every change; flag coordination requirements with adjacent roles.
- **Manual-only config**: infrastructure is set up via console without IaC. Mitigation: require all changes to be in Terraform/Ansible/Kubernetes manifests; surface drift as a CI failure.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: every infrastructure component must declare its auth surface; reject "internal-only" claims without a network policy or service-mesh boundary.
- **ASI04 Supply Chain**: AI model versions, vector database versions, and inference server versions must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct IaC modules, capacity formulas, or routing configs from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the system design spec is consumed by multiple downstream roles; treat it as a public contract and review all changes before deploy.
- **ASI09 Human-Agent Trust Exploitation**: do not present a design as "secure" without a security review; surface remaining risks and accepted trade-offs honestly.

## Related Skills

- **performance-profiling**: Benchmark and investigate performance bottlenecks after the design is implemented
- **debug-runtime-platform**: Debug system-level issues at OS, network, and runtime layers
- **plan-technical-delivery**: Coordinate system design phases with the delivery timeline
- **add-telemetry-instrumentation**: Define observability requirements for the system being designed
- **conduct-research**: Technology selection research when infrastructure decisions require vendor evaluation
- **security-audit**: Security review of the infrastructure design before production apply
- **database-maintenance**: Database-level investigation when storage design choices are being validated
- **architect-mcp-server**: Architect enterprise MCP tool surfaces, streamable HTTP transport, and externalized state
- **decompose-agentic-system**: Decompose massive multi-file systems into hierarchical DAG sub-agent execution scopes
