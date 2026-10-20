---
name: jquery-orchestrator
description: Use when a jQuery request spans multiple capability areas — source curation, core DOM, events, AJAX, plugins, performance, migration, testing, security, or CI integration — and needs one deterministic intake, explicit phase ownership, and a unified execution contract.
---

# jQuery Orchestrator

## Specialization

Coordinate cross-cutting jQuery requests from one intake when work spans source curation, DOM implementation, event handling, AJAX integration, plugin development, performance optimization, version migration, testing, security review, CI enforcement, and quality gating.

This skill is specialized for intake, phase ownership, and unified synthesis. It does not replace deep execution guidance — it routes to the appropriate specialist jQuery skill for each phase.

## Objective

Produce one deterministic jQuery execution contract from a single intake — with explicit phase ownership, evidence expectations, and closure checks — for any request that spans more than one jQuery capability area.

## Trigger Conditions

- A jQuery request spans more than one capability area (e.g., new feature implementation + security audit + test coverage).
- A project is adopting jQuery for the first time and needs end-to-end implementation guidance.
- An existing jQuery codebase requires a full-cycle review: sources → DOM → events → AJAX → performance → security → gate.
- A jQuery version upgrade spans multiple remediation areas (deprecated API, plugin compatibility, test updates).
- A team needs one intake instead of disconnected implementation, security, and review workflows.
- A major jQuery release requires an impact assessment across all capability areas.

## When Not to Use

- The request is clearly scoped to one capability area — use the specialist skill directly.
- Source-only freshness check (use `jquery-source-curation` directly).
- A single security finding requires remediation (use `jquery-security` directly).
- A single quality gate is needed for a completed feature (use `jquery-quality-gate` directly).

## Scope Boundaries

In scope:

- Deterministic jQuery intake and phased execution planning.
- Phase-output ownership with exactly one owner per required output.
- Unified execution recommendation for mixed jQuery requests.
- Cross-phase dependency mapping (source freshness → core → events/ajax → performance/security → testing → gate).

Out of scope:

- Deep implementation within any one phase.
- Non-jQuery frontend tooling unless it directly gates a jQuery phase.
- Server-side endpoint implementation.
- Framework migration (jQuery → React/Vue) — this skill covers jQuery-to-jQuery-v3 migration only.

## Inputs

- User objective and target jQuery surface (new feature, version upgrade, security audit, full project review).
- jQuery version in use or target version.
- Scope boundaries, browser target matrix, and risk level.
- Required outputs, known constraints, and delivery timeline.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness.

## Required Outputs

- Intake contract with objective, scope boundaries, and required outputs.
- Phase-output ownership matrix.
- Unified jQuery execution recommendation.
- Rejected-phase table with deterministic reason codes.
- Closure check confirming all required outputs are owned.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Route one mixed jQuery request | One intake and one phase contract exist |
| L2 Delivery | Coordinate a cross-phase jQuery effort | Every required output has one owning phase |
| L3 Hardening | Support production-grade jQuery delivery | Risks, CVE posture, evidence expectations, and blockers are explicit |
| L4 Expert Standardization | Establish reusable jQuery operating model | Reusable intake, security baseline, plugin conventions, CI quality policy documented |

## jQuery Capability Catalog

| Phase | Specialist Skill | When Active |
|---|---|---|
| Source Curation | `jquery-source-curation` | First adoption, major jQuery version change, source freshness check required |
| Core DOM | `jquery-core` | DOM selection, traversal, manipulation, chaining, or `.data()` usage |
| Events | `jquery-events` | Event binding, delegation, namespace design, custom events, deprecated event API |
| AJAX | `jquery-ajax` | `$.ajax()`, Deferred/Promise chains, CSRF token injection, JSONP replacement |
| Plugins | `jquery-plugins` | Plugin authoring, jQuery UI widget integration, jQuery Validation, community plugin evaluation |
| Performance | `jquery-performance` | Selector caching, DOM batching, handler accumulation, animation queue, memory leaks |
| Migration | `jquery-migration` | v1/v2 → v3 upgrade, jQuery Migrate plugin triage, native API replacement |
| Testing | `jquery-testing` | QUnit or Jest test design, event simulation, AJAX mocking, Deferred contract tests, plugin lifecycle tests |
| Security | `jquery-security` | XSS sink audit, CSRF review, JSONP exposure, CVE assessment, CSP compliance |
| CI Integration | `jquery-ci-integration` | Automated test execution, Migrate deprecation gate, ESLint API gate, CVE scan, bundle size enforcement |
| Quality Gate | `jquery-quality-gate` | Pre-merge review, pre-promotion gate, or full-project quality audit |

