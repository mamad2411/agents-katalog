---
name: rum-instrument
description: Instrument a web frontend so you can answer "what did this user actually do" — page views, clicks, JS errors and fetch spans, tied to a session id and to the backend traces they triggered. Trigger phrases include "add RUM", "set up real user monitoring", "instrument the frontend", "add browser monitoring", "track what users are doing", "why did this user see an error", "add session tracking", "instrument my React/Next/Vue app", or any variant naming OnePatch as the destination ("install OnePatch in my frontend", "add OnePatch RUM"). Installs `@onepatch/rum`, wires identity, decides trace propagation per backend after probing it, writes the tests, and documents the result in the repo's `TELEMETRY.md`. For backend/server instrumentation use `otel-instrument` instead.
---

# Instrument a frontend with `@onepatch/rum`

You are making a web app's behaviour queryable: which pages, which clicks, which failed requests, which JS errors, in order, per session, per user.

**This produces an action list, not a video.** No DOM, no session replay, no keystrokes. That is the design — an investigation reads what someone did, and skipping the recorder keeps the payload small and the privacy story ordinary.

Published by **OnePatch**; installs its browser package, which wraps the OpenTelemetry browser SDKs and speaks plain OTLP. For server-side work use `otel-instrument` — same ingest endpoint.

Work the phases in order. Phases 5 and 7 are what make this predictable rather than merely done.

## 1. Discover the frontend

Identify the browser surface and how it boots:

| Signal | Framework | Entry |
| --- | --- | --- |
| `next.config.*` | Next.js | `instrumentation-client.ts` (15+) or a client component |
| `vite.config.*` + `react` | Vite React | `src/main.tsx` |
| `react-scripts` | CRA | `src/index.tsx` |
| `nuxt.config.*` | Nuxt | `plugins/onepatch-rum.client.ts` |
| `svelte.config.*` | SvelteKit | `src/hooks.client.ts` |
| `vue` / `angular.json` | Vue / Angular | `src/main.ts` |
| plain `<script>` | none | prebuilt bundle (phase 3) |

`expo` / `react-native` → **stop.** This package needs browser APIs. Say so and offer `otel-instrument` for their backend.

A monorepo can hold several frontends. Do one, and say which you picked before writing anything.

Find how it knows who is signed in at the same time — the session hook, the auth context, the `me` query. Phase 3 can't be written without it, which is deliberate.

## 2. Get the ingest configuration

You need an `ingestUrl` shaped `https://<slug>.logger.onepatch.dev` and an `op_…` `ingestToken`. Three paths, in order:

1. **The user pasted them.** OnePatch onboarding has a *"Copy command for your coding agent"* button carrying both. Extract with `https://[a-z0-9-]+\.logger\.onepatch\.dev` and `op_[A-Za-z0-9_-]+`.
2. **The repo has them.** If `otel-instrument` already ran here, `OTEL_EXPORTER_OTLP_ENDPOINT` in an env file has the same host, usually next to the token. Reuse both rather than asking.
3. **Neither.** Ask the user to sign up at `app.onepatch.dev` and paste that payload. Never guess a URL or proceed with a placeholder — a wrong endpoint produces a silent nothing, the most expensive failure here.

`op_…` is a write-only, append-only, single-tenant bearer, designed like a Sentry DSN: **it belongs in the bundle.** Commit it, inline it, put it in `NEXT_PUBLIC_*` / `VITE_*`. Do not proxy it. No other credential goes in a browser — if the user offers a key that isn't `op_`-shaped, refuse it.

## 3. Install and initialise

```sh
bun add @onepatch/rum   # or npm / pnpm / yarn — 0.2.0 or newer
```

Placement, three rules: **once** per page load (twice is a warning and a wasted call); **client-side** (it no-ops outside a browser, so a server-rendered import is safe, but the call belongs on a client path); **early**, before the app's own `fetch` calls.

Four values decide whether the data is usable in a month:

- **`user` is who is using the app.** Required — `startRum` will not compile without it, because identity as a second call is a second call somebody forgets. Phase 4 picks its shape; put a resolver in now.
- **`appName` is `<service>-web`.** If the backend is `acme-api`, this is `acme-web`. It becomes `service.name` — the first column of the sort key and what the service map draws, so an unrelated name files the two halves of one trace in two unrelated places.
- **`environment` comes from wherever the backend reads its own.** Not a hand-typed `"production"` in a file that gets copied to staging. Disagreeing halves make every env-filtered query return half a trace, and each half looks fine alone.
- **`appVersion` is the commit sha.** Every build system has one: `NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA`, `VITE_COMMIT_SHA` fed from `$GITHUB_SHA`, `git rev-parse --short HEAD`. It becomes `service.version`, which turns "errors went up at 14:20" into "errors went up on this deploy". No sha available? Wire one in — that is this phase, not a follow-up.

