# Traefik Ingress Management

## Purpose
Manages IngressRoute CRDs per environment for all services.

## Role
DevOps Engineer

## Phase
Cross-phase (infrastructure)

## Triggered By
New service deployed; new UAT environment created.

## Inputs
- Service Helm chart

## Process
IngressRoute CRDs per environment (never nginx-style Ingress resources):
- SIT: `{service}.sit.internal`
- UAT: `uat-{KAN-N}.uat.internal` (per story)
- Staging: `{service}.staging.{domain}`
- Production: `{service}.{domain}`

TLS: cert-manager manages certificates automatically. Middleware: rate limiting, auth forwarding to Authentik for protected routes. IngressRoute for new service: created by Helm chart template (not manual).

## Outputs
IngressRoute CRDs configured per environment with TLS and middleware.

## Quality Gates
- [ ] IngressRoute CRDs used (never nginx-style Ingress)
- [ ] TLS certificates auto-managed via cert-manager
- [ ] Auth forwarding middleware applied to protected routes
- [ ] IngressRoute created via Helm template (not manual)

## References
- `.claude/skills/devops-engineer/uat-environment-management/SKILL.md`
- `.claude/skills/devops-engineer/helm-chart-management/SKILL.md`
