---
name: resume-ats-review
description: Analyze an attached resume or CV PDF, produce a heuristic ATS score with category breakdowns, and give prioritized fix instructions. Use when the user attaches a resume/CV and asks to analyze, ATS-score, critique, or improve it. Optional job description or target role tailors keyword gaps. Default is critique-only — do not rewrite wording unless asked.
category: career
risk: safe
source: community
date_added: "2026-09-14"
---

# Resume ATS Review

When this skill is invoked with a resume PDF (and optionally a job description), run a full international ATS review in one response.

## When to use

- User attaches a resume/CV PDF and says “analyze this,” “ATS score,” “critique my CV,” or similar.
- User is reviewing their own resume or a friend’s. Treat every new PDF as an independent review.
- Language of the PDF does not matter. Apply **international / US-UK ATS** rules even if the file is in French or another language. Do not apply francophone CV customs (photo, age, nationality as “normal”).

## When not to use

- The user wants you to write a resume from scratch with no PDF.
- The user only wants LinkedIn headline help, cover letters, or interview prep (unless they also attached a resume to score).

## Hard rules

- **Critique only by default.** Do not rewrite bullets, summaries, or a full CV unless the user explicitly asks in this or a follow-up message.
- **Do not invent** jobs, dates, metrics, skills, employers, or achievements. If unclear, ask or mark unknown.
- **Do not dump** the full resume text back.
- **Do not store, copy, or commit** the PDF or its contents into the repo or skill library.
- **Fail closed** if the PDF is missing, empty, scanned-with-no-readable-text, or otherwise unreadable. Do **not** invent a score. Say what failed and how to retry (export as a text-based PDF, higher-resolution scan, attach the file again).
- **One PDF per run.** If several resumes are attached, ask which to score. If one PDF plus a job description, analyze the PDF against the JD.
- **Heuristic, not a vendor.** Label the score as a heuristic rubric, not Workday, Greenhouse, Taleo, or any named ATS simulation.
- **Report language** follows the user’s chat language (typically English). Quote short original phrases only as evidence.
- **New PDF = clean slate.** Do not carry facts from a previous friend’s resume into this review.

## Workflow

1. Confirm a resume PDF is attached. If not, ask for it.
2. Read the **entire** document: header/contact, every section, dates, skills, education, extras, and visible layout (columns, tables, icons, images, headers/footers).
3. Map sections you actually see. Do not assume missing sections exist.
4. If a job title or job description is present, use it for the keywords category. If not, score generic ATS/recruiter readiness and say “no JD provided.”
5. Score each category with **one evidence line** tied to something in the PDF.
6. Compute the weighted overall score (0–100). Pick the band.
7. Write the report using the template below. Put the **top 5 highest-impact fixes** where they cannot be missed (P0 first).
8. End with a one-line offer to rewrite bullets or a full Markdown CV **only if they ask**.

## Scoring rubric (weights must sum to 100)

### Parseability — 25 points

Selectable text; single column preferred; standard headings (Experience, Education, Skills, or clear equivalents); no critical content in images, icons-as-headings, or headers/footers; tables and multi-column layouts are risks.

Deductions (examples, stack as needed, floor at 0):

- Text not selectable / image-only PDF: fail closed (no score) if nothing can be read; otherwise heavy deduction.
- Multi-column or table-based layout: −8 to −15.
- Icons or graphics used as section labels: −5 to −10.
- Contact or dates only in header/footer: −5 to −10.
- Unusual fonts, text boxes, or design that likely scrambles parse order: −5 to −10.

### Structure and completeness — 20 points

Contact method; experience; education; skills; reverse-chronological dates; consistent formatting and date style.

Deductions:

- Missing email or phone/LinkedIn-equivalent contact: −4 to −8.
- Missing experience, education, or skills section when expected for the seniority: −4 to −8 each.
- Dates missing, inconsistent, or not reverse-chronological: −3 to −8.
- Wild formatting inconsistency (mixed bullets, heading styles): −3 to −6.