```ts
// Next.js 15+: instrumentation-client.ts at the project root, which Next runs
// on the client before hydration. Other frameworks: top of the entry module.
import { startRum } from "@onepatch/rum";

startRum({
  ingestUrl: process.env.NEXT_PUBLIC_ONEPATCH_INGEST_URL!,
  ingestToken: process.env.NEXT_PUBLIC_ONEPATCH_INGEST_TOKEN!,
  appName: "<service>-web",
  // On Vercel these two come free as NEXT_PUBLIC_VERCEL_ENV and
  // NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA. Elsewhere, define them in the build.
  environment: process.env.NEXT_PUBLIC_APP_ENV!,
  appVersion: process.env.NEXT_PUBLIC_COMMIT_SHA!,
  user: async () => (await getSession())?.user ?? null, // phase 4
  connectTracesTo: [/* phase 5 decides this — leave it out until then */],
});
```

**Next.js 13–14** has no `instrumentation-client.ts`. Use a client component rendered in the root layout, and call `startRum` at module scope behind a `let booted` guard — an effect in a `<StrictMode>` tree runs twice in development.

**No bundler:** load `https://unpkg.com/@onepatch/rum/dist/onepatch-rum.min.js` in `<head>` before the app's own scripts and call `OnePatchRum.startRum({…})`.

## 4. Wire identity — the highest-value five minutes

A session with no user answers almost nothing, so identity is the `user` option rather than a follow-up call. Find where the app already knows who is signed in — grep for `analytics.identify(`, `posthog.identify(`, `Sentry.setUser(`, `datadogRum.setUser(`, or the auth provider's `onAuthStateChange` / `useUser` / session context — and pass whichever of these three shapes matches what that path can give you at boot:

```ts
user: { id: session.userId, email: session.email }  // already known synchronously
user: async () => (await me())?.user ?? null        // known shortly; awaited once
user: "anonymous"                                   // no sign-in exists in this app
```

A resolver returning `null` is honest and telemetry still flows — a login page, a cold load before the session request lands. `(await startRum(...)).identified` tells you which happened. Pick `"anonymous"` only for an app with no accounts at all; on a signed-in app it is how you ship RUM with no U in it.

Pass names too, not only ids: `user.id` and `org.id` are unreadable in a list of traces, and turning one back into a person or a customer is the first step of every lookup. `id`, `email`, `name`, `orgId`, `orgName` become the conventional `user.*` / `org.*` attributes; anything else passes through under the key you wrote.

The first batch of spans waits up to three seconds for the resolver, so the page-load spans carry the person too. Nothing to do — but don't work around a delay you see in `debug` output.

Then `identifyUser` for every later change — a sign-in, a workspace switch, sign-out — on the same path the app already tells its other analytics SDK:

```ts
identifyUser({ id: user.id, orgId: user.orgId, plan: user.plan });
identifyUser({ id: null, email: null, orgId: null });  // signed out
```

An explicit `null` clears the attribute; **omitting the key leaves the previous value stamped on later spans.** That is how someone who leaves a workspace stays tagged with it, and how one person's session ends up labelled as another's. Mount that call above any auth gate — inside the signed-in shell it never runs for the sign-in, onboarding, or error surfaces, which are the ones you most want a name on.

**Don't stamp anything you wouldn't put in a log line.** No tokens, no full addresses, no free text the user typed.

## 5. Decide `connectTracesTo` — probe before you list

This is the phase that can break the customer's application.

Joining a browser span to its backend span means attaching a `traceparent` header. Same-origin requests get it automatically with nothing at risk — **if the API is same-origin, skip this phase and leave `connectTracesTo` out.**

Cross-origin is the hazard. The header makes the request preflighted, and a backend whose `Access-Control-Allow-Headers` doesn't cover `traceparent` makes the browser refuse the request outright. Not untraced — refused.

The library won't let that happen at runtime: it probes each listed origin at startup and connects only those that pass. But it can only report, and a silently unconnected backend should reach the user now, from you. So probe from the terminal too, where the response headers are readable.

Pick a route that **exists** — an API path the frontend really calls. Probing `/` is the standard mistake: it often 404s ahead of the CORS middleware and tells you nothing.

```sh
curl -s -D - -o /dev/null -X OPTIONS "https://api.acme.com/v1/things" \
  -H "Origin: https://app.acme.com" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: traceparent" \
  | grep -i "^access-control-"
```

