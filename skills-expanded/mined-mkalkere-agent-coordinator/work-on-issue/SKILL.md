---
name: work-on-issue
version: 1.0.0
description: Full workflow to implement an issue — from claim to merged PR
uses:
  - coordination/ac-http
  - development/git
  - development/pr-create
  - development/pr-complete
requires:
  tools: [git, gh, curl]
  env: []
security:
  risk_level: write
  capabilities:
    - git:read
    - git:write
    - github:issue:read
    - github:pr:write
    - coordinator:write
  requires_approval: false
---

# Work on Issue

Full workflow from receiving a task to a reviewed PR. This skill orchestrates
the entire development lifecycle by composing other skills.

**Platform note**: Uses GitHub (`gh` CLI). The methodology is platform-agnostic;
only the tool commands are GitHub-specific.

## STOP — Read This Entire Skill Before Starting

Do NOT begin work until you have read every phase below.
Each phase has a **Checkpoint** — verify it before moving to the next phase.
Skipping any phase leaves the task in a broken state and blocks all downstream agents.

**After reading all phases, output this confirmation before proceeding:**
```
SKILL LOADED: work-on-issue
Phases: 0, 0.5, 1, 2, 3, 4, 5, 6, 7
Gate: After tests pass in Phase 3, proceed to Phase 4 IMMEDIATELY.
```

**Lifecycle Rule**: Once your primary work is done (tests pass), move to
lifecycle phases (commit, PR, notifications) IMMEDIATELY. If you skip them,
the task stays in a broken state. The system monitors lifecycle completion —
incomplete tasks may be flagged, restarted, or reassigned.

## Execution Model

This is a **bash skill** (`handler: type: bash`). The `issue_fetch` tool
(defined in tool.yaml) fetches issue details via `gh issue view`. The rest of
this workflow is orchestrated by YOU, the agent, following the phases below.
You compose other skills (git, pr-create, pr-complete, ac-http) as needed.

## When to Use

- Starting work on a new issue
- Picking up a task assigned through the coordinator
- Any time you need the full claim → branch → implement → PR → review cycle

## Methodology

### Phase 0: Workspace Setup (MANDATORY FIRST STEP)

**You MUST work in your own clone. Never modify files in the shared checkout.**

Your agent name comes from your identity.yaml (`name` field) and is provided
in your initialization prompt. Use it to construct your workspace path.

**Platform note**: Commands below use Git Bash syntax. On Windows, `$HOME`
expands to `C:\Users\<username>` in Git Bash. Adjust if using PowerShell.

Run these commands BEFORE doing anything else:

```bash
# Step 1: Check if the server already placed you in a worktree.
# When spawned via the coordinator, your cwd IS the worktree.
# A git worktree has a .git FILE (not a directory) pointing to the main repo.
if [ -f .git ]; then
    echo "Already in a git worktree at: $(pwd)"
    WORKSPACE="$(pwd)"
    # Ensure worktree is up to date with remote
    git fetch origin main
else
    # Step 2: Determine workspace path and clone/update
    AGENT_NAME="{your-agent-name}"     # from identity.yaml 'name' field
    REPO_NAME="{repo-name}"            # e.g., "agent-coordinator"
    REPO_URL="https://github.com/{owner}/{repo}"  # from task message
    WORKSPACE="$HOME/workspaces/${AGENT_NAME}/${REPO_NAME}"

    if [ ! -d "$WORKSPACE" ]; then
        git clone "$REPO_URL" "$WORKSPACE"
    else
        cd "$WORKSPACE" && git checkout main && git pull --ff-only
    fi

    cd "$WORKSPACE"
fi

# Step 3: VALIDATE — you must NOT be in the shared main checkout
echo "Current directory: $(pwd)"
git rev-parse --show-toplevel
```

> **Checkpoint**: Run `pwd`. The output MUST contain your agent name
> (e.g., `/workspaces/developer/`). If it does NOT, you are in the shared
> checkout. STOP and re-run the commands above.
>
> **Worktree check**: Run `cat .git` — if it says `gitdir: ...` you are in a
> worktree (correct). If `.git` is a directory, you are in a full clone (also OK).

