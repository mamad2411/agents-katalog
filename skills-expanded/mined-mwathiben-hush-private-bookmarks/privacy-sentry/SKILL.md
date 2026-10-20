---
name: privacy-sentry
description: "Enforces privacy-safe Sentry configuration for Hush Private Bookmarks. Triggers on any code importing @sentry/browser, calling Sentry.init, Sentry.captureException, Sentry.captureMessage, Sentry.setUser, Sentry.setContext, Sentry.setExtra, Sentry.setTag, Sentry.addBreadcrumb, beforeSend, beforeBreadcrumb, or files containing 'sentry' in the path. Prevents known Claude failure modes: auto-captured URLs via HttpContext, navigation breadcrumbs leaking page history, BrowserTracing sending URL-based transactions, Session Replay recording DOM, error messages interpolating bookmark titles, and sendDefaultPii enabling IP collection."
---

# Privacy-Safe Sentry — Hush Private Bookmarks

Proactive guardrail for all Sentry error reporting code in this project. Every rule is non-negotiable. Violations are privacy breaches that destroy the product's entire value proposition.

Hush Private Bookmarks is a privacy-first encrypted bookmarks browser extension. Users trust it to hide their bookmarks from everyone — including the developer. If Sentry captures a single bookmark URL, title, or password fragment, that trust is irreversibly broken.

**Scope**: All files importing `@sentry/browser`, any file in `lib/sentry*`, any entrypoint initializing Sentry, any code calling `Sentry.*` methods, any error class that may be captured by Sentry, any `beforeSend` or `beforeBreadcrumb` hook.

---

## When to Activate

```text
File imports @sentry/browser? ──────────────yes──▶ ACTIVATE
                │
                no
                │
File path matches *sentry*? ────────────────yes──▶ ACTIVATE
                │
                no
                │
Code calls Sentry.init or Sentry.capture*? ─yes──▶ ACTIVATE
                │
                no
                │
Code calls Sentry.setUser/setContext/setExtra/setTag? ─yes──▶ ACTIVATE
                │
                no
                │
Code calls Sentry.addBreadcrumb? ───────────yes──▶ ACTIVATE
                │
                no
                │
Code defines beforeSend or beforeBreadcrumb? ─yes──▶ ACTIVATE
                │
                no
                │
Code throws/catches errors that Sentry will capture? ─yes──▶ ACTIVATE
                │
                no
                │
Code defines custom error classes? ──────────yes──▶ ACTIVATE
                │
                no
                │
SKIP
```

**Keyword triggers**: `Sentry`, `@sentry/browser`, `captureException`, `captureMessage`, `beforeSend`, `beforeBreadcrumb`, `beforeSendTransaction`, `dsn`, `sentry.io`, `breadcrumb`, `setUser`, `setContext`, `setExtra`, `setTag`, `addBreadcrumb`, `replayIntegration`, `browserTracingIntegration`, `sendDefaultPii`, `skipBrowserExtensionCheck`.

## When NOT to Activate

- React components that only display error UI to the user (no Sentry calls)
- Unit tests that mock Sentry (but verify the mocks enforce these rules)
- Documentation files describing the error reporting strategy

---

## Quick Reference

| Parameter | Required Value | Violation Severity |
|-----------|---------------|-------------------|
| `sendDefaultPii` | `false` (explicit, never omit) | CRITICAL |
| `defaultIntegrations` | `false` (reconstruct allowlist) | CRITICAL |
| `skipBrowserExtensionCheck` | `true` (required for WXT) | HIGH |
| `beforeSend` | Must strip `request`, `transaction`, `user`, `extra.arguments`, `server_name` | CRITICAL |
| `beforeSendTransaction` | Return `null` (drop all transactions) | CRITICAL |
| `beforeBreadcrumb` | Drop any breadcrumb with URL data | HIGH |
| BrowserTracing | NEVER add | CRITICAL |
| Session Replay | NEVER add | CRITICAL |
| HttpContext integration | NEVER include | CRITICAL |
| BrowserSession integration | NEVER include | HIGH |
| Breadcrumbs integration | Only with `{ console: false, dom: false, fetch: false, history: false, xhr: false }` | CRITICAL |
| `Sentry.setUser()` | NEVER call with email, username, or IP | CRITICAL |
| `Sentry.setContext()` | NEVER pass bookmark data | CRITICAL |
| `Sentry.setExtra()` / `setTag()` | NEVER pass URLs, titles, or user data | CRITICAL |
| `Sentry.addBreadcrumb()` | NEVER pass URLs, titles, or user data | CRITICAL |
| `Sentry.captureMessage()` | NEVER interpolate user data into message | CRITICAL |
| Error messages | Zero PII — no URLs, no bookmark titles, no key bytes, no password fragments | CRITICAL |
| DSN | Public-facing in source code — this is expected and safe | INFO |

---

## Sensitive Data in This Project

These data types exist in the codebase and must NEVER reach Sentry:

| Data Type | Where It Lives | Why It's Sensitive |
|-----------|---------------|-------------------|
| Bookmark URLs | `Bookmark.url`, decrypted payloads | User's browsing history — the core secret |
| Bookmark titles | `Bookmark.title`, decrypted payloads | User-defined labels, often descriptive |
| Master password | Function parameters, `TextEncoder` input | Root encryption key |
| Recovery phrases | `@scure/bip39` output, `generateMnemonic()` return | Vault recovery seed — full compromise if leaked |
| Encryption keys | `CryptoKey` objects, `deriveKey()` output | AES-256-GCM key material |
| Salt values | `Uint8Array`, stored alongside ciphertext | Weakens PBKDF2 if correlated with other data |
| IV/nonce values | `Uint8Array`, prepended to ciphertext | IV reuse detection enables cryptanalysis |
| Plaintext data | Pre-encryption or post-decryption buffers | The user's actual secrets |
| Extension ID | `chrome-extension://[id]/` in stack frames | Per-installation fingerprint |

---

