---
name: soc2-review
description: Review and assess a SOC 2 Type 1 or Type 2 report — either a vendor's report for procurement diligence, or your own report to prepare for customer reviews. Calibrates expectations against the reviewer's industry, size, stage, and well-known procurement standards. Use whenever the user shares a SOC 2 report (PDF, attestation letter, bridge letter) along with any context — "review this vendor's SOC 2," "how would a bank evaluate our SOC 2," "review our own SOC 2 before we send it to prospects," or "diligence this vendor's SOC 2 for me." Also trigger for related requests where a SOC 2 is the primary artifact — gap analysis, peer-cohort comparison, readiness assessment, drafting follow-up questions, or producing a write-up to share with stakeholders. Produces a structured markdown report with risk-rated findings, a recommendation, and actionable next steps.
allowed-tools: Read Glob Grep
---

# SOC 2 Review

A skill for assessing a SOC 2 report — either a vendor's or your own — in the context of who the company actually is and who will be reviewing it. Surfaces gaps that matter, calibrated to the reviewer's perspective.

## Why this skill exists

Most SOC 2 reviews fail in one of two directions: either they rubber-stamp the report ("it has a SOC 2, ship it") or they hold a 30-person startup to the standards of a Fortune 500 enterprise and flag everything as a problem. Neither is useful.

A good SOC 2 review answers a different question: **given who this company actually is and who's evaluating the report, does their security program look like what the reviewer would expect — and where it doesn't, does that matter?**

This skill operates in two modes:

- **Vendor diligence** — you're evaluating a vendor's SOC 2 to decide whether to proceed with them. The classic procurement use case.
- **Self-review readiness** — you're assessing your own SOC 2 through the lens of a target reviewer (e.g., Fortune 500 financial services, hospital systems, state government) to understand what they'd flag and what to fix before sharing.

**Confidentiality.** SOC 2 reports are typically NDA-protected. This skill operates on local files only and produces a local markdown report; it does not transmit report contents anywhere. Don't paste report contents into third-party tools or chat surfaces outside this session.

## Inputs

The user provides:

1. **One or more SOC 2 documents** — typically PDFs. The primary artifact is a Type 1 or Type 2 report. Vendors commonly share several documents together; handle them as follows:
    - **Most recent full Type 2** → the primary artifact; everything in Step 2 is extracted from this.
    - **Bridge letter / attestation letter** alongside a Type 2 → extends the coverage period; any qualifications it raises become findings.
    - **Bridge letter alone, no full Type 2** → ask once whether the full Type 2 is available, then **proceed with shallow analysis** — flag the limitation prominently in the report header, the Gaps section, and the Recommendation. Conclusions are necessarily provisional. Don't block on a missing full report; partial output beats none, as long as the limitation is honest.
    - **Prior year's report** → use it as the source of truth for repeat-exception detection; note any exception that recurs from the prior year as a stronger finding.

    Note all documents received in the report header.

2. **Review mode and reviewer perspective** — see Step 0.5 below for the structured intake.

