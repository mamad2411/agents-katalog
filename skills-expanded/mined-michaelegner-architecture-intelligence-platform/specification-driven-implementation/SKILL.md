---
name: specification-driven-implementation
description: Use when implementing substantial work against an AIP release or increment specification (docs/specifications/<release>/specification.md or its iN-*.md increment specs) - producing a reviewed plan before changing production code, persisting it, implementing without altering normative semantics, and reconciling the result against the retained plan. Not needed for small maintenance changes that don't touch public contracts, identity, evidence, qualification, reconciliation, or release semantics.
---

# Specification-driven implementation

This is the Claude Code discovery entry point for this repository's specification-driven
implementation workflow. It intentionally carries no procedure of its own.

The canonical, full procedure — the nine phases, the stop conditions, the plan template, and the
reconciliation template — lives at
[`.agents/skills/specification-driven-implementation/SKILL.md`](../../../.agents/skills/specification-driven-implementation/SKILL.md).

Read that file in full and follow it exactly. Do not treat this file as a separate or abbreviated
version of the workflow — if the two ever appear to disagree, the canonical file is correct and
this file is stale and should be fixed to match it, not the other way around.
