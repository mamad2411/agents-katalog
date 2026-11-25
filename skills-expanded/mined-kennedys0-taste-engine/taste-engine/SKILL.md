---
name: taste-engine
description: Routes visual UI work to a user-chosen aesthetic and applies SEO readiness to public-facing websites. Use whenever a user asks to build, create, design, or redesign a website, portfolio, landing page, dashboard, web app, mobile app, UI/UX screen, frontend, or component, or add/refine micro-interactions or full-screen hero sections (including Indonesian prompts such as "build a portfolio website"). Before writing UI code, ask ONE style question and stop if no visual style or approved project design system is specified. If the prompt already names an aesthetic such as claymorphism, frutiger-aero, brutalism, neo-brutalism, minimalism, bento, retro-pixel, art-deco, y2k-futurism, or editorial, load its bundled style pack immediately and proceed WITHOUT asking again. Preserve established styles for minor fixes; for SEO-only tasks, load the SEO module without a visual style question; skip unrelated non-visual work. Detailed contracts live in references/router-playbook.md.
license: MIT
metadata:
  version: "0.13.1"
---

# Taste Engine — style router

**One universal process, many independent tastes — with anti-slop, conditional public SEO and optional style-aligned motion.** This file controls **when to ask, which style pack to load, and where the detailed contracts live**. The engine has no house aesthetic; `styles/*.md` hold the design instructions. Full contracts (material fidelity, hero geometry, SEO routing, PoW showcases, apply-steps, guardrails): [router playbook](references/router-playbook.md).

## Hard requirement: preflight before new visual implementation

For tasks that introduce or substantially redesign visual UI, **do not write UI code, generate mockups, or change design tokens until the visual direction is resolved**.

