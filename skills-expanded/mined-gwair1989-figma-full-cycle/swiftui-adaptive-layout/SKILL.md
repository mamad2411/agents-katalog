---
name: swiftui-adaptive-layout
description: 'Use when implementing, refactoring or reviewing adaptive SwiftUI layout: flexible containers, frames, alignment, padding, safe areas, keyboard dismissal, tab bar visibility during push navigation, backgrounds, decorative overflow and single-flow pagers with shared stationary elements. Works from project requirements, code or a design, without requiring Figma or a pipeline. Not a replacement for a full device-matrix adaptivity check.'
---

# SwiftUI Adaptive Layout

Build and review native flexible SwiftUI layout using the canonical
[layout rules](references/layout-rules.md), including LAY-01…LAY-13, keyboard dismissal,
tab bar visibility during push navigation and single-flow pagers.
Read those rules in full before implementation or layout review. For specification-only work,
read the relevant rule without starting implementation.

## Scope and inputs

Accept the project/screens, relevant code or design, and the requested implementation, refactor
or review. Figma, an MCP server, another skill, a pipeline manifest and a UI Plan are optional.
The complete skill is this directory; copying it alone preserves its rules and references.

Keep the project's resolved architecture, typography, colors, localization and Accessibility
scope. This skill owns layout decisions; it does not select an architecture, introduce a design
system or expand Accessibility requirements. Review requests produce findings; change code when
the user or caller has authorized implementation or fixes.

A caller requesting selected rules or review of supplied captures keeps its own evidence mode and
coverage scope. Apply those rules and return findings; do not start an additional matrix audit or
runtime walkthrough outside that scope. Unobserved motion remains unverified.

## Workflow

1. Resolve layout constraints from applicable project instructions, architecture/design-system
   documentation and the brief: supported devices/orientations, screen bounds, safe areas, any
   design reference canvas, spacing/scaling APIs and forbidden patterns. Documentation outranks
   legacy call sites. Use existing code only for undocumented details and mark that provenance;
   ask about contradictory rules or an architectural decision the change actually requires.
   Without a design, use documented component sizes and relational requirements; no Figma access
   or invented reference canvas is needed.
2. Separate screen containers, shared chrome, content and decoration. Describe parent/child
   relations and intended edge insets. For screens with editable text, plan how the keyboard
   dismisses using [Keyboard dismissal](references/layout-rules.md#keyboard-dismissal).
   For pushes from a tab root, apply [Tab bar visibility](references/layout-rules.md#tab-bar-visibility-on-push-and-pop).
   If page indicators identify pages of one flow, apply
   **Single-flow pagers**: record page order, stable/changing regions, inputs and animation.
3. Implement or review against LAY-01…LAY-13. Prefer flexible frames, alignment and padding;
   bound decorative overflow locally and keep backgrounds independent of content safe areas.
   Preserve the existing state owner. For paging, try standard platform controls first and
   resolve the documented custom-animation question before building a custom pager.
4. Verify the changed scope with the project's available build and preview/runtime routes.
   Follow LAY-11 for required previews, native-device coverage and edge measurements. A project
   or caller-supplied layout guard can support source review; this skill bundles no scripts and
   its operation does not depend on one. Record what each tool actually checked and manually
   inspect uncovered rules. Exercise pager inputs, keyboard dismissal and tab bar transitions
   in the running app when implemented or requested for interaction review.
5. Return changes or findings, resolved constraints/deviations, verification evidence and missing
   coverage in the user's language. A standalone invocation needs no generated spec, UI Plan,
   manifest, report file, branch or commit. Save a report only when requested. In pipeline mode,
   return evidence to the caller and let it update its own manifest and stage state.

## Completion

- Layout follows the resolved project constraints and the applicable rules; deviations have an
  explicit source and reason.
- A single-flow pager has one selection value, stable shared elements and the recorded inputs
  and content animation. Completion and external navigation follow product requirements.
- Verification claims name actual commands/captures and their results. Missing build/runtime
  access or required configurations remain explicit coverage gaps, not passing checks.

For a full configuration-matrix audit, use the separately installed `swiftui-adaptivity-check`
when available, or the project's validation workflow. It is not required to invoke this skill.
When called by a validator, return evidence to it instead of invoking it recursively.
