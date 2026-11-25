---
name: nist-csf-scanner
description: "NIST Cybersecurity Framework (CSF 2.0) compliance scanner — auditing codebases and infrastructure under 6 core functions. Use when checking NIST CSF compliance."
---

# NIST CSF Scanner

## Overview

This skill audits a codebase and its associated infrastructure configurations against the 6 core functions of the NIST Cybersecurity Framework (CSF) 2.0 (Govern, Identify, Protect, Detect, Respond, Recover). It determines compliance levels for each category and subcategory, aggregates evidence, and produces an actionable compliance report. The goal is to provide a concrete, evidence-based assessment of NIST CSF alignment and define a remediation roadmap.

**Core principle:** Compliance is not a checklist; it is a continuous chain of evidence. If there is no evidence, there is no compliance.

## The Iron Law

```
THE COMPLIANCE LEVEL FOR A CSF SUBCATEGORY CANNOT BE DETERMINED WITHOUT GATHERING AT LEAST ONE PIECE OF TANGIBLE EVIDENCE.
A DECLARATION WITHOUT EVIDENCE IS AN INVALID DECLARATION.
```

## When to Use

**Use this when:**
- An organization or client asks, "Are we compliant with the NIST CSF?"
- Preparing for SOC 2, ISO 27001, or PCI DSS audits (where CSF serves as an overarching umbrella).
- Measuring the maturity level of a security program.
- Conducting a post-incident review to identify which CSF functions failed or were weak.
- Referencing CSF during the "security-by-design" phase of a new project or product launch.

**Use this ESPECIALLY when:**
- Management assumes the system is secure, but lacks empirical evidence to back up the claim — a CSF audit highlights the gaps.
- An audit is approaching and you need to quickly locate missing controls.
- You need data-driven evidence to justify security budget requests or resource allocation.

**Don't skip when:**
- Foundational security controls (encryption, authentication, logging) are not yet in place — establish baseline controls first, then apply the CSF.
- You are looking for a one-off "checkbox compliance" exercise — CSF is a framework for continuous improvement, not a single point-in-time check.

## Phase 1: Establish the CSF 2.0 Framework and Target Profile

**BEFORE proceeding:**

Inventory the target codebase and infrastructure components (cloud services, CI/CD pipelines, logging pipelines).

1. **Load the 6 NIST CSF 2.0 functions:**
   - **Govern (GV):** Security governance, risk management, and organizational roles/responsibilities.
   - **Identify (ID):** Asset management, risk assessment, and supply chain risk management.
   - **Protect (PR):** Identity management, data security, platform security, and infrastructure resilience.
   - **Detect (DE):** Anomaly detection, continuous monitoring, and detection processes.
   - **Respond (RS):** Incident response planning, communication, analysis, and mitigation.
   - **Recover (RC):** Recovery planning, post-incident improvement, and communication.
2. **Define the target compliance profile** (Current vs. Target Tier):
   - Tier 1: Partial
   - Tier 2: Risk Informed
   - Tier 3: Repeatable
   - Tier 4: Adaptive

```yaml
# Example target profile configuration
target_profile:
  govern: Tier 2
  identify: Tier 2
  protect: Tier 3
  detect: Tier 2
  respond: Tier 2
  recover: Tier 1
```

## Phase 2: Audit the Codebase Against CSF Subcategories

**BEFORE proceeding:**

Prepare a checklist containing the subcategories of NIST CSF 2.0 (approximately 100+ subcategories).

1. **Automate scanning:** Map the outputs of SAST, DAST, and SCA tools to relevant CSF subcategories.
2. **Audit configurations:**
   - CI/CD pipeline security → PR.AA (Platform Security)
   - IAM roles and permissions → PR.AA (Identity Management)
   - Logging configurations → DE.CM (Continuous Monitoring)
3. **Inspect code patterns:**
   - Cryptographic usage → PR.DS (Data Security)
   - Error handling and exception bubbles → DE.CM (Anomalies and Events)
   - Authorization gates and checks → PR.AA (Access Control)
4. **Gather EVIDENCE for each subcategory:**
   - Code snippets (e.g., encryption configuration in a class → PR.DS-01).
   - Configuration files (e.g., CSPRNG settings → PR.DS-01).
   - Log samples (e.g., authentication logs → DE.CM-01).
   - Documented policies.
   - Gap Note: "No evidence found" — this is a valid audit finding.

```python
# Example audit scan output
scan_result = {
    "GV.OC-01": {  # Govern: Roles and Responsibilities
        "status": "COMPLIANT",
        "evidence": ["docs/security-roles.md", "oncall-roster.yaml"],
        "notes": "Responsibility matrix exists and on-call rotation is active."
    },
    "ID.RA-01": {  # Identify: Risk Assessment
        "status": "PARTIALLY_COMPLIANT",
        "evidence": ["docs/risk-assessment-q1-2026.md"],
        "notes": "Risk assessment exists but has not been updated in the last 3 months.",
        "remediation": "Update risk assessments on a regular, recurring schedule."
    },
    "PR.DS-01": {  # Protect: Data Security (encryption)
        "status": "NON_COMPLIANT",
        "evidence": [],
        "notes": "No AES-256 encryption implementation found; sensitive files are stored in plaintext.",
        "remediation": "Implement encryption at rest for all sensitive data points."
    }
}
```

