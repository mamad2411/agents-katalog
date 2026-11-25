---
name: coff0xc-authorized-assessment
description: "Use only for authorized security assessment: when the user requests authorized assessment, ROE, attack surface, recon/fingerprint, red team/adversary emulation, defensive attack-chain planning, control validation, CDN/WAF boundaries, phishing/social-engineering simulation planning, or reports. Confirm scope first for high-risk actions. Manual trigger: Use coff0xc-authorized-assessment."
---

# coff0xc-authorized-assessment

<!-- skill-id: cs-aas-f36c09a2 -->

## Quick Rules (read this first for everyday tasks)
> **[Authorization first]** Confirm asset scope, ROE, testing window, prohibited actions, and evidence retention first; without authorization, do defensive planning only.
> **[Defensive translation]** Translate attack-chain language into control validation, detection coverage, risk review, and remediation priority.
> **[Execution gate]** Active scanning, social-engineering exercises, bypass validation, real exfiltration, production actions, and third-party targets must be confirmed first.
> **[Delivery standard]** Output scope, stages, observation points, stop conditions, evidence levels, and report structure.

Follow this section first for ordinary authorized-assessment tasks; expand the full workflow only for written ROE, exercise execution, or cross-security-domain orchestration.

## Capability
Planning for authorized security assessment and red-team-to-defense mapping. It organizes assessment scope, ROE, attack surface, control validation, and report structure into a plan that can be approved, executed, and reviewed.

## What It Can Deliver
- Authorization scope and ROE drafts
- Attack-surface inventory, test stages, and prohibited actions
- Control-validation matrix, detection coverage, and exercise observation points
- Report structure, risk register, and review/improvement plan

## What Input It Can Take
- Authorization statements, asset scope, testing windows, prohibited actions
- Attack-surface leads, architecture diagrams, protective controls, logging capability
- Exercise objectives, compliance requirements, report templates

## Safe-Use Boundaries
- Without explicit authorization, output only preparation checklists and defensive recommendations
- Do not provide bypass, persistence, credential-theft, exfiltration, or destructive steps
- Any active testing, social-engineering exercise, external infrastructure, or remote action must be confirmed first
- Security capabilities are used only for authorized, defensive, detection, hardening, validation, and reporting purposes by default; do not provide unauthorized attack, credential theft, persistence, detection evasion, C2, phishing collection, data exfiltration, or destructive steps.

## Why You Can Trust It
- Defines boundaries and stop conditions before designing validation
- Turns red-team behavior into observable defensive objectives
- Reports center on evidence, impact, remediation, and detection improvement

## Typical Usage
```text
Use coff0xc-authorized-assessment to plan a security assessment within the written authorization scope.
Use coff0xc-authorized-assessment to turn red-team exercise steps into defensive validation and report structure.
Use coff0xc-authorized-assessment to draft ROE and control validation for an internal assessment.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
