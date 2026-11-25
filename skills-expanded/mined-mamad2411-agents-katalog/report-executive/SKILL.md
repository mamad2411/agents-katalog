---
name: report-executive
description: Executive and management risk summary from validated findings — synthesizes confirmed and likely findings into a non-technical risk overview suitable for C-suite, board members, and decision-makers. Focuses on business impact, regulatory exposure, resource requirements, and strategic remediation priorities. Drafts only from existing redacted findings and evidence; never includes raw proof, secrets, or exploit detail.
disable-model-invocation: true
risk: report-only
allowed-modes: [auto, bug-bounty, red-team, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: no
evidence-outputs: [report, finding-summary, redaction-notes, risk-matrix, executive-brief]
---

# Executive report — management risk summary from redacted findings

Use this skill to draft an executive summary report from validated, redacted findings and evidence. The audience is non-technical leadership: C-suite, board members, risk officers, and compliance leads. The report must communicate business risk, not technical exploitation detail. Every statement must be traceable to a verified finding in the local finding store. This skill never creates findings, never includes raw proof content, and never guesses impact.

## Required inputs

- Findings list from `pentest_agent_list_findings` filtered to `confirmed` and `likely` confidence.
- Evidence records referenced by each finding.
- Scope file confirming assessment boundaries.
- Engagement metadata: assessment type, dates, tester/team identifier, target organization.
- Any regulatory framework relevant to the assessment (GDPR, PCI DSS, HIPAA, SOX, ISO 27001, NIST CSF).

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` to verify redaction and reporting policy.
2. `pentest_agent_list_findings` to load the complete finding inventory with confidence and severity.
3. `pentest_agent_list_evidence` to load evidence records for each finding.
4. `pentest_agent_redact_evidence` for a final redaction pass on any evidence to be summarized.
5. `pentest_agent_render_report` with template `executive` to produce the final document.
6. No authorization cache required — this is report drafting from existing data.

## Workflow

### Phase 1 — finding aggregation and risk normalization

Convert technical findings into business-risk categories leadership understands.

1. **Severity-to-risk mapping**:
   | Technical Severity | Executive Risk Label | Business Impact Description |
   |---|---|---|
   | Critical (9.0-10.0) | Severe | Immediate threat to business continuity, regulatory action likely, material financial loss |
   | High (7.0-8.9) | Significant | Major control gap, probable data exposure, likely audit finding |
   | Medium (4.0-6.9) | Moderate | Control weakness requiring remediation, limited exposure |
   | Low (0.1-3.9) | Minor | Housekeeping finding, best-practice gap |
   | Informational | Observation | Not a risk, noted for awareness |
2. **Business-impact categories**: assign each finding to one or more:
   - **Financial**: direct monetary loss, fraud, ransom, regulatory fines, contract penalties.
   - **Data privacy**: PII/PHI exposure, GDPR/CCPA/HIPAA violation, customer trust erosion.
   - **Operational**: service disruption, downtime, degraded availability, supply-chain impact.
   - **Reputational**: brand damage, media exposure, customer churn, partner confidence.
   - **Compliance**: audit finding, certification risk, regulatory reporting obligation.
   - **Strategic**: competitive disadvantage, IP theft, M&A impact, market timing.
3. **Finding consolidation**: merge findings with a shared root cause into a single risk item. Example: three findings for missing authorization on `/api/users`, `/api/orders`, `/api/payments` → one risk item: "Inconsistent API authorization controls across customer-facing endpoints."
4. **Risk appetite alignment**: if the organization has a stated risk appetite (from policy or scope), classify each risk item as within or exceeding appetite.

### Phase 2 — executive summary construction

Build the one-page summary that busy executives will read first.

1. **Opening paragraph** (3-4 sentences): what was assessed, when, by whom, and the overall risk posture.
   - Example: "An authorized security assessment of [TARGET] web applications and supporting infrastructure was conducted between [DATES]. The assessment identified [N] confirmed findings, of which [X] are rated Severe and [Y] are rated Significant. The most urgent risk is [top finding], which could allow [worst-case impact] if not addressed."
2. **Risk posture statement**: one of:
   - **Critical risk posture**: one or more Severe findings with immediate remediation required. Active exploitation possible or likely.
   - **Elevated risk posture**: Significant findings present. No confirmed active exploitation but multiple control gaps. Remediation within 30 days recommended.
   - **Managed risk posture**: Moderate findings only. Controls generally effective with targeted improvements needed.
   - **Low risk posture**: Minor or informational findings only. Controls operating as designed.
3. **Top 3-5 risks in priority order**: one sentence per risk with business impact, not technical detail. Example: "Risk #1: Unauthorized access to customer payment data — a remote attacker could view, modify, or delete payment records for all customers, creating regulatory liability under PCI DSS and potential financial loss."
4. **Remediation summary**: total effort estimate (person-weeks), critical path (which fixes unlock others), estimated timeline to reduce posture to Managed or Low.
5. **Statement of limitations**: what was excluded from scope and why this report should not be treated as exhaustive.

### Phase 3 — risk matrix and priority dashboard

Provide a visual (or table-based) risk overview that leadership can scan in 30 seconds.

1. **Risk heat map** (as a markdown table):
   | Risk ID | Finding | Severity | Likelihood | Business Impact | Remediation Effort | Priority |
   |---|---|---|---|---|---|---|
   | R-001 | [Title] | Critical | High | Financial, Data Privacy | 2 weeks | 1 — Immediate |
   | R-002 | [Title] | High | Medium | Operational | 1 week | 2 — This sprint |
2. **Priority definitions**:
   - **Priority 1 — Immediate** (0-7 days): active exploitation possible, regulatory notification may be required, stop-other-work urgency.
   - **Priority 2 — This sprint** (1-4 weeks): significant control gap, likely to be exploited if left unaddressed.
   - **Priority 3 — This quarter** (1-3 months): moderate weakness, defense-in-depth improvement.
   - **Priority 4 — Backlog**: minor or housekeeping items.
3. **Resource estimate per priority band**: total person-weeks and any specialized skills or external support needed.
4. **Dependency map**: which fixes must precede others (e.g., "Patch the WAF before exposing the internal API to re-architecting").

### Phase 4 — regulatory and compliance impact

Connect findings to regulatory obligations the organization faces.

1. **Regulatory mapping** per finding:
   | Finding | GDPR Articles | PCI DSS Requirements | HIPAA Safeguards | ISO 27001 Controls |
   |---|---|---|---|---|
   | PII exposure via IDOR | Art. 5(1)(f), 32 | N/A | 164.312(a)(1), (c)(1) | A.9.4.1, A.18.1.3 |
   | Missing encryption at rest | Art. 32(1)(a) | Req. 3.4 | 164.312(a)(2)(iv) | A.10.1.1 |
2. **Breach-notification triggers**: which findings, if they had been discovered through an actual breach, would trigger mandatory notification under GDPR (72 hours), state data-breach laws, SEC materiality rules, or sector-specific regulations.
3. **Audit readiness impact**: what an external auditor would flag as a finding, and what evidence the organization has (or lacks) that controls are effective.
4. **Compliance timeline**: if a certification audit is imminent (within 6 months), which findings must be closed before the audit window.

### Phase 5 — strategic recommendations

Go beyond "fix the bug" to "improve the program."

1. **Immediate fixes** (0-30 days): the minimum set of changes to reduce Severe/Significant risks to Moderate or below.
2. **Program improvements** (1-6 months): changes to SDLC, security testing cadence, tooling investment, training.
3. **Metrics and KPIs**: suggest 2-3 measurable indicators leadership can track post-remediation:
   - Mean time to remediate critical findings (target: < 7 days).
   - Percentage of services with security headers deployed (target: > 90%).
   - Number of findings per assessment (trend downward over time).
4. **Investment recommendation**: what capability or tooling gap contributed to the findings, and what investment would prevent recurrence (e.g., "Deploy a WAF to protect against injection attacks while the engineering team addresses root causes in code").
5. **Re-assessment recommendation**: when to retest and what scope should be expanded.

## Decision points

- **Finding has no confirmed exploit but theoretical impact is severe**: rate as Significant, not Severe. Clearly label as "theoretical — exploitation not demonstrated during assessment."
- **Multiple findings share the same root cause**: consolidate into one risk item. Report the worst-case impact across all affected systems.
- **Organization has an accepted risk for a finding**: note as "Risk accepted by [role] on [date]. Included for awareness; no remediation expected." Do not inflate severity.
- **Regulatory impact is uncertain** (depends on legal interpretation): flag for legal review. Do not assert regulatory violation without clear evidence.
- **Finding severity is disputed internally**: present both the assessor's rating and the rationale for any difference. Let leadership decide.

## Prohibited behavior

- Including raw proof file content, raw secrets, passwords, API keys, or tokens.
- Including PII, PHI, or customer data from evidence excerpts.
- Inflating severity to create urgency — this destroys credibility.
- Speculating about impact beyond what evidence supports.
- Assigning dollar values to risk without organizational data on cost of breach.
- Naming individual developers, administrators, or staff members.
- Including exploit code, payloads, or reproduction steps beyond high-level description.
- Recommending specific vendor products without appropriate procurement context.
- Claiming the assessment was exhaustive or that no other vulnerabilities exist.

## Stop conditions

- Less than 3 findings with `confirmed` confidence exist → do not produce an executive report from thin data. Document that the assessment scope or methodology may need expansion.
- Key business-impact data is unavailable (e.g., data classification, system criticality ratings) → mark assumptions clearly and flag as "Requires business stakeholder review."
- Regulatory obligations of the organization are unknown → do not assert compliance status. Note "Regulatory impact analysis deferred pending legal review."

## Evidence template

```text
Executive risk summary for: [TARGET ORGANIZATION]
Assessment period: [START_DATE] to [END_DATE]
Assessment type: [black-box web app / internal network / mobile app / etc.]

Risk posture: [CRITICAL / ELEVATED / MANAGED / LOW]

Finding inventory:
  Severe (Critical): [N]
  Significant (High): [N]
  Moderate (Medium): [N]
  Minor (Low): [N]
  Observations (Info): [N]

Top risks:
  R-001 | [Severity] | [Title] | Business impact: [IMPORTANT sentence]
  R-002 | [Severity] | [Title] | Business impact: [IMPORTANT sentence]
  R-003 | [Severity] | [Title] | Business impact: [IMPORTANT sentence]

Regulatory exposure:
  - GDPR: [N] findings may impact personal data. Notification triggers: [list if applicable].
  - PCI DSS: [N] findings in CDE scope. Compliance status: [compliant / at risk / not assessed].
  - Other: [HIPAA / SOX / ISO 27001] — [summary].

Remediation roadmap:
  Priority 1 (0-7 days): [N] items, [X] person-weeks
  Priority 2 (1-4 weeks): [N] items, [X] person-weeks
  Priority 3 (1-3 months): [N] items, [X] person-weeks
  Priority 4 (backlog): [N] items

Limitations:
  - Scope excluded: [internal network / mobile apps / third-party integrations / etc.]
  - Assessment is a point-in-time evaluation. New vulnerabilities may have been introduced after testing.
  - This report summarizes technical findings at an executive level. Detailed technical appendices are available separately.

Redaction notes:
  - All raw proof file content excluded.
  - No secrets, tokens, passwords, or API keys included.
  - PII references from evidence replaced with category labels (e.g., "customer PII", "employee credentials").
  - Exploit reproduction details omitted; available in technical report on request.
```

## Handoff

1. Store executive report under `.pi/pentest-agent/engagements/<id>/reports/executive/`.
2. `pentest_agent_export_report` for a standalone PDF/Markdown copy.
3. If requested, generate a one-page slide-deck summary (Markdown with `---` slide separators).
4. Explicitly note: this report contains no raw proof content, no secrets, and no PII. All risk statements are traceable to `pentest_agent_list_findings` records with evidence IDs.
