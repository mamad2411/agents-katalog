---
name: sdlc-guided
description: Starts a human-in-the-loop agentic-sdlc run from a task description, an external work-item reference, or a greenfield idea. Triggers include "start sdlc", "implement this with sdlc", "begin SDLC workflow", or a request for the legacy sdlc:start command on a skills-based host. Not for: autonomous runs (sdlc-auto), pre-sized small tasks (sdlc-brief / sdlc-direct), or resuming an existing run (sdlc-runs).
version: 0.1.0
license: Apache-2.0
discoverable: true
authors:
  - agentic-os
---

# sdlc-guided

## Shared contract preflight

Before workflow actions, send this JSON request to the installed plugin's
`runtime/run.py` using Python 3.10+ (resolve the plugin root on the current host):

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"sdlc-guided"}
```

Use the returned policy and `references/runtime-contracts.md` for contract identifiers,
limits and dependency floors. Unknown fields or incompatible versions block startup.
Task envelopes use `contract_version: "1.0.0"` and `task_input`; legacy `raw_input`
is accepted only by the explicit `input.normalize` compatibility adapter with `legacy: true`.
This preflight validates policy; durable lifecycle and host enforcement are separate
capabilities. Never infer those capabilities from a successful policy response.


The doorway into the human-in-the-loop agentic-sdlc flow. On hosts like Codex
that have skills but no commands, this stands in for the retired `sdlc:start`
command.

## Stay a doorway

A doorway that starts doing the work is no longer a doorway, and a run whose
artifacts were half-written before Phase 0 cannot be reasoned about. So this
skill reads intent and delegates; it does not touch the repository.

Specifically, nothing here may:

- Make `.agentic/runs/<run-id>/`, or any other run or task directory.
- Write `meta.json`, `requirements.md`, `complexity.json`, `design.md`,
  `plan.md`, `events.jsonl`, `decisions.jsonl`, `work-item.md`, or any ledger.
- Do a phase's work early — no intake, no sizing, no brainstorming, no
  planning, no branch guard, no building, no QA, no status repair.
- Improvise `sdlc-engine` because the host would not invoke it.

That last one is the tempting failure. If `sdlc-engine` cannot be reached,
say startup is blocked and stop there. A hand-rolled approximation looks
helpful and leaves behind artifacts nothing downstream can trust. Ownership of
every artifact starts inside `sdlc-engine` Phase 0, and not one step sooner.

## When the project owns implementation

Read `.agentic/agentic-sdlc/config.json` before delegating. If it names project orchestrators, pass their
routing contract through to `sdlc-engine`: this package still owns intake,
planning, QA and the delivery handoff, while implementation is delegated once to
the orchestrator the project selected. Fleet workers are never called directly —
going around the project's own orchestrator is how two pipelines end up believing
they own the same change.

## Inputs

- `task_input` — whatever the user is asking for: prose, a tracker reference, or
  a path to a story file
- `mode_flag` — `--greenfield` when starting from nothing, otherwise unset
- `escalate_on` — risk flags that force a human decision; defaults to
  `["security", "breaking-change", "migration", "spend"]`

## Usage Examples

```text
Use the sdlc-guided skill for "rate-limit the public search endpoint"
Use the sdlc-guided skill for PROJ-812
Use the sdlc-guided skill with --greenfield "small Go service that signs webhooks"
```

## Steps

1. Take the user's own words as `task_input` — normalize whitespace, not meaning.
2. If `--greenfield` appears, set `mode_flag` to it and treat the rest as
   `task_input`.
3. Call the `sdlc-engine` skill:

   ```json
   {
     "contract_version": "1.0.0",
     "mode": "hitl",
     "task_input": "<the user's request, verbatim>",
     "mode_flag": null,
     "escalate_on": ["security", "breaking-change", "migration", "spend"]
   }
   ```

4. Hand over. The pipeline picks up at Phase 0, and because the mode is `hitl`,
   every judgment gate reaches the user through `gate-arbiter` instead of
   being decided for them.
5. Do nothing further. Any later artifact belongs to `sdlc-engine` or to one
   of the phase skills it calls.

## Preconditions

A full run reads a repo-guides baseline. When `.agentic/guides/` is missing
files, `sdlc-engine` halts and points at the `repo-guides` skill — this skill
does not pre-check that.

Before the pipeline reaches a phase that can write code, it must clear the
branch guard: current branch, configured base, `git status --porcelain`,
upstream state, whether the target branch exists, how to resolve a dirty tree,
and whether the base is current.

## Notes

- Verifying `superpowers` is Phase 0's job, not this skill's.
- There is no workflow logic here to maintain. Read intent, delegate, stop.
- The test of a correct response: it wrote nothing. Either the normalized inputs
  reached `sdlc-engine`, or the reply explains that delegation is blocked.
