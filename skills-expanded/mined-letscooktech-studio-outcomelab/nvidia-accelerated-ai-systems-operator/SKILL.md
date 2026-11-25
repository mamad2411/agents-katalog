---
name: nvidia-accelerated-ai-systems-operator
description: Safely plan, review, and operate NVIDIA-oriented or GPU-accelerated AI skill workflows covering AI-Q, cuOpt, DALI, Dynamo, NemoClaw, Omniverse, USD optimization, physical AI infrastructure, neural reconstruction, simulation-ready assets, and accelerated AI deployment. Use when adapting NVIDIA Agent Skills-style packs into OutcomeLab workflows or reviewing GPU/accelerated AI systems for setup, deployment, validation, scaling, security, cost, and production readiness.
---

# NVIDIA Accelerated AI Systems Operator

Developed by the LetsCookTech Open Source Team.

Apply the shared [OutcomeLab skill standard](../../docs/SKILL-STANDARD.md) for evidence, verification, risk, benchmarking, and improvement.

Operate GPU and NVIDIA-oriented AI workflows as production systems. This is an OutcomeLab adapter layer: it does not replace official vendor documentation or upstream skills. It adds classification, safety, validation, cost, security, and production-readiness review around accelerated AI tasks.

## Workflow

1. Classify the task domain: AI-Q deployment/research, cuOpt optimization, DALI data pipelines, Dynamo serving/routing/interconnect, NemoClaw sandboxing, Omniverse/USD workflows, physical AI infrastructure, neural reconstruction, or simulation asset pipelines.
2. Identify required hardware, drivers, CUDA/runtime versions, containers, credentials, endpoints, environment variables, storage, network, and licensing constraints.
3. Select the operating path: install, configure, run, validate, troubleshoot, scale, benchmark, secure, or decommission.
4. Inspect safety boundaries: secrets, certificates, service URLs, cloud credentials, GPU access, production data, destructive commands, external network calls, and cost exposure.
5. Create a validation plan: smoke test, health check, sample workload, performance baseline, logs, telemetry, rollback, and failure criteria.
6. Review production risks: GPU capacity, interconnect, scheduling, data movement, storage bandwidth, version drift, observability, incident recovery, and vendor lock-in.
7. Produce an evidence-backed plan or audit with exact commands only when authorization and environment details are supplied.

## Output contract

Return task classification, required inputs, missing artifacts, selected workflow path, safety checklist, setup/review plan, validation checks, performance and cost risks, security risks, rollback plan, confidence level, and review gaps.

## Quality gates

- Do not invent NVIDIA product commands, package names, endpoints, or compatibility claims.
- Require official docs, supplied files, or inspected scripts for version-specific steps.
- Never expose private certs, service URLs, tokens, or cloud credentials.
- Do not run install/deploy/stop commands without explicit authorization.
- Mark output incomplete when hardware, driver, runtime, or endpoint evidence is missing.
