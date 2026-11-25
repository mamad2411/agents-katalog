---
name: aa-import
description: Use when the user has an existing plan, PRD, or spec document they want brought into this planning system instead of a fresh grill and intake — or invokes /aa-import with a path or description of that document.
license: MIT
metadata:
  system: agent-agile
---

# aa-import

Resolve the Agent-Agile playbook root: use the first of these that exists — (1) `${CLAUDE_PLUGIN_ROOT}/playbooks`, (2) `./.claude/agent-agile/playbooks`, (3) `./.agents/agent-agile/playbooks`, (4) `~/.claude/agent-agile/playbooks`, (5) `~/.agents/agent-agile/playbooks`, (6) `./playbooks`.

Read `playbooks/planner.md` section **Import path** in full, and follow it exactly — do NOT re-derive or improvise the system. That section also depends on **The 8 intake questions**, **Pushback patterns**, and **Drafting the plan**; read those too before starting.

## Running the import

The skill's argument is a path to, or description of, the user's existing plan document.

1. Read the document in full — no skimming.
2. Answer the 8 intake questions from the document alone, without asking the user anything yet. Mark any thinly-answered question as a gap rather than guessing, using the same "thin answer" bar defined in **The 8 intake questions**.
3. Ask the user only the gaps, one question at a time, with the same pushback discipline as a fresh intake.
4. **Deliver the split statement** exactly as defined at the end of planner.md's **The 8 intake questions** — the "my part / your part" narration plus the process preview — before writing any files. Imported plans get it too: their authors are the users most likely to assume the system does everything.
5. Map the result onto the plan format and check the three things **Import path** names explicitly: whether the Key Results pass the three KR tests, whether every epic has a demo sentence, and whether any existing stories pass the worker-readiness test.
6. Write `.planning/PROJECT.md`, `.planning/ROADMAP.md`, and Epic 1's story cards from the templates at `playbooks/templates/PROJECT.md`, `playbooks/templates/ROADMAP.md`, and `playbooks/templates/STORY.md`, plus `.planning/PREREQS.md` and `.planning/CONFIG.md` from their templates. Produce a gap list alongside these files — what was missing or broken in the source document — not a silent rewrite. On a multi-epic import, a missing risk register is itself a gap to report: the source plan named no domain edges and no fixtures (see `playbooks/planner.md` "Research fan-out and the risk register"), and the user decides whether to run the fan-out before executing.
7. Update `.planning/STATE.md` from `playbooks/templates/STATE.md`, Phase `intake`.

## Panel and exits

Instruct the user to run `/aa-panel` next — an imported plan gets the same adversarial review as a freshly drafted one, no leniency for "it was already written." After the panel returns, resolve to exactly one of the three exits the playbook defines:

- **Proceed** — translate the document into the plan format and run the current epic.
- **Reshape** — back to intake, carrying the panel's findings as the starting gaps.
- **Kill** — write `.planning/LEARNINGS.md` from `playbooks/templates/LEARNINGS.md` explaining why, and stop.
