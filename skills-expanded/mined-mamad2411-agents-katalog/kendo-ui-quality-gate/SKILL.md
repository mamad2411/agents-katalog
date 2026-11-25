---
name: kendo-ui-quality-gate
description: Use when a Kendo UI implementation needs an expert, evidence-first quality decision covering component correctness, security, accessibility, performance, migration safety, and test coverage before merge or promotion.
---

# Kendo UI Quality Gate

## Specialization

Produce an expert, evidence-first go/no-go quality decision for Kendo UI implementations — covering widget API correctness, DataSource contract integrity, security posture, accessibility compliance, performance discipline, migration safety, and test coverage — before merge or promotion.

## Trigger Conditions

- A Kendo UI implementation is ready for merge or promotion review.
- A Kendo UI version upgrade requires pre-promotion validation.
- A legacy Kendo UI project requires a pre-production quality audit.
- Multiple Kendo UI findings have accumulated and a consolidated gate decision is needed.
- A release includes Kendo UI changes alongside other frontend code.
- A `kendo-ui-migration` completes and requires a final gate before cutover.

## Scope Boundaries

In scope:

- Widget API correctness: deprecated options/methods, missing `destroy()`, incorrect event binding teardown.
- DataSource contract: schema field mapping correctness, error handler presence, server-side operation flags.
- Security: XSS sinks via `#= #` templates, CSRF in transport, Upload restrictions, Editor sanitization, CVE posture.
- Accessibility: ARIA role compliance, keyboard interaction coverage, focus management.
- Performance: virtual scrolling configuration, server-side paging, deferred initialization, memory cleanup.
- Migration safety: deprecated API inventory, SASS variable compatibility.
- Test coverage: widget initialization, mock DataSource coverage, event simulation, destruction tests.

Out of scope:

- Server-side code quality.
- Non-Kendo UI JavaScript quality.
- CI/CD pipeline configuration (use `kendo-ui-ci-integration`).

## Inputs

- Kendo UI version in use.
- Scope of code under review (files, modules, or full project).
- Existing test results if available.
- Known risks or prior finding history.
- Target: merge gate, pre-promotion, or full project audit.

## Required Outputs

- Finding set with severity (`Blocker`, `Major`, `Minor`), location, and explicit remediation for each item.
- Overall gate recommendation: **Pass**, **Pass with Conditions**, or **No-Go**.
- Conditions list if recommendation is Pass with Conditions (must be resolved before promotion).
- Blocked items if recommendation is No-Go (must be resolved before re-gate).
- Coverage gaps: untested behaviors requiring test addition before gate passes.

## Gate Dimensions

### Dimension 1: Widget API Correctness

| Check | Pass Criterion |
|---|---|
| No deprecated widget options | Zero deprecated options in use for the current Kendo UI version |
| Destroy called on teardown | Every widget initialized in a SPA view has a matching `destroy()` call |
| Event handler teardown | Every `bind()` call has a corresponding `unbind()` in the widget lifecycle |
| Template encoding | All `#= #` expressions have documented trust classification; untrusted content uses `#: #` |

### Dimension 2: DataSource Contract

| Check | Pass Criterion |
|---|---|
| Schema model defined | `schema.model.id` and `schema.model.fields` defined for all CRUD DataSources |
| Error handler present | `error` event handler defined on all DataSources; no silent failures |
| Server-side flags consistent | `serverPaging`, `serverSorting`, `serverFiltering` match the actual API behavior |
| Transport security | CSRF token injected in all non-idempotent transport operations |

### Dimension 3: Security

| Check | Pass Criterion | Specialist Skill |
|---|---|---|
| XSS template audit | All `#= #` sinks classified as trusted or replaced with `#: #` | `kendo-ui-security` |
| CSRF coverage | Anti-forgery token present in create, update, destroy transport | `kendo-ui-security` |
| Upload restrictions | File type whitelist enforced server-side (client hint insufficient) | `kendo-ui-security` |
| Editor sanitization | Rich text Editor output is sanitized server-side before persistence | `kendo-ui-security` |
| CVE posture | No unpatched high/critical CVEs in Kendo UI dependency chain | `kendo-ui-security` |

### Dimension 4: Accessibility

| Check | Pass Criterion | Specialist Skill |
|---|---|---|
| ARIA roles present | All Kendo UI widgets emit correct ARIA roles per component contract | `kendo-ui-accessibility` |
| Keyboard navigation | Grid, DropDownList, DatePicker, Dialog pass keyboard interaction matrix | `kendo-ui-accessibility` |
| Focus management | Focus trapped in open Dialog/Window; restored on close | `kendo-ui-accessibility` |
| Color contrast | Text and UI components meet WCAG 1.4.3 AA (4.5:1 normal text, 3:1 UI) | `kendo-ui-accessibility` |
| Accessible names | All form widgets have associated `<label>` or `aria-label` | `kendo-ui-accessibility` |

### Dimension 5: Performance

| Check | Pass Criterion | Specialist Skill |
|---|---|---|
| Server-side paging | DataSources with > 500 row datasets use `serverPaging: true` | `kendo-ui-performance` |
| Virtual scrolling | Grids with > 1000 rows use `scrollable: { virtual: true }` | `kendo-ui-performance` |
| Deferred initialization | Widgets in hidden tabs/accordions initialize on reveal, not DOM ready | `kendo-ui-performance` |
| Memory cleanup | `destroy()` called in all SPA view teardown paths | `kendo-ui-performance` |
| Bundle size | Kendo UI bundle within project-defined gzip budget | `kendo-ui-performance` |

### Dimension 6: Test Coverage

| Check | Pass Criterion | Specialist Skill |
|---|---|---|
| Initialization tests | At least one initialization test per widget type in scope | `kendo-ui-testing` |
| Mock DataSource | All tests use local-array DataSource; no tests depend on live network | `kendo-ui-testing` |
| Event simulation | Primary user interactions tested via event simulation | `kendo-ui-testing` |
| Destruction tests | Destruction lifecycle tested for widgets initialized in SPA views | `kendo-ui-testing` |
| Validator tests | Custom validation rules have pass and fail test cases | `kendo-ui-testing` |

## Finding Severity Definitions

| Severity | Definition |
|---|---|
| Blocker | Security vulnerability (XSS, CSRF), WCAG AA failure, or data loss risk — must resolve before any promotion |
| Major | Widget misuse, missing error handling, performance threshold exceeded, or test coverage gap on critical flow |
| Minor | Style inconsistency, advisory performance improvement, or non-critical deprecated API usage |

## Gate Recommendation Logic

| Condition | Recommendation |
|---|---|
| Zero Blockers, zero Majors | **Pass** |
| Zero Blockers, one or more Majors with remediation plan | **Pass with Conditions** |
| One or more Blockers | **No-Go** |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Single-dimension check (e.g., security only) | Target dimension finding set complete with severity |
| L2 Practical | Full six-dimension gate for one feature | All six dimensions evaluated; gate recommendation issued |
| L3 Hardening | Full project gate before a major version promotion | No Blockers; all Majors have documented remediation plans with owners |
| L4 Expert | Reusable gate checklist template for a product team | Gate template documented and versioned; applicable to all future Kendo UI releases |
