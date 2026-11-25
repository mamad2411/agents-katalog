---
name: release
description: Cut a tagged GitHub Release for willow-2.0. Enforces the full sequence — CHANGELOG PR, CI gate, master pull, tag push.
---

# /release

> **Authorization gate.** Do not push the tag without USER's explicit approval. The tag triggers the public GitHub Release workflow — this is a one-way action.

---

## When to use this skill

- USER says "cut the release", "tag it", or "ship v…"
- The CHANGELOG `[Unreleased]` section has content ready to ship
- CI is green on master

---

## Pre-flight checks (run before any action)

```
git -C $WILLOW_ROOT pull origin master
cat $WILLOW_ROOT/VERSION                    # current version string
gh pr list --repo rudi193-cmd/willow-2.0 --state open   # no open PRs blocking the release?
gh pr checks <most-recent-pr> --repo rudi193-cmd/willow-2.0  # CI green?
```

Surface the results. If CI is not green on master, stop and report.

---

## Steps

**1. Verify CHANGELOG is ready**

Read `CHANGELOG.md`. The `[Unreleased]` section must have content. If it is empty or absent, stop — the CHANGELOG update PR must go first.

**2. CHANGELOG PR**

Open a worktree (`feat/release-vX.Y.Z`) — **pull master first**.

Update `CHANGELOG.md`:
- Rename `## [Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD`
- Leave an empty `## [Unreleased]` above it for the next cycle
- Fold any existing stub entry for `[X.Y.Z]` into the new section

Commit, push, open PR. Title: `chore(release): CHANGELOG for vX.Y.Z`.

**3. Wait for CI + USER approval**

Do not proceed until:
- All CI jobs on the CHANGELOG PR are green
- USER approves or merges the PR

**4. Pull master after merge**

```
git -C $WILLOW_ROOT pull origin master
```

Verify the merge commit is the new HEAD.

**5. Tag**

```
VERSION=$(cat $WILLOW_ROOT/VERSION)
git -C $WILLOW_ROOT tag "v${VERSION}" -m "Release v${VERSION}"
```

Show USER the tag before pushing:
> About to push tag `vX.Y.Z` to origin — this triggers the GitHub Release workflow. Confirm?

**6. Push tag (requires USER's go-ahead)**

```
git -C $WILLOW_ROOT push origin "v${VERSION}"
```

The `release.yml` workflow fires on the tag push and creates the GitHub Release.

**7. Verify**

```
gh release view "v${VERSION}" --repo rudi193-cmd/willow-2.0
```

Report the release URL.

---

## Hard constraints

| Rule | Reason |
|---|---|
| Never push a tag without explicit USER approval | Tag push is public and triggers release workflow |
| Always pull master after the CHANGELOG PR merges | Tag must point to the correct HEAD |
| CHANGELOG `[Unreleased]` must be non-empty | Empty release is a no-op and creates confusion |
| CI must be green on master before tagging | Tag on a broken master creates a broken release |

---

## Version scheme

`MAJOR.MINOR.PATCH` using CalVer (`YYYY.MM.N`). Current version is always in `VERSION` at repo root. Do not bump VERSION in this skill — VERSION is bumped separately when starting a new development cycle.

---

## Execution note

All git commands go through `agent_task_submit` → `kart_task_run`. Do not use the Bash tool for git or gh operations.
