---
name: quality-engineering
description: Coordinates a whole quality campaign: inspects the project to build a testing map, asks the decision-critical questions once, fixes the testing contract, selects which test disciplines actually apply to this product, sequences them, and issues the final quality verdict. Load first on any QA campaign, test plan, release validation or full product verification request.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core, project-exploration, testing-quality]
  outputs: [testing-map, testing-brief, testing-contract, test-strategy, campaign-plan, quality-verdict]
---

# Quality Engineering

`testing-quality` decides how one behaviour is tested. This skill decides what
a whole product needs before anyone can be told it is ready.

Two failure modes are equally bad: running every discipline on a brochure
site, and declaring a payment platform validated because the suite is green.
The campaign is the smallest set of disciplines that covers the risk this
product actually carries.

## 1. The project is the source of truth

Nothing is assumed. Not the framework, the runtime, the package manager, the
routes, the authentication mechanism, the database, the test runner, the
environments, the roles, the browser matrix, or the coverage that already
exists.

Run `project-exploration` first, then extend it with the quality specific
sweep in `resources/discovery-checklist.md`. The output is a testing map:

```
Product type        what kind of system this is, from section 4
Surfaces            web UI, API, jobs, CLI, mobile web, admin
Stack               runtime, framework, package manager, lockfile
Environments        which exist, which are safe to touch
Entry points        routes, endpoints, forms, uploads, webhooks
Identity            authentication mechanism, roles, tenancy model
Data                stores, migrations, seeds, fixtures
Existing coverage   frameworks configured, suites present, what they cover
Existing evidence   CI results, reports, known failures, skipped tests
Gaps                what the repository cannot answer
```

Only the `Gaps` line becomes a question. Everything else was read.

## 2. The testing brief

One batch, once, before a campaign of any size. Never one question at a time,
never a question the repository already answered.

The questions that materially change the plan:

```
Target environment and base URL, and whether it is production
Which environments may be exercised, and which are forbidden
Test accounts available, and the roles they hold
The business flows whose breakage is an incident
Browser and device support that is actually promised
Languages and locales in scope
Known bugs and known limitations, so they are not rediscovered
Authorization for security testing, and its exact boundary
Performance expectations, if any exist as requirements
Accessibility target, if one is contractual
Expected deliverables
Whether defects may be fixed, or only reported
Whether tests may write persistent data
Whether destructive scenarios are permitted
```

Drop every line discovery already settled. A brief of four questions on a
small project is a good brief. `clarification-gate` holds the general form of
this rule; this is its quality specific instance.

## 3. The testing contract

The answers become a short contract, and the contract becomes the source of
truth for the campaign. Format in `resources/testing-contract.md`.

```
Scope                what is tested, and what is explicitly not
Environment          base URL, environment name, application version
Objectives           what the campaign must answer
Critical flows       ordered, because they are tested first
Disciplines          which of the test disciplines are in the campaign
Allowed actions      writes, account creation, uploads, payments in test mode
Forbidden actions    named, including every production side effect
Security boundary    exact targets in scope, everything else out
Data constraints     what may be created, modified, or never touched
Device and browser   the matrix that will actually be exercised
Deliverables         report, evidence, tests committed to the repository
Acceptance           what a pass means for this campaign
```

Scope never expands silently. A discovery outside the contract is reported and
either added by decision or recorded as out of scope. `scope-and-change-control`
governs the same rule for delivery work.

## 4. Strategy by product type

The product type decides where the risk concentrates. Identify it, then weight
the campaign.

| Product type | Where the risk concentrates |
|---|---|
| marketing site | navigation, forms, assets, responsive, performance, metadata |
| SaaS | tenancy, roles, subscription states, invitations, data isolation, billing |
| e-commerce | cart, pricing, inventory, checkout, payment, order state, duplicates |
| marketplace | two sided permissions, listings, payouts, disputes, moderation |
| financial | amounts, rounding, idempotency, audit trail, authorization, reconciliation |
| healthcare | access control, consent, data retention, audit trail, correctness |
| administrative platform | roles, workflow states, records, exports, retention |
| dashboard | queries, aggregation correctness, empty and large data, permissions |
| public API | contract, versioning, authorization, rate limits, error shape |
| internal API | authorization between services, timeouts, retries, idempotency |
| authentication service | sessions, tokens, expiry, revocation, enumeration, lockout |
| real time application | connection loss, reconnection, ordering, duplicates, presence |
| content platform | rendering of user content, moderation, media, search |
| multi-tenant | isolation on every read and every write, identifier manipulation |

A product is often two of these. Take the union of the risks, not the
intersection.

## 5. Selecting the disciplines

Each discipline is a skill. It enters the campaign when its trigger is true,
and stays out otherwise, with the reason stated.

| Discipline | Skill | Enters when |
|---|---|---|
| layered automated tests | `testing-quality` | any behaviour is being changed or is unverified |
| API and contract | `api-testing` | the product exposes or consumes an HTTP contract |
| browser journeys | `playwright-automation` | there is a UI and a journey whose breakage matters |
| exploratory and usability | `exploratory-testing` | a human facing surface exists |
| adversarial interaction | `bug-hunting` | a UI or an API accepts repeated or concurrent action |
| accessibility | `accessibility-testing` | there is a UI, always |
| authorized security | `security-testing` | roles, tenancy, payments, uploads, or personal data exist |
| static security sweep | `security-audit` | source is available |
| reliability and recovery | `reliability-testing` | the system depends on anything that can fail |
| performance | `performance-engineering` | a threshold exists, or a symptom was reported |
| regression | `regression-testing` | anything was changed or fixed during the campaign |
| evidence and report | `test-reporting` | a campaign produces findings, which is always |

