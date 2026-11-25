---
name: "release-note-formats"
description: "Release note structures: release notes vs changelogs, audience needs, release types, formats by channel (GitHub release, blog, email, in-app), and a breaking change documentation standard. Use when choosing the shape and channel for release notes."
---

# Release Note Formats

> Release note structures for different audiences, channels, and release types.

## Knowledge Base

### Release Note vs Changelog

| Changelog | Release Notes |
|-----------|--------------|
| Technical record of changes | Communication to users |
| Every version, every change | Curated highlights |
| Developer audience | Multiple audiences |
| Keep a Changelog format | Flexible format |
| Lives in CHANGELOG.md | Lives in GitHub Releases, blog, email |

A changelog is the raw material. Release notes are the polished product.

### Audience Needs

| Audience | Cares About | Does Not Care About |
|----------|-------------|-------------------|
| End Users | New features, UX changes, fixed annoyances | API changes, internal refactors |
| Developers | API changes, SDK updates, breaking changes | Marketing copy, UI screenshots |
| Admins | Infrastructure changes, security patches, config changes | New UI features |
| Executives | Impact metrics, strategic features | Technical details |

### Release Types

| Type | Tone | Content Focus |
|------|------|--------------|
| Major (X.0.0) | Exciting but careful | Highlights, breaking changes, migration |
| Minor (0.X.0) | Positive | New features, improvements |
| Patch (0.0.X) | Reassuring | Bug fixes, security patches |
| Hotfix | Urgent, professional | Specific fix, impact scope |
| Security | Serious, actionable | CVE details, patch instructions |

### Format by Channel

**GitHub Release:**
- Full markdown with all details
- Code examples for API changes
- Links to migration guide
- Comparison link to previous version

**Blog Post:**
- Narrative introduction with context
- Feature highlights with screenshots
- Quotes from team or community
- Call to action (upgrade, try it)

**Email Digest:**
- 3-5 bullet points maximum
- Links to full release notes
- Clear upgrade call to action
- Unsubscribe option

**In-App Notification:**
- One sentence per feature (3-5 features)
- "New" badges on affected UI elements
- Link to "What's New" page

### Breaking Change Documentation Standard

Every breaking change entry must include:

1. **What changed**: One sentence describing the change
2. **Why it changed**: Brief rationale
3. **Migration path**: How to update (code diff preferred)
4. **Automated fix**: Codemod command if available
5. **Timeline**: When the old behavior will be fully removed (if deprecation)

## Patterns

1. **Highlight Reel**: Lead with the 2-3 most impactful changes. Bury the detailed list below.
2. **Progressive Detail**: Title > One-liner > Paragraph > Code example. Each level adds detail for readers who want it.
3. **Version Badge**: Clearly show the version number and release date at the top.
4. **Comparison Link**: Always link to the full diff (e.g., `v1.9.0...v2.0.0`) for developers who want to see every commit.
5. **Credit Contributors**: Thank contributors by name. It costs nothing and builds community.

## Anti-Patterns

1. **The Git Log Dump**: Pasting raw commit messages as release notes. Commits are not user communication.
2. **"Various bug fixes"**: Tells users nothing. List the actual bugs that were fixed.
3. **Breaking Changes Buried**: Hiding breaking changes in the middle of a feature list. They deserve their own prominent section.
4. **No Upgrade Path**: Announcing breaking changes without explaining how to migrate. Users feel abandoned.
5. **Marketing-Only**: Release notes that read like press releases with no technical substance.
6. **Stale Template**: Using the same generic template for every release without adapting to the content.

## References

- [GitHub Releases Best Practices](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Release Please](https://github.com/googleapis/release-please)
