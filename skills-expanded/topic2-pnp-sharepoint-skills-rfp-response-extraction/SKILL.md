---
name: rfp-response-extraction
description: >
  Extracts questions, mandatory requirements, submission rules, evaluation
  criteria, and administrative certifications from a Request for Proposal
  (RFP) document and populates a SharePoint List with each item categorized,
  flagged for mandatory status, source-traced, and ready for owner assignment
  and tracking. Handles addenda by letting later versions override earlier ones.
---

# RFP Extraction Skill

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

Parse an RFP stored in SharePoint and populate a structured **RFP Tracker**
List with every actionable item, each broken out by category, flagged mandatory
or not, traced to its source location, and given tracking columns for owner
assignment and progress monitoring.

---

## Prerequisites

- The RFP document (PDF, Word, etc.) must be accessible in SharePoint.
- The agent must have permission to create Lists and List items in the target site.
- If the package includes addenda, attachments, or a referenced Q&A document,
  those should also be accessible. Flag any that are missing in the summary.

---

## Step 1 — Read the RFP Document

1. Locate the RFP file in SharePoint using the path/URL provided. If the package
   has multiple documents (RFP body, SOW, attachments, addenda, Q&A), list every
   one and capture filename, page count, and document type.
2. Extract the full text of each document.
3. If a document is long, process it in sections but treat it as one document for
   extraction.
4. **Process addenda last and let them override.** If an addendum changes a due
   date, page limit, or requirement, the later version wins. Diff the changed
   section against the original — do not assume addenda are purely additive.

---

## Step 1b — (Optional) Capture Solicitation Metadata

Optionally capture solicitation-level facts to an **RFP Metadata** list (one
record per RFP). Skip for simple RFPs unless the user asks.

| Field | Where to look |
|---|---|
| RFP / reference number | Cover page or header |
| Issuing organization | Cover page |
| Primary contact + email + phone | Instructions to bidders section |
| Submission deadline (date + time + zone) | Instructions section — **check addenda** |
| Question / clarification deadline | Instructions section |
| Page limits | Instructions / format section |
| Font / margin / spacing rules | Format section |
| File format and naming convention | Submission instructions |
| Submission method (portal, email) | Submission instructions |
| Period of performance / contract term | Scope or terms section |
| Anticipated award / decision date | Timeline or evaluation section |
| Evaluation approach | Evaluation section (lowest price, best value, weighted scoring, etc.) |

If a field is missing, write `NOT SPECIFIED` and flag it in the summary so the
team can raise a clarifying question before the question deadline.

---

## Step 2 — Extract RFP Items

Extract every item falling into a category below; record the fields listed.

### Categories and What to Look For

| Category | What to Extract |
|---|---|
| **Question** | Any question the RFP poses (e.g., "Describe your approach to…", "How does your solution handle…") |
| **Mandatory Requirement** | Statements using *must*, *shall*, *required*, *mandatory*, *will be required to* |
| **Submission Rule** | How the proposal must be submitted (format, page limits, deadlines, file types, copies, labeling, volume structure) |
| **Evaluation Criterion** | Criteria, scoring weights, or factors used to evaluate proposals (e.g., "Price will account for 30% of the score") |
| **Administrative Certification** *(optional 5th — use when present)* | Representations & certifications, conflict-of-interest declarations, signatory authority, insurance/registration attestations, and similar pass/fail eligibility items |

### Fields to Record Per Item (write to the **RFP Tracker** list)

| Field | Value |
|---|---|
| **Item** | The requirement, question, or criterion text (verbatim or lightly trimmed) |
| **Category** | One of the five categories above |
| **Mandatory** | Yes / No — Yes for anything using obligatory language or marked required |
| **Source Location** | Page and/or section number in the source document |
| **Owner** | *(blank — assigned later by the team)* |
| **Status** | `Not Started` (default) |

---

## Step 3 — De-duplicate and Normalize

1. RFPs often restate the same requirement in multiple places. Merge obvious
   duplicates into one row, but keep both source locations in Source Location.
2. Split compound items — a sentence asking two distinct questions becomes two
   rows so each can be owned and answered separately.
3. Normalize phrasing for readability without changing meaning, but keep enough
   original wording that the row stays traceable to the document.

---

## Step 4 — Write to the RFP Tracker List

1. Create the **RFP Tracker** list items (or update existing ones on a re-run).
2. Place **Mandatory = Yes** rows at the top of the sort order if the view supports it.
3. Do not populate Available Content or Source columns — those are filled by the
   Content Finder skill in the next step of Phase 1.

---

## Step 5 — Report Back to the User

Provide a summary with:

- Total items extracted, split by category.
- Count of mandatory vs. non-mandatory items.
- Any solicitation metadata marked `NOT SPECIFIED` (if Step 1b ran).
- Any referenced attachments or addenda that could not be located.
- Any ambiguous items that may need human classification.
- Confirmation that the RFP Tracker list is populated, with a link to it.

### Example Summary Output

```
RFP Extraction complete — RFP Tracker populated.

Items extracted: 31
  • Questions:                 18
  • Mandatory Requirements:     7
  • Submission Rules:           4
  • Evaluation Criteria:        2
  • Administrative Certs:       0

Mandatory items: 9 (flagged and sorted to top)

Addenda processed: 1 (Addendum 2 moved the deadline +1 week — applied)

Items needing human classification: 2
  • Row 14 — compound item split into two questions
  • Row 22 — unclear whether procedural or content rule

RFP Tracker:
   https://contoso.sharepoint.com/sites/Proposals/Lists/RFPTracker

Next step: Run the Content Finder skill to match existing content to each row.
```

---

## Notes & Edge Cases

- **Scanned / image-only RFPs:** OCR first. Flag pages with low OCR confidence.
- **Conflicting addenda:** The latest one wins. Note the conflict in the summary.
- **No evaluation criteria stated:** Record this explicitly — the Strategy
  Synthesis skill needs to know weights are unstated so it can infer them.
- **Very large packages:** Extract from each document but write to a single
  tracker. Keep the source filename in Source Location so every row is traceable.
