---
name: unthrottled-route-check
description: Find Next.js API routes that call OpenAI, Anthropic or the Vercel AI SDK, or create a Stripe Checkout Session, with no rate limiter. Use when the user asks about rate limiting, AI cost per user, surprise API bills, refresh loops at checkout, or abuse protection before launch.
allowed-tools: Read Grep Glob
---

# unthrottled-route-check

Review only. Don't edit files unless the user asks for the fixes afterwards.

## Scope
Route handlers: `app/**/route.{ts,js}`, `src/app/**/route.{ts,js}`, `pages/api/**`, `src/pages/api/**`. Also read `middleware.ts` or `proxy.ts` at the project root (or in `src/`).

## Find the sinks
Grep the route files for these method calls, whatever the client variable is called (`openai.`, `llm.`, `client.`...):
- AI calls: `.chat.completions.create`/`.stream`/`.parse`, `.responses.create`/`.stream`/`.parse`, `.messages.create`, `.messages.stream`, `.images.generate`, `.embeddings.create`, `.completions.create`, `streamText(`, `generateText(`, `generateObject(`, `streamObject(`, and `fetch` to `https://api.openai.com` or `https://api.anthropic.com`, written as a literal or through a const base URL (``fetch(`${OPENAI_BASE}/...`)``, `fetch(ANTHROPIC_URL)`)
- Checkout: `.checkout.sessions.create`

`.messages.create` is also used by non-AI SDKs (for example SMS clients); drop those findings after reading the file.

For routes with no match, check their local imports (`./`, `../`, `@/`) one level deep: a helper such as `lib/ai.ts` may make the call.

## Look for a limiter
A route counts as limited only when it (or the helper it imports) imports a real limiter and uses it. A real limiter is a known package (`@upstash/ratelimit`, `@arcjet/*`, `rate-limiter-flexible`, `express-rate-limit`, `@unkey/ratelimit`) or a local module whose file name is `ratelimit`, `rate-limit`, `rate-limiter` or `limiter`. Using it means calling an imported binding (`enforce(...)`, `rateLimit(req)`) or building a value from one (`const rl = new Ratelimit(...)`, `const aj = arcjet(...)`) and then using that value (`rl.limit(id)`, `aj.protect(req)`, or passing it to a guard), before the sink runs. Other paths that merely contain "ratelimit", an object such as `rateLimits.limit(5)`, `.protect(` without an Arcjet import, a database query's `.limit(10)`, an unused limiter, or a mention in a comment or string don't count.

If `middleware.ts`/`proxy.ts` has a limiter, check that its `matcher` covers the route (a negative lookahead such as `/((?!api|_next/static).*)` excludes `/api`) and whether it keys on the user id or only the IP. IP-only limits let one signed-in user with several IPs (or a shared office IP) through or block wrongly.

## Report
For each finding give file:line, id, severity and fix.

| Id | Severity | Finding | Fix |
|---|---|---|---|
| U1 | high | AI call in a route with no limiter | Require a signed-in user, then limit per user id (for example Upstash `Ratelimit.slidingWindow(10, "60 s")`) and return 429 with `Retry-After`. Add a per-user monthly dollar cap and a provider-side project limit as a backstop. |
| U2 | medium | `checkout.sessions.create` in a route with no limiter | Limit per user, pass an `idempotencyKey`, reuse an open session for the same cart, and disable the button while the request runs. |
| U1/U2 | low | Same, but a middleware limiter exists | Confirm the matcher covers the route and the key is per user. |

End with: routes checked, findings by severity, and anything you couldn't confirm (dynamic imports, wrappers more than one import deep).

## Optional script
`scripts/scan-unthrottled.mjs` in this skill's folder automates the sink and limiter matching above with Node 20+ and no dependencies. It doesn't check whether the limit call comes before the sink, follows imports one level deep only (no `#` aliases), and doesn't see destructured clients (`const { messages } = client`). It is not run by this skill. To run it yourself: `node scripts/scan-unthrottled.mjs <project-dir>` (add `--json` or `--exit-zero`). It exits 1 when it finds a high or medium issue, so it can run in CI. It's a text scan: treat a clean result as "nothing found", not as proof the app is protected.
