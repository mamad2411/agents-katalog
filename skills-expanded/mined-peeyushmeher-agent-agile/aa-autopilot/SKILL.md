---
name: aa-autopilot
description: Use when multiple epics should run back to back without a human kicking off each one by hand, or the user invokes /aa-autopilot [--gate full-auto|checkpoint].
license: MIT
metadata:
  system: agent-agile
---

# aa-autopilot

Resolve the Agent-Agile playbook root: use the first of these that exists — (1) `${CLAUDE_PLUGIN_ROOT}/playbooks`, (2) `./.claude/agent-agile/playbooks`, (3) `./.agents/agent-agile/playbooks`, (4) `~/.claude/agent-agile/playbooks`, (5) `~/.agents/agent-agile/playbooks`, (6) `./playbooks`.

Read `playbooks/execution.md` sections "Autopilot" (including "The ambiguity protocol"), "Circuit breakers", and "Resume protocol", and follow them exactly; do not re-derive or improvise the loop or soften a circuit breaker.

## Wiring

1. **Gate mode.** Parse a `--gate full-auto|checkpoint` argument. If absent, use the `gate` field in `.planning/CONFIG.md`. If neither is set, the mode is interactive.
2. **Preflight.** Run the same collision check and `PREREQS.md` check as `/aa-execute-epic`'s pre-flight, before the loop starts at all — an autopilot run never begins on an unchecked epic.
3. **The loop.** For each pending epic in `.planning/ROADMAP.md`, in order:
   - Run the `/aa-plan-epic` behavior to slice the next pending epic into worker-ready story cards.
   - Run the `/aa-execute-epic` behavior for that epic: Wave 0 through Verification.
   - Re-run the pre-flight prerequisite check for this epic specifically before Wave 1 launches — prerequisites can go stale between epics (a key expires, a quota runs out), so this is deliberate, not redundant with step 2.
   - Apply the gate for this epic:
     - **Full-auto** — the verifier's verdict stands in for the human: pass approves, a redo-list triggers the redo path. Demo briefs accumulate so a human can review the whole run's `DEMO.md` files at the end.
     - **Checkpoint** — the epic runs and verifies automatically; notify the user only between epics, at natural pause points, rather than gating every single one.
     - **Interactive** — stop and present `DEMO.md` and the verifier's verdict to the user at this epic, exactly as a standalone `/aa-execute-epic` run would.
   - On approve, the integrator has already written `LEARNINGS.md` and flipped the `ROADMAP.md` row (per Wave 2); move to the next pending epic.
   - On redo or replan, follow "The review gate" in `playbooks/execution.md`, then resume the loop from that epic once it re-verifies.
4. **Circuit breakers.** Follow the circuit breakers in `playbooks/execution.md` "Circuit breakers" exactly as written — never push through or work around one (a panel-refresh BLOCK left unresolved at slicing time also stops the loop, per `playbooks/critics.md` "Panel refresh"):
   - An epic fails verification even after its full redo — stop the autopilot loop entirely. The most an epic ever gets is: fail → scoped redo (if eligible) → fail → full redo → fail → stop.
   - A prerequisite goes missing mid-run — stop immediately, reset its `PREREQS.md` status to `pending`, and notify whoever needs to resupply it.
   - Never fake a credential and never silently mock a missing paid service.
5. **Stopping.** Whenever the loop stops — a circuit breaker, an interactive gate, the end of the roadmap, or a context reset — update `.planning/STATE.md` per "Resume protocol": what's in progress, what's next, the pointers the next session needs (at most three files), and the blocker if there is one. `STATE.md` must say exactly where the run stopped and why; the next session reads only this file to resume.

## Hard rules

- Preflight is mandatory before the loop launches and again before every epic inside it — never skip the per-epic re-check to save a step.
- Any ambiguity the plan doesn't answer goes through the ambiguity protocol in `playbooks/execution.md` "Autopilot": check `.planning/DECISIONS.md` first (settled = applied, never re-asked), auto-resolve only what is reversible, pattern-matching, free, and security-clean (recording it in the ledger), and treat irreversible/paid/security ambiguity in full-auto as a circuit breaker — never guess on the user's behalf.
- A circuit breaker always stops the loop; it is never a reason to substitute a fake key, a stub response, or a "pretend this succeeded" workaround.
- Gate mode is fixed for the whole run once set at the start — don't silently switch modes mid-loop because one epic looks safe.
- Every session, including one that stops mid-loop, closes with exactly one `STATE.md` update — never leave the next session to reconstruct status from the epic history.
- Run the predictive budget check at every wave and epic boundary (the context budget in `playbooks/system.md` "The agent tree"): if current fill plus the next unit's estimated footprint crosses roughly 60% — or fill alone is past 40–50% — write `STATE.md` at the boundary and stop cleanly for a fresh-session resume before launching anything. This is routine hygiene, not a circuit breaker — a resumed loop is identical to one that never stopped, while a loop that rides to auto-compaction finishes its roadmap with the model at its weakest.
- The roadmap is done only when the evidence is on disk — every epic row flipped and the final epic's verifier verdict written and passing (the completion promise in `playbooks/execution.md` "Autopilot"). A loop that ends without that evidence reports itself as stopped, not done.
- Before any second redo of the same epic, run the unsatisfiable-check diagnosis in `playbooks/execution.md` "The review gate": identical finding + unchanged files = verifier-only recheck then breaker, never another paid wave.
