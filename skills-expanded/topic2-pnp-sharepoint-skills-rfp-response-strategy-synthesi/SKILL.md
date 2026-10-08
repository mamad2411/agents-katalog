---
name: rfp-response-strategy-synthesis
description: >
  Reads multiple input documents — past proposals, a win strategy brief,
  capability statements, a win/loss debrief, and RFP evaluation criteria —
  and synthesizes them into a recommended proposal Table of Contents and a
  content strategy brief. Produces an explicit competitive-positioning
  recommendation and a page-budget allocation table. Designed to run after
  content mapping (Phase 1) and before any drafting begins (Phase 3).
---

# Strategy Synthesis Skill

## Firm Profile (REQUIRED — fill in before use)

These values define who your firm is and how it writes. See `SETUP.md`.

- FIRM NAME:          [FIRM NAME]
- WHAT THE FIRM DOES: [one sentence]
- ROLE BOUNDARY:      [what the firm will NOT claim to do — leave blank if none]
- VENDOR STANCE:      [vendor-neutral OR resells/implements specific products]
- SPECIALIZATION:     [domains the firm credibly claims]
- VALUE MODEL:        [optional — the through-line your proposals argue]
- VOICE:              [3–5 adjectives]

---

## Purpose

Before any content is drafted, the proposal needs a coherent response strategy: a
clear point of view on what the client cares about most, how the firm's
capabilities map to those priorities, and what narrative arc is most persuasive.
This skill synthesizes multiple inputs into two deliverables — a **recommended
Table of Contents** and a **Content Strategy Brief** — that become the approved
blueprint for Phase 3. Nothing in Phase 3 should be drafted without an approved
output from this skill.

---

## Critical Output Rules

> **Do not output the Coverage Map, Table of Contents, or Content Strategy Brief
> to chat.** These are document deliverables. All content from Steps 6–8 goes
> directly into the Word document saved in Step 9. Chat output is limited to
> one-line progress updates per step and the final summary.

---

## Prerequisites

- The **RFP Tracker** List must be populated (Phase 1 complete), including the Available Content column.
- These documents must be accessible in SharePoint, locations confirmed by the user before running:
  - **Past Proposals** (2–3 from the Past Proposals Library, ideally same solution domain)
  - **Win Strategy Brief** (salesperson-authored: client context, competitive dynamics, deal-specific differentiators)
  - **Capability Statements** (2–3 firm-authored documents describing relevant services, methodologies, credentials)
  - **Win/Loss Debrief** (lessons learned from past similar deals)
- Write access to the **WIP Collaboration Folder** to save the output deliverables.

---

## Step 1 — Load and Read All Inputs

Read each input with a specific extraction goal — know what you are looking for
before you read. These extracts feed the analysis in Steps 2–4.

**RFP Tracker List:**
- Every row by category (Questions, Mandatory Requirements, Submission Rules, Evaluation Criteria)
- Evaluation-criteria scoring weights or relative-importance signals
- Which mandatory rows have Available Content matches vs. No Match — gaps shape the strategy
- All Submission Rules (format, page limits, deadlines, required appendices, response-order instructions) — these constrain the ToC regardless of strategy

**Past Proposals (2–3):**
- How the executive summary framed the value proposition
- Section-ordering decisions — what led, what followed, what went to appendix
- Where the proposal led with strength vs. neutralized a weakness
- Specific language, case studies, or proof points directly reusable for this RFP
- Structural patterns recurring across proposals — proven approaches

**Win Strategy Brief:**
- The salesperson's read on the client's top 2–3 priorities (ground truth for what to address first)
- Known or suspected competitors and their likely strengths (shapes neutralization themes)
- The firm's deal-specific differentiators as assessed by the salesperson (not generic firm differentiators)
- Relationship context, political dynamics, known evaluator preferences
- Red flags and risks explicitly flagged — must be addressed, not ignored
- **Pricing posture signals** — price-sensitive, best-value, or lowest-price (input to Step 4)

**Win/Loss Debrief:**
- What specifically worked in past similar deals (proof points, structural choices, differentiator framings)
- What cost points with evaluators (thin sections, unsubstantiated claims, structural mistakes)
- Client feedback themes — signals about what evaluators in this space care about
- Lessons that should constrain the ToC (e.g., "always include a standalone change-management section")