## Data Leak Vector Reference

Every field on a Sentry `Event` object that can contain user data, what populates it, and the required action.

| Event Field | Auto-Populated By | Contains | Action |
|-------------|-------------------|----------|--------|
| `event.request.url` | `HttpContext` integration (DEFAULT ON) | Current page URL (`chrome-extension://[id]/popup.html`) | **Remove HttpContext entirely** |
| `event.request.headers.Referer` | `HttpContext` integration | Previous page URL | **Remove HttpContext entirely** |
| `event.request.headers['User-Agent']` | `HttpContext` integration | Browser fingerprint string | **Remove HttpContext entirely** |
| `event.breadcrumbs[]` (navigation) | `Breadcrumbs` integration `history: true` (DEFAULT ON) | `{ from: "/path", to: "/path" }` — full URL paths | **Disable `history: false`** |
| `event.breadcrumbs[]` (fetch) | `Breadcrumbs` integration `fetch: true` (DEFAULT ON) | `{ method, url, status_code }` — full fetch URLs | **Disable `fetch: false`** |
| `event.breadcrumbs[]` (xhr) | `Breadcrumbs` integration `xhr: true` (DEFAULT ON) | `{ method, url, status_code }` — full XHR URLs | **Disable `xhr: false`** |
| `event.breadcrumbs[]` (console) | `Breadcrumbs` integration `console: true` (DEFAULT ON) | Full `console.log()` arguments | **Disable `console: false`** |
| `event.breadcrumbs[]` (dom) | `Breadcrumbs` integration `dom: true` (DEFAULT ON) | Clicked element HTML with text/attributes | **Disable `dom: false`** |
| `event.transaction` | `BrowserTracing` integration | `window.location.pathname` — URL path as transaction name | **Never add BrowserTracing** |
| `event.exception.values[].stacktrace.frames[].filename` | `GlobalHandlers` integration | `chrome-extension://[id]/popup.js` — reveals extension ID | **Scrub in beforeSend** |
| `event.exception.values[].stacktrace.frames[].abs_path` | `GlobalHandlers` integration | Absolute file path with extension ID | **Delete in beforeSend** |
| `event.exception.values[].value` | The thrown error's `.message` | Whatever the developer put in the error message | **Never interpolate PII into error messages** |
| `event.user` | `Sentry.setUser()` or `sendDefaultPii: true` | `id`, `email`, `username`, `ip_address` | **Never call setUser with PII; sendDefaultPii: false** |
| `event.extra` | `Sentry.setExtra()` or `wrap()` helper | Arbitrary data; `wrap()` dumps function arguments | **Delete `extra.arguments` in beforeSend** |
| `event.tags` | `Sentry.setTag()` or integrations | Arbitrary key-value pairs; some integrations add `url` tag | **Never set tags with user data** |
| `event.contexts.trace.data` | `BrowserTracing` span attributes | `http.url`, `http.query`, `http.fragment`, `server.address` | **Delete in beforeSend** |
| `event.contexts.culture` | `CultureContext` integration (DEFAULT ON) | `locale`, `timezone`, `calendar` — minor fingerprinting | **Remove CultureContext integration** |
| `event.server_name` | Sentry config or auto-detection | Hostname of the machine | **Delete in beforeSend** |
| `event.message` | `Sentry.captureMessage()` | Whatever string was passed | **Never interpolate PII** |
| Session envelope `attrs.user_agent` | `BrowserSession` integration (DEFAULT ON) | Full User-Agent string | **Remove BrowserSession integration** |
| Session envelope `attrs.ip_address` | `BrowserSession` + `sendDefaultPii` | User's IP address | **Remove BrowserSession integration** |
| Replay recording | `Replay` integration (NOT default) | Full DOM snapshots, URL history, network bodies | **Never add Replay** |
| Transaction spans | `BrowserTracing` (NOT default) | `http.url` on every fetch/XHR span | **Never add BrowserTracing** |

---

## Integration Allowlist / Blocklist

### ALLOWED — Safe to include

| Integration | Why Safe |
|-------------|---------|
| `inboundFiltersIntegration()` | Filters events by error message patterns — no data collection |
| `functionToStringIntegration()` | Patches `Function.prototype.toString` for Sentry wrappers — no data |
| `dedupeIntegration()` | Prevents duplicate events — no data collection |
| `linkedErrorsIntegration()` | Traverses `error.cause` chain — no new data, just links existing errors |
| `globalHandlersIntegration({ onerror: true, onunhandledrejection: true })` | Catches unhandled errors — filenames need scrubbing in beforeSend but otherwise safe |

### FORBIDDEN — Never include

| Integration | Why Forbidden |
|-------------|--------------|
| `httpContextIntegration()` | Auto-sets `event.request.url` to current page URL on EVERY event |
| `browserSessionIntegration()` | Sends session envelopes with `user_agent` and `ip_address` |
| `cultureContextIntegration()` | Sends `locale` + `timezone` — browser fingerprinting data |
| `browserTracingIntegration()` | Sets `transaction` to URL path; creates spans with full fetch/XHR URLs |
| `replayIntegration()` | Records DOM mutations, URL navigation history, network request bodies |
| `browserProfilingIntegration()` | Profiling data contains stack traces with full file paths |
| `feedbackIntegration()` | Captures user-typed text and email |
| `breadcrumbsIntegration()` (with defaults) | All sub-types enabled by default capture URLs |

### CONDITIONALLY ALLOWED — Only with explicit safety config

| Integration | Required Config |
|-------------|----------------|
| `breadcrumbsIntegration({ console: false, dom: false, fetch: false, history: false, xhr: false, sentry: true })` | All URL-bearing sub-types disabled; only Sentry event breadcrumbs kept |

---

## Hard Rules

### Rule 1: `sendDefaultPii` must be explicitly `false`

When `sendDefaultPii` is `true`, Sentry auto-populates `event.user.ip_address` from the client's IP and includes cookies in `event.request.cookies`. The default is `false`, but it must be set explicitly to prevent accidental changes.

