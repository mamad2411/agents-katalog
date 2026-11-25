---
name: security-check
description: Investigate changed code like a red-team reviewer for security bugs, permission gaps, data exposure, and abuse paths. Use for security reviews, permission audits, or when the user mentions security-check, vulnerability, or permission gap.
---

# Security Check

Thoroughly investigate the current feature for security problems and permission gaps. Think like a red-team tester, then suggest or apply focused fixes.

## Kiosk-Specific Threat Model

This is an **unattended public device**. Threats beyond standard web app concerns:
- Physical access: can a member of the public escape the kiosk app?
- Payment tampering: can card data or amounts be intercepted or modified?
- Admin escalation: is the PIN gate bypassable?
- Offline abuse: can orders be created without payment by manipulating local DB state?
- Log exfiltration: are secrets or card data leaking into logs?

## Security Checklist

- **Kiosk escape:** Can the public reach system UI, home screen, or admin panel? Is `PopScope(canPop: false)` in place on Payment/Confirmation? Is `immersiveSticky` enforced?
- **Payment integrity:** Is `PaymentService.charge()` the only SumUp entry point? Is the order written to DB *before* charge? Is the charge result verified before showing confirmation?
- **Constrained operations:** Are all SumUp operations going through the allowed operations list in `sumup-payments.mdc`? Any new MethodChannel calls?
- **Secrets:** Are any secrets, keys, or PINs hardcoded? Do they appear in logs, error messages, or DB records?
- **Input validation:** Are ticket quantities bounded? Are order IDs server-generated UUIDs? Is admin PIN input `obscureText: true`?
- **Logging:** Does any log event contain card data, PAN, CVV, or admin PIN?
- **Network:** Is HTTPS enforced? Is certificate validation disabled anywhere?
- **Authorization:** Does admin panel check PIN before showing any data? Is the PIN comparison constant-time?

## Project Security Rules

Load `.cursor/rules/common/security.mdc` and `.cursor/rules/android-kiosk/sumup-payments.mdc` before judging the diff.

## Workflow

1. Identify changed files and relevant trust boundaries.
2. Read project security rules.
3. Trace realistic abuse paths from the kiosk threat model.
4. Classify findings: Critical, High, Medium, Low.
5. Apply clear, local, behaviour-preserving fixes when in a finish-work workflow.
6. Ask before auth model changes or ambiguous product/security tradeoffs.

## Reporting

Lead with findings ordered by severity. For each: **What** (vulnerable behaviour), **Why** (exploit/exposure risk), **How** (fix or mitigation). If no issues, say so and note residual risk.
