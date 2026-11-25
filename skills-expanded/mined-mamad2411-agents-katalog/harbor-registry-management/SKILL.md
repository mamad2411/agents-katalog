# Harbor Registry Management

## Purpose
Manages the self-hosted Harbor image registry: projects, permissions, retention, and scanning.

## Role
DevOps Engineer

## Phase
Cross-phase (infrastructure)

## Triggered By
New service needing a registry project; ongoing maintenance.

## Inputs
- Service/image requirements

## Process
Self-hosted Harbor in internal cluster. Manages: project creation, user permissions, robot accounts for CI.

- Image retention policy: keep last 10 tags per branch type.
- Harbor Trivy: auto-scans on image push (no manual trigger needed).
- Vulnerability report: Security Engineer reads Harbor scan results.
- CI credentials: robot account with push/pull permissions only.

## Outputs
Configured Harbor projects, retention policies, and CI robot accounts.

## Quality Gates
- [ ] Retention policy enforced (last 10 tags per branch type)
- [ ] Trivy auto-scan confirmed enabled
- [ ] CI robot accounts scoped to push/pull only

## References
- `.claude/skills/devops-engineer/story-merge-pipeline/SKILL.md`
- `.claude/skills/security-engineer/sprint-dependency-audit/SKILL.md`
