---
name: retro
version: 1.0.0
description: |
  Engineering retrospective. Analyzes commit history, work patterns,
  and shipping velocity with persistent history and trend tracking.
  Auto-detects your git identity; portable across machines and repos.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# /retro -- Engineering Retrospective

Generates a comprehensive engineering retrospective analyzing commit history, work patterns, and shipping velocity. Built for a founder-engineer running multiple repos with Claude Code as a force multiplier.

## User-invocable
When the user types `/retro`, run this skill.

## Arguments
- `/retro` -- default: last 7 days, current repo
- `/retro 24h` -- last 24 hours
- `/retro 14d` -- last 14 days
- `/retro 30d` -- last 30 days
- `/retro compare` -- compare current window vs prior same-length window
- `/retro compare 14d` -- compare with explicit window
- `/retro all` -- scan all repos under ~/Development (uses last 7d)
- `/retro all 14d` -- all repos with explicit window

## Instructions

Parse the argument to determine the time window. Default to 7 days if no argument given. Use `--since="N days ago"`, `--since="N hours ago"`, or `--since="N weeks ago"` for git log queries. All times reported in **Eastern time** by default (adjust `--tz-hours` in scan.py if you are in another zone).

**Argument validation:** If the argument doesn't match expected patterns, show usage and stop:
```
Usage: /retro [window] [scope]
  /retro              -- last 7 days, current repo
  /retro 24h          -- last 24 hours
  /retro 14d          -- last 14 days
  /retro 30d          -- last 30 days
  /retro compare      -- compare this period vs prior period
  /retro compare 14d  -- compare with explicit window
  /retro all          -- all repos under ~/Development
  /retro all 14d      -- all repos with explicit window
```

### Identity

"Human" commits are yours. `scan.py` AUTO-DETECTS your git identity from
`git config user.name` / `user.email` in the first repo it scans. If you commit
under multiple names/emails, or squash-merges land under a bot identity you own,
pass them explicitly:

```bash
python3 ~/.claude/skills/retro/scan.py --days <N> --authors "Your Name" "you@email.com" "bot-name"
```

or set `RETRO_AUTHORS="Your Name,you@email.com"` in your environment. Everyone
else is counted as "automated" and excluded from your velocity metrics.

### Multi-Repo Mode (`all`)

When `all` is specified, do NOT hand-roll the scan. Run the committed engine:

```bash
python3 ~/.claude/skills/retro/scan.py --days <N>
```

It prints one JSON object with every metric below. It exists because re-deriving
this reach as inline shell has silently produced a clean, confident, WRONG table
more than once:

- **Reach.** `find -maxdepth 2 -name .git -type d` + local `main` can undercount
  human commits ~3x. Submodules store `.git` as a FILE, worktrees live at depth 3,
  and work lands on branches other than main. `scan.py` scans depth 4, accepts
  `.git` as file or dir, EXCLUDES `.worktrees/` (shares parent object DB), uses
  `git log --all`, and dedupes globally by SHA.
- **Test-path classification.** A `test/foo.mjs` dir (no leading slash) slips past a
  `/tests?/` regex, mislabeling test LOC as code and reporting a phantom low test
  ratio. `scan.py` anchors the classifier on `(^|/)`.
- **PR counting.** GitHub squash-merges stamp ` (#NNN)` on the subject and are
  authored as the merging identity, so filtering merges on your commit name alone
  undercounts PRs. `scan.py` counts human `(#NNN)` subjects plus classic merge-pr
  commits.

Trust `scan.py`'s numbers; do not "sanity-check" them by re-running a narrower
maxdepth-2 shell scan (that is the buggy path, not the reference).

### Step 1: Gather Raw Data

**Single-repo mode** (no `all`): `scan.py` also works scoped to one root ---
`python3 ~/.claude/skills/retro/scan.py --days <N> --roots .` --- or, if you must use
raw git, remember the three lessons above: `git log --all` (not `origin/main`), depth-4
repo discovery, and the `(^|/)tests?/` test-path anchor.

