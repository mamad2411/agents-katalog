---
name: build-web-frontend
description: Use when implementing or reviewing web frontend components, pages, and API integrations and you need a repeatable workflow for architecture, accessibility, performance, security, and testing.
---

# Build Web Frontend

## Specialization

Provide a repeatable, standards-aligned workflow for delivering production-grade web frontend features across any modern component-based framework (React, Vue, Angular, Svelte, or similar).

## When to Use

- Implementing a new web page, component, or user flow.
- Reviewing an existing frontend implementation against quality standards.
- Diagnosing frontend architecture, performance, accessibility, or security gaps.
- Preparing a frontend feature for production deployment.

## When Not to Use

- UX research and wireframe design (use `design-web-ux`).
- Backend or API implementation (route to `csharp-engineer`).
- Global coding policy enforcement across the repository (use `web-frontend.instructions.md`).

## Required Outputs

| Output | Description |
|---|---|
| Component implementation | All components built to UX spec with co-located tests |
| Test coverage | Unit tests for logic-bearing components/hooks; integration tests for key user flows |
| Accessibility audit result | Zero critical/serious axe violations; keyboard navigation and screen reader verified |
| Core Web Vitals baseline | LCP, CLS, INP measured and within targets; bundle size delta reviewed |
| Security review sign-off | CSP, token storage, input encoding, and third-party script integrity confirmed |
| Readiness summary | Open risks, deferred items, and next improvement actions documented |

## Depth Modes

| Level | Intent | Stop Rule |
|---|---|---|
| L1 Orientation | Understand component structure | Produce a working component with props, state, and one test |
| L2 Practical Delivery | Ship one feature safely | Deliver a complete feature with route, components, API integration, tests, and accessibility checks |
| L3 Specialist Hardening | Improve quality and resilience | Demonstrate measured Core Web Vitals improvement, full WCAG 2.1 AA audit pass, and security review sign-off |
| L4 Expert Standardization | Define reusable team standards | Produce reusable component patterns, testing templates, and a governance baseline for repeated delivery |

## Workflow

1. Define outcome, target users, UX handoff artifacts, and selected depth mode.
2. Establish component architecture: identify shared components, co-location strategy, and state boundaries.
3. Implement routing and layout structure; verify keyboard navigation and focus management at this stage.
4. Build components against UX specifications; annotate ARIA roles and labels as part of implementation, not post-hoc.
5. Connect to API or data layer using the approved service or hook abstraction; validate response schemas before consumption.
6. Add test coverage: unit tests for logic-bearing components and hooks, integration tests for key user flows.
7. Run accessibility audit (axe or equivalent); resolve all critical and serious violations before merge.
8. Measure Core Web Vitals in a production-like environment; address regressions before merge.
9. Apply security review checklist: CSP configuration, token storage, input sanitization, and no unsafe DOM injection.
10. Produce a short readiness summary with open risks, deferred items, and next improvements.

## Component Quality Checklist

- [ ] One component per file with co-located tests.
- [ ] No `any` types in props or state interfaces.
- [ ] No inline styles; design-token-aware styling in use.
- [ ] All images have descriptive `alt` text or `alt=""` for decorative images.
- [ ] All interactive elements are keyboard-accessible and have visible focus indicators.
- [ ] No `eval()`, `new Function()`, or unsafe DOM injection.
- [ ] No authentication tokens in `localStorage`.
- [ ] API response shapes validated before consumption.

## Accessibility Audit Checkpoints

Run at L2 and above before marking work complete:

- Automated scan with axe-core or equivalent; zero critical or serious violations.
- Manual keyboard navigation: tab order, focus trap in modals, skip-link availability.
- Screen reader spot-check on primary flow (VoiceOver or NVDA).
- Color contrast verified at all text and icon sizes.

## Performance Baseline

Measure before and after significant changes:

- LCP (Largest Contentful Paint): target ≤ 2.5 s.
- CLS (Cumulative Layout Shift): target ≤ 0.1.
- INP (Interaction to Next Paint): target ≤ 200 ms.
- Bundle size delta: flag increases greater than 10 KB (gzipped) for review.

## Security Checklist

- [ ] Content Security Policy is defined; `unsafe-inline` and `unsafe-eval` are absent or explicitly justified.
- [ ] Authentication tokens stored in `HttpOnly` cookies or in-memory only.
- [ ] All user-controlled input is encoded before rendering in DOM or URL contexts.
- [ ] No hardcoded credentials, API keys, or environment URLs in source.
- [ ] Third-party scripts are integrity-checked (SRI hashes).
