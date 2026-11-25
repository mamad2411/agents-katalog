---
name: release-notes
description: Drafts release notes from merged pull requests. Use when the user asks for release notes or a changelog entry for a tag. Do not use for marketing announcements.
---

# Release notes

Collect merged pull requests since the last tag, group them by area and write one line per change.

## Example

```bash
git log --merges --oneline v1.1.0..HEAD
```

The wording rules are in [the guide](references/GUIDE.md).
