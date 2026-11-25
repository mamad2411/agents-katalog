---
name: deploy-vllm-inference
description: Deploy, configure, scale, and optimize high-throughput LLM inference workloads using the vLLM V1 engine (default since 2025, current v0.32+). Use when serving self-hosted open-weight models (GLM-5, DeepSeek-V4, Qwen3.8, Kimi K2/K3, gpt-oss) on Kubernetes with Dynamic Resource Allocation (DRA), NVIDIA MIG slicing, dynamic chunked prefill, prefix caching, and multi-tier KV cache offloading.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "2.0.0"
---

# Deploy vLLM Inference

Use this skill when deploying, configuring, scaling, and benchmarking production LLM serving workloads with the vLLM v1 engine on Kubernetes.

## When to Use

- deploying self-hosted open-weight models (GLM-5, DeepSeek-V4, Qwen3.8, Kimi K2/K3, gpt-oss; DeepSeek-R1/Qwen2.5/Llama 3.3 are legacy generations) with the vLLM V1 engine
- configuring PagedAttention v3 with FP8 KV cache memory bounds (<2.4% fragmentation)
- configuring dynamic chunked prefill to eliminate decode latency jitter (TPOT)
- enabling hierarchical Radix Tree prefix caching for multi-turn conversations
- allocating GPU accelerators via Kubernetes 1.31+ Dynamic Resource Allocation (DRA) or NVIDIA MIG hardware slicing
- setting up queue-depth driven Horizontal Pod Autoscaling (HPA) via Prometheus metrics
- configuring high-speed `/dev/shm` tmpfs mounts and HugePages for RDMA RoCEv2 transfers

## Core Rules

- **Enforce vLLM V1 Architecture**: the V1 engine with standalone C++ core is the default (since early 2025; current release line v0.32+) — `VLLM_USE_V1=1` is only needed to pin the deprecated legacy V0 path; never deploy new workloads on V0.
- **Dynamic Chunked Prefill**: enable chunked prefill (`--enable-chunked-prefill=true`, `--max-num-batched-tokens 2048`) to interleave prompt prefill chunks (512–2048 tokens) with decode steps, locking TPOT jitter within ±2.0ms.
- **Prefix Caching with Radix Trees**: keep `--enable-prefix-caching=true` with block size 32 (`--block-size 32`) — prefix caching is on by default in V1, so verify rather than assume — to achieve $\ge 70\%$ cache hits on repeated prompts.
- **VRAM Utilization Safety Ceiling**: cap `--gpu-memory-utilization` between `0.88` and `0.90` to preserve headroom for PyTorch runtime activations and NCCL buffers.
- **Hardware Isolation**: multi-tenant inference must use NVIDIA MIG (`3g.40gb`) or Kubernetes Dynamic Resource Allocation (DRA — GA v1.34+, `resource.k8s.io/v1`) with CEL device selectors; software time-slicing on production inference is prohibited.
- **Queue-Depth Autoscaling (KEDA fronting HPA)**: autoscale pods on request queue depth (`vllm:num_requests_waiting`, target: 5) via KEDA managing the HPA, never solely on GPU compute utilization (KEDA-NOT-HPA rule in `system-design`).
- **Mandatory tmpfs `/dev/shm`**: mount an in-memory `tmpfs` volume of at least 16GiB on `/dev/shm` to prevent NCCL bus deadlocks.
- refer to `references/vllm-production-guide.md` for production StatefulSet manifests, DRA ResourceClaims, and Prometheus HPA configs.

## Suggested Process

### 1. Calculate VRAM Capacity & Sizing Model
Model GPU memory requirements:
$$\text{VRAM}_{\text{total}} = \text{Weights}_{\text{FP8/FP16}} + \text{KV-Cache}_{\text{FP8}} + \text{Activation-Workspace} + \text{Safety-Headroom (12\%)}$$
For Llama-3.1-70B FP8 on 8x H100 (640GB total VRAM), allocate 70GB weights + 480GB KV cache + 90GB activation headroom.

