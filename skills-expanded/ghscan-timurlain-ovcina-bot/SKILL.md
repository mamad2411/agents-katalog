---
name: baca-user
description: >
  Create tasks in Bača (the Ovčina organizers' task tracker) via API.
  Use this skill whenever the user asks to "remember to do X", "add a task",
  "note this for later", "we'll need to handle Y", "remind me to Z",
  "this is a TODO", or whenever you the agent realize during conversation
  that something concrete needs to be done by an organizer (printing,
  buying materials, contacting someone, preparing props, rule decisions).
  Also trigger when generating content that produces follow-up work —
  e.g. after creating a new creature, suggest adding a task to print its
  card; after a rule change, suggest a task to update the rulebook.
  This skill posts directly to baca.ovcina.cz/api/tasks using a static
  API key — no login required, no human in the loop.
---

# Bača Task Creation Skill

## What is Bača?

Bača (`baca.ovcina.cz`) is the Ovčina LARP organizers' task management web
app. It tracks all the practical work needed to run the games: printing
cards, buying materials, contacting players, preparing props, fixing rules,
etc. Tasks have status (Idea/Open/InProgress/ForReview/Done), priority,
category, assignee, comments, images, and direct shareable URLs.

Skills that produce structured content (lore, rules, economy, character
sheets) often surface follow-up tasks. This skill lets you write those
tasks straight into Bača so nothing gets lost.

## When to use

Trigger this skill whenever the conversation produces a concrete actionable
item that needs human follow-up. Examples:

- After generating a new creature card → "task: print 5 copies on cardstock"
- After designing a quest → "task: prepare props (parchment, candle, key)"
- After a rule clarification → "task: update rulebook section X"
- After lore work → "task: add new NPC to character database"
- User says "we should remember to do X" → just do it
- User says "add this to baca" / "note this" / "remind me" → just do it

**Do NOT use this skill for:**
- Discussion-level brainstorming ("we could maybe...")
- Questions about existing tasks (no read API exposed yet)
- Bulk imports (use the web UI instead)

## How to call the API

**Endpoint:** `POST https://baca.ovcina.cz/api/tasks`

**Headers:**
```
X-Api-Key: kl3F0jpJwC2cKbHPsYzOw77fC9IDqH679S8O85BqorA
Content-Type: application/json
```

**Request body** (only `title` is required):
```json
{
  "title": "Vyrobit nové stashe pro Daona",
  "description": "Tři kusy podle promptu z brain/daon-grimburgoth.md. MJ artist: Vess.",
  "priority": "Medium",
  "source": "loremaster",
  "dueDate": "2026-04-20T00:00:00Z"
}
```

**Field reference:**
| Field | Type | Notes |
|---|---|---|
| `title` | string | **Required.** Short, action-oriented. Czech preferred. |
| `description` | string? | Long context, references to docs, MJ prompts, etc. |
| `priority` | `"Low" \| "Medium" \| "High"` | Default `Medium`. Use `High` only for blockers. |
| `categoryId` | int? | Skip unless you fetched the categories first |
| `dueDate` | ISO 8601 UTC | Optional |
| `source` | string | **Always set this.** Identifies your skill (e.g. `"loremaster"`, `"rulemaster"`, `"economymaster"`) |
| `assigneeId` | int? | Don't set — let organizers self-assign |

**Response (201 Created):** Full TaskDto with `id`. Compute the URL as:
```
https://baca.ovcina.cz/tasks/{id}
```

**On error:**
- `400` — bad request (missing title, invalid JSON)
- `403` — wrong API key
- `5xx` — Bača is down, retry once after 30s, then give up gracefully

## Confirmation message

After successfully creating a task, **always tell the user**:

> ✅ Úkol #42 přidán do Bači — https://baca.ovcina.cz/tasks/42

Format: `✅ Úkol #{id} přidán do Bači — {url}`

If multiple tasks created in one go, list them all with the same format.

## Title-writing rules

- **Action verb first**: "Vytisknout karty", "Koupit folie", "Připravit prop"
- **Czech**, lowercase except proper nouns
- **Specific**: not "Karty", but "Vytisknout 40 karet creaturelingů"
- **Under 100 chars** — long context goes in `description`
- **No project codes or jargon** — organizers are not all developers

## Examples

### Example 1: After creating a creature

User: "Create a new creature called Mlhoběs for the dark forest"

After generating the creature lore + MJ prompt, also create a task:

```bash
curl -X POST https://baca.ovcina.cz/api/tasks \
  -H "X-Api-Key: kl3F0jpJwC2cKbHPsYzOw77fC9IDqH679S8O85BqorA" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Vygenerovat MJ obrázek pro Mlhoběse",
    "description": "Prompt v brain/creatures/mlhobes.md. Použít artist rotation: Vess. Po vygenerování přidat do creature deck.",
    "priority": "Medium",
    "source": "loremaster"
  }'
```

Then tell user: "✅ Úkol #57 přidán do Bači — https://baca.ovcina.cz/tasks/57"

### Example 2: After a rule decision

User asks about a rule edge case, you propose a fix:

```bash
curl -X POST https://baca.ovcina.cz/api/tasks \
  -H "X-Api-Key: ..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aktualizovat pravidla — sekce \"Boj s creaturelingem\"",
    "description": "Přidat upřesnění o tom, co se stane, když creatureling útočí na hráče v transformaci. Viz diskuse 2026-04-13.",
    "priority": "High",
    "source": "rulemaster"
  }'
```

### Example 3: User explicitly asks

User: "Add a task to buy laminating sheets"

```bash
curl -X POST https://baca.ovcina.cz/api/tasks \
  -H "X-Api-Key: ..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Koupit laminovací folie",
    "source": "user-request"
  }'
```

## Don't do these

- ❌ Don't create tasks during pure brainstorming — wait for concrete decisions
- ❌ Don't create duplicate tasks — if the user is iterating on the same idea, update the description in your head, then create one task at the end
- ❌ Don't set `assigneeId` — let humans self-assign
- ❌ Don't expose the API key in chat — it's static, treat it like a secret
- ❌ Don't promise the task is "done" — you're just adding it to the queue
- ❌ Don't use the API for reading/listing tasks — there's no machine-friendly read endpoint yet

## API key rotation

If the key stops working (403 errors), the user needs to rotate it via:
```bash
az containerapp update --name baca-api --resource-group ovcina \
  --set-env-vars "ApiKey__Secret=<new-value>"
```
Then update this skill file with the new key.
