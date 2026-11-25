---
name: game-asset-prompt
description: Generate ready-to-paste AI image-gen prompts for 2D game art (character/sprite, icon/UI/item, background/tileset) that stay consistent with the project's art style across separate chat sessions in Claude/Gemini/ChatGPT chat UIs. Use when the user wants to render, generate, or create game art/sprites/icons/backgrounds with AI, or mentions an "art style bible" for a game project. Maintains a persistent `art-style-bible.md` so style doesn't drift between requests, and gives a post-generation checklist plus post-processing guidance for common technical misses (transparency, size, aspect ratio).
user-invocable: true
---

# game-asset-prompt

Produces one ready-to-copy-paste image-gen prompt per asset request, anchored to a persistent per-project style bible, so a solo dev needs 1-2 tries instead of many. This skill never calls an image-gen API and never executes image processing — it only produces prompt text and instructions; the user pastes the prompt into their own chat tool and does post-processing by hand.

## Step 1 — Bible Check

Check whether `art-style-bible.md` exists at the project root.

- **Missing** → run the bootstrap Q&A in `references/bible-bootstrap-questions.md` (≤6 questions, validate none are skipped), write `art-style-bible.md` using that file's exact template, then continue to Step 2.
- **Present** → read it. Its fields are the source of truth for every prompt this skill generates — never restate style from memory, always read the current file.

## Step 2 — Asset Type

Ask which asset type is being generated, if not already stated: **character/sprite**, **icon/UI/item**, or **background/tileset**.

Load the matching template and follow its own steps to gather asset-specific input and produce the prompt:

- Character/sprite → `references/character-sprite-template.md`
- Icon/UI/item → `references/icon-ui-item-template.md`
- Background/tileset → `references/background-tileset-template.md`

Every placeholder token in these templates matches `references/bible-field-names.md` — substitute from the bible fields read in Step 1, never invent new field names.

**Reference image (if present)**: if the bible's `[REFERENCE_IMAGE_PATH]` isn't "none", or the user has an image for this specific asset, tell them to attach it directly in the chat alongside the generated prompt rather than describing it in words — a real image is a stronger consistency signal than any text description.

## Step 3 — Bible Drift Check (P2)

Before generating the prompt, compare the asset's requested style/palette against the bible:

- Warn (via `AskUserQuestion`) only when **both** hold: (a) the requested palette shares zero hex codes with `[PALETTE_HEX]`, AND (b) the requested art direction doesn't match `[ART_DIRECTION]` verbatim or as a clear synonym.
- If only one condition holds, treat it as normal variance — don't warn.
- On warning, offer to proceed as a one-off exception or update the bible.

## Step 4 — Output

After the prompt, always emit, in order:

1. The prompt itself, in a copy-pasteable code block.
2. A suggested filename: `{type}_{name}_{variant}_{frame}.png`, where `{type}` is `char`/`icon`/`bg` matching the asset type from Step 2, `{name}` is the asset's given name, and `{variant}`/`{frame}` are omitted when not applicable (e.g. a single non-animated icon has no frame suffix).
3. The post-generation checklist from `references/post-generation-checklist.md`.

If the user reports a technical miss (wrong size, not transparent, wrong aspect) after pasting the result into their chat tool, use `references/post-processing-guide.md` — don't regenerate the whole prompt from scratch; follow its two-turn fallback guidance first.

## Success criteria

A generated prompt is correct when: it contains the bible's style anchor phrase verbatim, states the correct technical spec (size/background/view) for the chosen asset type, includes negative constraints, and uses no tool-specific syntax (no Midjourney `--ar`, no Stable Diffusion `(weight)`) — so it works unchanged in Claude, Gemini, or ChatGPT chat.
