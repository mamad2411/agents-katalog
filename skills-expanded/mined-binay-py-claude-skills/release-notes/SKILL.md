---
name: release-notes
description: Draft release notes and a Keep-a-Changelog CHANGELOG.md section from git history — last tag..HEAD by default, grouped into Breaking/Added/Changed/Fixed/Removed/Security/Docs from Conventional Commits or, for free-form messages, from the first word ("Add", "Fix", "Remove"…); skips merges, wip, fixup! and version-bump commits, merges duplicate subjects, links PR/MR numbers and commit SHAs for GitHub and GitLab remotes, lists authors and Co-authored-by contributors, and suggests the next semver bump. Use when cutting a release, writing a GitHub release body, or starting or updating a CHANGELOG.
---

# release-notes

`scripts/release-notes.mjs` is zero-dependency Node 22+. It only reads git, except with `--write`. It never creates tags, commits or pushes.

```
node release-notes.mjs                                  # last tag..HEAD, printed
node release-notes.mjs --version 1.4.0                  # header ## [1.4.0] - today (default: ## [Unreleased])
node release-notes.mjs --from v1.2.0 --to v1.3.0
node release-notes.mjs --format github --version 1.4.0  # GitHub release body + "Full Changelog" compare link
node release-notes.mjs --version 1.4.0 --changelog CHANGELOG.md --write
node release-notes.mjs --cwd path/to/repo --repo-url none
```

The notes go to stdout; a summary goes to stderr: range, kept/skipped counts, commit style detected, link base, groups, and the **suggested bump** (major if anything is breaking, minor if anything was added, else patch, computed from the last semver tag).

## What it does
- **Range:** the latest tag reachable from `--to` up to `--to`. If `--to` is itself tagged, it describes that tag (previous tag..tag) and uses its version. No tags: the whole history, and it says so.
- **Grouping:** `feat` → Added, `fix` → Fixed, `perf` → Performance, `refactor` → Changed, `docs`, `test`, `build`/`ci`, `chore`. `type!:` or a `BREAKING CHANGE:` footer → Breaking, with the footer text under the bullet. Free-form subjects are grouped by their first word (Add/New → Added, Fix → Fixed, Remove/Delete/Drop → Removed, Update/Improve/Refactor/Rename → Changed, Docs/README → Docs); anything else lands in Changed. A leading `area: ` becomes a bold scope.
- **Skipped:** merge commits, `wip`, `fixup!`/`squash!`, "Initial commit", and subjects that are only a version (`v1.0.1`, `Bump version to 1.0.0`, `chore(release): 1.2.1`). Identical subjects are listed once.
- **Links:** from `git remote get-url origin` (https, ssh and `git@host:` forms; credentials in the URL are dropped). GitHub: `#12` → `/pull/12`. GitLab: `!7` → merge request, `#7` → issue. Other hosts get plain text.
- **`--write`:** inserts the section into the changelog below `[Unreleased]` and above the newest version, creating the file with the standard Keep-a-Changelog header if missing. It refuses if that version is already present (so re-running is a no-op), regenerates an existing `[Unreleased]` section in place, and saves `CHANGELOG.md.bak` before changing anything.

## How Claude should use it
1. Run it without `--write` and read the summary. Confirm the range and the version with the user; offer the suggested bump.
2. **Rewrite the bullets for users.** The output is commit subjects, which describe what the developer did. Turn them into what changed for the person using the project: merge related commits into one bullet, drop internal noise (refactors, CI, tests, typo fixes) unless it affects users, explain breaking changes with what to do about them, and keep the PR/commit links. Don't invent changes that aren't in the commits.
3. Show the rewritten section. Only after the user agrees, write it: run with `--write` to create the section, then edit the bullets in the file (or paste the rewritten text directly).
4. Tagging and publishing are the user's call. Give them the commands (`git tag v1.4.0 && git push origin v1.4.0`, `gh release create v1.4.0 --notes-file …`); don't run them.

## Limits
- It sees commit messages only. Squash-merged PRs show their squash subject; a PR merged with a merge commit shows its individual commits, and the merge commit (with the PR number) is skipped, so those bullets have no PR link.
- First-word grouping is a guess. "Make X faster" goes to Changed, "Handle Y" to Fixed. That is why step 2 exists.
- Contributors are git author names, not GitHub usernames, so there are no `@mentions`.
- Release date is today (override with `--date YYYY-MM-DD`). No compare-link references are added at the bottom of CHANGELOG.md.
