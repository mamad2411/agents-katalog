---
name: jquery-migration
description: Use when migrating jQuery from v1 or v2 to v3, using the jQuery Migrate plugin to assess compatibility, or planning a phased replacement of jQuery with native browser APIs.
---

# jQuery Migration

## Specialization

Plan and execute expert-level jQuery migrations — v1/v2 to v3 upgrades using the jQuery Migrate plugin, and phased jQuery-to-native-API replacement strategies — with deterministic compatibility checks, sequenced remediation, and rollback safety.

## Trigger Conditions

- Upgrading a project from jQuery 1.x or 2.x to jQuery 3.x.
- Installing or evaluating the jQuery Migrate plugin.
- Planning a phased replacement of jQuery with native browser APIs (`fetch`, `querySelectorAll`, `classList`, etc.).
- Auditing existing code for deprecated or removed jQuery APIs.
- Reviewing browser support implications of removing jQuery from a legacy codebase.
- A `jquery-quality-gate` identifies deprecated API usage that requires remediation.

## Scope Boundaries

In scope:

- jQuery 1.x/2.x → 3.x breaking changes and deprecation inventory.
- jQuery Migrate plugin installation, configuration, and console-warning triage.
- Phased native API replacement: Fetch, DOM, Events, Utilities.
- Browser support matrix decisions when dropping jQuery.
- Rollback plan for failed migration attempts.

Out of scope:

- Framework migrations (e.g., jQuery → React/Vue/Angular). This skill covers jQuery core migration only.
- Plugin compatibility upgrades beyond the decisions driven by a core jQuery version bump.
- Build tool or bundler reconfiguration (covered in project build tooling, not this skill).

## Inputs

- Current jQuery version(s) in use (may differ per page or module).
- Browser support matrix.
- jQuery Migrate plugin warning log if available.
- List of jQuery plugins in use and their jQuery compatibility declarations.
- Target: upgrade to jQuery 3.x, or replace jQuery entirely.
- Timeline and risk tolerance.

## Required Outputs

- Compatibility audit: breaking changes relevant to the codebase.
- jQuery Migrate plugin configuration and interpreted warning log.
- Phased remediation plan with per-phase scope, rollback trigger, and validation gate.
- Plugin compatibility matrix: which plugins support the target jQuery version.
- Native API replacement map (if full jQuery removal is targeted).
- Go/no-go recommendation for each migration phase.

## Breaking Changes Inventory: v1/v2 → v3

| Category | Change | Remediation |
|---|---|---|
| Ajax | `$.ajax()` returns a Deferred, not jqXHR in all paths | Chain `.done()/.fail()` on returned value; do not access `.success()/.error()` |
| Ajax | JSONP success is async — no longer fires synchronously | Ensure UI updates are in callbacks |
| Ajax | `$.parseJSON()` throws on invalid JSON | Wrap in try/catch |
| Events | `.on()` and `.off()` are the only supported bind/unbind APIs | Replace all `.bind()`, `.live()`, `.delegate()`, `.unbind()`, `.die()`, `.undelegate()` |
| Events | Event alias shorthand removed: `.load()`, `.unload()`, `.error()` | Replace with `.on('load', ...)` etc. |
| DOM | `.size()` removed | Replace with `.length` |
| DOM | `.context` and `.selector` properties removed from jQuery objects | Remove any reliance on these undocumented internals |
| DOM | `jQuery(html, props)` only accepts a `<tag>` string with a single top-level element | Adjust multi-element HTML strings |
| Selectors | `:eq()`, `:lt()`, `:gt()`, `:even()`, `:odd()` are extension pseudo-classes — not CSS standard | These still work but have performance cost vs. `.eq()`, `.filter()` methods |
| Effects | `.show()`, `.hide()`, `.toggle()` no longer animate inline-block elements by default | Use `.animate()` or CSS transitions for animated show/hide |
| Deferred | `.pipe()` removed | Replace with `.then()` |
| Utilities | `$.type()` returns `'symbol'` for ES6 symbols; `$.isFunction()` deprecated in 3.3 | Replace `$.isFunction(x)` with `typeof x === 'function'` |
| Utilities | `$.now()` deprecated in 3.3 | Replace with `Date.now()` |
| Utilities | `$.trim()` deprecated in 3.5 | Replace with `String.prototype.trim()` |
| XSS | `$.parseHTML()` behavior change — scripts in HTML strings are not evaluated by default in 3.5 | Review all `$.parseHTML()` and `.html()` call sites |

