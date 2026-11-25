---
name: coff0xc-purple-deception
description: "Use when the user requests purple team, ATT&CK, control validation, detection coverage, emulation plan, honeypot/deception, decoy/canary, SOC improvement, detection effectiveness, coverage metrics, or defensive-capability validation. Authorized defensive exercises only. Manual trigger: Use coff0xc-purple-deception."
---

# coff0xc-purple-deception

<!-- skill-id: cs-pdp-e45c2a90 -->

## Quick Rules (read this first for everyday tasks)
> **[Behavior mapping]** First map hypothesized attacker behavior to ATT&CK, log sources, detection logic, control points, and response actions.
> **[Coverage gate]** Output a detection-coverage matrix, gaps, false-positive risk, validation samples, and observation metrics.
> **[Defense first]** Prioritize planning, detection, review, and deception-defense design; real exercise actions must stay within ROE constraints.
> **[Hard boundary]** Confirm first for production exercises, decoy deployment, active adversarial work, third-party targets, and control changes that would affect users.

Follow this section first for ordinary purple-team/deception-defense tasks; expand the full workflow only for real exercise execution or multi-team control validation.

## Capability
Security-operations improvement capability for purple teaming, ATT&CK mapping, detection-coverage validation, and deception defense. It translates attacker-behavior language into defensive capability that is observable, detectable, and improvable.

## What It Can Deliver
- ATT&CK technique mapping and exercise hypotheses
- Detection-coverage matrix, log requirements, and response validation points
- Honeypot/decoy/canary design recommendations
- Exercise reviews, gaps, and improvement backlog

## What Input It Can Take
- Attack-behavior descriptions, detection rules, log sources, SOC feedback
- ATT&CK techniques, exercise plans, alert data, response processes
- Honeypot/decoy requirements, asset inventory, coverage metrics

## Safe-Use Boundaries
- Authorized exercises, defensive validation, and deception-defense design only
- Do not provide unauthorized attack, detection-evasion, persistence, or exfiltration steps
- Real exercises, phishing simulations, decoy deployment, and external interaction must be confirmed first
- Security capabilities are used only for authorized, defensive, detection, hardening, validation, and reporting purposes by default; do not provide unauthorized attack, credential theft, persistence, detection evasion, C2, phishing collection, data exfiltration, or destructive steps.

## Why You Can Trust It
- Every exercise action maps to an observable signal
- Detection effectiveness is validated with data sources, rules, and samples
- Output is an improvement loop, not just a list of attack techniques

## Typical Usage
```text
Use coff0xc-purple-deception to map these attack behaviors into an ATT&CK detection-coverage matrix.
Use coff0xc-purple-deception to design an authorized purple-team exercise and review metrics.
Use coff0xc-purple-deception to plan honeypot/canary coverage and detection validation.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
