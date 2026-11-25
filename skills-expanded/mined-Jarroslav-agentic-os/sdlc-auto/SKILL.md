---
name: sdlc-auto
description: Start an autonomous ("factory mode") SDLC run from a task description, external work-item reference, story path, or greenfield idea, on hosts that support skills but not custom slash commands. Trigger on "run autonomously", "factory mode", "ship this without asking", or a request for the legacy `sdlc:autonomous` command. Parses free-form intent into a structured payload and hands off to sdlc-engine — carries no orchestration logic of its own. Not for: human-in-the-loop runs (sdlc-guided), pre-sized small tasks (sdlc-brief / sdlc-direct), or carrying orchestration logic of its own.
version: 0.1.0
license: Apache-2.0
discoverable: true
author: agentic-os
---

# sdlc-auto

## Shared contract preflight

Before workflow actions, send this JSON request to the installed plugin's
`runtime/run.py` using Python 3.10+ (resolve the plugin root on the current host):

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"sdlc-auto"}
```

Use the returned policy and `references/runtime-contracts.md` for contract identifiers,
limits and dependency floors. Unknown fields or incompatible versions block startup.
Task envelopes use `contract_version: "1.0.0"` and `task_input`; legacy `raw_input`
is accepted only by the explicit `input.normalize` compatibility adapter with `legacy: true`.
This preflight validates policy; durable lifecycle and host enforcement are separate
capabilities. Never infer those capabilities from a successful policy response.


Skill-based entry point for autonomous-mode SDLC runs, for hosts (for example Codex) that
expose skills but not custom slash commands. Everything this skill does is intent
normalization and delegation — it holds zero workflow, QA, review, or git logic itself. All
phase execution lives in `sdlc-engine`; all gate resolution lives in `gate-arbiter`.

Treat this skill as a thin adapter in front of the legacy `sdlc:autonomous` command, mirroring
whatever human-in-the-loop entry point exists alongside it in the same skill family.

## When to invoke

- The user says "run autonomously", "factory mode", or "ship this without asking".
- The user asks for the legacy `sdlc:autonomous` command on a host that has no slash-command
  support.

## What this skill does not do

- Does not implement any SDLC phase, QA check, code review, or test logic.
- Does not create branches, commits, or open an MR/PR — autonomous mode never auto-merges and
  never opens an MR/PR by itself; the delegated pipeline halts after its branch-ready phase
  and hand-off to an MR/PR tool is a separate, manual step.
- Does not resolve judgment gates directly — every gate routes through `gate-arbiter`.
- Does not generate missing guide files, bypass the branch-guard, or auto-stash / hard-reset /
  force-push a dirty working tree absent explicit project policy allowing it.

## When the project owns implementation

Read `.agentic/agentic-sdlc/config.json` before delegating. A configured project orchestrator stays the sole
coordinator of its fleet even here — unattended mode changes who answers the
gates, not who owns the work. Hand it one bounded implementation request, consume
only summaries and serialized gate results, and stop at every human gate the
project declares.

Running unattended never relaxes a restriction: commit, push, migration, release
and production limits apply exactly as they do with someone watching.

## Inputs

| Field | Type | Default | Notes |
|---|---|---|---|
| `task_input` | string | — | Task text, work-item reference, story path, or greenfield idea |
| `mode_flag` | string/enum | none | Only `--greenfield` is recognized |
| `escalate_on` | string[] | `["security", "breaking-change", "migration", "spend"]` | CSV or list-style input |

Recognized CLI-style flags inside `task_input`: `--greenfield`, `--escalate-on`.

## Operating steps

1. **Parse `--greenfield`.** If the input contains `--greenfield "<text>"`, set
   `mode_flag = "--greenfield"` and capture `<text>` as `task_input`.
2. **Parse `--escalate-on`.** If the input contains `--escalate-on <comma-list>`, split the list
   on commas into the `escalate_on` array. If absent, use the default
   `["security", "breaking-change", "migration", "spend"]`.
3. **Capture the remainder.** Whatever text is left unconsumed by the two flags becomes
   `task_input` (verbatim, if no `--greenfield` flag was present).
4. **Delegate.** Invoke the `sdlc-engine` skill with `mode: "autonomous"` plus the three
   parsed fields — see payload shape below. Do not run any pipeline phase yourself.
5. **Gate resolution.** Every judgment gate inside the delegated pipeline resolves through
   `gate-arbiter`, in this priority order: mandatory escalation checks first, deterministic validation next, eligible fast-path
   approvals next, and an advisory stand-in only when needed. The coordinator owns the decision.
6. **Escalation.** The coordinator asks the user when confidence is low, a required approval is
   missing, a budget is exhausted, or a risk flag intersects the run's `escalate_on` set.
   Silence never grants approval.
7. **Precondition gate — `repo-guides`.** If required guide files under `.agentic/guides/` are
   absent, the pipeline halts immediately and the user is redirected to run the `repo-guides`
   skill first. This skill never generates guides itself.
8. **Branch-guard gate.** Must clear before any implementation-capable phase. Checks, in order:
   current branch; configured base branch; `git status --porcelain`; upstream tracking state;
   target-branch existence; dirty-state resolution; latest-base sync.
9. **Dirty-tree rule (autonomous mode).** A dirty working tree halts the run unless project
   policy explicitly allows auto-stash. Hard-reset or force-push-forward on a dirty tree is
   disallowed regardless of any other setting.
10. **Audit.** Every routed decision is committed through the runtime `decision.record`
    operation for the run, regardless of outcome. Refresh `<run_dir>/decisions.jsonl` with
    `legacy.export` only as a compatibility view; never append directly when the runtime is
    available.

## Delegation payload

Field names and literal values below are exact — do not rename or restructure when calling
`sdlc-engine`:

```json
{
  "contract_version": "1.0.0",
  "mode": "autonomous",
  "task_input": "<as captured>",
  "mode_flag": null,
  "escalate_on": ["security", "breaking-change", "migration", "spend"]
}
```

## Outputs

- A running (or halted-at-gate) `sdlc-engine` invocation in `mode: "autonomous"`.
- An authoritative runtime decision ledger, with `<run_dir>/decisions.jsonl` regenerated as a
  compatibility view for older readers.
- On success, a branch left at Phase 12 (branch-ready stop point) with no MR/PR opened.
  Hand the result to `mr-submit` (or an equivalent PR tool) as a separate, explicit step.
- On a precondition failure, a redirect instructing the user to run `repo-guides` before
  retrying.

## References

This skill carries no `references/` tree of its own — it has no workflow logic to document.
All reference material for phase behavior, gate checklists, and escalation rules lives in the
skills it delegates to:

- `sdlc-engine` — phase execution, including the Phase 12 branch-ready stop point.
- `gate-arbiter` — gate priority order, escalation-rule evaluation, and the
  `decisions.jsonl` / `events.jsonl` audit ledger format.
- `repo-guides` — populates `.agentic/guides/`, the prerequisite this skill checks for.
- `mr-submit` — the manual follow-on step for opening an MR/PR once Phase 12 is reached.
