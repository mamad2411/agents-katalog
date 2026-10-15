---
name: stacksmith-ops
version: 1.0.0
description: "Ops and project memory layer for any software project. Modes: checkpoint (save project state and context), learn (capture lessons and patterns), health (audit project health and drift), retro (run a retrospective). Trigger when saving progress before a handoff, reviewing project status, or running an end-of-sprint retrospective."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
---

## Command routing

Parse the user's invocation:

- `/stacksmith-ops checkpoint ...` -> checkpoint mode
- `/stacksmith-ops learn ...` -> learn mode
- `/stacksmith-ops health` -> health mode
- `/stacksmith-ops retro` -> retro mode

If no mode is provided, ask which ops mode they want.

All timeline logs in this skill use:
- `skill: "stacksmith-ops"`
- `mode: "checkpoint" | "learn" | "health" | "retro"`

---

## Mode: `checkpoint`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_SLUG=$(git remote get-url origin 2>/dev/null | sed 's|.*[:/]\([^/]*/[^/]*\)\.git$|\1|;s|.*[:/]\([^/]*/[^/]*\)$|\1|' | tr '/' '-' | tr -cd 'a-zA-Z0-9._-' 2>/dev/null || basename "$PWD")
echo "BRANCH: $_BRANCH"
echo "REPO: $_REPO"
echo "SLUG: $_SLUG"
_CHECKPOINT_DIR="$HOME/.mystack/projects/$_SLUG/checkpoints"
mkdir -p "$_CHECKPOINT_DIR"
echo "CHECKPOINT_DIR: $_CHECKPOINT_DIR"
ls -t "$_CHECKPOINT_DIR"/*-$(echo $_BRANCH | tr '/' '-')*.md 2>/dev/null | head -5 || echo "NO_CHECKPOINTS"
```

### Detect command

Parse the remainder of the command:
- `/stacksmith-ops checkpoint` -> save
- `/stacksmith-ops checkpoint save` -> save
- `/stacksmith-ops checkpoint resume` or `restore` -> restore
- `/stacksmith-ops checkpoint list` -> list
- `/stacksmith-ops checkpoint <title>` -> save with title

### Save

#### Step 1 - Gather state

```bash
echo "=== BRANCH ==="
git rev-parse --abbrev-ref HEAD 2>/dev/null
echo "=== STATUS ==="
git status --short 2>/dev/null
echo "=== DIFF STAT ==="
git diff --stat 2>/dev/null | tail -5
echo "=== STAGED ==="
git diff --cached --stat 2>/dev/null | tail -5
echo "=== RECENT LOG ==="
git log --oneline -10 2>/dev/null
echo "=== STASH ==="
git stash list 2>/dev/null
```

Also read `TODOS.md` and any open `PLAN.md` for context.

#### Step 2 - Summarize context

Using the gathered state plus the conversation history, produce:
1. what's being worked on
2. decisions made
3. remaining work
4. notes

If the user provided a title, use it. Otherwise infer a concise title.

#### Step 3 - Write checkpoint file

Write to `~/.mystack/projects/<slug>/checkpoints/<timestamp>-<title-slug>.md`:

```markdown
---
status: in-progress
branch: <branch>
timestamp: <ISO-8601>
files_modified:
  - <file1>
  - <file2>
---

## Working on: <title>

### Summary
<1-3 sentences>

### Decisions Made
- <decision 1 and why>
- <decision 2 and why>

### Remaining Work
1. <next step>
2. <next step>
3. <next step>

### Notes
<Gotchas, blocked items, open questions, things tried that didn't work>
```

The `files_modified` list comes from `git status --short`.

```bash
_TS=$(date +%Y%m%d-%H%M%S)
_TITLE_SLUG=$(echo "<title>" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | cut -c1-40)
_BRANCH_SLUG=$(echo $_BRANCH | tr '/' '-')
_FILE="$_CHECKPOINT_DIR/${_TS}-${_BRANCH_SLUG}-${_TITLE_SLUG}.md"
echo "Writing checkpoint to: $_FILE"
```

Also append to timeline:

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-ops\",\"mode\":\"checkpoint\",\"branch\":\"$_BRANCH\",\"outcome\":\"success\",\"action\":\"save\",\"title\":\"<title>\",\"repo\":\"$_REPO\"}" >> ~/.mystack/timeline.jsonl
```

### Restore

#### Step 1 - Find checkpoints

```bash
ls -t $_CHECKPOINT_DIR/*.md 2>/dev/null | head -10
```

Show as a numbered list. If only one checkpoint exists for the current branch, offer to restore it directly. If multiple exist, ask which one to restore.

#### Step 2 - Load checkpoint

Read the checkpoint file and present the saved summary, remaining work, and notes.

#### Step 3 - Offer next steps

Suggest the most relevant next skill:
- `/stacksmith-review code`
- `/stacksmith-qa`
- `/stacksmith-release prepare`
- `/investigate`

### List

```bash
ls -lt $_CHECKPOINT_DIR/*.md 2>/dev/null | head -20
```

Show checkpoints across all branches as a table.

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-ops\",\"mode\":\"checkpoint\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: `learn`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_SLUG=$(git remote get-url origin 2>/dev/null | sed 's|.*[:/]\([^/]*/[^/]*\)\.git$|\1|;s|.*[:/]\([^/]*/[^/]*\)$|\1|' | tr '/' '-' | tr -cd 'a-zA-Z0-9._-' 2>/dev/null || basename "$PWD")
_LEARN_FILE="$HOME/.mystack/projects/$_SLUG/learnings.jsonl"
echo "BRANCH: $_BRANCH"
echo "REPO: $_REPO"
echo "LEARN_FILE: $_LEARN_FILE"
[ -f "$_LEARN_FILE" ] && echo "TOTAL: $(wc -l < $_LEARN_FILE | tr -d ' ') entries" || echo "TOTAL: 0 entries"
mkdir -p "$HOME/.mystack/projects/$_SLUG"
```

### Learning format

Each learning is one JSON line in `~/.mystack/projects/<slug>/learnings.jsonl`:

```json
{"ts":"2026-04-04T10:00:00Z","skill":"stacksmith-review","mode":"code-review","type":"pitfall","key":"n-plus-one-products","insight":"Product.includes(:variants) needed in catalog controller - N+1 caused 3s load time","confidence":9,"branch":"feat/catalog","files":["app/controllers/catalog_controller.rb"]}
```

Fields:
- `type`: `pattern` | `pitfall` | `preference` | `architecture` | `tool`
- `key`: kebab-case slug
- `insight`: one sentence
- `confidence`: 1-10
- `source`: which skill captured it, or `user-stated`
- `files`: related files

Deduplicate by `key`; latest wins.

### Detect command

Parse the remainder:
- `/stacksmith-ops learn` -> show recent
- `/stacksmith-ops learn search <query>` -> search
- `/stacksmith-ops learn prune` -> prune
- `/stacksmith-ops learn export` -> export
- `/stacksmith-ops learn stats` -> stats
- `/stacksmith-ops learn add` -> manual add

### Show recent

```bash
[ -f "$_LEARN_FILE" ] && tail -50 "$_LEARN_FILE" || echo "NO_LEARNINGS"
```

Parse and display grouped by type, deduplicated by key.

If no learnings: tell the user they will be captured automatically from `/stacksmith-review code`, `/stacksmith-qa`, `/investigate`, and `/stacksmith-release prepare`.

### Search

```bash
_QUERY="<user's search terms>"
grep -i "$_QUERY" "$_LEARN_FILE" 2>/dev/null | tail -20 || echo "NO_MATCHES"
```

Display grouped matching entries.

### Prune

Check for:
- deleted referenced files
- contradictory duplicate keys
- old low-confidence entries

For each flagged entry, ask whether to remove, keep, or update it.

### Export

Format all learnings as markdown suitable for `CLAUDE.md` or other docs. Offer:
- copy to clipboard
- append to `CLAUDE.md`
- save as `learnings-export.md`

### Stats

Count unique learnings, breakdown by type and source, and average confidence.

### Manual add

Ask for:
- type
- key
- insight
- confidence
- optional related files

Then append to `learnings.jsonl` with:

```bash
_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "{\"ts\":\"$_TS\",\"skill\":\"stacksmith-ops\",\"mode\":\"learn\",\"type\":\"<type>\",\"key\":\"<key>\",\"insight\":\"<insight>\",\"confidence\":<n>,\"source\":\"user-stated\",\"files\":[<files>]}" >> "$_LEARN_FILE"
```

### How other skills capture learnings

Skills can append to the learnings file when they discover something valuable:

```bash
_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
_SLUG=$(git remote get-url origin 2>/dev/null | sed 's|.*[:/]\([^/]*/[^/]*\)\.git$|\1|' | tr '/' '-' | tr -cd 'a-zA-Z0-9._-' || basename "$PWD")
echo "{\"ts\":\"$_TS\",\"skill\":\"<skill>\",\"mode\":\"<mode>\",\"type\":\"pitfall\",\"key\":\"<key>\",\"insight\":\"<insight>\",\"confidence\":<n>,\"source\":\"<skill>\",\"branch\":\"$(git branch --show-current 2>/dev/null)\",\"files\":[\"<file>\"]}" >> "$HOME/.mystack/projects/$_SLUG/learnings.jsonl"
```

Guidelines:
- only capture confidence >= 7
- only project-specific lessons
- only real encountered pitfalls or successful patterns

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-ops\",\"mode\":\"learn\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: `health`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_SLUG=$(git remote get-url origin 2>/dev/null | sed 's|.*[:/]\([^/]*/[^/]*\)\.git$|\1|;s|.*[:/]\([^/]*/[^/]*\)$|\1|' | tr '/' '-' | tr -cd 'a-zA-Z0-9._-' 2>/dev/null || basename "$PWD")
echo "BRANCH: $_BRANCH"
echo "REPO: $_REPO"
mkdir -p "$HOME/.mystack/projects/$_SLUG"
_HEALTH_FILE="$HOME/.mystack/projects/$_SLUG/health-history.jsonl"
echo "HISTORY_FILE: $_HEALTH_FILE"
grep -A10 "## Health Stack" CLAUDE.md 2>/dev/null | head -10
```

