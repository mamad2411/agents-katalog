---
name: obsidian-music-journal
description: Create and maintain music-related journal entries in Obsidian; log listening sessions, DJ set plans, album reviews, discovery notes, and curation reflections.
---

# obsidian-music-journal

## Purpose
Maintain a structured music journal within the Obsidian vault. Captures listening sessions, album impressions, DJ set plans, curation session notes, and music discovery entries. Links journal entries to library tracks and set plans for a connected music knowledge graph.

## Invocation
- "Log a listening session for [artist/album]"
- "Write a note about [album] I just listened to"
- "Save today's music discoveries to Obsidian"
- "Create a DJ set plan note for [event/date]"
- "Log my curation session notes"
- "Review what I've been listening to this week"

## Workflow Steps
1. **Classify:** Determine note type: listening session, album review, DJ set plan, discovery note, or curation log.
2. **Template:** Load appropriate template from vault (e.g., `templates/listening-session.md`, `templates/album-review.md`).
3. **Populate:** Fill in metadata: date, artist, album, genres, BPM/key if DJ context, mood, rating, notes.
4. **Link:** Add wikilinks to related artist notes, genre MOCs, and previous sessions.
5. **Tag:** Apply tags: `#music`, `#listening`, `#dj`, `#review`, etc.
6. **Save:** Write note to configured folder (e.g., `Music Journal/YYYY/MM/`).
7. **Index:** Update Music Journal index note with new entry.

## Safety
- Never overwrite existing journal entries; always append or create new.
- Do not expose private session details in shared vault contexts.
- Confirm before deleting any journal note.

## MCP
- Uses **Obsidian Local REST API** for note creation and vault access.
- Works via `obsidian-vault-manager` skill as the underlying vault interface.

## References
- Obsidian: https://obsidian.md/
- Obsidian Templater plugin: https://github.com/SilentVoid13/Templater
- Obsidian Local REST API: https://github.com/coddingtonbear/obsidian-local-rest-api

## Companion Skills
- `obsidian-vault-manager` — underlying vault interface
- `dj-library-curator` — source of curation session data
- `dj-set-architect` — set plan notes stored here
- `subsonic-media-server` — now-playing data for listening sessions
- `homelab-logbook` — cross-reference for homelab-adjacent music events