**Capability Statements:**
- Core service and methodology descriptions mapping to RFP evaluation-criteria themes
- Named methodologies, credentials, and client-outcome proof points
- Language directly referenceable in the section-by-section drafting notes

---

## Step 2 — Analyze Evaluation Criteria and Mandatory Requirements

The evaluation criteria reveal what the client actually scores on — analyze them first.

1. Extract all **Evaluation Criterion** rows from the RFP Tracker.
2. Identify scoring weights / importance signals; the themes appearing most often across criteria; and any unusually specific criteria (often signal existing preferences or prior vendor relationships).
3. **Rank the evaluation criteria by implied importance.** This drives section ordering (Step 6) and page-budget allocation (Step 6b).
4. Cross-reference mandatory requirements: each mandatory item with no content match (flagged in Phase 1) is a **response gap** requiring explicit attention in the strategy.
5. **Capture the total proposal page limit** (and any per-section limits) from Submission Rules. Hold both the weight ranking and the page limit — the two inputs to Step 6b. If no limit is stated, record "no stated limit"; Step 6b uses a recommended length instead.

---

## Step 3 — Analyze Past Proposals and Win/Loss Debrief

Using the Step 1 extracts:
1. Identify each past proposal's structure/order, exec-summary framing and value proposition, and effective sections/approaches (cross-referenced with the Win/Loss Debrief).
2. From the Win/Loss Debrief, confirm what worked, what cost points, and any client-type-specific patterns (e.g., "buyers in this sector value implementation track record over methodology detail").
3. Note structural patterns recurring across multiple winning proposals — these likely reflect the firm's proven approach and should anchor the recommended ToC.

---

## Step 4 — Analyze Capabilities and Decide Competitive Posture

1. Map each capability statement's strengths to the ranked evaluation criteria — this reveals where the firm is naturally strong vs. where it must work harder.
2. Combine with the Win Strategy Brief extracts (priorities, competitors, differentiators, risks) from Step 1.

### Competitive Positioning Analysis

Take an explicit position on **how the firm should compete** before writing themes
— a proposal that wins on capability is structured very differently from one that
wins on price. For each lever, score the firm's position as **Lead with**,
**Match competitors**, or **Concede**:

| Lever | Lead with means… | Match means… | Concede means… |
|---|---|---|---|
| **Price** | We can credibly price below the likely competitive median and that is our strongest path to win. | Our price will be in band; neutralize price as a factor and shift evaluators to other dimensions. | Our price will be higher; we must justify the premium with capability or risk superiority. |
| **Capability / technical strength** | We have a defensible differentiator (named methodology, relevant prior experience, qualified personnel) no competitor can match. | Credible but not uniquely strong; meet every requirement cleanly. | Gaps in credentials or track record; neutralize, not win, on capability. |
| **Delivery risk** | We can credibly claim lower delivery risk (track record, named team commitment, transition plan, stability) than competitors. | Risk profile comparable to competitors; meet every requirement cleanly. | Visible risk (smaller firm, limited track record, dependencies); neutralize. |

Combine the three scores into a single recommendation: which lever the proposal
leads with, matches, and concedes/neutralizes. This is written into the Content
Strategy Brief as Section 3 (Step 8).

If the Win Strategy Brief and the RFP's evaluation approach contradict each other
(e.g., salesperson says "price will win" but evaluation weights capability at 60%),
**flag the conflict explicitly and surface it for human decision** in the Content
Gaps section — do not resolve it unilaterally.

---

## Step 5 — Synthesize and Identify Strategic Themes

Combine the Step 2–4 analysis into **strategic themes** that anchor the narrative.
A strategic theme ties a client priority (from evaluation criteria and Win Strategy
Brief) to a firm strength (from capabilities and past proposals).

### Strategic Theme Format (aim for 3–5)
```
Theme: [Short label, e.g., "Proven Delivery at Scale"]
Client priority it addresses: [e.g., "Implementation track record — 25% of scoring"]
Firm differentiator: [e.g., "200+ similar engagements, 94% on-time delivery rate"]
Supporting content available: [Document names from Available Content column]
Content gaps: [Any mandatory requirements not yet covered by this theme]
Risk: [e.g., "Competitor X likely claims similar track record — need specific proof points"]
```

