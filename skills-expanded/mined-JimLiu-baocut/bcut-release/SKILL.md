---
name: bcut-release
description: Release BaoCut Electron desktop apps through GitHub Actions tags by default; use local/manual packaging only when explicitly requested. Also handles App version bumps, release continuation and portable signing backups; excludes craft skills and legacy standalone CLI releases.
---

# BaoCut desktop releases

This is the Electron v3 App (`com.baocut.app`). The older baocut-app skill is a
reference, not this checkout's executable workflow. Keep this developer skill
outside the App's craft `skills/`; do not invoke legacy GPUI/npm/Homebrew releases.

## Select the workflow

| User intent | Read and follow |
| --- | --- |
| Ordinary release/publish request; no method specified | [Tag release](references/tag-release.md) — **default**. Push the frozen source tag; publish verified Mac arm64 first, then append Windows CPU/CUDA/Vulkan to the same Release. |
| Explicit local package/candidate, traditional or manual release, single-platform recovery/continuation | [Traditional release](references/traditional-release.md). Honor the requested platforms and local-only/public scope. |
| Signing identity, portable backups or GitHub credentials only | [Signing/backups](references/signing-backups.md). Do not create a tag or publish. |

Load only the reference needed for the selected intent. Do not ask users to choose
between the two release methods when they have not specified one: use tag release.
Do not silently fall back to traditional packaging after an Actions failure.
A specific local-only or platform-only instruction overrides the default all-platform
scope; follow the user's explicit method and limits.

## Shared release constraints

- Inspect git status before edits; preserve unrelated or concurrent work. Commit
  task-owned source changes before freezing a release. Follow repository commit,
  current-task push authorization and worktree cleanup rules; do not reuse push
  authorization from another task or request it again when already granted here.
- `apps/desktop/package.json` owns the App version. Synchronize root version and
  lockfile through npm; do not bump Cargo or protocol versions for an App release.
- Query actual releases/feeds before choosing a build. Builds strictly increase;
  already published tags/files are immutable.
- Keep the tag and all platform artifacts tied to one full source SHA. Never ship
  dirty-source binaries, private signing materials or intermediate notary submissions.
- Publish the Mac Release, its reconciled changelog and verified download links as
  soon as the Mac candidate passes; Windows/CUDA builds do not block this stage.
  Later platform completion updates that Release's assets, notes and feeds, never
  the Git tag or its source SHA. Report pending platforms separately; advance Latest
  at the completion step below.
- For every new published version/build, follow [release notes](references/release-notes.md):
  inventory the full commit/PR range, summarize large ranges in batches, reconcile
  coverage and publish the consolidated changelog. A local candidate keeps the
  same notes locally; platform continuation reuses the existing version's range.
- After every public release or platform continuation, check the download links
  using [download links](references/download-links.md). The READMEs and baocut.com
  link to `baocut.com/download/<id>`, which follows GitHub Releases by itself. Do
  not edit the READMEs or redeploy the site for a release; verify that baocut.com
  serves the new build.
- Report actual checks and skips. A tag push or credential check alone is not a
  completed release; publication requires successful jobs, public read-back, feeds,
  verified release notes and a passing baocut.com download check.

## Complete public release

After all selected platforms have published, public assets and feeds have passed
read-back, and the consolidated release notes are verified, mark the newest stable
desktop release **Latest** in GitHub's Releases tab:

```bash
gh release edit "$release_tag" --repo "$release_repo" --latest
gh api "repos/$release_repo/releases/latest" --jq '.tag_name'
```

Use the verified repository and tag for this task; the read-back must match that
tag. Platform publishers preserve the previous Latest while validation and uploads
are in progress, so this final step is required even when Actions succeeds.
Local candidates, drafts and prereleases do not advance Latest. When continuing
an older release, keep a newer published desktop version/build as Latest. Include
the verified Latest tag in the completion report.

The [desktop guide](../../../apps/desktop/README.md) owns packaging mechanics;
mode-specific references explain when to load it. Requests only to change release
configuration must not create a release tag or publish.