### Impact evidence — 20 points

Bullets show scope, tools, and outcomes. Flag missing metrics **without inventing numbers and without rewriting**.

Deductions:

- Duties-only bullets with no outcomes: −8 to −14.
- No tools, scale, or context: −4 to −8.
- Summary/objective is generic filler: −2 to −5.

### Keywords and targeting — 20 points

- **No JD:** skills density, standard role vocabulary, avoid keyword stuffing. Score generic readiness.
- **JD present:** match must-have requirements vs the PDF. List gaps. Do not add keywords the person never evidenced.

Deductions:

- Skills section missing or too vague: −5 to −10.
- JD attached but weak overlap on must-haves: −8 to −16.
- Keyword stuffing / unreadable skill walls: −4 to −8.

### Recruiter skim — 15 points

Length (~1 page early career, ~2 pages senior — call out, do not hard-fail); top-third signal (role, strength, not a photo); noise (photos, charts, skill bars, personal details that international ATS/privacy practice flags).

Deductions:

- Photo, headshot, or decorative graphics: −4 to −8.
- Age, nationality, marital status, or similar personal data: −3 to −6.
- Weak or missing top-of-page target role/summary: −3 to −6.
- Far too long or cramped/unreadable: −3 to −6.

### Overall score and bands

`overall = round(parseability + structure + impact + keywords + skim)` using the points awarded in each category (each category score is out of its weight).

- **90–100:** Strong ATS-ready; remaining issues are polish.
- **75–89:** Usable; clear gaps to fix before applying widely.
- **60–74:** Likely parse or skim problems; fix P0 before sending.
- **0–59:** High risk of being dropped or ignored.

Every deduction must map to a concrete observation. No unexplained numbers.

## Report template (always use this order)

### 1. Verdict

- Overall score / 100
- Band name
- One sentence on the main risk or strength

State that this is a **heuristic ATS-readiness score**, not a named vendor.

### 2. Category scores

For each category: points awarded / weight, then one evidence line.

### 3. What’s already working

3–6 bullets of real strengths from the PDF.

### 4. Prioritized fixes

Group as **P0 must-fix**, **P1 should-fix**, **P2 polish**.

Each item:

- **Observation** (what is in the file)
- **Why it matters** (ATS parse, recruiter skim, or targeting)
- **What to change** — an **instruction**, not replacement wording  
  Example: “Quantify the checkout project (orders/day, conversion, or latency). Do not invent a number if you do not have one.”

The first five P0/P1 items should be the highest-impact list (SC-002).

### 5. ATS parse risks

Explicit layout/parse issues, or “none material.”

### 6. Job-target gaps

Either a gap list against the JD/role, or the line: `No job description provided — keywords scored for generic ATS/recruiter readiness.`

### 7. Open questions

Missing dates, unclear titles, unreadable fragments. If none, say so.

### 8. Footer

`Ask if you want rewritten bullets or a full Markdown CV. I will not draft wording unless you ask.`

## Error templates

**No file:** “Attach a resume PDF and ask again (for example: analyze this).”

**Unreadable:** “I could not read text from this PDF (likely a scan or image-only export). Export a text-based PDF or a higher-resolution scan and re-attach. I am not assigning an ATS score.”

**Multiple resumes:** “I see more than one resume. Which file should I score?”

## Optional follow-up (only if asked)

If the user asks to rewrite:

- Still do not invent facts.
- Prefer in-place bullet rewrites and a structured Markdown CV they can paste into Word/Docs.
- Keep international ATS layout: single column, standard headings, no tables/icons as structure.

## Examples of invocation the skill should handle

- PDF attached + “analyze this”
- PDF attached + “ATS score this resume”
- PDF + pasted job description + “how does this fit”
- Friend’s PDF + “critique only, don’t rewrite”
