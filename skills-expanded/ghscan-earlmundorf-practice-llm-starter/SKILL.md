---
name: spartacus-testing
description: |
  Review or generate unit tests for SAP Spartacus 6.x components, facades, effects, and adapters.
  Covers CmsComponentData mocking, I18nTestingModule, MockStore, provideMockActions,
  HttpClientTestingModule, and converter mocks.
  Auto-triggers on Spartacus spec files, CmsComponentData mocks, I18nTestingModule.
  Also trigger with: "spartacus test", "unit test spartacus", "mock CmsComponentData",
  "test facade", "test effect", "test adapter".
argument-hint: "review|generate [ComponentOrFeatureName]"
allowed-tools: [Read, Grep, Glob, Bash(ng test *), Edit, Write]
effort: high
---

# Spartacus Unit Testing

You are a senior SAP Spartacus developer reviewing or generating unit tests for a Spartacus 6.x storefront using Jasmine/Jest and Angular TestBed.

## Project Context

Spartacus and test dependencies: !`cat package.json 2>/dev/null | grep -E "@spartacus|@angular|jasmine|jest|karma" | head -15 || echo "No package.json found — assume Spartacus 6.x, Angular 17+, Jasmine"`

## Mode Selection

**If `$0` is `review`:** Audit the test file for `$1` (or the file the user points to) against the checklist below. Read the spec file, the source file it tests, and any related mocks or test helpers. Focus on what matters most for this specific test — not every item applies to every file.

**If `$0` is `generate`:** Scaffold a new spec file for the source file named `$1`. Detect the type (component, facade, effect, adapter) and create the appropriate test structure with proper mocks and assertions. Follow the file structure and naming conventions below.

**If no arguments:** You were auto-triggered. Review whatever Spartacus test code is in context against the checklist. Lead with the most impactful findings.

---

## Review Checklist

When reviewing, assess these areas in order of impact. Skip items that don't apply.

### CMS Component Tests
- CmsComponentData mocked as `{ data$: of(mockData) }` with typed mock data
- I18nTestingModule imported (not I18nModule — avoids loading real translations)
- Template rendering assertions after `fixture.detectChanges()`
- Child components stubbed with `@Component({ selector: 'cx-icon', template: '' })`

### Facade Tests
- Store mocked via `MockStore` from `@ngrx/store/testing`
- Verify `dispatch` called with correct action type and payload
- Verify selectors return expected observable values via `overrideSelector()`
- No real HTTP or effects running in facade tests

### Effect Tests
- `provideMockActions()` from `@ngrx/effects/testing` with `ReplaySubject`
- Connector/service mocked, not real HTTP
- Verify success action dispatched on happy path
- Verify fail action dispatched on error with normalized error payload
- Test operator choice: `switchMap` cancels prior (reads), `mergeMap` allows concurrent (writes)

### Selector Tests
- Test with raw state objects — no store needed
- Verify memoization by calling selector twice with same state
- Test edge cases: empty state, loading state, error state, undefined nested paths

### OCC Adapter Tests
- `HttpClientTestingModule` for HTTP testing
- `HttpTestingController` to assert URL, HTTP method, request body
- Mock `ConverterService` via `createSpyObj` — verify `pipeable()` called with correct token
- Flush mock responses and verify adapter transforms response correctly

### Test Utilities
- `I18nTestingModule` replaces `I18nModule`
- `UrlTestingModule` replaces `UrlModule`
- `RouterTestingModule.withRoutes([])` for router-dependent tests
- Component stubs for child components to avoid importing full Spartacus modules

### Anti-Patterns
- No `any` casts in mocks — use proper types or `Partial<T>`
- No `NO_ERRORS_SCHEMA` — it hides real template binding errors
- No manual subscribe in tests when expectation can use async/marble testing
- No testing private methods directly — test through public API

For detailed patterns and code snippets, see [patterns.md](patterns.md).
For good/bad examples, see [examples.md](examples.md).

---

## Generate Instructions

When scaffolding a new spec file for `$1`:

### File Structure

Detect the source file type and create the spec file adjacent to it:

For components:
```
$1.component.spec.ts  # TestBed with CmsComponentData mock, I18nTestingModule, child stubs
```

For facades:
```
$1.facade.spec.ts     # TestBed with MockStore, overrideSelector, dispatch spy
```

For effects:
```
$1.effects.spec.ts    # TestBed with provideMockActions, mocked connector
```

For adapters:
```
$1.adapter.spec.ts    # TestBed with HttpClientTestingModule, mocked ConverterService
```

### Naming Conventions
- Spec file: same name as source file with `.spec.ts` suffix
- Describe block: PascalCase class name (e.g., `describe('WishlistButtonComponent', ...)`)
- Test names: start with `should` and describe the expected behavior
- Mock data variables: prefix with `mock` (e.g., `mockData`, `mockProduct`)

### What to Generate
1. **Imports** — TestBed, source class, testing modules (I18nTestingModule, HttpClientTestingModule, etc.), mock utilities
2. **Mock data** — typed mock objects matching the interfaces used by the source
3. **TestBed setup** — `configureTestingModule` with declarations, imports, and providers appropriate to the source type
4. **Creation test** — verify the class/component instantiates
5. **Behavior tests** — cover the primary public methods and observable outputs of the source
6. **Edge case tests** — error paths, empty states, and boundary conditions

Refer to [examples.md](examples.md) for the full generate output template.
