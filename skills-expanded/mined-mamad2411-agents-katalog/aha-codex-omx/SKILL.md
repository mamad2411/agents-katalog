---
name: aha-codex-omx
description: "Mode switch for Codex+OMX: full delegation x full capability surface x per-task OMX sub-mode matching. NOT for trivial edits, quick Q&A, read-only exploration, or when user says 'do it natively'."
---

# Aha-Codex-OMX — Full Power + Full Delegation Mode

Activates the full Codex+OMX (oh-my-codex, https://github.com/Yeachan-Heo/oh-my-codex) delegation surface. This is a stance declaration, not a procedure library.

## What This Mode Activates

- Full delegation: route each task to the appropriate OMX sub-mode by default, rather than executing natively.
- Full capability surface: all OMX sub-modes (planning, execution, review, research, team) are available — NOT locked to one sub-mode like autopilot.
- Per-task sub-mode matching: judge each task independently and select the matching OMX category.

## Pre-Check (Before Activating)

1. Verify OMX is installed and reachable: `omx --version`
2. Verify you are in a Codex session. If in OpenCode, point user to aha-opencode-omo instead — this skill is for Codex+OMX only.

## Sub-Mode Matching (NOT locked — judge per task)

Map task type to OMX sub-mode CATEGORY. Do not hardcode individual skill names — OMX has 48 catalog entries with frequent renames and deprecations (16 deprecated as of v0.18.1).

| Task type | OMX category |
|-----------|-------------|
| Planning, design, architecture | planning |
| Execution, implementation | execution |
| Team orchestration, parallel lanes | team |
| Review, QA gate | review |
| Research, investigation | research |

Run `omx list` for the current active skills — this is the dynamic source of truth.

Autopilot still requires the task to genuinely need a full gate loop. Do not default to autopilot for straightforward or bounded work.

## Retained Safety Boundaries (mode does NOT override)

Full delegation does NOT extend to the following. Subagents must pause and ask how:

- Credential/session material access or transport
- Provider config, quota, or billing operations
- Browser/CDP attach or session write
- Live draft, publish, deploy, or external write
- Global runtime config mutation
- OMX setup, update, or uninstall
- Primary gateway or root routing changes

## Do NOT Use This Mode For

- Trivial single-file edits
- Quick Q&A or informational lookup
- Read-only exploration or research
- When the user explicitly says "do it natively" or "don't delegate"

## Delegation Failure Handling

If a delegated subagent returns garbage or errors:

1. Re-delegate with clearer, more specific instructions
2. Escalate to a stronger sub-mode (e.g., plan -> autopilot)
3. Fall back to native execution

Do NOT silently accept garbage output.

## Native-First Resting State

This mode is explicit opt-in per task chain. Native-first is the default resting state. When the task chain completes or the user does not re-invoke the mode, return to native-first execution.

## Cost Awareness

Multi-agent delegation consumes more tokens than native single-pass. If the user signals cost concern, fall back to native-first.

## Rollback / Deactivation

- Soft: stop invoking the mode. Return to native-first.
- Hard: delete `~/.codex/skills/aha-codex-omx/` directory, then restart Codex — Codex caches skill metadata until restart.
