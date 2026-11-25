---
name: harness-update
description: Updates the vendored copy of the Belayline harness in this repository to a given tag (or the latest), in a draft PR, without overwriting what belongs to the project. Use when the operator asks to move to a new version of the harness.
argument-hint: "[vX.Y.Z]"
---

# Update the harness

Target version: $ARGUMENTS (empty = latest `vX.Y.Z` tag of `francoisgn/belayline-agentic-harness`).

1. Current version: `.harness/VERSION`. Latest tag: `git ls-remote --tags --refs https://github.com/francoisgn/belayline-agentic-harness.git 'v*'`
   (in a cloud session, the harness repository must be attached to the session). Read the harness's `CHANGELOG.md`
   between the two.
2. Branch from the up-to-date integration branch: `git switch -c chore/harness-<tag> origin/<integration>`.
3. Fetch the harness at the tag into a throwaway folder (`git clone --depth 1 --branch <tag> … "$TMPDIR/belayline"`),
   then `"$TMPDIR/belayline/scripts/harness-sync.sh" --target . --dry-run`, and without `--dry-run` if the
   result is as expected.
4. Exit code 3 (conflicts): a harness file was modified in the project. **Do not force** without approval: show the
   diff to the operator and propose either moving the change into the harness (PR on Belayline), or moving it
   out of the harness, or `--force`.
5. Reread the whole `git diff` (LESSONS L17); check that `harness-sync.sh --check` exits 0; the `@vX.Y.Z` references
   in `.github/workflows/harness.yml` follow.
6. One commit `Belayline: update to <tag>`, one push, a draft PR (`Refs #n` of the update issue, or
   `Direct-PR: harness update`; no `### Ledger`: nothing visible to the user), with, in the body, the items of the
   harness CHANGELOG that require an action in the project ("Action" lines).