**WRONG — omitted (relies on default):**
```typescript
Sentry.init({
  dsn: "https://...",
  // sendDefaultPii not specified — future SDK version could change default
});
```

**WRONG — enabled:**
```typescript
Sentry.init({
  dsn: "https://...",
  sendDefaultPii: true, // leaks IP address in every session envelope
});
```

**CORRECT:**
```typescript
Sentry.init({
  dsn: "https://...",
  sendDefaultPii: false, // explicit — never send PII automatically
});
```

---

### Rule 2: `defaultIntegrations: false` — reconstruct allowlist

Sentry's default integrations include `HttpContext` (auto-captures current URL), `Breadcrumbs` (captures navigation/fetch/xhr URLs), `BrowserSession` (sends user_agent + ip_address), and `CultureContext` (locale + timezone). All four leak data. Disable all defaults and explicitly add only the safe ones.

**WRONG — using defaults:**
```typescript
Sentry.init({
  dsn: "https://...",
  // defaultIntegrations not set — HttpContext, Breadcrumbs, BrowserSession all active
});
```

**WRONG — trying to remove individual integrations (fragile, depends on SDK version):**
```typescript
Sentry.init({
  dsn: "https://...",
  integrations: (defaults) => defaults.filter(i => i.name !== "HttpContext"),
  // Still includes BrowserSession, CultureContext, and default Breadcrumbs
});
```

**CORRECT:**
```typescript
Sentry.init({
  dsn: "https://...",
  defaultIntegrations: false,
  integrations: [
    Sentry.inboundFiltersIntegration(),
    Sentry.functionToStringIntegration(),
    Sentry.dedupeIntegration(),
    Sentry.linkedErrorsIntegration(),
    Sentry.globalHandlersIntegration({ onerror: true, onunhandledrejection: true }),
  ],
});
```

---

### Rule 3: No URL-capturing breadcrumbs

The `Breadcrumbs` integration has six sub-types, five of which capture URLs or user-visible content. If included at all, every sub-type except `sentry` must be explicitly disabled.

**WRONG — breadcrumbs with defaults:**
```typescript
Sentry.init({
  integrations: [
    Sentry.breadcrumbsIntegration(), // all sub-types ON: history, fetch, xhr, console, dom
  ],
});
```

**WRONG — disabling only some:**
```typescript
Sentry.init({
  integrations: [
    Sentry.breadcrumbsIntegration({ history: false, fetch: false }),
    // xhr, console, dom still ON — XHR breadcrumbs capture full request URLs
  ],
});
```

**CORRECT — all URL-bearing sub-types disabled:**
```typescript
Sentry.init({
  integrations: [
    Sentry.breadcrumbsIntegration({
      console: false,
      dom: false,
      fetch: false,
      history: false,
      xhr: false,
      sentry: true,
    }),
  ],
});
```

**CORRECT — omit breadcrumbs entirely:**
```typescript
Sentry.init({
  defaultIntegrations: false,
  integrations: [
    // breadcrumbsIntegration not included at all
  ],
});
```

---

### Rule 4: Never add Session Replay

`replayIntegration()` records full DOM mutations, URL navigation history, and network request/response bodies. It is the single most dangerous integration for a privacy extension.

**WRONG:**
```typescript
import { replayIntegration } from "@sentry/browser";

Sentry.init({
  integrations: [
    replayIntegration(), // records everything the user sees and does
  ],
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});
```

**WRONG — "disabled" via sample rate (still initializes, still hooks DOM):**
```typescript
Sentry.init({
  integrations: [
    replayIntegration(),
  ],
  replaysSessionSampleRate: 0,
  replaysOnErrorSampleRate: 0,
});
```

**CORRECT:**
```typescript
// Do not import replayIntegration at all.
// Do not reference replaysSessionSampleRate or replaysOnErrorSampleRate.
// The integration must never appear in the integrations array.
```

---

### Rule 5: Never add BrowserTracing

`browserTracingIntegration()` sets `event.transaction` to `window.location.pathname` and creates spans for every fetch/XHR call with full URLs in span attributes (`http.url`, `http.query`, `http.fragment`, `server.address`).

**WRONG:**
```typescript
import { browserTracingIntegration } from "@sentry/browser";

Sentry.init({
  integrations: [
    browserTracingIntegration(), // transaction = URL path, spans = fetch URLs
  ],
  tracesSampleRate: 1.0,
});
```

**CORRECT:**
```typescript
// Do not import browserTracingIntegration at all.
// Do not reference tracesSampleRate or tracePropagationTargets.
// The integration must never appear in the integrations array.
```

---

### Rule 6: Never set user identifiers

`Sentry.setUser()` attaches PII to every subsequent event. In this extension, there are no user accounts and no reason to identify users.

**WRONG:**
```typescript
Sentry.setUser({ email: "user@example.com" });
Sentry.setUser({ id: uniqueInstallId });
Sentry.setUser({ ip_address: "auto" }); // tells Sentry server to use the client IP
```

**CORRECT:**
```typescript
// Never call Sentry.setUser().
// If you must distinguish installations for error grouping,
// use a non-reversible, non-identifying value:
Sentry.setUser({ id: "anonymous" });
// Or better — don't call setUser at all.
```

---

### Rule 7: `beforeSend` must strip all PII fields

Even with safe integrations, defense-in-depth requires `beforeSend` to strip every field that could contain user data. This is the last line of defense if a future SDK version changes behavior or a developer accidentally adds a leaky integration.

**WRONG — no beforeSend:**
```typescript
Sentry.init({
  dsn: "https://...",
  // no beforeSend — relies entirely on integration config
});
```

**WRONG — beforeSend that only strips some fields:**
```typescript
Sentry.init({
  beforeSend(event) {
    delete event.request; // good
    return event;
    // forgot: transaction, user, extra.arguments, server_name, contexts.trace.data
  },
});
```