**Why**: Multiple agents may work simultaneously. If two agents modify the same
checkout, they corrupt each other's branches, overwrite files, and create merge
conflicts. Your own clone is your sandbox.

### Phase 0.5: Check Before Starting

Before claiming, verify the work isn't already in progress:

```bash
# Extract task_id from the bus message payload
TASK_ID="{task_id}"  # from the message that triggered you
COORDINATOR="${AC_COORDINATOR_URL:-http://localhost:9889}"

# Check coordinator task status
curl -s "${COORDINATOR}/tasks/${TASK_ID}"
# (read the JSON response — look for "status" and "agent_id" fields)

# Check GitHub issue
gh issue view {issue_number}
```

**Alternative**: Use the `coordinator_request` tool from the ac-http skill
instead of curl if available in your tool set.

Decision logic:
- If coordinator task `status` is `claimed` or `in_progress` by another agent → skip this task
- If GitHub issue has an assignee or "in progress" label → skip this task
- If the task `status` is `open` or `new` → proceed to Phase 1

**CRITICAL**: The `task` message that triggered you includes a `task_id` field.
Use this ID throughout the entire workflow. Do NOT create a new task via
`POST /tasks` — the task already exists on the coordinator board.

### Phase 1: Claim (MANDATORY)

```bash
COORDINATOR="${AC_COORDINATOR_URL:-http://localhost:9889}"
AGENT_NAME="{your-agent-name}"
TASK_ID="{task_id}"  # from bus message, NOT a new one

# Step 1: Claim the EXISTING task
curl -s -X POST "${COORDINATOR}/tasks/${TASK_ID}/claim?agent_id=${AGENT_NAME}"
# Expected: {"task_id": N, "claimed": true}
# If 409 → already claimed — see recovery below

# Step 2: Move to in_progress
curl -s -X POST "${COORDINATOR}/tasks/${TASK_ID}/status?new_status=in_progress&agent_id=${AGENT_NAME}"

# Step 3: Update GitHub issue
gh issue edit {issue_number} --add-assignee @me
gh issue edit {issue_number} --add-label "in progress"
```

**Publish to bus** (use the `bus_publish` MCP tool):
```json
{
  "channel": "work",
  "type": "task_claimed",
  "message": {
    "task_id": "{task_id}",
    "issue_number": "{issue_number}",
    "agent": "{your-agent-name}"
  }
}
```

> **Checkpoint**: Run `curl -s "${COORDINATOR}/tasks/${TASK_ID}"`.
> Verify: `status` is `in_progress`, `agent_id` is your name.

**If claim fails (409)**:
1. Publish `task_claim_failed` to the work channel with the task_id
2. Check for other available tasks: `curl -s "${COORDINATOR}/tasks?status=open"`
3. If another task is available, restart from Phase 0.5 with the new task
4. If no tasks available, publish `idle` status to the system channel and exit gracefully

### Phase 2: Branch

```bash
# Ensure on main and up to date
git checkout main && git pull --ff-only

# Create feature branch
git checkout -b fix/{issue_number}-{short-description}
# or: feat/{issue_number}-{short-description}

# Verify
git branch --show-current
```

> **Checkpoint**: `git branch --show-current` shows your feature branch name.

### Phase 3: Implement

Do the actual work:
1. Read and understand the issue requirements (`gh issue view {issue_number}`)
2. Write code to solve the issue
3. Run tests frequently during implementation (`py -m pytest tests/ -v` or equivalent)
4. Keep changes focused on the issue — no scope creep
5. Commit incrementally during complex changes (conventional commit format)

**GATE: Once tests pass, proceed to Phase 4 IMMEDIATELY.**
Do NOT continue refining implementation after tests pass. The lifecycle phases
(commit, PR, notifications) are more important than polish. You can always
iterate in Phase 6 after review feedback.

### Phase 4: Commit

```bash
# Step 1: Run full test suite
py -m pytest tests/ -v

# Step 2: Save learnings
# Write what you learned to .os/agents/{your-name}/memory/
# (use markdown files with descriptive names)

# Step 3: Stage specific files (NEVER use 'git add .' or 'git add -A')
git add src/path/to/changed/file.py tests/path/to/test.py
git add .os/agents/{your-name}/memory/

# Step 4: Commit with conventional format
git commit -m "fix(scope): description (#issue_number)"

# Step 5: Push to remote
git push -u origin $(git branch --show-current)
```