3. **A company context blurb** — describes the company being reviewed (the vendor in vendor mode, or the user's own company in self-review mode) across four required dimensions: **company size/stage**, **industry/data sensitivity**, **customer base**, and a fourth dimension that varies by mode:
    - Vendor mode: **intended use case** — what data the vendor will hold, how critical they are to your operations.
    - Self-review mode: **most sensitive data / highest-risk use case** — what's the most sensitive thing your customers trust you with?

### Collecting inputs when missing or sparse

If any required input is missing, run a structured intake using `AskUserQuestion` rather than a free-form ask. Skip questions for dimensions the user already supplied. Keep the option labels short — the tool surfaces them as buttons.

**Step 1 — Review mode.** Parse the user's initial message for signals before asking. Phrases like "our SOC 2," "our report," "how would X evaluate us," "readiness," "self-assessment" indicate self-review mode. Phrases like "vendor," "evaluating," "diligence," "should we proceed" indicate vendor mode. If ambiguous, ask:

- Our own SOC 2 (preparing for customer reviews)
- A vendor's SOC 2 (procurement diligence)

**Step 2 — Reviewer perspective.** This determines the evaluation bar. In self-review mode it's required; in vendor mode it's optional (refines the bar upward if the user's own organization has elevated standards — skip if standard procurement).

Self-review mode options:

- Enterprise SaaS procurement (Fortune 500 tech)
- Financial services (banks, insurance, asset managers — e.g. JP Morgan, BNY Mellon)
- Healthcare / hospital systems
- Federal government / FedRAMP
- State or local government
- Heavy industry, manufacturing, or construction
- Mid-market commercial buyers
- General enterprise — no specific vertical

Vendor mode options (framed as "Does your organization's industry raise the bar beyond standard vendor diligence?"):

- Standard enterprise procurement
- We're in financial services
- We're in healthcare
- We're a federal government agency
- We're in state or local government
- We're in heavy industry, manufacturing, or construction
- No special requirements

The user can also provide a free-text perspective for any case not covered by the options (e.g., "mid-stage private healthcare network," "Series C edtech selling to school districts").

**Step 3 — Company context.** Collect the four dimensions. The framing adapts by mode:

Vendor mode:

- **Company size / stage:** 1–15 (pre-seed/seed) · 15–50 (Series A) · 50–200 (Series B) · 200–1000 (Series C+/late-stage) · 1000+ (public/Fortune-1000) · I'm not sure
- **Industry / data sensitivity:** B2B SaaS (no special sensitivity) · Healthcare / PHI · Financial services / PCI · Critical infra or security tooling · Government / public sector · State or local government · Heavy industry / manufacturing / construction · B2C consumer
- **Customer base:** Primarily SMB · Mid-market · Enterprise · Regulated industries (banks, hospitals, gov)
- **Intended use case:** Free text — "What will this vendor hold or do for you, and how critical are they to your operations?"

Self-review mode:

- **Company size / stage:** Same options as above
- **Industry / data sensitivity:** Same options as above
- **Customer base:** Same options as above
- **Most sensitive data / highest-risk use case:** Free text — "What's the most sensitive data or highest-risk use case your customers trust you with?"

**Step 4 — Echo-back confirmation.** After collecting answers, echo back the assembled profile in one or two sentences so the user can correct before proceeding.

- Vendor mode: "Treating this vendor as a Series B health-tech vendor selling to hospitals, calibrating against that bar."
- Vendor mode with reviewer perspective: "Treating this vendor as a Series B health-tech vendor selling to hospitals. Your own standards as a financial services organization raise the bar on change management and processing integrity."
- Self-review mode: "Evaluating your SOC 2 as a Series B health-tech vendor selling to hospitals, through the lens of a Fortune 500 financial services reviewer. This raises the bar on change management, processing integrity, vendor risk management, and segregation of duties beyond what your typical customer base demands."

A reasonable minimum to proceed: review mode, company size/stage, industry, customer base, and (in self-review mode) reviewer perspective. Without these the analysis becomes generic and loses most of its value.

## Workflow

### Step 0: Confirm the document is a reviewable SOC 2

Before reading deeply, confirm the document is what we can actually work with. Read the first 2–3 pages and check:

- **Is it a SOC 2 at all?** Look for telltale strings: "Independent service auditor's report," "SSAE-18" (or "SSAE No. 18"), "Trust Services Criteria," "AICPA," "Service Organization Control." If absent, the user has shared something else — most likely an ISO 27001 cert, a pen test report, a vendor security questionnaire, or a customer-trust whitepaper. Stop and tell the user what they appear to have shared and that this skill needs a SOC 2 specifically. (If it's an ISO 27001 cert, say so plainly — there isn't an ISO skill yet, but pretending the SOC 2 review will work is worse.)

- **Is it a SOC 2 Type 1, Type 2, or something else?** Type 3 reports and "executive summary" / prospect-facing condensed versions exist but lack the Section IV control listing and exceptions that this skill depends on. If the document is dramatically shorter than typical (under ~30 pages), labeled "executive summary" or "for prospects," or lacks Section IV, decline gracefully — explain the skill needs a full Type 1 or Type 2 to produce useful findings.

- **Is the PDF text-extractable?** Some scanned SOC 2 PDFs have no embedded text layer. If the first read returns empty or near-empty content for pages that visually contain text, the PDF is image-only. Stop and tell the user: "This PDF appears to be image-only with no text layer. Run it through OCR (e.g., `ocrmypdf input.pdf output.pdf`) and re-share." Don't try to produce a report from no content.

If the document passes all three checks, proceed to Step 0.5.

### Step 0.5: Determine review mode and reviewer perspective

Run the structured intake from the "Collecting inputs" section above — review mode, reviewer perspective, company context, echo-back confirmation. This must be settled before Step 1 because the reviewer perspective affects what you look for and how you frame findings.

### Step 1: Read the report

Read Sections I (auditor opinion), III (system description), and IV (controls + exceptions) **in full** — these carry the signal. Skim Section II (management assertion — boilerplate unless unusually qualified). Read Section V (other information) for context only — it's unaudited; don't draw findings from it.

**Reading the PDF.** Claude Code's `Read` tool requires a `pages` parameter for PDFs over 10 pages. Read the table of contents first (`pages: "1-3"`), use it to locate Sections I, III, and IV, then read each in 10–20 page chunks. Don't try to read the whole PDF in one call — it'll fail. A typical pattern:

```
Read(file_path, pages: "1-3")     # ToC + opinion letter
Read(file_path, pages: "4-8")     # finish opinion + management assertion
Read(file_path, pages: "9-30")    # system description (Section III)
Read(file_path, pages: "31-50")   # controls + exceptions (Section IV)
... continue until Section IV is fully covered
```

The reference docs live alongside this SKILL.md; resolve their absolute path so reads work in both Claude Code and Codex:

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${SKILL_DIR}}"
```

If unfamiliar with SOC 2 report structure, section layout, or how to read exceptions, read `$SKILL_DIR/references/soc2-fundamentals.md` for a primer. **Do NOT load** `soc2-fundamentals.md` if you already know these things — it's a primer, not a required reference. **Do NOT load** `peer-cohort-heuristics.md` or `report-template.md` at this step — they're needed in Steps 3 and 5 respectively.

### Step 2: Extract structured findings

Pull the following from the report. Capture page references using the format `Section IV.5, p. 47` when the section is useful, or `p. 47` when section context isn't needed. Consistent format makes the report's evidence citations skimmable and lets the reader jump to the source quickly.

- **Auditor and opinion**: Who performed the audit. What kind of opinion (unqualified is the goal; qualified or adverse are red flags).
- **Report type and currency**: Type 1 or Type 2. For Type 2, extract the period covered and compute freshness (today's date minus the period end date). This is a single finding axis — do not generate separate findings for the testing window length and for staleness, since both describe how current the audit evidence is. Use this severity table:

    | Situation                                                                | Severity                                     |
    | ------------------------------------------------------------------------ | -------------------------------------------- |
    | First-year Type 2 with a 3–6 month period                                | No finding — normal for a first-year audit   |
    | Non-first-year Type 2 with period under 12 months (short testing window) | Medium                                       |
    | Period ended 12–18 months ago (stale report)                             | Medium                                       |
    | Period ended more than 18 months ago                                     | High                                         |
    | Coverage gap from the prior report's end date                            | Medium (or High if the gap exceeds 6 months) |

    When both a short window and staleness apply, report the single higher severity, not two findings. In vendor mode, if the report is stale (period ended >12 months ago), ask the user whether a current report is available before going deep on the rest of the extraction. In self-review mode, flag it as: "Your report's coverage period ended [N] months ago. A [reviewer type] reviewer will flag this immediately — prioritize getting your next audit period completed before sharing."

- **Trust Service Criteria (TSC) in scope**: Security is mandatory; Availability, Confidentiality, Processing Integrity, and Privacy are optional. Which the vendor included signals what they care about and what their customers demanded.
- **Additional frameworks attested**: Some SOC 2 reports include or reference additional criteria — HIPAA, HITRUST, NIST CSF mappings, PCI DSS additional criteria, ISO 27001 cross-references. Capture these; they're candidate **Strengths for stage** (program-maturity signal beyond what SOC 2 alone provides).
- **System scope**: What products/services/environments are in scope. Watch for narrow scoping (e.g., only the marketing site, not the actual product).
- **Subservice organizations**: AWS, GCP, Azure, datacenters, payment processors, etc. — and whether they're carved-out (their controls are not tested here, you rely on their own SOC 2) or inclusive (tested as part of this audit). Carve-out is normal; the question is whether the vendor monitors those subservice orgs.
- **Complementary User Entity Controls (CUECs)**: What the company expects _customers_ to do. Read these — they often shift real responsibility to the customer.
- **Exceptions / deviations**: The actual control failures the auditor found during testing. These are gold. Note severity, whether management responded, and whether remediation is described. **Cross-check against the prior year's report** if one was provided — repeat exceptions are a stronger finding than first-time ones.
- **Control inventory**: A high-level catalogue of what controls exist, organized by domain (access control, change management, incident response, vendor management, BCDR, HR/personnel, monitoring, encryption, vulnerability management, etc.).

### Step 3: Build the expectation profile

Two inputs feed the expectation bar:

**MANDATORY — READ**: Load `$SKILL_DIR/references/peer-cohort-heuristics.md` before building the expectation profile. The stage-based expectations, industry adjustments, customer-base adjustments, and reviewer perspective overlay mapping table live there. Do NOT attempt to calibrate from memory. **Do NOT load** `report-template.md` or `soc2-fundamentals.md` at this step.

1. **Subject company profile** — from the company context blurb, using the stage/industry/customer-base heuristics in `peer-cohort-heuristics.md`. This is the baseline.

2. **Reviewer perspective overlay** — if the reviewer perspective implies a higher bar than the subject's own customer base would produce, raise the bar to match. The mapping is documented in the "Applying a reviewer perspective overlay" section of `peer-cohort-heuristics.md`. Use those heuristics — don't make up your own bar.

A few principles worth holding onto:

- **Stage governs the operational maturity bar more than size.** A 50-person Series B will typically have more formal processes than a 50-person bootstrapped company, because they've raised institutional money and signed enterprise contracts that demanded it.
- **Industry governs the regulatory floor.** A healthtech vendor needs HIPAA-aligned controls regardless of size. A fintech vendor handling card data needs PCI scope handled. A vendor selling into financial services needs to look defensible to bank security teams.
- **Customer base governs the maturity ceiling.** A vendor selling to Fortune 500 has been through enough security questionnaires that gaps are unusual; a vendor selling to small restaurants has probably never been pressed on these things and gaps are expected.
- **The reviewer perspective overlay never lowers the bar.** It can only raise it. If the subject company's own profile already produces a higher bar than the reviewer perspective, the subject's bar stands.

In self-review mode, frame the profile as: "Your company profile is [X]. We're evaluating through the lens of [reviewer type], which raises the bar on [specific domains]."

In vendor mode, frame as: "Treating this vendor as [X], calibrating against that bar." If a reviewer perspective was provided, add: "Your own standards as [reviewer type] raise the bar on [specific domains]."

### Step 4: Compare and rate findings

Walk through the extracted findings against the expectation profile. For each gap or notable item, classify:

- **Critical** — a control failure or absence that's unusual even for this peer cohort and creates real risk for the use case or would be a serious concern for the target reviewer. Examples: production access without MFA at a vendor selling to enterprises; no encryption at rest for a company storing PII; an adverse or qualified auditor opinion; multiple repeat exceptions from prior years.
- **High** — a meaningful gap relative to peers, or a single significant exception with weak remediation. Examples: no formal incident response plan at a 100-person company; access reviews not performed; vendor management process is informal at a company that depends heavily on subprocessors.
- **Medium** — gap exists but is common at this stage, or is mitigated by other controls. Worth raising in follow-up but not a blocker. Examples: no formal threat modeling program at a 30-person startup; SOC monitoring is business-hours only at a non-24/7-SLA product.
- **Low / Observation** — worth noting for completeness but not a real concern at this stage. Examples: no dedicated CISO at a 25-person company; no formal red team exercises at Series A.
- **Strength** — call these out. Things the company does well _for their stage_ are signal too. A 40-person company with formal vendor risk management, working access reviews, and clean exception history is doing better than peers. Additional frameworks attested in the report (ISO 27001, HIPAA, HITRUST, NIST CSF, PCI DSS additional criteria) are program-maturity signal and belong here.

Avoid the trap of importing enterprise expectations wholesale. If you find yourself flagging "no 24/7 SOC" or "no dedicated security team of 10+" at a Series A, that's enterprise-grade reasoning misapplied. Fix it. The exception: if the reviewer perspective explicitly demands it (e.g., a Fortune 500 financial services reviewer may require 24/7 monitoring even from a Series A vendor — flag it, but note that it's the reviewer's elevated bar, not a peer-cohort gap).

**Framing "why it matters" by mode:**

- Vendor mode: "Why it matters for your use case" — tie to the user's intended use case.
- Self-review mode: "Why a [reviewer type] reviewer would flag this" — explain what the target reviewer's procurement or security team would think and why this would be a concern in their framework.

**CUECs deserve their own rating pass.** Walk through the CUECs from Step 2 with the same severity lens. A CUEC that shifts material responsibility — "customer is responsible for backing up exported data," "customer is responsible for monitoring authentication anomalies," "customer is responsible for retaining audit logs beyond 30 days" — should generate a Medium or High **finding**, not just a "CUECs that matter" bullet, when the user (vendor mode) is not realistically going to operate that control, or when the target reviewer (self-review mode) would find the shift objectionable.

**Deduplicate before finalizing.** Before moving to the report, scan your findings list for overlapping entries. If two findings share the same root cause, merge them into one finding at the higher severity. The canonical example: a short testing window and a stale report period are both symptoms of the audit evidence not being current — that's one "Report currency" finding (already handled in Step 2), not two. Other common overlaps: an exception in access reviews and an absence of a formal access review process; a weak management response and the underlying exception it responds to. One finding per root cause; cite all evidence.

**Common-gap checklist.** After rating findings, verify that the following high-signal controls appear in the report — or appear as findings if absent. These are the gaps most commonly missed because the report simply doesn't mention a control and the reviewer doesn't notice the absence. Cross-reference the company's stage from the peer-cohort heuristics to decide whether each item is expected.

- **Annual third-party penetration test** — expected from Series A onward. If the report describes no pen test and the company is post-Series-A, this is a finding (typically High for Series B+, Medium for Series A).
- **Formal incident response plan** — expected from Series A onward. Absence at a post-Series-A company is a finding (High if the company stores sensitive data or serves enterprise customers).
- **Access reviews completing on cadence** — expected from Series A onward. Look for evidence of reviews actually running, not just a policy that says they should. Absence or non-completion is a finding.
- **Encryption at rest for customer data** — expected at all stages when the company stores customer data. Absence is a finding (High for any company handling PII, PHI, or financial data; Medium otherwise).
- **Vendor / subservice organization management** — expected from Series B onward. A company with carved-out subservice orgs but no described process for monitoring those orgs' SOC 2s is a finding.

If any item above is absent from the report and expected for the company's stage per the peer-cohort heuristics, ensure it appears as a finding at the appropriate severity. If the report genuinely addresses all of them, move on — this checklist is a safety net, not a padding exercise.

### Step 5: Generate the report

**MANDATORY — READ**: Load `$SKILL_DIR/references/report-template.md` before generating the report. **Do NOT load** `peer-cohort-heuristics.md` again if already read in Step 3.

The template supports two modes via `<!-- MODE -->` markers — use only the sections matching the active review mode plus `<!-- MODE: both -->` sections. The `<!-- MODE -->` markers themselves should not appear in the final output.

The report is markdown, designed to be readable and skimmable — pasted into Notion or attached to a vendor risk ticket.

Do not include findings the company handled well unless they're notable strengths for their stage. The report should be honest, calibrated, and actionable — not a comprehensive control-by-control audit (that's what the SOC 2 itself is).

**CUECs in the report.** Material CUECs you rated as findings in Step 4 belong in **Findings** under their assigned severity. The separate **CUECs that matter** report section is the curated list of customer-side controls verbatim from the report — reference for whoever owns the relationship — not a duplicate of the findings.

**Recommendation rubric (vendor mode).** End the report with one of: Proceed / Proceed with conditions / Hold pending follow-up / Do not proceed. The recommendation is a judgment call, not a calculation, but the following is a reasonable default starting point — deviate when use case demands it:

| Severity tally                               | Default recommendation                                                                                                                                         |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Any Critical                                 | Hold pending follow-up — or **Do not proceed** if the Critical is structural (adverse opinion, scope mismatch, repeat criticals, RLS-equivalent base failures) |
| 0 Critical, 2+ High                          | Proceed with conditions                                                                                                                                        |
| 0 Critical, 0–1 High, several Medium         | Proceed with conditions or Proceed, depending on use case                                                                                                      |
| 0 Critical, 0 High, mostly Low / Observation | Proceed                                                                                                                                                        |

The use case can promote or demote the default by one level. A single Medium can warrant a Hold if the user is putting their entire customer database in this vendor's hands. A single Critical can warrant Conditions if the user's exposure is trivial. State the reasoning explicitly when deviating.

**Readiness rubric (self-review mode).** End the report with one of: Ready / Ready with caveats / Address before sharing / Significant gaps. The rubric and detailed definitions are in the "Self-review recommendation rubric" section of `report-template.md`.

**Follow-up questions (vendor mode).** Phrase them specifically — not "tell us about your incident response process" but "your SOC 2 doesn't describe a formal incident response runbook; can you share your IR plan and details on the last tabletop exercise?" Aim for 5–10. More than that and the vendor will treat it as a questionnaire rather than a focused diligence conversation.

**Remediation priorities + likely reviewer questions (self-review mode).** Instead of follow-up questions, produce two sections:

1. **Remediation priorities** — ordered by impact on readiness, each tied to a finding, with a rough effort estimate (quick win / quarter-level project / major initiative).
2. **Likely reviewer questions** — what the target reviewer would ask, with preparation guidance for each.

### Step 6: Save the file and hand off

**Company slug.** Lowercase ASCII alphanumerics + hyphens, derived from the company's primary name, max 40 chars. Examples: "Acme Corp." → `acme-corp`; "Datadog, Inc." → `datadog`; "Health-Stream Analytics LLC" → `health-stream-analytics`.

**Reviewer slug (self-review mode only).** Short slug for the reviewer perspective. Examples: "Fortune 500 financial services" → `fortune500-finserv`; "state government" → `state-gov`; "healthcare systems" → `healthcare`.

**Filename.**

- Vendor mode: `soc2-review-<company-slug>-<YYYY-MM-DD>-<HHMM>.md`
- Self-review mode: `soc2-readiness-<company-slug>-<reviewer-slug>-<YYYY-MM-DD>-<HHMM>.md`

Saved to the working directory. Always include time, so same-day re-reviews (vendor sends an updated report, or re-run with a different reviewer perspective) don't overwrite the original.

**In-chat handoff.** Don't paste the entire report inline. Give the user the verdict at a glance, then point at the file.

Vendor mode:

```
SOC 2 review for [Company] saved to: ./soc2-review-<slug>-<date>-<time>.md

- Critical: [N]  High: [N]  Medium: [N]  Low: [N]  Strengths: [N]
- **Recommendation: [Proceed / Conditions / Hold / Do not proceed]**
- [One-line headline — the single most important thing the user should know.]
```

Self-review mode:

```
SOC 2 readiness assessment saved to: ./soc2-readiness-<slug>-<reviewer>-<date>-<time>.md

- Critical: [N]  High: [N]  Medium: [N]  Low: [N]  Strengths: [N]
- **Readiness: [Ready / Ready with caveats / Address before sharing / Significant gaps]**
- [One-line headline — e.g., "A Fortune 500 bank would likely hold pending the missing IR tabletop and 24/7 monitoring gap."]
```

Three lines plus the file path. The user gets the verdict instantly and reads the file for detail.

## Output structure

The report follows this fixed structure (full template in `references/report-template.md`):

1. **Header** — company name, report type/period, auditor, review mode, reviewer perspective (self-review mode), date of review
2. **Executive summary** — 3–5 bullets capturing the headline; recommendation or readiness assessment; severity tally
3. **Company profile** — the peer cohort and reviewer perspective being used as the comparison baseline
4. **SOC 2 report at a glance** — opinion, TSC in scope, scope of system, subservice orgs, exception count
5. **Findings** — grouped by severity, each with: finding, peer expectation, why it matters (mode-adapted framing), evidence/page reference
6. **Strengths for stage** — what's notably good
7. **CUECs that matter** — the customer-side controls, framed per mode
8. **Recommendation** (vendor mode) or **Readiness assessment** (self-review mode) — with reasoning
9. **Follow-up questions for the vendor** (vendor mode) or **Remediation priorities + Likely reviewer questions** (self-review mode)

## Critical anti-patterns

- **NEVER rate an absent control as a confirmed failure.** "Report doesn't describe X" ≠ "auditor found X failed." These are different findings with different severity. An absence is a gap to note; a failure is an exception the auditor documented.
- **NEVER import enterprise expectations wholesale.** Flagging "no 24/7 SOC" or "no dedicated security team of 10+" at a Series A is a reviewer calibration failure, not a finding — unless the reviewer perspective explicitly demands it and you frame it as the reviewer's elevated bar, not a peer-cohort gap.
- **NEVER draw findings from Section V.** It's unaudited management-supplied content. Useful for understanding the vendor's narrative; not evidence of control effectiveness or failure.
- **NEVER treat carve-out subservice orgs as a finding by itself.** Carve-out is the standard model. The finding is whether the company monitors the subservice org's SOC 2 — not that they use a carve-out approach.
- **NEVER let the reviewer perspective reflexively escalate severity.** A Fortune 500 bank reviewing a Series A vendor has higher expectations, but they also understand what's stage-appropriate. Name the gap, explain why the reviewer cares, note it's the reviewer's elevated bar — don't auto-promote every missing control to Critical.
- **NEVER write generic follow-up questions.** "Tell us about your IR process" is a questionnaire item. "Your SOC 2 doesn't describe a formal IR runbook; can you share your IR plan and the date of the last tabletop exercise?" is a diligence question.
- **NEVER treat a few mild exceptions as a red flag.** Two to five minor exceptions with documented remediation in a 12-month Type 2 is normal for a healthy program. Zero exceptions across a complex system can be a sign of a soft auditor or narrow scope.
- **NEVER confuse a 3-month first-year Type 2 with insufficient coverage.** A short period for a first-year audit is normal — many vendors do a 3-month Type 2 the year after their Type 1. Flag it as "limited testing window" but don't penalize harshly.
