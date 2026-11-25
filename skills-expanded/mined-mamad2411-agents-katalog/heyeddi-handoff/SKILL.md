---
name: heyeddi-handoff
description: Implements screens from designer screenshots and handoff notes. Two-pass workflow — designer writes mockup-brief with Implementation spec, implementer builds shell then route, verify_handoff checks tokens and layout. Use when approved mockups exist — not for greenfield design.
disable-model-invocation: true
---

# HeyEddi Handoff

**Screenshot-first Vue implementation** — designer then implementer in two explicit passes (mockup-brief → shell → route). See `reference/handoff-to-code.md`.

## Subagents (default)

**Orchestrate in main chat; delegate phases via Cursor Task tool.** See `reference/subagents.md`.

- **Pass 1 (interpret):** `generalPurpose` subagent — mockup-brief + Implementation spec only; then `shell` for `describe_handoff`.
- **Pass 2 (build):** `explore` for catalog → `generalPurpose` for shell then route → `shell` for `verify_*`, npm, `@visual-auditor`.
- Do not inline Playwright or full implement in the same subagent as interpret.

Gate each phase before launching the next subagent.

## When to use

- Designer attaches desktop/mobile screenshots for a route
- `.heyeddi/designs/<feature>/` has reference images
- Implementing an approved mockup without Figma MCP

## Instructions

### Pass 1 — Designer (interpret)

1. Run `python scripts/load_handoff.py --route <route> --project-root <root>`.
2. Read `.heyeddi/product.md` — **Personas** + **Per-route intent** for this route; align brief microcopy and hierarchy (`heyeddi-design/reference/audience-design.md`).
3. Read `reference/interpret-mockups.md` (PNG) or `reference/low-fidelity-mockups.md` (`wireframe.md`) — write `mockup-brief.md` with **Implementation spec** + **Theme notes**.
4. Run `python scripts/describe_handoff.py --route <route> --sync-design`.
5. **Stop** — do not write Vue until Implementation spec is complete.

### Pass 2 — Implementer (build)

5. Read `reference/handoff-to-code.md` + `mockup-brief.md` Implementation spec.
6. Update `tokens.css` from spec — **no same-name aliases** (`--size-6: var(--size-6)` breaks spacing). Run `python scripts/verify_tokens.py --check`.
7. Build **AppShell / AppSidebar / AppTopBar**.
8. Run `python scripts/verify_handoff.py --route <route> --phase shell --check`.
9. Build route content (e.g. `SettingsView`) — override PrimeVue Card padding per spec.
10. Run `python scripts/verify_handoff.py --route <route> --phase full --check`.
11. Run `python scripts/verify_theme.py --check` — light/dark + PrimeVue surfaces (`reference/theme-coherence.md`).
12. Read `reference/mockup-contract.md` when needed.
13. Chain `@primevue-openprops-architect` → `@visual-auditor` when available.
14. **Append** Decision log — region → component + rationale.

## Modes

- Screenshot (v1): `reference/screenshot-mode.md` + `reference/interpret-mockups.md` + `reference/handoff-to-code.md`
- Wireframe / ASCII: `reference/low-fidelity-mockups.md` + `wireframe.md` (no PNG required)
- PrimeVue Card slots: `reference/primevue-card-slots.md` — body content in `<template #content>`
- Penpot (future): `reference/penpot-mode.md`
## When the task is complete — suggest next skills

When you have **finished the user's request** for this skill (not after every tool call or subagent phase), suggest what to run next:

1. Run:

   ```bash
   python .agents/skills/heyeddi-orchestrator/scripts/suggest_next_skill.py --current-skill heyeddi-handoff --project-root .
   ```

   Add `--route /path` if you worked a specific route.

2. Include the script's **`### Next step`** block in your **final** reply. The user copies the **Prompt** line into chat (e.g. `@heyeddi-design craft /settings`).

Pass `--mode shape` (or `craft`, `audit`, etc.) when you know which sub-command just finished.

See `@heyeddi-orchestrator` → `reference/next-skill-handoff.md`.

