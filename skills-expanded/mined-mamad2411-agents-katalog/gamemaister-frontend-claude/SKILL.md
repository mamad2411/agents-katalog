# gamemAIster Frontend

React 19 + TypeScript + MUI v7 + Vite frontend for a multi-TTRPG-system AI gamemaster app. State via Zustand stores (`src/stores/`), theming via MUI `createTheme()` per game system.

**Sibling repo:** `../gamemAIster-backend` (Python/FastAPI) has its own `CLAUDE.md` — read it too when a task touches both repos (very common: character-sheet/NPC field changes always span both). See "Character schema contract" below for the load-bearing detail of that relationship.

## Supported game systems

Shadowrun (5E/6E), Vampire: The Masquerade (5E), Call of Cthulhu (7E), Seventh Sea (2E), The Expanse (AGE system), Dragonlance: Shadow of the Dragon Queen (D&D 5E), a free-form Custom RPG, and **Slavic** — a homebrew "Baltic Slavic 800 A.D." setting built on **Forbidden Lands** (Free League Publishing, Year Zero Engine) rules: 4 attributes that double as health pools, damage applied directly to the governing attribute (no separate HP pool), "Broken" at 0. See the comment block above `SlavicCharacter` in `src/models/CharacterProps.tsx` for the mechanical detail.

## Character schema contract (frontend is the source of truth)

The `*Character` interfaces in `src/models/CharacterProps.tsx` are the canonical shape for both player character sheets and NPCs — not the backend. `npm run gen:npc-schemas` (`scripts/generate-npc-schemas.mjs`) generates JSON Schemas from these TS interfaces and writes them into `../gamemAIster-backend/tests/schemas/`. The backend's `tests/test_npc_schema_contract.py` validates that its NPC-generation pipeline (`merge_npc()` in `src/brain/npc_models.py`) produces output conforming to those schemas.

**Practical implication:** if you add/change a field on any `*Character` interface (e.g. adding an `armor` field), the workflow is: edit `CharacterProps.tsx` → run `npm run gen:npc-schemas` from this repo → switch to the backend repo and update its NPC stats/equipment Pydantic models, merge functions, and prompt templates to match → run `tests/test_npc_schema_contract.py` there to confirm. Don't hand-edit the JSON files under `gamemAIster-backend/tests/schemas/` — they're generated output and will just be overwritten/drift from the real contract.

## Commands

- `npm run dev` — Vite dev server (port 5173, configured in `.claude/launch.json` as `gamemaister-frontend` for `preview_start`)
- `npm run build` — `tsc && vite build` (typecheck is part of the build)
- `npx tsc --noEmit -p .` — typecheck only, fast sanity check after edits
- `npm run lint` — ESLint, `--max-warnings 0`
- `npm run gen:npc-schemas` — regenerate NPC JSON schemas after editing `CharacterProps.tsx`

## Theme architecture

Each supported TTRPG system has its own MUI theme in `src/themes/<system>.ts`, registered in the `themeMap` in `src/theme.ts`. Shared helpers live in `src/themes/helper.ts`:

- `getSafePaletteColor(theme, ownerStateColor)` — resolves a palette color key (`"primary"`, `"secondary"`, etc., or `"textPrimary"`/`"textSecondary"`/`"inherit"`) to an actual color string, with a sensible fallback.
- Custom `Theme`/`ThemeOptions` properties declared via module augmentation: `spinButtonBackgroundImage`, `scrollbarStyles`, `logo`, `trackColors`, `titleOverlayStyle` (optional), `accentColor` (optional).
- `accentColor` is the "active state" accent for a theme (e.g. Shadowrun's cyan `#00e5ff`) — used by anything that needs to fully replace a base/instance color on focus/active/selected state (loading-modal border, input focus rings) rather than layering a second color on top of the first. Falls back to the base color when unset, so themes without a dedicated accent are unaffected. See `styles.tsx`'s `trackInputStyle`/`textfieldStyle` and `FieldContainer.tsx`'s MAIN_SEND `TextField` for the pattern: `theme.accentColor ?? <instance-base-color>`.
- New systems: add `src/themes/<name>.ts` exporting a `createTheme()` object, add it to `themeMap` in `theme.ts`, and add any new Google Fonts to the `<link>` tags in `index.html` (a theme referencing a font that isn't loaded there silently falls back to the browser default — this caused a real, hard-to-notice bug across four themes before).
- Per-instance colored text/glow: when a component sets a literal/dynamic non-palette color via `sx` (e.g. `NpcCard.tsx`'s damage-track color, computed by `getTrackColor`), any theme-level "auto-glow" text-shadow (keyed off the MUI `color` prop, not `sx`) will NOT match it automatically — add a matching `textShadow` directly in that component's `sx`, derived from the same color value.

## CSS specificity gotcha (recurring)

Several inputs across the app set their focus-border color twice: once via a per-instance `sx` override (its own base color) and once via a theme-level `MuiOutlinedInput`/`MuiInputBase` global override (the active accent). When both rules end up with **equal class-selector specificity**, the winner is decided by source order, which is fragile and was observed to pick the wrong one in practice. Prefer compound selectors like `"& .MuiOutlinedInput-root.Mui-focused"` (classes on one node) over spreading `.Mui-focused` and the target class across separate descendant levels — count actual class-selector totals on both sides before assuming a fix works.

## Verification workflow — read this before testing UI changes

The project has no backend running by default in this environment (`http://192.168.0.109:8000` is unreachable), so:

- Login still works (any username "demo" + click "Demo Login").
- Most mission/character creation flows that call the backend will fail/hang. Patch `window.fetch` to hang (`window.fetch = () => new Promise(()=>{})`) to inspect a loading state without it erroring out from under you, or directly poke the relevant Zustand store via dynamic import in `preview_eval` (e.g. `(await import("/src/stores/historyStore.tsx")).default.getState().performOptimisticUpdate(...)`) to populate state without the backend.
- `characterStore` and others persist to `localStorage`, so test data survives reloads — clean up additions you don't want kept around, or expect them on the next session.

**Do your own UI verification for every visual/styling change** using the preview tools (`preview_start`, `preview_eval`, `preview_inspect`, computed-style checks) before reporting something as done — don't ask the user to check basic things you can check yourself.

**But escalate instead of rabbit-holing.** If a live check gives a result that contradicts your code-level reasoning (CSS specificity math, a confirmed-correct generated rule, etc.) and a _second_, differently-constructed check doesn't resolve the contradiction — stop. This environment has known flakiness (`document.hasFocus()` dropping mid-session, `getComputedStyle`/stylesheet-disable not reflecting synchronously, `preview_screenshot` and `requestAnimationFrame`-based waits timing out in the background tab). Don't keep spending turns trying new probing techniques on the same question. Instead:

1. State plainly what you verified with confidence (code review, generated CSS rules, isolated reproductions) and what you couldn't confirm live, and why (name the specific flaky symptom you hit).
2. Give the user a concrete manual test: what to click/do, and what a passing ("green") result looks like — specific enough that they don't have to guess (e.g. "open the NPC accordion, click into the damage number input — the outline should turn solid cyan with no trace of the orange/green damage color mixed in").

Don't burn further tool calls re-litigating the same already-contradicted check.
