---
name: design-system-conformance
description: Check a UI surface against the project's design system — tokens, components, patterns; flag bespoke values that should be tokens.
---

# design-system-conformance

> Walk a UI surface against the project's design system. Output is per-deviation findings: what bespoke value should become a token, or which off-system component should be replaced.

## When to use

- A new screen is being built and the team wants to keep design drift down.
- A design system audit reveals "we have 14 shades of gray". Pull this skill on the worst-offender screens first.

## Inputs

- The UI surface (route, component path, or screenshot + computed styles).
- The design system reference (tokens / components / patterns). If the project has none, surface that and stop — drift can't be measured against nothing.

## Procedure

1. **Tokens**: scan for any hardcoded `color`, `font-size`, `font-family`, `font-weight`, `line-height`, `border-radius`, `box-shadow`, `spacing` (margin/padding). Each hardcoded value is a finding unless it's documented as an exception.
2. **Components**: scan for native `<button>`, `<input>`, `<select>`, `<a>` styled bespoke. If the design system ships a `<Button>` component, the page should use it.
3. **Patterns**: density (table row height, list spacing), modal patterns, form patterns. A novel modal pattern on this one screen is almost always wrong.
4. **Iconography**: icons match the system's set + size + stroke weight. A new icon should join the system, not live on one screen.
5. **Spacing scale**: every margin/padding pulls from the spacing scale (e.g. 4 / 8 / 12 / 16 / 24 / 32). `padding: 13px` is a finding — pick 12 or 16.
6. **Per finding**: name the element, the bespoke value, and the system value it should map to.

## Output

```text
Design-system conformance: <surface>

Tokens (out-of-system):
  - .price color: #2D5BFF        → use `color.brand.500` (#2563EB).
                                    Note: bespoke value is darker than
                                    the token; if intentional, ask the
                                    DS team to add `color.brand.600`.
  - .card padding: 13px 14px     → use `space.3 space.4` (12px 16px).
  - .header font-size: 22px      → use `text.lg` (20px) or `text.xl` (24px).
                                    Picking 22 splits the scale.

Components (bespoke instead of system):
  - .my-button is a styled <a>. Replace with <Button variant="primary">
    from @example/ds.
  - .my-modal: bespoke modal pattern. Use <Modal> from the system; if
    a needed feature is missing, file an issue against the DS, don't
    inline a new one.

Patterns:
  - Form labels are placeholders, not labels. DS rule + WCAG. Move to
    real labels above the field.

Iconography:
  - .icon-trash is a stroke-weight-1 icon imported from Heroicons. DS
    set is stroke-weight-1.5 from Lucide. Replace.

Spacing scale violations: 4 elements use values off the scale (13, 14,
22, 33). All should snap to the nearest scale value.
```

## Quality bar

- Every finding cites the element + the bespoke value + the system value it should map to.
- If the system doesn't have a value to map to, that's a missing-token finding for the design system team — name it.
- Spacing scale check always run; off-scale values are a common drift source.
- Don't approve "we'll fix it later" without a tracked issue.

## Anti-patterns to avoid

- "Looks fine" without running the token scan.
- Adding bespoke values to "match the system spirit". Either it's in the system or it's a missing-token issue.
- Letting one screen invent a new pattern that other screens will copy.
- Migrating off the design system because "the components don't fit". Almost always cheaper to extend the system.
