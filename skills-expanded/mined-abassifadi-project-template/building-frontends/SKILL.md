---
name: building-frontends
description: Builds web and mobile user interfaces that are accessible (WCAG 2.2 AA), fast (Core Web Vitals), and maintainable — component structure, state management, forms and validation, API integration, error and loading states, and UI testing. Use when creating or changing screens, components, forms, or client-side logic.
---

# Building frontends

## Structure

- Organize by feature (`features/checkout/…`), with shared UI pieces in `components/`.
- Keep presentational components (they take props and render) separate from data-fetching and state logic, using hooks, services, or stores.
- Use one source of truth for each piece of state:

| Kind of state | Where it lives |
|---------------|----------------|
| Server data | A data-fetching cache such as TanStack Query or SWR, or the framework's loader |
| URL state (filters, page, selected tab) | The URL |
| Form state | A form library or local state |
| Cross-cutting client state (theme, current user) | A small global store or context |

- Don't copy server data into a global store.
- Generate API types and clients from the API contract (OpenAPI) when possible, so the frontend and backend can't drift apart.

## Every screen handles four states

**Loading, empty, error, and success.** Error states tell the user what happened and what they can do about it. Never show a blank screen or a raw stack trace.

## Forms

- Validate on the client to give quick feedback.
- **Always validate on the server too.**
- Show errors next to the field they belong to, and move focus to the first error.
- Disable submit while a request is in flight, and prevent double submission.

## Accessibility (WCAG 2.2 AA)

- Use semantic HTML first (`button`, `nav`, `main`, `label`). Add ARIA only when no native element does the job.
- Everything must be usable with the keyboard alone, with a visible focus indicator and a logical tab order.
- Text contrast must be at least 4.5:1. Never use color as the only way to convey meaning.
- Every input has a label, and every meaningful image has alt text.
- Respect `prefers-reduced-motion`.
- Check with automated tools (axe, Lighthouse) **and** a manual keyboard pass.

## Performance (Core Web Vitals)

Targets, measured at the 75th percentile of real users:
- LCP (Largest Contentful Paint) < 2.5 s
- INP (Interaction to Next Paint) < 200 ms
- CLS (Cumulative Layout Shift) < 0.1

How to get there:
- Split code by route.
- Lazy-load anything below the fold.
- Size and compress images, and set their dimensions.
- Avoid layout shifts.
- Cache static assets.

## Testing

- Component tests (Testing Library style) check what the user sees and does, not implementation details.
- Add a few end-to-end tests (Playwright or Cypress) for the critical user journeys in the spec.
- Mock the network at the boundary (for example with MSW), not inside components.

## Security

- Never inject user content with `innerHTML` / `dangerouslySetInnerHTML`.
- Keep tokens in `HttpOnly` cookies rather than `localStorage` when you can.
- Treat every client-side check as a convenience only. The server enforces the rules.
