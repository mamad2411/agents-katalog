---
name: squad-intake
description: Run a structured intake interview with the user — open a session, ask one focused question per turn, draft the bundle, confirm with the user, then commit. Supports green-field (mode=new) and refine-mode (mode=refine) flows.
argument-hint: "<optional starting idea or item id to refine>"
allowed-tools:
  - mcp__squad__squad_intake_open
  - mcp__squad__squad_intake_turn
  - mcp__squad__squad_intake_status
  - mcp__squad__squad_intake_commit
disable-model-invocation: true
---

You are running an intake interview with the user. The goal: turn a vague idea (or a captured stub item) into a well-shaped bundle that's ready to commit. The user said:

```
$ARGS
```

## Step 1 — Decide the mode

- If `$ARGS` contains an item id like `FEAT-007` or `BUG-014`, this is **refine mode**: the user wants to flesh out an existing captured stub.
- Otherwise it's **new mode**: green-field, the user has an idea but no item yet.

## Step 2 — Open the session

Call `squad_intake_open`:

- New mode: `{"mode":"new","idea_seed":"<short summary of $ARGS>"}`
- Refine mode: `{"mode":"refine","refine_item_id":"<the id>"}`

Capture the `session_id` from the result. If `resumed:true`, the user already had an open session — pick up where it left off (call `squad_intake_status` to read the prior transcript).

For refine mode, the `snapshot` field carries the original item's title / area / body so you can show the user what's there before asking what changes.

## Step 3 — Loop: ask, record, check

Repeat until `still_required` is empty:

1. **Ask one focused question.** Pick the next required field from the most recent `still_required` (or the default checklist fields if you haven't recorded a turn yet). Don't dump the whole checklist on the user — one question at a time, in priority order.
2. **Wait for the user's reply.**
3. **Record the turn.** Call `squad_intake_turn` with `role:"user"`, `content:"<the user's reply>"`, and `fields_filled:["<dotted field name>", ...]` listing the checklist fields this turn satisfied. Be honest — squad does NOT natural-language-parse the content; the structural validator runs at commit time and will reject incomplete bundles loudly.
4. **Read the new `still_required`.** Loop until empty.

If the user goes off-topic or asks a clarifying question, reply naturally — but only call `squad_intake_turn` when you have user content that fills a field.

## Step 4 — Draft the bundle

When `still_required` is empty, you have enough material to draft. Build a `bundle` object:

- **Item-only shape** (most green-field interviews): `{"items":[{"title":"...","intent":"...","acceptance":["..."],"area":"...","kind":"feat|bug|task|chore|debt|bet"}]}`
- **Spec/epic/items shape** (large initiatives that decompose): add a `spec:{...}` object and an `epics:[{...}]` array, then make sure every `items[i].epic` references an `epics[j].title`. The structural validator requires every item map to a real epic and every epic have ≥1 item.
- **Refine mode** is always exactly one item, no spec, no epics. The validator enforces this.

## Step 5 — Confirm with the user

Show the user a compact summary of the draft (titles, areas, item count) and ask:

> *"Ship it? (y/n/edit)"*

- **y** → step 6.
- **edit** → loop back to step 3 with the user's edits as new turns.
- **n** → tell the user the session stays open; they can resume later by re-running `/squad-intake`. If they want to abandon outright, they run `squad intake cancel <session-id>` themselves in a terminal — there is no `squad_intake_cancel` MCP tool by design, since squad does not give Claude a way to throw user work away.

## Step 6 — Commit

Call `squad_intake_commit` with `{"session_id":"<id>","bundle":{...},"ready":false}`. Default `ready:false` lands the item(s) in the inbox (status=captured) for triage. Pass `ready:true` only if the user explicitly says they want immediate-claimable items.

Report the result: item ids, file paths, and the next step (run `squad inbox` to triage, or `squad accept <ID>` to make a captured item ready).

## Error handling

The MCP tools surface typed errors:

- `not-found` — the session id is unknown. Probably stale; restart with `squad_intake_open`.
- `invalid-request` — wrong agent or session already closed. If closed, the user's previous session committed/cancelled successfully; tell them so.
- `invalid-params` — the bundle is structurally incomplete. The error message names the missing field; loop back to step 3 and ask for it.
- `conflict` — a spec or epic slug already exists. Ask the user to pick a different title.
