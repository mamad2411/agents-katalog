---
name: qahera-ui
description: "AI-Native UI Kit & Design System engine for Qahera UI Kit by Alwkala. Trigger on commands 'compose', 'scaffold', 'audit', 'theme', 'pattern', 'render', 'recipe', or requests to compose screens from canonical Qahera components, author new contracts and recipes, audit compliance against 17 invariants, generate multi-target renderers (HTML Native, React RSC, PHP, HTMX, Tailwind, Web Components), or apply Egyptian cultural themes."
metadata:
  version: 1.2.0
  author: Alwkala
  stack: Qahera UI Kit (HTML, React RSC, PHP, HTMX, Tailwind, Web Components)
---

# Qahera UI Kit — AI Native Design System Engine

A command dispatcher. This file does not perform operations directly — it routes user intents to the appropriate command, which loads the precise workflow and operational memory files.

$$\mathbf{\text{Qahera UI Kit}} = \mathbf{\text{Design System}} + \mathbf{\text{Registry}} + \mathbf{\text{AI Decision Layer}}$$

## Commands

| User intent | Command | What it loads |
|---|---|---|
| "Compose screen" / "Build layout" / "تركيب شاشة" / "صفحة جديدة" | `references/commands/compose.md` | `workflows/compose-screen.md` + `memory/templates-catalog.md` + `memory/patterns-catalog.md` + `memory/anti-slop-matrix.md` + `memory/7-axis-critique.md` |
| "UX Pattern" / "Compose pattern" / "أنماط الواجهة" / "تركيب نمط" | `references/commands/pattern.md` | `workflows/compose-screen.md` + `memory/patterns-catalog.md` + `memory/7-axis-critique.md` |
| "Scaffold component" / "New recipe" / "مكون جديد" / "إنشاء عقد" | `references/commands/scaffold.md` | `workflows/author-component.md` + `memory/controlled-vocabulary.md` + `memory/7-axis-critique.md` |
| "Audit template" / "Check template" / "فحص القالب" / "تدقيق القالب" | `references/commands/audit-template.md` | `workflows/audit-template.md` + `memory/anti-slop-matrix.md` + `memory/cli-tools.md` |
| "Audit kit" / "Check invariants" / "فحص المعايير" / "فحص الجودة" | `references/commands/audit.md` | `workflows/audit-kit.md` + `memory/anti-slop-matrix.md` + `memory/alpine-hydration-protocol.md` + `memory/cli-tools.md` |
| "Apply theme" / "Cultural theme" / "ثيم مصري" / "تغيير الطابع" | `references/commands/theme.md` | `workflows/compose-screen.md` + `memory/anti-slop-matrix.md` |

Read only the command file that matches the request. Do not load all files simultaneously.

## Non-Negotiable Invariants (AGENTS.md)

1. **YAML is Authoritative**: Canonical source of truth is strictly YAML (`contracts/`, `recipes/`, `tokens/`). Never edit generated files directly.
2. **Tokens Precede Styling**: Hardcoded hex, raw pixels, or arbitrary styles are prohibited. Trace everything to `--qhr-*` CSS custom properties.
3. **Contracts Precede Implementations**: No component exists without an explicit contract in `contracts/`.
4. **RTL is Infrastructure**: Logical CSS only (`margin-inline-start`, `padding-inline-end`, `inset-inline-start`). Never create separate RTL components.
5. **Arabic Typography Discipline**: **Alexandria** (display, headings, brand) & **Cairo** (body copy, UI labels, forms). **Amiri** is strictly forbidden in UI components.
6. **Renderer Parity Zero Drift**: Identical semantics and prop names across all 6 targets: `HTML Native`, `HTML Tailwind`, `PHP`, `HTMX`, `React RSC`, `JS Web Components`.
7. **Icons Canonical Architecture (`QAHERA-VISUAL-001`)**: Zero emoji. Icons strictly reference `icons/registry.yaml` or clean 24x24 SVG paths.
8. **Dogfooding Requirement (`QAHERA-COMP-001`)**: Compose screens exclusively from registered canonical components (`qhr-*`) and patterns (`patterns/`). Zero ad-hoc CSS classes.
9. **Alpine Hydration Integrity (`QAHERA-ALPINE-001`)**: Unique template `:key`s, zero nested `x-for`, zero interactive descendants in `<a>`, external `Alpine.data()`.
10. **Thematic Topography (`QAHERA-THEME-001`)**: Authentic Egyptian contexts (Heliopolis, Khedivial Downtown, New Cairo, Maadi, Nubia, Historic Cairo) via `[data-theme="..."]`.
11. **7-Axis Pre-Emit Critique**: All code emissions must be stamped with:
    `/* Pre-emit critique: P5 H5 E5 S5 R5 V5 D5 */`