> **Checkpoint**: `git log main..HEAD --oneline` shows your commits.
> `git push` succeeded (no errors).

### Phase 5: PR + Lifecycle (MANDATORY — DO NOT SKIP)

**This is the most commonly skipped phase. It MUST be completed or
downstream agents are never activated.**

```bash
# Step 1: Create the PR
gh pr create \
  --title "fix(scope): description (#issue_number)" \
  --body "Closes #{issue_number}

## Summary
- [what you changed and why]

## Test Plan
- [how to verify the changes]"
```

Record the PR number from the output.

```bash
# Step 2: Move task to review (releases ownership for reviewer)
COORDINATOR="${AC_COORDINATOR_URL:-http://localhost:9889}"
curl -s -X POST "${COORDINATOR}/tasks/${TASK_ID}/status?new_status=review&agent_id=${AGENT_NAME}"
```

**Publish to bus** (use the `bus_publish` MCP tool):
```json
{
  "channel": "work",
  "type": "pr_created",
  "message": {
    "task_id": "{task_id}",
    "issue_number": "{issue_number}",
    "pr_number": "{pr_number}",
    "title": "{pr_title}",
    "agent": "{your-agent-name}"
  }
}
```

> **Checkpoint**: `gh pr view` shows your PR. Task status is `review`.
> A `pr_created` message exists on the work channel.

### Phase 6: Iterate

Handle the review cycle. Phase 6 typically happens in a **separate session** —
after Phase 5, you may exit. When a review message arrives on the bus, your
wrapper restarts you with that context.

**Trigger**: A `review_completed` (changes requested) or `review_changes_requested`
message arrives on the work channel.

Steps:
1. Read the review comments: `gh pr view {pr_number} --comments`
2. For each comment, address the feedback in your workspace
3. Run tests: `py -m pytest tests/ -v` (or equivalent)
4. Commit and push fixes with conventional format
5. Re-publish `pr_created` to the work channel to re-trigger review
6. Repeat until a `review_approved` message arrives

**If `review_approved` arrives**: Proceed to Phase 7.

> **Checkpoint**: All review comments are addressed. New commits are pushed.
> `pr_created` is re-published to trigger re-review.

### Phase 7: Handoff to Human

**Agents do NOT merge PRs. Merging is a human-only action.**

After the PR is approved:
1. Verify CI passes and PR has an approval
2. **DO NOT merge** — leave the PR open for the human

**Publish to bus** (use the `bus_publish` MCP tool):
```json
{
  "channel": "work",
  "type": "merge_ready",
  "message": {
    "task_id": "{task_id}",
    "issue_number": "{issue_number}",
    "pr_number": "{pr_number}"
  }
}
```

The task stays in `approved` status. The human merges and moves to `done`.

## Output Format

Display this progress table as you complete each phase:

```
## Issue Workflow

- Issue: [#N — title]
- Phase: [0/0.5/1/2/3/4/5/6/7]
- Status: [in-progress/blocked/complete]

### Progress
| Phase | Status | Details |
|-------|--------|---------|
| 0. Workspace | [done/pending] | [workspace path] |
| 0.5. Check | [done/pending] | [task available?] |
| 1. Claim | [done/pending] | [task ID, status] |
| 2. Branch | [done/pending] | [branch name] |
| 3. Implement | [done/pending] | [summary] |
| 4. Commit | [done/pending] | [commit hash] |
| 5. PR | [done/pending] | [PR number, bus published?] |
| 6. Iterate | [done/pending] | [review status] |
| 7. Handoff | [done/pending] | [merge_ready published?] |
```

## Quality Criteria

> **Before committing**: Read `references/code-quality.md` in this skill directory.
> It contains patterns for test quality, DRY, closures, and clock domains
> based on real bugs found during independent code review.

