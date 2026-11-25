---
name: backend-errors
description: "Handling errors in a backend: problem details (RFC 9457) as the one format, a catalogue of stable error codes, mapping domain errors to statuses in one place per stack, validation errors with field paths, retryable failures and Retry-After, request ids returned to clients, logging each error once, crashes and panics, timeouts versus cancellations, causes from dependencies, messages for users and for developers, i18n. Read before adding endpoints or changing how failures are reported."
---

# Errors

The generated version: `200` with `{ "success": false }`, a different shape
per endpoint, the exception's text shown to the user, a stack trace in
production, one failure logged at four layers, a `500` for a client that
went away. One part of the backend; the whole is in `backend`. This is one
format, one place that maps, and a log that tells each story once.

## 1. One format

Every error response has the same shape. Keep the project's; with none, use
problem details (RFC 9457, which replaced RFC 7807) as
`application/problem+json`:

```json
{
  "type": "https://example.com/errors/out-of-stock",
  "title": "Out of stock",
  "status": 409,
  "code": "out_of_stock",
  "detail": "Only 2 left of Kopi Susu 250ml.",
  "left": 2,
  "errors": [{ "field": "items[0].quantity", "code": "too_many" }]
}
```

- `type` names the kind of problem and links to its docs; `title` is fixed
  per type; `detail` describes this occurrence and is safe to show.
- `code` is stable and machine-readable (`out_of_stock`, `email_taken`); the
  client decides what to show from it, never from `detail`. Extra members
  (`left`) carry what the message needs (section 10).
- `errors` lists every invalid field at once for a validation failure.
- A request id is in a header (`X-Request-Id`) on every response, so a user's
  report can be matched to the log. On a `5xx` it is in the body too
  (`requestId`), where the interface can show it for the user to quote.

## 2. A catalogue of codes

One module lists every code the API may return:

```ts
export const catalogue = {
  validation_failed: { status: 400, title: "Invalid request" },
  malformed_json:    { status: 400, title: "Malformed JSON" },
  unauthenticated:   { status: 401, title: "Sign-in required" },
  forbidden:         { status: 403, title: "Not allowed" },
  not_found:         { status: 404, title: "Not found" },
  email_taken:       { status: 409, title: "Email already registered" },
  out_of_stock:      { status: 409, title: "Out of stock" },
  stale_version:     { status: 409, title: "Changed by someone else" },
  rate_limited:      { status: 429, title: "Too many requests" },
  internal:          { status: 500, title: "Internal error" },
  dependency_down:   { status: 503, title: "Service unavailable" },
} as const;
export type ErrorCode = keyof typeof catalogue;
```

- `snake_case`, specific where the client can act on it (`email_taken`, not
  `conflict`), generic where it cannot (`not_found`, `internal`); never
  renamed or given a new meaning, since clients branch on them. A new code
  is safe; removing one is a breaking change (`backend-api`).
- Each is documented (status, cause, whether a retry helps, parameters:
  `docs-api`) and has a key in the client's message catalogue.

## 3. Mapped in one place

- The service raises domain errors that say what went wrong in the domain's
  words: `NotFound`, `Forbidden`, `Conflict("already_paid")`,
  `Validation(fields)`, `RateLimited`. It does not know about HTTP.
- One error handler (middleware, an exception handler, `IntoResponse`, the
  framework's renderer) turns them into status codes and the format above.
  Handlers do not build error responses by hand, each a little differently.
- Anything unexpected becomes a `500` with a generic message and the request
  id; the details go to the log only.

TypeScript with Hono (Express and Fastify handlers take the same body):

```ts
export class AppError extends Error {
  constructor(
    readonly code: ErrorCode,
    readonly params: Record<string, string | number> = {},
    readonly fields: { field: string; code: string }[] = [],
    options?: ErrorOptions,
  ) {
    super(code, options);
  }
}

app.onError((err, c) => {
  const e = err instanceof AppError ? err : new AppError("internal", {}, [], { cause: err });
  const { status, title } = catalogue[e.code];
  const requestId = c.get("requestId"); // from hono/request-id
  if (status >= 500) logger.error({ err, requestId }, e.code); // the one log line for it
  const body = {
    type: `https://example.com/errors/${e.code.replaceAll("_", "-")}`,
    title, status, code: e.code, ...e.params,
    ...(e.fields.length ? { errors: e.fields } : {}),
    ...(status >= 500 ? { requestId } : {}),
  };
  return c.body(JSON.stringify(body), status, { "Content-Type": "application/problem+json" });
});
```

Python with FastAPI:

```python
def problem(request: Request, code: str, fields: list[dict] | None = None, **params):
    status, title = CATALOGUE[code]
    body = {"type": f"https://example.com/errors/{code.replace('_', '-')}",
            "title": title, "status": status, "code": code, **params}
    if fields:
        body["errors"] = fields
    if status >= 500:
        body["requestId"] = request.state.request_id
    return JSONResponse(body, status_code=status, media_type="application/problem+json")

