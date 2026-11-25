---
name: github-release-notes
description: Generate GitHub release notes for the upcoming version, following the Keep a Changelog 1.1.0 spec. Use when the user is preparing a release and asks to "draft release notes", "generate release notes", "create GitHub release notes", "產生 release notes", "準備發布", "產生發布說明", or similar pre-release phrasings. Return the notes directly in chat as ready-to-paste Markdown — do NOT create or modify CHANGELOG.md or any other file.
allowed-tools: Bash(git log:*), Bash(git tag:*), Bash(git describe:*), Bash(git show:*), Bash(git diff:*), Bash(git rev-list:*), Bash(git rev-parse:*), Read
metadata:
  author: Lucas Yang
  version: "2026.07.12"
---

# GitHub Release Notes Generator

Generate release notes for the project's upcoming version that are ready to paste into a GitHub release. Follow the [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) "Types of changes" conventions.

## Process

1. Find the latest release tag:
   - `git describe --tags --abbrev=0` (fallback: `git tag --sort=-v:refname | head -n 1`)
   - If no tag exists, use the full history.
2. List commits since that tag: `git log <tag>..HEAD --no-merges --pretty=format:"%h %s"`.
3. If an existing `CHANGELOG.md` is present, read it briefly to match the project's tone, language, and wording style — but do NOT modify or create that file.
4. Classify each commit into one of the Keep a Changelog change types. Omit any type with no entries.
5. Output the release notes as Markdown, wrapped in a single fenced code block so the user can copy-paste into the GitHub release UI.

## Types of changes (Keep a Changelog 1.1.0)

Use these exact heading labels, always in English (see Writing rules):

- `Added` — new features
- `Changed` — changes in existing functionality
- `Deprecated` — soon-to-be-removed features
- `Removed` — now-removed features
- `Fixed` — bug fixes
- `Security` — vulnerability fixes

## Breaking changes

Keep a Changelog defines no dedicated category for breaking changes. Do NOT invent a `Breaking` heading. Instead, list each breaking change under its most relevant type (usually `Changed` or `Removed`) and mark the bullet with a fixed `**Breaking:**` prefix — this exact spelling and casing every time, never `**breaking change**`, `**BREAKING**`, or any variant:

```
### Changed
- **Breaking:** Renamed the `config.load()` option `path` to `configPath`

### Removed
- **Breaking:** Dropped support for Node.js 18
```

The `**Breaking:**` marker stays in English even when the rest of the notes are translated (see Writing rules).

## Output format

Output ONLY the release notes Markdown inside a single fenced code block. No preamble, no trailing commentary, no surrounding explanation.

Do NOT include a version heading (`## [x.y.z]`) or date — GitHub's release page already renders the tag and publish date, so duplicating them is redundant. Start directly at the `###` type headings:

```
### Added
- Short, user-facing description of the change

### Fixed
- Short, user-facing description of the fix
```

## Writing rules

- Each bullet is one line, user-facing, and describes the impact — not the implementation.
- Do not include commit hashes or author names. PR numbers are fine if the existing `CHANGELOG.md` already uses them.
- Merge duplicate or related commits into a single bullet.
- Skip purely internal noise (lint config tweaks, CI-only changes, formatting passes, dependency bumps without user impact) unless that's all that exists — then group the meaningful ones under `Changed`.
- Match the language of the project's existing `CHANGELOG.md` if one exists; otherwise default to English.
- ALWAYS keep the type headings (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`) and the `**Breaking:**` marker in English — even when the user explicitly asks to translate the notes into another language. Only the bullet descriptions are translated; these fixed labels never are.
- Omit empty change types entirely.
