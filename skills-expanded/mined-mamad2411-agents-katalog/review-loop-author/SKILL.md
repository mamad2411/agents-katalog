---
name: review-loop-author
description: Run the author side of the review loop — address findings and drive to LGTM. Single-pass by default; use --poll for in-session polling. Hybrid split — leader handles I/O, subagent does code fixes only.
---

# /review-loop-author — Author-Side Review Loop

Hybrid architecture: the **leader** handles all external I/O (inbox, git, gh, polling), spawns a **fix-only subagent** (Read/Edit/Write — no Bash) to address findings, then the **leader** commits, pushes, and sends messages.

## Arguments

```
/review-loop-author <PR_NUMBER> --reviewer <name> [--project <name>] [--task-id <id>] [--timeout 15] [--max-rounds 3] [--poll] [--dry-run]
```

- `<PR_NUMBER>` — required. The GitHub PR number.
- `--reviewer <name>` — **required**. Reviewer agent name (no default — caller must be explicit).
- `--project <name>` — optional. Auto-detected from `.oacp` project marker if omitted.
- `--task-id <id>` — optional. Enables task-aware message metadata and task-state updates.
- `--timeout <minutes>` — optional. Poll timeout in minutes (default: 15).
- `--max-rounds <N>` — optional. Max review rounds before escalation (default: 3).
- `--dry-run` — optional. Show plan without spawning.
- `--poll` — optional. Enable in-session polling for reviewer feedback (Step 6). Without this flag, the skill exits after sending messages (single-pass mode for event-driven dispatch via `/check-inbox`).

## Instructions

When the user runs `/review-loop-author`, do the following:

### 1. Parse arguments

Extract from the user's command:

- `PR_NUMBER` — required, first positional arg. Error if missing.
- `REVIEWER` — required `--reviewer` flag. **Error if missing** with message: "Missing required --reviewer flag. Usage: /review-loop-author <PR> --reviewer <name>"
- `PROJECT` — optional `--project` flag (auto-detected in step 2 if omitted)
- `TASK_ID` — optional `--task-id` flag (default empty)
- `TIMEOUT` — optional `--timeout` flag, default `15`
- `MAX_ROUNDS` — optional `--max-rounds` flag, default `3`
- `DRY_RUN` — optional `--dry-run` flag
- `POLL` — optional `--poll` flag

### 2. Gather context

```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown")
REPO_PATH=$(git rev-parse --show-toplevel)
```

Detect project name (if `--project` was not provided):

```bash
PROJECT=$(python3 -c "import json; print(json.load(open('${REPO_PATH}/.oacp'))['project_name'])" 2>/dev/null || basename "${REPO_PATH}")
```

Set derived paths:

```bash
OACP_ROOT="${OACP_HOME}"
INBOX_DIR="${OACP_ROOT}/projects/${PROJECT}/agents/<agent_name>/inbox"
SCRIPTS_DIR="${OACP_ROOT}/scripts"
```

### 3. Check preconditions

Verify all of the following. Report failures and stop:

- PR exists: `gh pr view <PR_NUMBER> --repo <REPO>` succeeds
- Current branch matches the PR's head branch
- Inbox directory exists: `${INBOX_DIR}`
- Send script exists: `${SCRIPTS_DIR}/send_inbox_message.py`
- gh is authenticated: `gh auth status` succeeds

### 4. Check for existing feedback (leader pre-scan)

Before sending a review request, check if the reviewer has already submitted feedback:

```bash
command ls -1 "${INBOX_DIR}/" 2>/dev/null | command grep '\.yaml$'
```

Look for YAML files where `from` matches `<REVIEWER>` and `related_pr` matches `<PR_NUMBER>`. Read matching files.

- If `review_lgtm` found → skip to Step 10 (handle LGTM)
- If `review_feedback` found → skip to Step 7 (parse feedback)
- If nothing found → proceed to Step 5

Also check GitHub for out-of-band feedback:

```bash
gh api repos/<REPO>/issues/<PR_NUMBER>/comments --jq '.[].body' 2>/dev/null
gh api repos/<REPO>/pulls/<PR_NUMBER>/comments --jq '.[].body' 2>/dev/null
gh api repos/<REPO>/pulls/<PR_NUMBER>/reviews --jq '.[] | "\(.state): \(.body)"' 2>/dev/null
```

If GitHub shows new actionable feedback not in inbox, note it for later.

### 5. Show plan and send review request

Display to the user:

```
Review Loop — Author Side (Hybrid Split)
  PR:         #<PR_NUMBER> (<REPO>)
  Branch:     <BRANCH>
  Reviewer:   <REVIEWER>
  Project:    <PROJECT>
  Task ID:    <TASK_ID or empty>
  Inbox:      <INBOX_DIR>
  Timeout:    <TIMEOUT> minutes
  Max rounds: <MAX_ROUNDS>
```

If `--dry-run`, stop here.

Generate a diff summary:

```bash
git diff main...<BRANCH> --stat
```

Write a concise 2-4 line summary. Then send the review request:

```bash
python3 ${SCRIPTS_DIR}/send_inbox_message.py ${PROJECT} \
  --from <agent_name> --to <REVIEWER> --type review_request \
  --subject "Review: PR #<PR_NUMBER>" \
  --body "pr: <PR_NUMBER>
branch: <BRANCH>
diff_summary: |
  <DIFF_SUMMARY>
task_id: <TASK_ID>
review_round: 1" \
  --related-pr <PR_NUMBER> --priority P1 \
  --oacp-dir "${OACP_ROOT}"
```

Post a PR comment for human visibility (status only — no diff details):

```bash
gh pr comment <PR_NUMBER> --repo <REPO> --body "**Review requested** — round 1. Details delivered via inbox."
```

Initialize: `current_round = 1`.

### 6. Poll for feedback (leader polling loop)

> **Single-pass mode (default)**: If `--poll` was NOT provided, skip this step entirely. The skill exits after Step 9. Subsequent invocations — dispatched by `/check-inbox` when `review_feedback` arrives — will detect the feedback in Step 4 and skip directly to Step 7.

If `--poll` was provided, poll the inbox for a response from the reviewer. On each iteration:

```bash
command ls -1 "${INBOX_DIR}/" 2>/dev/null | command grep '\.yaml$'
```

Look for YAML files where `from` matches `<REVIEWER>`, `related_pr` matches `<PR_NUMBER>`, and `type` is `review_feedback` or `review_lgtm`.

- **`review_lgtm` found** → Go to Step 10
- **`review_feedback` found** → Go to Step 7
- **Nothing found** → Check if elapsed time exceeds `<TIMEOUT>` minutes. If yes → Go to Step 12 (escalation). Otherwise sleep 30 seconds and repeat.

### 7. Parse review feedback (leader reads findings)

From the `review_feedback` message, extract from the body:

- `findings_packet` — path to the findings YAML (relative to project workspace)
- `round` — current review round number
- `blocking_count` — number of blocking findings
- `task_id` — optional task identifier (fallback to `<TASK_ID>`)

Check: if body contains `escalation: max_rounds_exceeded` → Go to Step 12.

Read the findings packet:

```bash
cat "${OACP_ROOT}/projects/${PROJECT}/${findings_packet}"
```

Store the full findings YAML content as `FINDINGS_CONTENT`.

Delete the `review_feedback` message from inbox:

```bash
rm "${INBOX_DIR}/<message_filename>"
```

### 8. Spawn fix subagent (code edits only)

Spawn a `general-purpose` subagent in the background with a lightweight model (e.g., `sonnet`).

**IMPORTANT**: The subagent uses ONLY Read, Edit, Write, Glob, Grep tools. Zero Bash calls. It cannot commit, push, or send messages.

The subagent prompt MUST include:

````
You are the fix subagent for PR #<PR_NUMBER> on repo <REPO>.

Your ONLY job: read the review findings, edit source files to address them, and output a summary of what you did. You receive all findings data pre-gathered.

CRITICAL: Do NOT use the Bash tool at all. You only need Read (to examine source files), Edit (to fix code), Write (to create new files if needed), and Glob/Grep (to search the codebase for context). You cannot commit, push, or send messages — the leader handles that.

## Context

- PR number: <PR_NUMBER>
- Branch: <BRANCH>
- Repo: <REPO>
- Repo path: <REPO_PATH>
- Round: <current_round>

## Findings to Address

```yaml
<FINDINGS_CONTENT>
```

## Instructions

### Step 1: Prioritize findings

Extract all findings where `status: open`. Sort by priority:
1. P0 blocking — critical, must fix
2. P1 blocking — major, must fix
3. Non-blocking P0/P1 — important but not merge-blockers
4. P2/P3 — minor issues and nits

### Step 2: Address each finding

For each open finding, in priority order:

1. Read the referenced file
2. Determine action:
   - **Fix** — if the finding is valid and the fix is clear, apply it
   - **Push back** — if the finding is incorrect or based on a misunderstanding, note it in your output
   - **Defer** — if out of scope for this PR, note it in your output
3. If fixing: make minimal, focused changes that address the finding without introducing new issues.

### Step 3: Output fix summary

As the LAST part of your output, print a structured summary block exactly like this:

```
---FIX_SUMMARY---
fixed:
  - id: "F-001"
    description: "<what was changed>"
    files: ["<path/to/file>"]
deferred:
  - id: "F-002"
    reason: "<why deferred>"
pushed_back:
  - id: "F-004"
    reason: "<why this finding is incorrect>"
files_modified:
  - "<path/to/file1>"
  - "<path/to/file2>"
---END_FIX_SUMMARY---
```

This block is parsed by the leader. Do not deviate from the format.
````

### 9. Commit, push, and send review_addressed (leader post-process)

After the subagent completes:

1. **Generate a GitHub token** for your configured app identity (if applicable). Use this token for `gh` commands and git push.

2. **Parse the fix summary** from the subagent's output. Look for the `---FIX_SUMMARY---` block and extract `fixed`, `deferred`, `pushed_back`, `files_modified`.

3. **Review changes** — run `git diff` in the repo to confirm the edits look correct.

