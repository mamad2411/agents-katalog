---
name: dev-code
description: Execute a dev-design plan step by step with user confirmation between each step. Creates branch, updates ticket, implements DB/backend/tests/frontend/E2E/logging sequentially. Offers to trigger /dev-review on completion. Usage — /dev-code <issue-number> [or design doc path]
argument-hint: "<issue-number> [or docs/dev-tech-designs/<ticket>-design.md]"
arguments:
  - name: input
    description: "GitHub issue number, or path to the design doc"
user-invocable: true
context: fork
effort: medium
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(git *)
  - Bash(gh *)
  - Bash(npm *)
  - Bash(npx *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - mcp__git__get_issue
  - mcp__git__update_issue
  - mcp__git__add_issue_comment
---

# Dev Code

> **MCP preferred:** When the `github` MCP is active, use `mcp__git__get_issue`, `mcp__git__update_issue`, `mcp__git__add_issue_comment` instead of `gh` CLI. Fall back to `gh` CLI if MCP unavailable.

Parse `$ARGUMENTS[0]` as either a GitHub issue number or a design doc path.

---

## Step 0 — Load the design plan

```bash
# Find the design doc
find docs/dev-tech-designs/ -name "<number>-design.md" | head -1
```

Read the full design doc. Extract:
1. All phases and their steps (in order)
2. The issue number and title
3. The branch naming convention (from conventional-commit skill: `feat/<number>-<slug>`)

Show the full plan to the user before doing anything:

> **Executing plan for #<number>: <title>**
>
> I'll work through these phases one step at a time. You'll confirm before each step runs.
>
> **Phases:**
> - Phase 1: Database (2 steps)
> - Phase 2: Backend types (1 step)
> - Phase 3: Repository (1 step)
> - Phase 4: Service (1 step)
> - Phase 5: Controller & routes (2 steps)
> - Phase 6: Unit tests (3 steps)
> - Phase 7: Frontend types & API hooks (2 steps)
> - Phase 8: Frontend components (3 steps)
> - Phase 9: Screen / page (1 step)
> - Phase 10: Playwright E2E (1 step)
> - Phase 11: Logging (1 step)
>
> **Before I start:** I'll create the branch and update the ticket status.
>
> Ready? (yes / update the plan first)

If the user says "update the plan first" — stop and let them edit the design doc. They resume by running `/dev-code <number>` again.

---

## Standards lookup (before each phase)

Before generating code for a new **phase**, call the `stack-dispatcher` agent via the Task tool. Pass:
- `task` — the phase summary (e.g. "implement Express route handlers for /users")
- `target_files` — the files this phase will create or edit

The dispatcher returns a concentrated rule set (≤300 lines) drawn from only the installed layers whose `paths:` patterns match these files. Use those rules — and only those rules — to inform the code you generate in this phase.

Do **not** Read layer detail files (`*.md` in `layers/<category>/<tech>/`) directly. The dispatcher and its layer-consultant sub-agents handle that in their own context windows. Reading them inline defeats the purpose of forking this skill.

Call the dispatcher **once per phase**, not once per file — phases generally touch related files, and one consultation covers them.

---

## Execution rules (apply to every step)

1. **Announce before acting:** Before each step, say: `▶ Step <X.Y> — <description>`
2. **Execute the step** as described in the design doc
3. **Show what was produced:** list created/edited files, show key code snippets (not full files)
4. **Wait for confirmation:** after each step, print:
   ```
   ✅ Step <X.Y> complete.
   → Next: Step <X.Z> — <description>
   Continue? (yes / skip / review plan / stop)
   ```
5. **Handle responses:**
   - `yes` — proceed to next step
   - `skip` — skip this step, record it was skipped, move to next
   - `review plan` — stop and tell user to edit `docs/dev-tech-designs/<number>-design.md`, then re-run `/dev-code <number>`
   - `stop` — stop here, summarise what was done, what remains

Never run the next step without explicit confirmation.

---

## Pre-execution: Branch & ticket

Before Phase 1, always run these two setup steps:

### Setup Step A — Create branch

```bash
# Derive slug from issue title
gh issue view <number> --json title --jq '.title' \
  | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | cut -c1-40

git checkout develop 2>/dev/null || git checkout main
git pull
git checkout -b feat/<number>-<slug>
```

Show the branch name. Wait for confirmation.

### Setup Step B — Update ticket status

```bash
gh issue edit <number> --add-label "in-progress"
gh issue comment <number> --body "🚀 Development started on branch \`feat/<number>-<slug>\`"
```

Wait for confirmation before Phase 1.

---

## Phase execution

Execute each phase and its steps exactly as written in the design doc.

### Key rules per phase type:

**Database steps:**
- Follow your database layer skill for schema changes and migration commands
- Never overwrite an existing schema file — append or modify specific sections only
- Pause and confirm required environment variables (connection strings etc.) before running migrations

**Backend steps:**
- Follow your backend layer skill: error handling pattern, response helpers, validation approach
- Follow api-conventions skill: consistent response envelope, correct status codes
- Follow security-principles skill: authenticate every route, check ownership in service layer

**Test steps:**
- Create test files alongside source files (not in a separate tree)
- Follow your testing layer skill: one describe per function/module, mock at the system boundary
- Run the test runner after creating tests and show pass/fail output

**Frontend steps:**
- Follow your frontend layer skill for component patterns
- Lists must handle all states: loading, empty, error, and data
- Forms must handle server-side validation errors (display per-field)
- Run the type checker after writing each file to catch errors immediately

**E2E steps:**
- Follow your E2E testing layer skill: page objects, accessible selectors
- Run the E2E test for the affected flow and show results

**Logging steps:**
- Use the project's structured logger (never `console.log` in production code)
- Log at the service layer for business events (create/update/delete)
- Never log passwords, tokens, or PII in any field

---

## Post-execution — Commit

After all steps (or when the user says done):

```bash
git add -p   # show what's staged
git status
```

> Here's what I built:
> - <list of created/modified files>
>
> Commit message I'll use:
> `feat(<scope>): <description> (#<number>)`
>
> Commit and push? (yes / edit message / no)

If yes:
```bash
git add <specific files only — no -A>
git commit -m "feat(<scope>): <description> (#<number>)"
git push -u origin feat/<number>-<slug>
```

---

## Completion — offer dev-review

> All steps complete for #<number>.
>
> **Built:**
> - Phase 1–11 executed (or list which were skipped)
> - Branch: `feat/<number>-<slug>`
> - Commit pushed
>
> Run code review now?
> ```
> /dev-review
> ```
> (yes / no)

If yes, trigger `/dev-review`. If no, remind them to run it before creating the PR.