Also classify:
- **Win themes** — clear, defensible advantage
- **Neutralization themes** — areas where the firm is not strongest but must respond credibly to avoid scoring below competitors
- **Risk themes** — RFP items or criteria that are genuine weaknesses; address honestly without conceding points unnecessarily

### Weak-Reference Compensation (when Content Finder flagged reference gaps)

If the Content Finder flagged any reference/past-performance row as **No Match** or
**weak match** (low relevance, dated, wrong sector, wrong scale), the Content
Strategy Brief **must** include a neutralization theme that compensates. A weak
references section is one of the most common reasons proposals lose — do not skip
this.

For each flagged gap, propose at least one compensating move:
- **Named staff with directly relevant experience** — put forward a key team member whose background includes comparable work; their experience travels with the firm.
- **Cited analog engagement** — cite an engagement with comparable scope, scale, and complexity, and explicitly draw the parallel for the evaluator.
- **Teaming partner reference** — if a teaming partner has a stronger reference, lead with the partner's reference under the joint structure and note the arrangement.
- **Methodology and risk-control overlay** — compensate with an unusually detailed risk register, transition plan, and QA narrative; evaluators accept a stronger process story when track-record evidence is light.

Write the compensation plan into the Content Strategy Brief as Section 6, in an
explicit subsection titled "Reference Gap Compensation".

---

## Step 6 — Produce the Recommended Table of Contents

Using the strategic themes and evaluation-criteria ranking as primary drivers,
produce a ToC that:
- Leads with the executive summary (firm's understanding of the client's situation + primary value proposition)
- Orders body sections to mirror the client's stated priorities (highest-weighted criteria earliest)
- Groups related requirements logically rather than responding in RFP sequence (unless the RFP requires it)
- Includes a section for each mandatory requirement not already covered thematically
- Ends with supporting appendices (team bios, case studies, certifications, pricing)

### Table of Contents Format
```
RECOMMENDED TABLE OF CONTENTS
[Client / RFP Name] — [Date]

1. Executive Summary
   1.1 Our Understanding of Your Needs
   1.2 Our Recommended Approach
   1.3 Why [Firm Name]

2. [Section tied to highest-weighted evaluation criterion]
   2.1 ...
3. [Section tied to second-weighted criterion or primary strategic theme]
   3.1 ...
[Continue for all major themes and mandatory requirements]

Appendix A — [e.g., Team Profiles]
Appendix B — [e.g., Case Studies]
Appendix C — [e.g., Required Forms / Certifications]
```
For each section, add a one-line annotation explaining the strategic rationale:
> *"Section 2 leads because 'Implementation Experience' carries 30% of evaluation weight and is our strongest differentiator."*

---

## Step 6b — Allocate Page Budget Across Sections

Allocate the total page limit (from Step 2) across ToC sections **proportional to
evaluation weight**. A page budget gives the Phase 3 agent a hard space constraint
per section and prevents low-weight sections from consuming pages that should go to
high-weight ones.

### Allocation Method
1. Take the body page limit (do this per section if the RFP specifies per-section limits). Reserve a fixed allowance for non-body content first:
   - Executive Summary: 5–8% of body pages (min 2, max 5)
   - Front matter (cover, ToC, transmittal): excluded if the RFP excludes them; otherwise 1 page
   - Appendices: typically outside the page limit; if inside, reserve based on what the RFP requires
2. Distribute **remaining body pages** in proportion to evaluation weight (a 40% factor receives 40% of remaining body pages).
3. Apply two adjustments:
   - **Minimum floor:** no body section below 2 pages (a 0.5-page section reads as thin).
   - **Cap for redundancy:** no body section above 50% of total body pages (concentrated allocation reads as imbalanced).
4. Round to whole/half pages. Sum and confirm it equals the body limit; rebalance leftover pages to the highest-weighted section first.
5. If no stated page limit, use a recommended body length of 25 pages (advisory proposals) or 40 pages (solution proposals) and allocate proportionally.

