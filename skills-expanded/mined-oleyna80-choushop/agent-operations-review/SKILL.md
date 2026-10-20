---
name: agent-operations-review
description: Optional local-only review of agent permission friction, approval waits, sandbox/tooling blockers, and outcome evidence after large Work Blocks, sprint closeouts, or agent orchestration incidents.
user-invocable: true
allowed-tools:
  - Read
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(npm *)
  - Bash(npx *)
  - Bash(curl *)
  - Bash(fuser *)
  - Bash(node *)
  - Bash(rg *)
  - Bash(jq *)
---

# Skill: Agent Operations Review

## Purpose

Use this skill to learn from how agents actually operated: permission friction,
approval waits, sandbox/tooling failures, repeated safe commands, and outcomes
after allowed actions.

This is not a TrustGate, permission engine, or new approval gate. It produces
recommendations only.

## When to Use

- Sprint closeout after large or multi-agent work.
- Repeated approval prompts slowed execution.
- Subagents waited on permissions or tool escalation.
- Sandbox/tooling failures affected verification.
- DB, deploy, webhook, provider, or security gates produced operational
  friction.
- Owner asks whether permissions, skills, or workflow rules should be tuned.

## When to Skip

- Small local changes with no permission friction.
- Discussion-only turns.
- Work Blocks where normal closeout already captures all relevant blockers.
- Any situation where useful analysis would require reading raw private
  transcripts, secrets, request/response payloads, or full client messages.

## Inputs

Prefer sanitized and local-only evidence:

- Work Block closeout summary.
- `memory-bank/progress.md` and active tasklist delivery notes.
- `git status`, `git diff --check`, verifier output.
- Final outcome anchors when relevant: commit hash, push result, CI run status,
  and remaining dirty/untracked files.
- Sanitized snippets of approval/tooling failures.
- `.claude/settings.local.json` or Codex approved-prefix summaries, but only for
  rule shape; do not print secrets or credentials.

Do not bulk-read Claude/Codex private session transcripts. If raw logs are
needed, stop and request a separate redaction plan.

## Review Questions

1. Which approvals or tool escalations repeated?
2. Which repeated actions appear safe enough to consider pre-allowing later?
3. Which actions must remain Hard Stops?
4. Did any allowed action cause failed checks, rollback, broken runtime, or
   unsafe evidence?
5. Did sandbox, MCP, model, or subagent tooling failures change the result?
6. Did current docs/skills create avoidable friction?
7. What should change: allowlist suggestion, skill update, mission-brief rule,
   verification rule, or no change?
8. Which blockers are still active, and which were resolved by fallback,
   review, commit, push, or CI evidence?

## Guardrails

- Recommendations do not change permissions automatically.
- Never recommend pre-allowing Hard Stops from `AGENTS.md`.
- Never weaken DB, deploy, secrets, destructive git, or real client
  communication gates.
- Do not store raw transcripts, secrets, tokens, full headers, full bodies,
  database row payloads, or client-private messages.
- Keep findings local-only unless Owner explicitly approves publication.
- Treat absence of negative evidence as a signal to review, not proof of safety.
- Separate active blockers from historical friction that was already resolved.

## Output

Use the template at `docs/templates/agent-operations-review-template.md`.

Required sections:

- Executive verdict
- Evidence reviewed
- Decision: keep / simplify / merge / remove
- Permission / approval friction
- Tooling / sandbox blockers
- Subagent coordination issues
- Outcome signals
- Outcome anchors
- Safe automation candidates
- Hard Stops to preserve
- Workflow or skill updates recommended
- Risks / unknowns
- Next action

## Handoff

- **Success condition**: Control Tower has a concise local-only recommendation
  for reducing friction without weakening safety.
- **Next**: Update workflow docs or settings only through a separately approved
  Work Block.
- **Auto-proceed**: 🟢 YES for read-only review inside approved scope.
- **Hard stop**: 🔴 YES before permission changes, config changes, secret
  handling, raw transcript parsing, deploy, live DB, destructive git, or real
  client communications.
