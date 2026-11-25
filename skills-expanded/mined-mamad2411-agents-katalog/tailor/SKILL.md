---
name: tailor
description: Analyze resume gaps against a job description and suggest targeted rewrites. Truth-preserving — never fabricates experience.
---

# /tailor -- JD-Targeted Resume Optimization

Analyze a resume against a specific job description, identify keyword gaps, and suggest truth-preserving rewrites that improve ATS match rate.

## CRITICAL: Truth-Preserving Mandate

NEVER suggest adding experience, skills, or achievements the user doesn't have.
Every rewrite suggestion MUST include a confidence note reminding the user to only
apply changes that reflect their actual experience. "Only add X if you actually
did/used X" is required on every suggestion that introduces a new keyword.

If a keyword gap cannot be addressed with existing experience, flag it as
unresolvable -- do NOT fabricate or stretch the truth.

## Workflow

Follow these steps in order. Use the "flag and continue" model throughout: deliver
the FULL report without pausing to interview the user mid-analysis.

### Step 1 -- Collect the Resume

Ask the user for their resume. Accept any of these formats:

- **Paste**: "Paste your resume text below."
- **File path**: Read the file from disk (`.txt`, `.md`, or similar text formats).
- **Krafter resume ID**: If the user provides a Krafter resume ID (UUID format), use the `get_resume` tool to fetch it. The ID may come from a URL like `https://app.getkrafter.com/resume/<id>`.

Store the raw resume text for tool input. If fetched from Krafter, also store the
resume ID for later use with `score_krafter_resume`.

### Step 2 -- Collect the Job Description (REQUIRED)

Prompt: "Paste the job description you're targeting. This is required for tailoring."

The job description is **mandatory** for the `/tailor` skill. If the user tries to
proceed without one, remind them that tailoring requires a JD to compare against.

Store the raw JD text as `jdText`.

### Step 3 -- Parse the Resume

Build the internal `ResumeData` structure from the raw resume text:

- Split into lines.
- Lines starting with bullet markers (`-`, `*`, numbered lists) are extracted as **bullets** (strip the marker).
- Short ALL-CAPS or Title-Case lines (under 50 characters) are extracted as **section headings**.
- Everything feeds into `rawText`.

If the resume came from Krafter (Step 1), skip manual parsing -- the tools handle
transformation internally via `toResumeData`.

### Step 4 -- Run Scoring Tools

Run **both** scoring tools to get the full picture. Choose the method that matches your environment:

**Option A — MCP tools available** (user has the MCP server configured):

For pasted/file resumes:
1. `score_ats` with `{ resumeText, jdText }` -- returns `ATSResult` with `score`, `matched`, `missing`, and `details` breakdown.
2. `score_resume` with `{ resumeText, jdText }` -- returns `ResumeScore` with `total`, `mode`, `breakdown`, `ats`, and `flags`.

For Krafter resumes:
1. `score_krafter_resume` with `{ id, jdText }` -- returns the full `ResumeScore` including the embedded `ATSResult`.

**Option B — CLI** (no MCP server needed):

1. Write the resume text to `/tmp/resume.txt` and the JD to `/tmp/jd.txt`. Use **plain text** — no markdown formatting, no `#` headings. Preserve bullet markers (`-`, `•`, `*`) from the original document as-is.
2. Run both commands:

```bash
# Full score with ATS:
npx @getkrafter/resume-toolkit score --resume /tmp/resume.txt --jd /tmp/jd.txt

# Standalone ATS analysis:
npx @getkrafter/resume-toolkit ats --resume /tmp/resume.txt --jd /tmp/jd.txt
```

Parse the JSON output from each command and continue to Step 5.

### Step 5 -- Gap Analysis

For **each missing keyword/term** from the ATS result:

1. **Search the resume** for related experience that could be reframed. Look for:
   - Synonyms or adjacent concepts (e.g., "container orchestration" relates to "Kubernetes")
   - Implicit skills (e.g., "built CI/CD pipelines" implies familiarity with automation tools)
   - Bullets that describe the activity without naming the specific technology

2. **If related experience exists**: mark as a **resolvable gap** -- the user's resume
   already contains evidence that could be reworded to surface the missing keyword.

3. **If no related experience exists**: mark as an **unresolvable gap** -- the keyword
   requires experience the resume does not reflect.

### Step 6 -- Generate Rewrite Suggestions

For each **resolvable gap**, produce a Before/After rewrite suggestion:

```
### [Missing Keyword]

**Before:** Led team of 8 engineers to deliver platform
**After:** Led team of 8 engineers to deliver microservices platform using Kubernetes
**Confidence:** Only add "Kubernetes" if you actually used it in this role
```

