---
name: git-auto-commit
description: Analyze real Git working-tree changes, learn the repository's commit style, generate detailed bilingual Chinese-English conventional commit messages with a body, and create safe local commits. Use when the user asks an agent to commit, auto commit, save changes to git, create a commit, generate a commit message, run a dry commit review, or explicitly invokes git-auto-commit.
---

# Git Auto Commit

Create a local Git commit only after inspecting the actual diff, repository history, and safety risks. Prefer the repository's existing commit style; when it is unclear, use detailed bilingual Chinese-English conventional commits with a subject plus body.

This skill is agent-neutral. Use it from Codex, Claude Code, Cursor, OpenCode, Gemini CLI, or any other coding agent that can read this `SKILL.md` file and run local shell commands.

## Quick Workflow

1. Verify the current directory is a Git repository.
2. Locate the skill directory. If this file is loaded from disk, use its parent directory as `SKILL_DIR`; otherwise ask the user for the installed `git-auto-commit` skill path.
3. Run the read-only snapshot helper:

```bash
export SKILL_DIR="/path/to/git-auto-commit"
python3 "$SKILL_DIR/scripts/git_commit_snapshot.py"
```

The snapshot JSON includes `has_conflicts`, `conflicted_paths`, `merge_in_progress`, `rebase_in_progress`, and separate `staged_*` / `unstaged_*` line counts. If `has_conflicts` is `true`, skip to [Merge Conflicts](#merge-conflicts) below.

4. Inspect the files that matter:
   - `git status --short`
   - `git diff --stat`
   - `git diff`
   - `git diff --cached` when staged changes exist
   - `git log --oneline -20`
5. Determine whether the change is one coherent commit.
6. Choose the commit type and scope from repository history and changed paths.
7. Stage only the intended files.
8. Commit locally with the selected message.
9. Report the commit hash, message, and any files intentionally left uncommitted.

Never push unless the user explicitly asks for push.

## Modes

- Normal: analyze, stage intended files, and create one local commit.
- Dry run: when the user says dry, dry-run, preview, only message, or only generate, do not stage or commit; return the recommended message and reasoning.
- Push: only push after a successful commit when the user explicitly asks for push.

## Safety Rules

Stop and ask before committing when any of these are true:

- Secret-like files or names are present: `.env`, `.envrc`, `.key`, `.pem`, `.p12`, `.pfx`, `.keystore`, `.jks`, `.kdbx`, `.ovpn`, `.netrc`, `.htpasswd`, `.htaccess`, `.npmrc`, `.pypirc`, credentials, token, password, api_key, secret, private_key, SSH private keys (`id_rsa`, `id_dsa`, `id_ecdsa`, `id_ed25519`).
- Unresolved merge conflicts are present (snapshot `has_conflicts` is `true`).
- The intent is unclear or multiple unrelated changes are mixed together.
- The diff is large, roughly more than 50 files or 1000 changed lines.
- The change appears destructive, such as broad deletion, migration, public API break, schema change, or major dependency upgrade.
- The user has unstaged and staged changes that appear to represent different intents.

Ignore dependency folders, generated build output, caches, and binary artifacts unless the repository clearly tracks them intentionally.

## Message Rules

Always read `$SKILL_DIR/references/commit-style.md` before writing the message. Prefer a **detailed** message: subject + body bullets that capture what changed and why, grounded in the real diff.

Default format:

```text
type(scope): 中英文混排描述

- 关键改动点 1（含关键符号/API 名）
- 关键改动点 2
- 行为影响或边界情况（如有）
```

Write the subject in natural mixed Chinese-English: Chinese for the description, English for technical terms, API names, and keywords. No need for a separate English translation.

Subject examples:

```text
feat(auth): 增加 OAuth2 登录支持
fix(player): 修复 video 播放时序竞态问题
refactor(network): 重构 HTTP interceptor 层
```

Body requirements (default — detailed):

- **Default: always include a body** with 2–8 short bullets summarizing the real diff.
- Cover: new/changed APIs or methods, behavior changes, refactors of key logic, important constraints or edge cases.
- Prefer concrete names from the diff (`onPanUpdate`, `multiType=3`, `FishUtil.isBossFishLevel`) over vague wording.
- Group related bullets; do not dump every touched filename.
- Only use subject-only for trivial one-liners (typo, comment-only, pure formatting, single-line config tweak) when the subject already says everything.
- Breaking changes: lead body with `BREAKING CHANGE: ...` then bullets.

Do not add AI attribution trailers such as:

```text
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Execution Rules

- Analyze real diffs; never infer the message from filenames alone.
- Respect existing repository commit language, length, emoji usage, and scopes.
- Keep unrelated working-tree changes untouched.
- Prefer staging explicit paths over `git add .` when unrelated changes are present.
- Do not add `Co-Authored-By` or other AI attribution trailers unless the user explicitly asks for them.
- Do not create tests, summaries, or formatting changes unless the user explicitly asked for them.
- Do not amend, reset, rebase, or discard work unless the user explicitly asked for that exact operation.

## Merge Conflicts

When the working tree or index contains unresolved merge conflicts, **do not attempt to resolve them automatically**.

The snapshot helper already reports `has_conflicts`, `conflicted_paths`, `merge_in_progress`, and `rebase_in_progress`. Check these fields first; the commands below are for manual verification.

Detection:

- Run `git status` and look for `Unmerged paths` or status codes `DD`, `AU`, `UD`, `UA`, `DU`, `AA`, `UU`.
- Run `git diff --name-only --diff-filter=U` to list conflicted files.
- Check for in-progress merge or rebase: `test -f .git/MERGE_HEAD` or `test -d .git/rebase-merge`.

Action:

1. Report the list of conflicted files to the user.
2. Ask the user to resolve conflicts manually (edit, `git add`, or `git rm <file>`).
3. Do not stage, commit, or push until all conflicts are resolved and the user confirms.
4. If a merge or rebase is in progress, inform the user and ask whether to continue, abort, or pause.

Never run `git commit` while conflicted files remain, even if the user asks to "just commit everything". Explain the conflict situation and wait for explicit resolution.

## Slash Command Prompt

For agents that support slash commands, create `/git-auto-commit` with the prompt in `commands/git-auto-commit.md`. The slash command should invoke this skill, then follow the same safety rules and execution workflow.
