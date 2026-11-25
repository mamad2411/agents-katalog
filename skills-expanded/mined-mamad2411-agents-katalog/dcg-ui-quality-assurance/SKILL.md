---
name: dcg-ui-quality-assurance
description: Audit or improve a DCG Smart web interface for accessibility, motion performance, visual consistency, loading states, and Thai user-visible copy. Use when building or reviewing landing pages, login, forms, menus, dashboards, dialogs, errors, empty states, or PWA behavior.
---

# DCG UI quality assurance

Apply this after `dcg-ui-ux-system`; it strengthens quality without replacing the DCG brand or a system's approved product accent.

1. Start with the current route, rendered UI, `docs/dcg-brand-system.md`, and the app's existing primitives. Do not infer a shared component merely from repeated code.
2. Keep all human-visible copy in Thai. Preserve only approved brand names such as `DCG Smart` and the product name in English.
3. Prefer native HTML elements and existing accessible primitives. Give every icon-only control an accessible Thai name; keep keyboard focus visible; connect field errors to their fields; use an announcement for critical errors and loading.
4. Provide a structural loading state, one clear empty-state action, local actionable errors, permission-denied state, offline/retry state, and success feedback where appropriate.
5. Keep motion optional and brief. Animate only `transform` or `opacity`; respect reduced-motion; never run an endless animation off-screen; do not animate large blur, layout, or full-screen surfaces.
6. Reuse the approved DCG brand asset and one icon family per release. Do not add a local logo, emoji, arbitrary gradient, or a second primitive library. The DCG infinity master is an approved brand exception to a generic no-gradient rule.
7. For a review, report only findings supported by: a governing DCG/app rule, a trace to the rendered route, and one deterministic correction. Do not turn unproven taste into a mandatory finding.
8. Make minimal changes. Do not alter backend behavior, authentication policy, dependencies, or production configuration as part of a visual-quality task.

Run the relevant Playwright checks from `docs/quality/playwright-standard.md` before a TEST release. Use `dcg-playwright-e2e` for browser automation.

External practice source: `ibelick/ui-skills` (MIT), used selectively for accessibility, motion, and evidence-based UI review. Do not apply its stack-specific or brand-conflicting rules without checking DCG standards.
