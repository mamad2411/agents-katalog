---
name: review-loop-reviewer
description: Run the reviewer side of the review loop — review PR diffs, produce findings, and evaluate quality gate. Single-pass by default; use --poll for in-session round 2 polling. Hybrid split — leader handles I/O, subagent does analysis only.
---

# /review-loop-reviewer — Reviewer-Side Review Loop

Hybrid architecture: the **leader** pre-gathers all data via Bash (git, gh, inbox), spawns a **`code-reviewer` subagent** (read-only — Read/Glob/Grep only), then the **leader** post-processes the verdict (writes findings packet, sends inbox messages, PR comments/approvals).

## Arguments

- `/review-loop-reviewer <PR_NUMBER> --author <name>` — required. The PR and the author agent name.
- `--project <name>` — override auto-detected project.
- `--task-id <id>` — optional task context.
- `--model sonnet` — model for the subagent (default: `sonnet`).
- `--dry-run` — show what the subagent would do without spawning it.
- `--poll` — enable in-session polling for `review_addressed` (Step 8). Without this flag, the skill exits after sending the verdict (single-pass mode for event-driven dispatch via `/check-inbox`).

## Instructions

When the user runs `/review-loop-reviewer`, do the following:

### 1. Parse arguments

Extract:

- `PR_NUMBER` — required, first positional arg. Error if missing.
- `AUTHOR` — required `--author` flag. Error if missing: "Error: --author is required. Specify the author agent name (e.g., --author claude)."
- `PROJECT` — optional `--project` flag, auto-detected if omitted.
- `TASK_ID` — optional `--task-id` flag (default empty).
- `MODEL` — optional `--model` flag, default `sonnet`.
- `DRY_RUN` — optional `--dry-run` flag.
- `POLL` — optional `--poll` flag.

### 2. Gather context

Detect the branch from the PR:

```bash
BRANCH=$(gh pr view <PR_NUMBER> --json headRefName -q .headRefName)
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
```

Detect the project name (from `--project` flag or `.oacp`):

```bash
PROJECT=${PROJECT_FLAG:-$(python3 -c "import json; print(json.load(open('.oacp'))['project_name'])" 2>/dev/null || basename $(git rev-parse --show-toplevel))}
```

Set derived paths:

```bash
OACP_ROOT="${OACP_HOME}"
REPO_PATH=$(git rev-parse --show-toplevel)
INBOX_DIR="${OACP_ROOT}/projects/${PROJECT}/agents/<agent_name>/inbox"
SCRIPTS_DIR="${OACP_ROOT}/scripts"
PACKETS_DIR="${OACP_ROOT}/projects/${PROJECT}/packets/findings"
```

### 3. Check preconditions

Verify:

- PR exists: `gh pr view <PR_NUMBER>`
- `--author` was provided (not empty)
- Inbox directory exists
- Scripts directory exists
- `gh` is authenticated

Pre-create the findings packets directory if it does not exist:

```bash
mkdir -p "${PACKETS_DIR}"
```

Report any failures and stop.

### 4. Pre-gather data (leader collects everything the subagent needs)

This is the critical step: the leader fetches ALL external data so the subagent never needs Bash.

#### 4a. Read project memory files

Read from the project workspace:

- `${OACP_ROOT}/projects/${PROJECT}/memory/project_facts.md`
- `${OACP_ROOT}/projects/${PROJECT}/memory/open_threads.md`

Store as `MEMORY_CONTEXT` (summarize to key points if very long).

#### 4b. Parse review_request from inbox

```bash
command ls -1 "${INBOX_DIR}/" 2>/dev/null | command grep '\.yaml$'
```

Look for files matching `*_<AUTHOR>_review_request.yaml`. If found, read and extract: PR number, branch, diff_summary, task_id, review_round. Then delete it.

Set `CURRENT_ROUND` from the review_request `review_round` field (default 1).
Set `TASK_ID` from the review_request `task_id` field if present (fallback to CLI `--task-id`).

If no review_request is found, proceed with `CURRENT_ROUND=1`.

#### 4c. Check existing GitHub comments

Fetch all 3 comment APIs to avoid duplicate findings:

```bash
INLINE_COMMENTS=$(gh api repos/<REPO>/pulls/<PR_NUMBER>/comments --jq '.[].body' 2>/dev/null || echo "")
REVIEW_COMMENTS=$(gh api repos/<REPO>/pulls/<PR_NUMBER>/reviews --jq '.[] | "\(.state): \(.body)"' 2>/dev/null || echo "")
ISSUE_COMMENTS=$(gh api repos/<REPO>/issues/<PR_NUMBER>/comments --jq '.[].body' 2>/dev/null || echo "")
```

Combine into `EXISTING_COMMENTS`.

#### 4d. Fetch full diff

```bash
git fetch origin <BRANCH>
DIFF_TEXT=$(git diff main...origin/<BRANCH>)
```

Store the full diff as `DIFF_TEXT`.

> **Large diffs**: If the diff exceeds ~100KB, save it to a temp file instead of embedding in the subagent prompt. Instruct the subagent to use the Read tool to load it.