@app.exception_handler(AppError)
async def on_app_error(request: Request, exc: AppError):
    return problem(request, exc.code, exc.fields, **exc.params)

@app.exception_handler(RequestValidationError)
async def on_invalid(request: Request, exc: RequestValidationError):
    # field_path(("items", 0, "quantity")) == "items[0].quantity"; CODES maps pydantic's types
    fields = [{"field": field_path(e["loc"][1:]), "code": CODES.get(e["type"], "invalid")}
              for e in exc.errors()]
    return problem(request, "validation_failed", fields)
```

Unexpected exceptions in FastAPI go through one middleware that logs with
the stack and returns `problem(request, "internal")`. Elsewhere:

- Go: handlers return `error` to one `writeError(w, r, err)` that picks the
  status with `errors.As`; Rust: an `AppError` enum (thiserror) that
  implements `IntoResponse`, returned with `?`.
- Spring: `@RestControllerAdvice` returning `ProblemDetail` (and
  `spring.mvc.problemdetails.enabled=true`); ASP.NET Core:
  `AddProblemDetails()` with an `IExceptionHandler`; Laravel:
  `->withExceptions()` in `bootstrap/app.php`; Rails: `rescue_from`; Django
  REST framework: its `EXCEPTION_HANDLER`.

## 4. Validation errors

- Every failure in one response, each with a path in the API's own casing
  and a code: `items[0].quantity`, `shippingAddress.postcode`; a query
  parameter or header by its name (`limit`). What the message needs goes
  with it: `{ "field": "name", "code": "too_long", "max": 120 }`.
- The library's codes mapped to yours (pydantic's `string_too_long` to
  `too_long`), so a library upgrade cannot change the contract.
- A body that is not JSON is `400` `malformed_json`, a wrong content type
  `415`: never a `500`.
- A rule only the service can check (the email is taken) still names the
  field, so the form marks it: `409` with
  `"errors": [{ "field": "email", "code": "taken" }]`.

## 5. What each side sees

- The client: the status, the code, a message it can show, the fields.
  Never a stack trace, an SQL statement or error, a file path, a library
  name, a hostname or a secret. In development the details can be shown; the
  switch is the environment, not a flag someone forgets.
- The log: everything, once, at the boundary: the error with its cause
  chain and stack, the request id, the route, the user id. Not the request
  body when it can hold passwords, tokens or card numbers.
- Errors that are the caller's fault (`4xx`) are logged at `info` or `warn`,
  ours (`5xx`) at `error`. A flood of `4xx` is a signal, not an incident.
  For a `4xx`, the request's own log line with the code is enough.
- Existence checks do not leak: "no account with that email" is the same
  response as "wrong password" on sign-in, and a record the caller may not
  see is a `404`, not a `403`, when its existence is itself private.

## 6. Log once, hide nothing

- Log where the error is handled, not everywhere it passes: the error
  handler for a request, the worker's wrapper for a job. Lower layers add
  context and pass it on; logging and rethrowing at each layer writes one
  failure three times with three messages.
- An error swallowed on purpose (a fallback taken, a cache that failed) is
  logged where it is swallowed, at `warn`: nothing else will see it.
- No empty `catch`, and no `catch` that logs and carries on as if it
  worked. Handle an error where something useful can be done (a retry, a
  fallback, a clear message); otherwise let it reach the handler.
- Keep the cause when wrapping, so the log shows the whole chain, and add
  what you were doing: `{ cause }` in JavaScript, `raise ... from exc` in
  Python, `fmt.Errorf("create invoice %s: %w", id, err)` in Go, `#[source]`
  or anyhow's `.with_context()` in Rust.
