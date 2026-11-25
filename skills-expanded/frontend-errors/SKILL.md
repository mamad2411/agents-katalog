---
name: frontend-errors
description: "When things fail in the browser: a map of failures, error boundaries per region, network and server errors shown where they happen, retries, sign-in expiry, offline, stale code after a deploy, not-found and error pages, reporting errors with context, and messages people can act on. Read before shipping any view that loads or saves data."
---

# When things fail in the browser

The generated app has one outcome: success. When a request fails, the
spinner turns forever, or the whole page goes white because one widget
threw; a toast says "Something went wrong" whatever went wrong; an expired
session loops between two redirects; a tab left open over a deploy breaks
on the next click; and nobody hears about any of it. This is how to
expect each failure, show it where it happened, keep what the user did,
and report it with enough context to fix. The server side is
`backend-errors`; the whole frontend is `frontend`.

## 1. The failure map

| Failure | The user sees | The code does |
|---|---|---|
| A render error (a bug) | the failed region's fallback, with Retry; the rest of the page works | error boundary, report |
| Network down, DNS, CORS (`fetch` rejects with a `TypeError`) | "You're offline" or "Can't reach the server", the last data kept | retry reads with backoff, hold actions |
| Timeout | "This is taking longer than usual" with Retry | abort after 10 to 15s |
| 400, 422 | each field's error beside it | map to fields (`frontend-forms`) |
| 401 | nothing, then the sign-in page if refresh fails | refresh once, replay, sign-in with a return path |
| 403 | what is not allowed and who can grant it | no retry, no redirect |
| 404 | a not-found view for that record or page | no retry |
| 409 | that it changed elsewhere, with a way to compare or reload | refetch; keep the user's edit |
| 429 | "Too many attempts. Try again in 30 seconds." | wait for `Retry-After`, disable the action until then |
| 5xx | "We couldn't save this. Try again." with Retry and a reference | retry reads, report with the request id |
| A code chunk missing after a deploy | "A new version is available", or one reload | reload once (section 7) |
| A third-party script blocked | nothing | no feature depends on analytics loading |

## 2. Error boundaries

