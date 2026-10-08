---
name: refine-prototype-to-app
description: Critique a canonical UI prototype, refine the prototype first, then implement and verify the corresponding application UI against it. Use when a user wants a design critique followed by prototype updates and production parity, especially for iOS or SwiftUI routes with multiple states, sheets, alerts, dialogs, accessibility requirements, or platform-version constraints.
---

# Refine Prototype to App

Turn critique into a verified prototype-first implementation. Keep the existing product structure, copy, and behavior authoritative unless the user explicitly changes them.

## Preserve the Source of Truth

1. Read the nearest repository instructions and design documentation completely.
2. Check repository status before edits. Use the repository's required worktree workflow when the checkout is shared or dirty.
3. Locate and distinguish:
   - canonical prototype sources from generated output;
   - the prototype build or generation command;
   - the production route and its state owners;
   - authoritative copy, behavior, localizations, and deployment target;
   - screenshot, visual-regression, build, and test commands.
4. Edit canonical sources and regenerate derived artifacts. Never hand-edit generated prototype pages.

Do not assign meaning to a placeholder, unfinished control, or ambiguous action. Trace it to implementation, documentation, tests, tickets, or product copy. Ask the user only when the answer would materially change behavior and cannot be discovered.

## Inventory the Experience

Inspect the rendered prototype and the production route, not source code alone. Capture a baseline when visual tooling is available.

Create a compact parity ledger covering every applicable surface:

| Surface | Prototype | App | Behavior owner | Validation |
| --- | --- | --- | --- | --- |
| Default route | present/missing | present/missing | file or model | screenshot/test |
| Alternate states | list states | list states | fixture or state | screenshot/test |
| Sheets, alerts, dialogs | list each | list each | action or binding | interaction/test |
| Navigation and actions | destination/result | destination/result | router/service | interaction/test |

Consider loading, populated, empty, error, disabled, signed-in/out, free/paid, permissions, destructive confirmation, success, light/dark appearance, text scaling, localization, and compact/large layouts. Include only states that are applicable or already implied by the authoritative product behavior.

## Critique Before Editing

Invoke `$critique` for the scoped route or feature. Let it use `frontend-design` as required, but interpret its advice through the target platform and repository design system.

For native iOS work, use `mobile-ios-design` when available. Apple conventions outrank web-specific anti-pattern advice: system typography, semantic colors, grouped settings, standard controls, and SF Symbols are often the correct choice.

Convert the critique into a prioritized acceptance checklist:

- Record each priority issue and concrete fix.
- Record smaller observations that can be fixed without widening scope.
- Mark items that affect behavior or copy separately from visual refinements.
- Map every accepted observation to a prototype change, an app parity change, or an explicit reason it is out of scope.

Do not stop after producing the report when the user requested implementation.

## Refine the Prototype First

Make the smallest coherent set of prototype changes that resolves the accepted critique:

1. Preserve the existing information architecture, copy, and actions unless explicitly authorized otherwise.
2. Establish consistent hierarchy, spacing, color semantics, icon treatment, affordances, and component states.
3. Keep decorative color subordinate to meaning and interaction hierarchy.
4. Use semantic, accessible labels for interactive icons.
5. For iOS, select SF Symbols and APIs supported by the minimum deployment target. Verify availability instead of assuming it.
6. Update every applicable prototype state, sheet, alert, and dialog—not only the default screen.
7. Run the canonical prototype generator and inspect the rendered result.

If a proposed production implementation cannot faithfully express the refined design within platform constraints, correct the prototype first. Do not quietly diverge in the app.

## Validate the Refined Prototype

Render the affected route and its states. Check:

- the critique acceptance checklist;
- hierarchy and primary-action clarity;
- state and dialog coverage;
- light/dark appearance and meaningful color without color-only meaning;
- focus, labels, contrast, Dynamic Type or text scaling, and reduced-motion behavior where applicable;
- compact and large layouts relevant to the target platform.

Fix prototype defects before moving to production code.

## Implement Production Parity

Use the refined prototype as the visual and interaction contract while preserving the app's real data flow and behavior.

1. Reuse existing navigation, models, services, analytics, persistence, and action handlers.
2. Implement every applicable state and dialog from the parity ledger.
3. Keep controls semantically native and accessibility labels meaningful.
4. Respect the minimum platform target and avoid unsupported symbols or APIs.
5. Update all required localizations when user-visible copy changes.
6. Add or update focused behavioral and accessibility tests for meaningful changes.
7. Avoid broader redesigns, dependency changes, compatibility shims, and unrelated refactors.

## Close the Parity Loop

Run the smallest relevant tests during implementation, then the repository's required final checks.

After a UI change:

1. Generate the prescribed route screenshots or visual artifacts.
2. Compare prototype and app across every parity-ledger row.
3. Check layout, hierarchy, color roles, symbols, copy, states, dialogs, navigation, and accessibility semantics.
4. Fix every accepted critique observation and every unintended divergence.
5. Re-run affected tests and screenshots after the final correction.

Do not claim parity from compilation alone. If visual capture is impractical, state exactly what was verified and what remains unobserved.

## Finish

Report:

- prototype sources and generated artifacts changed;
- production files and behaviors changed;
- critique observations resolved or explicitly deferred;
- states and dialogs covered;
- tests, builds, and screenshot checks with results;
- known risks or unverified surfaces;
- branch, commit, and PR or artifact links when created.
