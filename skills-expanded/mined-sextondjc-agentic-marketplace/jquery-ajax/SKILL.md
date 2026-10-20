---
name: jquery-ajax
description: Use when implementing or reviewing jQuery AJAX requests, Deferred objects, Promise chaining, error handling, and secure request configuration.
---

# jQuery AJAX

## Specialization

Implement and review expert-level jQuery AJAX patterns covering `$.ajax()`, shorthand methods, Deferred / Promise integration, error handling, request configuration, and cross-origin safety — grounded in official jQuery API documentation.

## Trigger Conditions

- Implementing `$.ajax()`, `$.get()`, `$.post()`, `$.getJSON()`, or `$.getScript()`.
- Designing Deferred-based async workflows with `.done()`, `.fail()`, `.always()`, `.then()`.
- Chaining multiple async operations or handling parallel requests with `$.when()`.
- Configuring AJAX defaults via `$.ajaxSetup()`.
- Handling AJAX events: `ajaxStart`, `ajaxStop`, `ajaxError`, `ajaxSuccess`.
- Reviewing AJAX error handling and retry logic.
- Assessing CORS configuration and cross-origin request safety.
- Evaluating whether native `fetch()` is a better fit than `$.ajax()`.

## Scope Boundaries

In scope:

- `$.ajax()` option surface: `url`, `method`, `data`, `dataType`, `contentType`, `headers`, `timeout`, `beforeSend`, `complete`, `success`, `error`.
- jQuery Deferred objects: creation, resolution, rejection, and chaining.
- `$.when()` for parallel request coordination.
- AJAX global event hooks and progress indicators.
- CORS headers and `crossDomain` option.
- Secure request patterns: CSRF token injection, header sanitization, response validation.

Out of scope:

- Server-side endpoint implementation.
- WebSocket or SSE patterns.
- Native `fetch()` implementation details — covered only as a migration decision point.

## Inputs

- Request type, endpoint contract, and expected response format.
- Authentication and CSRF requirements.
- jQuery version in use.
- Error handling and retry expectations.
- Parallel vs. sequential request coordination needs.

## Required Outputs

- Correct `$.ajax()` configuration with explicit `method`, `dataType`, and error handler.
- Deferred chain with `.done()`, `.fail()`, and `.always()` for all async paths.
- CSRF token injection strategy if POSTing to a CSRF-protected endpoint.
- `$.when()` usage for parallel coordination if applicable.
- Security review of response handling — explicit check for unsanitized HTML injection from response data.
- Native `fetch()` migration recommendation where jQuery is the only remaining dependency.

## Core Patterns

### $.ajax() Baseline

```javascript
$.ajax({
  url: '/api/resource',
  method: 'GET',
  dataType: 'json',
  timeout: 10000,
  beforeSend: function(xhr) {
    xhr.setRequestHeader('X-CSRF-Token', getCsrfToken());
  }
})
.done(function(data) { /* handle success */ })
.fail(function(jqXHR, textStatus, errorThrown) { /* handle error */ })
.always(function() { /* cleanup */ });
```

- Always specify `method` explicitly — never rely on `$.get()` / `$.post()` when custom headers or retry logic are needed.
- Always set `dataType` — prevents jQuery from guessing content type from the response, which can cause silent type coercion.
- Always set `timeout` — no timeout means the request can hang indefinitely.
- Never use success/error keys in the options object for new code; use `.done()` / `.fail()` on the returned Deferred.

### Deferred and Promise

- `$.ajax()` returns a jqXHR which is a Deferred-compatible object.
- Use `.then(successFn, failFn)` when chaining — `.then()` returns a new Deferred, enabling pipeline composition.
- Use `.done()` / `.fail()` / `.always()` when adding callbacks without chaining.
- Never mix success/error callbacks in the options object with Deferred methods — pick one pattern per call site.
- Map jqXHR to a native Promise at the boundary when integrating with `async/await` code:
  ```javascript
  const result = await Promise.resolve($.ajax({ ... }));
  ```

### Parallel Coordination

- Use `$.when(req1, req2, req3).done(function(r1, r2, r3) { })` for parallel requests.
- `$.when()` rejects on the first failure — design `.fail()` to handle partial completion if needed.
- For independent parallel requests where partial success is acceptable, wrap each in its own error handler before passing to `$.when()`.

### AJAX Defaults

- Use `$.ajaxSetup()` only for project-wide defaults (base URL prefix, CSRF headers, default timeout).
- Do not use `$.ajaxSetup()` to set success or error handlers — this creates hidden global behavior.
- Reset per-request options explicitly; `$.ajaxSetup()` values are inherited but overridable.

### Error Handling

- Always handle `.fail()` — silent failures create ghost states in the UI.
- Log `jqXHR.status` and `jqXHR.responseText` in the error path for diagnostics.
- Distinguish network errors (status 0) from server errors (4xx/5xx) and application errors (200 with error payload).
- Implement retry only for idempotent requests (GET); never auto-retry POST/PUT/DELETE without user confirmation.

### CSRF and Security

- Inject CSRF tokens via `beforeSend` using `xhr.setRequestHeader()` — do not embed tokens in query strings.
- Set `contentType: 'application/json'` and send `JSON.stringify(data)` for JSON APIs — avoids form-encoded payloads that bypass CSRF protections on some frameworks.
- Never use response data directly in `.html()` — pass through a sanitizer or use `.text()`. See `jquery-security`.
- Validate that `dataType: 'json'` is set when expecting JSON — prevents a malicious server from returning a `<script>` response that jQuery would execute if `dataType` is inferred as `script`.

### Native Fetch Decision Rule

If jQuery is used exclusively for AJAX (no DOM manipulation or event delegation), prefer native `fetch()` with an `AbortController` timeout rather than adding jQuery as a dependency. Retain `$.ajax()` when the project already uses jQuery broadly and the Deferred model simplifies existing async flows.

## Workflow

1. Define endpoint contract: method, URL, payload schema, response schema.
2. Configure `$.ajax()` with explicit `method`, `dataType`, and `timeout`.
3. Inject CSRF token via `beforeSend` if required.
4. Chain `.done()`, `.fail()`, and `.always()` — no silent paths.
5. Use `$.when()` for parallel coordination.
6. Validate response before any DOM operation.
7. Assess native `fetch()` migration if jQuery is the only remaining dependency.

## Done Criteria

- Every `$.ajax()` call has explicit `method`, `dataType`, and `timeout`.
- Every call has `.done()`, `.fail()`, and `.always()` handlers.
- CSRF tokens are injected in `beforeSend` for non-idempotent requests.
- Response data is not passed directly to `.html()`.
- `$.ajaxSetup()` contains no success/error callbacks.

## References

- [jQuery API: Ajax](https://api.jquery.com/category/ajax/)
- [jQuery API: $.ajax()](https://api.jquery.com/jquery.ajax/)
- [jQuery API: Deferred Object](https://api.jquery.com/category/deferred-object/)
- [jQuery API: $.when()](https://api.jquery.com/jquery.when/)
- [jQuery Learn: Ajax](https://learn.jquery.com/ajax/)
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
