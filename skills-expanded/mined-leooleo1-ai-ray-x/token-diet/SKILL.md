---
name: token-diet
description: Ask the raiox agents (Ray, Diet, Memo) how much context this session carries and how to carry less. Run it only when the person types /token-diet.
disable-model-invocation: true
---

# Token diet

Most of an agent's cost is re-reading its own context on every request.
Ask the three raiox agents, from the project root, in this order. In the
panel (`raiox open`) the same three answer inside each project's bot chat.

1. **Ray, this session:** `./target/release/raiox ask ray`. Report the
   context carried, what weighs most since the last compaction, and, above
   400K tokens, suggest finishing the current step and running `/compact`.
2. **Diet, what to cut:** `./target/release/raiox ask diet`. Give the top
   three suggestions in one line each, with the net saving (already counting
   summaries and re-reads) and the compaction point it would use. Never edit settings yourself: the person
   applies changes in the panel, which keeps a backup and an undo.
3. **Memo, what we kept:** `./target/release/raiox ask memo`. Say how many
   lessons are kept and whether ai-memory knows this project.

These commands only work in projects that have this skill installed. Keep
your answer short: everything you print stays in this session's context too.