| Response | Verdict |
| --- | --- |
| `allow-headers` names `traceparent` | Safe. List the origin. |
| `allow-headers: *`, `allow-origin: *` | Safe. A wildcard origin can't receive credentialed requests at all, so there are none to break. List it. |
| `allow-headers: *`, `allow-credentials: true`, `allow-origin` echoed | **Not safe.** A wildcard is illegal for a credentialed request, so cookie-bearing calls carrying `traceparent` are blocked while the same calls without it succeed. Ask for `traceparent` to be named explicitly. |
| `allow-headers` omits `traceparent` | Not safe. Offer to open a PR widening that backend's CORS. |
| no `access-control-*` at all | Inconclusive — you probably probed a route that 404s before CORS runs. Find a real one. |

List only origins that passed. Never a wildcard: the library rejects `connectTracesTo: ["https://*"]` outright, because it would attach trace headers to every third-party request the page makes — payment provider, CDN, analytics — and any one refusing the header breaks that request.

Tell the user, one line per origin, which backends are trace-joined and which aren't and why. For the ones that aren't, offer the CORS one-liner for their framework.

## 6. Name the actions worth naming

Clicks and navigations are captured already, and the click span carries the element and its xpath. What it can't carry is what the click *meant*.

```ts
recordAction("ran-workflow", { workflowId });
catch (error) { recordError(error, { where: "checkout" }); }
```

Add `recordAction` where the product has its own name for a step — the thing someone would search for. Three to six is right for a first pass; find them at the mutations, the submit handlers, and whatever the product's analytics already tracks. Don't wrap every button. Wrap handled errors that would otherwise vanish.

## 7. Write the tests

Instrumentation fails silently, so it gets tests. Match the repo's existing setup (vitest, jest, bun test). Four, in descending order of what they catch:

**7a. It starts, and every listed backend is connected** — catches a broken endpoint, a bad token shape, a wildcard, and CORS drift:

```ts
import { startRum } from "@onepatch/rum";
import { rumOptions } from "../src/rum-config"; // export the options so tests can see them

test("RUM starts and connects every backend it was told to", async () => {
  const status = await startRum(rumOptions);
  expect(status.started).toBe(true);
  expect(status.error).toBeUndefined();
  for (const backend of status.backends) {
    expect(backend.allowed, `${backend.origin}: ${backend.detail}`).toBe(true);
  }
});
```

Refactor phase 3 so the options live in one exported object — that is what makes this test possible and the only structural change asked for. This test reaches the network; if the repo's unit tests must stay offline, keep the assertions on the options, move the backend loop to a pre-deploy check, and say which you did.

**7b. Identity reaches the spans.** Assert `status.identified` is `true` for a signed-in session — one line, and it fails if the resolver races the session or returns the wrong shape. Then mock the package and assert `identifyUser` fires on the auth path with the fields you wired, and that sign-out passes `null` rather than omitting the keys.

**7c. It boots once, on the client.** Assert the init module is imported exactly once and (Next/Nuxt/SvelteKit) on a client-only path. A grep-shaped test is fine and catches someone adding a second `startRum` in a provider.

**7d. No wildcard in `connectTracesTo`.** One line. The library enforces it at runtime; the test makes a well-meaning "match all our subdomains" edit fail in CI instead.

Run them. Report the real result — if 7a fails because a backend is unconnected, that is the finding, not a test to relax.

## 8. Verify in a real browser

Tests are not proof that telemetry arrives. Boot the app, sign in, click something, navigate once. Confirm the session id (`OnePatchRum.sessionId()` with the script bundle, otherwise `debug: true` temporarily). Then ask the user to look in their OnePatch workspace: *"you should see a service called `<service>-web` with `click` and `documentLoad` spans within about ten seconds."* Check the spans carry an environment and a version, not blanks — `service.version: ""` is instrumented but unattributable, and that is only obvious now.

**Read `user.id` off one of those spans, including a `documentLoad` from the very first page.** This is the check we skipped on our own app and paid a week of anonymous telemetry for. A whole session with no `user.*` means the resolver returned `null` — usually a session request that isn't in flight yet at boot, or auth state read from a provider that hasn't mounted. Names on the later spans but not the load ones means something is still calling `identifyUser` instead of passing `user`.

If nothing arrives: a CORS error on the ingest URL means the host is wrong; 401 means the token is; no requests to the ingest URL at all means `startRum` isn't running — server path, or never imported. A `[onepatch/rum]` error names its own fix.

