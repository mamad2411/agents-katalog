---
name: code-review-nextjs
description: Review code for quality, security, accessibility, and best practices in Next.js and TypeScript projects. Use when the user asks for a code review, review of a PR, or feedback on code changes. Triggers on "revisar código", "code review", "revisión", "PR review", or when examining diffs and pull requests.
---

# Code Review (Next.js & TypeScript)

Structured code review for Next.js App Router and TypeScript. Apply when reviewing pull requests, single files, or when the user explicitly asks for a code review.

## When to Apply

- User asks for "code review", "revisar código", "revisión", "revisar este PR", or similar
- User shares a diff, file, or PR and wants feedback
- User asks "¿qué mejorarías?" or "is this correct?" about their code

## Review Checklist

Go through these areas and report findings. Mark each item as checked or with issues.

### Correctness & logic

- [ ] Logic is correct and handles edge cases (empty lists, null, undefined)
- [ ] No obvious bugs or off-by-one errors
- [ ] Async/await and Promises are used correctly; no unhandled rejections
- [ ] Loading and error states are handled (especially in UI)
- [ ] Forms: validation, submission, and error feedback are clear

### Next.js (App Router)

- [ ] Server Components by default; "use client" only when needed (hooks, events, browser APIs)
- [ ] File conventions: page.tsx, layout.tsx, loading.tsx, error.tsx where appropriate
- [ ] Data fetching: prefer server-side in Server Components; avoid unnecessary client fetch when data can be passed as props
- [ ] Route handlers and API routes: correct HTTP methods and status codes
- [ ] No sensitive data or secrets in client bundles
- [ ] Metadata (title, description) set for SEO where relevant

### TypeScript

- [ ] No `any`; use proper types or `unknown` with type guards
- [ ] Props and data structures have interfaces or types
- [ ] Strict null checks respected (optional chaining, nullish coalescing where needed)
- [ ] Generics used correctly when applicable
- [ ] Exported types/interfaces when used across modules

### Security

- [ ] No SQL injection (parameterized queries, Prisma, etc.)
- [ ] User input sanitized; no raw HTML injection (XSS)
- [ ] Auth/authorization checked where required (server actions, API routes, protected pages)
- [ ] No secrets or tokens in frontend code or logs
- [ ] CSRF considered for state-changing requests where applicable

### Accessibility (a11y)

- [ ] **Semantic HTML**: Use correct elements (nav, main, article, button, a, heading levels) instead of div/span for everything
- [ ] **Images**: All meaningful images have descriptive `alt` text; decorative images use `alt=""` or `role="presentation"`
- [ ] **Forms**: Labels associated with inputs (via `htmlFor`/`id` or wrapping); required fields and errors announced
- [ ] **Keyboard**: All interactive elements focusable and operable with keyboard; no keyboard traps; focus order is logical
- [ ] **Focus**: Visible focus indicator (outline/focus-visible); focus moved appropriately after modals/dialogs open or close
- [ ] **ARIA**: Use ARIA only when HTML semantics are insufficient (e.g. aria-label, aria-expanded, aria-live for dynamic content); avoid redundant or wrong ARIA
- [ ] **Color**: Color not the only way to convey information; sufficient contrast for text (WCAG AA minimum)
- [ ] **Motion**: Respect `prefers-reduced-motion` for animations where possible
- [ ] **Links vs buttons**: Links for navigation (href); buttons for actions; do not use div/span with onClick for interactive elements without proper role and keyboard support

### Maintainability & style

- [ ] Functions and components are focused and reasonably small
- [ ] Naming is clear (PascalCase components, camelCase functions/variables, UPPER_SNAKE for constants)
- [ ] No duplicated logic that could be extracted (DRY)
- [ ] Error handling is explicit and helpful (messages, logging where appropriate)
- [ ] No dead code or commented-out blocks that should be removed
- [ ] Imports organized; no unused imports

### Performance (high level)

- [ ] No obvious N+1 or unnecessary re-fetches
- [ ] Heavy or route-specific UI consider dynamic import (next/dynamic) where it helps
- [ ] Large lists consider virtualization or pagination if they impact performance

For detailed React/Next.js performance rules, use the vercel-react-best-practices skill when relevant.

### Tests (if applicable)

- [ ] Critical paths or complex logic have tests
- [ ] Tests are meaningful (behavior, not only implementation details)
- [ ] No flaky tests (e.g. time-dependent or order-dependent without control)

### Dependencies & environment

- [ ] New dependencies are justified and not redundant with existing ones
- [ ] Environment variables used for config/secrets; no hardcoded secrets
- [ ] No deprecated APIs used without a migration plan

## Feedback Format

Structure feedback as:

- **Critical**: Must fix before merge (bugs, security, broken behavior, serious a11y blockers)
- **Suggestion**: Should improve (readability, performance, patterns, accessibility improvements)
- **Nice to have**: Optional (style, minor refactors, extra tests)

Keep feedback actionable: say what is wrong and, when possible, how to fix it. For accessibility issues, suggest the correct pattern (e.g. "Use `<button>` instead of `<div onClick>`" or "Add `aria-live` for the success message").

## Optional: Performance (Next.js/React)

If the change touches rendering or data fetching, also consider:

- Avoiding unnecessary client components and "use client" boundaries
- Using React cache, parallel fetching, or streaming where it helps
- Not over-bundling (dynamic imports for heavy or route-specific code)

Reference the vercel-react-best-practices skill for detailed performance rules when relevant.
