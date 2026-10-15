---
name: findings-to-github-issues
description: >-
  End-to-end orchestrator that turns findings from ANY input (audit spreadsheet,
  code/security review, QA report, meeting notes, a pasted list of issues) into
  a GitHub Issues backlog with a milestone, labels, and a tracking issue. Drives
  the sibling github-backlog skills in order with safety gates. Trigger whenever
  the user says "turn this audit/spreadsheet/review/list of issues into GitHub
  issues", "create a backlog from these findings", "file these as GitHub issues",
  "import this xlsx/csv into GitHub", "make issues from this report", or hands
  you a source document and asks for it to land in GitHub. This is the headline,
  one-shot entry point (/github-backlog:run wraps it). Not for editing existing
  issues individually.
argument-hint: "[path-to-findings-file]"
effort: max
---

<!-- generated: third-party requirements -->
> **Requires:** `pip install requests` — this skill's scripts import `requests`.

# findings-to-github-issues (orchestrator)

Run the full pipeline: a source document in, a GitHub Issues backlog out. You
coordinate six sibling skills; each owns its step and its data contract. Your job
is to sequence them, keep the working files together, and enforce the safety gates
so nothing irreversible happens without the user seeing it first.

**Why an orchestrator:** the value is in the gates. Creating issues is a write the
user cannot easily undo (close is manual; notifications already fired), so the
pipeline is deliberately staged: read-only extraction and classification first, a
visual dry-run that creates nothing, an explicit human approval, then the real write.

## Data flow

```
github-extract-findings         -> findings.json
classify-github-issues   -> github_backlog_input.json  (consumed by create_github_issues.py)
github-create-issues     -> github_backlog_result.json (consumed by github_tracking.py)
```

**Working directory:** create one beside the source and keep all JSON files there.

## Process

### 0. Prereqs + auth (recommended on first run)

```powershell
powershell -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/setup_check_github.ps1"
```

Checks gh CLI, Python + requests + openpyxl, `GH_OWNER` / `GH_REPO`, and repo
reachability. For auth specifics, delegate to **github-auth**.

### 1. Extract → `findings.json` (delegate to **github-extract-findings**)

Have **github-extract-findings** read the source and normalize it to `findings.json`.
**Confirm the column mapping with the user** before moving on — which column is the
`key`, which are `current` / `expected`, where `severity` and `status` come from.

### 2. Triage → scoped subset (delegate to **github-triage-findings**)

Have **github-triage-findings** filter `findings.json` to the wave worth creating now.
**Recommend Critical + confirmed first.** Hold `needs-review` for a later wave.

### 3. Classify → `github_backlog_input.json` (delegate to **classify-github-issues**)

Have **classify-github-issues** map the scoped findings to GitHub Issues with labels,
milestone, body, and size estimate. It will show an estimates table.

> **GATE — estimates.** Show the table and get the user's OK / adjustments before
> the visual dry-run.

### 4. VISUAL DRY-RUN → validate, create nothing (delegate to **github-create-issues**)

Have **github-create-issues** render `github_backlog_input.json` as a formatted
table — title, labels, milestone, assignee per item. Nothing is created.

> **GATE — stop here.** Do not proceed until the user has explicitly approved the
> list. Present the count, the milestone, and the labels, and wait for a clear yes.

### 5. REAL RUN → `github_backlog_result.json` (delegate to **github-create-issues**)

Only after approval. The script creates labels, the milestone, each issue, then the
tracking issue:

```powershell
$env:GH_OWNER = "Cartagena365"
$env:GH_REPO  = "GlassHull"
python "${CLAUDE_SKILL_DIR}/scripts/create_github_issues.py" `
  --input  "<workdir>/github_backlog_input.json" `
  --output "<workdir>/github_backlog_result.json"
```

Then **verify the created items** — confirm each `key` got a `number` and `url` in
`github_backlog_result.json`, and surface any that failed.

### 6. Write-back tracking — spreadsheets only (delegate to **github-writeback-tracking**)

**Only if the source is a spreadsheet.**

> **GATE — back up the source first.**

Have **github-writeback-tracking** drive `github_tracking.py`: first `add-columns`,
then `writeback`. Both subcommands are idempotent.

### 7. Report back

Summarize the run:
- **Created:** count + clickable links + tracking issue link.
- **Held / skipped:** the triage wave deferred, plus any real-run errors.
- **Follow-ups:** the obvious next wave.

## Safety gates (non-negotiable)

1. **Visual dry-run before real run** — step 4 always precedes step 5.
2. **Explicit approval before any write** — never jump from classification to creation.
3. **Back up the source before write-back** — step 6 edits the file in place.
