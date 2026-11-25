---
name: build-blazor-web-apps
description: Use when implementing or reviewing Blazor web applications (.NET Client, Server, or MAUI Hybrid) and you need a repeatable workflow for component architecture, performance, accessibility, security, and testing.
---

# Build Blazor Web Apps

## Specialization

Provide a repeatable, standards-aligned workflow for delivering production-grade Blazor applications across Client-side, Server-side, and MAUI Hybrid hosting models with emphasis on .NET-idiomatic patterns, performance optimization, and accessible component design.

## When to Use

- Implementing new Blazor pages, components, or user flows.
- Reviewing an existing Blazor application against quality standards.
- Diagnosing Blazor architecture, performance, accessibility, or security gaps.
- Preparing a Blazor feature for production deployment.
- Migrating from one Blazor hosting model to another with quality guardrails.

## When Not to Use

- UX research and wireframe design (use `design-web-ux`).
- Mobile app implementation with MAUI (use `build-maui-apps` for MAUI native Android and iOS targets).
- Backend API or service implementation (route to `csharp-engineer`).
- Global Blazor policy enforcement (use instruction files in `.github/instructions`).

## Required Outputs

| Output | Description |
|---|---|
| Component implementation | All Blazor components built to UX spec with co-located tests |
| Interop validation | JavaScript interop call sites validated for nullability and error handling |
| Test coverage | Unit tests for component logic and parameter binding; integration tests for key user flows |
| Accessibility audit result | Zero critical/serious axe violations; keyboard navigation, focus management, and screen reader verified |
| Performance baseline | Metrics for Initial Load, Interaction (FID/INP), and CLS measured; bundle size deltas reviewed |
| Security review sign-off | Authorization guards, sensitive data handling, JS interop safety, and CSRF validation confirmed |
| Readiness summary | Open risks, deferred items, hosting model compatibility notes, and next improvement actions documented |

## Depth Modes

| Level | Intent | Stop Rule |
|---|---|---|
| L1 Orientation | Understand component structure | Produce a working Blazor component with @parameters, lifecycle, and one test |
| L2 Practical Delivery | Ship one feature safely | Deliver a complete feature with page routing, components, data binding, API integration, tests, and accessibility checks |
| L3 Specialist Hardening | Improve quality and resilience | Demonstrate performance baselines, full WCAG 2.1 AA audit pass, exhaustive error handling, and security review sign-off |
| L4 Expert Standardization | Define reusable team standards | Produce reusable component patterns, testing templates, hosting model patterns, and a governance baseline for repeated delivery |

## Hosting Model Selection

Choose one based on your constraints:

| Model | Use When | Considerations |
|---|---|---|
| **Blazor WebAssembly (Client-side)** | You need zero-dependency deployment, offline capability, or reduced server load. | Bundle size optimization critical; no direct database access; slower initial load. |
| **Blazor Server** | You need real-time interactivity, frequent state synchronization, or tight backend coupling. | Requires persistent WebSocket connection; not suitable for high-latency or connection-unstable environments. |
| **MAUI Hybrid** | You're building a desktop or hybrid app and want Blazor for UI. | Platform-specific packaging; platform-specific security considerations. |

## Workflow

1. Define outcome, target users, UX handoff artifacts, hosting model, and selected depth mode.
2. Establish component architecture: identify shared components, layout strategy, cascading parameters, and state boundaries.
3. Implement routing, navigation, and layout structure; verify keyboard navigation and focus management at this stage.
4. Build components against UX spec, annotate ARIA roles and labels, and define `@parameters` for clear contracts.
5. Bind form data, events, and two-way binding (@bind); validate input using `EditForm` and `DataAnnotationsValidator`.
6. Connect to API or data layer using dependency-injected service abstractions; validate response shapes before consumption.
7. For JavaScript interop: use JSInterop in a guarded wrapper, validate null responses, and handle JS errors gracefully.
8. Add test coverage: unit tests for component logic, parameter validation, and event handling; integration tests for key user flows.
9. Run accessibility audit (axe or equivalent); resolve all critical and serious violations before merge.
10. Measure performance in a production-like environment; address regressions before merge.
11. Apply security review checklist: authorization guards, sensitive data handling, JS interop safety, CSRF token validation.
12. Produce a short readiness summary with open risks, deferred items, and next improvements.

