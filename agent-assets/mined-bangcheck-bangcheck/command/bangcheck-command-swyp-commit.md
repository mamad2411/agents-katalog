# /swyp-commit — Commit + Push with Team Commit Rules

---

## IMPORTANT: Rules

**Placeholder Resolution:** NEVER execute a bash command while any `{placeholder}` remains unresolved. Collect all values through conversation first, then run the final command with real values substituted.

**No interactive UI:** Do NOT use interactive selection tools or AskUserQuestion. Display options as plain text and wait for the user to type a response.

**Conversational tone:** At every decision point, ask one question at a time in a natural conversational style rather than showing a numbered menu.

---

## Pre-checks

1. **Branch check** — block if main/master:
   > "Cannot commit directly to main. Create a branch with /swyp-entry pick."

2. **Change check** — `git status --short`, `git diff --stat`
   - No changes → stop

3. **Dangerous file scan** — `.env`, `*.pem`, `*.key`, `credentials.*`, `secret*`
   - Detected → immediately block + remove from staging + guide to .gitignore

---

## Step 1: Change Scope Analysis

```bash
git diff --stat
git diff --cached --stat
```

### Commit Split Decision

- Code + styles for same feature → 1 commit
- Different features → suggest split
- Code + unrelated config → suggest split

When splitting is suggested, ALWAYS show the reason first, then ask:

```
변경 파일이 {n}가지 관심사에 걸쳐 있어 분리를 추천합니다.

- {scope 1} ({type}): {files} — {reason}
- {scope 2} ({type}): {files} — {reason}

관심사가 다르면 롤백/이력 추적 단위가 달라 분리가 유리합니다.
분리할까요, 하나로 묶을까요?
```

Wait for the user's answer before proceeding. DO NOT run any git commands before this answer.

---

## Step 2: Commit Message Generation

### Format

```
type: description

#{issue_number}
```

### type List

| type | Purpose |
|------|---------|
| `feat` | Add new feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `refactor` | Code refactoring |
| `chore` | Package manager updates, misc |
| `design` | UI design changes |
| `comment` | Add or modify comments |
| `remove` | File deletion only |

### type Auto-recommendation

- New component/page → `feat`
- Bug keyword → `fix`
- Only .md changed → `docs`
- Import/variable name cleanup → `refactor`
- package.json/config → `chore`
- Only .css/.module.css → `design`
- Deletion only → `remove`

### Issue Number

1. Extract from branch name: `feat/12-login-page` → `#12`
2. If failed, ask user (can be omitted)

### Confirmation

```
Commit message:
  feat: implement login form layout

  #12

Proceed? (Y / edit)
```

---

## Step 3: staging + commit + push

```bash
git add {files}
git commit -m "type: description" -m "#{issue}"
git push  # (or git push -u origin {branch})
```

Skip push with `--no-push` option

---

## Step 4: Completion Report

```
Commit complete
- {hash} | feat: implement login form layout
- Branch: feat/12-login-page
- push: ✅
```

After the report, ask:

```
What would you like to do next?
  [1] Create a PR — /swyp-pr
  [2] Continue working — stay on branch
  [3] Done
```

(plain text — wait for the user to type a response)

---

## Safety Guards

| Rule | Action |
|------|--------|
| Direct commit to main | Block |
| .env/secret files | Block + guide to .gitignore |
| Nothing staged | Suggest adding all |
| amend | Only on explicit request |
| force push | Strictly forbidden |
| Missing issue number | Warn (allow) |
| 10+ files changed | Suggest split |
| AI infra paths in diff | Strip `Co-Authored-By:` — see §8.1 |

### §8.1 AI Co-authorship Strip Rule

If **any** staged file matches the following paths, **omit `Co-Authored-By:` from the commit message entirely**:

```
_wood/
.claude/
.swyp/
AGENTS.md
CLAUDE.md
.github/copilot-instructions.md
```

Detection:
```bash
git diff --cached --name-only | grep -E '^(_wood|\.claude|\.swyp|AGENTS\.md|CLAUDE\.md|\.github/copilot-instructions\.md)'
```

If matched → commit **without** `Co-Authored-By:` trailer, regardless of other files in the same commit.
