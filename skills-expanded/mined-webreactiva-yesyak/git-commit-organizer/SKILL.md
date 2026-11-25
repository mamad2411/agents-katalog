---
name: git-commit-organizer
description: Convention for branches and commits. It covers a feature branch named at the start of the work, a slug derived from it and reused in every document, and small atomic Conventional Commits with gitmoji that each include their tests, docs and decision records. Use it whenever you create a branch, commit, split work into commits, prepare history for a pull request, or name feature documents, and whenever the user mentions commits, branches, gitmoji, atomic commits or "commit this". Apply it even when the user only says "go ahead and implement".
---

# Git commit organizer

## Branch and slug

The work starts on a named branch. Ask the user for the branch name if they did not give one. Suggest `feat/<slug>` for a feature and `fix/<slug>` for a bug (`bug-intake`), with a short kebab-case slug.

The **slug** is the part after the prefix. For example, the slug of `feat/order-cancel` is `order-cancel`. Reuse it everywhere so all artifacts of one piece of work are easy to find:

| Artifact | Path |
| --- | --- |
| Spec and plan (features) | `docs/<slug>-spec.md`, `docs/<slug>-plan.md` |
| Bug report (bugs) | `.scratchpad/<slug>/bug-report.md` |
| Working files | `.scratchpad/<slug>/` |
| Work items | label or tag `<slug>` |

Create the branch before the first change. Never commit feature work on the default branch. One piece of work has one branch. The steps of a plan and the fixes of a change list are commits on it, not branches of their own.

Sometimes the environment or the user fixes a branch name that says nothing about the feature (for example a name that a cloud session assigns). Do not rename it and do not create a second branch. Choose a descriptive slug for the feature, write `Branch` and `Slug` as two separate rows in `progress.md`, and use that slug for every artifact. Documents that show a branch name show the real branch.

## Commit rules

1. **Atomic.** One commit does one thing: one feature step, one fix, one refactor. Commit each piece as soon as it passes the project's full check. Do not collect changes and split them later. Work gets lost when you split changes afterwards with stashes and restores.
2. **Refactor separate from behavior.** If a feature needs a refactor, commit the refactor first, with all tests passing and no behavior change.
3. **Complete.** A commit includes its tests, the docs it affects (README, AGENTS.md, spec, plan) and its ADR if it contains a decision.
4. **Green.** Run the project's full check (for example `npm test`) before every commit, and read its own exit code. A pipe to another command (for example `| tail`) returns the exit code of the last command. Do not commit with failing tests.

## Message format

Conventional Commits with gitmoji, in the document language of `simplified-technical-language`:

```text
<type>(<scope>): <gitmoji> <summary in the imperative, lowercase, no period>

Optional body: why the change was needed, in one short paragraph.

<attribution trailers required by the environment>
```

| Type | Gitmoji | Use |
| --- | --- | --- |
| feat | ✨ | New behavior |
| fix | 🐛 | Bug fix |
| fix | 🔒️ | Security fix |
| refactor | ♻️ | Structure change without behavior change |
| test | ✅ | Tests only |
| docs | 📝 | Documentation only |
| chore | 🔧 🙈 | Config, tooling, ignore files |
| style | 💄 | UI and CSS |
| feat | 🔊 | Logging |
| perf | ⚡️ | Performance |
| fix, feat | ♿️ | Accessibility |

Follow the repository's own convention if AGENTS.md or recent history shows a different one.

## Safety

- Never push, open a pull request, force-push, rebase shared history or delete branches unless the user asks for it.
- Never open a file for writing before you have read it, in the shell (`>`) or in a script. One failed command can empty a file that git does not track yet.
- After a script edits many files (renames, renumbering, merges), read `git diff --cached --stat` before the commit. A file that loses all its lines is a bug in the script, for example a file opened for writing before it was read.
- To read a committed version of a file, use `git show HEAD:<path>`, not `git stash`. If you must stash, add `--include-untracked` when new files matter, and check `git status` and `git stash list` afterwards.
- Before you finish, run `git status --short` and explain any file that is not committed.
