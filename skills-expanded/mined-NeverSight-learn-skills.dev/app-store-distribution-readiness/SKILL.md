---
name: app-store-distribution-readiness
description: Prepare mobile apps, desktop software, games, and utilities for distribution through App Store, Google Play, Steam, Microsoft Store, web, or direct download. Use when planning launch readiness, store metadata, screenshots, privacy disclosures, payments, subscriptions, store review, OS integration, updates, or release operations.
---

# App Store Distribution Readiness

Use this skill to prepare software for real-world distribution channels, not just a local build.

## Workflow

1. Identify product type and target channels.
2. Read `references/distribution-channel-matrix.md`.
3. Build channel-specific readiness: metadata, screenshots, payments, privacy, testing, review, release, support.
4. Identify OS integration requirements: permissions, notifications, storage, backup, update, file associations, startup behavior.
5. Produce launch blockers, review risks, and release checklist.

## Output format

```text
Channels:
Product type:

Readiness matrix:
- <channel> — metadata, policy, payments, testing, release, support

OS/platform details:
- <detail>

Launch blockers:
- <blocker and owner>
```