For hotspots (not in the JSON), after the scan (use YOUR identity for `--author`):
```bash
# top churned files, your commits, in-window (run per repo of interest)
git -C <repo> log --all --no-merges --since="<since>" --author="$(git config user.name)" \
  --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn | head -12
```

### Step 2: Compute Metrics

Calculate and present in a summary table:

| Metric | Value |
|--------|-------|
| Commits to main | N |
| PRs merged | N |
| Total insertions | N |
| Total deletions | N |
| Net LOC added | N |
| Test LOC (insertions) | N |
| Test LOC ratio | N% |
| Active days | N |
| Detected sessions | N |
| Avg LOC/session-hour | N |

### Step 3: Commit Time Distribution

Show hourly histogram in the display timezone using a bar chart:

```
Hour  Commits  ----------------
 00:    4      ----
 07:    5      -----
 ...
```

Identify and call out:
- Peak hours
- Dead zones
- Whether pattern is bimodal (morning/evening) or continuous
- Late-night coding clusters (after 10pm)

### Step 4: Work Session Detection

Detect sessions using **45-minute gap** threshold between consecutive commits. For each session report:
- Start/end time
- Number of commits
- Duration in minutes

Classify sessions:
- **Deep sessions** (50+ min)
- **Medium sessions** (20-50 min)
- **Micro sessions** (<20 min, single-commit)

Calculate:
- Total active coding time (sum of session durations)
- Average session length
- LOC per hour of active time

### Step 5: Commit Type Breakdown

Categorize by conventional commit prefix (feat/fix/refactor/test/chore/docs/verify). Show as percentage bar:

```
feat:     20  (40%)  --------------------
fix:      27  (54%)  ---------------------------
refactor:  2  ( 4%)  --
```

Flag if fix ratio exceeds 50% -- signals "ship fast, fix fast" pattern that may indicate review gaps.

### Step 6: Hotspot Analysis

Show top 10 most-changed files. Flag:
- Files changed 5+ times (churn hotspots)
- Test files vs production files in the hotspot list
- Config files (package.json, tsconfig, etc.) frequency

### Step 7: PR Size Distribution

From commit diffs, estimate PR sizes and bucket them:
- **Small** (<100 LOC)
- **Medium** (100-500 LOC)
- **Large** (500-1500 LOC)
- **XL** (1500+ LOC) -- flag these with file counts

### Step 8: Focus Score + Ship of the Week

**Focus score:** Calculate the percentage of commits touching the single most-changed top-level directory. Higher score = deeper focused work. Lower score = scattered context-switching. Report as: "Focus score: 62% (src/components/)"

**Ship of the week:** Auto-identify the single highest-impact PR or commit cluster in the window. Highlight it:
- PR number and title (or commit range)
- LOC changed
- Why it matters (infer from commit messages and files touched)

### Step 9: Week-over-Week Trends (if window >= 14d)

If the time window is 14 days or more, split into weekly buckets and show trends:
- Commits per week
- LOC per week
- Test ratio per week
- Fix ratio per week
- Session count per week

### Step 10: Streak Tracking

`scan.py` already returns `streak_days` -- use it. It counts consecutive days with at
least one commit authored by YOUR resolved identity (see Identity section) across the
full reach. Do NOT count all authors: bots may commit daily, so an author-blind streak
is meaningless. Display: "Shipping streak: N consecutive days".

### Step 11: Load History & Compare

Before saving the new snapshot, check for prior retro history:

```bash
ls -t .context/retros/*.json 2>/dev/null
```

**If prior retros exist:** Load the most recent one using the Read tool. Calculate deltas for key metrics and include a **Trends vs Last Retro** section:
```
                    Last        Now         Delta
Test ratio:         22%    ->    41%         +19pp
Sessions:           10     ->    14          +4
LOC/hour:           200    ->    350         +75%
Fix ratio:          54%    ->    30%         -24pp (improving)
Commits:            32     ->    47          +47%
Deep sessions:      3      ->    5           +2
```

