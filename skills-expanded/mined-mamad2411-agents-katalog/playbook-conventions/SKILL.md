---
name: playbook-conventions
description: Shared output structure, handoff protocol, and ADR format for Claude Code Dev Studio agents and skills. Use proactively when a domain agent or skill is producing deliverables, handing work off, or recording a decision.
---

# Playbook Conventions

The single source of truth for how playbook agents and skills format output, hand off
work, and record decisions. Pull this instead of restating the conventions inline.

## Output discipline

- **Lead with a Summary** — 2–4 sentences: what changed and what it affects.
- **Then the deliverables** — the domain-specific artifacts (code, schema, diagram,
  decision table, findings) the task called for.
- **Draft an ADR** — for any non-obvious architectural, security, or process decision,
  produce a `DECISIONS.md` entry (format below) for the user to approve.
- **Be explicit about trade-offs** — when a choice is genuinely context-dependent,
  present 2–3 options with pros/cons rather than a single opinion.

## Handoff protocol

You run as a subagent (or in the main loop). **Subagents cannot spawn other agents** —
they can only invoke skills.

- **To reach sibling expertise** — invoke the relevant skill with the Skill tool
  (e.g. a SaaS task pulls `saas-billing` + `saas-auth-sso`). You may pull several.
- **To engage another agent** (`plan-architect`, `secure-auditor`, `pr-code-reviewer`,
  `test-writer-runner`, `deploy-checklist`, or another domain agent) — you cannot call
  it directly; return to the orchestrator and name the agent and why.
- **After implementation** — route code through `pr-code-reviewer`; escalate
  security-sensitive changes to `secure-auditor`; verify behavior with
  `test-writer-runner` before hardening.

## Phase gates

Work proceeds through seven phases (Initialize → Architecture → Implementation →
Testing → Hardening → Documentation → Deployment). Do not advance past a phase until
its exit criteria are met. `main` should always be deployable.

## ADR format

```
## ADR-XXXX: <Title>

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Superseded | Deprecated
**Phase:** Initialize | Architecture | Implementation | Testing | Hardening | Documentation | Deployment
**Deciders:** <names or roles>

### Context
What situation or problem forced this decision?

### Decision
What was decided?

### Rationale
Why this option over the alternatives?

### Consequences
Trade-offs, risks, and follow-on work.

### Supersedes
ADR-XXXX (if applicable)
```
