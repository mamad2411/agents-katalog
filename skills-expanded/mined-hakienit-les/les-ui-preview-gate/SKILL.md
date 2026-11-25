---
name: les-ui-preview-gate
description: Gate frontend implementation behind user selection of preview options derived from Figma or wireframes, using the repository's existing design system and UI kit.
invocation: model
maturity: stable
route: frontend-preview
profile: frontend
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/architecture.md","../../policies/rules/change-scope.md","../../policies/rules/definition-of-done.md","../../profiles/frontend/rules/component-design.md","../../profiles/frontend/rules/state-management.md","../../profiles/frontend/rules/ui-completeness.md","../../profiles/frontend/rules/interaction-responsive.md","../../profiles/frontend/rules/visual-system.md","../../profiles/frontend/rules/browser-evidence.md","../../profiles/frontend/rules/frontend-verification.md","../../profiles/frontend/references/design-quality-bar.md"]
---

# UI Preview Gate

## Invoke

Bootstrap LES and require the frontend profile when a feature request includes
a Figma link, screenshot, or wireframe and asks for implementation.

## Inputs

The feature outcome, Figma or wireframe reference, repository design-system and
UI-kit locations, existing component seams, supported states/viewports, and any
available safe browser preview surface.

## Procedure

1. Inspect the reference, repository conventions, design tokens, UI kit, component seams, and relevant frontend states. Done when: the source, reuse boundary, and missing primitives are explicit.
2. Produce three to four preview options using existing components and record a short reuse map for each option. Done when: every option has an ID, source, component/pattern list, and known gaps.
3. Save the options and source/feedback metadata under the project gallery at `docs/ui-sandbox/`, then open the safe preview surface. Done when: every option is marked `Draft` and the preview evidence is available or explicitly `unavailable`.
4. Ask the user to select an option, answer a focused question, or give feedback. Done when: the response is captured or the task stops at `PENDING_USER_ACTION`.
5. Preserve prior rounds and create a new draft round for feedback; never overwrite the comparison history. Done when: the gallery retains the option lineage and current round is identifiable.
6. Mark the chosen option `Selected` and hand off to the normal implementation route. Done when: implementation is blocked until an explicit selection exists.
7. Mark the applied option `Implemented`, or `Superseded` when a later round replaces it. Done when: the gallery links the final option to implementation evidence and terminal status.

## Output

Preview-gate record containing source reference, option IDs, reuse maps, gallery
location, feedback rounds, selected/implemented status, preview evidence,
missing-primitives decisions, residual risk, and terminal status.

## Guardrails

Reuse existing components, variants, tokens, and patterns before proposing new
ones. If a required primitive is missing, ask the user for direction; do not
silently create a replacement. Do not implement before `Selected`, choose a
framework or library, publish, commit, push, or treat a screenshot as keyboard,
accessibility, responsive, browser, or implementation proof.

If the reference, design system, or safe preview surface is unavailable, report
the missing condition and stop before implementation.

## Verification

Verify that every option records its source and reuse map, every draft remains
recoverable, selection is explicit, and the final implementation evidence is
linked to one option. Keep visual, keyboard, accessibility, responsive,
performance, and browser evidence separate; report unavailable lanes without
promoting them to pass.