1. Examine the request, existing brand/design system, and any approved project style config.
2. **Style already explicitly selected** ("brutalist dashboard") → do not ask again; load that pack.
3. **Established project + incremental change** → preserve its style; no menu. A redesign request may override it.
4. **Otherwise ask exactly one concise style-selection question and stop.** Offer 6 contrasting choices plus "More styles / Custom / Send reference". Never silently select, never code while awaiting the reply, never ask a multi-question interview. The question template is in the [router playbook](references/router-playbook.md#8-mandatory-first-question-example-in-indonesian).
5. On answer: resolve the style ID via `styles/registry.json`, read **only** the selected pack(s), then execute.
6. If a tool-runner cannot pause for user input, report the unresolved selection; do not fabricate consent. An explicit autonomous best-effort default may authorize a provisional, reversible style.
7. **Domain pre-flight:** before resolving the visual direction, state the product domain and audience in one sentence (fold it into the style question if missing).

## Automatic invocation: the zero-command contract

- This is a **task-triggered skill**, not a slash-command workflow; agents should discover it on portfolio, website, app, dashboard, landing-page, and UI redesign requests even when the user never says "taste-engine".
- **Implicit style:** "build me a portfolio website" → ask ONE style question, end turn.
- **Explicit style:** "build a portfolio website in skeumorphsm style" → normalize the typo (`skeuomorphism` → `frutiger-aero`, variant `tactile`), read the pack, and build **WITHOUT asking again**. No question menu.
- **Established project / non-visual work:** no menu, no selector. Details: [auto-invocation](references/auto-invocation.md).

## Available style packs

Read `styles/registry.json` for IDs, **aliases, misspellings**, and negations. `python3 scripts/style_probe.py --prompt "..."` gives a deterministic hint; semantic interpretation wins. Never call a standalone style skill by name — read the local pack:

| ID | Direction | File to load once selected |
| --- | --- | --- |
| `claymorphism` | Sculpted tactile | [style pack](styles/claymorphism.md) |
| `frutiger-aero` | Mid-2000s gloss & nature-tech (Classic, Glass, Tactile) | [style pack](styles/frutiger-aero.md) |
| `brutalism` | Raw structural (Raw & Bento variants) | [style pack](styles/brutalism.md) |
| `neo-brutalism` | Playful bold | [style pack](styles/neo-brutalism.md) |
| `minimalism` | Restrained clarity & data cockpits | [style pack](styles/minimalism.md) |
| `swiss-editorial` | Typographic grid | [style pack](styles/swiss-editorial.md) |
| `retro-terminal` | Console aesthetic | [style pack](styles/retro-terminal.md) |
| `retro-pixel` | 8-bit/16-bit arcade desktop | [style pack](styles/retro-pixel.md) |
| `art-deco` | Geometric elegance & luxury (Modern, Classic, Minimal) | [style pack](styles/art-deco.md) |
| `y2k-futurism` | Chrome & iridescent cyber-optimism (Chrome, Holographic, Retro Tech) | [style pack](styles/y2k-futurism.md) |

**Custom is first-class:** an unlisted aesthetic gets a provisional project-specific definition using the same dimensions; never mislabel it as an existing pack.

## Router states

- **`needs-selection`**: new visual work, no direction → ask a style question **and stop**.
- **`ready`**: style or brand established → load the pack and implement.
- **`refine`**: small change → preserve style, touch only necessary tokens/components.
- **`custom`**: blend/screenshots/unspecified style → map to the same dimensions; confirm only consequential ambiguity.
- **`non-visual`**: backend, tests, docs, bug fixes → skip design selection entirely.

Detailed routing, blends, conflicts: [style router](references/style-router.md).

## Conditional companions — load only when relevant

- **Material fidelity:** selected styles must be **recognizable from the rendered interface**. Each pack has its own fidelity gate (`frutiger-aero`, `y2k-futurism`, clay, glass, and so on) plus explicit material exceptions that override generic anti-gradient/anti-shadow reflexes. Details: [playbook §1](references/router-playbook.md#1-material-fidelity--screenshot-level-contract).
- **Engineering:** every web UI gets the universal [Web Interface Quality](references/web-interface-quality.md) gate via the [Engineering Router](references/engineering-router.md); React/Next adds [React Performance](references/react-performance.md), React Native/Expo adds [Native Mobile](references/native-mobile.md) instead of web SEO. Never deploy without explicit intent.
- **Full-screen hero:** new public hero pages follow the [Hero Contract](references/hero-layout.md) — mobile-safe `100svh` minus the real header height, never a fixed `100vh` that clips. No hero for screens that don't need one.
- **Motion:** optional [Motion Engine](references/motion-engine.md) — never a second interview, no automatic dependency installs, reduced-motion respected. Mapping in `styles/motion-profiles.json`.
- **SEO:** automatic for a new or substantially redesigned **public website**; **no style question** accompanies it. **SEO-only** request → load [SEO module](references/seo.md) directly. Private/internal apps stay private. Details: [playbook §5](references/router-playbook.md#5-seo-routing-rules-detail).
- **PoW showcases** (`docs/*.html` and similar): reuse `presets/templates/pow-showcase.template.html` with its 7 canonical sections. Details: [playbook §6](references/router-playbook.md#6-pow-showcase-architecture-detail).

## Applying the style after selection

Condensed sequence (full detail: [playbook §7](references/router-playbook.md#7-applying-the-style-after-selection-detail)):

1. **Domain pre-flight** → 2. **load only the selected pack** ([Decision System](references/decision-system.md)) → 3. **build the project Design DNA** ([translation](references/translation.md), dark/light token coupling, [Responsive Baseline](references/responsive-baseline.md) with strict multi-column card balance) → 4. **resolve precedence** (safety/accessibility → request → brand → pack → conventions) → 5. **implement in the existing stack**, no assumed libraries → 6. **Anti-Slop Gate**: read [Anti-Slop Constitution](references/anti-slop.md) and [Anti-Slop Writing](references/anti-slop-copywriting.md), apply the pack's `## Anti-slop: style-specific` section → 7. **tiered quality** ([quality-tiers](references/quality-tiers.md), [writing calibration](references/writing-calibration.md)) → 8. **audit** ([quality gates](references/quality-gates.md), [anti-slop audit](references/anti-slop-audit.md)); fix Critical/High, report checks not run → 9. **SEO where relevant** → 10. **refine** from feedback ([feedback](references/feedback.md)).

## Non-negotiable anti-slop contract

All style packs and every custom style pass the **shared anti-slop quality bar** — no visual theme justifies deceptive data, useless nested cards, hype copy, misleading buttons, inaccessible typography or clutter. **Signature traits are exempt from aesthetic blacklists when purposeful and usable.** Anti-slop is a decision framework, not a minimalism preset; it belongs in the final QA pass, and non-visual tasks skip it entirely.

## Triggering examples — no manual skill call

| User prompt | Required agent behavior |
| --- | --- |
| `Build me a portfolio website` | Auto-discovered; ask for style and **STOP** until user replies |
| `Build me a skeumorphsm portfolio website` | Typo `skeuomorphism` → `frutiger-aero` (variant `tactile`); load pack directly; **do not ask** |
| `Create a brutalist portfolio` | Read `styles/brutalism.md` directly; build (not neo-brutalism) |
| `Build a glassmorphism landing page, not clay` | `glassmorphism` → `frutiger-aero` (variant `glass`); honor negative clay instruction |
| `Fix the broken checkout button` | Preserve existing UI style; no new menu |
| `Optimize SEO on my existing live portfolio` | Load `references/seo.md` directly; **no style prompt or redesign** |
| `Build an SEO-friendly Brutalism portfolio` | Load `styles/brutalism.md` + `references/seo.md`; **no style prompt** |
| `Build a private admin dashboard` | Do not expose restricted routes or create public sitemap for them |
| `Build a payment API endpoint` | Non-visual; no style menu |
| `Tambahkan micro-interaction pada tombol di UI existing` | Preserve existing style; CSS first, optional Anime.js v4 only if justified |
| `Build a brutalist landing page with a full-screen hero` | Brutalism + hero contract + public SEO; no extra style question |
| `Build a Retro Pixel portfolio` | Load `styles/retro-pixel.md` directly; build (not retro-terminal) |

## Compatibility note

This is an **instruction-based gate**, not a platform-enforced hook. For hosts that load skills unreliably, add the optional [`AGENTS.md` activation snippet](assets/AGENTS.snippet.md) or a host-specific pre-tool policy. A coding agent must be capable of pausing for the user's reply. For audits, redesigns and visual evidence, see [playbook §12](references/router-playbook.md#12-existing-projects-and-visual-evidence).
