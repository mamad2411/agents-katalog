---
name: desktop-to-mobile-adaptation
description: "Use to convert desktop layouts, dashboards, forms, marketing pages, data tables, charts, and workflows into mobile-first responsive experiences without losing core task capability."
---

# Desktop To Mobile Adaptation

Use this skill when a desktop design or existing desktop page needs a
mobile version, responsive rewrite, or mobile-first refactor.

## Required References

Read `../../references/desktop-to-mobile-conversion.md`,
`../../references/mobile-repair-playbook.md`, and
`../../references/design-system-and-tokens.md`.

## Conversion Rules

- Preserve the user's core task, domain vocabulary, primary actions, and
  data meaning. Do not turn a product workflow into a generic landing page.
- Inventory desktop landmarks: navigation, filters, primary/secondary
  actions, tables, charts, forms, destructive actions, helper text, and
  status messages.
- Decide what becomes stacked content, tabs, segmented controls, accordions,
  bottom sheets, sticky action bars, carousels, data cards, or overflow menus.
- Keep desktop and mobile parity explicit. If a control is removed from
  mobile, document why and where the user can still complete that task.
- Use base mobile styles and progressive `sm:`, `md:`, `lg:` enhancements
  when the project uses Tailwind or CSS-first responsive patterns.
- Verify long labels, dense numbers, localization-length text, validation
  errors, keyboard open state, safe areas, and landscape orientation.

## Output

For a plan: provide a section-by-section mobile adaptation map. For a code
task: implement the mobile-first version and verify screenshots at phone
and desktop widths.
