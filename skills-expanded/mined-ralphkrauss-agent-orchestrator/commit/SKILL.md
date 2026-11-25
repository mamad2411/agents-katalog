---
name: commit
description: Session-scoped commit of uncommitted changes. Stages relevant files, drafts a commit message from the diff, and commits immediately unless the request is genuinely ambiguous. Push is a separate action and only happens when the user explicitly asks, such as "commit and push". Use when user says "commit", "commit this", "commit changes", or "commit and push".
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Commit (Session-Scoped)

Commit uncommitted working tree changes from the current session. Stage only relevant files, draft a concise commit message from the diff, and commit without asking for a second confirmation when the user has already asked to commit. Push is separate and only happens on an explicit request.

Read `AGENTS.md` first for repository-wide git safety rules.

## Instructions

### Step 1: Assess Changes

```bash
git status
git diff --stat
git diff HEAD --stat
```

If no changes: report "Nothing to commit" and stop.

### Step 2: Stage Files

1. Review modified, staged, and untracked files that appear related to the current request.
   - Durable workflow artifacts in `plans/{branch-name}/` are related when they were produced or updated by the current work. Include resolution maps, implementation plans, test plans/results, and review artifacts when the user asks to commit/push that work unless explicitly excluded.
2. Skip files that are clearly unrelated:
   - `package-lock.json` unless the user explicitly changed packages
   - `.claude/worktrees/` internal files
   - credential files such as `.env`, `auth.json`, and API keys
3. Stage with specific file paths. Never use `git add -A` or `git add .`.
4. Only stop to ask the user if there is a real ambiguity:
   - untracked files might or might not belong in the commit
   - unrelated user changes are mixed into the same file and cannot be safely separated
   - the user requested a commit but there is no sensible scope to commit

If the scope is clear, do not ask for confirmation before committing.

### Step 3: Draft Commit Message

Read the staged diff to understand what changed:

```bash
git diff --cached
```

Draft a commit message:
- Subject line: imperative mood, under 72 chars, describes the why more than the what
- Body if needed: short bullet points for multiple changes
- No Co-Authored-By trailer
- Include the issue number if the current branch starts with a number, such as `#428`

Format:

```
{type}: {subject} (#{issue})

- {change 1}
- {change 2}
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

### Step 4: Commit Immediately

When the user asked to commit, treat that as the authorization to commit.

1. Stage the selected files.
2. Create the commit with the drafted message.
3. Report the commit hash, commit message, and short stat.

Do not pause for a second approval prompt unless the user explicitly asked to review the message first.

### Step 5: Push Only On Explicit Request

Commit and push are separate actions.

1. If the user asked only for `/commit`, stop after the commit.
2. If the user explicitly asked to push as part of the same request, such as "commit and push", push the current branch after the commit succeeds.
3. Do not ask for an extra confirmation before pushing when the request already explicitly included push.
4. If the branch has no upstream yet, push with upstream tracking.

Report whether the action stopped at commit or also pushed to the remote.

## Critical Rules

- No Co-Authored-By trailer. This is the user's commit.
- Session-scoped only. Commit what belongs to the current request and do not amend previous commits.
- Commit means commit. Once the user asks to commit, do it without a second confirmation unless the scope is genuinely ambiguous.
- Push is separate. Never push unless the user explicitly asked for it in the same request.
- Explicit push means push. If the request says "commit and push", do both without asking again.
- Never force-push, amend, or rebase. Create new commits only.
- Never commit secrets. Skip `.env`, credentials, `auth.json`, and API keys.
- Only ask when needed. Ask about untracked files only when it is genuinely unclear whether they belong in the commit.
- Respect hook failures. If pre-commit hooks fail, report the error and let the user decide. Do not retry with `--no-verify`.

## Checklist

- [ ] Reviewed the working tree and confirmed there was something to commit
- [ ] Staged only the files that belong in the commit scope
- [ ] Skipped secrets and clearly unrelated files
- [ ] Drafted a concise commit message from the actual diff
- [ ] Committed immediately when the user asked to commit and the scope was clear
- [ ] Pushed only if the user explicitly asked to push

## Reference

- `AGENTS.md` -- repository-wide git safety rules
