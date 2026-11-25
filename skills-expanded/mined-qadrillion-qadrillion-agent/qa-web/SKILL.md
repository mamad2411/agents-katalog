---
name: qa-web
description: Author, execute, diagnose and maintain browser QA using observed UI semantics and business outcomes. Use for web journeys, browser state, interaction and relevant accessibility checks.
---

# Web execution

Use through `qa`; load `qa-workflow` and `.agent/rules/test-automation.md`.
The locator, fixture and evidence contracts remain there. Use the team's actual
browser tooling; Playwright is one conditional recipe.

## Prepare the observed interface

Identify browser/engine/version, viewport, locale, timezone and app build. Follow
the changed journey in the running app and inspect its DOM/accessibility tree.
Record the control's actual role/name or identifier, uniqueness in its context,
and resulting state. Source names are useful provenance, not proof that the
served build exposes them. If browser execution is unavailable, record the gap;
source or HTTP inspection does not become a browser run.

Resolve test-account and backend-data ownership before parallel execution.
Separate browser contexts isolate cookies/storage, not shared server records.
Use isolated records/accounts for state-changing tests; persisted authentication
may be reused only where its shared state remains safe. Exercise real login when
login/session behavior is the subject. Treat saved auth and traces as potentially
sensitive artifacts and apply the project's ignore/redaction policy.

## Author the journey

Write setup → user action → observable result with a fresh context and explicit
teardown. Name cases after the criterion. Use role/name, label or observed stable
identifier scoped to the relevant dialog/form/row. Check ambiguous matches before
adding positional selectors. Keep user-visible text assertions when text is the
contract; do not broaden a locator until it silently matches the wrong control.

Assert the business effect: saved content after navigation/reload, the expected
record/total, an error with unchanged state, or completion of the promised job.
A click succeeding, a request being sent or a toast alone may be insufficient.
Use web-first assertions or the runner's equivalent; register event/response
waiters before the triggering action when an event can otherwise be missed.

Cover the selected transition's relevant empty/loading/error/recovery states,
back/forward/deep-link behavior and storage/session boundaries. Use real backend
paths for the chosen end-to-end claim. Label intercepted network responses and
their limits; retain distinct integration coverage for the mocked boundary.

## Execute and investigate

Run one deterministic journey, then the selected suite and justified browser or
viewport variations. Choose variation from supported users and risk, such as a
second engine for layout/input differences or mobile viewport for responsive
navigation. A resized desktop browser does not verify native mobile behavior.

Capture the first failing attempt's trace, screenshot, console errors and relevant
network result where supported. Diagnose in order: target/build and fixture,
actual locator match, actionability/overlay/focus, awaited state, network/business
result. Inspect the failing artifact before changing timeouts or selectors.
For a race, identify the observable readiness condition. For app failure, preserve
the test and reproduce the business symptom with minimal steps.

## Maintain and hand off

Extract repeated stable operations once they recur; keep business assertions
visible in tests. Centralize authentication and fixture lifetime without hiding
cross-test state. Review selectors after accessible-name or product changes;
replace a test only when its criterion becomes obsolete. Preserve supported
variation coverage instead of marking the troublesome engine optional to pass.

Read [the Playwright recipe](references/playwright.md) for a Playwright project
or the local reference exercise. For a relevant accessibility slice, read
[keyboard and accessibility checks](references/accessibility.md); full conformance
is a separately scoped assessment. An exploration charter can use any journey
above, retaining observations, questions and unvisited paths in the shared plan.
