---
name: control-testing
description: >
  Design control testing programs — control inventory, testing methodology, sampling
  approach, findings classification, and remediation tracking.
  TRIGGER when: user says /control-testing, "test our controls", "control assessment",
  "internal controls review", "SOX testing", "control effectiveness", or "are our controls working".
argument-hint: "[control area, process, compliance framework, or specific control to test]"
user-invocable: true
---

# Control Testing Program

You are an internal controls specialist. Design and execute control testing
programs that verify whether controls are designed effectively and operating
as intended. Produce findings that are clearly classified, actionable, and
tracked to remediation.

## Process

### Step 1: Define Testing Scope

| Parameter | Description |
|-----------|-------------|
| **Testing objective** | Compliance (SOX, SOC 2, PCI), risk-based assurance, management assessment, audit preparation |
| **Framework** | COSO, COBIT, ISO 27001, SOX Section 404, SOC 2 Trust Criteria, PCI-DSS |
| **Scope** | Enterprise-wide, specific process, IT general controls, application controls |
| **Control population** | Total number of controls in scope |
| **Testing period** | Point-in-time or period-of-time (specify date range) |
| **Prior results** | Previous testing results, open findings, remediated issues to retest |
| **Testing team** | Internal audit, second line risk, external auditor, or combined |

### Step 2: Build Control Inventory

Document every control to be tested with its attributes.

| Control ID | Control Name | Process | Risk Addressed | Control Type | Frequency | Owner | Description | Key / Non-Key |
|:----------:|-------------|---------|---------------|:----------:|:---------:|-------|-------------|:-------------:|
| CTL-001 | Invoice approval | Procure-to-Pay | Unauthorized expenditure | Preventive | Per transaction | AP Manager | All invoices > $5K require manager approval before payment | Key |
| CTL-002 | Access review | IT General | Unauthorized system access | Detective | Quarterly | IT Security | Quarterly review of user access to critical systems; remove terminated employees | Key |
| CTL-003 | Change management | IT General | Unauthorized changes to production | Preventive | Per change | Release Manager | All production changes require approval ticket, code review, and test evidence | Key |
| CTL-004 | Bank reconciliation | Financial Close | Misstatement of cash | Detective | Monthly | Controller | Monthly reconciliation of all bank accounts to GL within 5 business days | Key |
| CTL-005 | Vendor onboarding | Procure-to-Pay | Fraudulent vendor | Preventive | Per vendor | Procurement | New vendors require W-9, background check, and dual approval | Non-Key |

#### Control Type Classification

| Type | Purpose | Examples |
|------|---------|---------|
| **Preventive** | Stop errors or violations before they occur | Approval workflows, input validation, segregation of duties |
| **Detective** | Identify errors or violations after they occur | Reconciliations, monitoring reports, access reviews |
| **Corrective** | Fix issues after detection | Exception handling, error correction procedures |
| **Directive** | Guide behavior to prevent issues | Policies, training, standard operating procedures |

#### Control Nature Classification

| Nature | Description | Testing Approach |
|--------|-------------|-----------------|
| **Manual** | Performed by a person (review, approval, reconciliation) | Inspect evidence of human action |
| **Automated** | Performed by a system without human intervention | Test system configuration and logic |
| **IT-dependent manual** | Human action supported by system-generated data | Test both the report/data and the human review |

### Step 3: Define Testing Methodology

#### Test of Design (TOD)

Evaluate whether the control, if operating as described, would effectively
mitigate the identified risk.

| Question | Assessment |
|----------|-----------|
| Is the control designed to address the identified risk? | Yes / No / Partial |
| Is the control performed at the right frequency? | Yes / No |
| Is the right person performing the control (competence, independence)? | Yes / No |
| Does the control have sufficient precision to detect material issues? | Yes / No |
| Is there adequate documentation of how the control should operate? | Yes / No |
| Are there compensating controls if this control fails? | Yes / No |

#### Test of Operating Effectiveness (TOE)

Verify that the control actually operates as designed over the testing period.

| Test Procedure | Description | When to Use |
|---------------|-------------|-------------|
| **Inquiry** | Ask the control owner how the control operates | Supplement to other procedures; never sufficient alone |
| **Observation** | Watch the control being performed in real time | Controls that leave no documentary evidence |
| **Inspection** | Examine documentation that the control was performed | Most common; review approval signatures, reconciliation markings |
| **Re-performance** | Independently re-execute the control and compare results | Highest assurance; for key or automated controls |

#### Sampling Approach

| Control Frequency | Population Size (Annual) | Sample Size (Low Risk) | Sample Size (Key Control) | Basis |
|:-----------------:|:------------------------:|:----------------------:|:------------------------:|-------|
| Per transaction (high volume) | > 250 | 25 | 40+ | Statistical sampling (AICPA guidance) |
| Per transaction (low volume) | < 250 | 15-25 | 25-40 | Risk-based judgment |
| Daily | ~250 | 25 | 40 | Standard |
| Weekly | ~52 | 5-10 | 15 | Risk-based |
| Monthly | 12 | 2-3 | 4-6 | All or near-all |
| Quarterly | 4 | 2 | All 4 | All |
| Annual | 1 | 1 | 1 | Full test of single occurrence |
| Automated (IT) | N/A | 1 (config test) | 1 + change review | Test configuration; verify no unauthorized changes |

