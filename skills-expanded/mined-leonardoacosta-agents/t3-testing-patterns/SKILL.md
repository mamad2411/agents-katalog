---
name: t3-testing-patterns
description: >
  Testing patterns for T3 Turbo monorepos: Vitest with real database boundaries and typed
  provider fakes, plus Playwright E2E command and target selection, isolated CI lifecycle,
  fixtures, persona storage state, mutation ownership and cleanup, collection equality,
  sharding, quarantine, reporting, provider adapters, worker benchmarks, and flake triage.
  Use when writing or reviewing tests, choosing deployed/local/CI targets, designing E2E
  workflows, debugging flaky authentication or concurrency, or changing Playwright config.
  Triggers: unit test, vitest, createCaller, playwright, E2E_BASE_URL, test:e2e, fixture,
  persona, storageState, mutation cleanup, shard, fullyParallel, quarantine, retry, blob report,
  browser matrix, worker count, flake classifier, provider receipt.
user-invocable: false
disable-model-invocation: false
category: E2E
level: library
engineer: tdd-test-writer
gate: "pnpm lint"
bundles: []
allowed-tools: Read, Glob, Grep
paths: ["**/*.spec.ts", "**/*.test.ts", "packages/e2e/**"]
---


# T3 Testing Patterns

Use this file to choose a testing rule and load only the relevant deep-dive. For RED-GREEN-REFACTOR,
use `test-driven-development`; for database/type/env ownership, use `t3-code-patterns`.

## Reference Router

| Read when... | Reference |
|---|---|
| Choosing a root command, env boundary, deployed/local target, or isolated CI lifecycle | [`references/e2e-command-target-lifecycle.md`](references/e2e-command-target-lifecycle.md) |
| Designing fixtures, personas, auth state, mutation cleanup, parallel safety, or provider adapters | [`references/e2e-fixtures-personas-ownership.md`](references/e2e-fixtures-personas-ownership.md) |
| Designing collection, projects, shards, browser install, reports, quarantine, retry classification, or worker benchmarks | [`references/e2e-topology-evidence.md`](references/e2e-topology-evidence.md) |
| Authoring/debugging specs, waits, steps, lint gates, visual pilots, or audit journeys | [`references/e2e-authoring-debugging.md`](references/e2e-authoring-debugging.md) |
| Auth sign-ins flake or return 429 on preview/dev | [`../t3-code-patterns/references/better-auth-rate-limiting.md`](../t3-code-patterns/references/better-auth-rate-limiting.md) |

## Unit and Integration Rules

### Real database boundaries

Database query, migration, constraint, foreign-key, and tenant-isolation tests use a migrated test
Postgres. Never `vi.mock()` the Drizzle/database module: it proves a mock's behavior, not SQL or
schema behavior. Pure validators and formatters may use ordinary fakes. FK-heavy suites may use
Vitest `pool: "forks"` with `singleFork: true` when shared database ordering requires it.

### Typed callers and builders

Exercise tRPC procedures through `createCaller` and a stable typed context builder; never force a
context through `as any`. Put reusable factories in `packages/<pkg>/src/testing/builders.ts`, not
in sibling test files. Inline one-off data is fine; promote shapes reused by three or more tests.

### Provider seams

Business-service unit tests inject narrow typed payment, email, blob, or webhook capabilities.
Only production-adapter unit tests mock an underlying SDK or use recorded SDK fixtures. A separate
approved non-production integration lane proves credentials and SDK mapping; a fake never does.

### Coverage floors

Set coverage thresholds to the measured baseline minus one point. Refresh when the measured
baseline improves by more than three points or during the quarterly review.

## E2E Standards Matrix

