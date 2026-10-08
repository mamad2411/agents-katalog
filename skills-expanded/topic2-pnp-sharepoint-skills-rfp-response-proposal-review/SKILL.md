---
name: rfp-response-proposal-review
description: >
  Post-generation audit agent for proposal drafts. Runs three structured
  checks — strategy fidelity, RFP coverage, and content sourcing — against
  the generated proposal draft, the approved Strategy Brief, and the RFP
  Tracker list. Produces a Review Report Word document flagging issues before
  any human reviewer opens the draft. Designed to run after Phase 3 content
  generation and before the human review gate.
---

# Proposal Review Skill

## Firm Profile (REQUIRED — fill in before use)

These values define who your firm is and how it writes. See `SETUP.md`.

- FIRM NAME:          [FIRM NAME]
- WHAT THE FIRM DOES: [one sentence]
- ROLE BOUNDARY:      [what the firm will NOT claim to do — leave blank if none]
- VENDOR STANCE:      [vendor-neutral OR resells/implements specific products]
- SPECIALIZATION:     [domains the firm credibly claims]
- VOICE:              [3–5 adjectives]

---

## Purpose

An AI-generated proposal draft may look complete but contain three categories of
silent failure: drift from the approved strategy, missed RFP requirements, or
content not grounded in the firm's source material. None are obvious from a quick
read. This skill audits all three dimensions and produces a structured Review
Report telling the human reviewer exactly what to look at — and what has already
been verified — before they open the draft.

---

## Critical Output Rules

> **Do not output the Review Report or audit findings to chat.** All findings go
> into the Review Report Word document saved in Step 6. Chat output is limited to
> one-line progress updates per step and the final summary.
>
> **The Review Report Word document is the only deliverable.** Accumulate findings
> internally, then write the complete report in Step 6.

---

## Prerequisites

- The **generated proposal draft** (.docx) must be in the deal's WIP Collaboration Folder subfolder.
- The **Strategy Brief** (.docx, Phase 2) must be accessible — approved ToC, strategic themes, tone guidance, section-by-section drafting notes.
- The **RFP Tracker** List must be accessible with all columns populated, including Available Content and Source 1/2/3.
- Write access to the deal's WIP Collaboration Folder subfolder.

---

## Step 1 — Load All Inputs

Load and read the following before any checks.

**Proposal Draft** — read in full. Note:
- The actual section structure and headings present
- Text marked as placeholder (`[PLACEHOLDER`, `[TBD`, `[INSERT`, `[MISSING`, or similar)
- Sections notably thin (less than one substantive paragraph)
- Specific factual claims, statistics, or named outcomes that require source grounding

**Strategy Brief (Phase 2)** — extract:
- The approved Table of Contents (exact structure and order)
- The strategic themes (3–5, with client priority, firm differentiator, supporting content)
- Tone and voice guidance
- Section-by-section drafting notes
- Content gaps flagged in Phase 2 — these should appear as placeholders in the draft

**RFP Tracker List** — read all rows, focusing on:
- Every Question, Mandatory Requirement, and Evaluation Criterion — must be addressed in the draft
- Available Content — what the content generation agent was supposed to draw from
- Source 1/2/3 — the documents the agent should have consulted per row
- Rows where Available Content = "No Match" — these should appear as placeholders

---

## Step 2 — Strategy Fidelity Check

Cross-reference the draft against the approved Strategy Brief. *Did the draft
follow the blueprint?*

**2a — ToC Structure Check.** Compare actual headings against the approved ToC. For each approved section:
- **Present and correct** — exists and heading matches or is a reasonable equivalent
- **Present but repositioned** — exists but in a different order (flag — ordering was deliberate based on evaluation weights)
- **Missing** — an approved section is absent (critical failure)
- **Added** — draft contains a section not in the approved ToC (flag — may be appropriate or scope drift)

**2b — Strategic Theme Coverage.** For each of the 3–5 themes, assess:
- **Present** — a reader would understand the argument (not just a keyword)
- **Weak** — mentioned but not developed into a clear, evidenced argument
- **Absent** — no meaningful treatment

**2c — Tone and Voice.** Sample at minimum the exec summary, one mid-document body section, and one appendix-adjacent section. For each: does the writing match the tone guidance and Firm Profile VOICE? Are flagged language patterns present? Does it read as [FIRM NAME]-authored or generic consultant prose?