### 2. Claim GPU via Kubernetes DRA (GA v1.34+) or NVIDIA MIG
Declare a `ResourceClaim` requesting GPUs via CEL selectors (GA API `resource.k8s.io/v1`; beta-era `v1alpha3` is retired):
```yaml
apiVersion: resource.k8s.io/v1
kind: ResourceClaim
metadata:
  name: vllm-h100-claim
spec:
  devices:
    requests:
      - name: gpu
        deviceClassName: gpu.nvidia.com
        selectors:
          - cel:
              expression: "device.attributes['gpu.nvidia.com'].memory >= 80.GiB"
```

### 3. Configure vLLM v1 Engine Parameters
Define CLI flags in container arguments:
```bash
python3 -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3.1-70B-Instruct \
  --tensor-parallel-size 8 \
  --kv-cache-dtype fp8 \
  --block-size 32 \
  --max-num-batched-tokens 2048 \
  --enable-chunked-prefill true \
  --enable-prefix-caching true \
  --gpu-memory-utilization 0.90 \
  --port 8000
```

### 4. Deploy Kubernetes StatefulSet Manifest
Mount tmpfs `/dev/shm` (64GiB), HugePages (32GiB), and assign security capabilities (`IPC_LOCK`):
```yaml
volumeMounts:
  - name: dshm
    mountPath: /dev/shm
  - name: hugepages
    mountPath: /dev/hugepages
volumes:
  - name: dshm
    emptyDir:
      medium: Memory
      sizeLimit: 64Gi
  - name: hugepages
    emptyDir:
      medium: HugePages
```

### 5. Configure Queue-Depth Autoscaling (KEDA fronting HPA)
Prefer a KEDA ScaledObject driving these queue/KV signals (it manages the HPA below); the raw HPA binding via Prometheus Adapter remains valid:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-inference-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: vllm-v1-h100-cluster
  minReplicas: 2
  maxReplicas: 8
  metrics:
    - type: Pods
      pods:
        metric:
          name: vllm_num_requests_waiting_per_pod
        target:
          type: AverageValue
          averageValue: "5"
