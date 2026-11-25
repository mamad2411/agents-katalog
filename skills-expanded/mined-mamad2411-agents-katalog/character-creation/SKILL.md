---
name: character-creation
description: Use when creating a new pinu-bot character or doing a major character redesign. Covers neutral-first design, shared API mapping, emotion-family construction, visual harness review, and finish criteria for cross-state cohesion. Do not use for small one-off expression tweaks.
---

# Character Creation

Use this skill for new built-in characters and major character passes.

Read [`docs/character-creation.md`](../../../docs/character-creation.md) first.
Then use:

- [`docs/character-brief-template.md`](../../../docs/character-brief-template.md) before implementation
- [`docs/construction-api.md`](../../../docs/construction-api.md) when repeated character work is failing at the composition level

## Use This Skill When

- adding a new character
- doing a broad visual refactor of an existing character
- making a character respond properly to the shared API
- trying to resolve cross-state cohesion problems

## Do Not Use This Skill When

- making a small expression tweak
- adjusting one line weight or one facial detail
- fixing an isolated bug unrelated to overall character construction

## Workflow

1. Read `docs/character-creation.md`.
2. Fill out `docs/character-brief-template.md` before coding.
3. Inspect the current character surfaces that may need changes:
   - `src/character.ts`
   - `src/robotFace.ts`
   - `src/characters/*.ts`
   - `demo/index.html`
   - `test/visual.html`
   - `test/visual.spec.ts`
   - `README.md` if public behavior changes
4. Lock the character identity and neutral face before tuning emotions.
5. Lock the whole face composition before polishing individual parts:
   - dominant silhouette
   - centerline relationships
   - which 2-3 forms carry the character
   - what is structure vs decoration
6. Decide how the character maps the shared API:
   - `eyeShape`
   - `noseShape`
   - `mouthShape`
   - `browShape`
   - feature toggles
   - face themes
   - built-in emotion names
7. Treat the design as a display-symbol system, not an illustration:
   - keep the face robotic unless the brief explicitly calls for something else
   - abstract real-world references before drawing them
   - do not let brows, ears, muzzle pieces, or mask shapes become unrelated stickers
8. Build emotion families instead of isolated one-off states.
9. Use `test/visual.html` during the pass, not only at the end.
10. Verify `speak()` and other motion controls explicitly.
11. If local-part iteration keeps drifting, step back and use the construction-API proposal in `docs/construction-api.md` as the design frame instead of continuing to patch shape fragments.
12. Run:
   - `./scripts/check.sh`
   - `./node_modules/.bin/playwright test` if visuals changed

## Rules

- Neutral must read strongly on its own.
- The whole face must work as one composition before any single part is considered “good”.
- A character should still look like the same character in every core state.
- Shared API controls should behave coherently across characters.
- Do not use special-case charm details to hide unresolved structure.
- Do not solve a character as an animal illustration when the product needs a robot display face.
- If a shared control behaves differently for the character, translate it intentionally rather than accidentally ignoring it.

## Deliverables

- character implementation
- any shared helper changes needed to support it cleanly
- demo/docs alignment if public behavior changed
- updated visual snapshots only when rendering legitimately changed
