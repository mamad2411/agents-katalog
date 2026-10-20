---
name: implementation-integrity
description: Forbids and detects fake functionality: stub handlers, mock saves, fake success, hardcoded data pretending to come from a source, dead buttons, unfinished forms, simulated payments and placeholder business logic. Run before any feature is called complete and before every release.
license: MIT
metadata:
  category: delivery-skills
  version: 1.0.0
  depends_on: [engineering-core]
  outputs: [integrity-scan, stub-register, honest-completion-report]
---

# Implementation Integrity

A feature that appears to work and does not is worse than a feature that is
visibly missing. The missing one gets scheduled. The fake one gets shipped,
demonstrated, and discovered by a user.

This skill defines what counts as fake, how to find it, and what to do when
something genuinely cannot be built yet.

## 1. What counts as fake

| Pattern | Looks like | Actually |
|---|---|---|
| stub handler | an endpoint exists | returns a constant, ignores the input |
| mock save | a success message | nothing was persisted |
| fake success | the UI advances | no request was made, or its result was ignored |
| simulated delay | a spinner then a result | `setTimeout` pretending to be work |
| hardcoded data | a populated list | an array in the component, not the database |
| dead control | a button, a link, a menu item | no handler, or a handler that does nothing |
| unfinished form | a complete form | some fields are never read or never sent |
| placeholder logic | a business rule | returns true, or a constant, or the first case |
| fake authentication | a login screen | any password works, or the check is client side |
| fake payment | a checkout | no provider call, or the response is ignored |
| swallowed failure | a working feature | the error is caught and discarded, UI shows success |
| optimistic without rollback | instant feedback | the failure never reverts the display |
| TODO in a shipped path | a note | a hole a user will reach |

The last three are the subtle ones. They pass a demonstration, pass a happy
path test, and fail in production in a way that produces no error anyone sees.

## 2. The honesty rule

Every path a user can reach either works, or visibly does not exist.

There is no third state. A control that is present must do what it appears to
do. A feature that is not built is not rendered, or is rendered as
unavailable with a reason.

```
Acceptable:  the export button is absent, export is not built yet
Acceptable:  the export button is disabled with "Available in the next release"
Unacceptable: the export button downloads an empty file
Unacceptable: the export button shows "Export started" and does nothing
```

## 3. Legitimate incompleteness

Three cases are legitimate, and each has a required form.

**A prototype the requirement asked for.** The specification says prototype,
mockup or clickable demo. Then fake data is the deliverable. It is labelled in
the repository, in the UI, and in the handover.

**An external dependency that does not exist yet.** The provider account is
not created, the partner API is not available, the credentials have not
arrived.

```
Required form:
  the integration boundary is written and typed as it will really be
  a single adapter implements it, and throws a named error, not a fake success
  the UI shows the feature as unavailable, with the reason
  the blocker is recorded in the continuity notes and the checklist
  a test asserts the unavailable behaviour, so it cannot silently ship as fake
```

**A deliberate feature flag.** The code exists, is tested and is disabled. The
flag is read from configuration, the disabled path is honest, and the flag is
in the handover documentation.

Everything else is a defect.

## 4. Detection

Static passes, run over the diff or the repository. Adapt the patterns to the
project's language.

```
Markers
  TODO, FIXME, XXX, HACK, WIP, "not implemented", "coming soon"
  "placeholder", "dummy", "fake", "mock" outside test directories

Fake asynchrony
  setTimeout used to simulate work
  Promise.resolve of a literal in a path that should call something

Ignored results
  an await whose result is never read in a path that depends on it
  a catch block that is empty, or that logs and continues to a success state
  a response whose status is never checked

Hardcoded data
  arrays of objects in a component or a handler that mirror a table shape
  identifiers that look like sample data: test@, foo, bar, lorem

Dead controls
  a button with no onClick, or onClick={() => {}}
  a link with href="#" outside a deliberate anchor
  a form with no submit handler, or a handler that does not send

Placeholder logic
  a function returning a constant where the name implies a computation
  a permission check returning true
  a validation function that never rejects
```

Then the dynamic pass, which finds what the static one cannot: run the flow
and confirm the effect. Create the record, then read it back from the
database. Send the request, then check the provider dashboard or the log.

The static pass finds the honest stubs. The dynamic pass finds the ones that
were written to look complete.

## 5. The reload test

The cheapest test for fake persistence, and the one that catches most of it:

```
1  perform the action
2  observe the success feedback
3  reload the page from the server
4  is the change still there
```

A mock save passes steps 1 and 2 and fails step 3. A feature that has never
had step 3 performed on it is not verified, whatever the UI said.

## 6. Stub register

Anything legitimately incomplete under section 3 is registered, not
remembered.

```
| # | What | Why | Form | Blocker | Visible to user as |
|---|---|---|---|---|---|
| S1 | mail delivery | provider account pending | adapter throws NotConfigured | client to create account | "Email delivery is not yet configured" |
```

The register goes into the continuity notes and the delivery checklist. Item
16 of the checklist is marked done only when this register is the complete
list of incompleteness and every entry has the required form.

## 7. Protocol

1. Run the static passes of section 4 over the changed code.
2. Run the dynamic pass on every feature the change touches.
3. Apply the reload test to every persisting action.
4. Classify each finding: defect, or legitimate under section 3.
5. Fix every defect. There is no deferral for fake functionality on a path a
   user can reach.
6. Put every legitimate incompleteness into the required form and register it.
7. Report honestly, section 8.

## 8. Report

```
Scanned:        the diff for M6a, 14 files
Static findings: 3
  components/export-button.tsx:12  onClick={() => {}}, dead control
  lib/services/report.ts:40        returns a hardcoded array
  app/api/webhooks/route.ts:22     catch block logs and returns 200
Dynamic findings: 1
  the invitation form shows "Invitation sent" and no row is created; the
  service is called without await
Reload test:     invitations fails, courses passes, enrolment passes
Fixed:           4 of 4
Legitimate:      1, S1 mail delivery, registered
```

## 9. Auto-critique

Score from 0 to 5: static passes actually run, dynamic pass performed rather
than reasoned, reload test applied to every persisting action, correct
classification of legitimate incompleteness, required form applied, register
complete, honesty of the report.

Threshold: no axis below 3, average at least 4. One fake success left on a
reachable path is an automatic failure, whatever else the scan found.

## 10. Interfaces

- Upstream: every implementation skill, `delivery-planning`.
- Lateral: `code-review-protocol`, which treats these findings as blockers.
- Downstream: `project-continuity` for the register, `release-readiness`,
  which refuses a release with an unregistered stub.
