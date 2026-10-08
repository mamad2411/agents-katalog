---
name: prep-apply
description: "Discover jobs, tailor resumes, and present a list of ready-to-apply jobs with clickable links. Simon applies manually with Simplify, then reports back for tracking. Triggers on: 'prep apply', 'prepare applications', 'find and tailor', 'get jobs ready'."
---

# Prep Apply

> **Read this file fresh every time. Do not rely on memory.**

Simplified pipeline: discover → tailor → present links → Simon applies → track.

No browser automation for form filling. Simon uses Simplify Copilot to fill forms manually.

## Prerequisites

- `jobs.db` initialized: `python3 ~/work/personal/jobs/.claude/scripts/jobs_db.py init`
- `~/work/personal/jobs/full-time/form_profile.md` exists
- `~/work/personal/jobs/.env` exists with JOBDITTO credentials
- `typst` installed for PDF compilation
- `claude` CLI available for tailor agents

## Step 1: Discover Jobs

Read and execute the find-jobs skill:
```
Read ~/.openclaw/workspace/.claude/skills/find-jobs/SKILL.md and ALL source guides in sources/
Execute it — scrape all sources, insert into jobs.db
```

Report: "Discovery complete — {N} new jobs found"

## Step 2: Rank + Pre-screen

```bash
python3 ~/work/personal/jobs/.claude/scripts/jobs_db.py rescore
python3 ~/work/personal/jobs/.claude/scripts/jobs_db.py top --limit 10
```

For each top job, fetch the JD and check for sponsorship blockers:
- "not eligible for sponsorship", "must be US Citizen", "Green Card only", "clearance required", "TS/SCI", "public trust", "permanent resident", "no visa sponsorship", "unable to sponsor"

If blocked:
```bash
python3 ~/work/personal/jobs/.claude/scripts/jobs_db.py mark --url "{url}" --status rejected
```

Report: "Pre-screened — {N} jobs ready, {M} rejected (sponsorship)"

## Step 3: Fetch JDs

For each approved job, fetch the full job description:

```bash
AB="agent-browser --cdp 9223"
$AB navigate "{url}"
$AB wait --load networkidle
$AB eval "document.querySelector('main, article, [role=\"main\"], .job-description, #job-details')?.innerText || document.body.innerText"
```

Save to `/tmp/apply-{job}/jd.txt`. Prepend the URL as the first line.

**Fallbacks:** curl → WebFetch → ask Simon to paste

## Step 4: Tailor + Compile PDFs

For each job with a fetched JD:

### Create worktrees
```bash
BASE=~/work/personal/jobs
COMMIT=$(git -C $BASE rev-parse main)
git -C $BASE worktree add --detach /tmp/apply-{job} $COMMIT
```

### Strip unnecessary context from worktrees
```bash
mkdir -p /tmp/apply-{job}/.claude
echo '{}' > /tmp/apply-{job}/.claude/settings.local.json
rm -f /tmp/apply-{job}/.claude/CLAUDE.md /tmp/apply-{job}/CLAUDE.md
```

### Copy JD into worktree
```bash
cp /tmp/apply-{job}/jd.txt /tmp/apply-{job}/jd.txt
```

### Spawn tailor agents in parallel
```bash
cd /tmp/apply-{job} && claude --permission-mode bypassPermissions --print \
  "$(cat ~/.openclaw/workspace/.claude/skills/mass-apply/references/tailor-instructions.md)

  The job description is in jd.txt (already fetched — do NOT use browser tools).
  Read full-time/resume.typ and full-time/cover_letter.typ from this directory.
  Write all proposed changes to .claude/draft.md.
  DO NOT call AskUserQuestion or wait for user input.
  Stop after draft.md is written." > /tmp/apply-{job}-tailor.log 2>&1 &
```

Spawn ALL simultaneously. Poll every 30s for `.claude/draft.md` files. Timeout: 10 minutes per agent.

### Validate drafts

**Auto-reject:** JD contains sponsorship blocker keywords → mark rejected, skip
**Auto-approve:** Skills changes are reorders only, bullets from existing bank, wording adjustments only

### Compile PDFs
```bash
# Apply draft edits to .typ files in worktree, then:
typst compile /tmp/apply-{job}/full-time/resume.typ /tmp/openclaw/uploads/resume_{Company}_{Role}_{date}.pdf
typst compile /tmp/apply-{job}/full-time/cover_letter.typ /tmp/openclaw/uploads/cover_letter_{Company}_{Role}_{date}.pdf
```

Verify both PDFs exist and are non-zero.

### Revert and clean worktree
```bash
git -C ~/work/personal/jobs checkout -- full-time/resume.typ full-time/cover_letter.typ
git -C ~/work/personal/jobs worktree remove /tmp/apply-{job} --force
```

## Step 5: Present Job List

Output a numbered list with clickable links. Include company, role, platform, location, and the apply URL.

```
Ready to apply — {N} jobs tailored:

1. **{Company}** — {Role}
   {Platform} · {Location}
   → {apply_url}

2. **{Company}** — {Role}
   {Platform} · {Location}
   → {apply_url}

...

Tailored PDFs are in /tmp/openclaw/uploads/. Open each link, use Simplify to autofill, upload the tailored resume when prompted, then tell me which ones you applied to (e.g., "applied to 1, 3, 5" or "all except 4").
```

**URL selection:** For each job, prefer direct ATS URLs (Workday, Greenhouse, Ashby, Lever) over aggregator links (LinkedIn, Indeed). Check DB for multiple rows with the same company+role.

## Step 6: Wait for Response

Simon will reply indicating which jobs he applied to. Parse flexibly:
- Numbers: "1, 3, 5" or "applied to 1 3 5"
- Names: "did salesforce and playstation"
- Exclusions: "all except courier health"
- Confirmation: "all done" (means all jobs)

## Step 7: Track on Jobditto

For each job Simon applied to:

```bash
python3 ~/work/personal/jobs/.claude/scripts/track_application.py \
  --base-path ~/work/personal/jobs
python3 ~/work/personal/jobs/.claude/scripts/jobs_db.py mark --url "{url}" --status applied
```

For jobs Simon skipped:
```bash
python3 ~/work/personal/jobs/.claude/scripts/jobs_db.py mark --url "{url}" --status skipped
```

### Cleanup
```bash
# Delete compiled PDFs for applied jobs
rm /tmp/openclaw/uploads/resume_{Company}_*.pdf /tmp/openclaw/uploads/cover_letter_{Company}_*.pdf

# Remove any remaining worktrees
git -C ~/work/personal/jobs worktree prune
```

### Report
```
Tracked {N} applications:
✅ {Company} — {Role}
✅ {Company} — {Role}
⏭️ Skipped: {Company} — {reason}

Total applied: {N} today, {M} all-time
```

## Error Handling

- **find-jobs fails** → report which sources failed, continue with available jobs
- **Tailor agent times out** → skip that job, notify Simon
- **typst compilation fails** → read error, try to fix .typ, retry once
- **track_application.py fails** → show error, offer manual retry
- **No jobs found** → "No new jobs to apply to. Will check again later."
- **All jobs rejected** → "All {N} jobs had sponsorship blockers. No applications to prepare."
