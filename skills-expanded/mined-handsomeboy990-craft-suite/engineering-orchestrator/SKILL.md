---
name: engineering-orchestrator
description: Central routing layer for engineering work: classifies the request, detects the affected surface and the real stack, selects the smallest complete set of dev skills, orders them, defines the verification gates and decides when the task is done. Load first on any coding, review, debugging or release request.
license: MIT
metadata:
  category: dev-skills
  version: 1.1.0
  depends_on: [engineering-core, project-exploration]
  outputs: [task-classification, execution-plan, verification-gates, completion-verdict]
---

# Engineering Orchestrator

Decides what happens, in what order, and when to stop. Every other dev skill
is a specialist; this one is the lead engineer who assigns them.

Two failure modes are equally bad: activating everything for a typo, and
skipping a security gate to save tokens. The orchestrator optimises for the
smallest plan that still contains every mandatory gate.

## 1. Protocol

1. **Read the request literally.** Extract the requested outcome, not the
   supposed intent behind it. Record what was explicitly asked and what was
   not.
2. **Classify** the task into one or more categories from section 2.
3. **Locate the surface**: which application, which layer, which files. When
   this cannot be answered, exploration is the first step by definition.
4. **Establish the stack** through `project-exploration`, at the depth from
   its section 2.
5. **Compose the plan** from section 3, then apply the mandatory gates in
   section 4 and the exclusion rules in section 5.
6. **Announce the plan in one block**, at most one line per step.
7. **Execute step by step.** Before each step, classify its complexity with
   `task-complexity` and route it with `model-routing`; the two run per step,
   not once for the whole request, because a plan's steps rarely carry the
   same risk. On every dispatch to a subagent, resolve a model per
   `model-routing` section 7 and pass it through the dispatch override,
   without exception; an agent's own frontmatter default is never relied on
   to happen to match. Record the dispatch in `model-routing`'s routing log.
   After each step, check its exit condition before moving on.
8. **Re-plan when a step invalidates an assumption.** A discovery that changes
   the category restarts planning from step 2, and the change is stated. The
   same discovery is a reclassification for `task-complexity` and an
   escalation or de-escalation for `model-routing`: one event, read by all
   three, never three separate judgment calls reaching different answers.
   **Escalate without re-planning when a step's returned output fails a
   quality check** instead: shallow against the brief's acceptance items, a
   factual error found on verification, an uncited claim where one was
   required, a missed required section, a failed test or review gate, or a
   contradiction with a source. This is `model-routing`'s
   `output-quality-failure` trigger, section 6: the category and the plan do
   not change, the step is redispatched one model tier stronger with the
   failed output kept for comparison, and the escalation is recorded in the
   routing log. A second failure of the same step at the strongest tier is
   not redispatched a third time; it is anti-loop rule 5, a blocker reported
   to whoever owns the task, not absorbed by another dispatch.
9. **Close** with the completion verdict of section 7.

## 2. Classification

A request receives one primary category and any number of secondary ones. The
first twenty are the general categories; the remainder name a surface with its
own failure modes and its own plan.

| Category | Recognised by |
|---|---|
| EXPLORATION | unfamiliar codebase, how does X work, where is Y |
| ARCHITECTURE | new subsystem, boundary change, data ownership, scaling shape |
| FRONTEND | component, page, client state, form, rendering |
| BACKEND | endpoint, handler, service, job, queue, business rule |
| FULLSTACK | a feature crossing client and server |
| DATABASE | schema, migration, query, index, transaction |
| API | contract, versioning, payload shape, status codes |
| AUTHENTICATION | login, session, token, provider, password, MFA |
| SECURITY | vulnerability, audit, hardening, incident, dependency alert |
| VALIDATION | untrusted input, schema, sanitisation, boundary |
| DEBUGGING | reported defect, unexpected behaviour, failing test, crash |
| PERFORMANCE | slow, timeout, memory, bundle size, query cost |
| UI_UX | layout, visual design, interaction, accessibility, responsive |
| TESTING | coverage, missing tests, flaky test, test strategy |
| BROWSER_AUTOMATION | end to end flow, screenshot, visual check, journey |
| DOCUMENTATION | readme, api docs, setup, decision record |
| GIT | branch, commit, pull request, history, conflict |
| RELEASE | ship, deploy readiness, changelog, version |
| REFACTORING | restructure without behaviour change |
| DEPENDENCY | add, remove, replace or upgrade a library |
| QUALITY_CAMPAIGN | validate a whole product, QA campaign, release validation |
| ACCESSIBILITY | keyboard, screen reader, contrast, WCAG, audit |
| REGRESSION | after a fix or a merge, what still works |
| MIGRATION | framework, provider, database or architecture change |
| LEGACY | inherited codebase, no tests, nobody knows how it works |
| INCIDENT | production degraded, outage, data at risk, postmortem |
| INFRASTRUCTURE | provisioning, terraform, cloud resources, environments |
| PAYMENTS | checkout, subscription, invoice, refund, webhook from a provider |
| JOBS | queue, worker, cron, scheduled task, webhook consumer |
| REALTIME | websocket, live updates, presence, collaboration |
| FILES | upload, download, attachment, media, export, import |
| I18N | translation, locale, timezone, currency format, right to left |
| SEO | metadata, sitemap, canonical, indexing, structured data |
| DESIGN_SYSTEM | tokens, component library, theme, visual consistency |
| PRIVACY | personal data, retention, erasure, consent, export |
| CACHING | cache, invalidation, CDN, stale data |
| ANALYTICS | events, funnels, conversion, product measurement |
| FEATURE_FLAGS | toggle, gradual rollout, kill switch, experiment |
| SITE_TEMPLATE | a client site from a content file, portfolio or showcase, no-code handover |