## Component Quality Checklist

- [ ] One component per file with co-located tests.
- [ ] All `@parameters` are explicitly documented with `/// <summary>` XML doc comments.
- [ ] No `null!` suppression operators; use proper nullability annotation.
- [ ] No hardcoded sensitive data or secrets.
- [ ] Cascading parameters used for UI state that affects child components.
- [ ] Event handlers defined as private methods with clear naming (`OnButtonClick`, `OnInputChange`).
- [ ] All interactive elements have keyboard support and visible focus indicators.
- [ ] All images have descriptive `alt` text or `alt=""` for decorative images.
- [ ] ARIA roles and labels annotated for custom components.
- [ ] No `@onclick` or `@onchange` without error boundary or try-catch when calling async methods.

## Accessibility Audit Checkpoints

Run at L2 and above before marking work complete:

- Automated scan with axe-core or equivalent; zero critical or serious violations.
- Manual keyboard navigation: tab order, focus trap in modals, skip-link availability.
- Screen reader spot-check on primary flow (NVDA or VoiceOver).
- Color contrast verified at all text and icon sizes.
- Form labels properly associated with inputs (no placeholder-only pattern).

## Performance Baseline

Measure before and after significant changes (adjustments for hosting model):

| Metric | Client-side Target | Server-side Target |
|---|---|---|
| **Initial Load** | ≤ 3.5 s (WASM download + JIT) | ≤ 2.5 s |
| **CLS (Cumulative Layout Shift)** | ≤ 0.1 | ≤ 0.1 |
| **INP (Interaction to Next Paint)** | ≤ 200 ms | ≤ 200 ms |
| **Bundle Size** | Flag increases > 50 KB (gzipped WASM) | Flag increases > 10 KB (gzipped JS) |

## JavaScript Interop Checklist

- [ ] All JSInterop calls wrapped in try-catch or error boundaries.
- [ ] Null-coalescing operators used for JS return values (`result ?? defaultValue`).
- [ ] JavaScript methods validated to exist before calling from C#.
- [ ] No direct DOM manipulation; use Blazor component binding and JS interop only for necessary browser APIs.
- [ ] Module imports used instead of global script references when possible.

## Security Checklist

- [ ] Authorization logic guards all sensitive operations (`@if (context.User.IsInRole("Admin"))`).
- [ ] Forms protected with CSRF tokens (built-in for Blazor Server).
- [ ] No sensitive data in component parameters or query strings.
- [ ] API calls use HTTP-only cookies or bearer tokens in Authorization header (not localStorage).
- [ ] No `@Html.Raw()` or `MarkupString` with untrusted content without sanitization.
- [ ] Third-party JavaScript libraries integrity-checked or pinned to specific versions.
- [ ] Sensitive operations logged with audit trail (user, timestamp, action).

## Data Binding Best Practices

- Use `@bind` for two-way binding on form inputs within `EditForm`.
- Use `@onchange` for custom validation or side effects on input.
- Validate input using `DataAnnotationsValidator` + validation attributes.
- For complex state, use service layer with state management pattern (not component-level @state).

## Deployment Considerations by Hosting Model

### Blazor WebAssembly (Client-side)

- Use `PublishTrimmed=true` in .csproj to reduce WASM bundle size.
- Configure AOT compilation if bundle size is critical.
- Implement service worker and offline support for offline-capable apps.
- Use authentication via JWT or OIDC; store tokens in memory only.

### Blazor Server

- Use connection resilience middleware to handle WebSocket disconnections.
- Design for stateful sessions; implement state recovery on reconnection.
- Monitor server memory usage; unload unused circuits.
- Use `@attributes=@ExtraAttributes` for CSS classes or data attributes passed from parent.

### MAUI Hybrid

- Test platform-specific behaviors (back button, app lifecycle).
- Use platform-specific CSS media queries (`@media (platform: android)`, `@media (platform: ios)`).
- Validate that JS interop works across platforms (iOS requires different patterns than Android).

## Related Guidance

- **Architecture:** See `domain-design` skill for DDD patterns in backend services.
- **Testing:** See `test-driven-development` skill for test-first implementation.
- **Security Research:** See `security-research` skill for vulnerability assessments.
- **Performance Analysis:** See `performance-research` skill for detailed profiling.

## References

All source materials and templates are in the `./references` directory.
