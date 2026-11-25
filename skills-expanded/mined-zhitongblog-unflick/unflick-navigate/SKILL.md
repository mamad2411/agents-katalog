---
name: unflick-navigate
description: >-
  Find a moment inside a video and go to it — search what was said and jump to
  the line, walk chapters, or save and return to named bookmarks — with the
  unflick player. Use when the user asks "where do they say X", "jump to where
  they mention Y", "next chapter", "make chapters for this", "bookmark this
  spot", or "take me back to that bit". Requires the unflick MCP server (or CLI).
license: MIT
---

# unflick: find the moment, then go to it

Seeking by seconds is a poor way to find a scene. unflick can seek by what was
said, by chapter, and by a name the user gave a spot earlier.

## By what was said

The player reads the subtitle track it already has open — embedded, sidecar, or
one whisper.cpp generated (see the `unflick-subtitles` skill).

- `search_transcript(query, limit?)` — every match with its timestamp.
- `seek_to_text(query, occurrence?)` — jump to a match. Lands just *before* the
  line so the user hears it from the start.
- `transcript_get()` — the whole transcript as timed cues.

```bash
unflick transcript search "the treasure"
unflick transcript seek "the treasure" --occurrence 2
```

If there is no readable subtitle track, these say so — generate one first
rather than guessing at timestamps.

## By chapter

- `chapter_list()`, `chapter_seek(index)`, `chapter_next()`, `chapter_prev()`.
- `generate_chapters(count?)` — derive chapters from pauses in the transcript
  when the file has none of its own.
- `set_chapters(chapters)` — supply a list you wrote yourself:
  `[{"time": 0, "title": "Cold open"}, …]`.

Generated and supplied chapters are real navigation, not a side note: they mark
the progress bar and answer `chapter_seek`. They are cleared when the file
changes, so set them for the file that is playing now.

## By name

- `bookmark_add(name?, position?, file?)` — defaults to where playback is.
- `bookmark_list(file?, all?)`, `bookmark_goto(id)` — seeks within the current
  file, or opens the bookmarked file if it is a different one.
- `bookmark_rename(id, name)`, `bookmark_remove(id)`, `bookmark_clear(…)`.

```bash
unflick bookmark add --name "the good bit"
unflick bookmark list
unflick bookmark goto 1
```

Bookmarks survive restarts. They are keyed by path — for a disc that means the
drive letter, so a bookmark left on one DVD will be offered on the next disc in
that drive.

## Guidance

- Prefer `seek_to_text` over arithmetic on `get_status.position`: the user asked
  for a line, not a number.
- Repeated `bookmark_add` within a second is treated as a correction of the same
  spot, not a second bookmark — say so rather than reporting two.
- `bookmark_clear` refuses to guess "everything": pass a file, or `all`.
