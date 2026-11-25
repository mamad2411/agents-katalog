---
name: aa-panel
description: Use when a drafted plan (PROJECT.md, ROADMAP.md, and the current epic's story cards) needs adversarial review before execution starts, or the user invokes /aa-panel.
license: MIT
metadata:
  system: agent-agile
---

# aa-panel

Resolve the Agent-Agile playbook root: use the first of these that exists — (1) `${CLAUDE_PLUGIN_ROOT}/playbooks`, (2) `./.claude/agent-agile/playbooks`, (3) `./.agents/agent-agile/playbooks`, (4) `~/.claude/agent-agile/playbooks`, (5) `~/.agents/agent-agile/playbooks`, (6) `./playbooks`.

Read `playbooks/critics.md` in full — Panel protocol, Product critic, Spec auditor, Execution auditor, Market critic, Verdict format — and follow it exactly; do not re-derive or improvise the panel's doctrine. The panel gate in Panel protocol applies here: run this skill only for multi-epic projects — a single-epic throwaway skips the panel entirely.

## Wiring

1. Read the draft plan: `.planning/PROJECT.md`, `.planning/ROADMAP.md`, the current epic's story cards at `.planning/epics/EPIC-NN/stories/S*.md`, `.planning/epics/EPIC-NN/CONTRACTS.md` if it exists, and `.planning/RESEARCH.md` if it exists (per Panel protocol, the spec auditor alone receives it).
2. Read `.planning/CONFIG.md` for the `smart_tier` and `commercial` fields.
3. Spawn `aa-critic-product`, `aa-critic-spec`, and `aa-critic-execution` as parallel fresh subagents, each with the model configured for its tier in `.planning/CONFIG.md`. If `commercial: yes`, also spawn `aa-critic-market` the same way. Give each subagent exactly two inputs: its two sections of `playbooks/critics.md` verbatim — `Panel protocol` plus its own critic section (the same pair its agent definition names) — and the full draft plan gathered in step 1; nothing else. They do not see each other's output.
4. Collect every subagent's Verdict format block.
5. Fix every `BLOCK` finding by invoking planner behavior per `playbooks/planner.md` — spawn a fresh `aa-planner` subagent with the model configured for the smart tier in `.planning/CONFIG.md`, or apply the fix inline in the main loop if already holding full planning context; inline is default. Only the critic(s) whose findings forced a structural change get re-run, and only once.
6. Present the remaining `FLAG` findings plus the fixed plan to the user; the user's decision is the gate.
7. If the market critic's verdict is `KILL`, present its evidence and recommend stopping instead of presenting the plan for approval. If the user agrees to stop, write `.planning/epics/EPIC-NN/LEARNINGS.md` from `playbooks/templates/LEARNINGS.md` explaining why, and stop.
8. Update `.planning/STATE.md` to record the outcome of the gate.