### Important rules

1. Wrap, don't replace.
2. Read-only.
3. Respect `CLAUDE.md`.
4. Skipped is not failed.
5. Show raw output for failures.
6. Be honest about scores.

### Step 1 - Detect health stack

First check `CLAUDE.md` for `## Health Stack`. If present, use those exact commands.

Otherwise auto-detect:
- type checker
- linter
- test runner
- dead-code tool
- shell linter

Offer to persist the detected stack to `CLAUDE.md`.

### Step 2 - Run tools

Run each detected tool in sequence, recording:
- start time
- stdout/stderr
- exit code
- duration

### Step 3 - Score each category

Score:
- type check
- lint
- tests
- dead code
- shell lint

Compute weighted composite score, redistributing skipped weights.

### Step 4 - Present dashboard

Show:
- category scores
- status labels
- durations
- composite score
- first 10 lines of failing tool output when needed

### Step 5 - Persist to health history

Append the run to `~/.mystack/projects/<slug>/health-history.jsonl`.

### Step 6 - Trend analysis

Read the last 10 entries. Show:
- last 5 runs
- trend direction
- top recommendations by weighted impact

If first run: say there is no trend data yet.

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-ops\",\"mode\":\"health\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: `retro`

### Preamble (run first)

```bash
echo "Reading local timeline..."
cat ~/.mystack/timeline.jsonl 2>/dev/null | wc -l | tr -d ' ' | xargs echo "Total entries:"
[ -f ~/.mystack/timeline.jsonl ] && echo "TIMELINE: found" || echo "TIMELINE: none"
```

