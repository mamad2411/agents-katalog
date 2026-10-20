---
name: golden-path
description: Design a golden path / paved road for a team — the supported way to build, deploy, and operate one kind of service, with off-ramps documented.
---

# golden-path

> A golden path is the *one* supported way to build a class of service. Output is the path doc that a new team can follow without help.

## When to use

- A platform team is paving a road for "all new microservices look like this".
- Existing services are diverging in arbitrary ways and supportability is suffering.
- A workflow needs to ground a new service in conventions.

## Procedure

1. **Scope** — name the class of service the path covers ("internal HTTP API", "scheduled batch job"). Don't try to cover everything in one path.
2. **Stack** — pick the smallest stack that covers the class:
   - Language + framework.
   - Build tool + CI.
   - Container image base + Dockerfile pattern.
   - Deploy target (k8s manifest / Helm chart / serverless / VM).
   - Observability defaults (logs, traces, metrics, the same dashboard template).
   - Secrets: where they live, how they're injected.
3. **Decisions vs. flexibility** — list what teams cannot change without an exception, and what they can.
4. **Off-ramps** — when a team genuinely needs to leave the path, what's the process? Otherwise the path becomes a cage.
5. **Lifecycle** — onboarding (new service in < N minutes), upgrade (how the platform team pushes a new base image), deprecation (how a path version is retired).

## Output

```text
Golden path: Internal HTTP API (v2)

Stack:
  Language        Go 1.22 OR TypeScript 5.x (one of these)
  Framework       chi (Go) OR fastify (TS)
  Build           Bazel for Go, pnpm for TS
  Container       distroless base; multi-stage Dockerfile (template at …)
  Deploy          Kubernetes via shared Helm chart (chart at …)
  Observability   OTel SDK auto-instrumented; logs JSON to stdout; the standard
                  service dashboard template is auto-imported
  Secrets         External Secrets Operator + AWS Secrets Manager

Fixed (no exceptions without ADR):
  - distroless base image
  - JSON-stdout logging
  - OTel SDK + the standard exporter

Flexible (team choice):
  - Auth library inside the framework
  - DB driver (within the supported list: pgx, prisma, …)
  - Test framework

Off-ramp:
  Open ADR-XXX explaining the deviation. Platform team reviews within 1 week.
  Approval grants a 6-month exception; renewable.

Lifecycle:
  - Onboarding:  copier template `platform-go-api` → repo in ~10 min.
  - Upgrade:     platform team pushes a renovate PR; team merges within 30d.
  - Deprecation: 6-month deprecation window with explicit migration guide.
```

## Anti-patterns to avoid

- A "golden path" that's a 40-page document.
- Mandating everything, off-ramping nothing — teams will work around it.
- One path for too many service classes — each one becomes a half-fit.
