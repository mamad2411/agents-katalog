---
name: git-commit-convention
description: Write a one-line gitmoji commit message for staged changes, and execute the commit if requested. Use this skill whenever the user wants a commit message or asks to commit — in English or Korean. Trigger on phrases like "commit this", "write a commit", "suggest a commit message", "커밋 메시지 써줘", "커밋 해줘", "이거 커밋해줘", "커밋 메시지 만들어줘", "변경사항 커밋".
---

Write a gitmoji commit message for the staged changes. Commit messages are always in English.

## Steps

0. **Check prerequisites:** run `git rev-parse --git-dir 2>/dev/null` — if this fails (no output), tell the user this skill must be run inside a git repository and stop.

1. Run `git diff --staged` to see what is staged.
   - If nothing is staged, run `git status --porcelain` to check for any unstaged or untracked changes.
     - If changes exist, stage only tracked changes (modifications and deletions, no untracked): `git add -u`. Do NOT auto-stage untracked files unless the user explicitly asks.
     - Then re-run `git diff --staged` to confirm what is staged.
     - If nothing at all, tell the user there is nothing to commit and stop.
2. Check whether the staged changes are semantically cohesive — do they belong in one commit?
   - If the changes span **unrelated concerns**, split them. See the splitting guide below.
   - If the changes are cohesive (e.g. a feature and its direct test consequences), write one message.
3. Pick one gitmoji that best represents the primary intent.
4. Write a concise one-line description in English.
5. Decide what to do based on the user's intent:
   - **Message only** (e.g., "커밋 메시지 써줘", "what commit message should I use") → output the message(s) and stop.
   - **Actually commit** (e.g., "커밋해줘", "commit this", "commit and push", "커밋하고 푸시해줘"):
     1. Check the current branch: `git rev-parse --abbrev-ref HEAD`
     2. If on `main` or `master`: do NOT commit directly. Instead, suggest creating a feature branch first (use the `git-branch-convention` skill to propose a name, or derive one yourself if unavailable, e.g. `feature/describe-the-change`) and ask the user to confirm before proceeding.
     3. If on a feature branch: run `git commit -m "<message>"`, then if the user said "push", run `git push`.
   - When in doubt, output the message and ask whether to run the commit.

## Format

```
<gitmoji> short description of the change
```

Use the actual unicode emoji character (e.g. `✨`), not the colon code (e.g. ~~`:sparkles:`~~).

Keep the full line under 72 characters.

## Splitting commits

Commits should be small but meaningful. The right unit is a **coherent change** — everything that belongs together conceptually. A few examples:

| What changed | How to split |
|---|---|
| New feature + its tests | One commit — tests are a direct consequence |
| Domain model change + DB migration | One commit — tightly coupled |
| Domain change + unrelated refactor in another module | Two commits |
| Business logic change + test for that logic + unrelated test fix | Two commits — group business logic with its tests, separate the unrelated fix |
| New API endpoint + documentation update | One commit |

When you decide to split, output multiple commit messages, one per line, in the order they should be committed:

```
✨ add User domain model
🔧 add users table migration
✅ add unit tests for User domain
```

The user will then stage and commit each group separately.

## Examples

**Example 1 — new feature with tests:**
Diff shows: new `OrderService.kt`, new `OrderServiceTest.kt`
Output: `✨ add order service with validation logic`

**Example 2 — bug fix:**
Diff shows: off-by-one fix in `PaginationHelper.kt`
Output: `🐛 fix off-by-one error in pagination offset`

**Example 3 — mixed unrelated changes:**
Diff shows: new `PaymentService.kt`, unrelated fix in `UserRepository.kt`
Output:
```
✨ add payment service
🐛 fix user repository query
```

## Gitmoji reference

| Emoji | Use when |
|-------|----------|
| ✨ | New feature |
| 🐛 | Bug fix |
| 🔥 | Remove code or files |
| ♻️ | Refactor |
| 📝 | Documentation |
| 🎨 | Improve structure or format |
| ✅ | Add or update tests |
| 🚀 | Performance improvement |
| 🔧 | Configuration or migration |
| 📦 | Dependency change |
| ⬆️ | Upgrade dependency |
| ⬇️ | Downgrade dependency |
| 🔒 | Security fix |
| 🚑 | Critical hotfix |
| 💄 | UI or style change |
| 🏗️ | Architectural change |
| 🚧 | Work in progress |
| 🩹 | Simple or trivial fix |
| 💡 | Add or update comments |
| 🌐 | Internationalization |
| 🔀 | Merge branches |
| 🏷️ | Add or update types |

## Rules

- One line per commit. No body, no footer, no bullet points.
- Do not add any attribution, signature, watermark, or co-authorship line (no `Co-Authored-By`).
- Do not explain your reasoning. Just output the commit message(s).