- A provider's errors are mapped in its client module to yours
  (`PaymentDeclined`, `ProviderUnavailable`), its raw message kept for the
  log (`backend-integrations`); database errors are mapped by constraint
  name and SQLSTATE, never by message text (`backend-data`).

## 7. Timeouts and cancellations

| What happened | Answer | Log |
|---|---|---|
| A query or outbound call passed its deadline | `503`, or `504` at a gateway (`dependency_timeout`) | `warn`, counted in a metric |
| The whole request passed its deadline | `503` | `warn` |
| The client closed the connection | Nothing (nobody is listening); `499` in the access log | `info`, not an error |

- Tell them apart in code: Go `errors.Is(err, context.DeadlineExceeded)`
  versus `context.Canceled`; JavaScript `err.name === "TimeoutError"` (from
  `AbortSignal.timeout`) versus `"AbortError"`; Python `TimeoutError`
  versus `asyncio.CancelledError`, which is always re-raised.
- Cancellation flows down: the request's signal or context goes to every
  query and outbound call, so the work stops when the client leaves.

## 8. Crashes and panics

- A panic in one request is that request's `500`, not a dead process: a
  recover middleware (chi's `Recoverer`, tower-http's `CatchPanicLayer`) or
  the framework's own; Go's `net/http` alone drops the connection with no
  response. Goroutines and tasks you start are not covered: recover inside
  them, or one panic ends the process.
- A process-level failure (Node's `uncaughtException` or an unhandled
  rejection) leaves the state unknown: log it, flush error tracking, exit
  non-zero, and let the supervisor restart it (the platform, Kubernetes,
  systemd). Never catch it and carry on.
- Every `5xx` and crash reaches error tracking (Sentry or the project's)
  with the release, environment and request id, without bodies or personal
  data (`backend-observability`).

## 9. Failures that can be retried

- Say which ones: `429` and `503` carry `Retry-After`; a timeout or a lost
  connection to a dependency is a `503` or `504`, not a `500`.

| Status | Can the client retry? |
|---|---|
| `400`, `401`, `403`, `404`, `422` | No: the same request fails the same way |
| `409` | Not as it is: read the current state, then decide |
| `429`, `503` | Yes, after `Retry-After` (seconds, or an HTTP date) |
| `500`, `502`, `504` | Only when repeating is safe: a `GET`, or a write with an idempotency key |

- A write that may have happened before a failure is made safe to repeat
  (idempotency keys in `backend-api`), so a retry does not double it.
- Time limits on everything the request waits for: the database query, each
  outbound call (`backend-integrations`).

## 10. Messages people read

- Messages for users go through i18n (the `i18n` skill): the server sends the
  `code` and the parameters (`{ "code": "out_of_stock", "left": 2 }`), and the
  message is looked up in the user's language by whoever renders it. When the
  server renders text itself (emails, server-rendered pages), it uses the
  catalogue too.
- A server that fills `detail` picks the language from `Accept-Language`
  among its locales (or the default) and names it in `Content-Language`.
- Messages say what happened and what to do: "The code has expired. Request a
  new one." Not "Error 1043" and not "Something went wrong" when the cause is
  known. Never an exception's text, a provider's message or SQL.
- Messages for developers (logs, exceptions) stay in English.

## Check it

```sh
curl -si localhost:3000/api/orders/ord_missing
curl -si -X POST localhost:3000/api/orders -H 'content-type: application/json' -d '{"items":[{"quantity":0}]}'
curl -si -X POST localhost:3000/api/orders -H 'content-type: application/json' -d '{"items":'
```

- Each answers `application/problem+json` with a catalogue code: `404`;
  `400` naming every bad field; `400` `malformed_json`, not `500`.
- A test that makes a dependency throw gets a `500` with the generic title
  and a request id, and the log holds that id once, with stack and cause.
- Swallowed errors: `rg -n 'catch \([^)]*\) \{\s*\}|except[^:]*:\s*pass|_ = err\b'`.

## Avoid

`200` with `success: false`; a different error shape per endpoint; the stack
trace in the response; `catch (e) { console.log(e) }` and carry on; an error
message built from an exception's text and sent to the user; "Something went
wrong" for a failure whose cause is known; a sign-in that says which half was
wrong; a code renamed under the same version; the same error logged at every
layer; a cancelled request counted as a server error; a `500` for bad JSON.
