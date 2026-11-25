---
name: park
description: Fast guilt-free shelving of vault items you're not doing right now. Preserves context and sets an optional reminder date. Works for dev items, business tasks, personal errands, learning goals — anything in the vault. Use when the user says "park this", "not now", "shelve it", "put it aside", "I'll do this later", or invokes /park. Designed for ADHD minds that need permission to let things go without losing them.
---

# Park

Shelve a vault item with a reminder. No guilt, no loss — it stays where it is with a comeback date.

## Vault Path

`{{VAULT_PATH}}`

## Step 1: Identify the Item

If the user names the item or describes it, search for it:

```
mcp__vault-index__search_vault(query="{user's description}")
```

If multiple matches, show them numbered and ask which one.

If the user says "park this" with no description, check if there is a currently active task context (from the conversation or from `/tmp/claude-vault-context-${SESSION_ID}`). Park that item.

If nothing can be identified, ask: "What do you want to park?"

## Step 2: Ask for Reminder (optional)

Ask: **"When should I remind you? (default: 7 days, or say 'never')"**

Accept natural language:
- "tomorrow" → 1 day
- "next week" → 7 days
- "next month" → 30 days
- "2 weeks" → 14 days
- "never" → no reminder
- Specific date → use that date
- No answer / "whatever" / "sure" → 7 days

Calculate the `remind_after` ISO 8601 date from today.

## Step 3: Update the Vault Item

Read the item file. Update its frontmatter:

1. Add `parked` to the `tags` list (create the field if it doesn't exist)
2. Add `parked_at: {current ISO 8601 timestamp}`
3. Add `remind_after: {calculated ISO 8601 date}` (omit if "never")
4. Set `status: open` (release from any in-progress/claimed state)
5. Update `updated: {current ISO 8601 timestamp}`

If the item has an active claim, release it:
```
mcp__vault-index__release_item(item_id="{item_id}")
```

## Step 4: Keep Item In-Place

**Do NOT move the item.** It stays in its current folder so it remains categorized:
- Dev bugs stay in `01-Bugs/`
- Personal items stay in `07-Personal/`
- Business items stay in `06-Business/`
- etc.

The `parked` tag is how the morning briefing and vault-status find parked items across all folders.

**Exception**: If the item is in `04-In-Progress/`, move it back to its original queue folder (based on `domain` and `type` in frontmatter). If the original folder can't be determined, move to `03-Ideas/`.

## Step 5: Re-index

```
mcp__vault-index__index_vault(incremental=true)
```

## Step 6: Confirm

Single line confirmation:

```
Parked: "{item title}" — reminder set for {remind_after date}.
It's staying in {current folder}. I'll bring it up in your morning briefing when the reminder hits.
```

If "never" was chosen:
```
Parked: "{item title}" — no reminder set.
It's in {current folder} whenever you want it. Use /vault-status to see all parked items.
```
