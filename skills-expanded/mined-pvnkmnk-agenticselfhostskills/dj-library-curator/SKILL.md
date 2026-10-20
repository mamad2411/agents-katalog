---
name: dj-library-curator
description: Curate, tag, and organize the DJ music library; manage BPM analysis, key detection, genre tagging, and crate/playlist creation for DJ workflows.
---

# dj-library-curator

## Purpose
Maintain a DJ-ready music library with enriched metadata: BPM, key, energy level, genre, and crate assignments. Bridges the general music library (organized by beets) with DJ software requirements (Rekordbox, Serato, Traktor).

## Invocation
- "Analyze BPM and key for new tracks in DJ library"
- "Create a crate for [genre/mood/BPM range]"
- "Tag tracks in [folder] with DJ metadata"
- "Find tracks in key of Am at 128 BPM"
- "Export crate [name] as M3U playlist"
- "Sync DJ library with Navidrome playlists"

## Workflow Steps
1. **Ingest:** Identify tracks newly added by `music-library-organizer` that are DJ-relevant.
2. **Analyze:** Run BPM and key analysis (e.g., via `bpm-tools`, `keyfinder-cli`, or `essentia`).
3. **Tag:** Write BPM, key, energy, and DJ crate tags back to file metadata.
4. **Curate:** Assign tracks to crates based on genre, BPM range, key compatibility, or mood.
5. **Playlist export:** Generate M3U/PLS playlists per crate; optionally push to `subsonic-media-server`.
6. **Journal:** Log curation session and notable additions in `obsidian-music-journal`.
7. **Log:** Record activity in `homelab-logbook`.

## Safety
- Do not overwrite existing manual DJ tags without confirmation.
- Back up metadata before bulk re-analysis.
- Never remove tracks from crates without explicit instruction.

## MCP
- No dedicated MCP; orchestrates CLI tools (bpm-tools, keyfinder-cli) via agent subprocess.
- Integrates with `subsonic-mcp` for playlist sync.

## References
- bpm-tools: https://www.pogo.org.uk/~mark/bpm-tools/
- KeyFinder: https://github.com/ibsh/is_KeyFinder
- Essentia: https://essentia.upf.edu/
- Rekordbox XML export: https://rekordbox.com/

## Companion Skills
- `music-library-organizer` — upstream library source
- `subsonic-media-server` — playlist streaming target
- `dj-set-architect` — uses curated crates to build sets
- `obsidian-music-journal` — curation session notes
- `homelab-logbook` — activity logging
