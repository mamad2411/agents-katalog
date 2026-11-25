---
name: impeccable-design
description: Apply frontend/UI design guardrails and the Impeccable anti-pattern checklist (pbakaus/impeccable) when building or reviewing visual UI — landing pages, dashboards, marketing sites, component styling. Use for design critique, polish passes, or before shipping new UI; pairs with vanilla-web/next-stack (implementation) rather than replacing them.
compatibility: >
  Cursor Agent Skills (Nightly channel + Agent Skills enabled in Settings → Rules).
  This skill is guidance-only (checklist + when-to-suggest-tooling); it does not vendor
  the Impeccable npm package. Per-project tooling install is opt-in — see Install below.
metadata:
  author: janjaszczak
  version: "1.0"
  upstream: https://github.com/pbakaus/impeccable
---

# Impeccable Design Guardrails

## Purpose
Every model trained on the same SaaS templates converges on the same tells: Inter for
everything, purple-to-blue gradients, cards nested in cards, gray text on colored
backgrounds, a rounded-square icon tile above every heading, bounce/elastic easing.
This skill encodes the Impeccable anti-pattern checklist so those tells get caught
during generation/review, without requiring the full CLI+hook toolchain to be installed
in every project.

## When to activate
- Building or editing visual UI: landing pages, marketing sites, dashboards, new
  components, design-system tokens.
- User asks for a design critique/polish/audit ("make this look better", "review the
  UX", "does this look AI-generated"), or explicitly names an Impeccable-style command
  (`audit`, `critique`, `polish`, `distill`, `harden`, `bolder`, `quieter`, `colorize`,
  `typeset`, `layout`, `animate`).
- Does **not** activate for backend-only, CLI, or non-visual work.

## Anti-patterns to catch (condensed from the 46 detector rules)
- **Typography:** default/overused fonts (Arial, unconfigured system fonts, Inter used
  everywhere with no intent); skipped heading levels; line length too long/short for
  body text.
- **Color:** purple-to-blue gradients as a default; gray text on colored backgrounds;
  pure black/white (`#000`/`#fff`) instead of tinted near-black/near-white; low-contrast
  text.
- **Layout/components:** cards nested inside cards; a rounded-square icon tile above
  every section heading; cramped padding; inconsistent spacing scale; small touch
  targets (<44px) on interactive elements.
- **Motion:** bounce/elastic easing (reads as dated); motion with no purpose.
- **Structure:** side-tab borders as a lazy nav pattern; dark glow shadows used
  decoratively rather than for elevation.

## Workflow
1. **Context first.** If the project has `DESIGN.md` or `PRODUCT.md` (from a real
   Impeccable install, or hand-written), read it for audience, brand lane, voice,
   color/type/component decisions — do not invent a design system from scratch when
   one already exists.
2. **Shape before build** for new UI: state the audience/lane (brand vs product
   surface), then propose layout/type/color before writing markup, mirroring
   `/impeccable shape`.
3. **Build** using the active stack skill (`vanilla-web`, `next-stack`, etc.) — this
   skill supplies the design lens, not the implementation mechanics.
4. **Self-review against the checklist above** before marking UI work done — this
   replaces `/impeccable audit`/`critique`/`polish` when the CLI isn't installed.
5. **Harden**: error/empty/loading states, text overflow, i18n-safe spacing, responsive
   behavior — mirrors `/impeccable harden`.

## Install (opt-in, per project — do not run without asking)
Impeccable's own CLI adds a live browser-iteration mode, 46 *deterministic* (no-LLM)
detector rules, and a Cursor-native hook that blocks bad writes before they land
(`.cursor/hooks.json` → `.cursor/skills/impeccable/scripts/hook-before-edit.mjs`).
Suggest this when a project does sustained frontend work and the user wants automated
enforcement, not just review-time guidance:

```bash
npx impeccable install        # detects .cursor/.claude/.codex etc.; asks project vs global scope
/impeccable init               # inside the AI tool: writes PRODUCT.md / DESIGN.md
```

Requirements specific to Cursor: Nightly channel (Settings → Beta) and Agent Skills
enabled (Settings → Rules) — Cursor's stable channel does not run Agent Skills yet.
Confirm with the user before running `npx impeccable install` (network + writes
`.cursor/hooks.json`, `.cursor/skills/impeccable/`); this is a per-project decision,
not something to vendor into the global config repo.

## Output contract
- For review/critique: a findings list grouped by the anti-pattern categories above,
  each with file/selector and a concrete fix (not just "improve this").
- For new UI: the design rationale (audience, lane, key decisions) alongside the code.
- Do not claim a `/impeccable <command>` ran unless the CLI is actually installed in
  the project — otherwise say "checklist applied manually" instead.
