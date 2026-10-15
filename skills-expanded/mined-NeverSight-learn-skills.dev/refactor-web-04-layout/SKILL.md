---
name: refactor-web-04-layout
description: Use this skill when the user wants to check or generate front-end page layout and interaction code against the integrated-system UI standard — for example when they mention "page layout standard", "interaction rules", "page hierarchy", "modal/dialog sizing", "drawer sizing", "scrollbar rules", "hover feedback", "toast/notification rules", "generate a page", or "page template". It is step 4 of 5 of the frontend governance lane in the refactor-chain bundle. The ruleset is selected adaptively from the project's `package.json` `version` (supports `3.6.0-SNAPSHOT`, `3.6.1-SNAPSHOT`, `3.7.0-SNAPSHOT`).
---

# Front-End Layout & Interaction Standards — refactor-chain · Web lane · step 04/05

**Bundle:** refactor-chain (orchestrated, self-healing refactor chain-of-skills).
**Lane:** Frontend project governance (versioned) · **Position:** step 04 of 05 · **Prerequisite:** refactor-web-03-components · **Next:** refactor-web-05-naming.
**Adaptivity:** Selects the versioned ruleset from `package.json` `version` (supports `3.6.0-SNAPSHOT`, `3.6.1-SNAPSHOT`, `3.7.0-SNAPSHOT`).

## Purpose
This skill is the multi-version-adaptive checker and code generator for front-end page layout and interaction. Grounded in the *Integrated System UI Standard*, it enforces standardized constraints on layout structure, page hierarchy, modal/drawer sizing, scrollbars, hover feedback, and toast messages. It also ships page-level templates and reference samples so conforming page code can be generated quickly. The active rules are chosen automatically from the project version, so the same skill governs multiple releases without manual switching.

## When to use
- Verify that a page's layout complies — triggers: "page layout standard", "page hierarchy", "modal/dialog rules", "drawer rules".
- Verify that interaction behavior complies — triggers: "interaction rules", "scrollbar rules", "hover feedback", "toast/notification rules".
- Browse standard layout samples — triggers: "page sample", "layout sample", "dialog sample", "card sample".
- Generate a page from a template — triggers: "generate a page", "page template", "primary page", "full-screen page", "drawer page".

## Rules enforced
Version detection runs first and is mandatory: read the project root `package.json`, extract `version`, and route as follows — exact match to `3.6.0-SNAPSHOT` / `3.6.1-SNAPSHOT` / `3.7.0-SNAPSHOT`; fuzzy `3.6.x-SNAPSHOT` → `3.6.1-SNAPSHOT` (latest of the 3.6 series); fuzzy `3.7.x-SNAPSHOT` → `3.7.0-SNAPSHOT`; anything else or unreadable → default `3.6.0-SNAPSHOT` (baseline). Then load that version's `REFERENCE.md` for the full ruleset.

**S06 — Page layout (9 rules):**

| ID | Check | Level |
|------|--------|------|
| `S06-01` | Page hierarchy | ERROR |
| `S06-02` | Breadcrumbs | WARNING |
| `S06-03` | Outer-border consistency | WARNING |
| `S06-04` | Modal/dialog sizing | WARNING |
| `S06-05` | Drawer sizing | WARNING |
| `S06-06` | Fixed action area | WARNING |
| `S06-07` | Tab position | WARNING |
| `S06-08` | Full-screen coverage | ERROR |
| `S06-09` | Card spacing | SUGGESTION |

Key points: page hierarchy runs full-screen page > drawer page > modal dialog, and each nested page type must be less than or equal to its parent's type. Breadcrumbs must not exceed ten levels and their width must stay under 60% of the page width. Modal sizing: prompt/confirm boxes use the small size; single-column entry uses `480px` width; two-column entry uses `720px` width. Drawer sizing: detail drawers use `480px` width; entry drawers use `720px` width.

**S07 — Interaction behavior (8 rules):**

| ID | Check | Level |
|------|--------|------|
| `S07-01` | Unified scrollbar | WARNING |
| `S07-02` | Menu-bar interaction | WARNING |
| `S07-03` | Toast/notification rules | ERROR |
| `S07-04` | Hover feedback | SUGGESTION |
| `S07-05` | Ellipsis handling | WARNING |
| `S07-06` | Auto-lock | SUGGESTION |
| `S07-07` | Amount units | WARNING |
| `S07-08` | Navigation-bar memory | SUGGESTION |

Key points: scrollbars share one global style, hidden by default, shown on mouse-enter and hidden on mouse-leave. Toast messages: success is green and auto-dismisses (3 seconds); warning is yellow and either closes manually or auto-dismisses; error is red and must be closed manually; over-long text is auto-truncated. Hover feedback: buttons change color on hover, table rows highlight on hover, links show an underline on hover.

## Procedure
1. Detect the project version from `package.json` and resolve the version directory using the routing table above.
2. Load that version's `REFERENCE.md` to obtain the full check and generation rules.
3. For a check task: fix the scope (files/directory and rule category — layout, interaction, or all), run each rule per `scripts/layout-rules.md` and `scripts/interaction-rules.md`, then emit a report of compliant items, violations, and fix suggestions.
4. For a generation task: have the user pick the page type (primary / full-screen secondary / drawer / dialog), read the matching skeleton from `templates/` (`T01`–`T04`), adjust details against the matching sample (`E08`–`E14`), then self-check the output against S06 and S07.

## Guardrails
- Do not change business logic/behavior; structural + standards refactoring only.
- Never violate the page-hierarchy descent rule, always use the standardized modal/drawer widths, and keep every interaction behavior consistent with the global standard.

## Verify
Confirm the resolved version matches `package.json` (or documents the fallback). Every applicable S06 and S07 rule is checked with each violation carrying an ID, level, and fix suggestion. Any generated page passes an S06/S07 self-check, uses standard widths, and respects the hierarchy constraint.

## References
The exhaustive original rules, versioned rule sets, and templates are bundled verbatim under `references/original/` (source of truth).

## Chain position
Runs after refactor-web-03-components. On success the orchestrator advances to refactor-web-05-naming. `refactor-code-solid` runs by default as the final step of the lane.
