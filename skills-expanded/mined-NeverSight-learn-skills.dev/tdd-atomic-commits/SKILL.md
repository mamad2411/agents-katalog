---
name: tdd-atomic-commits
description: Create atomic Conventional Commits for TDD workflows. Splits a working tree containing both implementation and test changes into two commits per feature — implementation first, then its test — so git history reads like a clean, bisectable TDD story. Use this skill whenever the user asks to commit, says "commit this", "commit the changes", "make the commits", "finalize the commit", or whenever the staged/unstaged diff contains paired source and test files (foo.ts + foo.test.ts, foo.py + test_foo.py, foo.go + foo_test.go, Foo.java + FooTest.java, etc.) — even if the user doesn't explicitly say "atomic" or "conventional commits". Prefer this skill over a plain commit whenever implementation and test files appear together in the diff.
---

# TDD Atomic Commits

## Principle

Commit history should read like the story of the change, not a snapshot of the working tree. For TDD work, each logical feature becomes **two atomic commits**:

1. The implementation commit (`feat` / `fix` / `refactor` / …)
2. The test commit (`test`)

Implementation is committed **first** so that every commit in the history is self-contained: checking out the impl commit gives working code, and checking out the test commit gives working code plus the tests that prove it. The history is bisectable and each commit stands on its own.

This skill runs because the user explicitly asked for a commit. It is not a shell hook.

## Workflow

### Step 1 — Inspect the working tree

Run in parallel:
- `git status` (never `-uall`)
- `git diff` — unstaged changes
- `git diff --staged` — already staged changes
- `git log -n 5 --oneline` — so your subjects match the repo's existing style

Do not trust whatever is already staged. Review *all* changes and decide what belongs in which commit.

### Step 2 — Group changes into logical units

A logical unit is usually **one implementation file plus its test file**. Pair them:

**Primary — by filename convention:**
- TypeScript/JavaScript: `foo.ts` ↔ `foo.test.ts` / `foo.spec.ts` / `__tests__/foo.ts`
- Python: `foo.py` ↔ `test_foo.py` / `tests/test_foo.py` / `foo_test.py`
- Go: `foo.go` ↔ `foo_test.go`
- Ruby: `foo.rb` ↔ `foo_spec.rb` / `spec/foo_spec.rb`
- Java/Kotlin: `Foo.java` ↔ `FooTest.java` under `src/test/…`
- Rust: inline `#[cfg(test)]` belongs with its impl file; files under `tests/` are their own unit

**Secondary — by context.** If filenames don't line up, read the diffs: does the test file import/exercise a symbol the impl file just introduced? Does a single natural subject describe both? Pair them.

If a file plausibly belongs to more than one pair, or you cannot confidently pair it, **stop and ask the user** which grouping they want.

### Step 3 — Determine the commit type per unit

Use Conventional Commits types: `feat`, `fix`, `refactor`, `perf`, `docs`, `style`, `chore`, `build`, `ci`. Reserve `test` for the test half of a pair (or for commits that only touch tests).

Derive the scope from the module, feature, or domain concept — usually the directory name or the component being changed.

### Step 4 — Commit the implementation first, then the test

For each pair:

1. Stage **only** the implementation file by explicit path, then commit:
   ```
   <type>(<scope>): <imperative subject>
   ```
2. Stage **only** the test file by explicit path, then commit:
   ```
   test(<scope>): <what the tests now cover>
   ```

The test-commit subject is a loose guideline — e.g. "ensure token expiry rejects skewed clocks", "cover session lookup edge cases", "add regression test for null user id". Match the repo's existing `git log` style first; fall back to a short, specific description of what the tests now verify.

**Stage by explicit filename.** Never use `git add -A`, `git add .`, or `git add -u` — they sweep up unrelated files and break the atomic split. Always pass explicit paths to `git add`.

### Step 5 — Handle unpaired files

- **Only the test file changed** → one commit: `test(<scope>): <subject>`.
- **Only the implementation file changed** → tell the user:
  > "`path/to/file` has no corresponding test changes. Continue with the commit anyway?"
  If yes, commit with the appropriate type (`feat` / `fix` / `refactor` / …). If no, stop and let the user decide.
- **Unrelated files** (configs, docs, unrelated source) → ask the user whether to include, leave, or commit them separately with their own conventional type. Do not silently lump them in.

### Step 6 — Verify

After committing, run `git status` and `git log -n <commits_created> --oneline` and show the result to the user so they can confirm the history looks right and the working tree is clean.

## Fix workflow

For `fix` changes the impl-first rule still holds: commit the implementation fix first, then — **if the test had to change** to catch the regression or reflect the corrected behavior — commit the updated test as `test(<scope>): <subject>`. If the existing test was already adequate and nothing in the test file changed, a single `fix` commit is correct — do not invent a test commit.

## Complex cases — ask the user

When in doubt, ask. Good examples:
- Multiple features mixed in one working tree and it's unclear which files belong together
- One impl file that touches behavior exercised by two different test files (or vice versa)
- Renames/moves that git has recorded as add+delete
- Generated files, lockfiles, migrations, or snapshots that aren't obviously impl or test

A short clarifying question is cheaper than a wrong commit.

## Things to avoid

- Do **not** use `git add -A`, `git add .`, or `git add -u`. Stage by explicit path.
- Do **not** amend earlier commits unless the user explicitly asks. Always create new commits.
- Do **not** pass `--no-verify` to skip hooks. If a hook fails, investigate the root cause.
- Do **not** invert the order (test before impl). The whole point is that every commit is independently runnable, which requires impl-first.
- Do **not** bundle multiple logical units into one commit even when they share a scope. One feature → one pair.

## Example

Working tree:
```
modified:   src/auth/token.ts
modified:   src/auth/token.test.ts
modified:   src/auth/session.ts
modified:   src/auth/session.test.ts
```

Resulting history (oldest first):
```
feat(auth): validate token expiry against server clock
test(auth): ensure token expiry rejects skewed clocks
refactor(auth): extract session lookup into dedicated helper
test(auth): cover session lookup helper edge cases
```

Two logical units → four commits, each pair impl-first.