**CORRECT — see the Canonical beforeSend Template section below for the full implementation.**

---

### Rule 8: Scrub extension IDs from stack frame filenames

Stack frame `filename` and `abs_path` fields contain `chrome-extension://[unique-id]/file.js`. The extension ID is a per-installation fingerprint in development and a stable per-extension identifier on the Chrome Web Store. Scrub it to prevent tracking.

**WRONG — leaving filenames as-is:**
```typescript
beforeSend(event) {
  // no frame scrubbing — extension ID visible in every stack trace
  return event;
}
```

**CORRECT:**
```typescript
if (event.exception?.values) {
  for (const ex of event.exception.values) {
    if (ex.stacktrace?.frames) {
      for (const frame of ex.stacktrace.frames) {
        if (frame.filename) {
          frame.filename = frame.filename
            .replace(/chrome-extension:\/\/[^/]+/, "extension://_")
            .replace(/moz-extension:\/\/[^/]+/, "extension://_");
        }
        delete frame.abs_path;
      }
    }
  }
}
```

---

### Rule 9: DSN is public-facing — never hide it

The Sentry DSN is embedded in the extension's JavaScript bundle, which is publicly downloadable from the Chrome Web Store. Treating it as a secret (env vars, build-time injection, obfuscation) provides zero security and adds complexity. The DSN only authorizes sending events to a specific Sentry project — it cannot read events or access project settings.

**WRONG — unnecessary env var indirection:**
```typescript
Sentry.init({
  dsn: process.env.SENTRY_DSN, // undefined at runtime in browser extension
});
```

**WRONG — import.meta.env that may be stripped:**
```typescript
Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN, // requires build config, may be undefined
});
```

**CORRECT:**
```typescript
const SENTRY_DSN = "https://examplePublicKey@o0.ingest.sentry.io/0";

Sentry.init({
  dsn: SENTRY_DSN,
});
```

---

### Rule 10: No console breadcrumbs

If `Breadcrumbs` is included with `console: true` (the default), every `console.log()` call's arguments are captured as breadcrumb data. If any code path logs a URL, title, or error detail, it reaches Sentry.

**WRONG:**
```typescript
console.log("Encrypting bookmark:", bookmark.title); // title in Sentry breadcrumb
console.error("Failed to load:", bookmark.url);      // URL in Sentry breadcrumb
```

**CORRECT:**
```typescript
// 1. Never console.log sensitive data (CLAUDE.md rule: no console.log in production)
// 2. If breadcrumbs are included at all, console: false is mandatory
Sentry.breadcrumbsIntegration({ console: false, /* ... */ })
```

---

### Rule 11: Strip `event.contexts.trace.data`

If BrowserTracing is accidentally added (violating Rule 5), the trace context's `data` field contains `http.url`, `http.query`, `http.fragment`, and `server.address` from every fetch/XHR span. Strip it as defense-in-depth.

**CORRECT (in beforeSend):**
```typescript
if (event.contexts?.trace) {
  delete event.contexts.trace.data;
}
```

---

### Rule 12: Error messages must never contain PII

Every `throw new Error(...)`, `throw new CryptoError(...)`, and `Sentry.captureMessage(...)` string is sent to Sentry verbatim in `event.exception.values[].value` or `event.message`. Never interpolate bookmark URLs, titles, passwords, or key material into error messages.

**WRONG:**
```typescript
throw new Error(`Failed to encrypt bookmark: ${bookmark.title}`);
throw new CryptoError(`Decryption failed for ${bookmark.url}`, "decrypt");
throw new StorageError(`Cannot save bookmark "${title}" to storage`);
Sentry.captureMessage(`User bookmarked ${url}`);
```

**CORRECT:**
```typescript
throw new CryptoError("Encryption failed", "encrypt", { cause });
throw new CryptoError("Decryption failed — wrong password or corrupted data", "decrypt", { cause });
throw new StorageError("Failed to write encrypted payload to storage", { cause });
// Never call captureMessage with user data. If you must, use a static string:
Sentry.captureMessage("Bookmark storage write failed");
```

---

## Canonical Sentry.init() Template

Copy this exactly when initializing Sentry in any entrypoint. Do not modify the integration list or beforeSend without reading every rule in this document.

