---
name: batch-artifact-verification
category: release
description: Use when a batch (desktop or mobile) release reaches awaiting_verdict or was rolled back - read-only checks that the published artifact really exists and is served, and the exact yank step for a bad tag
source: olivierlacan/keep-a-changelog (MIT), adapted
---

# Batch artifact verification

A batch release (desktop, mobile and other human-cut components) has no bound runtime environment — see `post-deploy-verification`'s last section. Its evidence is whether the thing it built actually got published and is what users will fetch next, per executor.

## `github_actions` / `local`

```
run_terminal("gh release view <tag> --json tagName,isDraft,isPrerelease,isImmutable,publishedAt,assets")
```

Expect `isDraft: false`, the platform's assets present with `size > 0`, and the update-feed file if the app ships one (e.g. `latest-mac.yml`). If `gh` is unavailable but the repository is public, fall back to `fetch_url https://api.github.com/repos/<owner>/<repo>/releases/tags/<tag>`.

If the repository brief names an update feed or a Homebrew cask URL, `fetch_url` it and confirm it names the new version — that is what actually reaches an existing install, not the GitHub Release page by itself.

For a `local` executor, the exit code is the first signal: `local_run.exit_code == 0`, with `local_run.tail` showing the publish step actually ran (not just that the build compiled).

## `store`

Every entry in `store_builds[]` must have `build != baseline_build` and carry no `error`. A `baseline_build` of `"?"` means the baseline was never confirmed — say so rather than treating it as a pass. "Deployed" here means the build reached the internal/testing channel; promoting it to production is a human step taken in the store console, and your finish note says so explicitly rather than implying the rollout is live.

## Yanking a bad batch release

This is the first `manual_steps` item on a batch rollback (`rollback-runbook`), and you perform it yourself — it is the one write `release-terminal-scope` allows:

```
run_terminal('gh release edit <tag> --prerelease --title "<name> [YANKED]"')
```

This works on an immutable release (title, notes and prerelease/latest stay editable; assets and the tag itself do not) and removes it from GitHub's "latest" resolution (the most recent non-prerelease, non-draft release), which most update feeds follow via `/releases/latest`. Then point "latest" back at the previous good release:

```
run_terminal("gh release edit <previous-good-tag> --latest")
```

Record the exact commands you ran and their output as evidence on the card — this is not a suggestion for a human to carry out, it is work you did and are reporting.

Never delete the release or its tag, and never `git push --delete` it — an immutable tag cannot be reused (GitHub Docs: immutable releases), and SemVer §3 holds here too: a released version's contents are never modified, only marked bad. A cask/update-feed PR pointing at the new tag, or halting a store rollout, are human steps outside `gh release`'s reach — report them, naming exactly what needs to change and where.

✅ "Yanked v2.4.1: `gh release edit v2.4.1 --prerelease --title \"TaskTrooper 2.4.1 [YANKED]\"` (exit 0); restored latest to v2.4.0: `gh release edit v2.4.0 --latest` (exit 0). `gh release view v2.4.1` now shows `isPrerelease: true`. Left for a human: the Homebrew cask formula still points at v2.4.1 — needs a PR bumping it back to v2.4.0."

❌ "Release looks bad, someone should pull it." — no command run, no evidence, and it was this agent's job to run it, not a human's.

## Common Mistakes

- Treating a store build reaching the internal channel as "released to users" — it is not, until a human promotes it.
- Deleting a release or tag instead of marking it `[YANKED]` and moving `--latest`.
- Reporting a yank as done without the command output that proves it happened.
- Checking only `isDraft`/`isPrerelease` and skipping the update feed — a feed that still points at the bad tag means existing installs keep fetching it even after the GitHub Release itself is marked yanked.
