# /swyp-test — Test Scenario Management

Manages test cases for issues and tracks overall test status.

---

## IMPORTANT: Rules

**Placeholder Resolution:** NEVER execute a bash command while any `{placeholder}` remains unresolved. Collect all values through conversation first, then run the final command with real values substituted.

**No interactive UI:** Do NOT use interactive selection tools or AskUserQuestion. Display options as plain text and wait for the user to type a response.

**Conversational tone:** At every decision point, ask one question at a time in a natural conversational style rather than showing a numbered menu.

---

## Pre-checks

1. `gh auth status` — stop if not authenticated
2. `git remote get-url origin` — verify repo

---

## Case Selection

Instead of showing a numbered menu, ask conversationally:

```
Q. What would you like to do?
  - Check overall test status
  - View test details for a specific issue
  - Add test cases to an issue
  - Generate a test report by milestone
```

Wait for the user to describe what they want, then route to the appropriate flow below.

---

## status — Overall Test Status

```bash
gh issue list --repo {repo} --label "page" --state all --json number,title,body,state --limit 50
```

Parse "## Test Cases" section from each page issue body:
- `- [x]` → passed (✅)
- `- [ ]` → unverified (❌)

Output:

```
SWYP Test Status — {date}

## Overall Summary
| Total | Passed | Unverified | Progress |
|-------|--------|------------|----------|
| {n} | {n} | {n} | {%} |

## Details by Page

### [page] Login Page (#10) — 67% (6/9)

  Working correctly:
    ✅ Login success with email/password
    ✅ Kakao social login success
    ✅ Redirect to main page after login

  Exception handling:
    ✅ Wrong password → error message
    ❌ Network error → retry prompt
    ✅ Empty field submission → validation

  UI/UX:
    ✅ Mobile responsive OK
    ❌ Loading spinner
    ❌ Password show/hide
```

Warnings: page without test section, closed with unverified items, progress below 50%

---

## view — Test Details for Specific Issue

```bash
gh issue view {number} --repo {repo} --json number,title,body,labels
```

If page issue, also collect tests from child tasks:

```
[page] Login Page (#10) — Test Details

## Page Tests (6/9)
  ✅ / ❌ item listing

## Tests by Task
  #11 Login Form UI (3/3) ✅
  #12 Kakao Social Login (1/3) ⚠
```

---

## add — Add Test Cases

Adds to existing test section, or creates a new one if absent.

First, ask conversationally to tailor suggestions:

```
Q. Is this a form page, list page, CRUD page, task, or bug fix? (This helps me suggest relevant test categories)
```

Wait for the user's answer, then present tailored suggestions based on the table below:

| Type | Suggested Categories |
|------|---------------------|
| Form | Normal submission, validation, server error, UI/UX |
| List | Data loading, empty state, pagination, UI/UX |
| CRUD | Read/Create/Update/Delete, permissions, UI/UX |
| task | Feature operation, error scenarios, no existing impact |
| bug | Reproduction confirmed, fixed correctly, no regression |

After presenting suggestions and the user confirms which to add:

```bash
gh issue edit {number} --body "{updated_body}" --repo {repo}
```

After adding tests, ask:

```
Q. Would you like to add more test cases, view the updated issue, or return to the test overview?
```

Wait for the user's answer before continuing.

---

## report — Report by Milestone

```bash
gh issue list --repo {repo} --milestone "{name}" --state all --json number,title,body,labels,state --limit 100
```

```
Test Report — {milestone}

| Page | Total | Passed | Progress | Status |
|------|-------|--------|----------|--------|
| Login (#10) | 9 | 9 | 100% | ✅ |
| Checklist (#20) | 12 | 8 | 67% | ⚠ |

Risks:
- {warning for pages with low progress}
```

---

## Safety Guards

- Preserve original if issue body edit fails
- Issue without test section → guide to add
- Closed with unverified items → warning
