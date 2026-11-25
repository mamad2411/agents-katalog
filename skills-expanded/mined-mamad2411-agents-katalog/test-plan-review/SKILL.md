---
name: test-plan-review
description: Review a test plan against scope, risk, technique selection, environments, data, automation, exit criteria, and observability. Use as a peer-review or gate before plan approval.
source: self
date_added: 2026-05-01
---

# Test Plan Review

A peer review that pressure-tests a plan before it consumes weeks of effort. Catches scope gaps, weak techniques, missing exit criteria, and unrealistic environments early.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Standards | ISO/IEC/IEEE 29119-3 (test docs), ISTQB CTFL 4.0, IEEE 1028 (reviews) |
| Format | Async PR review of plan markdown + 30 min sync walkthrough |
| Output | Approved / Approved-with-changes / Rework |
| Roles | Author, reviewers (peer + tech lead + PM + SRE/Sec for cross-cutting) |
| Tracking | Comments resolved before merge; outstanding risks logged |

## When to Use

- New feature test plan before execution begins.
- Major release master plan.
- Migration / re-architecture plan.
- Compliance / regulatory plan (SOC 2, ISO, regulated industry).

## Review Checklist

### 1. Scope & alignment
- [ ] In-scope and out-of-scope explicit (lists, not vague areas)
- [ ] Linked to requirements / user stories / risks
- [ ] Stakeholder list complete; owners assigned

### 2. Risk
- [ ] Risk register present (technical, business, regulatory)
- [ ] Risks ranked by likelihood × impact
- [ ] Test depth is risk-proportional (high-risk → more techniques + more layers)

### 3. Technique selection
- [ ] EP / BVA applied where input ranges exist
- [ ] Decision tables for branchy logic
- [ ] State transition where state matters
- [ ] Exploratory charters for unknowns
- [ ] Property-based / fuzz where invariants exist
- [ ] Negative paths (auth, validation, errors) explicit

### 4. Test layers
- [ ] Pyramid balance documented (unit / component / contract / integration / E2E)
- [ ] No layer doing another's job (e.g., E2E re-validating unit logic)
- [ ] Test matrix per layer × area is complete

### 5. Non-functional
- [ ] Performance: SLOs, load/stress/spike/soak as needed
- [ ] Security: SAST/DAST/SCA, threat model, abuse cases
- [ ] Accessibility: WCAG 2.2 AA scope, AT matrix
- [ ] Reliability: chaos / failure injection
- [ ] Observability: traces, logs, metrics for failed tests

### 6. Environments & data
- [ ] Right environment for each layer (local/PR/staging/perf/canary)
- [ ] Test data realistic, masked, refreshed
- [ ] No PII; secrets sourced from manager
- [ ] Per-test data ownership (no shared mutable state)

### 7. Automation
- [ ] Tools chosen with rationale
- [ ] Selectors / data hooks defined
- [ ] CI integration explicit (PR / nightly / release gates)
- [ ] Reporting (HTML / Allure / dashboards)
- [ ] Maintenance & flake budget addressed

### 8. Exit criteria
- [ ] Coverage targets concrete (e.g., 100% endpoints; 0 critical a11y)
- [ ] Defect thresholds (e.g., 0 S1, ≤ 2 S2 with mitigation)
- [ ] Performance / a11y / security thresholds explicit

### 9. Operability
- [ ] Defect lifecycle owned (triage cadence, SLA per severity)
- [ ] Communication plan (slack channel, daily standup, exec status)
- [ ] Schedule + dependencies (other teams, vendors)
- [ ] Risks of the *plan itself* (single tester, environment instability)

### 10. Compliance & evidence
- [ ] Required evidence enumerated (test runs, sign-offs, ACR/VPAT)
- [ ] Traceability matrix maintainable
- [ ] Retention policy noted

## Reviewer Stance

- **Be specific.** "Add BVA for the discount tiers in §4.2" beats "test more edges".
- **Reference standards.** Cite ISTQB, ISO, WCAG, OWASP for asks.
- **Trade-offs explicit.** "Skipping AAA contrast is acceptable if X documented".
- **Prefer fewer, sharper questions** to a wall of comments.
- **Distinguish blocker vs. nit** with a label.

## Output Format

```
Test Plan Review — orders-api v3.14 — Reviewer: @qa-lead
Decision: APPROVED with changes (5 must-fix, 4 nits)

Must-fix:
  1. §3.2 — Decision table missing default rule for unknown region
  2. §4.4 — Perf plan has no soak; this release adds 24h cron — add soak
  3. §5.1 — Test data references prod snapshot; require masked source
  4. §6 Exit criteria — "no major bugs" — replace with severity thresholds
  5. §7 — No flake budget; add 1% target + quarantine policy

Nits:
  - §1 scope: clarify "out of scope" for 3rd-party tax service
  - Add traceability matrix template
  - Mention AT smoke for VoiceOver iOS
  - Reference ISO 29119-3 in references

Risks of the plan:
  - Single QA author for two services — request peer co-author
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Style edits dominating the review | Focus on risk, scope, exit criteria first |
| "Looks fine" approvals | Use the checklist; require specific yeses |
| Reviewers from one discipline | Include eng, PM, SRE, sec, a11y as relevant |
| Plan reviewed after execution started | Block execution until plan is approved |
| No re-review when scope grows | Trigger re-review on scope delta > 20% |
| Ignoring plan-itself risks | Plan capacity, env stability, vendor risk |

## References

- ISO/IEC/IEEE 29119-3 — Test documentation
- IEEE 1028 — Software Reviews and Audits
- ISTQB CTFL Syllabus 4.0 — Test planning & monitoring
- *Lessons Learned in Software Testing* — Kaner et al.
- Google's *Software Engineering at Google* — code review principles (transferable)
