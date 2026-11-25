---
name: legal-contractual
description: Covers the security-relevant contract surface, including DPAs, the clauses that matter (audit rights, breach notice, liability, subprocessors), cyber insurance, and regulatory vs contractual breach duties. Practitioner orientation, not legal advice. Use when the user is reviewing a vendor or customer contract, data processing agreement, security addendum or cyber insurance policy, or asks who must be notified of a breach under contract.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Legal & contractual surface

> **Not legal advice.** This is practitioner orientation so a security person can read a contract intelligently, flag the security-relevant clauses, and brief counsel. **Counsel/privacy/procurement own the language and the sign-off**: your job is to know what to look for and what it means operationally.

## The documents

- **MSA / main agreement**: liability, indemnity, term, governing law.
- **DPA (Data Processing Agreement)**: required when a processor handles personal data (GDPR Art. 28). Defines controller/processor roles, purpose, subprocessors, SCCs for cross-border transfer, deletion-on-exit, breach notice.
- **Security Addendum / Exhibit**: the actual security controls the vendor commits to (encryption, MFA, pen-test cadence, SDLC, certs). This is the technically enforceable part; read it, don't accept "industry standard."
- **SLA**: uptime + the _security_ SLAs (breach notice clock, vuln-remediation timelines).

## Clauses that matter (and what to push for)

- **Breach notification SLA**: the number, in hours, and the trigger. Push for **≤72h, ideally 24 to 48h**, from _discovery_ (not "confirmation"). Vague "without undue delay" = unbounded; pin it. Must be tight enough to let _you_ meet _your_ regulator clock (GDPR 72h, `load_skill privacy-eu`; NIS2 24h early-warning / DORA hours, `load_skill nis2-dora`). Define what's in the notice + a named contact path.
- **Audit rights**: right to audit / request evidence / receive SOC 2 + pen-test summaries on a cadence. Watch for "once per year, 90 days' notice, at your cost" defanging it. Right to audit _after a security incident_ regardless of schedule is the one that matters.
- **Right-to-pentest**: explicit permission to security-test the service (or to receive the vendor's recent test). SaaS often forbids testing without written consent; get it in writing or you can't validate. Define scope + safe harbor.
- **Liability caps & carve-outs**: caps often = 12 months' fees, which won't cover a real breach. Push **data-breach / confidentiality / IP-infringement** into a **super-cap or uncapped carve-out**. The cap is where the money is; read it with counsel. Watch exclusion of "consequential damages" swallowing breach costs.
- **Subprocessors / 4th parties**: list + **advance notice and a right to object** to new ones. Flow-down: subprocessors bound to equivalent terms. Concentration risk (everyone on one cloud): see `load_skill third-party-risk`.
- **Data residency / localization**: where data is stored/processed; transfer mechanism (SCCs, adequacy). Matters for GDPR, sector rules, and gov work.
- **Deletion / return on exit**: data returned or destroyed within N days of termination, with **certification**. Otherwise your data lives on indefinitely.
- **Security-control commitments**: encryption at rest/in transit, MFA, least privilege, logging, named certs maintained for the term. Make them _obligations_, not aspirations.

## Cyber insurance

Risk-transfer for residual risk; underwriting now effectively mandates a security baseline. **Read the conditions as a control checklist**: the policy tells you what "good" looks like to an insurer.

- **Covers (first-party)**: incident response, forensics, breach notification costs, business interruption, data restoration, **sometimes** ransom (shrinking). **Third-party**: liability to affected parties, regulatory defense/fines where insurable.
- **Underwriting demands (2025/26, hardened)**: **MFA everywhere** (phishing-resistant for privileged/remote), **EDR on all endpoints** (basic AV insufficient, ~88% of underwriters require EDR), **immutable/offline backups** (~82% of policies, up from ~45% in 2022), PAM, network segmentation, 24/7 monitoring, tested IR plan, vendor due-diligence. verify: https://www.secureait.com/2025/12/09/cyber-insurance-requirements-are-getting-tougher-what-every-organization-must-know-in-2026/
- **Common exclusions / denial traps**: **war/nation-state** exclusion (Lloyd's clauses), **social engineering / funds-transfer fraud** needs a separate endorsement, ransom payment may be excluded, **failure-to-maintain-stated-controls voids the claim**. ~37% of claims see a coverage dispute over a security gap (the one un-patched laptop, the one account without MFA). verify: https://www.sentinelone.com/cybersecurity-101/cybersecurity/cyber-insurance-statistics/
- **Operational rule**: your application answers become **warranties**: if you attest MFA-everywhere and one box lacks it, the payout can be voided. Answer truthfully; close the gap before signing. Keep evidence (`load_skill grc-automation`) to prove controls were live at incident time.

## Regulatory vs. contractual breach obligations (don't conflate)

- **Regulatory** = duty to a **regulator/data subjects** by law on a statutory clock (GDPR 72h, `load_skill privacy-eu`; NIS2 24/72h/1mo + DORA hours, `load_skill nis2-dora`; US state AG laws + sector rules, `load_skill privacy-us`, `us-sectoral-regs`). Non-compliance → fines.
- **Contractual** = duty to a **counterparty** by the contract's notice SLA. Non-compliance → breach-of-contract liability, not a regulatory fine.
- **One incident fires both, on different clocks, to different audiences.** Your IR runbook needs a notification matrix: which regulators + which customers/partners, each with its trigger and deadline. The contractual clock is often _shorter_ than the regulatory one; meet the tightest.
- **Practitioner stance**: pre-map obligations _before_ an incident. Mid-incident is the wrong time to read 40 DPAs to find notice deadlines. Counsel decides _what/whether_ to notify; you supply the facts and the clock.

## Pairs with

- Scoring/onboarding the vendor behind the contract: `load_skill third-party-risk`.
- The law, triggers, and breach clocks in detail: `load_skill privacy-eu`, `nis2-dora`, `privacy-us`.
- Evidence to prove control state for insurer/auditor: `load_skill grc-automation`.