**2d — Drafting Notes Compliance.** For each section with specific drafting notes, check whether the draft followed them. Flag any section where the note said to emphasise a differentiator or avoid a framing and the draft did the opposite.

---

## Step 3 — RFP Coverage Check

Re-run coverage logic on the **actual draft** — not the approved ToC. A
requirement being in the ToC does not mean it was addressed. For every RFP Tracker
row where Category = **Question**, **Mandatory Requirement**, or **Evaluation
Criterion**, locate the corresponding passage and classify:

- **Covered** — a substantive response exists (at minimum one paragraph directly addressing the requirement)
- **Placeholdered** — a clearly marked, descriptive placeholder exists in the relevant section (acceptable where Phase 2 flagged a gap; the text must say what is missing, not just mark a blank)
- **Missing** — neither a substantive response nor a placeholder exists (critical gap — flag for immediate action)
- **Thin** — a response exists but is less than one substantive paragraph, or only generic statements not specific to this RFP (moderate priority)

Produce a **Draft Coverage Map** (same format as the Phase 2 Coverage Map, plus a Coverage Status column):
```
DRAFT COVERAGE MAP
RFP Row | Item (abbreviated) | Category | ToC Section | Coverage Status | Notes
--------|-------------------|----------|-------------|-----------------|------
Row 1   | Describe transformation methodology | Question | Section 2 | Covered | 3 paragraphs, specific to client context
Row 2   | Provide 2 examples relevant experience | Question | Section 4 + Appendix B | Covered | 2 case studies present
Row 3   | Bidder authority to contract | Mandatory | Appendix C | Placeholder | Awaiting signed cert — noted correctly
Row 4   | 90-day execution plan | Question | Section 3 | Thin | Only 1 generic paragraph — needs specifics
Row 5   | Describe subcontracting strategy | Mandatory | Section 6 | Missing | No response and no placeholder — critical gap
```

---

## Step 4 — Content Sourcing Check

*Is the draft grounded in the firm's actual source material, or did the agent
invent content?* This is the hardest check to run precisely — focus on high-risk areas.

**High-risk areas:**
- Sections where RFP Tracker Available Content = "No Match" — no source material. If the draft has substantive content here (rather than a placeholder), flag as potentially hallucinated.
- Specific statistics, percentages, named client outcomes, or delivery timelines — the most likely hallucination vectors. Flag any not in the Available Content summaries or Source documents.
- Named methodologies/frameworks claimed as proprietary — verify they appear in capability statements or past proposals, not invented for this draft.

**Sourcing confidence per major section:**
- **High** — clearly grounded in available source material (Source 1/2/3 or capability statements)
- **Medium** — consistent with the firm's known positioning but not directly traceable to a specific source document
- **Low / flag for review** — specific claims, numbers, or outcomes that appear in no available source — human must verify before submission

---

## Step 5 — Placeholder Audit

Find and assess every placeholder.

1. Search all markers: `[PLACEHOLDER`, `[TBD`, `[INSERT`, `[MISSING`, `[DRAFT NOTE`, or any bracketed text signaling incomplete content.
2. For each placeholder:
   - Confirm it is **descriptive** (says what is missing and ideally who provides it)
   - Confirm it maps to a **known content gap** flagged in Phase 2 — if a placeholder appears for a requirement that had available content, flag as a content generation failure
   - Confirm it is **in the right section**
3. Flag any non-descriptive placeholder (e.g., `[TBD]` with no context) — must be rewritten before human review.
4. Produce a **Placeholder Register**:
```
PLACEHOLDER REGISTER
Section | Placeholder Text (abbreviated) | Content Needed | Owner | Priority
--------|-------------------------------|----------------|-------|--------
Section 3.2 | [PLACEHOLDER: 90-day plan detail] | Detailed execution timeline with milestones | Pursuit lead | High
Appendix C  | [PLACEHOLDER: signed certifications] | Executed legal forms | Contracts team | High
Section 5.1 | [PLACEHOLDER: data residency controls] | Technical SME input on data handling approach | SME | Medium
```

---

## Step 6 — Produce the Review Report

Compile all findings into a single Review Report Word document — what the human
reviewer reads before opening the draft.

