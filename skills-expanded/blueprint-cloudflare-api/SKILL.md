---
name: blueprint-cloudflare-api
description: "Build the spec's operations as the Worker's API, with validation and tests."
---

# API

1. One route per operation in the spec's API table, in the Worker's `/api/*` handler.
2. At the entry, before routing and before sign-in:
   - a POST / PUT / PATCH / DELETE whose `Origin` (or, without one, `Referer`) is not this Worker's own origin is
     refused with **403**;
   - a JSON body is read **once**, and a malformed one is refused with **400** for every path. A Worker reads bodies
     per route by default, which leaves a malformed body to whatever the route does with it.
3. Validate every body and parameter (zod is fine) and answer 400 with a message when it is wrong; 404 for a missing
   row. Every error reaches one handler that answers JSON without a stack trace.
4. `test/api.test.ts`: every route in both directions — the valid request succeeds with the right body, an invalid one
   is refused with 400 — through `SELF.fetch`.

Done when the check passes: `yarn build` and `yarn test` succeed and `test/` has the api tests.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