| Concern | Required standard |
|---|---|
| Public commands | Root `package.json` keys are named exactly `test:e2e` and `test:e2e:local`; their values may delegate through behavior-equivalent internal Turbo/package tasks. |
| Env loading | One package-owned `dotenvx run --overload --quiet` boundary; no nested loaders. |
| Target authority | A naked URL is insufficient. A private capability binds mode, operation, URL, target, non-production deployment, run, database, and service identities. Every non-loopback target requires HTTPS. |
| Canonical mode | Deployed HTTPS non-production only, with trusted identities and production denial before preparation; operation is test execution. |
| Local mode | Loopback only through exact `test:e2e:local`, with non-production database/service identities; operation is test execution. |
| CI mode | Loopback only with full run-owned app/database/service identities before provisioning and unchanged revalidation after preparation; operation is test execution. |
| Collection mode | Explicit `--list`/proven no-test-body operation only; exposes exact unfiltered `chromium` alone, with no setup dependency graph or web server. |
| Legacy variables | `BASE_URL` may appear in migration guidance but is never accepted as a fallback. No URL silently defaults to localhost. |
| Collection | One exact, unfiltered `chromium` completeness project; authored and collected normalized file sets must match. |
| Exclusions | Missing manifest means an empty set. If present, it is strict, validated, and the sole exclusion source. |
| Mutation execution | `fullyParallel: false` and one worker by default. Higher concurrency is earned with exact ownership, adapter safety, and target-class benchmark evidence. |
| Setup | Serial setup creates import-safe readiness state and a small eager persona set, never shared mutable test data. |
| Personas | Exact isolated persona mapping. Storage state is run-owned/gitignored, private `0700`/`0600`, atomic, short-lived, revoked and deleted; no privilege fallback. |
| Mutations | Server derives owner/run from an authenticated non-production capability, never client headers. Register creates immediately; pre-authorize update/delete via same-owner IDs or reversible leases; clean children first. |
| Providers | Explicit non-production run-scoped adapters with receipts, reset, escaped-record checks, and no production fallback; report live-provider evidence separately. |
| Distribution | Native Chromium sharding; workers, shards, and workflow matrix concurrency are distinct controls. Run shards with setup completed once and `--no-deps`. |
| Evidence | Blob plus JSON/JUnit per lane, fail-closed inventory, one retry and flake classification. Never upload storage state; scan/redact secrets before restricted, short-retention `always()` upload. |
| Quarantine | Structured owner/reason/issue/expiry metadata, ratcheting debt, and scheduled/manual quarantine execution. |
| Benchmarks | Target-class-specific, full-suite, unsharded, comparable records; two adjacent clean runs at the proposed worker budget. Retry-pass is not clean. |

## Decision Rules

1. **Mode matrix first.** Select canonical deployed-HTTPS, local loopback, CI loopback, or isolated
   collection-list operation before commands. Reject every unlisted mode/target/operation pairing.
2. **Ownership before speed.** Deny production in every mutation-capable mode. Treat the lane as
   serial until creates have narrow provenance, update/delete is authorized before side effects,
   cleanup is exact, and concurrency is demonstrated at the same target class.
3. **Completeness before compatibility.** Prove exact Chromium collection, then add tagged browser
   compatibility lanes; never split completeness across browser projects.
4. **Evidence before green.** Missing reports, cleanup records, shards, provider escaped-record
   checks, capability-omission records, secret scans, or flake classification make the run
   incomplete. A retry pass remains flaky.
5. **Determinism at the server seam.** Seed server-prefetched/RSC state and use run-scoped provider
   adapters. Browser interception is for browser transport behavior, not as a substitute for server
   business behavior.

## Authoring Minimum

- Import `test` and `expect` values from `@fixtures/base`; raw `@playwright/test` values bypass
  application fixtures. Type-only imports such as `Page` and `BrowserContext` remain valid.
- Prefer web-first conditions over sleeps. `waitForTimeout` needs a justified `@wait-exception`.
- Use `test.step` for multi-action journeys so traces identify the failing phase.
- Use per-test mutable fixtures and exact teardown; shared baseline fixtures are immutable/read-only.
- For logged-out coverage, set anonymous storage state explicitly rather than inheriting a default
  authenticated persona.

## Instant Navigation Regression Guard

`@next/playwright`'s `instant()` helper asserts what a navigation shows *before* the network
settles — catching Instant Navigations regressions unit tests can't see. Two named causes worth a
guard comment when touching shared server code:

- A `cookies()`/`headers()` call added to a shared layout or header de-opts every route beneath it
  to request-time rendering.
- A `<Suspense>` boundary moved during a refactor, turning an instant shell into a blocking wait.

```ts
import { expect, test } from "@fixtures/base";
import { instant } from "@next/playwright";

test("chat detail navigation is instant", async ({ page }) => {
  await page.goto("/chat");

  // Assertions inside the callback are the instant contract — must hold before network settles
  await instant(page, async () => {
    await page.click('a[href="/chat/123"]');
    await expect(page.locator("h1")).toContainText("Conversation");
    await expect(page.getByText("Loading messages…")).toBeVisible();
  });

  // Assertions after the callback may depend on streamed/network content
  await expect(page.getByText("42 messages")).toBeVisible();
});
```

> `instant()`'s exact signature is documented from release-note code samples, not verified
> against installed typings — check it against the `@next/playwright` version actually installed
> before relying on it.

## Cross-References

- `t3-code-patterns` — database imports, env validation, type ownership, and Better Auth scoping
- `test-driven-development` — RED-GREEN-REFACTOR process
- `tdd-integration` — test-writer, implementer, and refactorer orchestration
- `extend-before-create` section 11 — placement rules for scripts and seeders

Project-specific extensions belong in the project's E2E documentation; canonical safety and
evidence rules above must not be weakened there.
