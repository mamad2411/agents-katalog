---
name: soc2
description: "Covers how an AICPA SOC 2 examination is structured: Type I vs Type II, the five Trust Services Criteria, scoping, report anatomy, and the pitfalls that produce qualified opinions. Use when the user asks how to get a SOC 2 report, which criteria to include, Type I vs Type II, how to read a vendor's SOC 2, or audit-window and carve-out questions."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# SOC 2 (AICPA SOC for Service Organizations)

An **attestation** performed by a licensed CPA firm under AICPA **SSAE 18 (AT-C 105/205)**, against **TSP Section 100, 2017 Trust Services Criteria (TSC), with Revised Points of Focus, 2022** (current; the 2022 revision did **not** change the criteria, only added/updated _points of focus_). **Pending:** AICPA exposure drafts of the **2027 TSC + Description Criteria** (28 Oct 2026; comments to 15 Jan 2027) consolidate criteria and add AI points of focus; if adopted, effective for engagements beginning on/after **31 Dec 2027** (early adoption permitted); until then the 2017/2022 set applies. System-description criteria live in **DC Section 200**. SOC 2 is a **report**, not a certificate; there is no "SOC 2 certified". Verify exact current criteria text at the AICPA (purchase): https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services

Don't confuse the reports: **SOC 1** = controls over financial reporting (ICFR); **SOC 2** = the five TSC, restricted-use; **SOC 3** = same as SOC 2 but a public, general-use summary (no control detail).

## Type I vs Type II

- **Type I**: design of controls **at a point in time** ("as of <date>"). Fast, weaker assurance, often a stepping stone.
- **Type II**: design **and operating effectiveness over a period** (the _observation/observation period_, typically 6 to 12 months). This is what customers ask for. The criteria are identical; only the evidence and opinion differ.

## The five Trust Services Criteria

- **Security** (a.k.a. **Common Criteria, CC1 to CC9**): **mandatory in every SOC 2**. Built on the COSO framework's 17 principles plus supplemental criteria (logical/physical access, change mgmt, risk mitigation).
- **Availability**: uptime, capacity, BC/DR, monitoring.
- **Confidentiality**: protection of info designated confidential (NDAs, encryption, retention/disposal).
- **Processing Integrity**: processing is complete, valid, accurate, timely, authorized (transaction-system focused; often skipped).
- **Privacy**: handling of **personal information** against the AICPA privacy criteria (notice, choice, collection, retention, disposal). Distinct from Confidentiality (which covers any confidential data, not just PII).

Each criterion decomposes into sub-criteria, each illustrated by **points of focus**: guidance to consider, **not a checklist and not individually required**. Don't treat a point of focus as a mandatory control.

## Scoping

- Pick **Security + only the categories you can support with evidence.** Adding Availability/Privacy expands testing and exception risk; don't volunteer scope a customer didn't request.
- Define the **system boundary**: infrastructure, software, people, procedures, data for the in-scope service. Carve in/out subservice organizations (see CUECs below).
- **Subservice organizations** (e.g. AWS, GCP): **carve-out** (exclude their controls, common) vs **inclusive** (test them too, rare).

## Report anatomy

1. **Independent auditor's opinion**: unqualified (clean) / qualified / adverse / disclaimer.
2. **Management's assertion**: management's written claim that the description is fair and controls are suitably designed (and, Type II, operating effectively).
3. **System description** (Section III): written by management per DC 200.
4. **Tests of controls & results** (Section IV): the controls, the auditor's tests, and **exceptions/deviations**. Type II only fully populates this.
5. **CUECs (Complementary User Entity Controls)**: controls the report **assumes the customer (you) operates** for the stated controls to work. **Read these**; they're _your_ obligations when relying on a vendor's SOC 2. Parallel: **CSOCs** (complementary subservice org controls).

## Mechanics

- **Exceptions ≠ automatic qualification.** Auditor judges whether deviations breach a criterion; isolated exceptions with remediation can still yield an unqualified opinion. A material/pervasive failure → **qualified or adverse**.
- **Observation-period gaps**: a control implemented mid-period only has evidence from its go-live date; auditors flag the uncovered window. First Type II after a Type I: keep the period short enough to have evidence for the whole window.
- **Restricted use**: SOC 2 reports are for the entity, its customers, and their auditors; not public marketing (use SOC 3 for that).
- **Bridge/gap letter**: covers the interval between report period-end and a customer's reliance date; it's a management representation, **not** auditor assurance.
- **No score, no pass/fail mark**: assurance is the opinion + the exceptions, read together. "We have a SOC 2" is meaningless without _type, categories, period, opinion, and exceptions_.

## Pairs with

- Mapping CC/TSC to ISO 27001 Annex A or NIST CSF to reuse evidence: `load_skill control-mapping`, `load_skill iso27001`, `load_skill nist-csf`.
- Readiness gap assessment before the audit window: `load_skill gap-analysis`.
- Choosing SOC 2 vs ISO 27001 vs others: `load_skill choosing-a-framework`.
