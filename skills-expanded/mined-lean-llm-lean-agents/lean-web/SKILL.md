---
name: lean-web
description: "Load lean-web when working on web or Node.js projects: JavaScript, TypeScript, HTML/CSS, React, Next.js, Fastify, backend APIs, authentication/OAuth, monorepos, tooling, testing, or web performance. Apply framework-specific rules only when that stack is present."
---

# lean-web

## Contract
Co-load `lean-code`; `AGENTS.md` controls routing. Apply only the detected web/Node stack.

## Detect → locate → fix → verify
Inspect `package.json`, lockfile/manager, tsconfig, deployment and CI; preserve runtime/browser support. Use local binaries and one package manager; no unsolicited lockfile edits. Run scoped tests/typecheck/lint/build. Prioritize correctness, accessibility and security over performance.

## JavaScript / TypeScript
Follow existing ESM/CJS, exports, import extensions, module resolution and browser/Node targets. Prefer `const`, pure/local functions and early returns over hidden mutation. Derive types from runtime sources (`as const`/`typeof`); use `keyof`, `T[K]`, generics/utility types only to clarify contracts. Runtime-validate untrusted input to narrow `unknown`; avoid `any`, unsafe assertions, `@ts-ignore`, duplicate types and type gymnastics. Reproduce diagnostics with repo typecheck (`tsc --noEmit` if applicable), repair callers and rerun.
Native TS stripping only when Node version/support and repo setup allow: use `import type`, erasable syntax and proper extensions, not enums/parameter properties requiring transpilation. Keep existing TS build pipelines.

## Async / Node.js reliability
Choose `Promise.all`/`allSettled` by partial-failure policy; never swallow rejections or fire-and-forget required writes. Bound requests/timeouts/retries with backoff. Stream large files/ETL with `node:stream/promises` `pipeline()`, async transforms and backpressure, not whole-input buffering. Cache measured repeat work only: bounded LRU, inflight promise dedup, expiry/invalidation and user isolation; no global private-request cache. Shutdown: stop intake → drain → close DB/network/timers → exit; test open handles and async cleanup. Distinguish operational/programming errors. Profile with `node --cpu-prof`, safe heap snapshots/inspector.

## Web UI / HTML / CSS
Use semantic HTML, accessible names/labels, keyboard/focus states, heading order, contrast and responsive layouts. Prefer grid/flex and existing tokens/components over JS positioning or new design systems. Match SSR/client markup; avoid hydration flicker, layout shifts and reflows. Defer noncritical scripts; optimize images (dimensions, lazy below-fold, formats), fonts and critical resources. Test accessibility and scrolling before using `content-visibility` for long offscreen content. Preserve interaction and reduced-motion preferences.

## React / Next.js only
**Data/bundles:** remove waterfalls: start independent requests early/in parallel; stream/Suspense when supported. Keep server work server-side; narrow imports, dynamically import heavy optional UI, defer third-party libraries and inspect actual bundles. Auth-check server actions/loaders/routes, not just client gates. Dedup within request lifetimes; cross-request caches need explicit keys/invalidation and no data bleed. Minimize serialized server→client props; no module-level mutable request state.
**Rendering:** derive state during render, not effects; handle events in handlers. Localize state, stabilize keys; profile before `memo`/`useMemo`/`useCallback`. Use functional setters, refs for transient nonvisual values, transitions/deferred values for nonurgent expensive updates. Avoid nested component declarations and duplicate global listeners. Match installed React/Next APIs; React 19 ref-as-prop and `use()` are version-gated, not upgrade mandates.
**Composition:** replace many boolean behavior props with variants/compound components when simpler. Providers own shared state/actions; children compose UI. Prefer `children` over needless render-prop callbacks; don't force context or libraries on simple components.

## HTTP APIs / Fastify only
Follow framework architecture. Fastify: encapsulate plugins/routes/decorators, scope hooks to the correct lifecycle, schema-validate inputs/serialize outputs, set content types/statuses and centralize errors. Prefer async handlers, Pino and official plugins; enforce route authentication/authorization, CORS allowlists, secure headers, body/rate limits. Test handlers with `app.inject()` rather than a network server; use real service/database integration tests for wiring. Handle WebSocket/stream disconnects, backpressure and cleanup.

## Auth / OAuth / Better Auth only
Server-verify identity **and** authorization for sensitive operations. Cookies need HttpOnly, Secure, appropriate SameSite, CSRF/origin controls and safe session invalidation. No secrets/tokens in logs, URLs or public bundles.
OAuth: authorization-code + PKCE (`S256`) for public clients; verify `state`, exact allowed redirect URIs, JWT issuer/audience/expiry/signature with trusted keys/JWKS. Enforce refresh rotation/revocation and client-credential scope. No implicit flow or disabling CSRF/origin validation to silence errors.
Better Auth: resolve installed version (lockfile first), consult matching docs, keep existing DB adapter and secure `BETTER_AUTH_SECRET`/`BETTER_AUTH_URL`. Generate/migrate schema after plugin changes; distinguish ORM model/SQL table names, check `secondaryStorage` session precedence and cookie-cache limits. Align server/client plugins, origins, rate limits and provider callbacks. Verify sign-in/out, expired/invalid sessions, privilege boundaries and migration; destructive migrations require approval.

## Monorepo / Turborepo only
Inspect workspaces, manager, `turbo.json` and installed `turbo` docs (`node_modules/turbo/docs/README.md` or resolved path); use installed-version syntax. Preserve `dependsOn` graph, inputs/outputs, environment hash, cache isolation and lockfile consistency. Cache deterministic tasks only, never secrets in remote cache. Filter affected packages but include necessary dependent builds/tests. CI needs reproducible lockfile installs and clean-cache behavior.

## Tooling / lint / tests
Keep existing formatter, import sorting and ESLint/Prettier/neostandard config; ESLint 9 flat `eslint.config.*` only when the project opts in. No unrelated `--fix`. Isolate hangs/flakes: inspect timers, global state, worker teardown and sockets; retries diagnose, not fix. Test browser keyboard paths, responsive sizes and async failures. Performance evidence: bundle sizes, Core Web Vitals, request p95, CPU/memory.

## Node core / native ONLY when implicated
For `nodejs/node`, N-API, libuv or V8 work, inspect matching contribution/build/test conventions, engine version and ABI. Reserve `node-gyp`/`binding.gyp` and native debugging for native tasks. Profile event-loop stalls, thread-pool saturation, GC and hidden-class/deopt changes before tuning; use primordials where required to protect internals from prototype pollution. Don't impose core build conventions on ordinary apps.

## Other requested tasks only
Only when requested: docs—one tutorial/how-to/reference/explanation purpose per page, test commands/examples; agent instructions—non-discoverable actionable `AGENTS.md` conventions, not code/README duplication, prune stale rules; skills—compare verified skill-off/on outcomes, regressions and token cost, retain useful triggers; Git/GitHub—`gh`/scoped git evidence, preserve history/signing, no destructive changes or embargo disclosure; snippet graphics—installed renderer/config, verify output. These workflows do not activate for ordinary feature fixes.
