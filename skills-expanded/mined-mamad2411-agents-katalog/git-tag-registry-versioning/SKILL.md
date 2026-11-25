---
name: git-tag-registry-versioning
description: Add semver rollback and pinning to any git-backed asset registry (skills, prompts, commands, snippets) using namespaced annotated tags per item and per-release bundle.
category: arch
tags: [git, versioning, semver, registry, rollback, tags]
triggers: [version pin, rollback, git tag, registry versioning, skill versioning, prompt versioning, "install specific version"]
source_project: skills-hub
version: 1.0.0
---

# Git-Tag-Based Registry Versioning

Namespaced git tags turn a flat asset-registry repo into a versioned package store with per-item rollback — no database, no separate artifact host.

See `content.md` for the full pattern, including the dual-tag layout (per-item + per-release-bundle), registry schema additions, and the shallow-clone pitfall.
