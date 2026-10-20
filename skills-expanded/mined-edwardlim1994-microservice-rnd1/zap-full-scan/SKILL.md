# ZAP Full Scan

## Purpose
Active security scan against full staging deployment with all services running together — tests real attack surface.

## Role
Security Engineer

## Phase
Staging (pre-release)

## Triggered By
`/release-staging` deploys to Staging cluster.

## Inputs
- Staging cluster URL (all services running together)

## Type
Active attack simulation (~20 minutes). Tool: OWASP ZAP active scan. Target: full Staging cluster.

## Process

### Checks Included
- GraphQL introspection check (should be disabled in staging/prod)
- gRPC reflection check (should be disabled in staging/prod)
- Federation endpoint security (Apollo Router gateway)
- Kafka topic authorization checks
- OWASP Top 10 active tests
- OWASP API Security Top 10 tests

### Findings Classification
- Critical/High → create release blocking bug card immediately
- Medium → create bug card, fix in current sprint before release
- Low/Info → create backlog card

Results mapped to OWASP categories in `security-metrics-report`.

## Outputs
Classified findings and kanban cards; blocking status for release.

## Quality Gates
- [ ] Full active scan completed (not just baseline)
- [ ] GraphQL introspection verified disabled
- [ ] gRPC reflection verified disabled
- [ ] All findings classified and kanban cards created

## References
- `.claude/skills/security-engineer/semi-automated-pentest/SKILL.md`
- `.claude/skills/security-engineer/security-metrics-report/SKILL.md`