4. **Stage and commit** the modified files:

   ```bash
   git add <files_modified>
   git commit -m "Address review findings (round <current_round>)

   <list of F-xxx: brief description for each fixed finding>

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

5. **Push**:

   ```bash
   git push origin <BRANCH>
   ```

6. **Handle push-backs** — if the subagent flagged any findings as `pushed_back`, send a question to the reviewer for each:

   ```bash
   python3 ${SCRIPTS_DIR}/send_inbox_message.py ${PROJECT} \
     --from <agent_name> --to <REVIEWER> --type question \
     --subject "Question re: <finding_id> (#<PR_NUMBER>)" \
     --body "<push_back_reason>" \
     --related-pr <PR_NUMBER> --priority P2 \
     --oacp-dir "${OACP_ROOT}"
   ```

7. **Build changes summary** from the fixed/deferred/pushed_back lists.

8. **Send review_addressed**:

   ```bash
   python3 ${SCRIPTS_DIR}/send_inbox_message.py ${PROJECT} \
     --from <agent_name> --to <REVIEWER> --type review_addressed \
     --subject "Feedback addressed: round <current_round> (#<PR_NUMBER>)" \
     --body "commit_sha: <LATEST_COMMIT_SHA>
   changes_summary: |
     <CHANGES_SUMMARY>
   round: <current_round>
   task_id: <TASK_ID>" \
     --related-pr <PR_NUMBER> --priority P1 \
     --oacp-dir "${OACP_ROOT}"
   ```

9. **Post PR comment** for human visibility (status only):

   ```bash
   gh pr comment <PR_NUMBER> --repo <REPO> --body "**Feedback addressed (round <current_round>)** — updates pushed for re-review."
   ```

10. **Send review_request for round N+1** to trigger re-review:

    ```bash
    python3 ${SCRIPTS_DIR}/send_inbox_message.py ${PROJECT} \
      --from <agent_name> --to <REVIEWER> --type review_request \
      --subject "Re-review: PR #<PR_NUMBER> (round <current_round + 1>)" \
      --body "pr: <PR_NUMBER>
    branch: <BRANCH>
    diff_summary: |
      Addressed round <current_round> feedback. See review_addressed message for details.
    task_id: <TASK_ID>
    review_round: <current_round + 1>" \
      --related-pr <PR_NUMBER> --priority P1 \
      --oacp-dir "${OACP_ROOT}"
    ```

11. **Increment round**: `current_round += 1`. Check if `current_round > <MAX_ROUNDS>` → Go to Step 12. If `--poll` was NOT provided → exit (single-pass mode complete). Otherwise return to Step 6.

### 10. Handle LGTM (leader)

When a `review_lgtm` message is found:

1. Read the message body. Confirm `quality_gate_result: pass`.
2. Delete the message from inbox.
3. Post PR comment:

   ```bash
   gh pr comment <PR_NUMBER> --repo <REPO> --body "**Review loop complete** — LGTM received from <REVIEWER>. PR is merge-ready."
   ```

4. Do NOT merge the PR — the author or human decides when to merge.
5. Go to Step 11, then report: `STATUS: PASSED`

### 11. Clean up

Delete any remaining processed messages from inbox that belong to this PR (matching `related_pr: <PR_NUMBER>`). Do NOT delete messages for other PRs.

### 12. Handle timeout or escalation

Determine the reason: max rounds exceeded, reviewer escalation, or timeout.

1. Send escalation inbox message:

   ```bash
   python3 ${SCRIPTS_DIR}/send_inbox_message.py ${PROJECT} \
     --from <agent_name> --to team-lead --type notification \
     --subject "Review escalation: PR #<PR_NUMBER>" \
     --body "Review loop escalated after <current_round> rounds.
   Reason: <reason>
   Next steps: Suggest synchronous coordination or human review." \
     --related-pr <PR_NUMBER> --priority P1 \
     --oacp-dir "${OACP_ROOT}"
   ```

2. Post a PR comment:

   ```bash
   gh pr comment <PR_NUMBER> --repo <REPO> --body "**Review loop escalated** — <reason>. Manual coordination needed."
   ```

3. Go to Step 11, then report:

   - `STATUS: ESCALATED` (if max rounds or reviewer escalation)
   - `STATUS: TIMEOUT` (if poll timeout exceeded)

## Notes

- The subagent runs with zero Bash calls — all git/gh/inbox I/O is handled by the leader.
- Default subagent model is sonnet (sufficient for code fixes).
- **Idempotent sends**: Before sending `review_request` or `review_addressed` after a crash/restart, check the reviewer's inbox and own outbox for an already-sent message matching this PR+round. Skip the send if a duplicate exists.
- **Single-pass is the default**: The skill exits after Step 9. After sending `review_addressed`, it also sends a new `review_request` (round N+1) to trigger re-review via `/check-inbox` dispatch. Use `--poll` to revert to in-session polling.
- With `--poll`, handles multi-round loops (up to max-rounds) autonomously.
- The reviewer does not merge — the author (or human) decides when to merge.

## PR Comment Data-Minimization Rule

- PR comments must stay concise and status-oriented.
- Store rich detail in protocol messages and findings packets, not in PR comments.
- Never include command output, logs, stack traces, credentials, environment values, or local paths in PR comments.
- Use `--body-file` with a temp file for PR comments when the body contains dynamic content — avoids shell expansion leaking sensitive data.