#### 4e. Fetch PR title and body

```bash
PR_INFO=$(gh pr view <PR_NUMBER> --json title,body)
```

Store as `PR_TITLE` and `PR_BODY`.

### 5. Show plan

Display to the user:

```
Review Loop — Reviewer Side (Hybrid Split)
  PR:          #<PR_NUMBER> (<REPO>)
  Branch:      <BRANCH>
  Author:      <AUTHOR>
  Project:     <PROJECT>
  Task ID:     <TASK_ID or empty>
  Round:       <CURRENT_ROUND>
  Model:       <MODEL>
  Inbox:       <INBOX_DIR>
  Packets dir: <PACKETS_DIR>
  Diff size:   <line count of DIFF_TEXT> lines
  Existing comments: <count> found
```

If `--dry-run`, stop here.

### 6. Spawn analysis-only subagent

Spawn a `code-reviewer` subagent in the background using the configured model.

**IMPORTANT**: The subagent is read-only (Read, Glob, Grep tools only — no Bash, no Write). All external data is passed in the prompt. The subagent outputs the findings YAML in its verdict block; the **leader** writes the findings packet file.

The subagent prompt MUST include:

````
You are the analysis subagent for reviewing PR #<PR_NUMBER> on repo <REPO>.

Your ONLY job: analyze the diff and output a structured verdict with findings YAML. You receive all data pre-gathered — you do NOT need git, gh, or any Bash commands. The leader will write the findings packet file.

CRITICAL: You are a read-only code-reviewer agent. You have Read, Glob, and Grep tools only. Do NOT attempt to use Bash or Write tools. Output the findings YAML in your verdict block — the leader writes it to disk.

## Context

- PR number: <PR_NUMBER>
- Branch: <BRANCH>
- Repo: <REPO>
- Author: <AUTHOR>
- Project: <PROJECT>
- Task ID: <TASK_ID>
- Round: <CURRENT_ROUND>
- Findings packet path: <PACKETS_DIR>/<YYYYMMDD>_<topic>_<agent>_r<CURRENT_ROUND>.yaml

## PR Title

<PR_TITLE>

## PR Body

<PR_BODY>

## Project Context (Memory)

<MEMORY_CONTEXT>

## Existing PR Comments (do not duplicate these)

<EXISTING_COMMENTS or "None.">

## Full Diff

```diff
<DIFF_TEXT>
```

## Reviewer Heuristics

- R1: Only review issues in the diff — do not review entire files. Pre-existing issues belong in separate tickets.
- R2: Compare actual diff against the PR title/body description — flag discrepancies.
- R3: Mark blocking only for bugs, security issues, or protocol violations. Style nits are non-blocking (P2/P3).
- R4: Include a concrete recommendation for every finding.
- R5: (Handled by leader — skip.)
- R6: On re-review rounds, check if previous findings were addressed. Check for new issues introduced by fixes.
- R7: Verify breaking changes are called out in PR description.
- R8: Verify prerequisites/dependencies are accurately documented as required vs optional.

## Instructions

### Step 1: Analyze the diff

Read the diff carefully. Note:
- What changed and why (compare against PR title/body)
- Potential bugs, security issues, protocol violations
- Style issues, documentation gaps
- Any discrepancies between stated purpose and actual changes

If you need additional context about existing source files, use the Read tool.

### Step 2: Produce findings

Compose the findings YAML:
```yaml
packet_id: "<YYYYMMDD>_<topic>_<agent>_r<round>"
source_review_packet: ""
reviewer: "<agent>"
round: <N>
created_at_utc: "<ISO 8601 timestamp>"
summary:
  verdict: "fail|pass"
  blocking_count: <N>
  non_blocking_count: <N>
findings:
  - id: "F-001"
    severity: "P0|P1|P2|P3"
    blocking: true|false
    status: "open"
    area: "code|docs|tests|protocol"
    file: "<path>"
    line: <N>
    repro: "<how to reproduce>"
    expected: "<correct behavior>"
    evidence: "<evidence>"
    recommendation: "<suggested fix>"
```

Severity guidelines:
- P0: Critical — data loss, security vulnerability, crash
- P1: Major — incorrect behavior, protocol violation, missing required functionality
- P2: Minor — style issues, suboptimal patterns, documentation gaps
- P3: Nit — cosmetic, naming preferences, optional improvements

### Step 3: Evaluate quality gate

The gate PASSES when ALL of:
- Zero unresolved P0 findings
- Zero unresolved blocking findings

### Step 4: Output verdict

As the LAST part of your output, print:

```
---VERDICT---
result: pass|fail
blocking_count: <N>
non_blocking_count: <N>
packet_path: <full path where the leader should write the findings YAML>
summary: <1-2 sentence summary>
---FINDINGS_YAML---
<the complete findings YAML content>
---END_VERDICT---
```
````

### 7. Post-process (leader handles all messaging)

After the subagent completes, the leader:

1. **Parse the verdict** from the subagent's output. Look for the `---VERDICT---` block and extract `result`, `blocking_count`, `non_blocking_count`, `packet_path`, `summary`, and the findings YAML between `---FINDINGS_YAML---` and `---END_VERDICT---`.

2. **Write the findings packet** to `packet_path`. Verify the file was written correctly by reading it back.

3. **Generate a GitHub token** for your configured app identity (if applicable). Use for PR approval and comments.

   **Self-review guard**: Check if the PR was authored by the same identity:

   ```bash
   PR_AUTHOR=$(gh pr view <PR_NUMBER> --json author -q .author.login)
   ```

   If the current identity authored the PR, `gh pr review --approve` will fail. In this case, post an informational comment instead. The inbox LGTM should still be sent regardless.

4. **Branch on result**:

#### If gate PASSES (result=pass) → send LGTM

Send inbox LGTM message:

```bash
python3 ${SCRIPTS_DIR}/send_inbox_message.py ${PROJECT} \
  --from <agent_name> --to <AUTHOR> --type review_lgtm \
  --subject "LGTM: PR #<PR_NUMBER>" \
  --body "quality_gate_result: pass
merge_ready: true
merge_method: squash
task_id: <TASK_ID>
review_round: <CURRENT_ROUND>" \
  --related-pr <PR_NUMBER> --priority P1 \
  --oacp-dir "${OACP_ROOT}"
```

Submit PR review approval (using app token if available):

```bash
gh pr review <PR_NUMBER> --approve --body "LGTM — quality gate: pass. Merge ready."
```

Print: `STATUS: LGTM_SENT`

#### If gate FAILS (result=fail) → send feedback

Check if `CURRENT_ROUND >= 2` (max rounds). If so, add escalation.

Send inbox feedback message:

```bash
python3 ${SCRIPTS_DIR}/send_inbox_message.py ${PROJECT} \
  --from <agent_name> --to <AUTHOR> --type review_feedback \
  --subject "Review feedback: round <CURRENT_ROUND> (#<PR_NUMBER>)" \
  --body "findings_packet: packets/findings/<packet_filename>
round: <CURRENT_ROUND>
blocking_count: <blocking_count>
task_id: <TASK_ID>
review_round: <CURRENT_ROUND>" \
  --related-pr <PR_NUMBER> --priority P1 \
  --oacp-dir "${OACP_ROOT}"
```

If `CURRENT_ROUND >= 2`, append `escalation: max_rounds_exceeded` to the body.

Post PR comment for human visibility (status only):

```bash
gh pr comment <PR_NUMBER> --body "**Review feedback (round <CURRENT_ROUND>)** — changes requested. Blocking: <blocking_count>. Details via inbox."
```

If escalated: print `STATUS: ESCALATED` and stop.
Otherwise: print `STATUS: FEEDBACK_SENT_ROUND_<CURRENT_ROUND>`

### 8. Round 2 handling (leader polls and re-invokes)

> **Single-pass mode (default)**: If `--poll` was NOT provided, skip this step entirely. When `/check-inbox` receives the author's `review_addressed` + new `review_request` (round N+1), it dispatches a fresh `/review-loop-reviewer` invocation.

If `--poll` was provided, poll for the author's response after sending feedback:

```bash
command ls -1 "${INBOX_DIR}/" 2>/dev/null | command grep '\.yaml$'
```

Look for `*_<AUTHOR>_review_addressed.yaml`. Poll every 30 seconds for up to 10 minutes. When found:

1. Read and extract: `commit_sha`, `changes_summary`, `round`.
2. Delete the message.
3. Fetch updated diff:

   ```bash
   git fetch origin <BRANCH>
   DIFF_TEXT=$(git diff main...origin/<BRANCH>)
   ```

4. Increment `CURRENT_ROUND` and re-execute Steps 4c through 7.

If timeout, print `STATUS: FEEDBACK_SENT_ROUND_<CURRENT_ROUND>` and stop.

### 9. Clean up

After the review loop completes (LGTM sent, escalated, or timed out):

- Delete all processed inbox messages belonging to this PR.

## Notes

- The subagent is a `code-reviewer` (Read/Glob/Grep only) — zero Bash or Write calls. All external I/O is pre-gathered by the leader. The leader writes the findings packet.
- Default model is sonnet (sufficient for review — reading + analysis).
- Pre-creates `packets/findings/` directory in preconditions.
- **Failure state**: If the leader crashes after sending `review_feedback` but before the loop completes, the next invocation should check for already-sent feedback for this PR+round before re-sending.
- The reviewer does not need a separate worktree — it reads diffs from the existing repo.
- **Single-pass is the default**: exits after sending feedback. Event-driven re-review via `/check-inbox`.
- **Diff size guard**: If the diff exceeds ~3000 lines, warn the user. For diffs >100KB, save to a file and have the subagent read it instead of embedding in the prompt.

## PR Comment Data-Minimization Rule

- PR comments must be status-only summaries for humans.
- Keep details in inbox protocol messages and findings packets.
- Never include command output, logs, stack traces, credentials, environment values, or local paths in PR comments.
- Use `--body-file` with a temp file for PR comments when the body contains dynamic content.