Accessibility is not optional because nobody asked for it. It is dropped only
when there is no user interface at all.

## 6. Campaign order

```
1  discovery, testing map
2  brief and contract
3  static reading: existing suites, existing failures, existing skips
4  automated layers, lowest first: unit, integration, contract
5  API surface
6  browser journeys, the critical flows only
7  exploratory passes, then adversarial passes
8  accessibility
9  responsive and cross browser, where promised
10 reliability and recovery
11 authorized security testing
12 performance, against real thresholds
13 defect fixing, if the contract allows it
14 regression on everything the fixes touched
15 report, evidence, verdict
16 continuity notes
```

Steps are dropped by contract, never by fatigue. A dropped step is named in
the report with its reason.

## 7. Tooling

Inspect before installing. `dependency-selection` holds the general
evaluation; the quality specific rules are:

1. Read the package manifest, the lockfile and the CI configuration.
2. Use the runner the project already has. A second overlapping framework is a
   maintenance cost paid forever for one campaign.
3. Install only what the contract requires, with the project package manager,
   at a version compatible with the project.
4. Update the lockfile the way the project updates it, and commit it.
5. Verify the tool runs before writing anything with it.
6. Record every testing dependency introduced, and why, in the report.

A new framework is justified only when the project has none, or when the
existing one cannot observe the behaviour under test. Both cases are written
down before the install command runs.

## 8. Prohibitions

- Never report `everything looks good`. A pass names what was executed, what
  passed, and what was not covered.
- Never treat a green suite as evidence about behaviour the suite does not
  exercise.
- Never expand scope, or touch a target, outside the contract.
- Never run a destructive or security sensitive scenario without explicit
  written authorization in the contract.
- Never present an unreproduced observation as a defect.
- Never present a warning as a defect without deciding origin, impact and
  reproducibility.
- Never hide a discipline that was skipped.
- Never let coverage percentage stand in for coverage of behaviour.

## 9. The final quality gate

Ready means every line below is true, each with evidence. Anything else is
reported as it is.

```
1  critical flows exercised and passing
2  the mandatory cases of testing-quality covered on changed behaviour
3  regression run on everything the campaign touched
4  critical and high defects fixed, or accepted in writing by name
5  authorized security scope completed, findings ranked honestly
6  accessibility completed where a UI exists
7  responsive and browser matrix exercised as promised
8  console and network findings resolved or documented with a reason
9  reliability behaviour verified for the dependencies that can fail
10 performance measured against stated thresholds, or measured and reported
11 the suite is stable across two consecutive runs
12 report produced, evidence attached, gaps named
```

Verdict, one value only:

```
PASS                   every line true
PASS WITH WARNINGS     every blocking line true, named non blocking findings
BLOCKED                the campaign could not be run, with the exact blocker
FAIL                   a critical flow, a security boundary or a data path is broken
```

The verdict carries its reason in one sentence. `release-readiness` consumes
it; it does not replace it.

## 10. Campaign self-critique

Before declaring completion, review the campaign from other chairs:

```
QA lead              did we test what matters, or what was easy to test
senior developer     did we test behaviour, or implementation detail
security reviewer    did we cross a boundary, or only the front door
accessibility        did we press Tab, or only run a scanner
end user             could a real person complete the job
release manager      would we ship this, and what would we say if it broke
```

Any answer that exposes a hole reopens the campaign for that hole only, not
for everything.

## 11. Protocol

1. Run discovery and build the testing map.
2. Ask the remaining questions in one batch.
3. Write the contract and get it confirmed when anything in it is destructive,
   production facing or security sensitive.
4. Identify the product type and weight the risk.
5. Select the disciplines and state which are dropped and why.
6. Verify or install the tooling, minimally.
7. Execute the campaign in the order of section 6.
8. Record every finding as it appears, with evidence, through `test-reporting`.
9. Fix only what the contract allows, then re-test each fix and run regression.
10. Run the self-critique of section 10.
11. Apply the gate of section 9 and issue one verdict.
12. Write the continuity notes so the next campaign starts from here.

## 12. Auto-critique

Score from 0 to 5: discovery completeness, question economy, contract clarity,
correctness of the discipline selection, order respected, evidence quality,
honesty about what was not covered, verdict supported by that evidence.

Threshold: no axis below 3, average at least 4. A campaign that reports a pass
while a critical flow was never exercised scores 0 overall, whatever the rest
looks like.

## 13. Interfaces

- Upstream: `engineering-core`, `project-exploration`, `engineering-orchestrator`.
- Disciplines: `testing-quality`, `api-testing`, `playwright-automation`,
  `exploratory-testing`, `bug-hunting`, `accessibility-testing`,
  `security-testing`, `reliability-testing`, `regression-testing`,
  `performance-engineering`, `security-audit`.
- Lateral: `clarification-gate` for the question discipline,
  `scope-and-change-control` for scope, `dependency-selection` for tooling,
  `implementation-integrity` for fake functionality.
- Downstream: `test-reporting`, `release-readiness`, `project-continuity`,
  `shared/self-critique`.