- [ ] Agent works in its own clone (`~/workspaces/{agent-name}/{repo-name}/`), NOT the shared checkout
- [ ] Existing task is claimed using `task_id` from bus message — NOT duplicated via `POST /tasks`
- [ ] GitHub issue is assigned and labeled "in progress" on claim
- [ ] Task status is `in_progress` via `POST /tasks/{task_id}/status`
- [ ] `task_claimed` published to `work` channel after claiming
- [ ] Feature branch follows naming convention: `fix/{number}-desc` or `feat/{number}-desc`
- [ ] Implementation matches issue requirements, tests pass
- [ ] PR is created, linked to issue with `Closes #N`
- [ ] Task moved to `review` status (ownership released for reviewer)
- [ ] `pr_created` published to `work` channel with task_id + pr_number
- [ ] Agent NEVER merges PRs — merging is human-only
- [ ] After approval, `merge_ready` published and task stays in `approved`

## Common Mistakes

- **Working in the shared checkout** — Consequence: other agents' branches get corrupted. Human's working directory gets polluted with your uncommitted changes. Commits may include unrelated files.
  **Fix**: ALWAYS `cd ~/workspaces/{your-agent-name}/{repo-name}/` first.

- **Creating a new task instead of claiming the existing one** — Consequence: duplicate tasks on the coordinator board. Original task stays unclaimed forever. Dashboard shows wrong state.
  **Fix**: Use `POST /tasks/{task_id}/claim` with the `task_id` from the bus message.

- **Not updating task status to in_progress** — Consequence: task stays stuck on `claimed`. Other agents can't see progress. Dashboard shows stale state.
  **Fix**: Call `POST /tasks/{task_id}/status?new_status=in_progress` right after claiming.

- **Not publishing bus notifications** — Consequence: downstream agents (reviewer) are NEVER activated. PR sits unreviewed indefinitely. Task lifecycle is broken.
  **Fix**: Publish `task_claimed` after claiming, `pr_created` after PR, `merge_ready` after approval.

- **Exhausting turns on implementation** — Consequence: no PR created, no bus messages published, task is orphaned. The system may detect this and flag the task as incomplete.
  **Fix**: Once tests pass, move to Phase 4 immediately. Do not continue polishing after tests pass.

- **Scope creep** — Consequence: review takes longer, unrelated changes get mixed in, harder to debug if something breaks.
  **Fix**: Keep changes focused on the issue. Create separate issues for improvements.

- **Skipping tests** — Consequence: review cycle catches avoidable failures. Wastes turns on fix-review-fix loops.
  **Fix**: Run `py -m pytest tests/ -v` before committing.

- **Not linking the issue in PR** — Consequence: issue won't auto-close on merge.
  **Fix**: Include `Closes #N` in the PR body.

## Failure Recovery

If something goes wrong mid-workflow:

- **Tests fail in Phase 4**: Fix the failure. Do NOT skip to Phase 5 with broken tests.
  If you cannot fix it, commit what you have, create the PR anyway, and note the
  failure in the PR body so the reviewer knows.

- **Coordinator unreachable**: Create the PR anyway — git and GitHub work independently.
  Note in the PR body: "Coordinator status not updated — update manually." The lifecycle
  notifications can be sent when the coordinator is back.

- **`git push` fails**: Check auth (`gh auth status`), check branch protections, try
  `git push --set-upstream origin $(git branch --show-current)` explicitly. If auth
  fails, check `CLAUDE_CODE_OAUTH_TOKEN` or re-authenticate.

- **PR creation fails**: Verify branch was pushed (`git log origin/{branch}..HEAD`),
  check `gh auth status`, try `gh pr create` again with explicit flags.

- **Claim fails (409)**: See Phase 1 recovery steps above.

- **Issue already has a PR**: Check `gh pr list --head {branch}` — if a PR exists,
  don't create a duplicate. Push to the existing branch instead.

## Completion

The workflow is complete when ALL of these are true:
- [ ] Workspace is in own clone (`~/workspaces/{agent-name}/{repo-name}/`)
- [ ] Existing task is claimed (not duplicated) and `task_claimed` published to `work` bus
- [ ] GitHub issue is assigned and labeled
- [ ] Code is implemented, tested, committed, and pushed
- [ ] Learnings saved to `.os/agents/{your-name}/memory/` and committed
- [ ] PR is created and linked to the issue
- [ ] Task is in `review` status (ownership released for reviewer)
- [ ] `pr_created` published to `work` bus
- [ ] Agent does NOT merge — human merges after approval
- [ ] After approval: `merge_ready` published, task stays in `approved`
