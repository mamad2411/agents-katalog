---
name: ux-design
description: "Guided, section-by-section UX spec authoring for a screen, flow, or HUD. Reads game concept, player journey, and relevant GDDs to provide context-aware design guidance. Produces ux-spec.md (per screen/flow) or hud-design.md using the studio templates."
---

> Port provenance: adapted from the pinned upstream source at `984023ddac0d5e27624f2baacde6105e45de375f` under MIT; see the repository parity ledger for the exact path and blob.

# Ux Design

This is a full-fidelity Codex port of a large upstream studio workflow. Its
detailed phases, templates, checks, and handoff prompts live in
[`references/full-workflow.md`](references/full-workflow.md) to keep skill
discovery lightweight.

## Required procedure

1. Read `references/full-workflow.md` completely before executing this skill.
2. Follow its phases in order and preserve all approval, review, testing, and
   evidence gates.
3. Adapt shell syntax to the detected platform; use PowerShell on Windows and
   POSIX syntax on macOS/Linux.
4. Inherit the active Codex model and permission mode. Never weaken sandbox,
   approval, provenance, or human creative-control boundaries.
5. If a referenced project artifact is absent, report the gap and use the
   documented fallback instead of inventing completion evidence.