```
PROPOSAL REVIEW REPORT
[RFP Name] — [Date]
Prepared by: Review Agent (Phase 4)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERALL STATUS

[ READY FOR HUMAN REVIEW / REQUIRES REVISION BEFORE REVIEW ]

Critical issues (must fix before review):     [count]
Moderate issues (should fix before review):   [count]
Low-priority issues (fix before submission):  [count]
Placeholders requiring human input:           [count]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. STRATEGY FIDELITY
ToC structure: [Matches approved / Deviations noted — see table]
Strategic themes: [All present / Weak or missing — see list]
Tone and voice: [Compliant / Issues noted]
Drafting notes compliance: [Followed / Deviations]
[Findings table: Section | Issue | Severity | Recommended Action]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. RFP COVERAGE
[Draft Coverage Map table — from Step 3]
Summary: Covered [n] | Placeholdered [n] (acceptable) | Thin [n] | Missing [n] (critical)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. CONTENT SOURCING
[Per-section sourcing confidence ratings]
Flagged items requiring human verification:
  [Specific claims/statistics/outcomes not traceable to source — confirm or remove before submission]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. PLACEHOLDER REGISTER
[Placeholder Register table — from Step 5]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. PRIORITISED ACTION LIST
Before the human review session: [critical and moderate issues for the pursuit team]
Before submission (can be resolved during review): [low-priority issues and placeholder owners]
```

**Overall Status Logic**
- **REQUIRES REVISION BEFORE REVIEW** if any critical issue exists: missing RFP requirements with no placeholder, missing ToC sections, or low-confidence sourcing flags on scored sections.
- **READY FOR HUMAN REVIEW** if no critical issues, all gaps properly placeholdered, and the reviewer has a clear action list.

---

## Step 7 — Save and Report Back

1. Save the Review Report as **[ClientName]_Review_Report_[Date].docx** in the deal subfolder, alongside the proposal draft in the same WIP Collaboration Folder subfolder.
2. Report back with a concise summary (see below). Do not reproduce the full report in chat.

### Example Summary Output

```
Proposal Review complete.

Overall status: REQUIRES REVISION BEFORE REVIEW

Strategy Fidelity:
  ToC structure matches approved version
  Theme 2 (Vendor-Neutral Independence) present but underdeveloped
      — only mentioned in executive summary, not substantiated in body
  Section 4 tone: hedging language detected ("we believe", "we hope")
      — conflicts with tone guidance (confident, specific)

RFP Coverage: 31 rows checked
  Covered:        24 rows
  Placeholdered:   5 rows (all properly described — acceptable)
  Thin:            1 row (Row 4 — 90-day plan needs specifics)
  Missing:         1 row (Row 14 — subcontracting strategy:
                     no response and no placeholder — CRITICAL)

Content Sourcing:
  3 items flagged for human verification:
  • Section 2.3: "94% on-time delivery rate" — not found in any source document
  • Section 4.1: Named client outcome (healthcare) — not in capability statements
  • Appendix B: Case study dates — inconsistent with past proposal dates

Placeholders: 5 found, all descriptive and correctly located

Critical actions before human review:
  1. Add placeholder (or draft response) for Row 14 — subcontracting strategy
  2. Verify or remove 3 flagged claims in sourcing check
  3. Strengthen Theme 2 coverage in Section 3 body

Review Report saved to:
   WIP Collaboration Folder / Northwind_TransformationRFP_2026 /
   Northwind_Review_Report_2026-03-04.docx
```

---

## Notes & Edge Cases

- **Draft is very long:** Focus the sourcing check on sections covering the
  highest-weighted evaluation criteria first. If time is limited, flag that the
  sourcing check was partial and note which sections were not checked.
- **Multiple draft versions exist:** Confirm which file is the current draft
  before running. If multiple versions exist in the subfolder, ask the user to
  confirm the correct file.
- **Placeholder format varies:** Search broadly — `[`, `TBD`, `INSERT`, `DRAFT`,
  `NOTE:` — and standardise all placeholders to `[PLACEHOLDER: description —
  owner]` as part of this review.
- **Thin sections on low-weight criteria:** Note the evaluation weight when
  flagging thin sections so the reviewer can prioritise (a thin response on a
  5%-weighted criterion is less critical than on a 30%-weighted one).
- **Draft contains tracked changes:** Run the review against the accepted (final)
  version of the text, not the marked-up version. Note this in the report.
- **Content gap placeholders that were filled:** If the draft has substantive
  content in a section Phase 2 flagged as a content gap, flag it for human review
  — it may be appropriate or hallucinated. Do not assume it is correct simply
  because it is present.