If `TIMELINE: none`: "No local timeline yet. Run some skills and come back."

### Step 1 - Parse last 7 days

```bash
python3 - << 'EOF'
import sys, json
from datetime import datetime, timedelta, timezone
from collections import Counter, defaultdict
from os import path

cutoff = datetime.now(timezone.utc) - timedelta(days=7)
entries = []

try:
    with open(path.expanduser('~/.mystack/timeline.jsonl')) as f:
        for line in f:
            try:
                e = json.loads(line.strip())
                ts = datetime.fromisoformat(e['ts'].replace('Z', '+00:00'))
                if ts >= cutoff:
                    entries.append(e)
            except:
                pass
except FileNotFoundError:
    pass

if not entries:
    print("NO_DATA")
    sys.exit(0)

skills = Counter(e['skill'] for e in entries)
outcomes = Counter(e['outcome'] for e in entries)
branches = set(e.get('branch', 'N/A') for e in entries)
by_day = defaultdict(int)
for e in entries:
    ts = datetime.fromisoformat(e['ts'].replace('Z', '+00:00'))
    by_day[ts.strftime('%Y-%m-%d')] += 1

print(f"ENTRIES: {len(entries)}")
print(f"SUCCESS_RATE: {outcomes.get('success', 0)}/{len(entries)}")
print(f"BRANCHES: {len(branches)}")
print("SKILLS:")
for skill, count in skills.most_common():
    print(f"  {skill}: {count}")
print("BY_DAY:")
for day in sorted(by_day):
    print(f"  {day}: {by_day[day]}")

ship_days = sorted(set(
    datetime.fromisoformat(e['ts'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
    for e in entries
    if (
        (e.get('skill') == 'stacksmith-release' and e.get('mode') == 'ship')
        or e.get('skill') == 'ship'
    ) and e.get('outcome') == 'success'
))
streak = 0
if ship_days:
    check = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    for _ in range(30):
        if check in ship_days:
            streak += 1
            dt = datetime.strptime(check, '%Y-%m-%d') - timedelta(days=1)
            check = dt.strftime('%Y-%m-%d')
        else:
            break
print(f"SHIP_STREAK: {streak}")
EOF
```

### Step 2 - Git stats (enrichment)

```bash
git log --oneline --since="7 days ago" 2>/dev/null | wc -l | xargs echo "Commits this week:"
git log --since="7 days ago" --format="" --stat 2>/dev/null | \
  awk '/files? changed/ {f+=$1; i+=$4; d+=$6} END {printf "Files: %d | Insertions: +%d | Deletions: -%d\n", f, i, d}'
```

### Step 3 - Retrospective output

```text
## Retro [week of date]

### What shipped
- [N] commits across [N] branches
- Skills used: [list with counts, most used first]
- Success rate: N/N ([N]%)

### Shipping streak
[N days or last ship was N days ago]

### Patterns noticed
- [If many errors on a specific skill]
- [If qa ran without prior stacksmith-review code]
- [If no security run in a week with auth changes]
- [If no shipping movement after active commits]

### One focus for next week
[Single most impactful change based on the data]
```

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-ops\",\"mode\":\"retro\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