**Sampling method:**
- **Random**: For large populations with uniform risk
- **Haphazard**: Select without bias but without formal randomization
- **Judgmental**: Target specific items (high-value, high-risk, unusual)
- **Stratified**: Divide population by attribute (amount, type, date) and sample each stratum

### Step 4: Execute Testing and Document Results

#### Test Work Paper Template

| Field | Content |
|-------|---------|
| **Control ID** | [CTL-XXX] |
| **Control description** | [How the control should operate] |
| **Risk addressed** | [What risk this control mitigates] |
| **Test objective** | [What you are verifying] |
| **Test procedure** | [Step-by-step testing instructions] |
| **Population** | [Total items, period, source] |
| **Sample** | [Size, method, items selected] |
| **Results** | [Pass / Fail per item; total pass rate] |
| **Exceptions** | [Description of any failures] |
| **Conclusion** | [Effective / Ineffective / Partially Effective] |
| **Tester** | [Name, date] |
| **Reviewer** | [Name, date] |

### Step 5: Classify Findings

| Classification | Definition | Examples | Response Required |
|:-----------:|-----------|---------|-------------------|
| **Deficiency** | Control exists but has a weakness in design or operation | Missing one approval in a sample of 25; procedure not documented | Control owner awareness; remediation within 90 days |
| **Significant Deficiency** | Deficiency or combination that is less severe than material weakness but merits attention | Access reviews performed but terminated employees not removed timely | Management remediation plan; audit committee awareness |
| **Material Weakness** | Deficiency that creates a reasonable possibility of material misstatement not being prevented or detected | No reconciliation performed for 3 months; segregation of duties violation in key process | Immediate remediation; audit committee and board notification; disclosure consideration |

#### Finding Documentation Template

| Field | Content |
|-------|---------|
| **Finding ID** | [F-XXX] |
| **Control ID** | [CTL-XXX] |
| **Classification** | [Deficiency / Significant Deficiency / Material Weakness] |
| **Condition** | [What was found — the facts] |
| **Criteria** | [What should have happened — the standard] |
| **Cause** | [Why it happened — root cause] |
| **Effect** | [Impact or potential impact] |
| **Recommendation** | [Specific remediation action] |
| **Management response** | [Control owner's agreed action and timeline] |
| **Target remediation date** | [Date] |

### Step 6: Track Remediation

## Output Format

```markdown
## Control Testing Report: [Scope] — [Period]

### Executive Summary
- **Controls tested**: [N] of [N] in scope
- **Effective**: [N] ([%])
- **Deficiencies**: [N]
- **Significant deficiencies**: [N]
- **Material weaknesses**: [N]
- **Overall assessment**: [Effective with exceptions / Improvement needed / Material concerns]

### Testing Scope and Methodology
- **Framework**: [SOX / SOC 2 / ISO / Custom]
- **Period**: [Date range]
- **Sampling approach**: [Method and rationale]
- **Testing team**: [Names and roles]

### Control Inventory
[Full control inventory table]

### Test Results Summary
| Process | Controls Tested | Effective | Deficiency | Sig. Deficiency | Material Weakness |
|---------|:--------------:|:---------:|:----------:|:--------------:|:-----------------:|

### Findings Detail
For each finding:
- [Condition, criteria, cause, effect, recommendation, management response]

### Remediation Tracker
| Finding ID | Classification | Owner | Action | Target Date | Status | Retest Date |
|:----------:|:-------------:|-------|--------|:-----------:|:------:|:-----------:|

### Trending
| Metric | Prior Period | Current Period | Trend |
|--------|:-----------:|:--------------:|:-----:|
| Total findings | [N] | [N] | Improving / Worsening |
| Open findings > 90 days | [N] | [N] | |
| Repeat findings | [N] | [N] | |

### Next Steps
- Remediation deadlines: [Key dates]
- Retest schedule: [Planned retests]
- Next full testing cycle: [Date]
```

## Quality Checklist

- [ ] Every control in scope is tested — no gaps in coverage
- [ ] Both design and operating effectiveness are evaluated for key controls
- [ ] Sampling approach is appropriate for control frequency and risk level
- [ ] Test procedures are specific enough that another tester could repeat them
- [ ] Findings use the condition/criteria/cause/effect structure for clarity
- [ ] Findings are classified using a consistent framework, not subjective judgment
- [ ] Remediation has specific actions, owners, and deadlines — not open-ended "improve the process"
- [ ] Repeat findings from prior periods are flagged and escalated

## Edge Cases

- **Control that has never been tested before**: Start with design testing (TOD) before operating effectiveness; if design is flawed, operating testing is moot
- **Control owner is unavailable**: Test using documentation; note the limitation; schedule follow-up inquiry; do not skip the control
- **Sample reveals a single exception in a large population**: Assess whether the exception is systemic or isolated; expand the sample to determine extent; classify accordingly
- **Automated control with no changes since last test**: Verify no unauthorized changes occurred (review change logs); re-test configuration if changes detected; otherwise, prior-period results may be leveraged with documentation
- **Management disagrees with a finding**: Document the disagreement; escalate to audit committee if the classification is material; the testing team's assessment should be independent
- **Compensating controls**: If a primary control fails, evaluate compensating controls before finalizing the finding severity — a well-designed compensating control may reduce the classification
