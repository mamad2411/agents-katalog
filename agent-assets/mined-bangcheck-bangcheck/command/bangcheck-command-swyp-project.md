# /swyp-project — Project Board Creation and Management

Creates and manages GitHub Project boards, labels, and milestones.

---

## Pre-checks

1. `gh auth status` — stop if not authenticated
2. `git remote get-url origin` — verify repo
3. Scan existing labels/milestones/board status

---

## Case Selection

If no argument, display menu:

```
SWYP Project Management

1. [init]      Project initialization (labels + milestones + board + batch page registration)
2. [add]       Add page/feature (extend existing project)
3. [status]    Current project status (including test progress)
4. [update]    Change issue status (in progress/waiting/blocking, etc.)
5. [milestone] Create/close milestones
6. [label]     Add/modify labels
```

---

## init — Project Initialization

### Batch label creation (skip if already exists)

Type: `page`(#1D76DB), `task`(#0E8A16), `bug`(#D73A4A), `improvement`(#A2EEEF)
Priority: `P0-critical`(#B60205), `P1-urgent`(#D93F0B), `P2-normal`(#FBCA04), `P3-backlog`(#0E8A16)
Role: `frontend`(#7057FF), `backend`(#0052CC), `design`(#F9D0C4)
Status: `status:backlog`(#EDEDED), `status:todo`(#D4C5F9), `status:progress`(#0075CA), `status:blocked`(#E11D48), `status:review`(#F59E0B), `status:done`(#0E8A16)

```bash
gh label create "{name}" --color "{color}" --description "{desc}" --repo {repo} 2>/dev/null || true
```

### Milestone creation

Prompt user for name input (default: "Sprint 1"):

```bash
gh api repos/{repo}/milestones -f title="{name}" -f state="open"
```

### Project board creation

```bash
gh project create --owner {owner} --title "SWYP Checklist"
```

Note: Configure columns in GitHub web → `Backlog` → `Todo` → `In Progress` → `Review` → `Done`

---

## status — Status Overview

```bash
gh issue list --repo {repo} --state open --json number,title,labels,assignees,milestone --limit 100
gh pr list --repo {repo} --state open --json number,title,author,reviewRequests
gh api repos/{repo}/milestones --jq '.[] | {title, open_issues, closed_issues}'
```

Output:

```
SWYP Project Status — {date}

## Open Issues by Priority
| Priority | Open | Assigned | Unassigned |
|----------|------|----------|------------|

## Milestone Progress
| Milestone | Open | Closed | Progress |
|-----------|------|--------|----------|

## Open PRs
| PR | Title | Author | Review Status |
|----|-------|--------|---------------|
```

## Test Progress
| Page | Total | Passed | Progress |
|------|-------|--------|----------|
```

Warning conditions: unresolved P0, unassigned P1, PR without reviewer, issue without labels

---

## add — Add Page/Feature

Adds pages or features to existing project:
1. Add page (batch: page issue + task + test scenarios)
2. Add standalone task
3. Add infrastructure work

Assign to existing milestones, distribute assignees, auto-generate test scenarios

---

## update — Change Issue Status

```
/swyp-project update #12

Current: status:progress
1. [backlog]   Backlog
2. [todo]      Planned
3. [progress]  In Progress
4. [blocked]   Blocked (enter reason)
5. [review]    Awaiting Review
6. [done]      Done
```

상태 라벨 전이는 2026-08-05에 제거했다.

`status:*` 라벨이 이 저장소에 존재하지 않아 위 명령은 `gh` 오류로 끝났다.
보드의 상태 필드를 쓰거나, 라벨 체계를 먼저 확정한다(#224).

blocked: enter reason → add issue comment
done: warn if unverified tests exist

---

## milestone — Milestone Management

- `create` — enter name → create
- `close` — warn if open issues exist → move to next milestone or force close
- `list` — current milestone list + progress

---

## Safety Guards

- Do not recreate existing labels/milestones
- Verify open issues before closing milestone
- Prevent duplicate project board creation
