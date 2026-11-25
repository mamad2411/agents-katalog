---
name: add-rate-limit
description: Adds rate limiting to a named route group using your current stack, with sane limits, proper 429 replies and a test.
disable-model-invocation: true
---

Add rate limiting to this route group: $ARGUMENTS

1. Find how the app is served and whether a limiter exists already (express-rate-limit, slowapi, Rack::Attack, a gateway or CDN rule, Redis). Reuse it. Do not add a new store without asking.
2. Choose the key per route: IP for anonymous routes, user id or API key for authenticated ones, and both IP and account name for login. Mention proxy setups: read the real client IP only from a trusted forwarded header.
3. Propose limits and show the numbers before coding, for example 5 per minute for login, 60 per minute for general reads. A burst allowance is better than a hard cap.
4. Return 429 with a Retry-After header and the project's normal error body. Never reveal whether an account exists.
5. Check multi-instance behavior: an in-memory counter is wrong behind several servers, so say so.
6. Write a test that exceeds the limit, sees the 429, and checks that a different key is unaffected. Run the tests.

Report the limits, keys and any gap such as a shared store you did not set up.