**If no prior retros exist:** Skip the comparison section and append: "First retro recorded -- run again next week to see trends."

### Step 12: Save Retro History

After computing all metrics, save a JSON snapshot:

```bash
mkdir -p .context/retros
```

Use the Write tool to save the JSON file as `.context/retros/YYYY-MM-DD-N.json`:
```json
{
  "date": "2026-03-12",
  "window": "7d",
  "repo": "current-repo-name",
  "metrics": {
    "commits": 47,
    "prs_merged": 12,
    "insertions": 3200,
    "deletions": 800,
    "net_loc": 2400,
    "test_loc": 1300,
    "test_ratio": 0.41,
    "active_days": 6,
    "sessions": 14,
    "deep_sessions": 5,
    "avg_session_minutes": 42,
    "loc_per_session_hour": 350,
    "feat_pct": 0.40,
    "fix_pct": 0.30,
    "peak_hour": 22
  },
  "streak_days": 47,
  "tweetable": "Week of Mar 8: 47 commits, 3.2k LOC, 38% tests, 12 PRs, peak: 10pm"
}
```

### Step 13: Write the Narrative

Structure the output as:

---

**Tweetable summary** (first line, before everything else):
```
Week of Mar 8: 47 commits, 3.2k LOC, 38% tests, 12 PRs, peak: 10pm | Streak: 47d
```

## Engineering Retro: [date range]

### Summary Table
(from Step 2)

### Trends vs Last Retro
(from Step 11 -- skip if first retro)

### Time & Session Patterns
(from Steps 3-4)

Narrative interpreting what the patterns mean:
- When the most productive hours are and what drives them
- Whether sessions are getting longer or shorter over time
- Estimated hours per day of active coding
- How this maps to "founder who also builds" lifestyle

### Shipping Velocity
(from Steps 5-7)

Narrative covering:
- Commit type mix and what it reveals
- PR size discipline (are PRs staying small?)
- Fix-chain detection (sequences of fix commits on the same subsystem)

### Code Quality Signals
- Test LOC ratio trend
- Hotspot analysis (are the same files churning?)
- Any XL PRs that should have been split

### Focus & Highlights
(from Step 8)
- Focus score with interpretation
- Ship of the week callout

### Top 3 Wins
Identify the 3 highest-impact things shipped in the window. For each:
- What it was
- Why it matters (product/architecture impact)

### 3 Things to Improve
Specific, actionable, anchored in actual commits. Phrase as "to level up..."

### 3 Habits for Next Week
Small, practical, realistic for a very busy person. Each must take <5 minutes to adopt.

### Week-over-Week Trends
(if applicable, from Step 9)

---

## Compare Mode

When the user runs `/retro compare` (or `/retro compare 14d`):

1. Compute metrics for the current window (default 7d) using `--since="7 days ago"`
2. Compute metrics for the immediately prior same-length window using both `--since` and `--until`
3. Show a side-by-side comparison table with deltas and arrows
4. Write a brief narrative highlighting the biggest improvements and regressions
5. Save only the current-window snapshot to `.context/retros/`

## Tone

- Encouraging but candid, no coddling
- Specific and concrete -- always anchor in actual commits/code
- Skip generic praise -- say exactly what was good and why
- Frame improvements as leveling up, not criticism
- Keep total output around 2500-3500 words
- Use markdown tables and code blocks for data, prose for narrative
- Output directly to the conversation -- do NOT write to filesystem (except the `.context/retros/` JSON snapshot)

## Important Rules

- ALL narrative output goes directly to the user in the conversation
- The ONLY file written is the `.context/retros/` JSON snapshot
- Use `git log --all` (via `scan.py`), NOT `origin/<default-branch>` -- work lands on feature branches and in submodules/worktrees that a single-branch query silently drops
- Convert all timestamps to the display timezone
- If the window has zero commits, say so and suggest a different window
- Round LOC/hour to nearest 50
- Treat merge commits as PR boundaries
- Do not read CLAUDE.md or other docs -- this skill is self-contained
- On first run (no prior retros), skip comparison sections gracefully
