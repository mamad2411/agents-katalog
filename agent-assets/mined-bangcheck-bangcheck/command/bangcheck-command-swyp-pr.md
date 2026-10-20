# /swyp-pr — Issue-linked PR Creation

---

## IMPORTANT: Rules

**Placeholder Resolution:** NEVER execute a bash command while any `{placeholder}` remains unresolved. Collect all values through conversation first, then run the final command with real values substituted.

**No interactive UI:** Do NOT use interactive selection tools or AskUserQuestion. Display options as plain text and wait for the user to type a response.

**Conversational tone:** At every decision point, ask one question at a time in a natural conversational style rather than showing a numbered menu.

---

## Pre-checks

1. **Branch** — block if main/master
2. **uncommitted changes** — guide to /swyp-commit
3. **gh auth** — stop if not authenticated
4. **Commit check** — stop if `git log main..HEAD` has no commits
5. **Existing PR** — notify if open PR exists for same branch

---

## Step 1: Verify Issue Number

Priority:
1. Specified as argument: `/swyp-pr #12`
2. Extract from branch name: `feat/12-login-page` → `#12`
3. Extract from commit messages
4. Ask user (skip is allowed)

Issue verification: `gh issue view {number}` — check existence/state

### Test Scenario Check

Parse "## Test Cases" from issue body:

```
Issue #{number} test scenarios:
  ✅ Passed items
  ❌ Unverified items      ← warning
```

If unverified items exist, ask conversationally:

```
Q. Issue #{n} has {count} unverified test scenarios. Would you like to verify them before creating the PR, or proceed anyway?
  Unverified:
    □ {item 1}
    □ {item 2}
```

Wait for the user's answer before proceeding.

### Auto Status Label Change

이 단계는 2026-08-05에 제거했다.

`status:progress`·`status:review` 라벨이 이 저장소에 존재하지 않는다.
실제 라벨은 `유형:버그`·`유형:작업`·`높음`/`보통`/`낮음`·`백엔드`/`프론트엔드`뿐이라
위 명령은 `gh` 오류로 끝났다 — 시키는 대로 따라 하면 그 줄에서 멈춘다.

`_compliance-spec.yaml`의 `issue_labels` 규칙도 같은 이유로 비활성화돼 있다(#218).
라벨 체계가 확정되면 그 시점에 규칙과 이 단계를 한 번에 되살린다(#224).

PR 상태는 GitHub의 PR 상태 자체가 말한다 — 별도 라벨을 두면 정본이 둘이 된다.

---

## Step 2: Change Scope Analysis

```bash
git log main..HEAD --oneline
git diff main...HEAD --stat
```

---

## Step 3: PR Title

- 1 commit → use commit message
- Multiple → overall summary (72 chars max)
- Confirm with user

---

## Step 4: PR Body

```markdown
## Summary
- {bullet 1~3}

## Linked Issue
Closes #{number}

## Changes
| File | Change |
|------|--------|
| {path} | New/Modified/Deleted |

## Screenshots (if UI changes)
| Before | After |
|--------|-------|
| | |

## Checklist
- [ ] Feature works correctly
- [ ] No impact on existing features
- [ ] Code conventions followed
- [ ] Responsive verified (if applicable)
```

Omit "Linked Issue" if no issue. For multiple issues, use `Closes #N` for each.

---

## Step 5: Reviewer Assignment

Fetch collaborators:
```bash
gh api repos/{repo}/collaborators --jq '.[].login'
```

Then ask conversationally:

```
Q. Who should review this PR? (type names or GitHub handles, comma-separated — or press Enter to skip)
  Team members: {list from gh api}
```

Wait for the user's input before proceeding. Skip reviewers for draft PR.

---

## Step 5.5: Draft PR Check

Ask conversationally:

```
Q. Should this be a draft PR (not ready for review yet), or is it ready for review?
```

Wait for the user's answer, then add `--draft` flag if applicable.

---

## Step 6: push + PR Creation

```bash
git push -u origin {branch}  # when no upstream
gh pr create --title "{title}" --body "{body}" --base main --reviewer "{reviewers}"
```

Add `--draft` for draft PR

---

## Step 7: Completion Report

```
PR creation complete
- PR: #{number} — {url}
- base ← head: main ← feat/12-login-page
- Linked issue: #12
- Reviewer: @teammate

After merge:
  1. Issue #12 auto-closes
  2. git checkout main && git pull
  3. git branch -d feat/12-login-page
```

After the report, ask:

```
What would you like to do next?
  [1] View PR in browser — gh pr view --web
  [2] Continue on another issue
  [3] Done
```

(plain text — wait for the user to type a response)

---

## Safety Guards

| Rule | Action |
|------|--------|
| PR from main | Block |
| uncommitted changes | Guide to /swyp-commit |
| Existing open PR | Prevent duplicate |
| force push | Forbidden |
| PR without issue | Warn then allow |
| No reviewer | Warn then allow |