```typescript
import * as Sentry from "@sentry/browser";
import type { ErrorEvent, EventHint, TransactionEvent, Breadcrumb } from "@sentry/browser";

const SENTRY_DSN = "https://examplePublicKey@o0.ingest.sentry.io/0";

function scrubEvent(event: ErrorEvent, _hint: EventHint): ErrorEvent | null {
  // 1. Delete request — contains current page URL, Referer, User-Agent
  delete event.request;

  // 2. Delete transaction — contains URL path if BrowserTracing is active
  delete event.transaction;

  // 3. Strip user PII — keep only anonymous marker if set
  if (event.user) {
    event.user = { id: event.user.id };
  }

  // 4. Delete server_name — hostname, should not be present in browser but be explicit
  delete event.server_name;

  // 5. Strip wrap() helper's function arguments from extra
  if (event.extra) {
    delete (event.extra as Record<string, unknown>)["arguments"];
  }

  // 6. Strip trace context data — may contain http.url span attributes
  if (event.contexts?.trace) {
    delete event.contexts.trace.data;
  }

  // 7. Delete message if it somehow contains URL-like patterns (defense-in-depth)
  if (event.message) {
    event.message = stripUrlsFromString(event.message);
  }

  // 8. Scrub exception messages and stack frame filenames
  if (event.exception?.values) {
    for (const ex of event.exception.values) {
      // Scrub the error message — should already be PII-free, but defense-in-depth
      if (ex.value) {
        ex.value = stripUrlsFromString(ex.value);
      }

      // Scrub stack frame paths
      if (ex.stacktrace?.frames) {
        for (const frame of ex.stacktrace.frames) {
          if (frame.filename) {
            frame.filename = frame.filename
              .replace(/chrome-extension:\/\/[^/]+/, "extension://_")
              .replace(/moz-extension:\/\/[^/]+/, "extension://_");
          }
          delete frame.abs_path;
        }
      }
    }
  }

  // 9. Strip any remaining breadcrumbs that slipped through
  if (event.breadcrumbs) {
    event.breadcrumbs = event.breadcrumbs.filter((crumb) => {
      if (crumb.category === "navigation") return false;
      if (crumb.type === "http") return false;
      if (crumb.category === "fetch" || crumb.category === "xhr") return false;
      if (crumb.category === "console") return false;
      if (crumb.data?.url) return false;
      return true;
    });
  }

  // 10. Strip tags that might contain URLs
  if (event.tags) {
    delete event.tags["url"];
    delete event.tags["transaction"];
  }

  return event;
}

function stripUrlsFromString(str: string): string {
  return str
    .replace(/https?:\/\/[^\s"'<>)}\]]+/g, "[URL_STRIPPED]")
    .replace(/chrome-extension:\/\/[^\s"'<>)}\]]+/g, "[EXT_URL_STRIPPED]")
    .replace(/moz-extension:\/\/[^\s"'<>)}\]]+/g, "[EXT_URL_STRIPPED]");
}

export function initSentry(): void {
  Sentry.init({
    dsn: SENTRY_DSN,
    sendDefaultPii: false,
    skipBrowserExtensionCheck: true,
    defaultIntegrations: false,

    integrations: [
      Sentry.inboundFiltersIntegration(),
      Sentry.functionToStringIntegration(),
      Sentry.dedupeIntegration(),
      Sentry.linkedErrorsIntegration(),
      Sentry.globalHandlersIntegration({
        onerror: true,
        onunhandledrejection: true,
      }),
    ],

    beforeSend: scrubEvent,

    beforeSendTransaction: (_event: TransactionEvent): TransactionEvent | null => {
      // Drop ALL transactions — we do not use BrowserTracing,
      // but if it's accidentally added, this prevents URL leaks
      return null;
    },

    beforeBreadcrumb: (breadcrumb: Breadcrumb): Breadcrumb | null => {
      // Secondary defense: drop URL-bearing breadcrumbs at source
      if (breadcrumb.data?.url) return null;
      if (breadcrumb.category === "navigation") return null;
      if (breadcrumb.type === "http") return null;
      if (breadcrumb.category === "fetch" || breadcrumb.category === "xhr") return null;
      if (breadcrumb.category === "console") return null;
      return breadcrumb;
    },
  });
}
```

---

## Claude-Specific Pitfalls

These are failure modes observed in Claude-generated Sentry code. Each one has been seen in practice or is a high-probability mistake given Claude's training data.

### Pitfall 1: Using `sendDefaultPii: true`

Claude has been trained on many Sentry tutorials that set `sendDefaultPii: true` for "better error context." In this project, it enables automatic IP address collection via session envelopes.

**WRONG:**
```typescript
Sentry.init({
  dsn: "https://...",
  sendDefaultPii: true, // "recommended" in many tutorials
});
```

**CORRECT:**
```typescript
Sentry.init({
  dsn: "https://...",
  sendDefaultPii: false,
});
```

---

### Pitfall 2: Forgetting to disable HttpContext integration

`HttpContext` is a DEFAULT integration. It runs as a `preprocessEvent` hook on EVERY event, setting `event.request.url` to `window.document.location.href` — the full current page URL including the extension ID.

Claude typically forgets about this because most Sentry guides don't mention it — it's an invisible default.

**WRONG — defaults include HttpContext:**
```typescript
Sentry.init({
  dsn: "https://...",
  // HttpContext is silently active, setting event.request.url on every event
});
```

**WRONG — filtering approach (fragile):**
```typescript
Sentry.init({
  integrations: (defaults) => defaults.filter(i => i.name !== "HttpContext"),
  // May miss BrowserSession, CultureContext, Breadcrumbs defaults
});
```

**CORRECT:**
```typescript
Sentry.init({
  defaultIntegrations: false,
  integrations: [
    // Explicitly list only safe integrations — HttpContext is NOT here
  ],
});
```

---

### Pitfall 3: Adding BrowserTracing "for performance monitoring"

Claude frequently suggests BrowserTracing when discussing Sentry setup because it appears in most Sentry documentation. BrowserTracing sets `event.transaction` to `window.location.pathname` and creates spans with `http.url` for every fetch/XHR call.

**WRONG:**
```typescript
import { browserTracingIntegration } from "@sentry/browser";

Sentry.init({
  integrations: [
    browserTracingIntegration(), // "for performance monitoring"
  ],
  tracesSampleRate: 0.1,
});
```

**WRONG — "disabled" via sample rate (integration still hooks fetch/navigation):**
```typescript
Sentry.init({
  integrations: [
    browserTracingIntegration(),
  ],
  tracesSampleRate: 0, // integration is still initialized and patching APIs
});
```

**CORRECT:**
```typescript
// Do not import browserTracingIntegration.
// Do not set tracesSampleRate.
// Do not set tracePropagationTargets.
```

---

### Pitfall 4: Adding Replay "for debugging production issues"

Session Replay records full DOM mutations, URL navigation history, user clicks with element text, and optionally network request/response bodies. It is the highest-risk integration for a privacy extension. Claude suggests it because Sentry's own documentation promotes it aggressively.

**WRONG:**
```typescript
import { replayIntegration } from "@sentry/browser";

Sentry.init({
  integrations: [
    replayIntegration({
      maskAllText: true,      // still records URL navigation
      blockAllMedia: true,    // still records DOM structure
      maskAllInputs: true,    // still captures page transitions
    }),
  ],
});
```

**CORRECT:**
```typescript
// Never import replayIntegration.
// Never reference replaysSessionSampleRate or replaysOnErrorSampleRate.
// Even with masking options, Replay still tracks URL history and DOM structure.
```

---

### Pitfall 5: Breadcrumbs default sub-types are all ON

