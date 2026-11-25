---
name: conventional-commits
description: Writes git commit messages following the Conventional Commits 1.0.0 spec. Use when committing changes, when the user asks for a commit message, or when a repo enforces commit linting.
---

# Conventional Commits

When creating a commit message, follow Conventional Commits 1.0.0.

## When to use this skill

- The user asks to commit staged or unstaged changes.
- The user asks "write a commit message for this diff".
- The repo has `commitlint`, `husky`, or a `CONTRIBUTING.md` mentioning Conventional Commits.

## How to use it

1. Inspect the change first: `git diff --staged` (or `git diff` if nothing is staged). Never invent a message without reading the diff.
2. Pick the **type** from the actual change, not the file names:
   - `feat` — user-visible behavior added
   - `fix` — user-visible bug fixed
   - `refactor` — behavior-preserving restructure
   - `docs`, `test`, `build`, `ci`, `chore`, `style`, `perf`
3. Add a **scope** when the repo already uses them (check `git log --oneline -20` for the house style).
4. Subject line: imperative mood, lowercase after the colon, no trailing period, ≤ 72 chars.
5. Body (optional): explain *why*, wrap at 72. Footer: `BREAKING CHANGE:` or issue refs (`Closes #123`).

## Decision tree

- Mixed unrelated changes in one diff → propose splitting into multiple commits instead of one vague `chore`.
- Change is a revert → use `revert:` and reference the reverted SHA.
- Unsure between `fix` and `refactor` → does an end user observe the difference? Yes = `fix`, no = `refactor`.

## Done means

`git log -1 --format=%s` matches `^(feat|fix|refactor|docs|test|build|ci|chore|style|perf|revert)(\(.+\))?!?: .+` and the message honestly describes the diff.

---

Part of [awesome-antigravity-skills](https://github.com/LichAmnesia/awesome-antigravity-skills). Browse more Agent Skills at [orangebot.ai/skills](https://orangebot.ai/skills).
