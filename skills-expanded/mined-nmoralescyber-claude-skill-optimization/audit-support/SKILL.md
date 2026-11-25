---
name: audit-support
description: Supports SOX 404 internal control over financial reporting (ICFR) testing — sample selection sizing by frequency AND risk, defensible selection methods (random/systematic/judgmental/haphazard), audit-ready workpapers (self-contained, cross-referenced, IPE-tested), and control deficiency classification (CD / SD / MW) using likelihood-by-magnitude evaluation. Make sure to use this skill whenever the user says SOX testing, SOX 404, ICFR, prepare for our SOX audit, pull a sample for control [name], how big should my sample be for [frequency] control, build an audit workpaper, evaluate IPE / Information Produced by the Entity, classify this control deficiency, is this a material weakness, prep for external auditors, or describes any internal financial control testing activity. Do NOT use for: ongoing SOC 2 / ISO 27001 / GDPR / HIPAA program tracking (use operations:compliance-tracking — different scope, security/privacy not financial), customer-facing website legal page audits (use legal:legal-audit), pre-launch regulatory go/no-go on a new initiative (use legal:compliance-check), GL/bank/intercompany reconciliations (use finance:reconciliation), variance analysis (use finance:variance-analysis), or contract review (use legal:review-contract). Defining characteristic: SOX 404 ICFR testing — workpapers, samples, deficiency classification.
---

# Audit Support (SOX 404 / ICFR)

SOX 404 internal control over financial reporting (ICFR) testing methodology, sample selection, audit-ready workpapers, and deficiency classification (CD / SD / MW).

**Important:** This skill assists with workflows. All sample selections, workpapers, and deficiency conclusions should be reviewed by qualified financial professionals (internal audit, controller, external auditor) before reliance. "Significance" and "materiality" are ultimately auditor judgments.

## When to use vs. adjacent audit/compliance skills

| Skill | What it does |
|---|---|
| **finance:audit-support (this one)** | SOX 404 ICFR testing — workpapers, samples, deficiency classification (financial controls) |
| `operations:compliance-tracking` | Ongoing program operations for SOC 2, ISO 27001, GDPR, HIPAA, PCI (security/privacy, not ICFR) |
| `legal:legal-audit` | Customer-facing website legal page audit (ToS, privacy, etc.) |
| `legal:compliance-check` | Pre-launch regulatory go/no-go on a proposed initiative |
| `finance:reconciliation` | GL/bank/intercompany reconciliations specifically |
| `finance:variance-analysis` | Budget vs. actual / period-over-period variance commentary |
| `legal:review-contract` | Contract review against playbook |

This skill is exclusively about **SOX 404 testing of internal controls over financial reporting (ICFR)**. It is the operational counterpart to `operations:compliance-tracking` (which tracks security/privacy programs).

## SOX 404 testing flow (the steps this skill drives)

1. **Scoping** — confirm control is in scope (significant account × relevant assertion × key control)
2. **Design effectiveness** — walkthrough; confirm control is properly designed
3. **Operating effectiveness** — pull sample, test, document
4. **IPE testing** — if control relies on a system report, separately test report's completeness & accuracy
5. **Conclude** — pass / exception
6. **If exception → classify** — CD / SD / MW per likelihood × magnitude

## 1. Sample selection

### Sample size — by frequency AND risk

Sample size is a function of (a) control frequency (which determines population size) and (b) inherent risk of the control. Use this matrix:

| Control frequency | Pop. size | Low risk | Moderate risk | High risk |
|---|---|---|---|---|
| Annual | 1 | 1 | 1 | 1 |
| Quarterly | 4 | 2 | 2 | 3 |
| Monthly | 12 | 2 | 3 | 4–5 |
| Weekly | ~52 | 5 | 8 | 15 |
| Daily | ~250 | 20 | 30 | 40 |
| Per-transaction (small pop. <250) | <250 | 20 | 30 | 40 |
| Per-transaction (large pop. 250+) | 250+ | 25 | 40 | 60 |
| Multiple times per day / system-enforced automated | n/a | 1 (+ ITGC) | 1 (+ ITGC) | 1 (+ ITGC) |

**Risk uplift factors** (push toward the next risk tier — choose higher sample size):
- Sole control addressing a significant assertion (no redundancy)
- Prior-period deficiency on this control
- New control (no prior testing history)
- External auditor will rely on management's testing
- Process or system changed during the period
- Significant management estimate / judgment involved
- High-fraud-risk account (cash, revenue, related party)

**Roll-forward considerations:** if testing at interim (e.g., Q3 cutoff), add a roll-forward sample for Q4 — typically 3–5 items spread across the remaining period — to extend the conclusion through year-end.

