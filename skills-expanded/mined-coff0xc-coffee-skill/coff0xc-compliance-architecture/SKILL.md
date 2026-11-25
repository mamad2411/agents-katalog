---
name: coff0xc-compliance-architecture
description: "Use when the user requests security architecture, threat modeling, compliance, data security/privacy/DLP, or baselines: STRIDE, MLPS (China classified protection), PCI-DSS, GDPR, ISO27001, SOC2, CIS/NIST, control evidence, risk register, audit log, executive/compliance report, release evidence. Manual trigger: Use coff0xc-compliance-architecture."
---

# coff0xc-compliance-architecture

<!-- skill-id: cs-car-a64d8e31 -->

## Quick Rules (read this first for everyday tasks)
> **[Scope first]** Define system boundaries, data classification, trust boundaries, compliance frameworks, control objectives, and evidence sources first.
> **[Architecture gate]** Map each risk to assets, threats, controls, owners, verification evidence, and residual risk.
> **[Auditable output]** Deliver threat models, control matrices, gaps, priorities, exceptions, and remediation paths.
> **[Hard boundary]** Confirm first for legal opinions, customer commitments, formal certification statements, production policy changes, and public releases.

Follow this section first for ordinary security-architecture/compliance reviews; expand the full workflow only for formal audits, customer delivery, or enterprise control governance.

## Capability
Governance capability for security architecture, threat modeling, compliance mapping, data security, and maturity assessment. It turns system design, control requirements, and audit evidence into risk-decision material that can actually land.

## What It Can Deliver
- Architecture risk reviews and trust-boundary diagrams
- STRIDE/threat modeling, control matrices, and gap analysis
- Data classification, privacy, DLP, and log-audit recommendations
- Compliance evidence checklists, remediation paths, and launch gates

## What Input It Can Take
- Architecture diagrams, data flows, system descriptions, launch plans
- Compliance requirements, control items, audit evidence, policy documents
- Data classification, permission models, logs, and risk registers

## Safe-Use Boundaries
- Design reviews, gap analysis, and evidence organization can be done directly
- Does not substitute for legal opinions, formal audit sign-off, or regulatory conclusions
- Production policy changes, permission tightening, and data-handling actions must be confirmed first
- Security capabilities are used only for authorized, defensive, detection, hardening, validation, and reporting purposes by default; do not provide unauthorized attack, credential theft, persistence, detection evasion, C2, phishing collection, data exfiltration, or destructive steps.

## Why You Can Trust It
- Maps control items to concrete system evidence
- Distinguishes must-fix, acceptable risk, and later improvement
- Output is understandable to engineering, audit, and management alike

## Typical Usage
```text
Use coff0xc-compliance-architecture for a pre-launch security architecture review and threat modeling.
Use coff0xc-compliance-architecture to map these control items into an audit evidence checklist.
Use coff0xc-compliance-architecture to build a risk model and remediation roadmap.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