Rules for rewrites:
- Show the **exact original bullet** as "Before".
- Show a **minimal edit** as "After" -- change as few words as possible to incorporate the keyword naturally.
- Include a **Confidence** note on every single rewrite that introduces a new keyword. The note MUST say "Only add [keyword] if you actually [did/used/worked with] [keyword]".
- Prefer surfacing keywords that are already implicit rather than adding entirely new claims.
- If a single bullet could address multiple missing keywords, show one rewrite per keyword -- do not overload a single suggestion.

### Step 7 -- Flag Unresolvable Gaps

For each **unresolvable gap**, produce a gap notice:

```
### [Missing Keyword]

**Gap:** [Keyword] -- This JD requires [keyword] experience. Consider adding this
if you have relevant experience, even from side projects, coursework, or
certifications.
```

Frame these as opportunities, not failures. Suggest concrete places the user
could gain or demonstrate the skill (side projects, certifications, open source
contributions).

### Step 8 -- Present the Full Report

Compile everything into a single, structured report. Do NOT pause to ask
questions -- deliver the complete analysis in one response.

#### Report Structure

```
## Tailoring Report: [Job Title from JD]

### Current Scores
- **Overall Quality:** X/100 (mode: with-jd)
- **ATS Keyword Match:** Y/100
- **Breakdown:**
  - Quantification: X/100 (weight: 25%)
  - Verb Strength: X/100 (weight: 20%)
  - ATS Match: X/100 (weight: 30%)
  - Bullet Structure: X/100 (weight: 15%)
  - Section Completeness: X/100 (weight: 10%)

### Matched Keywords (What's Working)
List all matched keywords from the ATS result. Group by bigrams and unigrams
if the list is long. This shows the user what they're already doing well.

### Diagnostic Flags
List any flags from the scorer (e.g., "Fewer than 40% of bullets contain
measurable results", "No summary/profile section found").

### Suggested Rewrites (Resolvable Gaps)
[One subsection per resolvable gap, using the Before/After/Confidence format
from Step 6]

### Unresolvable Gaps
[One subsection per unresolvable gap, using the Gap format from Step 7]

### Projected Impact
Implementing these changes could improve your ATS match from X% to ~Y%.

Calculate the projected Y% by assuming all resolvable gap keywords would become
matched. The formula:
- Current matched = number of matched terms
- Projected matched = current matched + number of resolvable gaps
- Total JD terms = matched + missing
- Projected score = round((projected matched points / total points) * 100)

Use bigram weight (1.5) and unigram weight (1.0) for accurate projection.

### Action Items
Numbered list of concrete next steps:
1. Apply the suggested rewrites (after verifying accuracy)
2. Address any structural issues flagged by the scorer
3. Consider ways to fill unresolvable gaps (courses, projects, certifications)
4. Re-run /score after making changes to verify improvement
```

## Tone and Formatting

- Be constructive and actionable -- frame everything as improvement opportunity
- Use the Before/After format consistently for every suggestion
- Always include the Confidence note -- no exceptions
- Use bullet points and clear hierarchy for scanability
- Keep language professional but encouraging
- Frame gaps as opportunities, not failures or shortcomings
- Be specific: name the exact bullet, the exact keyword, and the exact change

## Edge Cases

- **Very short resume (< 50 words):** Flag that the resume is too short for meaningful tailoring. Suggest building out content first, then re-running `/tailor`.
- **JD is too short or vague:** Flag that the JD lacks specific keywords. Provide what analysis you can, but note the limited data.
- **Perfect ATS match (100%):** Congratulate the user. Focus the report on the other quality dimensions (quantification, verb strength, bullet structure) instead.
- **Zero matched keywords:** This usually means a major career pivot or wrong resume. Flag it clearly and suggest whether tailoring is the right approach vs. a full rewrite.
- **Krafter resume fetch fails:** Fall back to asking the user to paste the resume text directly.

## Tool Reference

| Tool | Input | Output |
|------|-------|--------|
| `score_ats` | `{ resumeText: string, jdText: string }` | `ATSResult { score, matched[], missing[], details }` |
| `score_resume` | `{ resumeText: string, jdText?: string }` | `ResumeScore { total, mode, breakdown, ats, flags[] }` |
| `score_krafter_resume` | `{ id: string, jdText?: string }` | `ResumeScore { total, mode, breakdown, ats, flags[] }` |
| `get_resume` | `{ id: string }` | Krafter resume object (JSON) |
