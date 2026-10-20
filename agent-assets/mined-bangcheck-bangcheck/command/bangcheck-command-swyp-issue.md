# /swyp-issue — GitHub Issue Registration

Determines type and priority interactively and creates a structured issue.

---

## Entry Point: Cache-First Spec Loading

**Before any issue creation involving spec data (page/task from spec), run this check:**

```bash
CACHE="_wood/cache/spec-snapshot.json"
if [ -f "$CACHE" ]; then
  echo "CACHE_HIT"
  cat "$CACHE" | jq '{cached_at, screen_count: (.screens | length)}'
else
  echo "CACHE_MISS"
fi
```

| Result | Action |
|--------|--------|
| `CACHE_HIT` | Load screens from cache — **skip all MCP Drive calls** |
| `CACHE_MISS` | Run `step-01-read-drive.md` once to populate cache, then continue |

> 명세 없이 bug/improvement 이슈는 캐시 체크 없이 바로 진행.

---

## IMPORTANT: Placeholder Resolution Rule

**NEVER execute a bash command while any `{placeholder}` remains unresolved.**
Collect ALL required values through conversation first, then construct and run the final command with real values substituted.

Required values before any `gh issue create`: `repo` (from `git remote get-url origin`), `title`, `priority`, `milestone` (or skip), `assignee` (or skip).

**Labels are NOT used.** Do NOT pass `--label` to any `gh issue create` command.

**GitHub Projects board linking is MANDATORY after every issue creation:**
```bash
# Store issue URL from gh issue create output, then:
gh project item-add 2 --owner SWYP-Backend --url {issue-url}
```
Project: `2` (SWYP Checklist, owner: SWYP-Backend). Run this immediately after every `gh issue create`.

---

## Pre-checks

1. `gh auth status` — stop if not authenticated
2. `git remote get-url origin` — resolve `{repo}` (e.g. `SWYP-Backend/project`)
3. Duplicate check — search for similar titles and warn

---

## Case Selection

```
SWYP Issue Registration

1. [page]        Page-level issue (parent — includes task checklist)
2. [task]        Task-level issue (child — linked to parent issue)
3. [bug]         Bug report
4. [improvement] Improvement suggestion
```

Direct invocation: `/swyp-issue page login-page`, `/swyp-issue task #10 login-form`, `/swyp-issue bug kakao-login-failure`

---

## Common: Priority Recommendation

**Display as plain text only. Do NOT use interactive selection tools or AskUserQuestion.**
Output the list as text and wait for the user to type a number.

Auto-recommendation logic:

| Condition | Recommendation |
|-----------|----------------|
| bug + crash / white screen / data loss / service down | P0-critical |
| bug + 500 error / login failure / payment failure / core feature broken | P1-urgent |
| page or task issue | P2-normal |
| task issue | Inherits parent priority |
| improvement / refactoring | P3-backlog |

Output format (plain text, no interactive UI):

```
Select priority (enter a number):

1. P0 — Immediate (service completely down)
   e.g. service down, data loss, full white screen
   → Stop everything and respond right now

2. P1 — Same day (core feature broken)  ← {recommendation if applicable}
   e.g. login failure, payment failure, 500 error, key API not responding
   → Handle before other tasks, target same-day resolution

3. P2 — Next sprint (general feature development)
   e.g. new page, intermittent error, bug with a workaround
   → Handle according to sprint schedule

4. P3 — Backlog (non-urgent improvement)
   e.g. UI improvement, refactoring, minor bug, typo
   → Handle when there is spare capacity

Recommendation: {P0/P1/P2/P3} ({reason})
```

## Common: Milestone + Assignee

Display open milestones list → select (or skip)
Assignee: self / select team member / skip

---

## page — Page-level Issue

Information gathering:
1. Page name
2. List of main features (separated by Enter)
3. Test scenarios (auto-suggested + user edits)
4. API endpoint (optional)

Auto-suggested task items:
- Page layout + routing
- Core UI components
- API integration
- Error handling
- Loading states
- Responsive layout

If form page, add: validation, submit logic, success/failure feedback
If list page, add: pagination, filter/sort, empty state UI

```bash
gh issue create --repo {repo} --title "[page] {title}" \
  --milestone "{milestone}" \
  --body "{body: description + task list + API + test cases + completion criteria}"
# Capture the output URL, then immediately link to project board:
gh project item-add 2 --owner SWYP-Backend --url {issue-url}
```

After creation: "Would you like to create individual task issues from the task list?" → if Y, batch create

---

## task — Task-level Issue

Parent verification:
- Parent number provided as argument → confirm
- If not provided, display open page issue list → select (or create independently)

```bash
gh issue create --repo {repo} --title "[task] {title}" \
  --milestone "{milestone}" \
  --body "Parent: #{parent}\n\n## Implementation Details\n{desc}\n\n## Completion Criteria\n- [ ] Feature works correctly\n- [ ] Code conventions followed"
# Immediately link to project board:
gh project item-add 2 --owner SWYP-Backend --url {issue-url}
```

After creation, automatically add issue number to parent checklist

---

## bug — Bug Report

Interactive collection: Steps to reproduce → Expected result → Actual result → Error log (optional)

Keyword-based priority recommendation:
- Crash/white screen/data loss → P0
- Error/failure/broken → P1
- Slow/inconvenient/intermittent → P2
- Typo/minor/trivial → P3

```bash
gh issue create --repo {repo} --title "[bug] {title}" \
  --body "{Steps to reproduce + expected/actual result + environment + screenshot}"
# Immediately link to project board:
gh project item-add 2 --owner SWYP-Backend --url {issue-url}
```

---

## improvement — Improvement Suggestion

Collect: Current situation → Improvement direction → Reason
Default priority: P3-backlog

---

## Post-creation Common Processing

1. Report issue URL
2. Always display the next-action menu:

```
Issue #{n} created: {url}

What would you like to do next?
  [1] Start working now    — create branch + set status:progress
  [2] Create task issues   — batch-create checklist items as individual task issues
  [3] Register another     — create another issue
  [4] Go to PM space       — check sprint status
  [5] Go to FE space       — start frontend work
  [6] Go to BE space       — start backend work
  [7] View backlog         — unassigned issue list
  [8] Done                 — exit
```

| Input | Action |
|-------|--------|
| 1 | Run pick flow (create branch + update label) |
| 2 | Parse checklist → batch create task issues linked to parent |
| 3 | Return to case selection |
| 4 | Load `/swyp-pm` agent |
| 5 | Load `/swyp-fe` agent |
| 6 | Load `/swyp-be` agent |
| 7 | Run backlog flow |
| 8 | Exit |

---

## Safety Guards

- Duplicate issue detection → warning
- Task without parent → warn then allow
- Linking to closed parent → warn then confirm
