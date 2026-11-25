---
name: app-audit
description: Evidence-driven application audit protocol for security, authorization, privacy, concurrency, state integrity, reliability, performance, accessibility, visual consistency, responsive behavior, and release readiness. Use for incremental checks, pre-merge review, pre-launch audits, high-stakes deep audits, AI-generated code review, hardening, or release-gate design. Prefer this protocol over ad-hoc review when the user asks whether software is safe or ready to ship.
---

# App Audit

An agent-agnostic protocol for auditing software without confusing confidence with evidence.

The protocol is designed around four failure modes of AI-assisted review:

1. **Inherited assumptions:** the reviewer repeats the implementation agent's reasoning.
2. **Scope blindness:** the reviewer audits visible files while missing the real architecture and blast radius.
3. **Static-only certainty:** suspicious code is reported as a confirmed vulnerability without reproduction.
4. **Audit theatre:** a long checklist creates the appearance of rigor without testing the product's actual risk model.

The audit therefore follows a strict sequence:

**Mode selection → reconnaissance → risk model → scope declaration → independent discovery → runtime verification → adversarial verification → report → remediation → re-audit → release decision.**

Do not skip or reorder phases in Release Audit or Deep Audit unless a phase is impossible. If impossible, mark it `NOT TESTED` and explain why.

---

## 0. Select audit mode

State the selected mode and reason in one sentence.

| Mode | Use when | Coverage | Verification |
|---|---|---|---|
| **Fast Check** | Recent diff, named files, small feature, incremental review | Change-impact graph plus affected domains | Static evidence; targeted runtime checks when cheap |
| **Release Audit** | Pre-merge, pre-launch, whole feature or application | All relevant domains across declared critical flows | Critical/High require strong evidence and reproduction where environment permits |
| **Deep Audit** | Payments, auth/authz, multi-tenancy, sensitive/personal data, irreversible actions, or high-impact launch | Independent specialist passes plus runtime and adversarial verification | Critical/High must be independently reproduced or explicitly remain unverified |

Default to **Release Audit** for a vague but serious review request.

Escalate to **Deep Audit** when the system includes payments, authentication/authorization, multi-tenancy, sensitive personal data, destructive or irreversible operations, regulated workflows, or when Release Audit finds plausible Critical/High issues.

Never silently reduce requested scope because the repository is large. Propose staged coverage instead.

### Fast Check blast-radius rule

Fast Check is not limited to changed lines. Before reviewing, identify changed symbols and trace callers, consumers, shared state, persistence effects, authorization boundaries, public contracts, migrations, configuration, and tests. Expand scope when a small diff has broad blast radius.

---

## 1. Reconnaissance: map the system before judging it

Do not declare scope until repository reconnaissance is complete.

Inspect, where present:

- repository tree and workspace boundaries;
- README and architecture docs, but verify claims against implementation;
- package manifests and lockfiles;
- build, runtime, framework, routing, middleware, and deployment configuration;
- frontend entry points and shared state;
- backend/API entry points, server actions, RPC, GraphQL, jobs, queues, cron, workers;
- authentication, authorization, roles, tenancy, middleware, policies, RLS/security rules;
- database schema, migrations, ORM/query layer, transactions, constraints, indexes;
- file/object storage and upload/download paths;
- webhooks and third-party integrations;
- environment variable usage, secret handling, logs, analytics, telemetry, source maps;
- design tokens, shared components, themes, styling architecture;
- tests, fixtures, mocks, CI workflows, scanners, lint/type checks, E2E/browser tooling.

Do not infer architecture from package manifests alone. Follow imports, routes, handlers, data access, middleware, and deployment configuration.

Produce a concise **System Map**:

```markdown
## System Map
- Runtimes and deployable surfaces:
- User roles and privilege levels:
- Critical user flows:
- Sensitive assets/data:
- Trust boundaries:
- Persistence layers:
- External services and webhooks:
- Background/async processing:
- Shared UI/design-system layer:
- Existing tests and controls:
- High-risk surfaces:
- Unknowns requiring clarification or runtime access:
```

For Fast Check, produce a smaller **Change Impact Map** instead.

---

## 2. Establish product context and risk model

An audit cannot calibrate severity without understanding what failure means.

Infer from repository and conversation first. Ask only focused questions for material unknowns.

Establish:

- primary product purpose and critical user journeys;
- sensitive or regulated data handled;
- money movement or financially consequential actions;
- destructive, irreversible, or externally visible actions;
- tenant/user isolation requirements;
- realistic attacker capabilities and exposed surfaces;
- availability and recovery expectations;
- compliance, contractual, or policy constraints explicitly known;
- deployment stage and expected scale;
- whether speed, robustness, or both are the dominant release objective.

Do not invent compliance obligations. If unknown, say unknown.

Create a short **Risk Model** that ranks critical flows and assets. Use it to calibrate severity and testing effort.

---

## 3. Declare scope and testability

Only now declare scope.

Show:

- flows, roles, surfaces, endpoints, files/areas, and domains in scope;
- explicit exclusions;
- environment/tooling available;
- runtime tests possible;
- constraints that prevent verification.

Each domain receives one status in the final report:

- `PASS WITHIN TESTED SCOPE`
- `PARTIAL`
- `FAIL`
- `NOT TESTED`

Never use bare `PASS` for a whole security or accessibility domain. Passing tested checks is not proof of total security or full WCAG conformance.

---

## 4. Independence and evidence protocol

These rules are non-negotiable.

1. **Fresh-read rule.** Audit actual source and runtime behavior. Treat implementation intent, prior summaries, comments, and earlier agent reasoning as claims to verify.
2. **Evidence threshold.** A confirmed finding requires at least one of: precise code path showing reachable impact; reproducible runtime behavior; captured request/response; failing test; scanner result manually validated; observable accessibility or visual failure.
3. **Hypothesis separation.** Suspicious patterns without sufficient evidence belong under `Needs Verification`, never mixed with confirmed findings.
4. **Independent verification.** In Deep Audit, a verifier that did not perform the discovery pass receives only the finding claim, minimal context, evidence pointers, and reproduction hypothesis. Its job is to disprove the finding first, then reproduce it.
5. **No remediation before verification.** Do not patch Critical/High findings before independent verification unless the user explicitly orders emergency containment. Record emergency containment separately.
6. **Redaction.** Never include live secrets, session tokens, personal data, private keys, or exploit payloads containing real sensitive data in reports. Redact while preserving evidentiary value.
7. **No false assurance.** State explicitly that the audit reduces risk but does not prove the application secure, compliant, or defect-free.

### Evidence artefacts

Where tooling permits, preserve:

- file and line references;
- sanitized request/response samples;
- console and server errors;
- screenshots or screen recordings;
- network traces;
- test output;
- accessibility tree observations and automated violations;
- reproduction scripts or minimal test cases;
- timing/order evidence for concurrency bugs;
- before/after behavior for remediated findings.

Maintain an evidence index so report claims can be traced to artefacts.

---

## 5. Discovery passes

Load and execute the relevant specialist references:

- Security and privacy → `references/security.md`
- Concurrency and state integrity → `references/concurrency.md`
- Reliability and performance → `references/reliability.md`
- Accessibility → `references/accessibility.md`
- Visual, interaction, responsive, and content consistency → `references/ui-consistency.md`
- Runtime/browser verification → `references/runtime-testing.md`

Trace critical flows end-to-end across client, network, server, data layer, async jobs, and external integrations.

### Deep Audit orchestration

Run Deep Audit as six explicit stages:

**A. Reconnaissance:** one mapping pass creates the System Map and Risk Model.

**B. Independent specialist discovery:** specialists inspect relevant surfaces independently. Give each the System Map, Risk Model, declared scope, and source access. Do not give specialists one another's conclusions.

**C. Finding normalization:** deduplicate exact duplicates while preserving distinct causes, exploit paths, and impacts. Do not merge different failure modes because they touch the same file.

**D. Adversarial verification:** fresh verifier attempts to falsify each Critical/High claim, then reproduce it. Record `REPRODUCED`, `NOT REPRODUCED`, or `BLOCKED` with reason.

**E. Runtime verification:** execute the runtime matrix against critical flows and discovery hypotheses. Static analysis proposes; runtime testing confirms or refutes.

**F. Synthesis:** only evidence-backed findings enter confirmed findings. Remaining concerns go to `Needs Verification` with next action.

If multi-agent execution is unavailable, simulate independence with sequential fresh passes: clear conclusions from the working context where possible, re-read source, and explicitly adopt a falsification role during verification. State this limitation.

---

## 6. Runtime and browser testing

Runtime testing is a first-class phase, not an optional afterthought, for Release Audit and Deep Audit when an executable environment exists.

Use `references/runtime-testing.md`.

Prioritize critical flows and hypotheses from static discovery. Test real transitions and failure modes, including network degradation, session expiry, permission changes, retries, duplicate actions, navigation interruption, malformed content, viewport stress, keyboard-only use, and multi-tab behavior.

Do not claim runtime verification if only source code was inspected.

If the application cannot run, report exactly why and mark affected checks `NOT TESTED` or `PARTIAL`.

---

## 7. Reporting

Deliver the complete audit report before proposing code changes.

