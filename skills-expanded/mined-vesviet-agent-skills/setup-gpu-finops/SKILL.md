---
name: setup-gpu-finops
description: Configure GPU telemetry, DCGM metrics, and Kubecost to attribute AI compute costs to specific namespaces or teams. Use when managing GPU infrastructure budgets, tracking AI workload unit economics, or optimizing accelerator capacity.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Setup GPU FinOps

Use this skill to implement cost transparency for self-hosted AI models and GPU workloads in Kubernetes clusters.

## Core Rules

- **DCGM Integration**: Deploy the NVIDIA DCGM Exporter to expose low-level GPU metrics (utilization, memory, power) to Prometheus.
- **Namespace Attribution**: Use Kubecost (or OpenCost) custom pricing sheets to map GPU node costs down to the pod and namespace level.
- **Idle Optimization**: Implement KEDA (Kubernetes Event-driven Autoscaling) or Karpenter to scale GPU nodes to zero when inference queues are empty.
- **Alerting**: Configure Slack/PagerDuty alerts for teams exceeding their daily GPU compute budget.
- **Metric Standardization**: Normalize GPU metric names with `hw.gpu.*` prefixes via OpenTelemetry Collector processors.
- **MIG-MULTI-TENANT-ISOLATION**: For H100/A100/B200, configure NVIDIA MIG (Multi-Instance GPU) partitions to provide hardware-level isolation between teams sharing the same physical GPU — enforces memory and compute boundaries and prevents one tenant's OOM from affecting another's inference workload.
- **KEDA-INFERENCE-AUTOSCALING**: Deploy KEDA ScaledObjects driven by vLLM or Triton inference queue depth metrics to scale model replicas to zero when queues are empty for >15 minutes — configure `cooldownPeriod: 900s` to prevent flapping.
- **VLLM-APC-COST**: Enable vLLM v0.6+ Automatic Prefix Caching (APC) to reuse KV cache for repeated system prompts; structure prompts with static content first and dynamic user content last for maximum cache hit rate — reduces GPU compute cost by 20-60% for high-traffic repeated-context workloads.
- **KV-CACHE-OFFLOAD-COST (2026)**: for agentic and long-context workloads, extend KV cache into CPU RAM / storage tiers (vLLM-SGLang offloading, NVIDIA ICMS, storage-backed KV) before scaling GPU count — offloaded KV turns idle GPU VRAM back into serving capacity; price the tiers separately in cost dashboards.
- **SPECULATIVE-DECODING-THROUGHPUT (2026)**: EAGLE-3 / MTP draft models deliver up to 6.5x decode throughput on supported stacks (vLLM, SGLang; TPU support since 2026-10) — model the throughput-per-dollar gain using measured draft acceptance rate, and treat acceptance < ~70% as a net loss.
- **RACK-SCALE-PRICING (2026)**: maintain pricing sheets for rack-scale Blackwell systems (GB300 NVL72: 72 GPUs, ~278GB HBM3e each, NVLink-pooled domain) with per-GPU fractional allocation math; track the Vera Rubin roadmap for refresh depreciation windows.

## Suggested Process

### 1. Deploy NVIDIA DCGM Exporter DaemonSet

Install hardware telemetry infrastructure:
- Deploy the NVIDIA DCGM (Data Center GPU Manager) Exporter as a DaemonSet across GPU-enabled Kubernetes nodes.
- Configure profiling metrics: GPU utilization (`DCGM_FI_DEV_GPU_UTIL`), framebuffer memory used (`DCGM_FI_DEV_FB_USED`), and power draw (`DCGM_FI_DEV_POWER_USAGE`).
- Verify the exporter exposes Prometheus metrics on port 9400.

### 2. Configure Prometheus Metric Scraping & Relabeling

Wire metrics into the monitoring cluster:
- Add a Prometheus `PodMonitor` or `ServiceMonitor` targeting DCGM exporter endpoints.
- Configure metric relabeling rules to attach Kubernetes pod, namespace, model name, and node group labels.
- Set up an OpenTelemetry Collector pipeline to transform and export metrics with standardized `hw.gpu.*` naming conventions.

### 3. Integrate Kubecost / OpenCost Pricing Sheets

Configure cost allocation models:
- Define custom GPU pricing tables in Kubecost/OpenCost reflecting cloud provider or on-premise hourly rates per accelerator type (A100, H100, L4, T4).
- Configure allocation algorithms to split node base cost by fractional GPU sharing (MIG or time-slicing) when multiple pods share an accelerator.
- Validate that cost breakdown dashboards attribute dollar spend accurately by namespace, team, and model deployment.

