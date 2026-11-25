---
name: release-surface-verification
description: Use before claiming a GitHub, public template, or release-page update is complete, especially after version bumps, tags, GitHub Releases, README badges, About/sidebar text, topics, links, or public onboarding changes.
---

# Release Surface Verification

Use this skill whenever the task affects what another person sees on GitHub or another public project surface.

## Purpose

Prevent false completion where the source layer changed but the user-visible surface was not verified.

The source layer includes local files, commits, pushed branches, tags, and release notes in the working tree.

The visible surface includes the GitHub repository page, About sidebar, topics, latest-release panel, release page, rendered README, badges, documentation links, and any browser-rendered setup instructions.

## Activate For

- version bump, tag, release, or changelog update
- GitHub Release creation or edit
- README, README_CN, badge, About, topic, landing-page, setup-guide, or docs-navigation change
- user asks whether a public repo, template, release, or share link is ready
- previous run may have claimed completion from git state alone

## Required Checks

Before saying the public update is complete, verify both layers:

1. Source layer:
   - working tree status for intended files
   - commit exists if the task required a commit
   - tag exists and is pushed if the task required a version tag
   - changelog and version references are consistent
2. Visible surface:
   - GitHub Releases page shows the expected release
   - repository sidebar `Latest` release points to the expected version
   - About description and topics match the intended public positioning
   - rendered README/README_CN show the expected version, badges, and links
   - important docs links resolve from the public page
3. Boundary:
   - if a surface cannot be verified, state `TO VERIFY` with the exact surface
   - do not describe the release as complete when only the source layer has been checked

Use the GitHub connector, GitHub CLI, or browser verification when available. If no live GitHub check is available, report the limitation clearly and provide the exact manual checks for the user.

## Output Format

```text
Release surface verification:
- Source layer:
- GitHub release page:
- Sidebar latest release:
- About/topics:
- Rendered README/docs:
- Links:
- Privacy/public boundary:
- Verdict: PASS / PARTIAL / BLOCKED
- Remaining manual checks:
```

## Guardrails

- Do not create or publish a release unless the user requested that action.
- Do not change repository visibility without explicit user confirmation.
- Do not add private project details, credentials, institutional data, participant material, screenshots, or local paths to public release notes.
- Do not use star count, release badge, or About status as proof that setup instructions work.
