---
name: release-notes-writer
description: Turn a commit range into release notes written for the people who use the software, grouped by user-visible change. Use when tagging a release rather than summarising development activity.
license: MIT
allowed-tools: Bash Read Write
metadata:
  category: communication
x-internal-review-status: draft
---

# Release notes

Write for someone deciding whether to upgrade.

## Grouping

Group by what changed for the user: added, changed, fixed, deprecated, removed
and security. Do not group by component or by author.

## Wording

State the change and its consequence. "Search now returns results for
hyphenated terms" beats "refactored the tokenizer".

## Breaking changes

List every breaking change first, with the migration step next to it. A
breaking change discovered after upgrading is a support burden.