If a backend was meant to be trace-joined, prove it: trigger a request, find the span, check the backend's span shares the trace id. One end-to-end trace beats any amount of configuration review.

## 9. Add a browser section to `TELEMETRY.md`

**`TELEMETRY.md` at the repo root is the one place a repo describes what it emits** — written by `otel-instrument`, kept fresh by the `telemetry-docs-freshness` monitor, and front-loaded into the agent's context whenever a telemetry skill runs. The browser is another emitter in that repo, so it goes in that file. Don't start a second document; a repo with two telemetry docs has one that's stale.

A frontend in its own repo gets a browser-only `TELEMETRY.md` — that is complete, not half-written, so don't invent placeholder server sections. The corollary matters more: **when the frontend is a separate repo, the backend's doc will never mention the browser.** Nothing stitches the two together, so the propagation table is the only place the FE↔BE join is written down. Name the backend *services* there, not just origins, so a reader from either side can find the other.

Append, under a `## Browser (RUM)` heading:

```markdown
## Browser (RUM)

- `service.name`: `<service>-web`
- `deployment.environment.name`: from `<env var, and where the backend reads the same value>`
- `service.version`: from `<the build's commit sha var>`
- Framework: <framework + version> · Package: `@onepatch/rum` <version> · Init: `<file:line>`

### Identity

| Attribute | Source |
|---|---|
| `user.id`, `user.email` | `user` resolver at init, `src/rum-config.ts:12` |
| `org.id`, `org.name` | `identifyUser` on workspace switch, `src/auth/session.ts:41` |

### Named actions

| Action | Fires when | Attributes | Source |
|---|---|---|---|
| `ran-workflow` | User clicks Run on a workflow | `workflowId` | `src/workflow/RunButton.tsx:88` |

### Automatic spans

`documentLoad`, `documentFetch`, `resourceFetch`, `click`, `HTTP GET`/`POST`, `webvitals`, `visibility`, plus JS errors.

### Trace propagation

| Origin | Joined | Why |
|---|---|---|
| same-origin | yes | automatic |
| `https://api.acme.com` | yes | `allow-headers` names `traceparent` — joins `service.name = acme-api` (repo `acme/backend`) |
| `https://legacy.acme.com` | no | wildcard `allow-headers` with credentials — would break cookie-bearing requests |

## Not captured

No session replay, no DOM, no keystrokes, no form contents. Console capture is off.

URLs are recorded as they are, query string and fragment included, because the query is usually where the URL says which thing. `scrubQueryStrings: true` drops both — set it if these URLs carry reset tokens, magic-link codes or email addresses rather than identifiers.
```

List only what the code actually emits — walk the real `recordAction` sites, don't copy the examples. `file:line` on every hand-written row. Keep "Not captured"; it's the section a privacy reviewer opens first.

## 10. Close the loop

> Your frontend now reports to `<slug>.logger.onepatch.dev` as `<app-name>`. Commit the `TELEMETRY.md` changes alongside the instrumentation so OnePatch picks up what your actions mean.
>
> Things to ask in your OnePatch workspace:
> - "what did <user email> do in their last session?"
> - "which pages threw errors in the last hour?"
> - "show me sessions where checkout failed"

If they haven't connected GitHub, point them at the onboarding step — the context engine reads `TELEMETRY.md` from the repo, and you can't drive that OAuth flow. **If this frontend is its own repo, say so specifically:** connecting the backend repo is not enough.

## Don't

- **Don't add session replay.** Not with this package, not alongside it. If the user wants a video, explain what the action list answers and let them decide; don't quietly install a recorder.
- **Don't list `connectTracesTo` entries without probing.** Every other shortcut here costs data. This one costs the customer's API calls.
- **Don't proxy the ingest token.** It is designed to be public.
- **Don't turn on `captureConsole` by default.** Console lines carry personal data more often than spans do.
- **Don't set `scrubQueryStrings: true` reflexively.** It reads as the safe choice and usually isn't: it also drops the fragment, so a hash-routed app loses its route and "which page was this?" stops having an answer. Set it when you've looked at the app's real URLs and they carry secrets, not identifiers — and say which way you set it.
- **Don't reach for `user: "anonymous"` to get past a type error.** It compiles and it ships RUM that can never answer "what did this person do". If the session isn't available synchronously, that is what the resolver form is for.
- **Don't leave `appVersion` as a placeholder.** `"dev"` in production is worse than nothing: it looks answered.
- **Don't instrument React Native with this**, leave `debug: true` committed, or call `startRum` inside a React effect without a module-scope guard.
- **Don't report success without phase 8.** A green test suite and zero spans is the normal way this goes wrong.
