---
name: thai-pdpa
description: Use this skill for any task drafting a Thai PDPA-compliant privacy notice, consent banner, or cookie consent flow. Trigger on "PDPA", "นโยบายความเป็นส่วนตัว", "privacy policy ไทย", "consent banner", "cookie consent", "ขอความยินยอมข้อมูลส่วนบุคคล", "พ.ร.บ.คุ้มครองข้อมูลส่วนบุคคล". If the request is a GDPR-only privacy notice with no Thai users/data involved, use general GDPR patterns instead — do not silently apply Thai PDPA rules to a non-Thai context or vice versa; they overlap but aren't identical.
---

# Thai PDPA (พ.ร.บ.คุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562)

## Overview

A generic privacy notice translated from a GDPR template misses PDPA-specific requirements — most commonly, PDPA requires consent to be opt-in with **no pre-checked boxes**, and consent for non-essential purposes must be separable from the general terms of service. A model without this skill tends to produce a GDPR notice with Thai words substituted in, which reads as compliant but isn't structurally aligned with PDPA's consent mechanics.

**Not legal advice.** This skill drafts structure and language; it does not replace review by a lawyer or the organization's DPO before publishing a real privacy notice or consent flow.

## When to use

- เขียน privacy notice / นโยบายความเป็นส่วนตัว สำหรับเว็บไซต์หรือแอป
- ออกแบบ consent banner / cookie consent ที่ไม่ติ๊ก checkbox ไว้ล่วงหน้า
- ตรวจสอบว่าข้อความขอความยินยอมที่มีอยู่เข้าข่าย dark pattern หรือไม่
- อธิบายสิทธิของเจ้าของข้อมูลส่วนบุคคลภายใต้ PDPA

## When NOT to use

- Pure GDPR compliance work with no Thai data subjects — PDPA and GDPR overlap heavily (both are consent/rights-based frameworks) but have different specific requirements; don't cross-apply without checking
- The task needs a legally binding data processing agreement (DPA) between controller and processor — that's a contract-drafting task requiring a lawyer, not a template-fill task

## Core knowledge

- **PDPA** = พระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562, in full enforcement since 1 June 2022 (after delayed effective dates for earlier compliance deadlines). Regulator is the PDPC (คณะกรรมการคุ้มครองข้อมูลส่วนบุคคล) via its office, the สคส.
- **Valid consent** must be: freely given, specific to each purpose, informed (clear language, not buried in T&Cs), and given by a clear affirmative action. **No pre-ticked checkboxes** — this is the single most commonly violated rule in copy-pasted GDPR templates.
- **Sensitive personal data** (มาตรา 26) — race/ethnicity, political opinion, religious belief, sexual behavior, criminal record, health data, disability, union membership, genetic/biometric data — requires **explicit** consent (a higher bar than general consent) or a specific statutory exemption. Do not lump sensitive-data consent into the same checkbox as general data processing.
- **Legal bases** beyond consent exist (contract performance, legitimate interest, legal obligation, vital interest, public task) — not every data use needs a consent checkbox; a privacy notice should state the correct basis per purpose, not default everything to "consent."
- **Data subject rights**: access, rectification, erasure, restriction of processing, data portability, objection, and withdrawal of consent. Withdrawal must be **as easy as** giving consent — a "call our office to unsubscribe" flow for something that was a one-click opt-in is itself a compliance gap.
- **Cross-border transfer**: transferring personal data outside Thailand requires the destination to have adequate protection standards or additional safeguards (e.g. contractual clauses, consent) — flag this explicitly if the notice covers a foreign-hosted service.
- **Enforcement**: administrative fines, criminal penalties for certain violations involving sensitive data, and civil liability including punitive damages are all possible under PDPA — this is a real regulatory regime, not a symbolic one, which is why the disclaimer in this skill is load-bearing.

## Common mistakes

1. Pre-checking a consent checkbox — the most common and most visible PDPA violation.
2. One all-or-nothing consent checkbox covering multiple unrelated purposes (marketing + analytics + service delivery) instead of granular, purpose-specific consent.
3. Translating a GDPR notice directly instead of checking whether PDPA's specific consent/rights language applies the same way.
4. Treating "consent" as the only legal basis and forcing a checkbox even for processing that's actually necessary for contract performance.
5. Making the "reject" button visually smaller, hidden, or harder to reach than "accept" (a dark pattern that undermines "freely given" consent).
6. Not mentioning cross-border data transfer when the service is hosted or processed outside Thailand.
7. No clear, low-friction path to withdraw consent later.

## Templates

- `templates/privacy-notice-th.md` — full privacy notice structure with the required PDPA sections
- `templates/consent-banner.md` — cookie/consent banner pattern with the anti-patterns to avoid called out explicitly

## Known limitations

- PDPC guidance and enforcement practice continue to evolve since full enforcement began in 2022 — verify current PDPC notifications/guidelines (สคส. ประกาศ) for anything with real compliance stakes, especially sector-specific rules (health data, financial data, children's data).
- This skill does not draft data processing agreements, cross-border transfer contractual clauses, or breach-notification procedures — those need a lawyer.
- Templates here are structural drafting aids. Do not remove the "not legal advice" disclaimer when reusing or editing these files.
