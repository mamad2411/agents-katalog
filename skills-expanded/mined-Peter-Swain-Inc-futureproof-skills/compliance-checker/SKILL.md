---
name: compliance-checker
description: |
  Audits policies, workflows, and vendor agreements against regulatory
  frameworks (GDPR, SOC 2, HIPAA, PCI DSS, ISO 27001, SOX, CCPA), producing
  a risk-rated findings register and remediation roadmap. Use when a user
  says "review this policy for GDPR compliance", "are we SOC 2 ready",
  "audit our data handling against HIPAA", or "what are the compliance gaps
  in this vendor contract". For regulatory gap analysis, not project-level
  risk registers or vendor evaluation.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="compliance-checker")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to load the user's regulatory environment, prior audit findings, known risk areas, and organisational compliance maturity level.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Material under review** — share the document, process description, policy, vendor agreement, or operational workflow to audit
- **Applicable regulatory frameworks** — which standards apply? (e.g., GDPR, SOC 2, HIPAA, PCI DSS, ISO 27001, SOX, CCPA, industry-specific regulations)
- **Scope and boundary** — is this a full-scope compliance review or targeted to specific control domains (e.g., data retention, access management, incident response)?
- **Compliance objective** — what is the immediate driver? (upcoming audit, new regulation, vendor due diligence, board reporting, ICA-facing trust requirement, M&A readiness)
- **Known gaps or prior findings** — any outstanding remediation items, previous audit observations, or areas of suspected non-compliance?

If FutureProof context contains prior compliance sessions, surface previous findings and ask the user to confirm whether those items have been remediated or remain open.

## Step 3: Establish the Control Framework

Before analysing, construct the applicable **Compliance Control Matrix (CCM)**:

1. **Framework mapping** — map the user's stated regulatory requirements to specific control objectives (e.g., GDPR Article 32 → encryption at rest and in transit; SOC 2 CC6.1 → logical access controls)
2. **Control hierarchy** — organise controls into domains:
   - **Governance & oversight** — policy ownership, board-level accountability, compliance officer designation
   - **Data management** — classification, retention, disposal, cross-border transfer, consent management
   - **Access & identity** — least privilege, role-based access, MFA, privileged access management
   - **Operational security** — change management, incident response, business continuity, disaster recovery
   - **Third-party risk** — vendor assessment, contractual safeguards, sub-processor management, right-to-audit clauses
   - **Monitoring & assurance** — logging, continuous monitoring, internal audit cadence, evidence retention
3. **Materiality threshold** — classify each control as **Critical** (regulatory mandate with enforcement risk), **High** (industry expectation or contractual obligation), or **Moderate** (best practice, maturity enhancer)

Apply any user-specific `instructions` from FutureProof context to weight domains appropriately (e.g., if the user operates in healthcare, elevate HIPAA-specific controls; if ICA agreements mandate specific certifications, flag those as Critical).

## Step 4: Conduct the Compliance Assessment

Perform a structured, evidence-based review of the submitted material against the CCM:

### 4a. Document & Process Analysis
- **Completeness** — are all required policy elements present per the applicable framework? (e.g., does a privacy policy contain all GDPR Article 13/14 disclosures?)
- **Currency** — are documents dated, version-controlled, and reviewed within the required cadence?
- **Specificity** — do policies contain actionable procedures, or are they aspirational statements lacking operational detail?
- **Consistency** — do cross-referenced documents align? (e.g., does the data retention schedule match what the privacy policy states?)

### 4b. Control Effectiveness Evaluation
For each applicable control domain, assess:
- **Design effectiveness** — is the control designed to meet the regulatory objective if operating as intended?
- **Implementation evidence** — does the submitted material demonstrate the control is actually implemented (not merely documented)?
- **Gap identification** — where controls are absent, incomplete, or insufficiently evidenced, document with specificity

### 4c. Risk Rating
Assign each finding a risk rating using a standardised taxonomy:
- 🔴 **Critical** — direct regulatory violation or material control absence; immediate remediation required; potential enforcement, penalty, or breach exposure
- 🟠 **High** — significant gap that would likely result in an audit finding; remediation required before next assessment cycle
- 🟡 **Moderate** — partial control implementation or documentation weakness; remediation recommended to improve compliance posture
- 🔵 **Low / Observation** — best-practice enhancement; no immediate regulatory risk but would strengthen maturity

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver Output

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce a **Compliance Assessment Report** with the following sections:

### 5a. Executive Summary
- One-paragraph compliance posture statement suitable for board or leadership reporting
- Overall readiness rating: **Audit-Ready**, **Conditionally Ready** (with stated conditions), **Not Ready** (with critical blockers)
- Count of findings by risk rating (🔴 / 🟠 / 🟡 / 🔵)

### 5b. Findings Register
A structured table for each finding:

| # | Control Domain | Framework Reference | Finding Description | Risk Rating | Evidence Gap | Remediation Action | Recommended Owner | Target Date |
|---|---------------|---------------------|--------------------:|:-----------:|:------------:|:------------------:|:-----------------:|:-----------:|

Populate with specific, actionable findings — not generic observations. Each remediation action must be a concrete task (e.g., "Draft a data sub-processor register including contractual review dates and append to Vendor Management Policy v3.2"), not vague guidance.

### 5c. Critical Remediation Roadmap
For all 🔴 and 🟠 findings, produce a sequenced remediation plan:
- **Phase 1 (Immediate — 0–30 days)** — critical violations requiring urgent action
- **Phase 2 (Short-term — 30–90 days)** — high-risk gaps requiring structured remediation
- **Phase 3 (Ongoing — 90+ days)** — moderate enhancements and continuous improvement items

### 5d. Compliance Control Matrix (Populated)
Return the CCM from Step 3, now populated with assessment status per control:
- ✅ **Conforming** — control designed and operating effectively
- ⚠️ **Partially Conforming** — control exists but has gaps in design or evidence
- ❌ **Non-Conforming** — control absent or materially deficient
- ⬜ **Not Assessed** — outside scope of this review

### 5e. ICA & Stakeholder Impact Note
Where findings affect ICA-facing commitments (e.g., DPA obligations, SLA compliance claims, trust page representations), flag these explicitly with recommended ICA communication actions.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="compliance-checker", experiment={
  hypothesis: "Implementing a pre-audit self-assessment checklist for control owners reduces critical findings by surfacing gaps before formal review",
  variants: ["control: current ad-hoc review process", "variant: structured self-assessment checklist distributed to control owners 30 days before compliance review"],
  measurement: "Number of 🔴 and 🟠 findings in next compliance assessment compared to current session baseline",
  expected_impact: "40% reduction in critical and high-risk findings at next review cycle"
})
```

## Step 7: Request Research

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:request_research(skill="compliance-checker",
  query="Regulatory enforcement trends, new compliance obligations, and updated framework requirements for [user's applicable frameworks] in 2024–2025, including emerging AI governance and data sovereignty mandates",
  reason="Ensure compliance assessments reflect current enforcement priorities and upcoming regulatory changes that may introduce new control requirements"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="compliance-checker", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```