12. **SVG Dimensional Discipline (`QAHERA-SVG-001`)**: All `<svg>` icons and motifs must define explicit `width`, `height`, and `viewBox` attributes, paired with defensive CSS scaling (`max-width: 100%`).
13. **Popover Wrapper Clean Encapsulation (`QAHERA-POPOVER-001`)**: Dropdown and megamenu wrappers (`.qhr-*-wrapper`) must tightly encapsulate triggers with zero `padding-bottom`. Use explicit alignment modifiers (`--start`, `--center`, `--end`) and `max-inline-size: calc(100vw - 32px)`.
14. **Navigation Purity & BiDi Flow (`QAHERA-NAV-001`)**: Zero hardcoded numbers/counts in navbar headers, single primary header CTA, externalized theme strips, and mandatory `<bdi dir="ltr">` isolation for Latin terms in Arabic copy.
15. **Compiler Bundle & Asset Integrity (`QAHERA-BUILD-001`)**: All atomic component styles must be registered in `CANONICAL_ORDER` in `cli/build-css.js`, compiled to `dist/qahera.css`, and previews must exclusively link to production `dist/` assets.
16. **Hero Skyline Panorama & Architectural Discipline (`QAHERA-HERO-001`)**: Hero section height MUST match the background illustration height (e.g. `height: clamp(500px, 62vh, 588px); max-height: 588px;`) to eliminate excessive empty top void. Symmetrical two-column isolation (`max-width: min(100%, 540px)`) with zero typo-visual overlap, flush bottom alignment (`align-items: flex-end`), feathered inward gradient masks, and mirrored RTL symmetry (`transform: scaleX(-1)`).
17. **Smart Custom Data & IDE Autocomplete (`QAHERA-CSS-DATA-001`)**: All design tokens and component interfaces must be exported to `qahera.css-data.json` and `qahera.html-data.json` conforming to Microsoft Custom Data v1.1 schemas. Zero guessing of token names; instant IDE hover cards and autocomplete.

## Progressive AI Context Protocol

When reasoning about UI components, load only the minimum required layer:
- **Level 0 (Templates & Patterns)**: `memory/templates-catalog.md` & `memory/patterns-catalog.md`.
- **Level 1 (Metadata)**: Read component `purpose`, `use_when`, `avoid_when`.
- **Level 2 (Recipe)**: Read `recipes/<name>.yaml` — structure, tokens, and slots.
- **Level 3 (Renderer)**: Read target renderer (`renderers/<framework>/<name>.*`).
- **Level 4 (Example)**: Inspect real usage in `examples/previews/` or `templates/`.

## Tooling Scope (Rule 10)

- **Languages**: Node.js (>= 18.0.0), YAML, CSS, HTML
- **Mutations**: Local workspace files (`contracts/`, `recipes/`, `renderers/`, `tokens/`, `patterns/`, `behavior/`, `templates/`)
- **CLI Tools**: `bin/qahera.js` (`add`, `init`, `list`, `build`, `validate`, `build:css`, `build:icons`, `build:ide-data`, `cdn`, `test`)
- **Network**: None required (100% offline deterministic execution)