### 4. Implement Scale-to-Zero & Dynamic Autoscaling

Optimize GPU compute efficiency:
- Configure Karpenter node pools or Cluster Autoscaler to dynamically provision GPU instances on demand.
- Deploy KEDA ScaledObjects driven by inference request queue depth (vLLM / Triton metrics) to scale model replicas down to zero during idle periods.
- Configure node termination grace periods to allow in-flight inference requests to drain cleanly.

### 5. Establish Budget Thresholds & Anomaly Alerting

Protect against cost overruns:
- Define PrometheusRule alert thresholds for low utilization on allocated GPUs (e.g., utilization < 15% for > 30 minutes).
- Configure budget alert notifications via Slack or PagerDuty when daily/monthly cost burn rates exceed target limits.
- Set up automated scaling circuit breakers for runaway experimental batch jobs.

### 6. Validate Pipeline & Dashboards

Use skill: `performance-profiling`
- Generate synthetic inference load to verify Prometheus records utilization spikes in real time.
- Verify Kubecost allocation reports reflect cost per inference request.
- Confirm idle scale-down shuts down unneeded GPU nodes within the configured TTL.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/deployment-plan.json`** — Required fields: `infrastructure_changes[]`, `config_updates[]`, and `validation_run` output proving Prometheus is scraping DCGM metrics successfully.

## Failure Modes

- **DCGM not scraping**: the exporter is deployed but Prometheus cannot reach port 9400. Mitigation: verify NetworkPolicies and the ServiceMonitor selector; surface a smoke test in the deployment plan.
- **MIG not configured**: H100/A100/B200 GPUs are shared without MIG partitions, allowing OOM cross-contamination. Mitigation: enable MIG partitions for multi-tenant GPUs; enforce memory and compute boundaries.
- **Cost attribution missing**: Kubecost reports node-level cost but no per-namespace or per-model breakdown. Mitigation: configure custom GPU pricing sheets; verify the dashboard shows per-model dollar spend.
- **Scale-to-zero flapping**: KEDA scales model replicas to zero and back rapidly under bursty load. Mitigation: set `cooldownPeriod: 900s`; tune the queue-depth threshold to prevent flapping.
- **vLLM APC not enabled**: repeated system prompts are re-tokenized on every request. Mitigation: enable Automatic Prefix Caching in vLLM v0.6+; structure prompts with static content first.
- **Idle GPU still running**: a GPU node sits at < 15% utilization for 30+ minutes without scaling down. Mitigation: configure Karpenter or Cluster Autoscaler to scale to zero on empty inference queues.
- **Budget alert ignored**: a daily burn rate alert fires but no automation responds. Mitigation: wire PagerDuty/Slack; configure an automated circuit breaker for runaway jobs.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: GPU node access and DCGM endpoints must be access-controlled; reject anonymous scraping.
- **ASI04 Supply Chain**: DCGM, KEDA, and Kubecost versions must be validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct KEDA ScaledObjects, MIG partition configs, or Kubecost pricing from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the deployment plan is consumed by FinOps and SRE roles; emit a structured contract so each role can validate the rollout.
- **ASI09 Human-Agent Trust Exploitation**: do not present GPU spend as "optimized" without showing the per-model cost breakdown; surface unallocated cost honestly.

## Checklist

- [ ] NVIDIA DCGM Exporter DaemonSet deployed and exposing metrics on GPU nodes.
- [ ] Prometheus scraping and relabeling rules configured with pod and namespace metadata.
- [ ] Kubecost / OpenCost custom GPU pricing sheets configured and verified.
- [ ] Scale-to-zero autoscaling (KEDA/Karpenter) configured for inference queues.
- [ ] Low-utilization and budget-overrun alerting rules active.
- [ ] Grafana and cost attribution dashboards verified under active load.
- [ ] `deployment-plan.json` emitted.

## Related Skills

- **setup-llm-gateway**: Correlate GPU infrastructure spend with model token usage and routing policies
- **add-telemetry-instrumentation**: Standardize GPU metric collection using OTel Collector and DCGM conventions
- **aws-infrastructure**: Provision GPU EC2 instances, EKS node groups, and FinOps cost allocation tags
- **system-design**: Model GPU capacity requirements and inference compute topology
- **setup-deployment**: Apply Kubernetes manifests, DaemonSets, and KEDA autoscalers to deployment sources
- **performance-profiling**: Analyze GPU memory bandwidth, compute utilization, and kernel execution latency