### Selection method — pick the right one

| Method | When to use | How |
|---|---|---|
| **Random** | Default for transaction-level controls with large, listable populations | Number population sequentially → random number generator → select. Statistically defensible. |
| **Systematic** | Sequential populations where even period coverage matters | Interval = pop / sample size; random start in first interval; pick every Nth. Avoid if periodic patterns in pop. |
| **Judgmental (targeted)** | Small populations OR risk-based supplement to random | Pick items by risk attribute: large $, period-end, manual, related-party, new vendor/customer, override. **Document rationale per pick.** |
| **Haphazard** | Last resort when random is impractical and population is homogeneous | No specific pattern, spread across period, avoid unconscious bias (no "round numbers / top of list"). NOT statistically valid. |
| **Stratified** | Population has distinct sub-populations with different risk profiles | Split into strata (e.g., > $100K vs ≤ $100K); sample each stratum at appropriate size. |

**Always document:** population definition, population source (system + report + date pulled), completeness check on the population (footing, count match to GL), method, sample size, and per-item rationale (for judgmental).

### Population definition checklist

Before sampling:
- [ ] What is the EXACT population (transactions, users, changes, JEs, accounts)?
- [ ] What is the source system and the report used?
- [ ] What is the period covered?
- [ ] Has the population been tested for completeness and accuracy (IPE — see below)?
- [ ] Are there exclusions (and are they documented)?

## 2. Workpaper template

A workpaper a third party can re-perform meets these standards: **self-contained, cross-referenced, evidence-preserved, reviewer-trailed, conclusion-explicit.**

Per control tested:

```
WORKPAPER: [Control ID] - [Control Name]
Test period: [Start - End]
Prepared by: [Name, Date]    Reviewed by: [Name, Date]

1. CONTROL DESCRIPTION
   - Control ID:
   - Description (who/what/when/how):
   - Type: Manual / Automated / IT-Dependent Manual
   - Frequency:
   - Process / cycle:
   - Risk(s) addressed:
   - Assertion(s) addressed:
   - Key / non-key:

2. DESIGN EFFECTIVENESS (walkthrough)
   - Walkthrough date + transaction selected:
   - Evidence: [attach process flow + sample documentation]
   - Conclusion: [Effectively designed / Design gap]

3. POPULATION
   - Source system + report:
   - Date pulled:
   - Total population:
   - Completeness check (foot/count match):
   - IPE testing reference (if applicable): WP-IPE-XX

4. SAMPLE SELECTION
   - Method: [Random / Systematic / Judgmental / Stratified / Haphazard]
   - Rationale for method:
   - Sample size: [N] (with risk justification)
   - Selection details: [list of items selected; for judgmental, rationale per item]

5. TEST PROCEDURES (per sample)
   For each sample item, document:
   - Item ID + description
   - Procedures performed (inspect / observe / re-perform / inquire)
   - Evidence inspected (with file reference)
   - Result: Pass / Fail / N/A
   - If Fail: nature of exception, root cause, magnitude

6. SUMMARY
   - # tested:
   - # passed:
   - # failed:
   - Roll-forward results (if applicable):

7. IPE / INFORMATION PRODUCED BY THE ENTITY (if applicable)
   - Report relied upon:
   - Completeness test: [how validated]
   - Accuracy test: [how validated]
   - Conclusion on IPE:

8. CONCLUSION
   - [Operating effectively for the period tested]
   - OR [Deficiency identified — see deficiency evaluation WP-DEF-XX]

9. CROSS-REFERENCES
   - Walkthrough: WP-WT-XX
   - IPE WP: WP-IPE-XX
   - Deficiency WP: WP-DEF-XX (if applicable)
   - Supporting evidence: see attached folder
```

## 3. IPE — Information Produced by the Entity

If the control relies on a system-generated report (aging, exception list, JE listing, user access list), the report itself must be tested.

**Completeness:** does the report include ALL items it should? Test by:
- Reconciling totals/counts to the source system or GL
- Comparing record count to a separate query
- Reviewing report parameters (date filters, exclusions) for appropriateness

**Accuracy:** is the data in the report correct? Test by:
- Re-performing key calculations (e.g., aging buckets, balances)
- Tracing a sample of report rows back to source transactions
- Reviewing report logic / SQL if accessible

Document IPE separately in WP-IPE-XX and cross-reference from the control workpaper. **Without IPE testing, the control test is not complete** for IT-dependent manual controls.

## 4. Deficiency classification (CD / SD / MW)

Use a **likelihood × magnitude** evaluation. Likelihood is the chance the control failure could lead to a misstatement; magnitude is the size of the potential misstatement.

### Decision matrix

