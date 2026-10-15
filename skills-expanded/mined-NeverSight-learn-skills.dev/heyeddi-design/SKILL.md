---
name: heyeddi-design
description: End-to-end UI design for HeyEddi stack (PrimeVue, DESIGN.md, semantic tokens — OpenProps on scaffold default). Use when the user wants to design, explore, critique, or improve existing frontend — e.g. "enterprise view", "critique the login page", "this UI looks bad", "settings page". Runs discovery, critique, polish, craft, document. Sub-commands init, discover, shape, craft, critique, polish, document. Not for pre-made screenshot handoff — use design-handoff instead.
version: 2.1.0
---

Designs and builds production UI within PrimeVue, project `DESIGN.md`, and semantic CSS tokens. **OpenProps is the HeyEddi scaffold default but not mandatory** — detect token source per `reference/token-strategy.md`.

**You do not need design vocabulary from the user.** Plain intent ("enterprise view for our app") is enough — ask questions until direction is clear.

## Subagents (default)

**Delegate by sub-command** — see `reference/subagents.md`. Main chat confirms briefs and merges results.

| Always delegate | Subagent |
|-----------------|----------|
| `@visual-auditor` / Playwright | `shell` |
| `validate_vue`, npm test, build | `shell` |
| `critique`, `craft`, `polish` (route work) | `generalPurpose` |
| `research`, wireframe `explore` | `generalPurpose` |
| Codebase scan for `document` | `explore` |

Do not run visual capture inline during craft/handoff turns.

## Setup (every session)

1. Run `python scripts/load_context.py --project-root <root>` once per session (skip if output is already in the conversation).
2. If `product_exists` is false and the task needs strategic context, run **`init`** before shape/craft.
3. Read the sub-command reference file for the invoked mode (required — do not skip).
3a. Read `reference/surface-completeness.md` once per session when shaping, crafting, or critiquing any route — design full surfaces, not happy-path minimums.
3b. Read `reference/foundations.md` once per session — responsive, theme, i18n, a11y, reading modes are **always on** unless `product.md` waives them.
3c. Read `reference/token-strategy.md` when styling — detect OpenProps vs custom tokens before writing CSS.
3d. Read `reference/modern-reference.md` when shaping or crafting **marketing, dashboard, or settings** routes — avoid plain admin-template output.
3e. Read `reference/audience-design.md` when shaping, crafting, or polishing **any user-facing route** — tie direction to `product.md` personas.
3f. Read `reference/design-ambition.md` when shaping, crafting, or polishing **flagship routes** — project-specific signature and impressive craft bar (default; do not wait for user to ask).
4. After **craft**, **polish**, **critique** (when leading to polish), or **shape** (brief confirmed), append to **Decision log** in `.heyeddi/design.md` per `reference/design-talk.md` — **cite primary persona + pattern borrowed + memorable detail for this project**.
5. After implementation, run `reference/audience-fit.md` on flagship routes before calling done.
6. Chain `@primevue-openprops-architect` validation and full **`@visual-auditor`** fix loop (review vs spec → fix → document) at 375/768/1440.

## Commands

| Command | Purpose |
|---------|---------|
| *(no sub-command)* | Vague design request → start **`discover`** |
| `init` | Create or refresh `PRODUCT.md`; offer `document` for `DESIGN.md` |
| `discover` | Discovery interview only — no code, no final brief yet |
| `research` | Web trend / reference research for current design direction |
| `explore` | Concept images + wireframes after discovery |
| `shape` | Full planning flow: discover → research → explore → confirmed brief |
| `document` | Generate or refresh `DESIGN.md` from code or seed questions |
| `craft` | Build a screen in Vue (runs `shape` first if no confirmed brief) |
| `critique` | UX review of **existing** UI — write report, no code unless asked |
| `polish` | Refine an existing route (**after critique**) |

Visual proof always delegates to `@visual-auditor` via **Task** (`shell` subagent) — see `reference/subagents.md`.

## Routing rules

1. **Existing UI — critique or improve** ("critique", "review", "what's wrong", "looks bad", "ugly", "fix this page", "polish the login"): load `reference/critique.md` first. If user wants fixes in the same turn → critique, then `reference/polish.md`. Do **not** start greenfield `discover` when code already exists for the target route.
2. **No sub-command, vague greenfield** ("enterprise view", "design the settings area" with no existing screen): load `reference/discover.md`. Do not jump to code.
3. **Sub-command matches table above**: load `reference/<command>.md` and follow it. Remaining words are the target/brief.
4. **`craft` without a confirmed design brief**: pause and run `shape` (full flow) first; resume `craft` only after explicit brief confirmation.
4b. **`craft` on flagship routes** (`/`, `/login`, `/dashboard`, `/settings`): if `load_context` reports `audience_ready: false`, stop — `@product-translator` or `discover` first.
5. **`polish` without critique this session**: run **critique** first, then polish.
6. **`init` blocker**: if `load_context` reports missing `PRODUCT.md` and the task is net-new or strategic, complete `init` then resume the original command.
7. **Screenshots / approved mockups provided**: stop — tell the user to use `@design-handoff` instead.
8. **Never invoke impeccable** — this skill replaces it for the HeyEddi stack.

## Artifacts

| Artifact | Location |
|----------|----------|
| Design brief (confirmed) | `.heyeddi/designs/<feature>/brief.md` |
| Wireframes | `.heyeddi/designs/<feature>/wireframes/` |
| Research notes | `.heyeddi/designs/<feature>/research.md` |
| Concept direction | Chat images + summary in brief |
| Design system | `.heyeddi/design.md` — [DESIGN.md format](https://getdesign.md/what-is-design-md); see [Superhuman example](https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/superhuman/DESIGN.md) |
| Product context | `.heyeddi/product.md` (legacy: root `PRODUCT.md`) |
| Skill reports, critiques | `.heyeddi/docs/` (critique reports, ship notes, audits) |

Use kebab-case for `<feature>` (e.g. `enterprise-settings`).

## Stack constraints

- **Foundations:** responsive, system light/dark, `en`+`es` i18n, WCAG 2.2 AA, dyslexia reading mode option — see `reference/foundations.md`.
- **Tokens:** semantic CSS variables from project `tokens.css` / `DESIGN.md` — OpenProps when the project already uses it; custom `:root` vars otherwise (`reference/token-strategy.md`). No raw hex in Vue/CSS unless documented exception.
- **Components:** PrimeVue from project catalog in `DESIGN.md`; no duplicate wrapper components.
- **Register:** `product` (app UI) vs `brand` (marketing) from `PRODUCT.md` — shapes density, nav patterns, and polish level.

See `context/VOCABULARY.md`, `context/ANTI_PATTERNS.md`, `context/EXAMPLES.md`, and `reference/foundations.md`.
