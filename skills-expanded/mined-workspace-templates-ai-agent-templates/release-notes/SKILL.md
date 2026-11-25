---
name: release-notes
description: Writes user-facing release notes from merged pull requests since the last release, grouped by what users can now do.
disable-model-invocation: true
---

Write release notes for the changes since: $ARGUMENTS (the latest tag if empty).

1. Collect merged changes with `git log <since>..HEAD --merges --oneline`; if the project squashes, use `git log --no-merges`. When `gh` is available, read the pull request titles and descriptions for context.
2. Drop internal work: refactors, tests, CI, dependency bumps without user effect.
3. Write for the people who use the product, not the people who build it. Lead each item with the benefit ("You can now export reports as CSV"), then one clause of detail.
4. Put anything that needs action first under **Before you upgrade**: breaking changes, migrations, renamed settings, removed features, with the exact step to take.
5. Then use the sections **New**, **Improved**, **Fixed**. Credit external contributors by handle if the history shows them.

Keep it under 300 words and avoid jargon and internal ticket numbers. Show the draft, ask what to change, and do not publish or tag anything.