When `breadcrumbsIntegration()` is called without arguments, ALL six sub-types are enabled: `console`, `dom`, `fetch`, `history`, `xhr`, `sentry`. Five of the six capture URLs or user-visible content.

Claude typically adds `breadcrumbsIntegration()` without arguments because that's how examples appear in documentation.

**WRONG:**
```typescript
Sentry.init({
  integrations: [
    Sentry.breadcrumbsIntegration(), // all defaults ON
  ],
});
```

**What this captures:**
- `history`: Every navigation as `{ from: "/path", to: "/path" }` — full URL paths
- `fetch`: Every fetch as `{ method: "GET", url: "https://api.example.com/bookmarks" }` — full URLs
- `xhr`: Same as fetch for XMLHttpRequest
- `console`: Every `console.log()` argument verbatim
- `dom`: Clicked element as HTML string: `<button class="delete-btn">Delete "My Secret Bookmark"</button>`

**CORRECT:**
```typescript
Sentry.init({
  integrations: [
    Sentry.breadcrumbsIntegration({
      console: false,
      dom: false,
      fetch: false,
      history: false,
      xhr: false,
      sentry: true,
    }),
  ],
});
```

---

### Pitfall 6: `Sentry.setContext()` with bookmark data

Claude adds `setContext` calls to provide "helpful debugging context." In this project, any bookmark data in context is a privacy violation.

**WRONG:**
```typescript
Sentry.setContext("bookmark", {
  title: bookmark.title,
  url: bookmark.url,
  folder: bookmark.folder,
});
```

**WRONG — "sanitized" but still leaky:**
```typescript
Sentry.setContext("operation", {
  action: "encrypt",
  target: bookmark.url.substring(0, 20), // still 20 chars of the URL
});
```

**CORRECT:**
```typescript
Sentry.setContext("operation", {
  action: "encrypt",
  itemCount: bookmarks.length,
});
// Only non-identifying, aggregate data
```

---

### Pitfall 7: `Sentry.setExtra()` or `Sentry.setTag()` with user data

Similar to setContext, Claude adds extra data for "debugging." Tags are indexed and searchable in Sentry's UI, making leaked URLs even more accessible.

**WRONG:**
```typescript
Sentry.setTag("page", window.location.href);
Sentry.setExtra("failedBookmark", JSON.stringify(bookmark));
Sentry.setExtra("lastAction", `Encrypted ${bookmark.title}`);
```

**CORRECT:**
```typescript
Sentry.setTag("entrypoint", "popup"); // static, non-identifying
Sentry.setTag("action", "encrypt");   // generic operation type
// Never pass dynamic user data to setExtra or setTag
```

---

### Pitfall 8: Error messages containing bookmark titles or URLs

Claude interpolates context into error messages for "better debugging." In Sentry, `error.message` is sent verbatim as `event.exception.values[].value`.

**WRONG:**
```typescript
throw new Error(`Failed to encrypt bookmark: ${bookmark.title}`);
throw new Error(`Storage write failed for ${bookmark.url}`);
throw new CryptoError(`Cannot decrypt "${title}"`, "decrypt");
throw new StorageError(`Bookmark "${title}" not found in folder "${folder}"`);
```

**WRONG — JSON.stringify leaks everything:**
```typescript
throw new Error(`Operation failed: ${JSON.stringify(bookmark)}`);
```

**CORRECT:**
```typescript
throw new CryptoError("Encryption failed", "encrypt", { cause });
throw new StorageError("Storage write failed for encrypted payload", { cause });
// Error message is a static string. Dynamic context stays in `cause` (a DOMException or TypeError).
// cause is traversed by linkedErrorsIntegration but DOMExceptions don't contain user data.
```

---

### Pitfall 9: `Sentry.captureMessage()` with interpolated user data

Claude uses `captureMessage` for custom logging. The message string is sent to Sentry as `event.message`.

**WRONG:**
```typescript
Sentry.captureMessage(`User decrypted ${bookmarks.length} bookmarks from ${folderName}`);
Sentry.captureMessage(`Failed to load bookmark: ${bookmark.url}`);
Sentry.captureMessage(`Password attempt for vault: ${vaultId}`);
```

**CORRECT:**
```typescript
Sentry.captureMessage("Bulk decryption completed");
Sentry.captureMessage("Bookmark load failed");
// Or better — use captureException with a typed error class instead of captureMessage
```

---

### Pitfall 10: `window.crypto` in service worker context

MV3 background scripts are service workers with no `window` global. This applies to both crypto code AND Sentry initialization. Sentry's HttpContext integration calls `window.document.location.href` — which throws in a service worker.

**WRONG:**
```typescript
// In background.ts (service worker):
window.Sentry = Sentry; // ReferenceError: window is not defined
```

**CORRECT:**
```typescript
// In background.ts (service worker):
// Sentry.init() works fine in service workers as long as HttpContext is removed
// (HttpContext tries to read window.document.location.href)
// Our config already excludes HttpContext via defaultIntegrations: false
```

---

### Pitfall 11: Forgetting `skipBrowserExtensionCheck: true`

Sentry v10 detects browser extension contexts and logs a warning (or silently disables the SDK in content scripts). WXT extensions need `skipBrowserExtensionCheck: true` to run in popup/options pages.

**WRONG:**
```typescript
Sentry.init({
  dsn: "https://...",
  // SDK may silently disable itself in extension context
});
```

**CORRECT:**
```typescript
Sentry.init({
  dsn: "https://...",
  skipBrowserExtensionCheck: true,
});
```

Note: Sentry in content scripts (injected into `https://` pages) is deliberately blocked by Sentry's detection and should NOT be bypassed. Only initialize Sentry in dedicated extension pages (popup, options, manager) and the background service worker.

---

### Pitfall 12: `beforeSend` returning `null` on all events

A common overcorrection: making beforeSend so aggressive that it drops EVERY event. This breaks error reporting entirely — you get zero visibility into production errors.

