---
name: pci-dss
description: "Covers PCI DSS v4.0.1: the version timeline, CDE scoping rules, SAQ types, the 12 requirements, and the scoping mistakes that fail an assessment. Use when the user handles payment card data, asks which SAQ applies, how to reduce PCI scope, what changed in v4.0, or how to prepare for a QSA assessment."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# PCI DSS v4.0.1

Protects **cardholder data**. Contractual (card brands), not law, but enforced hard. Everything depends on **scope**: PCI applies to the **CDE** (cardholder data environment): every system that stores, processes, or transmits **account data**, _plus_ systems connected to or that could impact the security of those.

Canonical source: PCI SSC `PCI DSS v4.0 / v4.0.1` document library, `pcisecuritystandards.org`. Web-fetch for exact requirement text and the current SAQ instructions.

## Version timeline (get this right)

- **v4.0** released Mar 2022; **v3.2.1 retired 31 Mar 2024**.
- **v4.0.1** (minor clarifying revision) published Jun 2024; still current (Nov 2026). PCI SSC ran an RFC on v4.0.1 (3 Jun to 20 Jul 2026) to plan a possible revision; no successor draft is published.
- A large block of **future-dated requirements became mandatory 31 Mar 2025** (e.g. anti-phishing, automated log review, client-side script integrity 6.4.3 / 11.6.1, MFA refinements). After that date they are **required, not best-practice**; verify the exact list against the current standard.
- New in v4.0: the **Customized Approach** (meet the objective your own way, with a **Targeted Risk Analysis** + assessor validation) alongside the traditional **Defined Approach**.

## Account data: what's in scope

- **Cardholder Data (CHD)**: PAN, cardholder name, expiry, service code. PAN is the trigger; if PAN is stored you must protect it (render unreadable via truncation/hashing/encryption).
- **Sensitive Authentication Data (SAD)**: full track, CAV2/CVC2/CVV2/CID, PIN/PIN block. **SAD must NOT be stored after authorization**, even encrypted. This is the first rule.

## SAQ types (self-assessment questionnaires, for eligible merchants)

Validation level depends on how you handle cards. Pick wrong and you under/over-scope:

- **SAQ A**: fully outsourced e-commerce/MOTO, _no_ CHD touches your systems (e.g. fully hosted/redirect or iframe). Smallest scope. Since the **Jan 2025 SAQ A revision**, 6.4.3/11.6.1 (and 12.3.1) are **no longer SAQ A line items**, replaced by an **eligibility criterion**: confirm your site isn't susceptible to script attacks that could affect the e-commerce system (iframe pages: 6.4.3/11.6.1-style techniques, or your PSP's confirmation its embed includes script protection). The requirements stay in the standard (A-EP, D, RoC).
- **SAQ A-EP**: e-commerce that _partially_ outsources but your site delivers payment-page elements (direct-post / JS that touches the payment form). Much larger than A, commonly confused with A.
- **SAQ B**: imprint machines / standalone dial-out terminals, no electronic storage.
- **SAQ B-IP**: standalone IP-connected PTS terminals, no storage.
- **SAQ C-VT**: virtual terminal, manual entry, one device, no storage.
- **SAQ C**: payment app on an internet-connected system, no storage.
- **SAQ P2PE**: validated P2PE solution, hardware terminals only.
- **SAQ D**: everyone else (merchants that store CHD or don't fit above, **and all service providers**, D-SP). Effectively the full standard.

Higher transaction volumes (Level 1) require a **QSA-led RoC** (Report on Compliance), not an SAQ; verify brand thresholds.

## The 12 requirements (6 goals)

1. Install/maintain **network security controls** (firewalls/segmentation)
2. Apply **secure configurations** (no vendor defaults)
3. **Protect stored account data**
4. **Strong cryptography in transit** over open/public networks
5. Protect systems from **malicious software**
6. **Secure systems & software** (patching, secure dev, 6.4.3 script integrity)
7. **Restrict access by need-to-know**
8. **Identify users & authenticate** (incl. MFA)
9. **Restrict physical access**
10. **Log and monitor** all access
11. **Test security regularly** (scans, pentest, 11.6.1 payment-page tamper detection)
12. **Support with policy & programs** (incl. TPSP/vendor management)

## Scoping mistakes that fail an assessment

- **Flat network**: no segmentation means _everything_ is in the CDE. Segment (and prove it with segmentation pen-testing) to shrink scope.
- **Forgetting connected/security-impacting systems**: AD, jump hosts, monitoring, NTP, DNS, hypervisors that _touch_ the CDE are in scope even if they never see a PAN.
- **Storing SAD**: caching CVV in logs, app debug, or a payment gateway response is an automatic fail.
- **PAN in unexpected places**: logs, error dumps, email, screenshots, backups, call recordings, dev/test data.
- **Claiming SAQ A while delivering payment-page code**: that's A-EP. Redirect/iframe-to-PSP = A; your-JS-touches-the-card-field = A-EP.
- **Out-of-date third-party (TPSP) responsibilities**: you inherit their PCI status only with a documented responsibility matrix.

## Pairs with

- Network-segmentation validation testing is done by the assessor/pentester (not marq).
- Gap assessment / control mapping against your other frameworks: `load_skill gap-analysis`, `load_skill control-mapping`.
