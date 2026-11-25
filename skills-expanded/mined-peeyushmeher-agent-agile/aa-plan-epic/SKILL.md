---
name: aa-plan-epic
description: Use when the current epic on the roadmap is done and the next pending epic needs to be sliced into worker-ready story cards, or the user invokes /aa-plan-epic.
license: MIT
metadata:
  system: agent-agile
---

# aa-plan-epic

Resolve the Agent-Agile playbook root: use the first of these that exists — (1) `${CLAUDE_PLUGIN_ROOT}/playbooks`, (2) `./.claude/agent-agile/playbooks`, (3) `./.agents/agent-agile/playbooks`, (4) `~/.claude/agent-agile/playbooks`, (5) `~/.agents/agent-agile/playbooks`, (6) `./playbooks`.

Read `playbooks/planner.md` sections "Slicing epics into stories" and "The worker-readiness test", `playbooks/system.md` section "The memory spine", and `playbooks/critics.md` section "Panel refresh", and follow them exactly; do not re-derive or improvise the slicing process. When the epic is a UI epic (its demo sentence describes something a person sees or clicks), also read `playbooks/design.md` and apply it: design directions before Wave 0 on the first UI epic with no design system (2–4 self-contained HTML mockups, pick recorded in `.planning/DECISIONS.md`, tokens into the contracts), and a data-verify contract on every UI story card.

## Wiring

1. Read exactly three files — the three-file epic-to-epic read rule from "The memory spine": `.planning/PROJECT.md`, `.planning/ROADMAP.md`, and the previous epic's `LEARNINGS.md`. Read nothing else from prior epics, with the memory spine's two slicing-time exceptions: read `.planning/DECISIONS.md` when it exists (settled decisions carry forward, never re-opened), and run one targeted grep across all prior epics' `LEARNINGS.md` for this epic's files and topics — a search, never a read-everything; bake any hits into the story cards.
2. Identify the next pending epic on the roadmap.
3. Slice it into story cards per `playbooks/planner.md` "Slicing epics into stories": enumerate every shared artifact, assign each one to Wave 0 or to exactly one story, pairwise-check every story's file list against every other story's in the same wave for overlap, and assign waves — Wave 0 (contracts and shared setup), Wave 1 (parallel stories with no cross-story reads), Wave 2 (integration, with an epic-level acceptance check tied to the demo sentence).
4. Write each story card to `.planning/epics/EPIC-NN/stories/S*.md` from `playbooks/templates/STORY.md` — one file per story, exactly the five fields: Goal, Files it owns, Acceptance check, Grader, Contracts consumed. Split a story only for parallel width or fresh-mind verification, per `playbooks/planner.md` "Slicing epics into stories" — never because two things merely feel like separate concerns.
5. Run the worker-readiness test from `playbooks/planner.md` "The worker-readiness test" against every card in the epic — no sampling. A card that fails gets split, sharpened, or has its ambiguity moved into Wave 0's `CONTRACTS.md`. Do not report the epic sliced while any card still fails the test.
6. **Panel refresh check.** If `ROADMAP.md` holds 5 or more epics and the epic just sliced sits in the 4th, 7th, 10th … row position (current row order, re-derived now, never stored), run the panel refresh per `playbooks/critics.md` "Panel refresh": read `.planning/CONFIG.md` for the smart tier (the deliberate, narrow exception to step 1's three-file rule), spawn `aa-critic-spec` and `aa-critic-execution` as parallel fresh subagents with standard panel inputs, fix every BLOCK inline with the affected critic re-run once, and route FLAGs by gate mode as the playbook defines. A BLOCK still standing after the re-run stops an autopilot run with a `STATE.md` update, exactly like a circuit breaker. Run the KR-drift tripwire against the `LEARNINGS.md` already in hand from step 1.
7. Update `.planning/STATE.md`: phase set to the new epic's wave, what's in progress, the next action, and pointers to the files the next session must read.
