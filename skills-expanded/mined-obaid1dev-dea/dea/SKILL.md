---
name: dea
description: Design Engineer Anything. Give the agent a website name or URL (or screenshots) and it extracts the full design system (colors with roles, dark mode, typography, spacing, radius, shadows, motion, hover and focus states, layout, components, page anatomy, responsive behavior), then builds a new site or app, or redesigns an existing project, in that design. Use whenever the user wants to extract or reverse-engineer a site's design, design system, brand colors, fonts, or theme; asks to "redesign my app using the design of X", "make it look like Vercel/Linear/Stripe/Apple", "clone the look/feel/style of this site", "match this design", "get the tokens/CSS variables/Tailwind config from this website", "build a landing page in the style of X", or shares a link or screenshots as a design reference. Also use to blend two designs or document a design system from a live site.
---

# DEA: Design Engineer Anything

Act like a senior design engineer. Take any site (or screenshots), measure its design precisely with a real browser, look at it with your own eyes, write it up as a design system, and then build or redesign something in that system. Measured values first, judgment second, never guessed hex codes.

## Contents
- Modes and intake
- Workflow (Phases 1-7)
- Rules
- Tool tiers and commands
- Reference files

## Modes and intake

Infer the mode from the request. Ask at most ONE question, and only if a missing detail would make the work wrong (no target at all, or a redesign with no project provided).

| Mode | Trigger | Output |
|---|---|---|
| **Extract** | "get the design system of X", "what fonts/colors does X use" | `design/<site>/` with `DESIGN.md`, `tokens.*`, screenshots |
| **Redesign** | "redesign my app/site using X's design" | Restyled project + before/after + changelog |
| **Build** | "build a landing page/app in the style of X" | New project in that design |
| **Blend** | "A's layout with B's colors" | Combined system + build |
| **Replicate (own site)** | user owns the target | Faithful rebuild including content |

