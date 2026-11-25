---
name: hotfix
description: "Hotfix or patch a released version from main with a regression test, gates and owner approval. Use for hotfix, patch release, urgent fix to a release."
---

# hotfix

1. Check git flow is set up: `git flow version` and `git config --get gitflow.branch.develop`. If git flow is missing, stop and tell the owner to install it with `brew install git-flow`; never hand-roll it. If uninitialized, run the init commands in [Maintaining the kit](../../../docs/maintaining.md#release).
2. Check `git status --porcelain`, fetch origin, and compare the starting branch with its origin ref. Stop on a dirty tree or a branch behind/diverged from origin; never stash or reset the owner's work. Require the starting branch to be up to date before proceeding.
3. Switch to synchronized `main`; determine X.Y.(Z+1) from the current released version. Stop if that tag already exists. Run `git flow hotfix start X.Y.(Z+1)`.
4. Make the fix with a regression test, bump only the source plugin manifest version, run `node scripts/build-harness.mjs`, and add the matching version section in `CHANGELOG.md`. Stop if the changelog section is missing. Follow [Release](../../../docs/maintaining.md#release).
5. Run `run-gates`, review and commit the fix, then run `run-gates` again on that exact clean head. Stop for the owner's explicit go-ahead before finishing or publishing.
6. With that go-ahead, run `git flow hotfix finish -m vX.Y.Z X.Y.Z` using the chosen patch version; push `main`, `develop` and the tag. Check `gh release view vX.Y.Z` before manual release creation; distinguish not-found from other errors. If the workflow cannot run and the release is confirmed absent, create it from the matching changelog section as described in [Release](../../../docs/maintaining.md#release).
7. Follow the same Gemini export, leak check and publishing steps there. Never copy `.leakcheck.local` into a committed file. Report gate evidence and the release URL.

Tagging, pushing `main`/tags, creating a release and publishing the `gemini` branch need the owner's explicit go-ahead in that session. Stop before each unless that session's explicit go-ahead covers it.
