---
name: atelier-ui
description: Adaptive frontend and visual design orchestrator skill. Routes cleanly between brand/landing sites, SaaS/app UI refinement, and 3D/WebGL visual builds using 1-turn intake, progressive module loading, zero-install fallbacks, and deterministic QA gates. Trigger on UI/website design, redesign, landing pages, dashboards, or visual polish requests.
slash_commands:
  - name: atelier-ui
    description: Adaptive frontend design and Chrome CDP visual verification workflow.
---

# Atelier UI — Design Orchestrator

Keep context lean. Never load every module at once—route to **one** build module after intake, and offload mechanical checks to scripts.

In commands and paths below, `<skill>` is the directory containing this `SKILL.md` file (for example `~/.gemini/config/skills/atelier-ui`, `%USERPROFILE%\.gemini\config\skills\atelier-ui` on Windows, or workspace-local `.agents/skills/atelier-ui`). Always quote `"<skill>/..."` in shell commands so paths with spaces work.

## Workflow

### 1. Probe Environment (Once)
Run the capability scanner in the project root:
```bash
node "<skill>/scripts/detect-env.mjs"
```
Do not assume external tools (`impeccable`, `agent-browser`) exist. Use the JSON output (`project.framework`, `project.devCommand`, `tools.impeccableCmd`, `tools.agentBrowser`, `tools.browserBinary`, `tools.cdpSupported`) to pick the stack and QA tier.

### 2. Intake (1 Turn, With Defaults)
Read `<skill>/modules/01-intake.md` only if any core question is open.
- Ask all missing questions in **one** numbered message with defaults (or start immediately if the user gave full details or said `"defaults"` / `"go ahead"`).
- Write the settled plan to `.atelier/BRIEF.md` so context compaction never loses requirements.

### 3. Route to ONE Build Module
Pick the surface mode from the brief and read **only that file**:
- **Brand / Landing / Portfolio / Local Business (`Persuade` or `Experience`)**: read `<skill>/modules/02-brand-site.md`.
- **SaaS / Dashboard / Docs / Existing App (`Operate` or `Read`)**: read `<skill>/modules/03-app-ui.md`.
- **3D World / WebGL / Shaders (`3D`)**: read `<skill>/modules/04-3d-visual.md`.

### 4. Universal Craft Floor (Always Active)
1. **Tokens over raw hex:** Use CSS custom properties (`:root`) or the project's existing Tailwind/theme tokens.
2. **No layout traps:** `overflow-x: clip` on `html, body` (never `100vw`); `minmax(0, 1fr)` on image grid tracks; `min-width: 0; overflow-wrap: break-word` on display headings.
3. **Motion & accessibility:** Never `transition: all`; animate only `transform` / `opacity` / `clip-path` / `filter`; add `:focus-visible` and `@media (prefers-reduced-motion: reduce)`.
4. **Anti-slop ban list:** No unearned purple-to-blue gradients, no gradient text on body/headings, no nested cards inside cards, no `01/02/03` eyebrow kickers above headlines, no emojis as UI icons, no invented testimonials, logos, or metrics.
5. **Contrast & states:** Body text >= 4.5:1, large text >= 3:1; every interactive control covers default, hover, focus-visible, disabled, loading, empty, and error states.
6. **Clean copy:** Buttons are `<Verb> <Object>` (never generic `"Learn more"`). Never leave placeholder text (`Lorem ipsum`, `Acme`, `TODO`).

*(Mechanical checks live in `lint-ui.mjs` and `check-ui.mjs`; structural layout rules such as nested cards and `minmax(0, 1fr)` are verified by you and the Tier 3 critic.)*

### 5. Verify & Critic Gate
After building, read `<skill>/modules/05-qa-gate.md` and execute the QA ladder:
1. Static slop lint (`tools.impeccableCmd` if detected, plus `node "<skill>/scripts/lint-ui.mjs" <target-dir>`).
2. Browser check (`agent-browser`, your environment's browser tool, or `node "<skill>/scripts/check-ui.mjs" <target> --out .atelier/shots --full --sheet`) at desktop (`1440x900`) and mobile (`390x844`).
3. Optional zero-context visual critic review using the captured screenshots (when `QA Depth` is `critic` or `deep`).

## Files in This Skill
| Path (under `<skill>/`) | Load When |
|---|---|
| `modules/01-intake.md` | Step 2: clarifying ambiguous briefs & writing `.atelier/BRIEF.md` |
| `modules/02-brand-site.md` | Step 3: new marketing, company, local business, or portfolio pages |
| `modules/03-app-ui.md` | Step 3: dashboards, tools, docs, or refining existing apps |
| `modules/04-3d-visual.md` | Step 3: Three.js, WebGL, or shader builds |
| `modules/05-qa-gate.md` | Step 5: running lints, browser checks, and zero-context critic reviews |
| `library/themes.json` | Step 3 (`02-brand-site`): dealing non-generic color & font pairings |
| `scripts/detect-env.mjs` | Step 1: detecting project stack and installed CLI/browser tools |
| `scripts/lint-ui.mjs` | Step 5: built-in zero-dependency slop & Craft Floor linter |
| `scripts/check-ui.mjs` | Step 5: built-in zero-dependency Chrome DevTools Protocol (CDP) verifier |