|   | Magnitude: Inconsequential | Magnitude: > Inconsequential, < Material | Magnitude: Material |
|---|---|---|---|
| **Likelihood: Remote** | Not a deficiency | Control Deficiency (CD) | Significant Deficiency (SD) |
| **Likelihood: Reasonably possible** | Control Deficiency (CD) | Significant Deficiency (SD) | **Material Weakness (MW)** |
| **Likelihood: Probable** | Control Deficiency (CD) | Significant Deficiency (SD) | **Material Weakness (MW)** |

### Definitions

- **Control Deficiency (CD)** — design or operation failure that prevents employees, in the normal course, from preventing/detecting misstatements timely. Below SD threshold.
- **Significant Deficiency (SD)** — less severe than MW, but important enough to merit attention by those charged with governance.
- **Material Weakness (MW)** — reasonable possibility that a material misstatement will not be prevented or detected timely.

### Strong indicators of MW (presumptive — document if you conclude otherwise)

- Restatement of previously issued financials to correct an error
- Identification of fraud (any magnitude) by senior management
- External auditor finds a material misstatement that internal controls didn't catch
- Ineffective audit committee oversight
- Ineffective period-end financial reporting process
- Pervasive ITGC failure affecting reliance on multiple application controls

### Compensating controls

If a compensating control exists that would prevent or detect the misstatement at the same magnitude:
- Document the compensating control AND test it
- If compensating control operates effectively → may reduce severity classification
- A compensating control does NOT eliminate a deficiency, but can downgrade severity

### Aggregation

Multiple individually-minor deficiencies in the same process or affecting the same assertion may aggregate to SD or MW. For each cycle:
1. List all CDs in the cycle
2. Evaluate combined likelihood × magnitude
3. Document aggregation analysis explicitly

### Remediation plan template (for each identified deficiency)

- **Root cause:** design gap / execution failure / staffing / training / system / IPE
- **Remediation action(s):** specific
- **Owner:**
- **Target date:**
- **Validation plan:** how & when re-tested to confirm effectiveness (typically requires sufficient time of operation post-remediation before re-conclusion)

## Standard control categories (with typical test approaches)

### Revenue (order-to-cash)
- Contract approval, 3-way match, revenue recognition review, AR aging review
- Sample: 25–40 invoices Q1–Q3 + 3–5 roll-forward
- Trace: contract → order → fulfillment → invoice → revenue posting → cash receipt

### Procure-to-pay (P2P)
- PO approval, 3-way match, vendor master changes, disbursement approval
- Sample: 25–40 disbursements Q1–Q3 + roll-forward
- Trace: PR → PO → receipt → invoice → match → approval → payment

### Close & financial reporting (CFR)
- Journal entry review, account reconciliation review, management review of financials
- Sample: 1 of each per quarter (4 total); MRC samples include re-performance of the reviewer's work
- Test: prep → independent review → evidence of challenge → resolution
- Almost always IPE-dependent → test the underlying reports

### Payroll
- New hire / termination access, payroll run review, payroll reconciliation
- Sample: 25 hires/terms + 4 quarterly reviews

### IT general controls (ITGC)
- Logical access (provisioning, deprovisioning, privileged access review)
- Change management (development → test → production with approvals)
- Computer operations (backup, batch monitoring, problem mgmt)
- Sample: 25 user adds, 25 terms, 25 changes; 4 quarterly access reviews
- ITGC failures often pervasive — propagate to all reliant application controls

### Entity-level controls (ELC)
- Code of conduct, whistleblower hotline, fraud risk assessment, audit committee oversight
- Sample: typically full population review (low frequency)
- Ineffective ELC (especially audit committee, tone at top) → strong MW indicator

## Tools that should be connected for best output

- **ERP** (NetSuite, SAP, Oracle, Workday) — population reports, JEs, sub-ledger
- **Provisioning system** (Okta, Entra, IdP) — ITGC user samples
- **Ticketing / change-mgmt** (Jira, Linear, ServiceNow, GitHub) — change samples
- **Document storage** (Box, Drive, SharePoint) — workpaper repository
- **GRC platform** (AuditBoard, Workiva, Hyperproof) — control matrix + workpaper hosting

## Output

Always produce:
1. **Sample selection memo** — population definition, source, completeness check, method, rationale, selections
2. **Testing workpaper** — per template above, fully populated
3. **Per-sample evidence checklist** — exactly what to collect for each sample item
4. **IPE workpaper** (if control relies on a report)
5. **Deficiency evaluation** (if exceptions) — likelihood × magnitude → CD/SD/MW with rationale, compensating controls considered, remediation plan
6. **Reviewer instructions** — what the reviewer should re-perform / look for
