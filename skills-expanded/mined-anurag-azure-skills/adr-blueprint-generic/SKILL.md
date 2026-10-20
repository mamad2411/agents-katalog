---
name: "adr-blueprint-generic"
description: "Stack-agnostic Architecture Decision Record blueprint: produce complete ADRs (Context, Options considered, Decision, Consequences) for ANY stack (backend, frontend, gateway, integration). Use when the resolved stack is not Java/Spring."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# ADR Blueprint (stack-agnostic)

Produce one ADR per significant decision. Every ADR MUST have all four sections — no TBD/stub.

```
## ADR-NNN — <decision title>
Status: Accepted | Proposed
Context: <forces, constraints, requirements driving the decision; reference DesignArtifacts>
Options considered: <2+ real options with trade-offs>
Decision: <the chosen option, stated clearly>
Consequences: <positive + negative results, follow-ups>
```

## Decision areas by stack
- **Frontend (React/RN):** navigation lib, state management, API/data-fetching layer, theming/design-token strategy, Figma->component translation, auth/token storage, error/loading states, testing approach.
- **Gateway (Kong):** fronting pattern, plugin selection (auth/rate-limit/cors/observability), upstream/LB/health, env overlays, decK GitOps.
- **Integration (MuleSoft):** flow decomposition, DataWeave strategy, error handling, connector config, secure properties, API autodiscovery.
- **Backend:** architecture style, persistence, messaging, security, observability.

Keep ADRs consistent with tsa.json and the resolved stack. No Java-specific content unless the stack is Java.
