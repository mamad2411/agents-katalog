---
name: claim-module-implement
description: Explains the reading order, layer conventions, and gotchas for implementing a new screen/field/endpoint inside pticare's packages/module_claim (the claim/bồi thường module) — ClaimFormEngine vs foundation's FormEngine, ClaimStepCubit step pattern, the module's own GetIt container, ClaimApi/ClaimFailureMapper. Use when the user asks to build, finish, or extend a claim step or screen (S13b, S13c, S21b, S21c, S23, step 4), add a field to Step1Fields/Step2Fields/Step3Fields, wire a new ClaimApi endpoint, or otherwise write code inside module_claim/lib/src.
---

# claim-module-implement

How to add code to `packages/module_claim` — a new step/screen, a new field on
an existing step, or a new `ClaimApi` endpoint — without breaking the module's
deliberate departures from the rest of the app (own form engine, own DI
container, own step-stack). The module's `doc/` is the source of truth; this
skill is the order to read it in and the traps that aren't obvious from a
single file.

## When to use this

- Implementing one of the still-missing claim screens: S13b/S13c (beneficiary
  account), S21b (care facility picker), S21c (document upload), S23 (photo
  capture), or step 4 — check `module_claim/doc/README.md`'s "Đã dựng" table
  first, it's the single place that says what's actually built vs. still a
  stub, and it changes independently of this skill.
- Adding/changing a field on `Step1Fields`, `Step2Fields`, or `Step3Fields`,
  or touching `ClaimFormEngine` / `ClaimFieldValidator`.
- Wiring a new `ClaimApi` (retrofit) call or changing `ClaimFailureMapper`.
- Reviewing a PR that touches `module_claim/lib/src/**`.

## When NOT to use this

- Foundation package version/override mechanics (git ref vs. local path,
  `pubspec_overrides.yaml`) — that's [[foundation-use]], not this skill.
- Screens outside `module_claim` (host app `lib/features/**`) — those follow
  `Cubit` + `.arb` + `goNamed` per the host `CLAUDE.md`, not this module's
  rules. This module is the one deliberate exception in the repo.
- Generic BLoC/Cubit state design questions with no claim specifics — use
  `flutter-cubit-ui` or `bloc-pattern` instead.

## Steps

1. **Read in this order, not code-first:**
   `module_claim/doc/README.md` (map + what's built) →
   `doc/decisions/adr-001-*.md` and `adr-002-*.md` (why the module diverges) →
   `doc/specs/S2x-*.md` for the screen's *behavior* (as-built from the old app)
   → `doc/steps/step-N-*.md` for *how to build it in this module*. When specs
   and steps disagree: specs win on behavior, steps win on module structure.
   `step-1-customer-info.md` §0 has the shared engine contract read by every
   step — read it even when implementing step 2/3, not just step 1.

2. **Never reach for `foundation_form_dynamic`'s `FormEngine`.** This module
   hydrates `ClaimFormEngine` (`lib/src/engine/`, implements the
   `FormFieldEngine` port from `foundation_core`) instead — `FormEngine` resets
   `visible`/`required` unconditionally on every hydrate/change, which claim's
   business-driven show/hide rules can't survive. Add fields by extending the
   static `RuntimeContract` built by `Step{1,2,3}Fields`, not by asking a
   backend for schema — there is no schema endpoint.

3. **`fieldKey` must equal the key used in the `PATCH /pticare/v2/claims/{id}`
   body.** The PATCH always sends the *entire* profile across all three steps,
   so the body is built directly off engine node keys — invent a different key
   and either the PATCH silently drops the field or `ClaimPayloadBuilder`
   needs a translation table nobody asked for.

4. **Carry the four behaviors copied from `FormEngine` into any new
   validation/error-handling code**, they have real bugs behind them, not
   decoration: touched-set only marks fields that are `visible && enabled` at
   the moment `validateOnContinue()` runs; `setBusinessErrors` is a *complete*
   verdict (absent key = no error, clears stale ones); the return value is
   computed from the *resulting* error state, not from whether anything
   changed; `clearBusinessErrors()` must still run when schema validation
   fails first. Copy the corresponding test alongside the behavior.

5. **Register new dependencies in the module's own `GetIt.asNewInstance()`
   container** (`lib/src/di/module_injection.dart`), never the host's
   `GetIt.instance` and never with `injectable` codegen — the registration
   list is small and hand-written by design, at least two entries take
   runtime params (`dio`/`baseUrl`) that can't be code-generated anyway, and
   landing in the shared container collides with
   `configureFormDynamicDependencies()`'s `isRegistered<FormEngine>()` guard.

6. **New `ClaimApi` calls declare a real request/response type**, never
   `HttpResponse<dynamic>` or a raw `Map` — that's what lets a wrong-shape
   response fail at retrofit codegen and land in `ClaimFailureMapper` as
   `Failure.parsing` instead of a runtime cast crash. Confirm the response key
   names against a real captured payload before typing the DTO (see
   `doc/integration/claim-api.md` "Tên khoá lấy ở đâu" — several endpoints'
   field names were only confirmed after a real capture, e.g.
   `contractEffectDate`/`contractExpiryDate`, not `startDate`/`endDate`).
   `POST`/`PATCH /v2/claims` only succeed when the parsed `id > 0` — HTTP 2xx
   alone doesn't mean success.

7. **Don't touch token/auth headers in module code.** The host's `Dio` arrives
   pre-configured with `token-id: Bearer <token>` + `User-Agent: DLife`; the
   module only owns path/method/DTO-mapping/error-mapping. Don't reuse the
   host's existing `GetIt<Dio>` for claim calls — its interceptor stamps a
   plain `token` header, not `token-id: Bearer`, and claim needs its own `Dio`
   instance wired through `configureClaimModuleDependencies(dio:, baseUrl:)`.

8. **Strings go through `easy_localization` JSON** under
   `assets/translations/{vi,en,ko}.json`, not `.arb` — this module is the
   repo's one exception to the host's `.arb`-only rule. Add the same key to
   all three locale files in the same commit.

9. **After adding/changing a screen or field, update
   `module_claim/doc/README.md`'s "Đã dựng" table** in the same commit — it's
   the single place that says what's built vs. still a stub, and the host repo
   `CLAUDE.md`'s "Còn dang dở" section may also need a line removed once a
   listed gap (e.g. `insuredPersonId`, disk-backed draft store) is closed.

10. Run `dart run melos run claim:test` (or `flutter test` from inside
    `packages/module_claim`) — the module resolves and tests independently of
    the host, don't skip straight to a host-level `melos run test`.

## Anti-patterns to refuse

- Wiring a new field or screen through `foundation_form_dynamic`'s
  `FormEngine`/`FormDelta`/`FieldPatch` — this module intentionally has none
  of those; adding them back reopens the exact bugs ADR-001/ADR-002 exist to
  avoid.
- Registering a new service in the host's shared `GetIt.instance` "for
  consistency" — it collides with the BEP modules' `FormEngine` guard.
- Adding `path:` overrides to `foundation_*` directly in `pubspec.yaml`
  instead of `pubspec_overrides.yaml` — see [[foundation-use]].
- Guessing a new endpoint's response field names instead of confirming them
  against a captured payload (`doc/integration/claim-api.md` already flags two
  still-unconfirmed shapes — don't add a third).
- Reading `getCustomerProfile`'s thrown `Failure.validation` as a bug to
  silently "fix" by guessing a path — it's deliberate until the endpoint is in
  spec (see `doc/integration/claim-api.md` "Còn chưa chắc").