### Page Budget Table Output (Section 8 of the Content Strategy Brief)
```
PAGE BUDGET ALLOCATION
Total body limit: 25 pages

Section | Title                              | Evaluation Weight | Allocated Pages | Rationale
--------|------------------------------------|-------------------|-----------------|----------
1       | Executive Summary                  | —                 | 2.0             | Fixed allowance (8% of body)
2       | Technical Approach                 | 40%               | 9.0             | Highest-weighted factor
3       | Management Approach                | 20%               | 4.5             | Second-weighted factor
4       | Relevant Experience                | 20%               | 4.5             | Body narrative; references in appendix
5       | Team & Key Personnel               | 10%               | 2.5             | Body narrative; résumés in Appendix A
6       | Pricing Narrative                  | 10%               | 2.5             | Body narrative; pricing in separate section
        | TOTAL                              | 100%              | 25.0            |
```
The Phase 3 agent treats allocated pages as a **hard ceiling, not a target**.
Overflow goes to an appendix (if the RFP allows) or is cut — drafting outside the
budget is not allowed without re-approval at the human gate.

---

## Step 7 — Verify Full RFP Coverage

Before finalising the ToC, cross-reference every RFP Tracker row against the
proposed sections. The ToC must account for every Question, Mandatory Requirement,
and content-bearing Submission Rule — no row left without a home. A compelling
structure that misses a requirement is a compliance failure.

### Coverage Mapping Process
1. Take every row where Category = **Question**, **Mandatory Requirement**, or **Evaluation Criterion**.
2. For each, identify the ToC section that covers it (covered = a reasonable reader would expect it addressed there).
3. Flag any row that cannot be mapped — these are **coverage gaps**.
4. For each gap: add a subsection to an existing section, or add a standalone section. Do not leave gaps unresolved.
5. For **Submission Rules**, classify each before deciding how to handle it:
   - **Procedural Submission Rules** govern *how* the proposal is submitted (page limits, font/margin, file format, delivery method, deadline, number of copies). These do not require a section/appendix — add each to a **Submission Checklist** (a separate table in the deliverable) so the team can verify compliance. Do not map procedural rules to ToC sections.
   - **Content Submission Rules** specify *what must be included* (signed certifications, pricing workbook, staffing plans, résumés, letters of commitment). Each must have a named home — a body section or a required appendix in the ToC. Add any missing appendices now.
   - If ambiguous, treat as content, assign a ToC home, and note the ambiguity in the Coverage Map.
6. Check whether the RFP requires responses in a specific sequential order (Submission Rules). If so, flag it — the ToC may need to follow RFP numbering rather than strategic ordering, with themes applied within sections.

### Coverage Map Output
```
COVERAGE MAP
RFP Row | Item (abbreviated) | Category | Rule Type | ToC Section / Checklist | Notes
--------|-------------------|----------|-----------|-----------------------|------
Row 1   | Describe your transformation methodology | Question | — | Section 2 — Approach | Primary coverage
Row 2   | Provide 2 examples of relevant experience | Question | — | Section 4 + Appendix B | Examples in appendix, referenced in body
Row 3   | Bidder must have authority to contract  | Mandatory | — | Appendix C — Certifications | Admin qualifier
Row 4   | 90-day execution plan                    | Question | — | Section 3 — Execution Plan | Standalone section added
Row 5   | Submit proposal in PDF, max 30 pages      | Submission Rule | Procedural | Submission Checklist | No ToC coverage needed
Row 6   | Include signed pricing workbook           | Submission Rule | Content | Appendix D — Pricing Workbook | Required appendix added
[GAP]   | Describe subcontracting strategy         | Mandatory | — | NOT COVERED | Add Section 6 or subsection
```
Do not proceed to Step 8 until the Coverage Map shows zero content gaps. Procedural
rules should all appear in the Submission Checklist with no ToC mapping. If a
content gap cannot be resolved without human input (e.g., SME content that doesn't
exist), flag it explicitly in the Content Gaps section of the Content Strategy Brief.

---

## Step 8 — Produce the Content Strategy Brief

