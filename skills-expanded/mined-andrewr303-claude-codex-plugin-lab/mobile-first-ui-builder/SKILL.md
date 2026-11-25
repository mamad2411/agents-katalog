---
name: mobile-first-ui-builder
description: "Use to design and implement new mobile-first responsive UI from scratch, including layout, controls, states, interaction, accessibility, and visual polish."
---

# Mobile First UI Builder

Use this skill when creating a new page, app surface, component, prototype,
or feature that needs strong mobile and responsive UX.

## Required References

Read `../../references/design-system-and-tokens.md`,
`../../references/accessibility-touch.md`, and
`../../references/framework-playbooks.md`.

## Build Standards

- Inspect the existing app shell, primitives, token system, icon library,
  route patterns, and state-management approach before adding UI.
- Build the actual usable experience first. Avoid marketing-only shells
  unless the user requested a landing page.
- Prefer semantic controls: buttons for commands, links for navigation,
  inputs for values, toggles for binary settings, segmented controls for
  modes, tabs for peer views, menus for option sets, and sliders/steppers
  for bounded numeric values.
- Include non-happy paths: loading, empty, error, disabled, success,
  partial data, stale data, long text, and reduced motion.
- Keep layouts stable with grid/flex constraints, aspect ratios, minmax,
  container queries, and predictable wrapping.
- Use real visual assets when a website or app needs product/place/person
  context. Do not rely on decorative gradients or abstract blobs.
- Verify mobile, tablet, and desktop render before handoff.