## Phase 3: Gap Analysis and Remediation Prioritization

**BEFORE proceeding:**

Ensure all subcategories have been audited and evidence has been cataloged.

1. **Calculate compliance percentages:**
   - COMPLIANT: Evidence exists and the control is active.
   - PARTIALLY_COMPLIANT: Evidence exists but is incomplete or outdated.
   - NON_COMPLIANT: No evidence of the control exists.
   - NOT_APPLICABLE: The subcategory does not apply to this project environment.
2. **Prioritize gaps:**
   - Critical: NON_COMPLIANT controls on high-risk data or systems.
   - High: PARTIALLY_COMPLIANT controls on sensitive systems.
   - Medium: PARTIALLY_COMPLIANT controls on low-risk systems.
   - Low: COMPLIANT controls that require continuous monitoring.
3. **Develop a remediation roadmap:**
   - Short term (0-30 days): Address Critical gaps.
   - Medium term (30-90 days): Address High gaps.
   - Long term (90+ days): Address Medium and Low gaps.

```
NIST CSF COMPLIANCE REPORT SUMMARY
=======================================
Total Subcategories Audited: 108
COMPLIANT:             45 (41.7%)
PARTIALLY_COMPLIANT:   32 (29.6%)
NON_COMPLIANT:            28 (25.9%)
NOT_APPLICABLE:         3  (2.8%)

By Core Function:
  Govern (GV):  35% COMPLIANT — ⚠️ Weak
  Identify (ID): 50% COMPLIANT — 🟡 Moderate
  Protect (PR):  30% COMPLIANT — ⚠️ Weak (Critical: Missing data encryption at rest)
  Detect (DE):   45% COMPLIANT — 🟡 Moderate
  Respond (RS):  60% COMPLIANT — ✅ Strong
  Recover (RC):  20% COMPLIANT — ⚠️ Weak

Top 5 Urgent Remediations:
  1. PR.DS-01 (Data Encryption) — Critical — Est: 14 days
  2. ID.AM-01 (Asset Inventory) — Critical — Est: 7 days
  3. DE.CM-03 (Log Monitoring) — High — Est: 21 days
  4. GV.RM-01 (Risk Management Process) — High — Est: 30 days
  5. RC.RP-01 (Recovery Plan) — High — Est: 45 days
```

## Phase 4: Final Verification

Before marking complete:

- [ ] Have all 6 functions of NIST CSF 2.0 been scanned?
- [ ] Is at least one piece of evidence documented for each subcategory? (If no evidence exists, is it marked NON_COMPLIANT?)
- [ ] Is the target profile (Current vs. Target Tier) defined?
- [ ] Does the gap analysis contain prioritized remediation steps?
- [ ] Does the report contain an executive summary for management and technical teams?
- [ ] Is a concrete fix proposed for every NON_COMPLIANT subcategory?
- [ ] Is a justification documented for every NOT_APPLICABLE subcategory?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Gathering evidence for this subcategory is too difficult, I will just assume we are COMPLIANT" — **Assumptions do not constitute compliance. Compliance without evidence is invalid.**
- "Let's only scan the Protect function and defer the rest" — **CSF is a holistic framework. Skipping functions makes the framework ineffective.**
- "There is encryption somewhere in the code, I will use that as evidence" — **Evidence must be specific and reachable. A vague claim is not evidence.**
- "We passed our SOC 2 audit, so we are automatically CSF-compliant" — **Frameworks overlap only partially. You must verify CSF controls independently.**
- "This subcategory does not apply to our project" — **Confirm this objectively. Do not mark items as inapplicable just because they are hard to verify.**

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why is this marked COMPLIANT? Show me the evidence." — You failed to document evidence.
- "You only audited the Protect function; what about the rest?" — You failed to scan all CSF functions.
- "This remediation step is too vague; what actions do I need to take?" — Propose actionable fixes.
- "Our target profile is Tier 3, but you evaluated us against Tier 1." — Correct the target profile configuration.
- "What evidence did you find for this subcategory?" — Ensure all findings map to explicit files or logs.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Gathering evidence takes too long; let's skip to the summary." | Evaluations without evidence are based on assumptions, which introduce compliance risks. |
| "CSF is too broad; we only need to focus on Protect." | Cybersecurity is a system. Focusing on one function leaves other vectors exposed. |
| "We are secure, so the framework is just paperwork." | Security requires proof. Frameworks establish verifiable trust. |
| "I'll reference our old audit reports as evidence." | Stale reports do not reflect the current system state; fresh evidence is required. |
| "I don't understand this subcategory, so I'll mark it NOT_APPLICABLE." | Research the subcategory requirements. Do not skip difficult items. |

## Related Skills

- **mitre-attack-mapper** — Map findings from Detect (DE) and Protect (PR) functions to MITRE ATT&CK techniques.
- **purple-team-analyzer** — Test Respond (RS) and Recover (RC) functions through purple team simulation exercises.

## Self-Review

After completing this process:

1. **Framework Check:** Were all 6 functions of CSF 2.0 fully evaluated?
2. **Evidence Check:** Is there a clear evidence link or a NON_COMPLIANT tag for every subcategory?
3. **Remediation Actionability:** Are remediation suggestions concrete, listing specific files or code paths?
4. **Iron Law Audit:** Did you compile at least one piece of evidence for each analyzed subcategory?