- One at the root as the last resort, a full-page message with Reload
  (Next `global-error.tsx`, Nuxt `error.vue`, the root route's boundary);
  one per route (Next `error.tsx`, React Router's `ErrorBoundary` export,
  SvelteKit `+error.svelte`); and one around each independent widget (a
  chart, a side panel, a feed), so one failure blanks nothing else.
- Boundaries catch errors during render, not in event handlers or async
  code: those are caught where they happen, or passed into the boundary
  (TanStack Query's `throwOnError`, `showBoundary` from
  react-error-boundary's `useErrorBoundary`).
- Reset when the context changes (`resetKeys` with the route or record
  id), and on Retry, which also refetches the failed query:

```tsx
<QueryErrorResetBoundary>
  {({ reset }) => (
    <ErrorBoundary onReset={reset} resetKeys={[orderId]} FallbackComponent={PanelError}>
      <Suspense fallback={<ActivitySkeleton />}>
        <ActivityPanel orderId={orderId} />
      </Suspense>
    </ErrorBoundary>
  )}
</QueryErrorResetBoundary>
```

- The fallback says what failed ("Activity could not be loaded") and
  offers Retry, sized like the region it replaces.
- Elsewhere: Vue `onErrorCaptured` and Nuxt `<NuxtErrorBoundary>`; Svelte
  5's `<svelte:boundary>` with a `failed` snippet; Angular's `ErrorHandler`.

## 3. Where to show a failure

- In the region that failed, keeping the last good data visible and
  marked stale when there is some (`frontend-data`).
- A toast only for work in the background (an autosave, a message
  sending), and then the item itself is marked too ("Not sent. Retry").
- Never a blank page, a stack trace, raw JSON, `[object Object]` or
  `undefined` on screen.
- A failed save keeps the dialog or form open with everything typed.
- Errors after an action are announced (`role="alert"`); errors in a
  region that loads by itself use the region's text, no alarm.

## 4. Status handling in one place

The API client turns responses into `ApiError` (`frontend-architecture`);
one function turns errors into what the interface says and whether a retry
makes sense, so no component writes its own:

```ts
export function describeError(error: unknown): { message: string; retry: boolean } {
  if (error instanceof ApiError) {
    switch (error.status) {
      case 403: return { message: t("errors.forbidden"), retry: false };
      case 404: return { message: t("errors.notFound"), retry: false };
      case 409: return { message: t("errors.conflict"), retry: false };
      case 429: return { message: t("errors.rateLimited", { seconds: error.retryAfter ?? 30 }), retry: true };
      default:
        if (error.status >= 500) return { message: t("errors.server"), retry: true };
        return { message: t(`errors.${error.code}`, { defaultValue: t("errors.request") }), retry: false };
    }
  }
  if (error instanceof DOMException && error.name === "TimeoutError") return { message: t("errors.timeout"), retry: true };
  if (error instanceof TypeError) return { message: t("errors.network"), retry: true }; // offline, DNS, CORS
  return { message: t("errors.unexpected"), retry: true };
}
```

- **401**: the client refreshes once and replays (`frontend-data`); if
  that fails, the cache is cleared and the user goes to sign-in with a
  return path. A 401 from the refresh itself goes straight to sign-in:
  never a loop.
- **403**: say what they cannot do and who can grant it ("Only workspace
  admins can change billing"). Hide controls people cannot use in the
  first place, while the server still checks.
- **404**: a not-found view with a way on (the list, search), and the real
  `404` status on server-rendered pages (`frontend-seo`).
- **409**: fetch the current version, keep the user's edit, and let them
  compare or apply it again; never overwrite silently.
- **422**: the fields (`frontend-forms`).
- **429**: count down from `Retry-After`, with the button disabled until
  then.
- **5xx**: an apology in plain words, Retry, the request id shown small
  ("Reference 7f3a2c") for support, and a link to the status page if there
  is one.

## 5. Retries

- Automatic for reads that can be repeated, with backoff (TanStack Query's
  default of 3, `frontend-data`); never for writes, unless they carry an
  idempotency key and the server honours it.
- Otherwise a Retry button that re-runs only what failed, shows that it is
  working, and after two or three failures points to the status page or
  support.

## 6. Offline

- `navigator.onLine === false` means offline; `true` means nothing (a
  captive portal, a dead connection). Treat failed requests (`TypeError`)
  as the signal, with the `online` and `offline` events as hints.
- A banner while offline says what still works: "You're offline. Changes
  are kept on this device and sent when you reconnect" only if that is
  built; otherwise "You're offline. Reconnect to save."
- Actions that need the network are disabled or queued, on purpose:
  TanStack Query pauses mutations while offline and runs them on
  reconnect, which is a queue whether you meant one or not.
- Reads refetch on reconnect (TanStack Query's default). A service worker
  and offline storage only when the product is meant to work offline.

## 7. After a deploy

A tab opened before a deploy asks for code chunks the new deploy removed.
The import fails: `vite:preloadError` in Vite, `ChunkLoadError` in webpack;
the browser says "Failed to fetch dynamically imported module" (Chrome),
"error loading dynamically imported module" (Firefox) or "Importing a
module script failed" (Safari).

- Keep the previous build's assets on the CDN for a few days after each
  deploy: most of these never happen.
- Reload once when a chunk fails, and only once:

```ts
window.addEventListener("vite:preloadError", (event) => {
  try {
    if (sessionStorage.getItem("reloaded-for-deploy")) return; // tried once: the boundary shows it
    sessionStorage.setItem("reloaded-for-deploy", "1");
  } catch {
    return; // storage blocked: no reload loop risked
  }
  event.preventDefault();
  window.location.reload();
});
```

  Clear the key once the app has run for a minute, so the next deploy gets
  its reload too.
- Long-lived tabs (dashboards, editors) check a `/version.json` on focus
  and offer "A new version is available. Reload" rather than breaking on
  the next click.

## 8. Reporting

- Catch what nothing else caught: `window` `error` and
  `unhandledrejection` events; React 19's root options (`onUncaughtError`,
  `onCaughtError`, `onRecoverableError`); Vue's `app.config.errorHandler`;
  SvelteKit's `handleError` in `hooks.client.ts`; Angular's `ErrorHandler`.
- Send to Sentry (or the project's tracker) with the release, environment,
  route, the user's id (never their email or name), breadcrumbs, and the
  API's request id, to join with the server's log (`backend-errors`):

```ts
Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  release: import.meta.env.VITE_RELEASE, // the commit SHA
  environment: import.meta.env.MODE,
  sendDefaultPii: false,
  tracesSampleRate: 0.1,
  ignoreErrors: ["ResizeObserver loop completed with undelivered notifications"],
  denyUrls: [/^chrome-extension:\/\//, /^moz-extension:\/\//],
});
Sentry.setUser({ id: user.id });
```

- Source maps uploaded at build (`@sentry/vite-plugin` and the like) and
  deleted from the deploy when the code should not be browsable.
- Scrub personal data: no form values, tokens or emails in messages,
  URLs or breadcrumbs.
- Report what you will act on: render errors, 5xx, failed chunks, network
  failures in aggregate. Expected answers (422, 401, 404 on a typed URL)
  are not errors; reporting them buries the real ones.

## 9. Messages

What happened, what to do next, in plain words, through i18n (`i18n`), in
the product's voice (`writing`), keeping what the user typed:

| Not | Say |
|---|---|
| Error 500 | We couldn't save your changes. Try again in a moment. |
| Network Error | You're offline. Reconnect to save your changes. |
| Forbidden | Only workspace admins can change billing. Ask an admin for access. |
| Not found | This invoice doesn't exist, or it was deleted. |
| Too many requests | Too many attempts. Try again in 30 seconds. |

Never blame the user, no "Oops!", and no jokes where money or work was
lost. In development, detail and overlays; in production, no stack traces
on screen and no noisy `console.log` (a `no-console` rule that allows
`warn` and `error`).

## Check it

- MSW (`frontend-testing`) returns each status in turn: 401, 403, 404,
  409, 422, 429 with `Retry-After`, 500, `HttpResponse.error()`, and a
  delay past the timeout. Each shows its message in its region, nothing
  typed is lost, and one failing panel leaves the page working.
- DevTools offline: the banner appears, actions behave as designed, data
  returns on reconnect.
- Throw inside one widget (a temporary line, removed after): its fallback
  shows, the rest works, Retry recovers.
- Build, open the app, deploy a new build without the old assets, click
  into a lazy route: one reload or the prompt, never a white page.
- Staging: a test error reaches the tracker with release, route and a
  readable stack, and no personal data.
- `preview`: no console errors on any screen.

## Avoid

A white page from one widget's error; spinners that never end; "Something
went wrong" for every failure; raw JSON or stack traces on screen; a toast
for an error that belongs in a form; lost input after a failure; retrying
writes, or 4xx; a 401 redirect loop; trusting `navigator.onLine`; reload
loops after a deploy; old assets deleted at once; reports without release
or request id; personal data in reports; expected 4xx reported as
errors.
