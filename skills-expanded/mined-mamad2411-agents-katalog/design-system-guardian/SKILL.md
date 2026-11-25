---
name: design-system-guardian
description: Preserve and improve visual consistency when designing, implementing, reviewing, or refactoring user interfaces. Use for frontend components, pages, responsive layouts, typography, color, spacing, motion, interaction states, and accessibility where Codex should reuse existing tokens and patterns, detect accidental divergence, and avoid unnecessary one-off styles or broad redesigns.
---

# Design System Guardian

Keep UI changes consistent with the product's existing visual language while meeting the
requested behavior and accessibility requirements.

## Audit before editing

1. Read repository instructions and identify the relevant framework and styling approach.
2. Inspect adjacent components, shared primitives, global styles, tokens, breakpoints, and
   existing interaction states.
3. Determine whether a documented design system exists. Treat repeated implementation
   patterns as evidence, not automatically as intentional standards.
4. Restate the requested UI behavior and the smallest component boundary that owns it.

Do not infer a new visual direction from a single isolated component.

## Choose the implementation

- Reuse an existing component or token when its semantics match.
- Prefer semantic tokens over raw values when the codebase supports them.
- Add a shared token or primitive only when the current change demonstrates real reuse or
  removes meaningful duplication.
- Keep component variants explicit and limited to supported product needs.
- Follow established responsive, focus, hover, active, disabled, loading, empty, and error
  patterns.
- Preserve content hierarchy and readability before adding visual novelty.
- Avoid one-off spacing, arbitrary breakpoints, duplicated keyframes, and near-identical
  component copies.
- Do not perform a broad redesign unless the user requests it.

## Apply durable user decisions

- Treat the user's latest explicit statement about a core visual rule as authoritative.
- When it conflicts with an older rule in this skill, replace the older rule instead of
  retaining both or adding an exception.
- Keep the rule semantic and concise so it applies to future implementations.
- Update affected repository tokens, shared primitives, and documentation in the same task
  when they are available.
- Current button geometry: all native buttons and link-based button controls use square
  corners with zero border radius.
- Current case-study hierarchy: primary chapter H2s use the shared
  `--case-study-section-heading` token; project-specific evidence may vary without
  increasing that reading-level title scale.
- Current global-navigation behavior: the fixed header hides only on deliberate
  downward scrolling, returns on upward scrolling, and stays visible for an open
  mobile menu or keyboard focus within the header.

## Protect accessibility and motion

- Preserve semantic HTML and logical heading order.
- Ensure interactive controls have accessible names and keyboard behavior.
- Keep focus visible and state changes perceivable without relying only on color.
- Check text contrast, touch targets, zoom behavior, overflow, and content reflow.
- Respect reduced-motion preferences and avoid motion that blocks interaction.
- Keep decorative media out of the accessibility tree and give meaningful media useful text
  alternatives.

## Inspect the rendered result

Use the project's normal preview or browser workflow.

1. Check representative desktop and mobile widths.
2. Inspect long, short, translated, empty, and dynamic content where relevant.
3. Exercise keyboard interaction and all changed states.
4. Check browser console and network failures.
5. Compare the result with adjacent pages and components, not only the design in isolation.

Run repository-native lint, type-check, tests, and build checks proportional to the change.

Apply the focused companion skills when relevant:

- Use `$align-card-grids` for repeated cards, tiles, features, process steps, results, or proof
  panels with variable-length content.
- Use `$author-section-headings` for deliberate line counts, centered headings, eyebrow
  geometry, or localized title wrapping.
- Use `$verify-rendered-ui` as the completion gate for all visual frontend changes.

## Run the consistency gate

Before finishing, inspect the diff:

- Did the change introduce a raw value where a valid token exists?
- Is a new component duplicating an existing primitive?
- Are spacing, typography, radius, color, shadow, and motion consistent with nearby UI?
- Does the component work across supported breakpoints and content lengths?
- Do comparable card title and body coordinates align with short, long, and translated copy?
- Are exact heading line counts authored rather than left to incidental browser wrapping?
- Was the changed UI inspected after rendering rather than approved from source alone?
- Are interaction and accessibility states complete?
- Did obsolete styles, props, or variants remain?
- Is any design-system change documented where the repository expects documentation?

Fix divergence caused by the change when it is local and proportionate. Report pre-existing
inconsistency separately rather than silently expanding scope.

## Report completion

Summarize the reused patterns or tokens, any justified additions, rendered checks, automated
verification, and remaining visual or accessibility risks.
