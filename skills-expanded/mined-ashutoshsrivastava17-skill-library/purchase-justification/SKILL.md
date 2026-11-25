---
name: purchase-justification
description: >
  Write purchase justification documents with business case, ROI analysis,
  alternatives considered, and budget impact. Support internal approval
  workflows with clear rationale for procurement decisions.
  TRIGGER when: user says /purchase-justification, "purchase justification",
  "business case for purchase", "buy approval", "procurement approval",
  "justify a purchase", "purchase request", or asks about building a case
  for approving a procurement spend.
argument-hint: "[product or service] [estimated cost]"
user-invocable: true
---

# Purchase Justification

You are a procurement business analyst. Produce a clear, compelling purchase justification document that gives approvers the information they need to make a confident funding decision — including the business problem, proposed solution, financial analysis, risk assessment, and alternatives considered.

## Core Principles

1. **Lead with the problem, not the product** — Approvers care about the business impact, not feature lists
2. **Quantify everything possible** — Dollars, hours, percentages, and headcount tell a clearer story than adjectives
3. **Show your homework** — Demonstrate that alternatives were genuinely evaluated, not rubber-stamped
4. **Be honest about risk** — Acknowledging risk builds credibility; hiding it erodes trust
5. **Match depth to spend** — A $5K purchase needs 1 page; a $500K purchase needs a full business case

---

## Process

### Step 1 — Gather Inputs

Collect the information needed to build the justification.

| Input | Description | Fallback If Missing |
|---|---|---|
| Product / Service | What is being purchased | Ask before proceeding |
| Vendor | Proposed vendor name | Note as "vendor TBD" if in RFP phase |
| Estimated Cost | One-time and recurring costs | Provide a range with assumptions |
| Budget Source | Which budget or cost center funds this | Flag for finance to assign |
| Business Problem | The pain point or opportunity this addresses | Infer from context and confirm |
| Requesting Team | Department and sponsor | Ask before proceeding |
| Urgency | Why this purchase is needed now | Document the cost of delay |
| Alternatives Evaluated | Other options considered and why they were rejected | Note that evaluation is pending |
| Approval Threshold | Spending authority tiers for this amount | Reference standard procurement policy |

### Step 2 — Define the Business Problem

Frame the problem in terms that resonate with approvers.

| Component | Description | Example |
|---|---|---|
| **Current State** | What is happening today | "Customer onboarding takes 14 days on average due to manual document processing" |
| **Business Impact** | Quantified cost of the problem | "Estimated $320K/year in delayed revenue recognition and 2.1 FTE of manual effort" |
| **Root Cause** | Why the problem persists | "No automated document extraction; reliance on spreadsheet-based workflows" |
| **Trigger** | Why this is being addressed now | "Volume has grown 40% YoY; current process cannot scale without adding headcount" |
| **Strategic Alignment** | How solving this supports company goals | "Supports Q3 OKR to reduce onboarding time to < 5 days" |

### Step 3 — Present the Proposed Solution

Describe what is being purchased and why this option was selected.

| Element | Content |
|---|---|
| **Solution Overview** | 2-3 sentence plain-language description of the product/service |
| **Key Capabilities** | 3-5 specific capabilities mapped to the stated problem |
| **Vendor Rationale** | Why this vendor over alternatives (price, fit, references, risk) |
| **Implementation Scope** | What is included — deployment, configuration, training, support |
| **Timeline** | Expected implementation duration and key milestones |
| **Dependencies** | Internal resources, integrations, or approvals required |

### Step 4 — Build the Financial Analysis

Provide a clear picture of costs, benefits, and return on investment.

#### Cost Breakdown

| Cost Component | Year 1 | Year 2 | Year 3 | Total (3-Year) | Notes |
|---|---|---|---|---|---|
| License / Subscription | $... | $... | $... | $... | Per-seat / flat / usage-based |
| Implementation / Setup | $... | — | — | $... | One-time |
| Integration | $... | — | — | $... | One-time |
| Training | $... | $... | — | $... | Initial + refresher |
| Support / Maintenance | $... | $... | $... | $... | Included or add-on |
| Internal Resources | $... | $... | $... | $... | FTE time for project |
| **Total Cost** | **$...** | **$...** | **$...** | **$...** | |

#### Benefit Quantification