## jQuery Migrate Plugin Workflow

1. Install the development (unminified) version of jQuery Migrate alongside the target jQuery version.
2. Open the browser console and collect all deprecation warnings.
3. Group warnings by category: Events, Ajax, Selectors, Effects, Utilities.
4. Prioritize warnings that indicate runtime errors (not just deprecations) — fix these first.
5. Remediate each category in order, re-running the Migrate plugin after each batch.
6. When no new warnings appear: remove the Migrate plugin and run smoke tests.
7. Record the final warning log for the migration evidence artifact.

```html
<!-- Development migration setup -->
<script src="jquery-3.x.x.js"></script>
<script src="jquery-migrate-3.x.x.js"></script>
```

## Native API Replacement Map

| jQuery | Native Equivalent | Notes |
|---|---|---|
| `$(selector)` | `document.querySelectorAll(selector)` | Returns NodeList, not jQuery object |
| `$.ajax()` | `fetch()` + `AbortController` | Add CSRF header in `headers` option |
| `$(el).on(event, handler)` | `el.addEventListener(event, handler)` | Manage delegation manually |
| `$(el).addClass(cls)` | `el.classList.add(cls)` | IE 11+: classList supports SVG in modern browsers |
| `$(el).attr(name)` | `el.getAttribute(name)` | |
| `$(el).data(key)` | `el.dataset.key` | Note: jQuery `.data()` cache is not reflected in `dataset` |
| `$(el).css(prop)` | `el.style.prop` or `getComputedStyle(el).prop` | |
| `$(el).hide()` | `el.style.display = 'none'` | |
| `$.parseJSON()` | `JSON.parse()` | |
| `$.trim(str)` | `str.trim()` | |
| `$.isArray(x)` | `Array.isArray(x)` | |
| `$.each(arr, fn)` | `arr.forEach(fn)` | |
| `$.extend({}, a, b)` | `Object.assign({}, a, b)` or spread `{...a, ...b}` | Deep merge still requires a utility |

## Phased Migration Strategy

### Phase 0 — Compatibility Baseline
- Install jQuery Migrate. Collect and categorize all warnings.
- Identify plugin compatibility blockers.
- Record browser support matrix.

### Phase 1 — Deprecated API Remediation
- Fix all jQuery Migrate warnings: replace deprecated event methods, removed utilities, and API changes.
- Gate: Migrate plugin emits zero warnings.

### Phase 2 — jQuery Version Upgrade
- Swap to target jQuery version. Run smoke tests.
- Gate: All functional smoke tests pass; no new console errors.

### Phase 3 — Plugin Compatibility
- Upgrade or replace plugins incompatible with the new jQuery version.
- Gate: All plugin functionality operates correctly.

### Phase 4 (Optional) — Native API Replacement
- Replace jQuery usage module by module with native equivalents.
- Apply the native replacement map; maintain behavior parity.
- Gate: Equivalent test coverage passes on native implementation.

### Rollback Trigger
Any gate failure triggers rollback to the prior phase. Document the failing assertion and root cause before retrying.

## Workflow

1. Collect current jQuery version and Migrate warning log.
2. Identify breaking changes relevant to the codebase from the inventory.
3. Build plugin compatibility matrix.
4. Sequence phases and assign go/no-go gate for each.
5. Execute Phase 0 and Phase 1 before changing the jQuery version.
6. After Phase 3 passes, assess Phase 4 if full jQuery removal is in scope.

## Done Criteria

- jQuery Migrate emits zero warnings after Phase 1.
- Target jQuery version is loaded and smoke tests pass.
- All plugins are verified compatible.
- A rollback trigger is documented for each phase.
- If native replacement: replacement map is complete and test coverage is maintained.

## References

- [jQuery Migrate Plugin](https://github.com/jquery/jquery-migrate)
- [jQuery 3 Upgrade Guide](https://jquery.com/upgrade-guide/3.0/)
- [jQuery Blog: jQuery 3.0 Released](https://blog.jquery.com/2016/06/09/jquery-3-0-final-released/)
- [jQuery API: Deprecated](https://api.jquery.com/category/deprecated/)
- [MDN: Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [MDN: Element.classList](https://developer.mozilla.org/en-US/docs/Web/API/Element/classList)
