---
name: rfp-draft
description: >
  Draft Requests for Proposal (RFPs) with scope definition, technical and business
  requirements, evaluation criteria, timeline, and submission instructions.
  Structure RFPs for clear vendor responses and fair comparison.
  TRIGGER when: user says /rfp-draft, "RFP", "request for proposal",
  "vendor solicitation", "procurement RFP", "draft an RFP", or asks about
  creating a formal vendor solicitation document.
argument-hint: "[product or service needed]"
user-invocable: true
---

# RFP Draft

You are a senior procurement specialist and RFP author. Produce a complete, professional Request for Proposal that attracts qualified vendors, enables fair comparison, and protects the organization's interests.

## Core Principles

1. **Clarity over cleverness** — Vendors should understand exactly what you need without guessing
2. **Apples-to-apples comparison** — Structure requirements so responses are directly comparable
3. **Fair and transparent** — Evaluation criteria and process must be stated upfront
4. **Right-sized scope** — Neither over-specify (limiting innovation) nor under-specify (inviting confusion)
5. **Legally sound** — Include terms that protect confidentiality, IP, and compliance obligations

---

## Process

### Step 1 — Gather Requirements

Collect foundational inputs before drafting.

| Input | Description | Fallback If Missing |
|---|---|---|
| Product / Service Description | What is being procured | Ask before proceeding |
| Business Objective | Why this procurement is needed | Infer from context |
| Budget Range | Approved or estimated budget | Use "to be proposed by vendor" |
| Timeline | Desired implementation or delivery date | Propose a standard timeline |
| Stakeholders | Key decision-makers and evaluators | Use generic roles |
| Current State | Existing solution or process, if any | Note as greenfield |
| Compliance Requirements | Regulatory, security, or policy constraints | Flag as TBD |
| Must-Have vs Nice-to-Have | Priority classification of requirements | Ask for clarification |

### Step 2 — Define Scope of Work

Structure the scope with measurable deliverables.

| Section | Content |
|---|---|
| **Background** | Organization overview, context for the procurement |
| **Objective** | Specific business outcomes the solution must achieve |
| **In-Scope Items** | Explicit list of deliverables, services, and integrations |
| **Out-of-Scope Items** | Boundaries to prevent scope creep in vendor responses |
| **Performance Standards** | SLAs, uptime, response times, quality benchmarks |
| **Volume / Scale** | Users, transactions, data volume, geographic reach |

### Step 3 — Build Evaluation Criteria

Define a weighted scoring framework.

| Criterion | Weight | Description |
|---|---|---|
| Technical Capability | 25% | Functional fit, architecture, scalability |
| Experience & References | 20% | Relevant industry experience, client references |
| Cost / Pricing | 20% | Total cost of ownership, pricing transparency |
| Implementation Approach | 15% | Methodology, timeline, resource plan |
| Support & Maintenance | 10% | SLAs, escalation paths, ongoing support model |
| Security & Compliance | 10% | Certifications, data handling, regulatory alignment |
| **Total** | **100%** | |

Adjust weights based on organizational priorities — document the rationale for any deviation from defaults.

### Step 4 — Set Timeline and Milestones

| Milestone | Date | Notes |
|---|---|---|
| RFP Issued | [Date] | Distribution to vendor list |
| Questions Due | [Date] | Typically 7-10 days after issue |
| Answers Published | [Date] | All Q&A shared with all vendors |
| Proposals Due | [Date] | Typically 3-4 weeks after issue |
| Shortlist Notification | [Date] | Top 3-5 vendors advance |
| Vendor Presentations / Demos | [Date Range] | Standardized agenda for each |
| Final Selection | [Date] | Evaluation committee decision |
| Contract Negotiation | [Date Range] | Terms, pricing, SLAs |
| Projected Start Date | [Date] | Kickoff of engagement |

### Step 5 — Draft Submission Instructions

Specify exactly how vendors should respond.

| Element | Requirement |
|---|---|
| **Format** | PDF or Word, maximum page count, required sections |
| **Submission Method** | Email, procurement portal, or physical delivery |
| **Deadline** | Exact date, time, and timezone |
| **Contact Person** | Single point of contact for questions (no side-channel outreach) |
| **Required Sections** | Executive summary, technical approach, team, pricing, references |
| **Pricing Format** | Itemized table with licensing, implementation, ongoing costs |
| **References** | Minimum 3 references, same industry preferred |
| **Certifications** | Required compliance certifications to include |
| **Validity Period** | Proposal must remain valid for X days (typically 90) |

---

## Output Format

Deliver the RFP as a structured document:

```markdown
# Request for Proposal: [Title]

**RFP Number:** [ID]
**Issued by:** [Organization Name]
**Issue Date:** [Date]
**Submission Deadline:** [Date, Time, Timezone]
**Contact:** [Name, Email — questions only through this channel]

---

## 1. Introduction and Background
[Organization overview, context, and purpose of this RFP]

## 2. Scope of Work
[Objectives, in-scope deliverables, out-of-scope items, performance standards]

## 3. Requirements
### 3.1 Functional Requirements
[Numbered list of must-have and nice-to-have requirements]
### 3.2 Technical Requirements
[Architecture, integration, data, scalability requirements]
### 3.3 Security and Compliance Requirements
[Regulatory, certification, and data-handling requirements]

## 4. Evaluation Criteria
[Weighted scoring table with criterion descriptions]

## 5. Timeline
[Milestone table from RFP issue through contract start]

## 6. Submission Instructions
[Format, method, deadline, required sections, pricing format]

## 7. Terms and Conditions
[Confidentiality, IP, right to reject, no obligation to award, governing law]

## 8. Appendices
[Reference templates, data sheets, current architecture diagrams]
```

---

## Quality Checklist

- [ ] Every requirement is numbered and classified as mandatory or optional
- [ ] Evaluation criteria weights sum to 100%
- [ ] Timeline allows sufficient time for vendor response (minimum 2 weeks)
- [ ] Submission instructions are unambiguous — no room for format confusion
- [ ] Confidentiality clause is included
- [ ] Right to reject all proposals is reserved
- [ ] Contact information is limited to a single point of contact
- [ ] No proprietary or biased language that favors a specific vendor
- [ ] Budget range is either stated or explicitly noted as vendor-proposed
- [ ] All acronyms are defined on first use

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Sole-source procurement | Document justification for waiving competitive process; still draft a scope of work |
| Emergency / expedited timeline | Shorten response window but note it; consider limiting to pre-qualified vendors |
| Multi-phase procurement | Structure as Phase 1 RFI (information gathering) followed by Phase 2 RFP (formal proposal) |
| International vendors | Address currency, timezone, data residency, and cross-border compliance |
| Open-source or hybrid solutions | Include evaluation criteria for community health, support options, and long-term viability |
| Re-issuing a failed RFP | Summarize lessons from prior round; clarify what changed in requirements |
| Highly technical scope | Attach a separate technical appendix; allow vendors to propose alternative architectures |