**WRONG:**
```typescript
beforeSend(event) {
  // "safety first" — but this means Sentry does nothing
  if (event.request || event.breadcrumbs?.length) {
    return null;
  }
  return event;
}
```

**CORRECT:**
```typescript
beforeSend(event) {
  // SCRUB the event, don't DROP it. Strip PII fields, then return the event.
  delete event.request;
  // ... (see canonical template)
  return event; // always return the scrubbed event
}
```

---

### Pitfall 13: `Sentry.addBreadcrumb()` with sensitive data

Claude adds manual breadcrumbs for "operation tracking." Manual breadcrumbs bypass integration filters and go directly into the event.

**WRONG:**
```typescript
Sentry.addBreadcrumb({
  category: "bookmark",
  message: `Saved bookmark: ${title}`,
  data: { url: bookmark.url, title: bookmark.title },
});
```

**WRONG — partial "sanitization":**
```typescript
Sentry.addBreadcrumb({
  category: "crypto",
  message: `Encrypted ${bookmarks.length} items`,
  data: { firstTitle: bookmarks[0].title }, // still leaks one title
});
```

**CORRECT:**
```typescript
Sentry.addBreadcrumb({
  category: "operation",
  message: "Bulk encryption completed",
  data: { count: bookmarks.length },
  level: "info",
});
// Only static messages and numeric/boolean data
```

---

### Pitfall 14: `beforeSendTransaction` not configured

If BrowserTracing is accidentally added (violating Rule 5), transaction events are sent separately from error events. `beforeSend` does NOT run on transactions. A separate `beforeSendTransaction` hook is required.

**WRONG — no beforeSendTransaction:**
```typescript
Sentry.init({
  beforeSend: scrubEvent,
  // Transactions bypass beforeSend entirely — URL-based transaction names reach Sentry
});
```

**CORRECT:**
```typescript
Sentry.init({
  beforeSend: scrubEvent,
  beforeSendTransaction: (_event) => null, // drop ALL transactions
});
```

---

### Pitfall 15: BrowserSession integration leaking `user_agent` and `ip_address`

`BrowserSession` is a DEFAULT integration. It sends session envelopes on page load and navigation. Session envelopes contain `attrs.user_agent` (full User-Agent string, a browser fingerprint) and `attrs.ip_address` (when `sendDefaultPii: true`).

Even with `sendDefaultPii: false`, the session envelope still reaches Sentry's server with the client's IP visible in the transport layer. The Sentry server may log it depending on project settings.

**WRONG — defaults include BrowserSession:**
```typescript
Sentry.init({
  dsn: "https://...",
  // BrowserSession is silently active, sending session envelopes
});
```

**CORRECT:**
```typescript
Sentry.init({
  defaultIntegrations: false,
  integrations: [
    // BrowserSession is NOT listed — no session envelopes sent
  ],
});
```

---

### Pitfall 16: CultureContext integration leaking locale and timezone

`CultureContext` is a DEFAULT integration that sends `locale` (e.g., `"en-US"`), `timezone` (e.g., `"America/Los_Angeles"`), and `calendar` in `event.contexts.culture`. Combined with other metadata, this is browser fingerprinting data.

For a privacy extension, even minor fingerprinting vectors should be eliminated.

**WRONG — defaults include CultureContext:**
```typescript
Sentry.init({
  dsn: "https://...",
  // CultureContext silently active, sending locale + timezone
});
```

**CORRECT:**
```typescript
Sentry.init({
  defaultIntegrations: false,
  integrations: [
    // CultureContext is NOT listed
  ],
});
```

---

### Pitfall 17: Multiple Sentry.init() calls across entrypoints without consistent config

WXT extensions have multiple entrypoints (popup, background, options, manager). Each needs its own `Sentry.init()` because they run in separate JavaScript contexts. Claude may write different configs for each, with some missing privacy protections.

**WRONG — inconsistent configs:**
```typescript
// popup/main.tsx
Sentry.init({ dsn: "...", sendDefaultPii: false, defaultIntegrations: false, /* ... */ });

// background.ts
Sentry.init({ dsn: "...", sendDefaultPii: false }); // forgot defaultIntegrations: false!
// HttpContext, BrowserSession, Breadcrumbs all active in background
```

**CORRECT — single shared init function:**
```typescript
// lib/sentry.ts
export function initSentry(): void {
  Sentry.init({ /* full privacy-safe config */ });
}

// popup/main.tsx
import { initSentry } from "@/lib/sentry";
initSentry();

// background.ts
import { initSentry } from "@/lib/sentry";
initSentry();
```

---

### Pitfall 18: Catching and re-throwing with added context

Claude wraps existing error handlers with additional context that includes user data, then the re-thrown error's message contains PII.

**WRONG:**
```typescript
try {
  await encryptBookmark(bookmark);
} catch (error) {
  throw new Error(`Failed to process "${bookmark.title}": ${error.message}`);
  // Sentry captures this with the title baked into the message
}
```

**WRONG — wrapping in a new error with URL:**
```typescript
catch (error) {
  const wrapped = new StorageError(`Write failed for ${bookmark.url}`);
  wrapped.cause = error;
  throw wrapped;
}
```

**CORRECT:**
```typescript
catch (cause) {
  throw new CryptoError("Bookmark encryption failed", "encrypt", { cause });
  // Static message. Original error preserved as cause for linkedErrorsIntegration.
}
```

---

### Pitfall 19: Forgetting that `linkedErrorsIntegration` traverses `error.cause`

`linkedErrorsIntegration` (which is in our allowlist) follows the `.cause` chain and includes each linked error in the event. If any error in the chain has a message containing PII, it reaches Sentry.

This is NOT a reason to remove `linkedErrorsIntegration` — it's a reason to ensure ALL error messages in the chain are PII-free.

**WRONG:**
```typescript
const innerError = new Error(`Bookmark "${title}" corrupted`);
throw new CryptoError("Decryption failed", "decrypt", { cause: innerError });
// linkedErrorsIntegration sends innerError.message to Sentry
```

