---
name: aa-new-project
description: Use when the user wants to plan a new project from a clear idea, has already locked an idea with aa-grill, or invokes /aa-new-project.
license: MIT
metadata:
  system: agent-agile
---

# aa-new-project

Resolve the Agent-Agile playbook root: use the first of these that exists — (1) `${CLAUDE_PLUGIN_ROOT}/playbooks`, (2) `./.claude/agent-agile/playbooks`, (3) `./.agents/agent-agile/playbooks`, (4) `~/.claude/agent-agile/playbooks`, (5) `~/.agents/agent-agile/playbooks`, (6) `./playbooks`.

Read `playbooks/planner.md` sections **The 8 intake questions**, **Pushback patterns**, **Drafting the plan**, **Research fan-out and the risk register**, **Slicing epics into stories**, **The worker-readiness test**, and **Extracting PREREQS**, in full, and follow them exactly — do NOT re-derive or improvise the system.

## Intake

If `.planning/IDEA.md` exists, read it and, per planner.md's Grill → intake mapping, confirm the pre-filled answers back to the user instead of re-asking them. Ask only the questions the grill didn't answer, plus the three it never answers (hard constraints, riskiest unknown, review-batch appetite) — always fresh. If IDEA.md does not exist, ask all 8 questions from scratch, one at a time, applying the pushback patterns to every thin answer before moving on.

After the eighth answer and before writing any files, **deliver the split statement** exactly as defined at the end of planner.md's **The 8 intake questions** — the "my part / your part" narration plus the process preview. It is a required step, not optional color.

## Drafting

Draft the plan inline in this conversation, following **Drafting the plan** — this is the default; do not spawn a separate agent for this step unless the user asks for it. Produce, in order:

1. `.planning/PROJECT.md` from `playbooks/templates/PROJECT.md`.
2. `.planning/ROADMAP.md` from `playbooks/templates/ROADMAP.md` — every epic, riskiest first, one-line demo sentences; only the current epic (Epic 1) gets full detail.
3. If the roadmap draft is multi-epic, run **Research fan-out and the risk register** exactly as written (including its off-ramp): spawn `aa-researcher-domain` and `aa-researcher-ecosystem` as parallel fresh subagents with the model configured for the smart tier in `.planning/CONFIG.md` (ask for tiers now if CONFIG.md doesn't exist yet), synthesize `.planning/RESEARCH.md` from `playbooks/templates/RESEARCH.md`, then revise the roadmap draft against the risk register — `[fixture: …]` tags on epic lines, Epic 1/2 riskiest-first re-examination.
4. Slice Epic 1 into story cards per **Slicing epics into stories**, writing each from `playbooks/templates/STORY.md` — including one fixture story per `[fixture: …]` tag on Epic 1. Apply **The worker-readiness test** to every card before calling it done.
5. `.planning/PREREQS.md` from `playbooks/templates/PREREQS.md` per **Extracting PREREQS**, status `pending` for every row.
6. `.planning/CONFIG.md` from `playbooks/templates/CONFIG.md` — ask the user for smart_tier, cheap_tier, gate, and commercial if not already set.
7. `.planning/STATE.md` from `playbooks/templates/STATE.md`, Phase `intake`, pointing at PROJECT.md, ROADMAP.md, and Epic 1's stories.

## Handoff

If the roadmap has more than one epic, tell the user the plan must go through the panel before anything runs, and instruct them to run `/aa-panel` next — do not start execution first. If the roadmap is a single throwaway epic, the panel may be skipped — see the gate rule in `playbooks/critics.md` section `Panel protocol`; say so and name the next command instead.
