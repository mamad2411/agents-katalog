---
name: frontend
description: Frontend atomic skills - delegates to orchestrator/frontend/ for coordination
type: reference
---

# Frontend Skills

This is a **skill reference**. Orchestration logic lives in `orchestrator/frontend/ORCHESTRATOR.md`.

## Atomic Skills (in skills/frontend/)

| Skill | Purpose | Single Responsibility |
|-------|---------|----------------------|
| dependency-validation | Bundle size, redundancy, security audit | Package health |
| module-boundary-check | Layer separation, circular deps, import rules | Architecture enforcement |
| perf-profiling | CPU, memory, render, network, battery, startup | Performance measurement |
| perf-recommendations | Optimization suggestions against budgets | Performance analysis |
| security-scan | Secrets, vulnerabilities, AppSec audit | Security detection |
| security-remediation | Fix generation for scan findings | Security fixing |

## Orchestration

For cross-platform coordination (iOS/Android/RN routing, design handoff, feature parity):
→ See `orchestrator/frontend/ORCHESTRATOR.md`