Misclassification is cheap to fix and expensive to ignore. When two categories
compete, take the one with the stricter gates.

## 3. Plan composition

Canonical plans live in `resources/execution-plans.md`, one per category, in a
machine checkable format. The orchestrator starts from the canonical plan and
adapts it to the project.

Adaptation rules:

- A step whose skill has no purchase on this project is dropped, with the
  reason stated. Example: `playwright-automation` on a repository with no
  browser surface.
- A step is added when the surface demands it. Example: adding
  `input-validation` to a FRONTEND task because the page introduces a server
  action.
- Steps are never reordered across a gate boundary from section 4.

Composition for multi category requests: merge the plans, deduplicate, and
keep the earliest position of each step.

## 4. Mandatory gates

These are never dropped to save time. Dropping one is a defect in the plan,
not an optimisation.

| Gate | Applies when | Enforced by |
|---|---|---|
| Exploration before decision | any unread code is touched | `project-exploration` |
| Validation before persistence | any new external input reaches storage or a side effect | `input-validation` |
| Authorization before exposure | any new route, action or query returning user scoped data | `security-audit` |
| Security review before merge | auth, payments, uploads, user content, permissions, secrets, dependencies | `security-audit` |
| Test before done | any behaviour change | `testing-quality` |
| Review before delivery | any code written by the agent | `code-review-protocol` |
| Continuity before handoff | any session that changed the repository | `project-continuity` |
| Author check before commit | every commit | `git-workflow` |

A gate can be satisfied by evidence rather than by a full skill run. Example:
the test gate is satisfied when the change is covered by an existing test that
was executed and observed to fail before and pass after.

## 5. Exclusion rules

The orchestrator does not activate:

- `architecture-design` for a change confined to one existing module;
- `ui-ux-engineering` for a change with no visual output;
- `playwright-automation` when no browser tooling exists and the task does not
  justify introducing it;
- `performance-engineering` without a measurement or a concrete symptom;
- `dependency-selection` unless a library is actually being added, replaced or
  removed;
- `release-readiness` outside an explicit ship or release request;
- itself, recursively. One orchestration per request, re-planned in place.

## 6. Anti-loop rules

1. A skill runs at most twice per task. The second run must state what changed
   since the first.
2. A finding rejected once is not re-raised in the same form.
3. When two skills disagree, the stricter one wins for security and
   correctness, the project convention wins for style.
4. Verification is not repeated when its inputs are unchanged.
5. When a plan produces no progress twice in a row, the orchestrator stops and
   reports the exact blocker rather than cycling.

These five rules are enforced here, at the orchestrator. `token-optimization`
is the discipline that keeps each individual step proportional; it does not
duplicate this section and this section does not duplicate it.

## 7. Completion verdict

The task is complete when all of the following are true, each with evidence:

1. Every step of the plan ran or was dropped with a stated reason.
2. Every mandatory gate that applies was satisfied.
3. The definition of done from `engineering-core` section 8 passes.
4. The user visible outcome matches the literal request.
5. What remains is named, or nothing remains.

The verdict is one of `Complete`, `Partial` with the named remainder, or
`Blocked` with the exact external blocker. There is no fourth value, and
`Complete` is never used to mean almost complete.

## 8. Plan announcement format

```
Category: BACKEND, secondary SECURITY
Surface: apps/api, payments module
Plan:
  1 project-exploration L2, payments slice
  2 architecture-design, transaction boundary only
  3 backend-engineering, the endpoint
  4 input-validation, request body and idempotency key
  5 security-audit, authorization and amount handling
  6 testing-quality, unit plus integration
  7 code-review-protocol
  8 technical-documentation, api reference
  9 project-continuity
  10 git-workflow
Dropped: ui-ux-engineering, no visual surface.
```

Nine lines of plan for a day of work is correct. Nine paragraphs is not.

## 9. Auto-critique

Score from 0 to 5: classification accuracy, minimality of the plan, presence
of every applicable gate, correctness of the ordering, quality of the dropped
step reasons, honesty of the completion verdict.

Threshold: no axis below 3, average at least 4. A plan missing an applicable
gate scores 0 on that axis regardless of the rest, and is recomposed.

## 10. Auto-critique of the orchestrator itself

Every fifth task, verify that plans are not drifting toward a fixed maximal
sequence. Symptom: the same twelve steps for tasks of very different size.
Cause: classification collapsed into one category. Correction: re-read
section 2 and re-derive the surface.

## 11. Interfaces

- Upstream: `engineering-core`.
- Downstream: every skill in `dev-skills`.
- Reference data: `resources/execution-plans.md`,
  `resources/routing-table.md`.
- Validated by: `tests/validate-orchestration.sh`.