A short companion document to the ToC giving the Phase 3 agent and the human
reviewer a clear set of instructions for *how* the proposal should be written, not
just what it should contain.

```
CONTENT STRATEGY BRIEF
[Client / RFP Name] — [Date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. SITUATION SUMMARY
What the client is trying to achieve, based on the RFP and Win Strategy Brief.
[2–3 sentences — the agent's synthesis of what the client actually cares about,
 not a restatement of the RFP]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. OUR CORE VALUE PROPOSITION FOR THIS DEAL
The single overarching message the proposal should convey. [1–2 sentences]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. COMPETITIVE POSITIONING RECOMMENDATION  (from Step 4)
  • Price:        [Lead with / Match / Concede] — [1-sentence rationale]
  • Capability:   [Lead with / Match / Concede] — [1-sentence rationale]
  • Delivery risk:[Lead with / Match / Concede] — [1-sentence rationale]
  Overall recommendation: [1–2 sentences — which lever leads, matches, neutralizes;
  what evaluator behavior this implies; any conflict with the Win Strategy Brief the
  human gate must resolve]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. STRATEGIC THEMES
[3–5 themes in the Step 5 format]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. TONE AND VOICE GUIDANCE
- Overall tone: [from Firm Profile VOICE — e.g., "Confident and specific — avoid hedging"]
- Technical depth: [e.g., "Moderate — client is a business buyer, not technical"]
- Language to emphasize: [e.g., "Outcomes, track record, client-centricity"]
- Language to avoid: [e.g., "Jargon, vague superlatives, boilerplate disclaimers in body text"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. RISKS AND NEUTRALIZATION STRATEGY
[For each risk/weakness, a 1–2 sentence recommended handling approach]
  6a. Reference Gap Compensation (required if Content Finder flagged reference gaps)
  [For each flagged gap row, the chosen compensating move from Step 5 and a
   1-sentence drafting instruction]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. CONTENT GAPS REQUIRING SME OR SALESPERSON INPUT
[RFP items with no content match and no existing capability coverage — must be
 addressed by a human before Phase 3 drafting begins]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. PAGE BUDGET ALLOCATION
[Page Budget Table from Step 6b]
  Drafting rule: allocated pages are a hard ceiling, not a target. Overflow goes to
  an appendix (if the RFP allows) or is cut. No section exceeds its allocation
  without re-approval at the human gate.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. SECTION-BY-SECTION DRAFTING NOTES
For each ToC section:
  Section [X]: [Allocated pages from Section 8] — [Drafting instruction — what to
  emphasize, what content to draw from, what to avoid, and where the section
  reinforces the competitive positioning stance from Section 3]
```

---

## Step 9 — Save Deliverables and Report Back

1. **Locate or create the deal subfolder** in the WIP Collaboration Folder before saving:
   - Naming convention: `[ClientShortName]_[RFPShortName]_[Year]` (one or two meaningful words each, underscores, no spaces — e.g., `Northwind_TransformationRFP_2026`)
   - Use the client name and RFP title from the Win Strategy Brief or RFP Tracker. Check whether the subfolder exists; if so, save into it, else create it first.
   - All subsequent phase outputs save into this same subfolder — it is the single deal workspace.
2. **Create and save the deliverable Word document** as **[ClientName]_Strategy_Brief_[Date].docx** (a properly formatted .docx — not text, chat, or markdown export), structured with clear headings in this order:
   1. Cover information: RFP name, date, prepared by
   2. Coverage Map (Step 7) — as a table
   3. Submission Checklist (Step 7) — as a table, if any procedural rules were identified
   4. Recommended Table of Contents (Step 6) — including strategic rationale annotations
   5. Page Budget Table (Step 6b) — as a table
   6. Content Strategy Brief (Step 8) — all nine sections, in order
   - If the interface does not support direct Word creation/upload to SharePoint, create the document in the workspace and provide the user a download link with instructions to upload it manually.
3. **Report back** with a concise summary only (below). Do not reproduce the full document content in chat.

### Example Summary Output