```

### 6. Verify Engine Health, Throughput & Cache Telemetry
Verify endpoints via HTTP probes:
```bash
curl -f http://localhost:8000/health
curl -s http://localhost:8000/metrics | grep -E "vllm:num_requests_waiting|vllm:gpu_cache_usage_factor"
```

## Checklist

- [ ] Confirm vLLM v1 engine is enabled (`VLLM_USE_V1=1`) with C++ standalone core
- [ ] Verify `--enable-chunked-prefill=true` and `--max-num-batched-tokens 2048` are set
- [ ] Confirm `--enable-prefix-caching=true` is enabled with `--block-size 32`
- [ ] Validate `--gpu-memory-utilization` is capped between 0.88 and 0.90
- [ ] Verify container mounts tmpfs on `/dev/shm` with minimum 16GiB capacity
- [ ] Ensure multi-tenant GPU allocation uses NVIDIA MIG or K8s DRA (GA v1.34+) CEL selectors
- [ ] Confirm autoscaling (KEDA fronting HPA) scales on request queue depth (`vllm_num_requests_waiting_per_pod`)

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: `contract_type`, `version` (vLLM engine + model revision), `environments[]`, `steps[]` (each with `order`, `action`, `is_destructive` — GPU ResourceClaim creation, StatefulSet rollout, HPA attachment), and `rollback_plan`. Populate `ai_gpu_infrastructure` with the GPU topology (tensor-parallel size, MIG/DRA claim) and `verification` with `/health` and `vllm:num_requests_waiting` probe evidence.
- Skip emission for single-node local experiments with no downstream handoff.

## Failure Modes

- **KV-cache OOM under burst**: the prefix-cache hit rate collapses under novel traffic, concurrent prefills consume the KV pool, and the engine is OOM-killed. Mitigation: size the KV cache from the VRAM formula with the 12% safety headroom, cap `--gpu-memory-utilization` at 0.90, and alert on `vllm:gpu_cache_usage_factor` before the kill.
- **Tensor-parallel port collision**: multiple TP-8 replicas bind the same default distributed-init/NCCL port on one node and hang at startup. Mitigation: assign each pod a unique distributed-init port/hostname and confirm NCCL init in the readiness probe.
- **Silent quantization quality loss**: switching weights or KV cache to FP8 (`--kv-cache-dtype fp8`) degrades long-context accuracy with no error logged. Mitigation: benchmark a golden set before and after quantization; only promote the configuration if accuracy holds.
- **Undersized `/dev/shm`**: the tmpfs mount is below 16GiB, starving the v1 SPSC ring buffers and deadlocking NCCL. Mitigation: mount an in-memory tmpfs of at least 16GiB (the reference manifest uses 64GiB) plus HugePages; reject manifests without it.
- **Autoscaling on GPU utilization**: the HPA scales on GPU compute utilization, so decode-heavy queues grow while GPUs look busy. Mitigation: bind the HPA to queue depth (`vllm:num_requests_waiting`, target 5), never solely on GPU utilization.
- **Software time-slicing on production**: multi-tenant GPU sharing falls back to time-slicing, reintroducing TPOT jitter and noisy-neighbor preemption. Mitigation: enforce NVIDIA MIG (`3g.40gb`) or DRA CEL selectors; reject time-sliced production layouts.
- **Health green, throughput dead**: `/health` returns OK while prefix caching is disabled and the cache hit rate hovers near 0. Mitigation: verify `--enable-prefix-caching=true` with `--block-size 32` and cache-hit telemetry in the verification step, not just the health endpoint.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: the served model follows instructions from untrusted end-user traffic, so jailbreaks steer generation toward policy violations. Mitigation: treat inference traffic as untrusted, keep system prompts immutable per deployment, and front the endpoint with the patterns from `prompt-injection-defense`.
- **ASI03 Identity & Privilege Abuse**: Radix-tree prefix caching reuses KV blocks across users, letting one tenant's cached context surface in another tenant's responses. Mitigation: partition tenants into separate deployments or MIG slices so prefix caches are never shared across trust boundaries.
- **ASI04 Supply Chain**: model weights pulled from unverified mirrors can be poisoned or tampered. Mitigation: pull only from the canonical publisher repository pinned by revision SHA, and record weight hashes plus quantization metadata in a CycloneDX 1.6 AI/ML BOM (see `supply-chain-security`).
- **ASI05 RCE Guard**: the OpenAI-compatible server exposes engine-facing parameters (chat template kwargs, LoRA adapter names, sampling overrides); unvalidated passthrough becomes arbitrary engine configuration. Mitigation: expose only a validated allowlist of request fields; reject unknown kwargs at the gateway.
- **ASI07 Inter-Agent Communication**: GPU topology and capacity claims are consumed by DevOps and SRE roles. Mitigation: emit the schema-validated `deployment-plan.json` so downstream roles verify DRA/MIG claims against the ordered steps instead of trusting prose.
- **ASI09 Human-Agent Trust Exploitation**: reporting the deployment as production-ready from the VRAM sizing formula alone. Mitigation: present measured throughput, TPOT jitter, and cache-hit numbers from the verification probes before declaring success.

## Related Skills

- **setup-gpu-finops**: GPU capacity modeling, DCGM telemetry, and OpenCost attribution
- **setup-llm-gateway**: Centralized LiteLLM proxy routing, failover, and rate limiting
- **deploy-aws-eks-workloads**: Kubernetes deployment, Karpenter node provisioning, and Pod Identity
- **debug-runtime-platform**: Diagnosing pod crash loops, NCCL deadlocks, and container networking
- **add-telemetry-instrumentation**: OpenTelemetry Collector pipelines and GenAI semantic conventions
