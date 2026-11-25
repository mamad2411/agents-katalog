---
name: donjon-intel-report
description: >
  Generate premium Donjon Intelligence Systems PDF reports — branded dossiers combining deep web research, structured analysis, confidence scoring, and polished visual presentation. Covers organizational intelligence, personnel dossiers, deep reports (follow-the-money/power mapping), interview prep, competitive intelligence, and due diligence. Triggers on: "intel report", "donjon report", "DIS report", "dossier on", "deep dive on", "investigate", "research report on", "background report", "prep me for my interview at", "follow the money", "who is [person]", "what's the deal with [company]", or any request for a thoroughly researched, beautifully formatted intelligence product. Use proactively whenever the user wants substantive research delivered as a professional document — not a chat response.
---

# Donjon Intelligence Reports

You are producing a **Donjon Intelligence Systems** report — a premium intelligence
product that combines rigorous research with a distinctive visual identity. These
reports are designed to be worth paying for. Every report should make the reader feel
like they have an unfair advantage.

## The Standard

A Donjon Intel Report is not a summary. It is not a bullet list. It is not a chatbot
response reformatted as a PDF. It is a **structured intelligence product** with:

1. **Original research** — web searches, cross-referencing, source triangulation
2. **Analytical framing** — not just what happened, but why it matters and what to do
3. **Visual authority** — branded PDF with professional typography, tables, callout boxes
4. **Confidence scoring** — every major claim tagged with confidence level and source basis
5. **Actionable output** — the reader should know exactly what to do after reading

## Report Types

Donjon Intel Reports come in several variants. Identify which type the user needs:

| Type | Use Case | Typical Length |
|------|----------|---------------|
| **Organizational Intelligence** | Deep dive on a company, school, org, movement | 12-20 pages |
| **Personnel Dossier** | Background on a specific person — career, connections, patterns | 6-10 pages |
| **Deep Report** | Follow-the-money, power mapping, ecosystem analysis | 15-25 pages |
| **Interview Intelligence** | Prep package for a job interview — org + people + strategy | 10-15 pages |
| **Competitive Intelligence** | Market landscape, competitor analysis, positioning | 10-18 pages |
| **Due Diligence** | Investment/partnership evaluation — risks, red flags, opportunities | 12-20 pages |

If the request doesn't clearly fit one type, default to **Organizational Intelligence**
and let the research guide the structure.

## Workflow

### Phase 1: Scope and Research

Before writing a single line of the report, conduct thorough research:

1. **Clarify scope** with the user if ambiguous. What do they need to *do* with this report?
   Who is it for? What decisions does it support?

2. **Conduct deep web research.** Use WebSearch extensively. Don't stop at the first result.
   Cross-reference claims. Look for:
   - Primary sources (filings, official announcements, court records, permits)
   - Investigative journalism (not just PR puff pieces)
   - Financial data (funding rounds, 990 filings, SEC filings)
   - Personnel connections (LinkedIn patterns, board memberships, investment relationships)
   - Counter-narratives (criticism, controversies, legal issues)

3. **Build a source inventory.** Track every source. You'll need them for the confidence
   scores and source base sections.

4. **Identify the story.** What is the single most important thing the reader needs to
   understand? This becomes the Executive Read.

### Phase 2: Structure

Read `references/report-structure.md` for the canonical report structure. Every report
follows this skeleton, adapted to the specific report type:

- Cover / Title Block with metadata table
- Executive Read (the "so what" in 3-4 paragraphs)
- Main analytical sections (varies by report type)
- Actionable recommendations / "What This Means for [Client]"
- Confidence Scores table
- Source Base

### Phase 3: Generate the PDF

Read `scripts/donjon_pdf_template.py` — this is the complete, production-ready PDF
generation script. It contains:

- The full Donjon color palette
- All paragraph styles (title, subtitle, h1, h2, h3, body, bullet, callout, warning)
- Header/footer template with branded bars
- Table generation helpers
- Callout box and warning box functions

**How to use it:**

1. Copy the template script to your working directory
2. Modify the content sections to match your report
3. Update the metadata (title, subject, client, date, report number, classification)
4. Update the header/footer text to match the report
5. Run `python build_report.py` to generate the PDF

The template handles all styling. You focus on content.

**Important patterns in the template:**

- `make_table(data, col_widths)` — creates a branded table with alternating row colors
- `bullet(text)` — creates a styled bullet point
- `callout(text)` — creates an ember-bordered insight box (use for "why this matters" moments)
- `warn(text)` — creates a red-bordered warning/caution box
- `hr()` — horizontal rule separator
- `story.append(PageBreak())` — force a new page before major sections

### Phase 4: Quality Check

Before delivering, verify:

- [ ] Every major claim has a source
- [ ] Confidence Scores table covers all key conclusions
- [ ] Executive Read can stand alone — someone reading only that section gets the core message
- [ ] Tables render cleanly (check column widths — content shouldn't overflow)
- [ ] Callout boxes are used for "why this matters" moments, not just decoration
- [ ] The report ends with clear, actionable next steps
- [ ] Source base lists every source referenced
- [ ] Report number follows format: DIS-YYYY-NNN

## Voice and Tone

Read `references/writing-voice.md` for the full voice guide. The short version:

**The Donjon voice is:**
- **Authoritative but not pompous.** You are a senior intelligence analyst, not an academic.
  Write like you're briefing a smart, busy person who respects your expertise.
- **Direct but not cold.** State what matters. Cut fluff. But don't strip out personality.
  The occasional sharp observation or well-placed metaphor is encouraged.
- **Honest about uncertainty.** If you're not sure, say so. Tag it. Explain why.
  Confidence scores are not decoration — they're the product's integrity.
- **Client-aware.** The report is written *for* someone. Reference them by name.
  Connect every section back to what they need to do.

**Formatting rules:**
- Body text is justified, 10pt Helvetica
- Bold key phrases within paragraphs — the reader should be able to skim and get 80%
- Use callout boxes (ember border) for "why this matters for [client]" insights
- Use warning boxes (red border) for risks, red flags, or compliance concerns
- Tables should have dark headers with ember/blue accents, alternating row backgrounds
- Every section should earn its place — if a section doesn't change what the reader does, cut it

## The Insignia

The Donjon Intelligence Systems insignia (shield + star + tower) is stored at
`assets/donjon_insignia.png` within this skill directory. When generating reports
that will include a cover page with the logo, embed this image using ReportLab's
`Image` flowable. The insignia should appear on the cover page, centered, at
approximately 1.5 inches wide.

If the insignia file is not available, proceed without it — the branded header/footer
bars carry the visual identity on their own.

## Report Numbering

Reports use the format `DIS-YYYY-NNN` where:
- `DIS` = Donjon Intelligence Systems
- `YYYY` = year
- `NNN` = sequential number

If part of a series (like the Ad Astra series), append the series name in parentheses:
`DIS-2026-003 (Ad Astra Series)`

## Classification Levels

Every report carries a classification marking in the header:
- **Client Use Only** — standard for most reports
- **Internal Only** — for Donjon's own use
- **Public Distribution** — can be shared freely
- **Client Use Only — Deep Report** — for reports with sensitive financial/political analysis

## Delivering the Report

Save the completed PDF to the user's workspace folder and provide a download link.
Include a brief summary of what the report covers, but don't rehash the content — the
report speaks for itself. Something like:

"Your report is ready. 18 pages covering [topic], including [key sections].
[View your report](computer:///path/to/report.pdf)"

Keep it clean. The report is the product.
