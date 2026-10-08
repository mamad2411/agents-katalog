---
name: cp
description: Commit and push in one step. Use when user says "/cp", "commit and push", "커밋하고 푸시", "커밋 푸시", "변경사항 올려줘", or wants to stage, commit, and push changes in a single action. Optionally accepts a commit message as argument. Not for creating, reviewing, or merging pull requests — commit and push only.
user-invocable: true
---

# Commit & Push Skill

Streamlined git workflow: stage, commit, and push in one command. Does not
create, review, or merge pull requests — for those, use a different skill.

## Usage

### Basic

```bash
/cp                        # Auto-generate commit message
/cp "fix: resolve bug"     # Use provided message
```

### Korean Triggers

- "커밋하고 푸시"
- "커밋 푸시"
- "변경사항 올려줘"

## Workflow

`<current-branch>` anywhere below means the output of `git branch --show-current`.

### 1. Protected Branch Check

```bash
git branch --show-current
```

If the result is `main`, `master`, or otherwise matches the remote's default
branch (`origin/HEAD`), stop and ask the user to confirm before doing
anything else. Do not commit or push to a protected branch without explicit
confirmation.

### 2. Analyze Changes

```bash
git status                 # See all changes
git diff                   # Unstaged changes
git log -5                 # Recent commits — also check trailer conventions (used in step 4)
```

### 3. Stage Files

Prefer specific files over `git add -A`:

```bash
git add src/component.tsx src/utils.ts
```

**Never stage:**
- `.env` files
- Credentials or secrets
- Large binary files (unless intentional)

**Secret scan** — after staging, check what's actually going into the commit:

```bash
git diff --staged | grep -iEn "(api[_-]?key|secret|password|passwd|token)[a-z0-9_-]*[\"']?[[:space:]]*[:=][[:space:]]*[\"']?[a-z0-9_/+.-]{6,}|ghp_[a-z0-9]{20,}|github_pat_[a-z0-9_]{20,}|(^|[^a-z0-9])sk-[a-z0-9-]{16,}|AKIA[0-9A-Z]{16}|xox[baprs]-[a-z0-9-]+|BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY"
```

The pattern matches assignment context (`KEY=value`, `key: value`, JSON pairs) with a 6+ char value, well-known token prefixes (GitHub `ghp_`/`github_pat_`, OpenAI `sk-`, AWS `AKIA`, Slack `xox*`), and private key blocks — prose like "password reset guide" or identifiers like `tokenizer` don't trip it. If this matches anything, stop and confirm with the user before committing.

### 4. Generate Commit Message

Base the message on what's actually staged, not the full working tree:

```bash
git diff --staged
```

Follow Conventional Commits:

| Prefix | Use Case |
|--------|----------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `refactor:` | Code restructuring |
| `style:` | Formatting (no logic change) |
| `test:` | Adding tests |
| `chore:` | Maintenance tasks |

**Trailers**: only add a trailer like `Co-Authored-By: Claude <noreply@anthropic.com>`
if `git log -5` (step 2) shows the repo already uses that convention on recent
commits. Don't insert it unconditionally.

### 5. Commit

Use HEREDOC for proper formatting:

```bash
git commit -m "$(cat <<'EOF'
type: concise description

Optional body with more details.
EOF
)"
```

Include the `Co-Authored-By` trailer (or any other trailer) only per the
convention check in step 4.

### 6. Push

```bash
git push origin <current-branch>
```

If upstream not set:

```bash
git push -u origin <current-branch>
```

If this is rejected, see **Push Rejected Recovery** below.

## Push Rejected Recovery

If `git push` is rejected (non-fast-forward), never run a bare `git pull` —
it can silently create a merge commit or, on a rebase-configured branch,
rewrite history in a way that's hard to walk back. Instead:

1. `git fetch`
2. Check the situation:
   ```bash
   git status -sb
   git log HEAD..@{u} --oneline   # commits on the remote you don't have
   git log @{u}..HEAD --oneline   # commits you have that the remote doesn't
   ```
3. **Fast-forward possible** (only behind, no local-only commits — `git status -sb`
   shows `behind N` with no `ahead`): run `git pull --ff-only`, then retry the push.
4. **Diverged** (`git status -sb` shows both `ahead` and `behind`, both log
   commands above are non-empty): do not merge or rebase automatically.
   Report the situation to the user — ahead/behind counts and the commits on
   each side — and wait for instructions.

## Error Handling

| Error | Solution |
|-------|----------|
| "Nothing to commit" | No changes detected, inform user |
| "Push rejected" | Follow **Push Rejected Recovery** above — never bare `git pull` |
| "Pre-commit hook failed" | Fix issues, stage again, create NEW commit |
