---
name: dcc-design
description: Use this skill to generate well-branded interfaces and assets for DCC (Developer Control Center), either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.
If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.
If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

Key rules for DCC:

- Dark-only. Near-black background ladder (`--bg-0`…`--bg-3`), depth via background step + 1px hairline, shadows only on overlays.
- One cyan accent (`--accent`); status colors (healthy/degraded/failing/deploying/unknown) are the only other saturated colors, always paired with a glyph.
- IBM Plex Sans for chrome; JetBrains Mono for every identifier, URI, SHA, timestamp, log line.
- Voice: calm, terse, sentence case, verb-first actions, middle-dot fact strings, actionable errors. No emoji.
- Source spec: https://github.com/shaes-farm/dcc (docs/ARCHITECTURE.md).
