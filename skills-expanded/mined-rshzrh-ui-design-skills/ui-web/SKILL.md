---
name: ui-web
description: Generate slop-free UI for React + Tailwind + shadcn/ui. Use whenever the user asks to build, design, scaffold, restyle, or improve a screen, component, page, landing, app, or any web interface. Replaces frontend-design, design-html, design-shotgun, design-consultation. Two phases — tokens first (with approval gate), then UI — both gated by a self-audit checklist that the model MUST run before claiming done.
---

# ui-web — Slop-Free Web UI Skill

You are generating production-grade web UI in React + TypeScript + Tailwind. This skill exists because untouched LLMs produce **AI slop**: purple→blue gradients, Inter everywhere, 3-icon-card grids, "Lightning fast / Powered by AI" copy, glassmorphism by default, arbitrary spacing values, and the median of every Tailwind tutorial scraped from GitHub. This skill replaces guesses with **constraints**.

The non-negotiable rule: **NEVER use a buzzword in place of a token.** Words like *clean*, *modern*, *professional*, *sleek*, *premium* are banned from your reasoning. Every aesthetic choice must trace back to a named anchor recipe in `anchors.md` and a token in the project's `tailwind.config.ts`.

---

## Workflow (follow in order)

### Step 0 — Project scan (decides bootstrap vs extend mode)

Before any other action, check for:

```
DESIGN_RULES.md            # at repo root → if exists, you are in EXTEND mode
tailwind.config.{ts,js}    # → if exists with custom theme, you are in EXTEND mode
app/globals.css            # check for CSS custom properties / tokens
src/styles/tokens.css
```

- **If `DESIGN_RULES.md` exists**: read it. Read the existing `tailwind.config.*`. Skip to **Step 3 (Phase 2: UI)**. Use only existing tokens. NEVER add new colors/spacing/radii without asking.
- **If tokens exist but no `DESIGN_RULES.md`**: read tokens, infer the closest matching anchor, ask the user to confirm the inferred anchor, then write `DESIGN_RULES.md` and proceed to Phase 2.
- **If neither exists**: you are in **bootstrap mode**. Continue to Step 1.

### Step 1 — Intake (interactive, bootstrap only)

Use AskUserQuestion to gather, in this order:

1. **Anchor pick** — show the 8 recipes from `anchors.md` (one-line summary each). Let the user pick 1–3. If 2–3, ask which is primary and which contributes type vs color vs motion.
2. **Ban menu** — show the 8 ban patterns from `ban-patterns.md` with the 3 default-on items pre-checked. Confirm.
3. **Project context**:
   - Content density: airy / balanced / dense
   - Primary surface: marketing site / app / docs / dashboard / mobile-web
   - Dark mode: required / optional / none
   - Brand color (if any): hex value or "derive from anchor"

Do NOT ask vibe questions ("how should it feel?"). Ask only the questions above.

### Step 2 — Phase 1: tokens (gated)

Generate, in this order:

1. **`tailwind.config.ts`** — extend `theme` using the chosen anchor's recipe. Use the template at `templates/tailwind.config.ts.tmpl`. Required keys: `colors`, `spacing`, `borderRadius`, `fontSize`, `fontFamily`, `boxShadow`, `transitionDuration`, `transitionTimingFunction`.
2. **`app/globals.css`** (or `src/index.css` for Vite) — CSS custom properties mirroring the Tailwind tokens, plus dark-mode overrides if requested.
3. **`eslint.config.js` patch** — enable the slop-blocking lint rules from `templates/eslint.slop.cjs.tmpl`. Add a `lint:design` script to `package.json`.
4. **`DESIGN_RULES.md`** at repo root — fill `templates/DESIGN_RULES.md.tmpl` with the chosen anchors, active bans, token file paths, and verification command.
5. **`CLAUDE.md` patch** — append (do not overwrite): `Before any UI/UX work, read and follow DESIGN_RULES.md.`

Then **run the Token Audit** from `verification.md` and print the PASS/FAIL table to the user. **Do not proceed to Phase 2 until the user approves.**

### Step 3 — Phase 2: UI

Generate the requested screen/component using **only tokens from the config**. Follow:

- **`component-anatomy.md`** — exact rules for button, input, card, list, nav, modal, toast, empty-state, form-field, table-row.
- **`motion.md`** — easing curves and durations.
- **`copy-voice.md`** — every string is real, contextual copy. No lorem ipsum, no filler.
- **`icons-imagery.md`** — icon library, sizing, alignment. No emoji bullets in serious UI.

Then **run the UI Audit** from `verification.md` AND `pnpm lint:design` (or `npm`/`yarn` equivalent). Print the audit table. Fix every FAIL before claiming done.

---

## Files in this skill

| File | When to read |
|---|---|
| `anchors.md` | Step 1, before showing the user choices. ALWAYS read fully — never quote from memory. |
| `ban-patterns.md` | Step 1, when showing ban menu. Step 2 and 3, when verifying. |
| `component-anatomy.md` | Step 3, before writing any component. |
| `motion.md` | Step 3, when adding any transition or animation. |
| `copy-voice.md` | Step 3, before writing any user-facing string. |
| `icons-imagery.md` | Step 3, when choosing icons or images. |
| `verification.md` | After Step 2 (Token Audit) and after Step 3 (UI Audit). MANDATORY — do not skip. |
| `templates/*` | Use as the basis for the generated files; fill placeholders, never ship as-is. |

## Hard rules (the model must obey these always)

1. **No arbitrary values.** Forbidden: `mt-[13px]`, `w-[372px]`, `text-[#3a4f6b]`, `rounded-[7px]`. Every value must be a token in `tailwind.config.ts`. If you need a value that does not exist, ask the user to add it to the token set.
2. **No buzzwords in code or comments.** Banned strings in your output: *clean*, *modern*, *professional*, *sleek*, *premium*, *beautiful*, *elegant* (except in copy if the user explicitly asked for those words).
3. **No default-style-tells unless the chosen anchor explicitly allows them.** Specifically: no `bg-gradient-to-r from-purple-* to-pink-*`, no `from-indigo-* to-purple-*`, no `backdrop-blur` on regular cards (only on iOS-style chrome/sheets if anchor allows).
4. **No filler copy.** No lorem ipsum. No "Lightning fast", "Built for the modern web", "Powered by AI", "Get started in seconds", "The future of X", "Beautiful and intuitive".
5. **Touch targets ≥ 44px** on any control intended for tap.
6. **Focus rings always visible.** Never `focus:outline-none` without an explicit replacement.
7. **Every async surface has empty + loading + error states.** No exceptions.
8. **Dark mode parity.** If the project supports dark mode, every component you write must work in both — verify by reading the colors you used.
9. **You must run the verification checklist** before responding "done". Print the audit table to the user.

## What this skill is NOT

- Not a magic-aesthetic generator. You still have to pick an anchor and follow it.
- Not a copy generator. Phase 2 stops and asks for real copy when needed.
- Not a brand-design tool. Brand identity (logo, custom typography family selection beyond what anchors provide) is the user's call.
- Not a replacement for design review with humans. The audit table is a floor, not a ceiling.
