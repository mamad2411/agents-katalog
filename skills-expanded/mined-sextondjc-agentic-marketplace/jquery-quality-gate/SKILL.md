---
name: jquery-quality-gate
description: Use when jQuery code or a jQuery-dependent project needs an expert, evidence-first quality decision covering correctness, security, performance, migration safety, and test coverage before merge or promotion.
---

# jQuery Quality Gate

## Specialization

Produce an expert, evidence-first go/no-go quality decision for jQuery implementations — covering API correctness, security posture, performance discipline, migration safety, plugin integrity, and test coverage — before merge or promotion.

## Trigger Conditions

- A jQuery implementation is ready for merge or promotion review.
- A jQuery codebase is being assessed before a version upgrade.
- A legacy jQuery project requires a pre-production quality audit.
- Multiple jQuery findings have accumulated and a consolidated gate decision is needed.
- A release includes jQuery changes alongside other frontend code.

## Scope Boundaries

In scope:

- jQuery API correctness: deprecated API usage, `.prop()` vs `.attr()` misuse, missing `.off()` in teardown.
- Security: XSS sinks, CSRF exposure, JSONP usage, known CVEs, CSP violations.
- Performance: uncached selectors, unbound handlers, layout thrash, animation queue issues.
- Migration safety: deprecated API inventory, plugin compatibility.
- Plugin integrity: authoring pattern compliance, chainability, destruction.
- Test coverage: event simulation, AJAX mock coverage, Deferred contract tests, plugin lifecycle tests.

Out of scope:

- Server-side code quality.
- Non-jQuery JavaScript quality (route to appropriate frontend quality skill).
- CI/CD pipeline configuration.

## Inputs

- jQuery version in use.
- Scope of code under review (files, modules, or full project).
- Existing test results if available.
- Known risks or prior finding history.
- Target: merge gate, pre-promotion, or full project audit.

## Required Outputs

- Finding set with severity, location, and explicit remediation for each item.
- Overall gate recommendation: **Pass**, **Pass with Conditions**, or **No-Go**.
- Conditions list if recommendation is Pass with Conditions (must be resolved before promotion).
- Blocked items if recommendation is No-Go (must be resolved before re-gate).
- Coverage gaps: untested behaviors requiring test addition before gate passes.

## Gate Dimensions

### Dimension 1: API Correctness

| Check | Pass Criterion |
|---|---|
| No deprecated API | Zero `.bind()`, `.live()`, `.delegate()`, `.unbind()`, `.die()`, `.undelegate()`, `.load()` (event), `.error()` (event), `.size()`, `.pipe()` calls |
| `.prop()` vs `.attr()` | Boolean DOM properties use `.prop()` only |
| `.data()` cleanup | Every `.data()` write has a corresponding `.removeData()` or element removal path |
| Chaining preserved | All `$.fn` plugin methods return `this.each()` |
| No `.on()` without `.off()` in teardown | Every dynamically bound handler has a teardown path |

### Dimension 2: Security

| Check | Severity if Failed | Pass Criterion |
|---|---|---|
| jQuery version ≥ 3.5.0 | Critical | Version confirmed ≥ 3.5.0 |
| No unsanitized `.html(dynamic)` | Critical | All `.html()` / `.append()` sinks use `.text()` or DOMPurify-sanitized input |
| No `$(userInput)` constructor with HTML | Critical | Constructor receives selectors or native elements only |
| CSRF on non-GET requests | High | All POST/PUT/DELETE inject CSRF token via `beforeSend` |
| No JSONP to untrusted origins | High | No `dataType: 'jsonp'` to non-controlled hosts |
| No `$.globalEval()` | High | Absent from codebase |
| CSP compatibility | Medium | No `.attr('onclick', ...)` or inline event injection |

Any Critical or High security finding blocks gate passage — these require resolution before re-gate.

### Dimension 3: Performance

