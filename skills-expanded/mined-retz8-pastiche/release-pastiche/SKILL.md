---
name: release-pastiche
description: Ship a pastiche release — version bump, plugin build, CHANGELOG entry, release commit, tag, GitHub Release, milestone close. Use when the user invokes `/release-pastiche` after a TODO group's final feat→main merge. Human-triggered only; never run from an automated routine.
---

# release-pastiche

Run on `main`, clean working tree, after every task of the group has merged.

## Workflow

1. **Determine the version.** Default: the completed group's minor from `_dev/TODO.md` (provisional — confirm with the user; hotfix releases are a patch bump instead).
2. **Bump** `version` in `package.json`.
3. **Build:** `npm run build` — verify `dist/claude-code/` regenerated and its `plugin.json` carries the new version.
4. **CHANGELOG entry.** Move `[Unreleased]` content (if any) and derive the rest from commits since the last release tag: `feat(...)` → *Added*, `fix(...)` → *Fixed*, breaking/behavior changes → *Changed*. Section header: `## [<version>] - <today>`. Fresh empty `[Unreleased]` on top.
5. **Commit** everything as one commit: `chore(release): v<version>`.
6. **Tag** `v<version>` and push branch + tag.
7. **GitHub Release:** `gh release create v<version>` with the new CHANGELOG section as body.
8. **Close the milestone** for the shipped group.
9. **Tick TODO.md**: confirm all the group's task checkboxes are ticked and parent issues closed; flag any that aren't.