| Benefit | Calculation | Annual Value | Confidence |
|---|---|---|---|
| Labor savings | X hours/week x $Y/hour x 52 weeks | $... | High / Medium / Low |
| Revenue acceleration | X days faster x $Y/day in revenue | $... | High / Medium / Low |
| Error reduction | X errors/month x $Y cost per error | $... | High / Medium / Low |
| Avoided headcount | X FTEs not hired x $Y fully loaded | $... | High / Medium / Low |
| Risk mitigation | Reduced exposure to [risk] valued at $Y | $... | High / Medium / Low |
| **Total Annual Benefits** | | **$...** | |

#### ROI Summary

| Metric | Value |
|---|---|
| Total 3-Year Cost | $... |
| Total 3-Year Benefit | $... |
| Net Benefit | $... |
| ROI | ...% |
| Payback Period | X months |
| NPV (at X% discount rate) | $... |

### Step 5 — Document Alternatives Considered

Show that the recommendation was reached through a fair evaluation.

| Option | Description | Estimated Cost | Pros | Cons | Why Not Selected |
|---|---|---|---|---|---|
| **Recommended** | [Proposed solution] | $... | ... | ... | — (Selected) |
| Alternative A | [Description] | $... | ... | ... | [Specific reason] |
| Alternative B | [Description] | $... | ... | ... | [Specific reason] |
| Do Nothing | Maintain status quo | $0 direct | No spend | Problem persists/grows | [Quantified cost of inaction] |
| Build In-House | Develop internally | $... | Full control | Time, opportunity cost | [Specific reason] |

### Step 6 — Assess Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Implementation delay | Medium | Medium | Phased rollout; buffer in timeline |
| Vendor lock-in | Medium | High | Negotiate data portability and exit clause |
| User adoption resistance | Medium | Medium | Change management plan; executive sponsorship |
| Integration complexity | Low | High | Proof of concept before full commitment |
| Budget overrun | Low | Medium | Fixed-price implementation; contingency reserve |
| Vendor viability | Low | High | Financial review; escrow for source code |

---

## Output Format

Deliver the purchase justification as a structured document:

```markdown
# Purchase Justification — [Product/Service Name]

**Requested by:** [Name, Title, Department]
**Date:** [Date]
**Vendor:** [Vendor Name]
**Total Estimated Cost:** [$Amount] over [Duration]
**Budget Source:** [Cost Center / Budget Line]
**Approval Required From:** [Name(s) based on spending authority]

---

## 1. Executive Summary
[2-3 sentences: problem, proposed solution, expected ROI, requested action]

## 2. Business Problem
[Current state, business impact, root cause, trigger, strategic alignment]

## 3. Proposed Solution
[Solution overview, key capabilities, vendor rationale, timeline]

## 4. Financial Analysis
### Cost Breakdown
[Multi-year cost table]
### Benefits
[Quantified benefit table with confidence levels]
### ROI Summary
[ROI, payback period, NPV]

## 5. Alternatives Considered
[Comparison table including do-nothing and build options]

## 6. Risk Assessment
[Risk matrix with mitigations]

## 7. Recommendation
[Clear statement: "We recommend approving..." with the top 3 reasons]

## 8. Approval
| Approver | Role | Signature | Date |
|---|---|---|---|
| [Name] | [Title] | _________ | _______ |
```

---

## Quality Checklist

- [ ] Business problem is stated in terms of business impact, not technology gaps
- [ ] ROI calculation uses conservative, defensible assumptions
- [ ] At least 3 alternatives are documented (including do-nothing and build-in-house)
- [ ] Cost breakdown includes internal resource costs, not just vendor invoices
- [ ] Benefits are quantified with stated confidence levels (High / Medium / Low)
- [ ] Risks are honest — not minimized to make the case look better
- [ ] The executive summary can stand alone for a busy approver
- [ ] Payback period is realistic (if > 18 months, justify why it is still worthwhile)
- [ ] Budget source and approval authority are identified
- [ ] Document length matches spend level — concise for small purchases, detailed for large

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Purchase under $5K (low-threshold) | Produce a 1-page summary: problem, solution, cost, approval line — skip full ROI |
| Recurring SaaS with auto-renewal | Flag the renewal date; note that inaction means implicit re-approval at current terms |
| Replacing an existing tool | Include migration costs, parallel-run period, and user retraining in the cost analysis |
| Benefits are primarily qualitative | Use a scoring framework (High/Medium/Low impact) instead of forcing dollar estimates |
| Multiple departments share the cost | Document the cost-split agreement and each department's approval requirement |
| Emergency purchase already made | Frame as retroactive justification; document the urgency and note process exception |
| Purchase requires board or legal approval | Add compliance and legal review steps; extend the approval chain section |
