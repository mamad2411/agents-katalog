---
name: ns-proto-creator
description: >-
  (NS) Playwright reverse-prototyping face — capture live UI, then create or
  evolve a single prototype/ tree (git history; never v1/v2 copies). Use when
  prototyping from a URL, reversing a screen into prototype/, evolving an
  existing prototype, AS-IS flows/fields, or "prototype this app/page". Do NOT
  use for normative appearance MDs only (ns-proto-visual-guide), full SDD
  (ns-spec-driven), bare code fixes (ns-code-coder), or brownfield prepare
  (/ns-harness-prepare).
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.0"
depends:
  - ns-harness
  - ns-code-frontend-design
  - ns-code-best-practices
  - ns-sdd-living-spec-consolidator
  - ns-proto-visual-guide
---

# Proto Creator

**Delivery face:** Playwright reverse prototyping. Capture → AS-IS docs → create/evolve one `prototype/` → quality → living appearance → optional visual guides.

**Orchestrate.** Load worker `SKILL.md` at delegation. No inline full design checklists or Element|How tables.

## Layout (locked)

```
{product_root}/
  prototype/              # THE prototype — create once, evolve forever
  docs/                   # AS-IS briefs, screenshots, appearance guides
  docs/specs/             # Living domain specs (when consolidating)
```

- Missing `prototype/` → **create**.
- Existing `prototype/` → **evolve in place**.
- Never scaffold `vN/prototype/` or ask version-folder name. Versioning = **git**. Optional: remind commit after meaningful evolve.

## Harness discovery

See `../ns-harness/references/harness-discovery.md` and `../ns-harness/references/artifact-layout.md`.

| Variable | Resolve via |
| -------- | ----------- |
| `{product_root}` | `AGENTS.md` product anchor |
| `{harness_root}` | Harness discovery |

## Near-miss routing

| User wants | Redirect |
| ---------- | -------- |
| Only `*-visual.md` / descrição normativa / guia de aparência | `ns-proto-visual-guide` |
| Full SDD version / requirements / tasks | `ns-spec-driven` |
| Bare bugfix, no prototype scope | `ns-code-coder` |
| Brownfield architecture map only | Tell user run `/ns-harness-prepare` |

## Boot (mandatory, once per session)

Short natural-language questions. No giant questionnaire.

1. **Base URL** — login / which Playwright MCP profile if multiple.
2. **Scope** — screens, roles, add/change.
3. **Prototype mode** — detect `{product_root}/prototype/`:
   - absent → **create**
   - present → **evolve in place**

No version-id / `v1` folder question.

## Journey

```mermaid
flowchart TB
  boot[Boot questions]
  capture[Capture Playwright]
  asis[AS-IS docs]
  build[Build or evolve prototype]
  quality[Best practices + guidelines]
  living[Living appearance]
  handoff[Offer visual guide]

  boot --> capture --> asis --> build --> quality --> living --> handoff
```

| Phase | Reference / worker | Behavior |
| ----- | ------------------ | -------- |
| Capture | `references/capture-playwright.md` | Discover Playwright MCP; navigate; screenshots; note structure, fonts, icons, density |
| AS-IS | `references/as-is-docs.md` | Write/update `{product_root}/docs/` briefs from evidence |
| Build / Evolve | `references/build-prototype.md` + `ns-code-frontend-design` | Only under `{product_root}/prototype/`; mirror flows/fields/states; modern stack — no legacy clone |
| Quality | `ns-code-best-practices` | Hygiene + Web Interface Guidelines fetch on prototype surfaces |
| Living | `ns-sdd-living-spec-consolidator` **appearance** | Create `docs/specs/` + INDEX if missing; SHALL for visible product behavior only |
| Handoff | `ns-proto-visual-guide` | Offer / run for implementation appearance MDs |

## Hard rules

- One prototype tree; evolve in place; never parallel `vN/` copies
- Fidelity from live Playwright evidence; no invented screens
- Stack-free modern UI under `prototype/` — load `ns-code-frontend-design`
- English for this skill's artifacts; project docs language follows repo
- Versioning = git; optional commit remind after meaningful evolve
- No hardcoded product-specific login — project rules / user credentials path

## Related skills

- `ns-proto-visual-guide` — normative appearance MDs
- `ns-harness-codebase-reverse-spec` — business reverse from code (complement URL capture)
- `ns-code-frontend-design` / `ns-code-best-practices` — design + quality workers
