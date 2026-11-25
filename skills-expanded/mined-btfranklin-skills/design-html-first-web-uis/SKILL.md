---
name: design-html-first-web-uis
description: >-
  Design or implement an HTML-first web interface. Use native browser features, progressive enhancement, server-rendered updates, and minimal JavaScript. Do not use for visual design, framework architecture, games, or browser debugging.
---

# Design HTML-First Web UIs

## Workflow

1. Inspect the stack, templates, routes, form handling, JavaScript, CSS, browser targets, and repository guidance. Preserve established conventions.
2. Describe the interaction as links, forms, navigation, disclosure, selection, or transient UI before choosing an implementation.
3. Select the smallest native element that preserves server control and meaningful URLs. Use JavaScript only when HTML and CSS cannot provide the required behavior.
4. Define the baseline behavior without enhancement, then add optional native APIs, server-driven partial updates, or small scripts.
5. Implement the smallest complete change. Keep state in URLs, form controls, or server responses when these locations support the interaction. Do not keep a second copy of the same state in the client.
6. Validate keyboard use, focus, accessible names, error handling, history/navigation, no-JavaScript behavior, and relevant browser support.

## Decisions

- Prefer links for navigation and forms for state-changing requests.
- Prefer `details` and `summary`, `dialog`, and popover behavior when their semantics match the interaction. Do not use a native element when its semantics do not match the design.
- Use server-rendered pages or fragments for authoritative application state. Keep each user workflow usable without the enhancement layer. A full-page route can provide the fallback for a partial-update endpoint.
- Preserve normal HTTP behavior: validation errors, redirects, CSRF protection, idempotency expectations, and back/forward navigation.
- Use animations and view transitions only for presentation. Respect reduced-motion preferences. Do not require motion to complete a task.

## Verify Current Information

Verify current browser support and API syntax when they affect the result. Use MDN, WHATWG, and relevant framework documentation. Also verify accessibility behavior and framework integration when they affect the result. Record the source and check date in plans or reports. Do not present information from memory as current.

## Resource

Read [references/html-first-patterns.md](references/html-first-patterns.md) when selecting a native primitive, designing progressive enhancement, or preparing the validation matrix. Load it only when those details are needed.

## Output

Return a repository-specific patch or plan. Identify the semantic baseline, enhancement layer, required JavaScript, fallback behavior, accessibility decisions, and completed verification. Ask a question only when an unresolved product choice will change the implementation.
