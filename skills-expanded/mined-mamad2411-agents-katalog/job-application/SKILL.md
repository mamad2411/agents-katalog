---
name: job-application
description: Draft tailored resumes and cover letters, then generate PDF applications. Use when the user wants to apply for a job, create a resume, write a cover letter, generate an application PDF, or mentions a job description to apply for. Triggers on "apply for", "draft application", "job application", "resume", "cover letter", paste of a job description, or explicit /job-application invocation.
disable-model-invocation: false
---

# Job Application Skill

Draft tailored resumes and cover letters for a job application, then generate a single PDF with cover letter on page 1 and resume on page 2.

## Arguments

| Arg | Description | Required |
|-----|-------------|----------|
| **mode** | One of: `full` (default), `draft`, `pdf` | No (defaults to `full`) |
| **path** | Path to job description file, or company directory | Mode-dependent |

## Modes

### `full` (default) — End-to-end application

Drafts resume + cover letter, then generates PDF in one shot.

### `draft` — Draft only

Drafts resume.md and cover-letter.md without generating PDF.

### `pdf` — PDF only

Generates PDF from existing resume.md and cover-letter.md in an application directory.

## Usage

```
/job-application                           # full mode, paste JD in prompt
/job-application draft                     # draft only
/job-application pdf applications/company  # PDF from existing drafts
```

## Content Sources (Load Before Writing)

Before drafting, load these memory files if they exist:

- `$CLAUDE_CONFIG_DIR/memory/career-history.md` — Source material (NEVER fabricate beyond this)
- `$CLAUDE_CONFIG_DIR/memory/core-voice.md` — Voice fingerprint
- `$CLAUDE_CONFIG_DIR/memory/professional-voice-guide.md` — Professional overlay for cover letters
- `$CLAUDE_CONFIG_DIR/memory/write-like-a-human.md` — AI-tell prevention
- `$CLAUDE_CONFIG_DIR/memory/how-to-write-well.md` — Clarity rules

**Fallback (vanilla install — these files are personal and won't exist):** if
`career-history.md` is absent, ask the user for their career history (roles,
achievements, skills) and use their answer as the sole source material — still
never fabricate beyond what they provide. If the voice-overlay files
(`core-voice.md`, `professional-voice-guide.md`, `write-like-a-human.md`,
`how-to-write-well.md`) are absent, skip them and write in a clear, professional
default voice.

## Workflow

### Step 1: Extract JD & Map Keywords

Pull exact phrases from JD in these categories:
- Required skills (technologies, methodologies, tools)
- Soft skills (leadership style, collaboration patterns)
- Scope indicators (team sizes, revenue, scale)
- Industry terms (domain-specific language)

For each keyword, classify: EXACT MATCH, SYNONYM MATCH, PARTIAL MATCH, or GAP.

Flag callback triggers: recognizable companies, quantified achievements, rare skill combos, acquisition/IPO involvement.

### Step 2: Draft resume.md and cover-letter.md

Read `references/drafting-guide.md` for structure, authenticity constraints, and AI-tell detection.

Output directory: `./INBOX/applications/{company-name}/` if an `INBOX/` exists, else `./applications/{company-name}/` in the current directory (or ask the user where to write).

Save:
- `resume.md`
- `cover-letter.md`

### Step 3: Run ATS Checks

Read `references/ats-checks.md` and run ALL checks before saving.

If any check fails: report failures, fix, then save. Do not save failing applications.

### Step 4: Generate PDF (full and pdf modes)

**Dependency:** the PDF step requires `weasyprint` (`pip install weasyprint`) plus
its system libraries (Pango, Cairo, GDK-PixBuf — e.g. `brew install pango` on
macOS, `apt install libpango-1.0-0 libpangocairo-1.0-0` on Debian/Ubuntu). If
`weasyprint` isn't available, skip PDF generation, tell the user the drafted
`.md`/`.html` files are ready, and note "the PDF step requires weasyprint".

1. Read resume.md and cover-letter.md from application directory
2. Read the HTML template from `assets/application-template.html`
3. Generate `application.html`:
   - Page 1: cover letter (NO name header — starts with letter body)
   - Page 2: resume (semantic HTML classes from template)
4. Run: `weasyprint application.html "Resume - {Applicant Name} - {Company} {Year}.pdf"` (use the applicant's name if known, else ask)
5. Keep application.html for future style edits

### Step 5: Terminal Summary

Report:
- Top 3 keyword alignments
- Any gaps flagged
- Files created
- DO NOT output full document content to terminal

## Follow-up Handling

For style requests ("make font bigger", "reduce margins"):
1. Edit `<style>` block in application.html
2. Re-run weasyprint
3. Confirm change

## Resources

- `references/drafting-guide.md` — Resume/cover letter structure, authenticity constraints, AI-tell detection
- `references/ats-checks.md` — ATS screening optimization, positioning strategy, pre-delivery checklist
- `assets/application-template.html` — HTML/CSS template for PDF generation
