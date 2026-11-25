---
name: aa-grill
description: Use when the user has a rough or vague product idea that needs interrogation before any planning — or invokes /aa-grill. Locks the idea into .planning/IDEA.md or recommends against building it.
license: MIT
metadata:
  system: agent-agile
---

# aa-grill

Resolve the Agent-Agile playbook root: use the first of these that exists — (1) `${CLAUDE_PLUGIN_ROOT}/playbooks`, (2) `./.claude/agent-agile/playbooks`, (3) `./.agents/agent-agile/playbooks`, (4) `~/.claude/agent-agile/playbooks`, (5) `~/.agents/agent-agile/playbooks`, (6) `./playbooks`.

Read `playbooks/planner.md` section **The Grill** in full, including the **Grill → intake mapping** table inside it, and follow it exactly — do NOT re-derive or improvise the system. The interrogation script, its handling rules, and the valid "recommend not building it" outcome are all defined there; use them as written.

## How this skill runs

This is a live conversation, not a subagent job — it runs in the main loop. Ask the seven grill questions from the playbook one at a time, in order. Never dump the list at once. Apply the playbook's handling rules on every answer: a vague answer gets narrowed into a forced choice built from the answer's own words before moving on; "everyone" and "it'd be cool" are rejected outright per the playbook.

If the idea fails its own questions — no real user, no real switch reason, no number that would move — say so plainly, name which questions it failed, and recommend against building it. Stop there; do not write IDEA.md for an idea you've just recommended against.

## Closing the grill

Once all seven questions produce real answers:

1. Write `.planning/IDEA.md` from the template at `playbooks/templates/IDEA.md`, filling Problem, Exact user, The one action, Why now / why switch, Non-goals, and Success signal from the grill answers. Once written, IDEA.md is locked — do not reinterpret it later.
2. Update `.planning/STATE.md` from the template at `playbooks/templates/STATE.md`: set Project to a short working name for the idea (confirm it with the user in one breath before writing it), Phase to `grill`, Now to "grill complete, IDEA.md locked", Next to "run /aa-new-project", Pointers to `.planning/IDEA.md`, and Blockers to `none`.
3. Tell the user the grill is done and offer `/aa-new-project` as the next step. State, using the Grill → intake mapping table, exactly which of the 8 intake questions are already pre-filled from this conversation and which three (hard constraints, riskiest unknown, review-batch appetite) will still be asked fresh.
