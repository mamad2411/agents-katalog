---
name: meta-wearables-knowledge-base
description: Source-pinned knowledge base for Meta Wearables — Device Access Toolkit (DAT) iOS and Android API atlases, device sessions, camera, audio, display, Web Apps, sensors, transport, compliance, release operations, and the official source registry. Use when a meta-wearables-ops skill links into it, or when you need the cited reference for a Meta smart-glasses SDK surface.
---

# Meta Wearables knowledge base

Shared reference library for the meta-wearables-ops skills. Every document lives under
`references/` in this skill's directory. Other meta-wearables-ops skills link here with
`../meta-wearables-knowledge-base/references/<path>`; if your tool installs skills
under prefixed directory names, find this skill by name and resolve the same
`references/<path>` inside it.

## Where to start

- `references/70-meta-wearables/README.md` — the lane overview, current source
  snapshot, and reading order.
- `references/70-meta-wearables/00-platform-and-route-selection.md` — choose between
  native iOS, native Android, and Display Web Apps.
- `references/sources/meta-wearables-source-registry.md` and
  `references/sources/meta-wearables-source-freshness-log.md` — check these before
  calling any SDK claim current. Pin exact package revisions in real apps.

Search the tree for the API or capability name instead of reading it front to back.