## Deterministic Workflow

1. Lock objective, risk boundary, jQuery version, and required outputs.
2. Classify the request into one or more capability phases from the catalog above.
3. Assign exactly one owner per required output using the phase assignment table.
4. Map cross-phase dependencies:
   - Source freshness must precede all other phases when version context is uncertain.
   - Core, Events, and AJAX must precede Performance and Security reviews.
   - Migration must precede the Quality Gate if a version upgrade is in scope.
   - Testing must precede the Quality Gate.
5. Identify phases not active and record them in the rejected-phase table with reason codes.
6. Confirm closure: every required output has an owner.
7. Emit the execution contract.

## Phase Assignment Table

| Required Output Type | Owning Phase |
|---|---|
| Source freshness baseline, version-impact note | Source Curation |
| Selector patterns, traversal chains, manipulation sequences, `.data()` usage | Core DOM |
| Event handler bindings, delegation topology, namespace plan, custom event contracts | Events |
| `$.ajax()` configuration, Deferred chains, CSRF strategy, parallel coordination | AJAX |
| Plugin implementation, jQuery UI widget, jQuery Validation config, plugin evaluation report | Plugins |
| Selector cache audit, DOM batching plan, handler accumulation analysis, debounce patterns | Performance |
| Migrate warning log, breaking-change remediation, native API replacement map, phased migration plan | Migration |
| Test suite: DOM isolation, event simulation, AJAX mocks, Deferred contracts, plugin lifecycle | Testing |
| XSS finding inventory, CSRF audit, JSONP replacement, CVE assessment, CSP finding | Security |
| CI jobs: test execution, Migrate gate, ESLint API gate, CVE scan, bundle budget, artifact contract | CI Integration |
| Gate recommendation (Pass / Pass with Conditions / No-Go), finding set, conditions/blockers | Quality Gate |

## Rejected Phase Reason Codes

| Code | Meaning |
|---|---|
| `P1` | Phase is out of scope for this request |
| `P2` | Phase dependency not yet met — deferred to next iteration |
| `P3` | Phase was already completed in a prior gate cycle — evidence is current |
| `P4` | Request is too narrow to warrant this phase |

## Example Contracts

### Scenario A: New jQuery Feature with Security Mandate

Phases active: Core DOM → Events → AJAX → Security → Testing → Quality Gate
Phases rejected: Source Curation (P3 — sources current), Migration (P1 — no version change), Performance (P4 — narrow scope), Plugins (P1 — no plugins involved)

### Scenario B: jQuery v1 → v3 Upgrade

Phases active: Source Curation → Migration → Core DOM (deprecated API fixes) → Events (deprecated event API) → AJAX (Deferred API) → Testing (regression suite) → CI Integration (Migrate gate + ESLint API gate) → Quality Gate
Phases rejected: Plugins (only if no plugins are in scope), Security (defer to separate cycle unless CVE is in scope)

### Scenario C: Full Project Audit

All phases active. Source Curation must complete before other phases consume its version-impact note. Security and Performance run in parallel after Core, Events, and AJAX are reviewed. Testing and Quality Gate are final.

## Done Criteria

- Intake contract exists with objective, boundaries, and required outputs.
- Phase-output ownership matrix has no unowned or multiply owned outputs.
- Deterministic phase order and handoff criteria are explicit.
- Rejected-phase table exists with reason codes for all excluded phases.
- Closure check passes.

## References

- [jQuery API Documentation](https://api.jquery.com)
- [jQuery Learn Center](https://learn.jquery.com)
- [jQuery Migrate Plugin](https://github.com/jquery/jquery-migrate)
- [jQuery 3 Upgrade Guide](https://jquery.com/upgrade-guide/3.0/)
- [jQuery Blog](https://blog.jquery.com)
- Companion skills: `jquery-source-curation`, `jquery-core`, `jquery-events`, `jquery-ajax`, `jquery-plugins`, `jquery-performance`, `jquery-migration`, `jquery-testing`, `jquery-security`, `jquery-ci-integration`, `jquery-quality-gate`


