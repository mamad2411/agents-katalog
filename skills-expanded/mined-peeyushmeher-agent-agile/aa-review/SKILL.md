---
name: aa-review
description: Use when the user wants to review a finished epic's demo, decide whether to approve, redo, or replan an epic, or invokes the review gate, for example "/aa-review", "let's review this epic", "walk me through the demo", "I want to give feedback on this epic".
license: MIT
metadata:
  system: agent-agile
---

# aa-review

Resolve the Agent-Agile playbook root: use the first of these that exists — (1) `${CLAUDE_PLUGIN_ROOT}/playbooks`, (2) `./.claude/agent-agile/playbooks`, (3) `./.agents/agent-agile/playbooks`, (4) `~/.claude/agent-agile/playbooks`, (5) `~/.agents/agent-agile/playbooks`, (6) `./playbooks`.

Read `playbooks/execution.md`'s "The review gate" section from that root, and run the gate exactly as it describes.

1. Find the current epic from `.planning/STATE.md` and `.planning/ROADMAP.md`, then read that epic's demo brief at `.planning/epics/EPIC-NN/DEMO.md`. If `DEMO.html` exists alongside it, tell the user to open that file first — it's the same brief as a clickable page (verdict banner, story table, copyable commands) — and treat `DEMO.md` as the canonical text you walk them through.
2. Walk the user through it in order: what was built, then the exact steps to test it, then what "working" looks like and the edge cases worth poking. Encourage the user to actually run the steps rather than take the brief's word for it.
3. Ask the user for exactly one outcome: approve, redo, or replan.

Whatever the outcome, any ruling the user attaches a reason to — a scope call, a tradeoff picked, a "never do X again" — gets appended as a row to `.planning/DECISIONS.md` (create it from `playbooks/templates/DECISIONS.md` if absent), so no later session re-asks a question the user already settled at a gate.

**Approve.** The epic is done. Flip its row in `.planning/ROADMAP.md` to `approved`, append the epic-level check to `.planning/CONTROL.md` (create it from `playbooks/templates/CONTROL.md` on first approval), and update `.planning/STATE.md` to point at planning the next epic.

**Redo.** Convert every tip the user just gave — and every finding already recorded from verification — into a new, concrete acceptance-check line added to the specific story card or cards it affects, at `.planning/epics/EPIC-NN/stories/S*.md`. Name the exact story each tip lands on; a tip with no obvious story owner belongs on whichever story's file list is closest to what it's about, never left as a general note. Never write a vague "make it better" line — each new check must be a runnable command or a verifiable assertion, matching the existing acceptance-check style already on that card. Once every tip is a check, instruct the user to re-run `/aa-execute-epic` for this epic, so Wave 1 re-runs the affected stories against their sharpened cards and Wave 2 re-integrates and re-verifies — or, if the redo-list qualifies for the scoped redo in `playbooks/execution.md` "The review gate" (every finding file-specific, all files owned by one story, contracts untouched), note that the re-run should take the cheap path: one fix worker plus re-verification, no full wave re-run. Update `.planning/STATE.md` to record that this epic is mid-redo and which stories changed. Once a redo's new check goes green in the re-run, it joins `.planning/CONTROL.md` — the review gate in `playbooks/execution.md` covers the minting rule.

**Replan.** The story breakdown itself was wrong, not just the implementation. Flip the epic's row in `.planning/ROADMAP.md` back to `pending`, and flag every downstream epic in `.planning/ROADMAP.md` for re-examination — a replan can invalidate assumptions later epics were built on, so those rows need a fresh look before they're trusted again. Update `.planning/STATE.md` to point at re-slicing this epic, noting what was learned that triggered the replan.