```
Strategy Synthesis complete.

Inputs processed:
  • RFP Tracker list:           31 rows analyzed (18 Questions, 7 Mandatory,
                                 4 Evaluation Criteria, 2 Submission Rules)
  • Past proposals reviewed:     3 (2 wins, 1 loss)
  • Win Strategy Brief:          Read and synthesized
  • Capability Statements:       3 documents
  • Win/Loss Debrief:            Read and synthesized

Competitive positioning recommendation:
  • Price:        Match     — bid in band, neutralize as a factor
  • Capability:   Lead with — named methodology + relevant prior experience
  • Delivery risk: Match    — strong transition plan offsets firm size

Strategic themes identified: 4
  1. Governance-First Transformation              (win theme)
  2. Vendor-Neutral Independence                  (win theme)
  3. Structured Knowledge Transfer                (win theme)
  4. 90-Day Execution Readiness                   (neutralization theme)

Reference gap compensation: 2 flagged rows
  • Row 9  — Healthcare reference gap → cite analog engagement + name lead
                                 with sector experience
  • Row 17 — Security reference gap   → lead with teaming partner reference

Page budget allocated: 25 body pages
  Exec Summary 2.0  •  Technical 9.0  •  Management 4.5
  Experience 4.5    •  Team 2.5  •  Pricing 2.5

Coverage Map: 31 rows mapped
  Fully covered:               27 rows
  Coverage gaps resolved:       2 rows (new subsections added to ToC)
  Appendix items confirmed:     2 (Certifications, Pricing Workbook)
  Submission rules classified:  4 total
    • Procedural (Submission Checklist): 2 (page limit, file format)
    • Content (ToC/Appendix):            2 (signed pricing workbook, staffing plan)

Content gaps requiring human input before Phase 3 (5 items):
  • Row 9  — Examples of engagements in a healthcare context (none in library)
  • Row 14 — Subcontracting strategy (firm policy input needed)
  • Row 19 — Data residency controls (SME required)
  • Row 26 — Pricing model and rate card (salesperson must provide)
  • Row 30 — Innovation roadmap (no existing content)

Deal workspace:
   WIP Collaboration Folder / Northwind_TransformationRFP_2026 /

Strategy Brief (Word document):
   Northwind_Strategy_Brief_2026-03-03.docx
   [ SharePoint link or download link ]

Next steps: Salesperson and pursuit lead to open the Strategy Brief, review the
Coverage Map, competitive positioning recommendation, and Page Budget Table, and
approve the ToC before Phase 3 drafting begins. Resolve 5 content gaps before
handoff to drafting agent.
```

---

## Notes & Edge Cases

- **No Win Strategy Brief provided:** Do not proceed — notify the user that the
  synthesis will be significantly less targeted without it. Offer to run a reduced
  synthesis using only the RFP and capability documents, and flag the output as preliminary.
- **Conflicting signals:** If the Win Strategy Brief contradicts evaluation
  criteria (e.g., salesperson emphasizes price but evaluation weights approach),
  flag the conflict explicitly and do not resolve it unilaterally — surface it in
  the Competitive Positioning Recommendation for human decision.
- **No stated page limit:** Step 6b uses a recommended body length (25 pages
  advisory, 40 solution) and notes the assumption in the Page Budget Table. The
  human gate must confirm before Phase 3.
- **No stated evaluation weights:** Infer weights from order (lists are often
  descending importance), note the inference in both the ToC rationale and the Page
  Budget Table, and flag for human confirmation.
- **No reference gaps:** When Content Finder flags zero reference gaps, Section 6a
  reads "No reference gaps flagged — no compensation required" rather than being
  omitted — making it explicit that the check ran.
- **RFP requires sequential response:** Detected in Step 7. The Coverage Map flags
  it and the ToC follows RFP numbering — themes applied within sections. The Page
  Budget Table still applies, allocating pages to RFP-numbered sections by the
  evaluation weight of whatever they cover.
- **Ambiguous submission rules:** When a rule sits between procedural and content
  (e.g., "provide a management plan as part of your technical response"), classify
  as content and assign a ToC home — safer to include a section than omit one. Note
  the ambiguity in the Coverage Map.
- **Confidentiality of past proposals:** Do not include client names or
  identifiable details in the deliverables. Reference them as "Prior Engagement A,"
  "Prior Engagement B," etc.
