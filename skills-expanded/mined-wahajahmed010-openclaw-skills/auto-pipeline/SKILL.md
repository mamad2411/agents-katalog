---
name: auto-pipeline
description: Full automatic pipeline — paste a JD URL or text and get evaluation, report, PDF, draft answers, and tracker entry. Triggers on auto-pipeline, full pipeline, evaluate and apply, end to end.
---

# Auto-Pipeline — Full Automatic Pipeline

Read `~/.openclaw/workspace/skills/career-ops/references/scoring-system.md` first.

## Data Paths

- CV: `~/.openclaw/workspace/career-ops-data/cv.md`
- Profile: `~/.openclaw/workspace/career-ops-data/config/profile.yml`
- Reports: `~/.openclaw/workspace/career-ops-data/reports/`
- Tracker: `~/.openclaw/workspace/career-ops-data/data/applications.md`
- Output: `~/.openclaw/workspace/career-ops-data/output/`

## Workflow

### Step 0 — Extract JD

If URL: Use Playwright (preferred) → WebFetch (fallback) → WebSearch (last resort). If text: use directly.

### Step 1 — A-G Evaluation

Execute full evaluation (see evaluate skill). Include Block G Legitimacy.

### Step 2 — Save Report

Save full evaluation in `reports/{###}-{company-slug}-{YYYY-MM-DD}.md`. Include **URL:** and **Legitimacy:** in header.

### Step 3 — Generate PDF

Read `config/profile.yml`. Check `cv.output_format`:
- If `"latex"`, execute LaTeX pipeline (see latex skill)
- Otherwise, execute HTML/PDF pipeline (see pdf skill)

Run: `node ~/.openclaw/workspace/skills/career-ops/scripts/generate-pdf.mjs`

### Step 4 — Draft Application Answers (only if score >= 4.5)

If score >= 4.5:
1. Extract form questions (Playwright or generic)
2. Generate responses following "I'm choosing you" tone
3. Save as section H in the report

**Tone rules:**
- Confident without arrogance
- Specific and concrete — reference something REAL from JD and something REAL from CV
- Direct, no fluff, 2-4 sentences per response
- The hook is the proof, not the statement

### Step 5 — Update Tracker

Record in `data/applications.md` with all columns. If any step fails, continue and mark as pending.

## German Mode

Read `references/german-locale.md` for DACH-specific checks.