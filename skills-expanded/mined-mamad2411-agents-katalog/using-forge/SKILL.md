---
name: using-forge
description: >
  Forge dispatch skill: the session bootstrap that makes Forge's skills auto-trigger as a
  reasoning-driven SYSTEM. Reach for this FIRST, before ANY response (including clarifying
  questions, codebase exploration, or file reads), whenever there is even a 1% chance a Forge
  skill applies. Carries the 1%-rule, the announce-before-acting rule, an anti-rationalization
  red-flags table, a subagent escape hatch, and an intent-to-skill routing table: add/build/scope
  a feature to plan; implement an existing task to dev; fix a failing test or bug to dev (debug
  first); type-check/lint/tests to validate; push and open a PR to ship; address PR/review
  feedback to review; post-merge health to verify; what to work on to triage-ready; where am I /
  current stage to status; create/close/search an issue to issue-basics; drive one issue
  end-to-end to smith; monitor a PR to shepherd. Run `forge skill for "<situation>"` for a
  deterministic fallback. NOT itself a stage; the kernel skill is the fuller umbrella index
  once oriented.
allowed-tools: Read, Bash(forge:*)
terminal: true
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute one specific task, ignore this skill and do
the task you were given. This dispatch rule is for the top-level session, not for a scoped
subagent — otherwise every subagent would re-enter routing instead of working.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a Forge skill applies to what you are doing, you MUST
invoke that skill BEFORE any response or action.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of it.
</EXTREMELY-IMPORTANT>

## The rule

**Invoke the relevant or requested Forge skill BEFORE any response or action** — including
clarifying questions, exploring the codebase, or checking files. If it turns out wrong for the
situation, you don't have to follow it — but you check first.

Then **announce** `Using [skill] to [purpose]` and follow the skill exactly. If it has a
checklist or HARD-GATE, create one todo per item.

When unsure WHICH skill fits, either consult the routing table below or run
`forge skill for "<what you are about to do>"` for a deterministic best-fit answer.

## Intent → skill routing table

Process skills set the approach first; then the stage/implementation skill carries it out.

| When the situation is… | Start with |
|------------------------|-----------|
| "Add / build / scope a new feature", "let's build X" | `plan` |
| Implement a task that a plan already defined | `dev` |
| "Fix this bug" / a failing test / unexpected behavior | `dev` (if `superpowers:systematic-debugging` is installed, apply its technique first, then implement via `dev`) |
| Run type-check, lint, security, or tests | `validate` |
| Push the branch and open a PR | `ship` |
| Address PR / review-agent feedback (CodeRabbit, Greptile, CI) | `review` |
| Post-merge health check, close issues | `verify` |
| "What should I work on?" — rank the ready queue | `triage-ready` |
| "Where am I?" / current stage / stale or active work | `status` |
| Create / update / close / search / comment on ONE issue | `issue-basics` |
| Claim an issue and PROVE the lease before mutating | `claim-safety` |
| Drive one issue plan→merged-PR under human gates | `smith` |
| Monitor / shepherd a PR's CI + checks (never merges) | `shepherd` |
| Deep, multi-source web research | `research` / `parallel-deep-research` |
| "How does Forge fit together?" / which verb for X | `kernel` |
| Safe revert / undo a merged change | `rollback` |

If two skills seem to apply, run the process skill first (`plan`, `systematic-debugging`), then
the doing skill. `kernel` is the umbrella index — use it to orient, not to do the work.

## Red flags — these thoughts mean STOP, you are rationalizing

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for a skill. |
| "I need more context first" | The skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for a skill. |
| "This doesn't need a formal stage" | If a skill exists, use it. |
| "I remember what that skill says" | Skills evolve. Read the current version. |
| "The skill is overkill here" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "It's obviously a plan/dev/ship" | Then invoking it costs nothing. Invoke it. |

## Subagent escape hatch

You do NOT have to hold every skill in your own context. When a task is independent and
bounded, dispatch a subagent with the specific skill and a self-contained brief, and keep only
its conclusion. Parallelize independent tasks (see `superpowers:dispatching-parallel-agents`).
Reviewers/verifiers that find nothing must say so and name what they inspected.

## Agent-agnostic

This skill syncs to every harness mirror (`.agents/`, `.claude/`, `.codex/`, `.cursor/`,
`.hermes/`), and the same routing guidance is reachable via `forge skill for "<situation>"` on
any harness — never branch on harness identity. On Claude the SessionStart hook injects this
text automatically; elsewhere, AGENTS.md points here and the CLI router is the fallback.

## User instructions win

CLAUDE.md / AGENTS.md and direct user requests take precedence over skills, which in turn
override default behavior. Skip a skill only when your human partner explicitly tells you to.
