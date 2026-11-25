---
name: ship-mobile-app
description: Build, change, debug, and prepare production mobile apps across domain meaning, local and server state, lifecycle, platform, and release boundaries. Use for non-trivial Flutter, React Native, iOS, or Android work involving persistence, sync, auth, offline behavior, notifications, permissions, native integrations, signed builds, or store delivery. Do not use for isolated snippets, UI-only styling with an obvious check, web- or server-only work, app ideation, or store marketing alone.
license: MIT
metadata:
  author: aiopshwang
  version: "0.1.1"
---

# Ship Mobile App

Build the user path, not merely the code that resembles it.

A mobile change is complete only to the boundary actually observed. Source code,
tests, debug builds, signed artifacts, store state, and behavior on a real device
are different facts. Use the strongest practical evidence for the requested
result, and label every untested layer honestly.

The general completion discipline here is shared with the `goal-to-proof`
skill; when both are installed, this skill supplies the mobile-specific
boundaries and `goal-to-proof` supplies the overall gate.

## Frame the user loop

Inspect the repository and existing product before proposing a new architecture.
Find the current screens, domain models, persistence path, backend contracts,
platform configuration, release workflow, tests, and recent relevant failures.
Classify existing pieces as **reuse**, **extend**, **replace**, or **new**.

For substantial work, determine:

- **User scene:** who is doing what, under which realistic conditions?
- **Entry and action:** how does the user reach and perform the behavior?
- **Success:** what can the user observe or do afterward?
- **Recovery and return:** how do they correct, undo, retry, or find it again?
- **Non-goals:** what is deliberately outside this change?

Do not let a requested screen, library, or implementation detail substitute for
the underlying user problem when the mismatch would invalidate the result.

## Trace the truth boundaries

Map only the boundaries touched by the request:

1. **Domain truth:** the data means what its label and product behavior claim.
2. **State truth:** local, optimistic, queued, committed, stale, and failed states
   remain distinguishable.
3. **Lifecycle truth:** the behavior survives the relevant cold start, resume,
   background, deep-link, notification, permission, and account transitions.
4. **Platform truth:** native configuration and the signed artifact contain what
   the runtime path needs.
5. **Claim truth:** UI copy, AI output, analytics, privacy text, and completion
   reports never claim more than the observed state supports.

Trace the relevant path end to end:

```text
user action -> UI state -> domain decision -> durable state/sync
            -> platform or external service -> signed artifact -> user-visible result
```

For each touched boundary, identify its authority, failure state, and direct proof.
When the work crosses several boundaries or includes time, identity, offline data,
AI, or native services, read [boundary checks](references/boundary-checks.md).

## Build a real vertical slice

Prefer the smallest slice that exercises the requested user loop over disconnected
layers that merely compile.

- Reuse established repositories, state owners, navigation, and release paths.
  Do not create a parallel source of truth because it is locally convenient.
- Put domain decisions in deterministic code where practical. Inject clocks,
  identities, and effectful adapters so boundary behavior is testable.
- Define important invariants once and enforce them at the authority that can
  guarantee them: a local database, trusted service, OS, or external provider.
  Client checks improve UX; add server constraints when the server owns truth.
- Make writes idempotent where retries are possible. Use explicit ordering,
  stable tie-breakers, ownership scopes, and pagination rather than SDK defaults.
- After a mutation, reconcile the UI, derived state, background work, and remote
  confirmation as one contract. Prevent older asynchronous results from
  overwriting newer state.
- Choose the fail mode by risk. Safety, publication, destructive operations, and
  authorization uncertainty normally fail closed. Non-critical presentation may
  use a deterministic fallback instead of taking the feature down.
- Complete the loop when relevant: discover, act, confirm, edit or undo, find
  again, and receive only notifications that reflect the latest state.

Keep authorization separate from implementation ability. Do not infer permission
to deploy, upload, submit, publish, migrate production data, spend money, or change
external account settings.

## Keep the product truthful

Model states that would change the user's understanding instead of collapsing
them into a boolean:

- missing is not zero;
- no recorded event is not proof that no event occurred;
- optimistic is not committed;
- durably queued is not remotely saved;
- upload accepted is not store availability;
- inference is not observation;
- permission requested is not permission granted.

Derive success copy and available recovery actions from the actual state. Never
say an action was saved, sent, deleted, published, or completed when the system
only attempted, scheduled, or inferred it.

Treat time, identity, and measurement labels as product contracts. Define the
anchor, time zone, day boundary, unit, denominator, population, window, and
missing-data rule when any of them affect the result. At account boundaries,
remove prior-user state from the active session. Clear disposable caches, widgets,
notifications, and background artifacts; quarantine or retain recoverable queued
writes under their original identity according to an explicit recovery or discard
policy. Never expose or transmit them as another user.

For AI-backed features, compute authoritative facts and eligibility outside the
model when feasible. Give the model only the minimum structured facts it needs.
Do not let the same probabilistic component both generate a high-stakes item and
grant its final safety approval. Validate the exact model, tool, response-mode,
and endpoint combination used by the app; successful pieces do not prove their
composition.

## Verify the layer that can fail

Start with the original symptom or an equivalent failing case. Add the smallest
regression that fails for the intended reason before changing the implementation
when the bug and test boundary are reproducible.

Select checks by risk, not ceremony:

- invariant and boundary-value tests for domain decisions;
- repository, schema, queue, and API tests for persistence and synchronization;
- rendered interaction tests under realistic geometry, keyboard, theme, text
  scale, rapid actions, and failure states for UI bugs;
- cold/warm start, background/resume, deep-link, notification, permission-denied,
  and account-switch checks when lifecycle is involved;
- merged native configuration for resolved release settings, then the exact
  packaged or signed artifact as a separate proof for permissions, entitlements,
  identity, environment values, and versions;
- emulator or physical-device execution for OS-owned behavior;
- remote read-back for uploads, store state, backend migrations, and provider
  configuration when access and authorization permit it.

Read [verification ladders](references/verification-ladders.md) when the required
evidence is unclear or the work approaches distribution. Do not weaken tests,
guards, privacy controls, or acceptance criteria merely to obtain green output.

When retries are not producing new evidence, classify the failing boundary before
editing again: application logic, build toolchain, signing, provider configuration,
device or account state, transport, or store processing. Capture the exact error
and compare a known-good path before changing an adjacent layer.

Use [failure patterns](references/failure-patterns.md) for repeated failures,
release-only defects, or planning a risky cross-boundary feature. The examples are
synthetic and describe diagnostic patterns, not mandatory architecture.

## Coordinate release as a transaction

When release or store delivery is in scope, coordinate the exact app commit,
backend and migration state, production configuration, version and build number,
signed artifact, store metadata, privacy claims, rollout order, compatibility,
rollback, and any human-owned console step.

Build/sign success, upload transport, store processing, review, and user
availability are separate states. Preserve a known signed artifact across a safe
transport retry instead of rebuilding it without cause. Verify the final remote
state after an authorized upload or submission.

Do not hard-code changing SDK, OS, or store-review rules in the implementation
plan. Check current first-party documentation when those rules affect the work.

## Report the actual boundary reached

Lead with the user-visible outcome and strongest evidence. Include:

```markdown
Result:
Target platform and user path:
Verified evidence:
State and data guarantees:
Not verified / external actions remaining:
Rollback or recovery notes, if relevant:
```

Use **verified**, **partially verified**, or **not verified** precisely. Never
describe a simulator check as a physical-device check, source configuration as
artifact inspection, an attempted upload as publication, or another agent's
report as direct observation.
