---
name: remembering
description: Save durable facts into the org's memory via bonez:memory. Use when the user says "remember", "from now on", "always", or "never", when you learn a durable preference, convention, decision, or correction, when you hit a non-obvious gotcha worth keeping, or when deciding whether something belongs in long-term memory.
---

# Remembering

Facts saved through `bonez:memory` are mounted into the context of FUTURE sessions — yours and every other agent's in this org, in any harness. A good memory is one that will still be true, useful, and understandable next week with none of this conversation's context.

Saving is a PRIMARY action, not end-of-task cleanup. The moment you learn something durable, save it right then, while you can still phrase it well. Under-saving is the common failure: a fact you don't store is a mistake the whole org repeats.

```json
{"op": "save", "content": "POC repos push straight to main, not via a PR.", "layer": "org", "temporality": "static"}
```

`recall` is free — use it liberally. `save`/`update`/`delete` are writes; the plugin gates them behind a permission prompt, so expect the harness to ask — that is the gate working, not an error.

## WHEN to remember

- The user tells you to. "Remember that…", "from now on…", "always/never…" is an explicit, non-negotiable save.
- A durable USER fact (`layer: personal`): who they are, how they want you to work, a standing preference.
- FEEDBACK — a correction or confirmed-good approach. Save the correction AND the reason, so future sessions apply the principle, not just the instance.
- A durable ORG fact (`layer: org`): a convention, process, rule, or decision that applies beyond this task.
- A REFERENCE the user relies on repeatedly — dashboard, ticket system, doc, channel — and what it's for.

## WHEN NOT

- One-off details that only matter to the task in front of you.
- Anything recoverable from the code or the graph. Memory is for what is NOT re-derivable — if asked to remember something recoverable, save the non-obvious part (the why, the gotcha) instead of the raw fact.
- How a specific symbol behaves — that is knowledge attached to code, not a memory.

If your only hesitation is durability, save it as `temporality: temporal` rather than dropping it — temporal memories are cheap to supersede, and a slightly-stale memory beats a lost one.

## NEVER STORE (hard rules)

- Secrets or credentials of ANY kind — passwords, API keys, tokens, connection strings, `.env` values — even if the user pastes one into chat. They belong in a secret store, never in memory.
- Sensitive personal data (health, ethnicity, religion, orientation, politics, precise location, financial account numbers) UNLESS the user explicitly and specifically asks.

## How to write a good one

- One or two sentences that stand ALONE. "The deploy script lives in infra/, not the app repo" — never "it's in the other one". Resolve relative dates to absolute.
- Pick the layer: `personal` = about the user · `org` = about the organization.
- Pick temporality: `static` = always true · `temporal` = can change later (superseded, not duplicated).

## Before you save

- Sensitive, or contradicts a memory already in your context? Confirm with the user first.
- Already mounted? Don't re-save. Fact changed? `{"op": "update", "key": "...", "content": "..."}` (the `key` from its `save`/`recall` result) to replace it in place — never pile up duplicates. `update` re-sends the WHOLE fact, not a diff: pass every field you want kept, not just the one that changed. Unsure whether it exists: `{"op": "recall", "query": "deploy conventions"}` first.
