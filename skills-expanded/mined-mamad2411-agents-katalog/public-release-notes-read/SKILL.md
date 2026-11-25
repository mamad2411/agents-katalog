---
name: public-release-notes-read
skill_id: browser-skill:public-release-notes-read
description: Read public GitHub release notes for a named project
when_to_use:
  - host: github.com
    path_prefix: /
    intent_keywords: [release, notes, changelog, version, tag]
    require_auth: false
    mutation_boundary: read_only
steps:
  - caption: Read the requested public release notes
    capability_target: fetch_url
    mutation_boundary: read_only
adapter_preferences:
  preferred: browserbase
  fallback: owned_browser
  declined: []
schema_version: 1
metadata:
  luke:
    tags: [github, releases, changelog, read-only]
    related_skills: [browser-skill:github-public-pr-read]
platforms: [macos]
---

# Public release notes read

## Purpose
Read a named project's public GitHub release page and return the published
release title, version, date, and noteworthy changes.

## Reads
- Public GitHub release headings, dates, release notes, and visible asset names.

## Never
- Never sign in, read a private repository, download an asset, or change GitHub.
- Never treat generated asset metadata as a reason to expose personal data.

## Lands in
- Return a concise, attributable summary in the current Luke Ask thread.

## Steps
1. Open the public GitHub release page named by the user.
2. Read the requested release title, tag, date, and published notes.
3. Summarize the changes without inventing details that are not on the page.

## Success criteria
- Result identifies the project and requested release.
- Result includes the published version or tag and a concise change summary.

## Failure behavior
- If the release is missing, private, or unavailable, explain that limitation
  without asking for credentials or substituting a different release.

## Redaction
Omit query strings, user-entered values, email addresses, tokens, and any
unexpected private or authenticated content.
