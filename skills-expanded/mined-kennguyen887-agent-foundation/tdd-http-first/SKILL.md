---
name: tdd-http-first
description: Drive a feature/bugfix test-first when the project mandates HTTP-layer-only testing — the failing RED test must be an HTTP/route-harness test (e.g. supertest), never a service/validator/util unit test. Trigger phrases — "làm theo TDD", "viết test fail trước", "write the failing test first", "do this test-first" — in any repo whose rules forbid unit tests.
metadata:
  last-updated: 2026-06-23
  author: Ken Nguyễn <ntnpro@gmail.com>
---

## When to use

You are about to implement or change endpoint behavior — a new route, a new request/response field, new validation, or a bugfix on an existing route — and you want to drive it test-first (RED → GREEN → REFACTOR), in a project whose testing rule is **HTTP-layer-only** (see the global `~/.claude/CLAUDE.md` "HTTP-layer testing rule": every test for an HTTP service goes through the HTTP layer via `supertest` / the project's route harness; no `tests/services|validators|utils` unit tests that bypass the route).

This skill exists because of a **collision**: the generic test-driven loop's reflex is "write a failing **unit** test first," but the HTTP-layer-only rule forbids exactly that. So here, RED = a failing **HTTP-layer** test. A fresh assistant doing "TDD" will reach for a unit test and violate the rule — that is the mistake this skill prevents.

Division of labor:
- **The loop discipline itself** (one behavior at a time, watch it fail for the *right* reason, write the *minimal* code to go green, then refactor) → the standard TDD RED/GREEN/REFACTOR discipline. Apply it; this skill doesn't restate it.
- **Binding that loop to the HTTP-layer-only rule** (where the RED test lives, what counts as a real RED, the escape hatch) → this skill.

## Steps

1. **(RED) Write one failing HTTP-layer test.** Decide WHERE it goes first: **add to the existing test file for that route/area** (a new `describe(...)` block); create a new file only when none builds that router/area. Use the project's route harness. Worked example (listings-api — `buildTestApp` + auto-mocked `repos`; follow the repo's `author-lean-http-tests` skill for placement):
   ```js
   import { jest } from "@jest/globals";
   import supertest from "supertest";
   import { buildTestApp, repos, src } from "../../helpers/infrastructure.js";

   // Mock external collaborators BEFORE importing the router (ESM hoist gotcha):
   // jest.unstable_mockModule(...) must run before the dynamic import below.
   const { default: SomeRouter } = await import("../../../src/app/http/routes/SomeRouter.js");

   let app;
   beforeAll(async () => { app = await buildTestApp(SomeRouter, { userId: "1", companyId: "company-1" }); });
   beforeEach(() => { jest.clearAllMocks(); });

   test("returns the new zipCode field", async () => {
     repos.Lease.findById.mockResolvedValue(makeLease({ zip_code: "50010" }));
     const res = await supertest(app).get("/api/v1/leases/lease-1");
     expect(res.status).toBe(200);
     expect(res.body.data.zipCode).toBe("50010"); // the contract you're driving
   });
   ```
   - Set per-case return values on the mocked repos; mock external services (S3, DocuSign, auth, etc.) explicitly above the router import — they are not auto-mocked.
   - Use whichever test fn the linter allows (listings-api whitelists `test`/`describe`, not `it`).

2. **Run it and confirm it fails for the RIGHT reason.** A test written before the route exists 404s — a *false* RED (fails on routing, not your behavior). Assert the concrete contract (`res.body.data.<field>`, a 400 validation body, a status) so it still bites *after* the route is wired. If you only assert `status` on a brand-new route, also assert a body field so GREEN is real.

3. **(GREEN) Write the minimal implementation** to make that one assertion pass (schema field, ViewModel mapping, validation rule, controller logic). Re-run — see it pass.

4. **(REFACTOR)** Clean up with the test green. Repeat from step 1 for the next behavior (happy path, then error/validation path — critical flows need both).

5. **Escape hatch — do NOT fall back to a unit test.** If a behavior genuinely cannot be reached through HTTP (logic inside a mocked service/validator the route never executes), then per the HTTP-layer-only rule you **skip the test entirely**. "Untestable through HTTP" means "untested", not "unit-tested as a workaround". Writing a `tests/services|validators` test to get a RED is the exact anti-pattern this skill forbids — restructure so the behavior is reachable via the route, or leave it untested.

## Verification

Run the single file (RED first, then GREEN after implementing). In listings-api:
```
NODE_OPTIONS=--experimental-vm-modules npx jest --runInBand tests/app/http/<name>.test.js
```
- **RED is valid** only when the first run fails on *your assertion* (e.g. `expected "50010", received undefined`) — NOT on a 404, an import error, or a missing mock. If it fails for a plumbing reason, fix the test setup until it fails on the contract.
- **GREEN**: same command passes after the minimal implementation.
- Lint clean on the changed files.

## Related
- **The generic TDD RED/GREEN/REFACTOR loop** this adapts — apply that discipline, then layer on these constraints. **The standard loop defaults to unit tests; this skill overrides that wherever HTTP-layer-only testing is mandated.**
- Global `~/.claude/CLAUDE.md` → "HTTP-layer testing rule" — the authoritative no-unit-tests rule this operationalizes.
- In listings-api: the `author-lean-http-tests` project skill (WHERE the test goes + HOW MANY cases) and `add-flag-gated-endpoint-group` (fuller `buildTestApp` harness reference).
