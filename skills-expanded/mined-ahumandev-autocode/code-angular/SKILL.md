---
name: code-angular
description: Angular Standards - Use this skill to learn how to update Angular code. This is the Angular coding standard that you MUST apply to all your Angular code.
---

# Angular Standards

- Never pack entire UI or feature into one component/file.
- Compose pages from separate, focused, reusable Angular components. Explicit component boundaries override nearby monolithic patterns.
- Give each component its own `.ts` file. Co-locate related files; use external HTML/styles for nontrivial UI, following repo conventions.
- External templates alone do not satisfy component decomposition.
- Reuse existing components first. Split repeated UI or meaningful independent UI; avoid tiny arbitrary wrappers.
- Define typed inputs/outputs and clear component responsibilities. Never mutate another component's state or input objects.
- Put shared logic and data access in focused services/functions
- Use dependency injection for shared dependencies.

## Version and organization

- Check nearby conventions before editing. Match existing naming and file layout.
- Stay compatible. Use stable, supported APIs; never silently upgrade, migrate, add dependencies, or swap architecture.
- Organize by feature; keep component, template, styles, tests, and related logic together.
- Prefer supported standalone components, `input()`, `output()`, and `inject()` for new code when compatible with project conventions. Never blindly convert existing NgModules.
- Keep strict types across component contracts, services, forms, and templates. Never use `any`; narrow `unknown` at untrusted boundaries.

## State and templates

- Keep templates simple; move complex logic into typed component members or focused functions. Keep template expressions free from side effects.
- Use project-supported control flow. Track lists with stable item identity, never changing/random keys.
- Use signals for local reactive state; `computed` for derived state. Never use effects for state propagation.
- Preserve existing RxJS streams. Clean up subscriptions with async pipe or `takeUntilDestroyed` where supported; follow existing lifecycle cleanup otherwise.
- Render loading, error, and empty states explicitly; preserve retry paths and prevent duplicate submissions where applicable.

## Forms and accessibility

- Use typed reactive forms for complex forms; follow existing conventions for simple forms. Validate inputs; expose actionable field errors.
- Prefer semantic native HTML. Associate labels and errors with controls; preserve keyboard operation, visible focus, and sensible focus restoration.

## Security and performance

- Use Angular safe bindings and sanitization. Never bypass trust checks, inject unsafe DOM/HTML, or compile user-generated templates.
- Justify performance changes with measurements; follow project change-detection conventions. Never mandate OnPush or zoneless mode.
- Preserve lazy-loading boundaries; avoid repeated expensive template work and unnecessary subscriptions.

## Verification

- Add behavior tests for component contracts, interactions, forms, accessibility, and async states affected by changes. Cover reused component boundaries and public inputs/outputs.
- Use existing test runner; never replace tooling for this task.
- Run existing build, type, lint, and test checks relevant to changes. Report failures and unrun checks with reasons; never claim unrun checks passed.

## Angular References

- [Style](https://angular.dev/style-guide)
- [Components](https://angular.dev/guide/components)
- [Signals](https://angular.dev/guide/signals)
- [RxJS interop](https://angular.dev/ecosystem/rxjs-interop)
- [Dependency injection](https://angular.dev/guide/di)
- [Typed forms](https://angular.dev/guide/forms/typed-forms)
- [Forms](https://angular.dev/guide/forms)
- [Accessibility](https://angular.dev/best-practices/a11y)
- [Security](https://angular.dev/best-practices/security)
- [Performance](https://angular.dev/best-practices/performance)
- [Testing](https://angular.dev/guide/testing)
