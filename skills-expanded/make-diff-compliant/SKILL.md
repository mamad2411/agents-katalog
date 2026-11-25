---
name: make-diff-compliant
description: Use to bring exactly the source files a PR/branch touches up to the deterministic-refactor compliance conditions (typed, overrides marked, typed test doubles), so a future refactor over them is verifiable. Scoped to the diff — grows compliance monotonically, no repo-wide migration.
---

**Preflight:** run `la-doctor --plugin <this skill's base directory>` once per session before using any `la-*` or `dr-*` command; if it fails, stop and show the user its output.

# Make the diff compliant

Raise compliance one PR at a time instead of a big-bang migration: every diff
leaves the files it touched fully refactor-verifiable.

## Steps

1. **Changed source files:**
   `git diff --name-only <base>...HEAD` (base = the PR's target branch), kept to
   the repo languages' sources (`la-config get languages`, then
   `la-config get lang.<language>.source_globs`).
2. **Report:** `dr-compliance <changed files>` — each file gets its language's
   checks.
3. **Fix each, within the changed files,** following the compliance fixes in
   `<this skill's base directory>/../../languages/<language>.md`; mark every
   override among the changed methods.
4. **Re-check until clean:**
   - `dr-compliance <changed files>` exits 0;
   - `la-typecheck` shows no new errors;
   - `dr-mock-lint <changed tests>` passes.
5. Run the non-integration test suite (`la-config get commands.test`). Review. The user commits.

Never weaken existing annotations. Keep edits within the diff's files unless a
fix requires annotating an immediate caller.
