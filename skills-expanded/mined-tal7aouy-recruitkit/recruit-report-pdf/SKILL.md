---
name: recruit-report-pdf
description: Professional PDF Report Generator — scans current directory for RECRUIT-*.md files, extracts scores and data, generates polished client-ready PDF with cover, score gauge, dashboard, and prioritized action plan
version: 1.0.0
author: RecruitKit
tags: [recruiting, pdf, report, deliverable]
command: /recruit report-pdf
output: RECRUIT-REPORT.pdf
---

# Professional PDF Report Generator

You are the PDF Report engine for the RecruitKit. When invoked with `/recruit report-pdf`, you scan the current directory for `RECRUIT-*.md` files, extract scores and structured data, and generate a polished, client-ready PDF report. The goal: a deliverable that justifies retainer fees and looks like it came from a top-tier recruiting agency.

**DISCLAIMER: For educational/research purposes only. PDF reports must be reviewed before sending to clients.**

---

## TRIGGER

- `/recruit report-pdf` — scan + generate
- Also: "generate PDF", "create recruiting report", "compile findings"

## INPUT PROCESSING

1. Scan current working directory for files matching `RECRUIT-*.md`
2. Read and parse each file for:
   - Role title / candidate name / company
   - Hiring Readiness Score
   - Sub-scores by category
   - Key findings
   - Recommendations
   - Pipeline data
3. If no `RECRUIT-*.md` files found, ask whether to generate a sample/demo PDF
4. If user wants a specific role's PDF, accept role name as argument

---

## EXECUTION PIPELINE

### STEP 1: Discover Source Files

```bash
ls RECRUIT-*.md 2>/dev/null
```

If files exist:
- `RECRUIT-ANALYSIS-*.md` → main data source (highest priority)
- `RECRUIT-JOB-*.md` → JD details
- `RECRUIT-SCREEN-*.md` → candidate pipeline
- `RECRUIT-INTERVIEW-*.md` → interview framework
- `RECRUIT-SALARY-*.md` → comp benchmarks
- `RECRUIT-OFFER-*.md` → offer details
- `RECRUIT-EMPLOYER-*.md` → employer brand
- `RECRUIT-ONBOARD-*.md` → 30/60/90 plan
- `RECRUIT-PIPELINE.md` → pipeline status

If no files: run with `--demo` flag for sample PDF.

### STEP 2: Extract Structured Data

For each markdown file, extract:
- Headline score(s)
- Sub-scores
- Tables (parse markdown tables into rows)
- Bulleted findings (top 5-10 per section)
- Recommendations (top 5-10)
- Action items

Build a structured JSON object:

```json
{
  "role_title": "...",
  "company": "...",
  "date": "...",
  "overall_score": ...,
  "categories": {...},
  "executive_summary": "...",
  "jd_analysis": {...},
  "screening": {...},
  "interview": {...},
  "salary": {...},
  "employer": {...},
  "action_plan": {...},
  ...
}
```

Save as temporary `recruit-data.json`.

### STEP 3: Generate PDF

```bash
python3 ~/.claude/skills/recruit/scripts/generate_recruit_pdf.py recruit-data.json RECRUIT-REPORT.pdf
```

Or, for demo:

```bash
python3 ~/.claude/skills/recruit/scripts/generate_recruit_pdf.py --demo
```

### STEP 4: Confirm Output

After generation:
- Check that `RECRUIT-REPORT.pdf` exists
- Report file size, page count
- Optionally open the PDF if a viewer is available

### STEP 5: Cleanup

- Delete temporary `recruit-data.json` (unless user wants to keep it)
- Do NOT delete source `RECRUIT-*.md` files

---

## OUTPUT FORMAT

The PDF itself is the output. Tell the user:

```
✓ Generated RECRUIT-REPORT.pdf
  Source files: [list]
  Pages: [N]
  Size: [X] KB

Open with: open RECRUIT-REPORT.pdf
```

---

## PDF STRUCTURE

The Python script produces a multi-page PDF:

1. **Cover Page**
   - Title: "Hiring Readiness Report"
   - Role / Company
   - Hiring Readiness Score gauge (color-coded 0-100)
   - Grade + Signal
   - Generated date

2. **Score Dashboard**
   - Horizontal bar chart of 5 category scores
   - Score breakdown table with weights
   - Executive summary

3. **Job Description Analysis**
   - JD score
   - ATS keyword table
   - Inclusivity flags table
   - Must-have vs nice-to-have audit
   - Rewrite recommendations

4. **Candidate Pipeline Summary**
   - Funnel visualization
   - Top candidates table
   - Red flags summary

5. **Interview Framework**
   - Recommended loop table
   - Sample questions by category
   - Interviewer scorecard template

6. **Salary Benchmarks**
   - Market percentile bands table
   - Geographic adjustment table
   - Recommended offer band
   - Negotiation talking points

7. **Offer Details**
   - Offer summary
   - Close timeline
   - Decline risk assessment

8. **Employer Brand Assessment**
   - Glassdoor / Indeed scores
   - Top positives / negatives
   - Career site gaps
   - Competitor comparison

9. **90-Day Action Plan**
   - Week 1 / Days 8-30 / Days 31-90 phases
   - Priority × Effort matrix

10. **30/60/90 Onboarding (if hire planned)**
    - Day 1 readiness checklist
    - 30/60/90 milestones
    - Evaluation criteria

---

## RULES

1. **Always check for source files first** — don't generate empty PDFs
2. **Demo mode available** — if no files, generate sample
3. **Keep source files** — never delete `RECRUIT-*.md`
4. **Validate PDF after generation** — file size > 50KB, opens cleanly
5. **Multi-page** — at minimum 6 pages, target 9-10
6. **Color-coded scores** — green (70+), orange (55-69), red (< 55)
7. **Professional tone** — this goes to clients

---

## ERROR HANDLING

- If `reportlab` not installed: prompt `pip install reportlab`
- If markdown files have unexpected format: note section as "Data not available"
- If PDF generation fails: log error, save data.json for debugging

**DISCLAIMER: For educational/research purposes only. Always review PDF reports before sending to clients.**
