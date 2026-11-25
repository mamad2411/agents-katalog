---
name: social-engineering-defense
description: "Covers defending against phishing, vishing, smishing, pretexting and BEC: out-of-band verification for payments and credentials, caller identity verification, reporting culture, and DMARC/SPF/DKIM and MFA backstops. Use when the user asks how to stop CEO fraud or invoice fraud, verify help-desk callers, prevent deepfake voice scams, or harden against social engineering."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Social-engineering defense

Social engineering attacks the human, so the defense is **process + technical
backstops**, not "be more careful." In the AI/deepfake era, content-based
detection ("does this look fake?") is losing: shift defense to **process
enforcement** that holds regardless of how convincing the lure is. This is the
defensive pair to marq's passive people-OSINT tools; for the
program/culture side see `load_skill security-awareness`.

## Threat taxonomy (quick reference)

- **Phishing**: mass email lure → credentials/malware/payment.
- **Spear-phishing / whaling**: targeted, recon-driven, often impersonating an exec.
- **Vishing**: phone/voice, now with cloned-voice deepfakes; 41% of CISOs report a
  deepfake social-engineering incident on an employee audio call, 36% on video, in the past year (Gartner, Sep 2026).
  verify: https://www.gartner.com/en/newsroom/press-releases/2026-09-22-gartner-survey-finds-41-percent-of-cisos-reported-at-least-one-social-engineering-incident-involving-a-deepfake-in-the-past-12-months
- **Smishing**: SMS/iMessage/WhatsApp lures, often "package"/"toll"/"boss needs you."
- **Pretexting**: fabricated scenario to extract info or access (IT support, auditor, new vendor).
- **BEC**: compromised or look-alike business email → fraudulent wire/payroll/invoice change.
- verify (AI-era trends): https://hoxhunt.com/blog/business-email-compromise-statistics

## The core control: out-of-band verification

The single highest-value defense for money and access. Make it mandatory policy,
not judgment:

- **Any payment instruction, new payee, bank-detail change, or payroll change**
  → verify by **calling a number you already have on file** (vendor master /
  internal directory), **never** a number from the email/text/caller. Callback,
  don't call-forward.
- **Credential/MFA/account changes** (reset, device enrollment, "I'm locked out")
  → verify the requester through a second channel before acting.
- **Dual authorization** above a defined threshold; **mandatory waiting period**
  for first-time or changed payees.
- Treat urgency + secrecy + channel-switch as the red flag; that's the BEC
  signature, regardless of how legitimate the message reads.
- verify: https://www.cisa.gov/ (BEC guidance) and FBI IC3 BEC advisories.

## Caller / identity verification (anti-vishing, anti-pretext)

- Help desk: verify identity with something **not publicly knowable and not on
  the badge** (e.g. ticket-driven callback to the number in HR records, manager
  confirmation): never DOB/employee-ID/last-4 alone, all of which leak.
- Establish a **duress / verification phrase** or internal callback protocol for
  high-stakes requests; deepfake voice/video can now pass "it sounded like them."
- Default posture: a real exec under real pressure will tolerate a 2-minute
  verification. Anyone who won't is the tell.
- Vendors/IT impersonation: confirm via the relationship's known contact, not
  contact details supplied in the request.

## Reporting culture (the scalable detector)

- One person reporting protects everyone who already clicked: reporting is the
  human SOC sensor. Make it one-click (**Report Phish** button) and blameless.
- Measure **report rate** and **time-to-report**, not click rate alone
  (`load_skill security-awareness` for the metrics rationale).
- Close the loop: reports feed triage/IR; tell reporters what happened so the
  behavior reinforces. Silence kills reporting.
- Wire reports to the SOC → `load_skill incident-response-leadership` on confirmed compromise.
  Triage a reported message with `load_skill phishing-email-analysis`; a confirmed
  mailbox/BEC takeover goes to `load_skill bec-email-investigation`.

## Technical backstops

- **DMARC at p=reject** (with aligned SPF + DKIM): stops domain spoofing and
  look-alike-from-your-domain. CISA BOD 18-01 mandates p=reject for US federal
  domains; PCI DSS v4.0.1 req. 5.4.1 makes anti-phishing controls (DMARC/SPF/DKIM
  named) mandatory for card-data orgs since Mar 31, 2025. Rollout to p=reject and
  the Gmail/Yahoo/Microsoft bulk-sender rules: `load_skill email-security`.
  Limit: DMARC does **not** stop a _real compromised account_ or display-name
  spoofing from a different domain; layer the rest.
  verify: https://dmarcreport.com/blog/business-email-compromise-bec-scams-take-new-dimension-with-multi-stage-attacks/
- **Phishing-resistant MFA** (FIDO2/passkeys > push > SMS) on all email and
  remote access; it defeats credential phish and limits BEC account takeover.
- **Mail hygiene**: external-sender banners, look-alike/cousin-domain detection,
  newly-registered-domain blocking, attachment sandboxing, link rewriting.
- **Lookalike-domain monitoring + takedown**; register obvious typo-squats.
- **Conditional access / impossible-travel** + session-token protection to catch
  post-phish logins.
- **Least privilege + segmentation** so a single compromised user isn't game-over.

## Decision rule (frontline)

Money or access requested + urgency or channel-switch or secrecy → **stop,
verify out-of-band on a known-good number, before acting.** No exceptions for
seniority. Process beats content detection every time.