**CORRECT:**
```typescript
// Ensure every error in the chain uses static messages:
const innerError = new StorageError("Encrypted payload corrupted or truncated");
throw new CryptoError("Decryption failed — wrong password or corrupted data", "decrypt", {
  cause: innerError,
});
```

**Also safe**: `cause` being a browser-native `DOMException` or `TypeError` — these never contain user data. Only YOUR custom errors need message hygiene.

---

## Entrypoint Initialization Pattern

Each WXT entrypoint runs in an isolated JavaScript context. Sentry must be initialized once per context. Use a single shared module to guarantee consistent configuration.

```
lib/sentry.ts          ← Single source of truth for Sentry config
  ├── popup/main.tsx   ← import { initSentry } from "@/lib/sentry"; initSentry();
  ├── background.ts    ← import { initSentry } from "@/lib/sentry"; initSentry();
  ├── manager/main.tsx ← import { initSentry } from "@/lib/sentry"; initSentry();
  └── options/main.tsx ← import { initSentry } from "@/lib/sentry"; initSentry();
```

**Do NOT** initialize Sentry in content scripts. Content scripts run in the context of web pages — Sentry's browser extension detection deliberately blocks this, and we should respect that boundary.

---

## Pre-Commit Verification Checklist

Before marking any Sentry-related task as complete, verify ALL of the following.

### Configuration

- [ ] `sendDefaultPii` is explicitly `false` — not omitted, not `true`
- [ ] `defaultIntegrations` is `false` — not omitted, not using filter function
- [ ] `skipBrowserExtensionCheck` is `true`
- [ ] `beforeSend` is defined and strips: `request`, `transaction`, `user` (except anonymous id), `extra.arguments`, `server_name`, `contexts.trace.data`, `tags.url`, `tags.transaction`
- [ ] `beforeSend` scrubs extension IDs from stack frame `filename` fields
- [ ] `beforeSend` deletes `abs_path` from all stack frames
- [ ] `beforeSend` strips URL patterns from `event.message` and `exception.values[].value`
- [ ] `beforeSend` filters breadcrumbs (navigation, http, fetch, xhr, console, any with `data.url`)
- [ ] `beforeSendTransaction` returns `null` (drops all transactions)
- [ ] `beforeBreadcrumb` drops URL-bearing breadcrumbs at source
- [ ] `beforeSend` returns the scrubbed event (not `null`) — error reporting must work

### Integrations

- [ ] Integration list contains ONLY: `inboundFilters`, `functionToString`, `dedupe`, `linkedErrors`, `globalHandlers`
- [ ] `httpContextIntegration` is NOT in the list
- [ ] `browserSessionIntegration` is NOT in the list
- [ ] `cultureContextIntegration` is NOT in the list
- [ ] `breadcrumbsIntegration` is either absent OR configured with `{ console: false, dom: false, fetch: false, history: false, xhr: false }`
- [ ] `browserTracingIntegration` is NOT imported or referenced anywhere
- [ ] `replayIntegration` is NOT imported or referenced anywhere
- [ ] `browserProfilingIntegration` is NOT imported or referenced anywhere
- [ ] `feedbackIntegration` is NOT imported or referenced anywhere
- [ ] `tracesSampleRate` is NOT set (no need without BrowserTracing)
- [ ] `replaysSessionSampleRate` is NOT set (no need without Replay)
- [ ] `replaysOnErrorSampleRate` is NOT set (no need without Replay)

### No Forbidden Patterns

- [ ] Zero calls to `Sentry.setUser()` with `email`, `username`, or `ip_address`
- [ ] Zero calls to `Sentry.setContext()` with bookmark URLs, titles, or passwords
- [ ] Zero calls to `Sentry.setExtra()` with user data
- [ ] Zero calls to `Sentry.setTag()` with URLs or user data
- [ ] Zero calls to `Sentry.addBreadcrumb()` with URLs, titles, or user data
- [ ] Zero calls to `Sentry.captureMessage()` with interpolated user data
- [ ] Zero error messages (`throw new Error(...)`) containing bookmark URLs, titles, passwords, or key material
- [ ] Zero `console.log()` calls with sensitive data in production code
- [ ] Zero uses of `window.crypto` or `window.location` — use `globalThis` equivalents

### Architecture

- [ ] Sentry init lives in `lib/sentry.ts` — single source of truth
- [ ] `lib/sentry.ts` has zero React/DOM imports
- [ ] Every entrypoint (popup, background, manager, options) calls `initSentry()` from `lib/sentry.ts`
- [ ] Content scripts do NOT initialize Sentry
- [ ] DSN is a plain string constant — not env var, not build-time injection
- [ ] Custom error classes (`CryptoError`, `StorageError`, etc.) use static messages only

### Testing

- [ ] Unit test verifies `beforeSend` strips `event.request`
- [ ] Unit test verifies `beforeSend` strips `event.transaction`
- [ ] Unit test verifies `beforeSend` strips `event.user` PII fields
- [ ] Unit test verifies `beforeSend` scrubs extension IDs from frame filenames
- [ ] Unit test verifies `beforeSend` strips URL patterns from exception messages
- [ ] Unit test verifies `beforeSend` filters URL-bearing breadcrumbs
- [ ] Unit test verifies `beforeSend` returns the event (not null)
- [ ] Unit test verifies `beforeSendTransaction` returns null
- [ ] Unit test verifies `beforeBreadcrumb` drops navigation/fetch/xhr/console breadcrumbs
- [ ] Grep confirms zero occurrences of `replayIntegration` in codebase
- [ ] Grep confirms zero occurrences of `browserTracingIntegration` in codebase
- [ ] Grep confirms zero occurrences of `sendDefaultPii: true` in codebase
- [ ] `tsc --noEmit` passes with zero errors
- [ ] `vitest` passes with zero failures
- [ ] `eslint` passes with zero errors
