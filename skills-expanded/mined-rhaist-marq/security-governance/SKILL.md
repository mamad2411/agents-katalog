---
name: security-governance
description: Covers structuring a security governance program, including the policy/standard/procedure/guideline hierarchy, security charter, operating model and RACI, committee cadence, and the policy lifecycle with exceptions. Use when the user asks how to write or organize security policies, set up a security steering committee, define security roles and responsibilities, or manage policy exceptions.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Security governance

Governance = who decides, on what authority, and how it's written down. The deliverable
is a documented-authority chain: charter → policy → standard → procedure, plus a body
that owns decisions and a cadence that reviews them. NIST CSF 2.0 made this a first-class
**Govern (GV)** function (2024) with six categories: GV.OC context, GV.RM risk strategy,
GV.RR roles/authorities, GV.PO policy, GV.OV oversight, GV.SC supply-chain. Map your
program to these so it travels: https://csf.tools/reference/nist-cybersecurity-framework/v2-0/gv/

## The document hierarchy (people conflate these: don't)

| Type          | Answers             | Binding?  | Changes      | Example                                                        |
| ------------- | ------------------- | --------- | ------------ | -------------------------------------------------------------- |
| **Policy**    | _Why / what_        | Mandatory | Rarely (yrs) | "All access requires MFA." Board/exec-approved, tech-agnostic. |
| **Standard**  | _What, exactly_     | Mandatory | Periodic     | "MFA = FIDO2 or TOTP; SMS prohibited." Measurable, testable.   |
| **Procedure** | _How, step by step_ | Mandatory | Often        | "To enroll a YubiKey: 1… 2… 3…" Owned by the doing team.       |
| **Guideline** | _Recommended_       | Advisory  | As needed    | "Prefer hardware keys for admins." Best-practice, not audited. |

Rules of thumb: a policy that names a vendor or a port number is really a standard.
A standard you can't test against is really a guideline. Audit tests against
**standards**, not policy prose. Keep policies short (1 to 2 pages) so they survive
re-org and tooling churn; put the churn in standards/procedures.

## Security charter

The charter is the program's mandate: without it the CISO has responsibility but no
authority. One page, signed by the CEO/board. Must state:

- Mission/scope of the security function and what's explicitly out of scope.
- The CISO's decision authority (what they can mandate vs recommend) and escalation path.
- Reporting line (to whom, how often) and budget-ownership.
- The governance body it convenes (below) and its decision rights.

## Operating model & RACI for security decisions

Pick a model and name it: **centralized** (security owns controls; small/regulated orgs),
**federated** (central policy, BU-local execution; most mid/large), or **embedded**
(security engineers sit in product teams; fast-moving eng orgs). Then make decision
rights explicit. A workable default RACI:

| Decision                        | Board | CISO | Risk owner (biz) | Security team | IT/Eng |
| ------------------------------- | ----- | ---- | ---------------- | ------------- | ------ |
| Approve security policy         | A     | R    | C                | C             | I      |
| Set risk appetite               | A     | R    | C                | I             | I      |
| Accept a residual risk          | A/C\* | C    | **A**            | R             | I      |
| Approve a policy exception      | I     | A    | R                | C             | I      |
| Pick/standardize a control      | I     | A    | C                | R             | C      |
| Declare/manage a major incident | I     | A    | C                | R             | R      |

\*Board accepts only above an escalation threshold (e.g. risk > $X or > appetite).
Key principle: **the business risk owner accepts risk, not security**: security advises
and records. If security "owns" all risk acceptance, the org never makes real tradeoffs.

## Governance body & reporting cadence

| Forum                       | Who                        | Cadence   | Decides                                            |
| --------------------------- | -------------------------- | --------- | -------------------------------------------------- |
| Security/risk steering cmte | CISO + business + IT leads | Monthly   | Exceptions, control standards, initiative priority |
| Exec risk committee         | C-suite                    | Quarterly | Risk appetite, budget, top-risk treatment          |
| Board / audit committee     | Board                      | Quarterly | Oversight, accept top residual risk, strategy      |
| Out-of-cycle                | As needed                  | On Sev1/2 | Major incident, material change                    |

Reporting _content_ and how to frame metrics for these audiences is a separate skill:
`load_skill board-metrics-reporting` (framing) and `load_skill security-metrics` (what to measure).

## Policy lifecycle & exceptions

1. **Draft** → review by affected owners → **approve** at the right level (policy = exec/board;
   standard = CISO). 2. **Publish** somewhere everyone can find it; communicate the change.
2. **Review on a fixed cadence**: annually, or on trigger (new reg, incident, major change).
   Every doc carries owner + last-reviewed + next-review date; a policy with no review date is dead.
3. **Retire** explicitly: superseded docs get archived, not left to rot.

**Exceptions are the pressure valve; make them formal, time-boxed, and visible:**

- Every exception names: the rule, the reason, a compensating control, a **risk owner who
  accepts**, and an **expiry date** (default ≤ 90 days; no permanent exceptions).
- Track them in one register; review at the steering committee. A pile of "temporary"
  exceptions to the same standard means the standard is wrong; fix the standard.
- An expired exception is a finding. Feed material ones to `report_finding` so governance
  gaps land in the same `render_report` deliverable as technical findings.

## Pairs with

- Framework choice that sets the governance baseline: `load_skill choosing-a-framework`, `load_skill nist-csf`.
- Risk appetite & register the body governs: `load_skill risk-assessment`.
- Multi-year build-out of the program: `load_skill security-program-roadmap`.
