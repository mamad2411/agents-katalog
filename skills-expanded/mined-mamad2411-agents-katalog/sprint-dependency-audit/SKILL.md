# Sprint Dependency Audit

## Purpose
Audits all project dependencies for known CVEs and security issues.

## Role
Security Engineer

## Phase
Development

## Triggered By
Sprint start, new critical CVE discovered, pre-release re-audit.

## Inputs
- `package.json`/lockfiles across workspaces
- Docker image manifests

## Cadence
- Sprint start: full dependency audit
- Triggered: when critical CVE appears in Bun, Apollo, gRPC-js, Kafka etc.
- Pre-release: quick re-audit to confirm no new CVEs since sprint start

## Process
1. Run `npm audit` (lists known vulnerabilities).
2. Run OWASP Dependency Check (comprehensive CVE database check).
3. Read Harbor Trivy scan results for Docker images (auto-runs on image push).
4. Update `security-knowledge-base` with findings.
5. For each Critical CVE:
   a. Create immediate kanban card: `type: task`, `priority: critical`
   b. Notify PM: new critical CVE requires immediate fix task
   c. PM adds to current sprint
6. For High/Medium CVE: create kanban card for next sprint.
7. For Low CVE: log in `security-knowledge-base` only.

## Outputs
Updated `security-knowledge-base`, kanban cards for actionable CVEs.

## Quality Gates
- [ ] All three audit tools run
- [ ] security-knowledge-base updated
- [ ] Critical CVE kanban cards created immediately
- [ ] PM notified of critical findings

## References
- `.claude/skills/security-engineer/security-knowledge-base/SKILL.md`
- `.claude/skills/pm/kanban-board-management/SKILL.md`
