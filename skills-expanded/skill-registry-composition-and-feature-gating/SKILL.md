---
name: skill-registry-composition-and-feature-gating
description: "Compose skill registries in fixed phases with explicit feature gates so merged command surfaces stay deterministic and cheap to refresh."
metadata:
  author: ychampion
---

# SKILL: Skill Registry Composition and Feature Gating
**Domain:** command-surfaces  
**Trigger:** Use when a coding agent assembles skills or prompt commands from multiple sources and optional features can enable, disable, or delay some of them.  
**Source Pattern:** Distilled from reviewed command-surface, registry-bootstrap, and dynamic-skill loading implementations.

## Core Method
Assemble the registry in explicit phases instead of letting sources merge opportunistically. Start from the always-on local surface, then layer bundled skills, project-local skills, plugin-provided entries, and remote or MCP-discovered skills in a stable order. Apply feature gates before importing or materializing each optional phase so disabled sources do not cost startup time or leak partial entries into the merged view. After composition, dedupe by canonical command identity and memoize the final snapshot so listing, search, and execution all see the same result.

## Key Rules
- Keep the phase order fixed and documented so later additions do not silently change precedence.
- Check feature gates before loading optional modules or scanning optional sources.
- Deduplicate after all enabled sources are collected, using one canonical identity rule for listing and execution.
- Cache the merged snapshot, not just individual source scans, so downstream consumers stay in sync.
- Invalidate every derived surface that depends on the merged registry when any source changes.

## Example Application
If a terminal coding agent loads built-in skills, project-local skills, and MCP-discovered prompt tools, first collect the always-on built-ins, then project-local skills, then gated remote sources. Dedupe the combined list, cache that snapshot, and feed the same snapshot to help menus, slash-command discovery, and command execution.

## Anti-Patterns (What NOT to do)
- Don’t let optional sources self-register at import time before checking whether the feature is enabled.
- Don’t dedupe each source independently and assume the final merged list will stay clean.
- Don’t let help text, search, and execution build separate registry snapshots from different source orders.