| Check | Pass Criterion |
|---|---|
| Selectors cached | No repeated `$()` query for the same element within a function scope |
| No layout thrash | DOM reads and writes are not interleaved within the same operation |
| Delegation preferred | Dynamic element handlers use `.on(event, selector, handler)` delegation |
| Scroll/resize debounced | High-frequency event handlers are wrapped in debounce or throttle |
| `.stop()` before `.animate()` | New animations call `.stop()` on the element before starting |
| Handler accumulation absent | No `.on()` called multiple times without `.off()` on the same element |

### Dimension 4: Migration Safety

| Check | Pass Criterion |
|---|---|
| jQuery Migrate clean | Zero jQuery Migrate warnings if Migrate plugin is installed |
| Deprecated API absent | Confirmed by Dimension 1 checks |
| Plugin compatibility declared | Each plugin specifies supported jQuery versions and target version is in range |

### Dimension 5: Plugin Integrity (if plugins exist)

| Check | Pass Criterion |
|---|---|
| IIFE wrapping | Plugin is wrapped in `(function($) { }(jQuery))` |
| Re-init guard | Plugin uses `$.data()` check before re-initialization |
| Chainability | `$.fn.pluginName` returns `this.each()` |
| Event namespace | All internal event bindings use plugin namespace |
| Destroy method | `destroy()` unbinds all events and calls `removeData()` |

### Dimension 6: Test Coverage

| Check | Pass Criterion |
|---|---|
| DOM isolation | All tests use `#qunit-fixture` or per-test DOM reset |
| Event simulation coverage | Success and propagation-stopped paths are tested |
| AJAX mock coverage | Success, error, and timeout scenarios are mocked |
| Deferred contract coverage | `.done()`, `.fail()`, and `.always()` are independently exercised |
| Plugin lifecycle coverage | Init, option override, method call, and destroy are tested |
| AJAX mocks cleared | `$.mockjax.clear()` or equivalent is called in `afterEach` |

## Gate Decision Matrix

| Outcome | Condition |
|---|---|
| **Pass** | All dimensions pass with zero findings |
| **Pass with Conditions** | No Critical or High security findings; Minor/Medium findings documented with resolution timeline |
| **No-Go** | Any Critical finding; any unmitigated High security finding; two or more High-severity findings across any dimension |

## Workflow

1. Confirm jQuery version — flag immediately if < 3.5.0 (Critical).
2. Run Dimension 1 (API Correctness) — enumerate deprecated API usage.
3. Run Dimension 2 (Security) — audit all HTML sinks, AJAX configuration, and CVE exposure.
4. Run Dimension 3 (Performance) — audit selector caching, DOM batching, and event topology.
5. Run Dimension 4 (Migration Safety) — run jQuery Migrate if upgrading; audit plugin compatibility.
6. Run Dimension 5 (Plugin Integrity) — if plugins exist.
7. Run Dimension 6 (Test Coverage) — verify test patterns against pass criteria.
8. Aggregate findings and apply gate decision matrix.
9. Emit gate recommendation with explicit finding list and conditions or blockers.

## Finding Format

Each finding must include:

- **ID**: `JQ-NNN` (sequential)
- **Dimension**: Correctness / Security / Performance / Migration / Plugin / Testing
- **Severity**: Critical / High / Medium / Low
- **Location**: File, function, or line reference
- **Description**: What is wrong and why it matters
- **Remediation**: Exact change required to resolve

## Done Criteria

- All six dimensions have been evaluated.
- Gate recommendation is explicit: Pass, Pass with Conditions, or No-Go.
- Every finding has a severity, location, and remediation.
- Conditions or blockers are enumerated for non-Pass recommendations.

## References

- [jQuery API Documentation](https://api.jquery.com)
- [jQuery Migrate Plugin](https://github.com/jquery/jquery-migrate)
- [jQuery 3 Upgrade Guide](https://jquery.com/upgrade-guide/3.0/)
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [DOMPurify](https://github.com/cure53/DOMPurify)
- [jQuery Learn: Performance](https://learn.jquery.com/performance/)
- [QUnit Docs](https://qunitjs.com)
