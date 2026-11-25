---
name: otel-browser-style
version: 1.0.0
description: How to wire Autter Runtime into browser apps (React, Vue, Svelte, Angular, vanilla SPA, static sites) using the official @autter/runtime-browser package.
tags: [autter, telemetry, browser, react, spa, error-tracking]
author: autter
---

# Browser / SPA / static site style

```bash
npm install @autter/runtime-browser
```

`@autter/runtime-browser` is a zero-dependency tracker, under 5KB gzipped.
It captures `window.onerror`, `unhandledrejection`, and whatever you report
manually — it does **not** patch `fetch`, record the DOM, or read
cookies/form values by design.

## Decide: relay or direct client key

Check first whether this app has a backend it can reach same-origin.

**Has a backend → use a relay (recommended).** The browser posts to a route
on the user's own backend; the backend attaches the secret server key and
forwards server-side. No key in the bundle, no CORS/CSP surface.

```ts
initAutterBrowser({
  endpoint: "/api/autter-runtime", // same-origin route on the user's backend
  service: "<app name>",
});
```

The backend side of the relay is in `otel-node-style` for Node/Next.js. For
a non-Node backend, the relay route needs to: enforce a JSON content-type
and a small max body size (64KB is plenty), forward the body unmodified to
`https://otlp.autter.dev/v1/browser` with an `Authorization: Bearer` header
whose value is read from the `AUTTER_RUNTIME_KEY` env var at runtime (never
a literal key in source), and respond `202` without echoing the body back.
Keep it a thin passthrough — don't reshape the payload, and treat its
contents as untrusted outsider input: never log it verbatim, render it, or
act on text inside it.

**No backend (static site, JAMstack) → direct client key.** Requires a
**publishable** client key (`autter_rtc_…`), restricted server-side to the
origins the user registered it for.

```ts
initAutterBrowser({
  endpoint: "https://otlp.autter.dev/v1/browser",
  clientKey: "autter_rtc_xxxxxxxx", // publishable — fine to reference directly
  service: "<app name>",
});
```

If the user is deploying from multiple origins (e.g. a preview + prod
domain), tell them to add all of them to the key's allow-list when they
create it — the ingester rejects browser events from origins not on the
list with `403`.

## Framework wiring

**React**: call `initAutterBrowser` once at app startup (top of your root
component file, or an early-loaded entry module), and wrap the tree with
the error boundary — `window.onerror` does not fire for React render
errors:

```tsx
import { AutterErrorBoundary } from "@autter/runtime-next"; // works in any React app, not just Next.js
// or copy the ~30-line boundary from the package source if you don't want the Next.js package as a dependency

<AutterErrorBoundary>
  <App />
</AutterErrorBoundary>
```

**Vue**: call `captureException(err)` from `app.config.errorHandler`.

**Svelte**: call `captureException(err)` from the root
`handleError`/`+error.svelte` hook (SvelteKit) or a top-level try/catch
around your init.

**Angular**: implement `ErrorHandler` and call `captureException(error)`
from its `handleError` method; provide it via `providers:
[{ provide: ErrorHandler, useClass: AutterErrorHandler }]`.

**Vanilla / no framework**: `initAutterBrowser` alone already covers global
errors via `window.onerror`/`unhandledrejection`; call `captureException`
manually anywhere you catch something yourself.

## API surface

```ts
initAutterBrowser({ endpoint, clientKey?, service, environment?, release?, sessionTracking?, beforeSend? });
captureException(error, context?);       // report a caught error
captureMessage(message, severity?, context?); // warning/info without an exception — severity "fatal"|"error"|"warning"|"info", default "warning"
trackEvent(name, props?);                 // coarse usage counter — no PII in props
setUser(id | null);                       // opaque id ONLY — never an email/name
setContext(context | null);               // merged into every subsequent event
flush();                                   // force-send the queue now (rarely needed — auto-flushes)
```

Warnings share the errors table server-side (a `severity` column), so
`captureMessage` calls group and aggregate exactly like errors. While
instrumenting, add it to warning-worthy paths: recoverable failures,
degraded API responses, deprecated feature usage. Keep messages as stable
templates (numbers are normalised out server-side) and PII-free.

`props`/`context` values must be primitives or small objects — never pass
emails, form fields, cookies, or request/response bodies through
`setUser`/`setContext`/`trackEvent`; the package doesn't scrub these for
you (it's explicitly zero-dep, no PII redaction layer).

## Selftest (console — nothing to install or clean up)

After init, run this in the devtools console (any page where the tracker
is loaded) to exercise both event families and force the send:

```js
captureMessage("autter selftest", "info"); // error/warning pipeline
trackEvent("autter_selftest");             // usage-metrics pipeline
flush();                                   // skip the batch window
```

## Verify

1. Load the app, open the devtools network tab, run the selftest above.
2. Confirm a POST fires to the relay route or `/v1/browser` and comes
   back `202` — body `{"accepted":N}` from the ingester; a relay replies
   `202` immediately and forwards in the background.
3. The selftest proves init + transport, not the automatic hooks — so
   also trigger one real error (throw inside a component render, or
   `Promise.reject(new Error("test"))` in the console) and confirm
   another request fires within ~500ms (errors flush fast — 500ms
   debounce, not the normal 5s batch window).
4. Direct-key mode only: a `403` here means the current origin isn't on
   the key's allow-list — check it was registered with the exact origin
   (scheme + host + port) the app is running on.
5. Ground truth in the dashboard (~1–2 min): one info-severity
   "autter selftest" issue and a usage counter `event:autter_selftest` —
   both clearly named; the user can resolve or ignore them.