```markdown
# Audit Report — [application / feature]

**Mode:** Fast Check | Release Audit | Deep Audit
**Audit date:** [date]
**Release target / commit / branch:** [if known]

## Executive summary
[Risk posture, strongest evidence, major unknowns, and release recommendation in concise prose.]

## System Map / Change Impact Map
[Concise map from reconnaissance.]

## Risk Model
[Critical flows/assets and why they matter.]

## Declared scope
- In scope:
- Explicitly out of scope:
- Runtime environment tested:
- Verification constraints:

## Scope adherence
| Domain | Status | Evidence summary | Gaps |
|---|---|---|---|

## Confirmed findings
[Critical → Informational, then category.]

## Needs Verification
[Hypotheses, missing evidence, and exact next verification step.]

## Evidence index
[Artefact ID → type → location → redaction note.]

## Prioritised remediation plan
[Order by realistic risk: impact × exploitability × reachability × likelihood, with business context.]

## Quick wins
[Low-regression-risk fixes.]

## Structural changes / deeper investigation
[Architecture-level work and unresolved risks.]

## Suggested regression coverage
[Tests and controls that would prevent recurrence.]

## Release recommendation
[Safe to ship | Ship with known risks | Do not ship]
[Justification tied to findings, verification status, and untested critical scope.]

## Assurance statement
This audit reduces risk within the declared and tested scope. It does not prove the application secure, compliant, accessible in all contexts, or defect-free, and does not replace appropriate human review, penetration testing, compliance assessment, or real-world staging where those are warranted.
```

### Finding template

```markdown
### [ID] [Severity] · [Category] · [Title]
- **Location:** exact file/function/endpoint/flow and line range where available
- **Affected flow/assets:**
- **Preconditions:** attacker/user/system state required
- **Issue:**
- **Realistic impact:**
- **Reachability/exploitability:**
- **Evidence:** artefact IDs and concise explanation
- **Reproduction:** sanitized, safe steps
- **Recommended fix:** smallest safe remediation first; structural option if needed
- **Regression test:** test that would fail before and pass after
- **Confidence:** Confirmed | High Confidence | Needs Verification
- **Verification status:** Reproduced | Not Reproduced | Blocked | Not Required
```

### Severity calibration

Severity is contextual, never assigned from a code smell alone.

- **Critical:** realistic path to catastrophic impact such as broad sensitive-data exposure, unauthorized high-impact money movement, full tenant isolation failure at scale, remote system compromise, or irreversible systemic corruption.
- **High:** serious compromise or loss affecting meaningful users/data/operations with realistic reachability.
- **Medium:** material issue requiring specific conditions, limited scope, or meaningful but recoverable impact.
- **Low:** narrow impact, difficult preconditions, defense-in-depth gap, or localized UX/accessibility defect.
- **Informational:** useful observation without demonstrated material impact.

Consider impact, reachability, attacker prerequisites, blast radius, sensitivity, compensating controls, detectability, and recoverability.

---

## 8. Remediation protocol

Only remediate after the report is delivered and the user authorizes changes, except explicit emergency containment.

### Phase 0 — Immediate blockers
Contain confirmed release-blocking risk: broken authorization, verified sensitive-data exposure, duplicate high-impact side effects, destructive corruption, critical accessibility blockers in essential flows, or equivalent context-specific failures.

### Phase 1 — Safe quick wins
Small, isolated fixes with low regression risk: validation, pending-state guards, error handling, missing labels, focus restoration, token misuse, obvious state gaps.

### Phase 2 — Structural fixes
Authorization model, tenant isolation, idempotency architecture, transaction boundaries, cache/state model, shared validation, component architecture, policy redesign, observability.

### Phase 3 — Regression prevention
Unit, integration, E2E, permission-matrix, concurrency, accessibility, visual-regression, security regression tests; deterministic CI checks; monitoring and alerting; documentation.

For each fix record:

- what changed;
- why;
- files/surfaces modified;
- tests added/updated;
- checks run;
- residual risk.

Prefer the smallest change that safely resolves the verified cause. Avoid opportunistic rewrites during blocker remediation.

---

## 9. Re-audit and closure

After remediation:

1. Re-run the original reproduction or failing test.
2. Re-run the affected specialist pass.
3. Test adjacent flows touched by the fix.
4. Confirm no authorization, state, accessibility, or visual regression was introduced.
5. Update finding status: `FIXED`, `MITIGATED`, `ACCEPTED RISK`, or `OPEN`.
6. Recalculate release recommendation.

A code change alone does not close a finding. Verification closes it.

---

## 10. CI/CD add-on

Only load `references/cicd.md` when the user asks for automated checks, pipeline integration, pre-deploy gates, or continuous audit.

Keep three layers distinct:

1. **Deterministic controls:** lint, type checks, tests, dependency review, secret scanning, SAST, policy checks, accessibility automation where applicable.
2. **Agent semantic review:** diff-scoped Fast Check when a supported headless agent runner exists.
3. **Human-triggered release assurance:** Release Audit or Deep Audit before significant releases.

Never imply that CI scanners or an agent prompt prove security.

---

## Operating principles

- Explore before judging.
- Model risk before assigning severity.
- Trace flows, not files.
- Treat client-side controls as UX, not security boundaries.
- Prefer falsification over confirmation.
- Separate discovery from verification.
- Separate hypotheses from findings.
- Preserve evidence and redact secrets.
- Runtime behavior outranks speculation.
- A short report of reproduced issues is better than a long report of maybes.
- Untested scope must remain visible.
- The audit is complete only when the release decision reflects both findings and verification gaps.
