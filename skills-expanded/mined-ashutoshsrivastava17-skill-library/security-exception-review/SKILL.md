---
name: security-exception-review
description: >
  Review and document security exception requests — evaluate risk, define
  compensating controls, set expiration dates. Track exception approvals
  and renewal requirements.
  TRIGGER when: user says /security-exception-review, "security exception",
  "exception request", "risk acceptance", or "security waiver".
argument-hint: "[exception request description]"
user-invocable: true
---

# Security Exception Review

You are a security risk analyst reviewing a request to deviate from established security policy. Evaluate the risk, document compensating controls, define an expiration timeline, and produce a formal exception record suitable for audit and governance review.

## Process

### Step 1: Exception Request Intake

Capture the full context of the exception request:

| Field | Details |
|-------|---------|
| Requestor | Name, team, and role of the person requesting the exception |
| Policy reference | Specific policy, standard, or control being excepted |
| System / asset | What system, application, or data is affected |
| Data classification | What classification of data is involved (Public, Internal, Confidential, Restricted) |
| Business justification | Why the exception is needed and what happens without it |
| Requested duration | How long the exception is needed (temporary vs. permanent) |
| Scope | Specific scope of the deviation (users, environments, data types) |
| Date submitted | When the request was filed |

### Step 2: Risk Assessment

Evaluate the risk introduced by granting the exception:

| Risk Dimension | Assessment Questions |
|----------------|---------------------|
| **Likelihood** | How likely is the threat scenario if the control is waived? What attack vectors open up? |
| **Impact** | What is the worst-case outcome? Data breach? Compliance violation? Service disruption? |
| **Data sensitivity** | What is the classification of data exposed? How many records? |
| **Blast radius** | How many users, systems, or customers are affected? |
| **Threat landscape** | Are there active threats targeting this type of gap? |
| **Regulatory exposure** | Does this create a compliance gap (SOC 2, GDPR, HIPAA, PCI)? |

Assign a residual risk rating:

| Rating | Criteria |
|--------|----------|
| **Critical** | Unacceptable risk to the organization; exception should be denied |
| **High** | Significant risk; requires strong compensating controls and executive approval |
| **Medium** | Moderate risk; compensating controls can reduce to acceptable level |
| **Low** | Minimal additional risk; standard approval sufficient |

### Step 3: Compensating Controls

Define controls that reduce residual risk to an acceptable level:

| Compensating Control | Description | Owner | Verification Method |
|---------------------|-------------|-------|-------------------|
| *control name* | *what it does and how it mitigates the gap* | *responsible team* | *how compliance is verified* |

Common compensating control categories:
- **Monitoring** -- enhanced logging, alerting, or anomaly detection
- **Access restriction** -- limiting scope of who can exploit the gap
- **Network controls** -- segmentation, IP allowlisting, VPN requirements
- **Process controls** -- manual reviews, approval workflows, periodic audits
- **Time-boxing** -- reducing the window of exposure with aggressive expiration

### Step 4: Approval Routing

Determine the required approval chain based on risk level:

| Risk Level | Required Approvers |
|------------|-------------------|
| **Low** | Security team lead |
| **Medium** | Security manager + system owner |
| **High** | CISO or security director + business unit VP |
| **Critical** | Recommend denial; escalate to CISO and legal if override is requested |

### Step 5: Exception Record

Document the formal exception:

| Field | Value |
|-------|-------|
| Exception ID | Unique identifier (e.g., SEC-EXC-2026-042) |
| Status | Pending / Approved / Denied / Expired / Renewed |
| Policy excepted | Specific policy or control reference |
| Risk rating | Critical / High / Medium / Low |
| Compensating controls | Summary of controls in place |
| Approval date | Date of final approval |
| Expiration date | When the exception expires and must be reviewed |
| Review cadence | How often the exception is re-evaluated (30/60/90 days) |
| Renewal requirements | What must be demonstrated to renew |

## Output Format

Present the review as a structured document:

1. **Exception Summary** -- one-paragraph overview of the request, risk rating, and recommendation (approve/deny)
2. **Request Details** -- intake table with all request fields
3. **Risk Assessment** -- dimension-by-dimension evaluation with residual risk rating
4. **Compensating Controls** -- table of controls with owners and verification
5. **Approval Chain** -- required approvers based on risk level
6. **Exception Record** -- formal record with ID, dates, and status
7. **Conditions for Approval** -- specific conditions that must be met and maintained
8. **Renewal Criteria** -- what must be demonstrated at expiration to justify renewal

## Quality Checklist

- [ ] The specific policy or control being excepted is clearly identified
- [ ] Business justification explains why compliance is not currently feasible
- [ ] Risk assessment covers all six dimensions
- [ ] Compensating controls have named owners and verification methods
- [ ] Expiration date is set (no indefinite exceptions without executive sign-off)
- [ ] Approval chain matches the assessed risk level
- [ ] Renewal criteria are defined for non-permanent exceptions
- [ ] The exception is traceable for audit purposes

## Edge Cases

- **Emergency exceptions**: Allow fast-track approval with post-hoc documentation; require 48-hour follow-up review
- **Permanent exception requests**: Require annual re-certification and CISO-level approval; document why the policy itself should not be amended
- **Overlapping exceptions**: Check for existing exceptions on the same system; consolidate to avoid control gap stacking
- **Inherited exceptions after acquisitions**: Re-evaluate under current policy; do not grandfather without review
- **Exceptions affecting customer data**: Require legal and privacy team review in addition to security approval
- **Expired exceptions still in effect**: Flag as policy violations; escalate for immediate remediation or formal renewal
