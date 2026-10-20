---
name: dj-set-architect
description: Design and sequence DJ sets using harmonic mixing principles, BPM flow analysis, and energy curve planning; generate set plans and tracklists from the curated DJ library.
---

# dj-set-architect

## Purpose
Plan and sequence DJ sets by analyzing the curated library for harmonic compatibility, BPM flow, and energy curves. Produces structured set plans with track order, transition notes, and key/BPM metadata. Supports export to DJ software formats and Obsidian set planning notes.

## Invocation
- "Plan a 60-minute techno set starting at 128 BPM"
- "Build a set for [mood/genre] using library tracks"
- "Sequence [list of tracks] into a harmonic set"
- "Generate a warm-up set from 120 to 132 BPM"
- "Export set plan for [name] as M3U"
- "Save set plan to Obsidian vault"

## Workflow Steps
1. **Define parameters:** Gather target duration, genre, BPM range, energy curve shape (build, peak, cool-down), and key preferences.
2. **Query library:** Pull candidate tracks from `dj-library-curator` crates matching parameters.
3. **Filter:** Remove tracks not yet analyzed (no BPM/key); flag for analysis if needed.
4. **Sequence:** Apply harmonic mixing rules (Camelot Wheel); build BPM flow curve respecting energy shape.
5. **Review:** Present draft tracklist with BPM, key, transition notes.
6. **Refine:** Accept user edits to swap or reorder tracks.
7. **Export:** Output M3U playlist; optionally push to `subsonic-media-server`.
8. **Journal:** Save set plan to `obsidian-music-journal` as a structured note.
9. **Log:** Record set plan in `homelab-logbook`.

## Safety
- Do not auto-delete or reorder tracks in the source library.
- Always confirm before overwriting an existing set plan.
- Flag harmonic clashes clearly; never silently ignore key incompatibilities.

## MCP
- No dedicated MCP; uses `subsonic-mcp` for playlist output; Obsidian MCP for note creation.

## References
- Camelot Wheel: https://www.harmonic-mixing.com/
- Mixed In Key: https://mixedinkey.com/
- bpm-tools: https://www.pogo.org.uk/~mark/bpm-tools/

## Companion Skills
- `dj-library-curator` — source of analyzed, curated tracks
- `subsonic-media-server` — playlist streaming target
- `obsidian-music-journal` — set plan note storage
- `homelab-logbook` — session logging
