---
name: changelog-release-notes
description: Turn raw commit history into two artifacts — an internal changelog (complete, technical) and user-facing "What's New" notes (benefit-first, jargon-free). Use when the user says "write release notes", "what's new for this version", "changelog since last release", "announce the update", or is tagging/shipping a version. Don't use for writing project setup docs — use docs-readme-writer.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Builder Dev, Releases, Changelog, Communication]
    related_skills: [git-ship-flow, docs-readme-writer, github-pr-review, vercel-deploy-check]
---

# Changelog & Release Notes

One git history, two audiences, two documents. The **internal changelog** is complete and technical — every meaningful change, with shas, for the team debugging next month. The **"What's New"** is short and benefit-first — only what users can see or feel, written as outcomes ("Search is 3x faster"), never as commits ("refactored search indexing"). Mixing the two produces notes nobody reads.

## When to Use

- Cutting a release/tag and needing notes for it.
- User wants "what changed since <version/date>" for the team or for users.
- Writing the app's What's New screen, launch tweet source material, or CHANGELOG.md entry.
- **Not for:** how-to-run documentation — use `docs-readme-writer`. Not for making the release commits themselves — use `git-ship-flow`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Find the last release tag | `git describe --tags --abbrev=0` (none? use a date: `--since="2026-07-01"`) |
| Commits since then | `git log <tag>..HEAD --oneline --no-merges` |
| Commits with body + files | `git log <tag>..HEAD --no-merges --pretty=format:"%h %s%n%b" --stat` |
| Merged PR titles (richer) | `gh pr list --state merged --search "merged:><date>" --json number,title` |
| Group by area | `git log <tag>..HEAD --oneline --no-merges -- app/ api/ supabase/` (repeat per path) |
| Tag the release | `git tag -a v1.4.0 -m "v1.4.0" && git push origin v1.4.0` (gate behind confirm) |

## Procedure

1. **Precheck** — `git fetch --tags`; find the last tag (or agree a since-date with the user). Confirm the version number for this release and where each artifact goes (CHANGELOG.md, GitHub Release, in-app What's New, email).
2. **Collect** — pull the commit list with bodies. PR titles via `gh` are usually better-written than raw commits — prefer them when available. Success: a raw list you could defend as "everything since <tag>".
3. **Classify every commit** — Added / Changed / Fixed / Security / Internal (refactors, deps, CI). Then mark each: **user-visible?** The test: would a non-developer notice this in the app? Cryptic commits (`wip`, `fix stuff`) → read the diff (`git show <sha> --stat`) or ask; never guess a change's meaning from a vague message.
4. **Internal changelog** — every non-noise commit, grouped by category, each line `change — <sha>`. Complete beats pretty. Append to `CHANGELOG.md` under a `## [v1.4.0] - <date>` heading (Keep-a-Changelog shape).
5. **What's New** — user-visible items only, max ~5, ordered by user impact, each rewritten commit→benefit: "add debounce to search input" → "Search results now appear as you type." Bug fixes users noticed get owned plainly ("Fixed: exports no longer fail on large projects"); silent-fix items users never saw can stay internal. Security fixes: say an issue was fixed; don't publish the exploit recipe.
6. **Confirm before publishing** — What's New copy and tags are public. Show both artifacts; on explicit yes: append CHANGELOG.md, tag (`git tag -a`), and optionally `gh release create v1.4.0 --notes-file notes.md`.

## Output Template

```markdown
<!-- CHANGELOG.md (internal) -->
## [v1.4.0] - 2026-07-24
### Added
- CSV export on projects dashboard — a1b2c3d
### Changed
- Search input debounced 300ms — d4e5f6a
### Fixed
- Export crash on >1k rows — b7c8d9e
### Security
- Rate limiting on /api/auth — e0f1a2b
### Internal
- Bumped Next 15.2 → 15.4 — c3d4e5f

<!-- What's New (user-facing) -->
# What's New in <App> — July 24
**Export your projects to CSV** — one click from the dashboard.
**Faster, smoother search** — results appear as you type.
**Fixed** — large exports no longer fail partway through.
```

## Pitfalls

- **Commit-messages-as-release-notes** — "refactor useAuth hook" means nothing to a user and clutters What's New. Recovery: apply the would-a-non-dev-notice test to every line; internal-only items live in the changelog, benefits live in What's New.
- **Missing changes because merge commits hid them** — squash-merged PRs vs merge commits change what `git log` shows. Recovery: cross-check the commit list against `gh pr list --state merged` for the window; the union is the truth.
- **Overpromising in benefit language** — "Search is now instant" when it's debounced. Recovery: every What's New claim must be traceable to a specific sha and honest about scale; when unsure, describe the change, not a superlative.
- **Publishing exploit details in security notes** — "fixed auth bypass via X header" is a how-to for old clients. Recovery: "Fixed a security issue affecting authentication; no action needed" publicly; full detail stays in the internal changelog.
- **Version tagged before artifacts agreed** — tag pushed, then notes change, now the release and docs disagree. Recovery: notes approved first, tag last; if already pushed wrong, add a follow-up tag rather than deleting a public one.

## Verification

- [ ] Commit window is explicit (tag..HEAD or since-date) and cross-checked against merged PRs
- [ ] Every changelog line carries its sha; no vague commit went in unread
- [ ] Every What's New item passes the non-developer-would-notice test
- [ ] No security exploit details in the public artifact
- [ ] User approved both artifacts before anything was appended, tagged, or published
- [ ] CHANGELOG.md heading, tag name, and What's New title all agree on the version
