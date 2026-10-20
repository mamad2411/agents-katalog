## Agent skills

Read this file first. Then follow the referenced documents in the order described here.

### Issue tracker

Issues are tracked in Linear using the workflow described in `.agents/agents/issue-tracker.md`.

### Agent orchestration

When work is executed from Linear tickets, use `.agents/agents/orchestrator.md` as the source of truth for ticket ownership, agent permissions, branch naming, worktree isolation, and delegation boundaries.

### Triage labels

This repo uses the default canonical triage labels. See `.agents/agents/triage-labels.md`.

### Domain docs

This repo uses a shared domain-doc set for multiple bounded contexts. See `.agents/agents/domain.md`.

### Operating model

All agents should follow `.agents/agents/operating-model.md`.
For implementation or review work, treat `.agents/agents/operating-model.md` as the baseline contribution policy for branching, commits, PR scope, testing expectations, naming, code quality, and documentation updates.

### Engineering standards

When the task involves writing, refactoring, or reviewing code:

- Read the relevant ADRs in `docs/architecture/adr/` before changing code when they apply to the affected area.
- Apply `.agents/skills/engineering-guardrails/` as the default reusable procedure for implementation and review guardrails.
- Apply `.agents/skills/local-validation/` when choosing or running local tests, coverage checks, secret scans, or repo validation evidence.
- When local validation or debugging uses `docker compose`, apply `.agents/skills/docker-compose-context-hygiene/` to keep logs, runtime evidence, and chat context under control.
- Use `src/services/*/CONTEXT.md` as the source of truth for ubiquitous language and bounded-context terminology.

### Product and architecture

Use `docs/product/ers.md` as the normalized operational summary of the academic ERS.
Use `docs/architecture/repo-structure.md` to avoid assuming implementation folders that do not exist yet.
