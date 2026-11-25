---
name: mage-character-builder
description: |
  Design a new AI character from a list of traits with Mage and save it for
  reuse: gender, ethnicity, hair, skin, body, eyes, face, features, age, and
  clothing become a full-body portrait, then a character with an @handle. The
  Character Builder: Attributes app as a skill, on Mango 4 by default. Use when:
  "build a character", "create a character from scratch", "character creator",
  "design a person: red hair, green eyes, freckles", "make me an AI
  influencer", "I need a model with these traits", "generate a character I can
  reuse". NOT for: saving an existing photo as a character (mage-characters),
  exploring a look from a starter image (mage-character-muse), a turnaround
  sheet (mage-character-sheet), or recreating a real person.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Character Builder

Build a character from a checklist of traits, generate a full-body portrait, adjust until it is right, then save it with an `@handle`. This is the [Character Builder: Attributes app](https://www.mage.space/apps/character-builder-attributes) as a skill: the same attributes, prompt and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, and `create_character`. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **No input image.** The character comes from the attributes alone.
3. **Fictional people only.** Don't use this to approximate a real person.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always state the model and the price in Gems. A single image can start with its price in the same message; a batch waits for a yes.
4. Generating costs Gems; saving the character is free.
5. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

Read `references/attributes.md` for the fourteen attributes and their exact prompt words.

1. Take every attribute the request gives. **Gender is required**; ask for it if it is missing.
2. Don't ask about the rest one by one. With the price, say in one line which attributes are still open and that the model chooses them, and generate without waiting. If you had to ask for gender, list the open attributes in that same question.

## Build the prompt

With at least one attribute besides gender:

```
A full-body standing portrait shot of a <gender> with <attribute words, joined with ", ">. High quality, detailed, studio lighting, wide shot.
```

With gender only:

```
A full-body standing portrait shot of a <gender>. High quality, detailed, studio lighting, wide shot.
```

`<gender>` is `female` or `male`. The other words come from `references/attributes.md`, in its order. Nothing else goes in the prompt.

## Settings

- Model: Mango 4 (`mango`, `model_id: "mango-v4"`) at `resolution: "1K"`, the app's default. Other models the app offers: `references/models.md`.
- `aspect_ratio`: always `4:5`.
- No `image`.

## Run

```json
{
  "model_id": "mango-v4",
  "resolution": "1K",
  "aspect_ratio": "4:5",
  "prompt": "<the built prompt>"
}
```

1. `get_model` for the architecture, once per conversation, to confirm its fields and options.
2. `estimate_cost` with the exact config. Say the model and the price in Gems. One image can start in the same message; more than one waits for a yes.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120` until the status is `completed`, `failed`, or `cancelled`.

## Adjust

Show the portrait. To change a trait, change that attribute and generate again with the full prompt; every run is a new person, so the face changes too. When the user likes a face and wants to change only details, move to `mage-character-muse` with that image as the starter.

## Save

When the user approves a portrait, offer to save it:

1. Ask for a name. The handle is derived from it unless the user picks one (1–15 lowercase letters, digits, `_` or `-`, starting with a letter; it can't change later).
2. `create_character` with `name`, `image` (the result's URL), and the optional `handle`.
3. Reply "Saved @handle. Mention @handle in any prompt to use them."

Then `mage-character-sheet` can turn the portrait into a full reference sheet.

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's policy or the model's filter refused it. Never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |
| `handle_taken` | Suggest another handle, or leave it out to derive one. |

## References

- `references/attributes.md`: the attributes, their exact prompt words, and the rules for combining them.
- `references/models.md`: every model the app offers for this, with ids and resolutions.
