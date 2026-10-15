---
name: reference-trash-rules
description: Determines which TRaSH Guide rules apply from current context (file path, chapter, or stack) and references them. Use when the user asks to reference TRaSH rules, which rules apply here, or when working on media stack docs (Chapter2c, Chapter 3b), docker_compose/media, or docker_compose/accelerated and the agent should follow the correct guidelines.
---

# Reference TRaSH Rules by Context

When the user asks to **reference TRaSH rules**, **which rules apply here**, or when you are working on media stack content and need to apply the right guidelines: infer context from the **current file path**, **open documents**, or **user mention**, then apply the mapping below. TRaSH Guides are the **gold standard**; the agent must **open the links** in the rules (or on [trash-guides.info](https://trash-guides.info/)) to get the correct, up-to-date guide—not rely only on embedded summaries.

---

## Command behavior

The "command" is a user request such as:

- "Reference TRaSH rules"
- "What TRaSH rules apply here?"
- "Which guidelines should I follow for this?"

**Response:**

1. **Infer context** from the current file path, the file the user has open or mentioned, or the stack/chapter they name (e.g. media, accelerated, Chapter 2c, Chapter 3b).
2. **Resolve which rules apply** using the context → rules mapping below.
3. **List** the applicable Cursor rule files (`.cursor/rules/trash-guides-*.mdc`) and the corresponding TRaSH sections (URLs).
4. **Remind** that TRaSH is the gold standard and that the agent should open those links for the correct guide when configuring or documenting.

---

## Context → rules mapping

Use the **first matching** row (most specific wins). Paths are relative to repo root.

| Context | Applicable rules |
|--------|-------------------|
| **Media stack** — `docs/Chapter2c-media.md`, `docs/Chapter2c*.md`, `docker_compose/media/**` | gold-standard, file-folder-structure, radarr, sonarr, prowlarr, bazarr, qbittorrent, sabnzbd, plex, guide-sync, misc, glossary |
| **Accelerated / Plex transcoding** — `docker_compose/accelerated/**`, or topic is Plex/transcoding/4K | gold-standard, file-folder-structure, plex, misc (x265/4K Golden Rule), glossary |
| **Docker compose & config** — `docs/Chapter3b*`, or future chapter covering compose and configurations | gold-standard, file-folder-structure, misc (how to provide a compose); plus media stack rules if the chapter covers media stack (radarr, sonarr, etc.) |
| **Single app mentioned** — User names one app (e.g. "Radarr", "qBittorrent") | gold-standard + the matching rule(s): radarr, sonarr, prowlarr, bazarr, qbittorrent, sabnzbd, plex, guide-sync, file-folder-structure (always for paths), glossary (for terms) |
| **Unclear or general** | gold-standard, file-folder-structure, glossary; suggest "For media stack, also reference: radarr, sonarr, prowlarr, bazarr, qbittorrent, sabnzbd, plex, guide-sync, misc." |

**Rule file names** (under `.cursor/rules/`):

- `trash-guides-gold-standard.mdc` — always when any TRaSH context applies
- `trash-guides-file-folder-structure.mdc`
- `trash-guides-radarr.mdc`, `trash-guides-sonarr.mdc`, `trash-guides-prowlarr.mdc`, `trash-guides-bazarr.mdc`
- `trash-guides-qbittorrent.mdc`, `trash-guides-sabnzbd.mdc`
- `trash-guides-plex.mdc`, `trash-guides-guide-sync.mdc`, `trash-guides-misc.mdc`, `trash-guides-glossary.mdc`

---

## How to respond

1. State the **inferred context** (e.g. "Media stack (Chapter 2c / docker_compose/media)").
2. List the **applicable rule files** and **TRaSH URLs** (from the Source link in each rule, or [trash-guides.info](https://trash-guides.info/)).
3. Add: "Open these links for the correct, up-to-date guide. TRaSH is the gold standard; follow it as well as possible when configuring or documenting."

If the user is about to edit a specific app (e.g. compose for qBittorrent), name that rule and its TRaSH section explicitly so the agent follows it.
