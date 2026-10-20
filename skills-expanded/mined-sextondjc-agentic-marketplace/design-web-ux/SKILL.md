---
name: design-web-ux
description: Use when defining or improving web application UX and you need a practical flow from user research through component specification and engineering handoff.
---

# Design Web UX

## Specialization

This skill is specialized for the workflow described in this file and should remain narrowly bounded to that responsibility.

It does not cover mobile UX (use `design-mobile-ux`), high-fidelity prototyping (use `prototype-mobile-ui`), or usability test scripting (use `usability-test-scripts`).

## Scope

Design and validate UX for web applications across desktop, tablet, and mobile breakpoints, from discovery through implementation-ready handoff artifacts.

## Required Outputs

- Problem statement, user goals, and prioritized experience risks.
- Task flows and low-to-mid fidelity wireframes for core and edge journeys.
- Responsive breakpoint specifications for desktop, tablet, and mobile.
- Accessibility and usability findings with concrete remediation.
- Implementation-ready handoff package with behavior specs and acceptance cues.

## Workflow

1. Define the target users, business goal, and success criteria for the feature or flow.
2. Gather evidence: analytics, support tickets, user sessions, and 5–8 interviews or usability reviews.
3. Map top tasks, current pain points, and journey assumptions to be validated.
4. Produce task flows and low-fidelity wireframes for primary, edge, and error states.
5. Define responsive behavior: layout shifts at each breakpoint, content priority changes, and touch vs. pointer interaction differences.
6. Apply web UX conventions: clear information hierarchy, consistent navigation patterns, and keyboard-navigable flows.
7. Evolve to mid-fidelity wireframes with content hierarchy, spacing intent, and interactive element sizing.
8. Run usability tests (5+ participants), capture severity-ranked findings, and iterate on critical and high issues.
9. Prepare handoff package: annotated wireframes, behavior specifications, accessibility annotations, acceptance cues, and instrumentation hooks.
10. Define success metrics and validation loop before implementation sign-off.

## Accessibility and Usability Heuristics

- Maintain WCAG 2.1 AA contrast ratios and readable typography at all breakpoints.
- Ensure keyboard navigability for all interactive elements with visible focus indicators.
- Keep navigation predictable; breadcrumb or progress cues for multi-step flows.
- Provide visible feedback for loading, success, error, and empty states.
- Support screen readers with meaningful landmark structure, labels, and announced state changes.
- Minimize cognitive load: one primary action per view and plain-language microcopy.

## Responsive and Adaptive Guidance

- Design for desktop-width viewport first, then define how layouts adapt to tablet and mobile breakpoints.
- Specify explicit breakpoints; do not rely on "it shrinks automatically."
- For mobile breakpoints, apply thumb-reach-aware placement for primary actions.
- Use progressive disclosure for complex forms and data-heavy views at narrow widths.
- Preserve feature parity across breakpoints unless a documented exception exists.

## Instrumentation and Validation

Track these metrics per key flow after launch:

- Task completion rate.
- Time on task.
- Error rate and recovery rate.
- Drop-off points by step.

## Handoff Checklist

Before routing to `web-frontend-engineer`:

- [ ] Annotated wireframes for all states (default, loading, error, empty, success).
- [ ] Behavior specifications for interactive elements and transitions.
- [ ] Responsive breakpoint notes for each layout section.
- [ ] Accessibility annotations: roles, labels, focus order, and state announcements.
- [ ] Acceptance cues for each acceptance scenario.
- [ ] Usability findings summary with severity ratings and dispositions.

