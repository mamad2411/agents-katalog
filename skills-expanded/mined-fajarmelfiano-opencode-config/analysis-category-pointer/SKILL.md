---
name: analysis-category-pointer
description: "Pointer to a library of 3 specialized Analysis skills. Use when working on analysis-related tasks."
risk: none
---

# Analysis Capability Library 🎯

This is a **pointer skill**. The 3 specialized Analysis skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **nexrad-mosaic-construction** — Construct a quality-aware NEXRAD multi-radar mosaic from aligned single-site products with explicit coverage, beam geometry, quality weighting, overlap resolution, and provenance.
- **nexrad-radar-visualization** — Plot NEXRAD Level II/III site scans and decoded radar mosaics with correct radar geometry, map grids, units, quality masks, timestamps, and provenance.
- **radar-satellite-analysis** — Interpret weather radar and satellite observations by validating product metadata and geometry, deriving storm and cloud structures, tracking evolution, and quantifying uncertainty.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/analysis/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/analysis`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
