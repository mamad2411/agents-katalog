---
name: ATS Resume Checker
description: Diagnose and fix ATS parsing failures in resumes. Use this skill whenever someone mentions ATS, applicant tracking, resume rejection, keyword matching, resume scanning, parsing errors, or wonders why they are not getting callbacks. Also trigger for general resume optimization requests, resume file format questions, or when a user uploads a resume and mentions job applications.
---

# ATS Resume Checker

Diagnose why a resume fails automated screening and fix it.

## How ATS Systems Work

Applicant Tracking Systems extract text from uploaded documents, parse it into structured fields (name, email, employer, title, dates, skills), then score the parsed data against the job requisition. Failures happen at three layers: file extraction, structural parsing, and keyword scoring.

## Diagnostic Checklist

Run through each layer in order. Stop and fix before moving to the next.

### Layer 1: File Extraction

The system must be able to read the file at all.

**Pass criteria:**
- File is .docx or a text-layer PDF (not a scanned image)
- No password protection or form fields
- File size under 5 MB
- Filename uses only alphanumeric characters, hyphens, and underscores

**Common failures:**
- PDF exported from Canva or Photoshop as flattened image: text is invisible to parsers
- .pages or .odt format: most ATS reject outright
- Filename like "resume (2) FINAL.pdf": some systems choke on parentheses and spaces

**Fix:** Export from Word as .docx. If PDF is required, print-to-PDF from Word so the text layer is preserved. Name the file `FirstnameLastname_Resume.pdf`.

### Layer 2: Structural Parsing

The system must map content to the right fields.

**Pass criteria:**
- Contact info is in the document body, not in a header, footer, or text box
- Single-column layout with no tables used for positioning
- Section headings use standard labels the parser recognizes
- Dates follow a consistent format throughout
- No content is embedded in images, charts, icons, or shapes

**Standard section labels** (use these exact words):
- Professional Experience, Work Experience, or Experience
- Education
- Skills, Technical Skills, or Core Skills
- Professional Summary or Summary
- Certifications
- Projects

**Risky labels** (parsers may not recognize):
- "Where I Have Made an Impact" instead of Experience
- "My Toolbox" instead of Skills
- "Learning Journey" instead of Education

**Fix:** Replace creative headings with standard ones. Move contact information out of header/footer into the first lines of the document body. Remove all tables, text boxes, and multi-column layouts. Use simple bullet characters (a round bullet, a hyphen, or an asterisk).

### Layer 3: Keyword Scoring

The system compares parsed skills and phrases against the job requisition.

**Process:**
1. Extract every distinct requirement from the job posting
2. Classify each as Required or Preferred based on language cues
3. Check whether the resume contains each keyword or a close synonym
4. Calculate match percentage: (matched keywords / total required keywords) x 100

**Language cues for Required:** "must have", "required", "X+ years of", listed under Requirements, repeated 3+ times in the posting.

**Language cues for Preferred:** "nice to have", "bonus", "ideally", "preferred", listed under Preferred Qualifications.

**Target:** 80%+ match on required keywords for a strong submission.

**Keyword placement priority:**
1. Summary section: include 5-8 top keywords naturally
2. Skills section: list keywords explicitly using exact phrasing from the posting
3. Experience bullets: weave keywords into achievement statements
4. Repeat critical keywords 2-3 times across different sections without stuffing

**Synonym traps:** If the posting says "stakeholder management" and the resume says "working with teams", the parser will not match. Use the exact phrase from the posting when it accurately describes your work.

## Output Template

When checking a resume, produce this report:

```
ATS DIAGNOSTIC REPORT

FILE CHECK
- Format: [pass/fail + detail]
- Text extraction: [pass/fail]
- Filename: [pass/fail]

STRUCTURE CHECK
- Contact info location: [pass/fail]
- Layout type: [pass/fail]
- Section headings: [list each heading + pass/fail]
- Date consistency: [pass/fail]
- Embedded graphics: [pass/fail]

KEYWORD MATCH (against provided job posting)
Required keywords: X/Y matched (Z%)
  Matched: [list]
  Missing: [list with suggested placement]
Preferred keywords: X/Y matched (Z%)
  Matched: [list]
  Missing: [list]

ESTIMATED SCORE: X%
TARGET: 80%+

PRIORITY FIXES (ordered by impact)
1. [highest impact fix]
2. [next fix]
3. [next fix]
```

## Things to Never Do

- Do not add skills the person does not actually have
- Do not repeat the same keyword more than 4 times
- Do not sacrifice readability for keyword density
- Do not use invisible or white-colored text to hide keywords
