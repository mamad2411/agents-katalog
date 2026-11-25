---
name: aa-execute-epic
description: Use when a sliced epic (story cards already written) is ready to build, or the user invokes /aa-execute-epic.
license: MIT
metadata:
  system: agent-agile
---

# aa-execute-epic

Resolve the Agent-Agile playbook root: use the first of these that exists — (1) `${CLAUDE_PLUGIN_ROOT}/playbooks`, (2) `./.claude/agent-agile/playbooks`, (3) `./.agents/agent-agile/playbooks`, (4) `~/.claude/agent-agile/playbooks`, (5) `~/.agents/agent-agile/playbooks`, (6) `./playbooks`.

Read `playbooks/execution.md` sections "Wave 0 — contracts", "Pre-flight", "Wave 1 — stories", "Wave 2 — integrate", "Verification", and "The review gate", and follow them exactly; do not re-derive or improvise the sequence.

This skill stays lean: it dispatches subagents and collects their output. It never writes application code itself.

## Wiring

1. **Wave 0 — contracts.** Spawn a fresh `aa-contractor` subagent with the model configured for the smart tier in `.planning/CONFIG.md`. Give it every story card's `Contracts consumed` field. It writes `.planning/epics/EPIC-NN/CONTRACTS.md`. Once written, treat it as frozen — do not let any later step edit it.
2. **Pre-flight.** Both checks must pass before Wave 1 launches:
   - Run the collision check: `node <playbook-root>/../scripts/collision-check.js <epic-dir>`, where `<playbook-root>` is the playbook root resolved above (in a source checkout of this repo that is simply `node scripts/collision-check.js <epic-dir>`). A clean run exits 0 with `{"ok":true}`. A collision exits 1 with a JSON report naming every contested file and the stories that claim it. On a collision, refuse to launch Wave 1 — report the exact colliding files and stories, and send the epic back to slicing so the shared file moves into `CONTRACTS.md` or the stories get merged.
   - Read `.planning/PREREQS.md`. Every row must be `verified`, or `done` in the specific case where `verified` isn't actually checkable. Run any stated verification command now — don't trust the checkbox. A `pending` row, or a `done` row whose verification command fails, blocks launch: stop and treat it exactly like the missing-prerequisite circuit breaker in `playbooks/execution.md` "Circuit breakers" rather than pushing forward.
   - Print the readiness dashboard from `playbooks/execution.md` "Pre-flight" — the gate table (contracts pinned, collisions, prerequisites, graders on every card, control-set size) and its CLEARED/BLOCKED verdict — before dispatching anything. Any ✗ row is the refuse behavior above; the dashboard renders the decision, it never softens it.
3. **Wave 1 — stories.** Spawn one fresh `aa-worker` subagent per story card, in parallel, each with the model configured for the cheap tier in `.planning/CONFIG.md`. Give each worker exactly two inputs — its own story card and `CONTRACTS.md` — nothing else: no other story's card, no wider exploration mandate. Each worker builds against its `Files it owns` list, runs its own acceptance check, and writes `.planning/epics/EPIC-NN/stories/SN.report.md` as a typed report from `playbooks/templates/REPORT.md`. A failed check starts the worker's bounded repair loop — fix and re-run, up to 3 repair rounds within the same dispatch; only an exhausted loop reports `FAIL`, and that story is flagged and not merged.
4. **Wave 2 — integrate.** Spawn a fresh `aa-integrator` subagent with the model configured for the smart tier in `.planning/CONFIG.md`. It parses every `SN.report.md`'s typed fields (flagging mechanically: FAIL status, files touched outside ownership, deviations, contract change requests), wires the cross-story seams, runs the epic-level acceptance check (the demo sentence, exercised for real — with up to 3 seam-repair rounds on failures it owns), runs every row of `.planning/CONTROL.md` when the file exists, writes `DEMO.md` and `LEARNINGS.md`, flips the epic's `ROADMAP.md` row, and updates `STATE.md`. Any flagged story from Wave 1 is its problem to resolve or note in `LEARNINGS.md` — never quietly dropped from the merge.
5. **Verification.** Spawn a fresh `aa-verifier` subagent with the model configured for the smart tier in `.planning/CONFIG.md` — someone who wrote none of the epic's code. It checks whether the demo sentence is actually true, re-runs acceptance checks rather than trusting the reports, pokes the edge cases in `DEMO.md`'s "what to look for" section, and returns a plain verdict: pass, or a redo-list of specific findings.
6. **The review gate.** Present `DEMO.md` and the verifier's verdict at the gate, per the mode set in `.planning/CONFIG.md`'s `gate` field (interactive/checkpoint/full-auto — see `playbooks/execution.md` "Autopilot" for what each mode means for who reads the gate). The gate has exactly three outcomes:
   - **Approve** — the epic is done. Append its epic-level check to `.planning/CONTROL.md` (create from `playbooks/templates/CONTROL.md` on first approval).
   - **Redo** — convert every tip and finding into a new, concrete acceptance check on the specific story or stories it affects, re-run Wave 1 for those stories and Wave 2 to re-integrate, then verify again. If the redo-list qualifies for the scoped redo in `playbooks/execution.md` "The review gate" (every finding file-specific, all files owned by one story, contracts untouched), take that path instead: one cheap-tier fix worker plus re-verification, no wave re-run — one scoped attempt only, then escalate to the full redo.
   - **Replan** — send the epic back to slicing entirely; the roadmap after it gets re-examined.

## Hard rules

- Never write application code in this skill's own context — every artifact comes from a spawned subagent.
- A worker never receives another story's card or open-ended exploration latitude; if a card can't be completed from just its card and `CONTRACTS.md`, that is a slicing defect, not something to patch around here.
- A collision or an unverified prerequisite is a full refuse, never a "proceed carefully."
- Never fake a credential or silently mock a missing paid service to get past a blocked prerequisite — that is always the missing-prerequisite circuit breaker, not a workaround.
- `CONTRACTS.md` is frozen once Wave 0 writes it; route any correction through Wave 2 or a redo, never a mid-wave edit.
