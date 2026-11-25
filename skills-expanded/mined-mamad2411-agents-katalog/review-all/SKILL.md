---
name: review-all
description: >-
  Run a two-agent code review: spawn two fresh, clean-context agents that examine
  the SAME committed branch diff in parallel. One agent runs Codex's native
  `codex review --base` command, while the other independently reviews the code
  against Google's "What to look for in a code review" guidance. Merge both
  outputs into one agreement-ranked report. Use this whenever the user asks for
  "review-all", a second-opinion review, a dual review, a cross-check before a
  PR, or a maximum-confidence review of committed branch changes. Do not use it
  to APPLY fixes; it is review-only.
---

# Review All - two clean-agent code review

## What this does, and why it has this shape

Two independent reviewers examine the same change, then their findings are
reconciled. The value is not "two reviews"; it is the **agreement signal**: when
both clean agents independently flag the same issue, confidence is high. When
only one flags something, it deserves scrutiny.

Four properties make the signal useful, and the procedure exists to
protect them:

1. **Clean context per reviewer.** Each reviewer must start fresh, with no
   memory of this orchestration or of each other, or they stop being
   independent. Spawn two agents with clean context; if the agent API supports a
   `fork_context` flag, set it to `false`. Do not paste either reviewer's output
   into the other reviewer.
2. **Same target.** Agreement only means something if both looked at the exact
   same diff. Resolve the target once and hand the identical `base...HEAD` range
   to both.
3. **Two complementary review paths.** One clean agent runs Codex's native
   `codex review --base "$base"` command. The other clean agent performs a
   direct review using `references/review-guide.md`, which is based on Google's
   "What to look for in a code review":
   https://google.github.io/eng-practices/review/reviewer/looking-for.html
4. **Genuine parallelism.** Spawn both agents before waiting for either result.
   Do not serialize the reviews.

This skill is **review-only**. Never pass `--fix` / `--comment`, never apply
patches, and never tell the user you are about to change code.

## Not a PR-finishing loop

This skill should be run once after a batched fix, or at most once more after a
second batched fix if valid P0-P2 findings remain. Do not rerun `review-all`
after each individual fix.

## Procedure

### Step 1 — Resolve the shared target (one base, one range)

The target is `base...HEAD` (merge-base diff of the current branch), so both
reviewers see exactly the commits this branch adds.

```bash
current=$(git rev-parse --abbrev-ref HEAD)

# Base precedence: user-provided --base > origin's default branch > main > master
base="$ARG_BASE"   # whatever the user passed, may be empty
if [ -z "$base" ]; then
  base=$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null \
         | sed 's@^refs/remotes/origin/@@')
fi
[ -z "$base" ] && git show-ref --verify --quiet refs/heads/main   && base=main
[ -z "$base" ] && git show-ref --verify --quiet refs/heads/master && base=master

echo "current=$current base=$base"
git diff --shortstat "$base"...HEAD
git diff --name-only "$base"...HEAD
```

### Step 2 — Pre-flight (fail fast, don't waste a review)

Stop and tell the user plainly if any of these hold:

- Not inside a git repo.
- No base branch could be resolved → ask the user which base to diff against.
- `current` *is* the base branch → there is nothing to compare; ask for a base.
- The diff is empty (`git diff --shortstat "$base"...HEAD` prints nothing) →
  there are no committed changes to review. Remind the user this mode reviews
  **committed** changes only; if their work is uncommitted, they should commit
  first.
- Codex is not ready: `codex login status` does not report a logged-in account.
  Report it and offer to run the Google-rubric review alone.

### Step 3 - Spawn BOTH clean agents in parallel

Use the agent/subagent facility available in the current environment. Start both
review agents before waiting. If the API exposes `fork_context`, set it to
`false` for each agent. Give each agent only the repo path, resolved base, and
its task.

**Agent A: Codex review-command agent**

Task prompt:

> You are a clean-context review-command runner. In the repo at `<repo path>`,
> run Codex's native review command against the committed branch diff:
>
> `codex review --base <base>`
>
> This is review-only. Do not pass `--fix` or `--comment`, do not post anything
> to GitHub, and do not modify files. Return the native command output and, if
> possible, a normalized JSON array of findings:
> `{"file":"...","line":<int or null>,"priority":"P0|P1|P2|P3","category":"design|functionality|complexity|tests|naming|comments|consistency|documentation|security|other","title":"<one line>","description":"<evidence and impact>"}`.
> If the command finds nothing, return `[]` after the raw output summary. If the
> command fails, return the exact failure and stop.

**Agent B: Google-rubric review agent**

Read `references/review-guide.md` next to this `SKILL.md`, then give the agent
this task with the full rubric pasted in:

> You are an independent code reviewer with clean context. In the repo at
> `<repo path>`, review **only** the committed changes in `git diff <base>...HEAD`.
> Apply this review rubric, based on Google's "What to look for in a code
> review":
>
> <paste the full contents of references/review-guide.md here>
>
> Constraints: This is review-only. Do **not** pass `--comment` or `--fix`, do
> **not** post anything to GitHub, and do **not** modify any files. Use system
> context as a lens to judge the changed lines, but anchor every finding to the
> diff (a changed line, or something the change should have touched but didn't,
> like a missing test). Skip nitpicks a linter, formatter, typechecker, or
> compiler would catch.
>
> Return your findings to me as a JSON array and nothing else. Each finding:
> `{"file": "...", "line": <int or null>, "priority": "P0|P1|P2|P3",
> "category": "design|functionality|complexity|tests|naming|comments|consistency|documentation|security|other",
> "title": "<one line>", "description": "<why it's a problem, with evidence>"}`.
> Assign `priority` per the rubric's P0–P3 scale. If you find nothing, return
> `[]`. If the change does something notably well, you may add one finding with
> priority `P3` and category `other` titled "Good: …".

After both agents have been spawned, wait for their results.

### Step 4 — Collect both results

- Await the Google-rubric review agent's JSON.
- Await the Codex review-command agent's raw output and/or normalized JSON.
  **Parse the native Codex output semantically**; don't rely on a rigid regex.
  What the native reviewer's output often looks like:
  - A preamble block (Codex version, workdir, model, and a dump of the diff and
    the shell commands it ran) — **skip all of it**.
  - The findings appear after a `codex` marker as a summary line followed by
    `Full review comments:` and a list of entries shaped like
    `- [P2] <title> — <path>:<start>-<end>` with a description paragraph under
    each. Each entry is one finding.
  - The findings block is often printed **twice** (streamed, then repeated as
    the final message). Dedupe — it's the same findings, not new ones.
  - Codex already tags each finding `[P0]`–`[P3]`; keep those labels as-is —
    it's the same scale the Google-rubric reviewer uses, so no remapping is
    needed.
  - Harmless `git: warning: confstr()` / `xcrun_db` lines come from the
    read-only sandbox; ignore them.

If one side fails (Codex errored, an agent returned nothing usable), continue
with whatever you have and say so explicitly in the report — a half review
clearly labeled beats a silent gap.

### Step 5 — Merge, dedupe, rank

Normalize both sides into the same finding shape, then reconcile:

- **Dedupe** by same file + overlapping/adjacent lines + same underlying issue
  (semantic match, not string match — the two agents will word things
  differently).
- **Tag the source** of every finding: `both`, `google`, or `codex`.
- **Resolve priority** for each merged finding: if both reviewers flagged it but
  assigned different priorities, take the **higher** (more severe) one and note
  the split.
- **Rank** primarily by priority (P0 → P3). Within a priority tier, list
  findings both agents agree on first — independent agreement is the strongest
  confidence signal this skill produces.
- **Surface disagreement** rather than hiding it: if the two agents conflict
  on whether something is a bug, show both positions briefly. That tension is
  often the most useful part of the report.

### Step 6 — Present one unified report

Lead with a verdict, then a priority overview table, then findings grouped by
priority tier. Tag every finding with its priority, its source (`both` /
`google` / `codex`), and its rubric dimension.

```
## Review-all: <current> vs <base>  (<N> files, +<adds>/-<dels>)

**Verdict:** APPROVE / REQUEST CHANGES / COMMENT
**Overall correctness:** patch is correct / patch is incorrect
Codex review and Google-rubric review examined the same diff independently; <X>
findings agreed.

### Findings overview
| Priority | Count | Where | Summary |
| -------- | ----- | ----- | ------- |
| P0 | <n> | <file:line or —> | <short or "none"> |
| P1 | <n> | … | … |
| P2 | <n> | … | … |
| P3 | <n> | … | … |

### P0      ← show only tiers that have findings
1. [P0] **<title>** — `file:line` · _both_ · functionality
   <merged description>

### P1
...

### P2
...

### P3
...
```

Derive the verdict from the priorities (same logic the kelos reviewer uses):

- **Overall correctness** is "patch is incorrect" if there's any P0 or P1
  finding; otherwise "patch is correct". Ignore P2/P3 nits for this call.
- **REQUEST CHANGES** when there's a P0/P1; **APPROVE** when only P2/P3 (or
  nothing); **COMMENT** when you genuinely need the author's input before
  deciding.

Keep it tight: no emojis, cite `file:line`, mark agreed (`both`) findings clearly
since that's the highest-confidence signal, and don't pad single-model findings to
look like consensus. If both agents found nothing, say so and stop. A notable
strength may be a one-line "Good:" note under the lowest tier — matter-of-fact,
not flattery.

## Notes & edge cases

- **Committed changes only.** `codex review --base` and `base...HEAD` both ignore
  uncommitted/untracked files. If the user wants those reviewed, they must commit
  first (a future `--working-tree` mode could cover that case).
- **Large diffs.** Codex may take a while; that's exactly why it runs in its own
  clean agent. Don't kill it early.
- **Arguments.** Accept an optional base override (e.g. `review-all --base develop`
  or `review-all develop`). If none is given, auto-resolve per Step 1.
- **Don't double-review.** Both reviewers must get the identical range; never let
  one drift to working-tree and the other to branch scope.
