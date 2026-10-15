---
name: harmony-usage-rules
description: Apply when auditing, critiquing, or checking Harmony compliance; when running accessibility checks; or when the user asks about Harmony do's and don'ts or usage rules. Use for design rules (accessibility, component usage, layout).
disable-model-invocation: false
---

# Harmony Usage Rules

Apply these rules when auditing, critiquing, or checking Harmony design system compliance.

## Where to find rules

**Option A — Harmony npm package (if installed):** Read `{harmonyRoot}/docs/RULES.md` from the installed Harmony package (e.g. `node_modules/@deltek/harmony-components/docs/RULES.md` or `node_modules/@deltek-sst/harmony-design-system/docs/RULES.md`).

**Option B — Integration kit sources (always available):** When no Harmony npm package is installed, derive rules from the kit's vendored files:

- **`harmony-styles/tokens.css`** — Design token definitions (colors, spacing, typography, radii, shadows)
- **`harmony-styles/components.css`** — Component-level styling rules and states
- **`harmony-styles/layout.css`** — Layout and shell rules
- **`reference-components/*.tsx`** — Read-only spec for component behavior, props, states, and accessibility attributes

Use these files to check:
- **Component usage:** Does the MUI/shadcn implementation match the expected Harmony component behavior defined in `reference-components/`?
- **Token usage:** Are Harmony tokens used correctly (not hardcoded hex, arbitrary px values, or non-token spacing)?
- **Accessibility:** Do components include required ARIA attributes, keyboard handling, and focus management as shown in `reference-components/`?
- **Layout:** Does the layout follow Harmony shell and composition rules from `layout.css` and `reference-components/ShellLayout.tsx`?

## Integration kit context

The host app uses **MUI or shadcn** components with the Harmony theme applied. When checking compliance:
- Verify host components use Harmony tokens through the theme (CSS vars, MUI theme overrides, or Tailwind extensions)
- Reference `reference-components/*.tsx` for expected behavior — these are read-only spec, not imported into the host app
- Check that the mapping playbook passes (1-8) have been correctly applied

## Scripts subfolder

The `scripts/` folder contains documentation about extracting rules from upstream Harmony doc pages (heading patterns, HTML structure). These are for maintainers updating the rule set from the full Harmony documentation site — not needed for day-to-day design critiques.