Intake checklist (infer, do not interrogate): target(s) as URL / name / screenshots; mode; adaptation level (default: **adopt the full design system but keep the user's brand, logo, copy and content**, see `references/brand-fusion.md`); the user's stack (for Redesign scan the project; for Build default to Next.js + Tailwind if unspecified, or plain HTML/CSS/JS for a simple static page, or the stack the user named); pages/screens to cover.

If only a name is given, web-search for the official site, confirm the domain, and continue. For a ranked choice (several plausible sites), pick the official product site and state it.

## Workflow

### Phase 1: Capture (measure)
Choose the best tier available and say which one you used (details in `references/extraction-playbook.md`):
1. **Tier A, Playwright (preferred):**
   ```bash
   node scripts/extract.mjs <url> --out design/<site> [--pages /pricing,/docs] [--crawl 3]
   ```
   Produces `raw.json` plus screenshots (desktop, tablet, mobile, dark, per-section, extra pages) and measures tokens, components, hover/focus diffs, fonts, breakpoints.
2. **Tier B, browser tool** (Claude in Chrome, Playwright/DevTools MCP): evaluate `scripts/inpage.js` in the page, save as `raw.json` (`{"light": <result>, "url": ...}`), take the screenshots with the tool.
3. **Tier C, static fallback** (no browser): `fetch_assets.py` then `analyze_css.py`. Declared CSS only; say what is missing.
4. **Tier D, screenshots only:** `image_palette.py` to measure colors from pixels; read the rest visually.
Capture the homepage plus 2-4 representative inner pages (pricing, content, form/app screen). Never defeat bot protection or logins; if blocked, ask for screenshots.

### Phase 2: Look (required, never skip)
Open and actually view the key screenshots: desktop fold, desktop full page, a couple of section shots, mobile, dark if present. Apply `references/visual-analysis.md`: grid, hierarchy, density, type voice, color behavior, shape, depth, imagery, component signatures, motion cues, responsive moves. Note what the numbers cannot tell you (illustration style, hero visuals, effects).

### Phase 3: Synthesize (turn measurements into a design system)
```bash
python3 scripts/synthesize.py design/<site>/raw.json --out design/<site> --name "<Site>"
```
Writes `tokens.json`, `tokens.css`, `tailwind.config.js`, `tailwind-v4.css`, `DESIGN.md`. Then do the refinement pass in `references/design-system-spec.md`: verify roles against the screenshots, resolve low-confidence items, replace every `<!-- AGENT -->` marker (aesthetic summary, consistency rules), add what scripts cannot see, document hover/focus/active states, confirm dark mode. In Extract mode, stop here and deliver.

### Phase 4: Decide the adaptation
Pick the level from `references/brand-fusion.md` (default: full system, user's brand and content). For Blend, write the per-axis mapping at the top of `DESIGN.md`. Keep a one-paragraph decision note.

### Phase 5: Build or redesign
- **Build / Replicate:** follow `references/rebuild-guide.md`: tokens, fonts (open alternatives for proprietary fonts, `references/font-alternatives.md`), global styles, layout shell, primitives, sections following the page anatomy, motion, responsive, dark mode.
- **Redesign:** follow `references/redesign-existing-app.md`: `scripts/scan_project.py`, capture "before", migrate in passes (tokens, shell, primitives, screens, polish), preserve behavior and accessibility, keep a changelog.
Use the user's content, logo and images. If none are provided, use realistic placeholder copy and neutral shapes or gradients, never the reference site's assets.

### Phase 6: Verify (fidelity loop, max 3 rounds)
1. Serve the result and capture it: `node scripts/extract.mjs http://localhost:PORT --shots-only --out design/rebuild`.
2. `python3 scripts/compare.py design/<site>/screenshots/desktop-full.png design/rebuild/screenshots/desktop-full.png --out design/compare`, then view `side-by-side.png`. Fix the worst bands first (container width, section padding, type size and line-height, color roles, radius, shadow). Repeat for mobile and dark.
3. Also run build, lint, type-check and tests; check contrast (AA for body text), no horizontal overflow, focus-visible states, reduced-motion handling.
Stop when structure, spacing, type hierarchy and color relationships match; content will differ and that is fine.

### Phase 7: Deliver
Short summary: what you captured (tier, pages), the aesthetic in two sentences, what you built or changed and where, before/after or reference/result screenshots, assumptions, what was substituted (fonts, assets), unknowns, and next steps. Point to `design/<site>/DESIGN.md`. Keep chat replies brief; the detail lives in the files.

## Rules

- **Measure, do not guess.** Colors, sizes, fonts and spacing come from `raw.json`/`tokens.json` or pixel sampling. Mark estimates as estimates with a confidence.
- **Look at the screenshots.** Scripts infer roles; you verify them. Correct anything that does not match what you see.
- **Brand identity is the user's.** Never ship another brand's logo, name, trademarks, photography, illustrations, proprietary font files, or verbatim copy. Reproduce the design language, not the identity. Never build deceptive look-alikes (fake login/checkout/support pages, phishing, anything passing as the original). Read `references/ethics-and-ip.md` when the request is for a near-exact clone of someone else's site.
- **Preserve behavior in redesigns.** Change appearance only: no logic, routing, data or API changes. Work on a branch/copy, commit per pass if git is available.
- **System before pages.** Tokens, fonts, global styles and primitives first; pages inherit.
- **Cover the states.** Hover, focus-visible, active, disabled, loading, empty, error; mobile; dark mode when the reference has it.
- **Accessibility holds.** Keep or improve semantics, keyboard use, focus rings; if the reference fails contrast, keep the look but meet AA for body text and say so.
- **Stay polite and in scope.** Capture only public pages (or the user's own authorized session), a handful of pages per site, no hammering, no bypassing protections.
- **No secrets.** Never ask for passwords; use a saved browser session (`--auth`) or screenshots.
- **Be honest about gaps.** List unknowns (blocked stylesheets, uncaptured states, WebGL/video heroes, fonts you substituted).
- **Files, not essays.** Put the design system in `DESIGN.md` and the tokens in code; keep chat output short.

## Tool tiers and commands (quick reference)

```bash
# one-time (Tier A): npm i -D playwright && npx playwright install chromium
node scripts/extract.mjs <url|file|http://localhost:3000> --out design/<site>      # capture
node scripts/extract.mjs <url> --shots-only --out design/rebuild                  # screenshots only (verification)
python3 scripts/synthesize.py design/<site>/raw.json --out design/<site> --name "<Site>"
python3 scripts/compare.py <ref.png> <new.png> --out design/compare              # needs Pillow
python3 scripts/image_palette.py <shot.png> --colors 8 --sample x,y --grid 6x4   # needs Pillow
python3 scripts/scan_project.py <project-dir>                                    # before a redesign
python3 scripts/fetch_assets.py <url> --out design/<site>/src && python3 scripts/analyze_css.py design/<site>/src --out design/<site>/raw.json --url <url>   # Tier C
```
Run scripts from the skill folder or use their full paths. If Playwright is missing and cannot be installed, drop to Tier B/C/D. If Node is unavailable, Tier C/D still work with Python only (standard library; Pillow only for the two image tools).

## Reference files

| File | Read when |
|---|---|
| `references/extraction-playbook.md` | Phase 1: tiers, flags, hard cases (bot checks, SPAs, login, WebGL), folder convention |
| `references/visual-analysis.md` | Phase 2: how to read screenshots; estimating values from pixels; aesthetic vocabulary |
| `references/design-system-spec.md` | Phase 3: refinement checklist, token naming, quality bar for `DESIGN.md` |
| `references/brand-fusion.md` | Phase 4: adaptation levels, blending, mapping to the user's brand |
| `references/rebuild-guide.md` | Phase 5-6: per-stack setup, primitives, motion, responsive, dark mode, fidelity loop |
| `references/redesign-existing-app.md` | Redesign mode: step-by-step migration that preserves behavior |
| `references/font-alternatives.md` | Whenever the reference uses a proprietary font |
| `references/ethics-and-ip.md` | Near-exact clone requests; what to copy and what never to copy |
