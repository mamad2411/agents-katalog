---
name: cuecaps-captions
description: Add animated word-by-word captions to a video or audio file with Cuecaps, and optionally cut dead space, filler words and retakes. Use when the user wants captions or subtitles on a TikTok, YouTube Short, Reel or YouTube video, a transparent caption overlay for Premiere Pro, DaVinci Resolve or Final Cut Pro, an SRT or VTT file, or wants the pauses cut out of a talking clip.
---

# Captions with Cuecaps

Cuecaps finds every spoken word, times it to the frame and renders it in one of 10 animated styles. The video is
rendered on the user's machine, never uploaded.

## Pick the route

1. **The Cuecaps MCP server is connected and has `caption_video`** (local server, `npx -y cuecaps-mcp` with a key):
   call `caption_video` with the absolute `path`. It writes `<name>.captions.<ext>` next to the input.
2. **Only `list_styles` and `studio_link` are available** (hosted server, `https://cuecaps.com/mcp`): call
   `studio_link` and give the user the link and the steps it returns. They drop the video in, click Find words and export.
3. **No Cuecaps server is connected:** suggest adding the hosted one (`claude mcp add --transport http cuecaps
   https://cuecaps.com/mcp`) or open https://cuecaps.com/studio for them.

## Settings

- `style`: call `list_styles` first if the user hasn't named one. Karaoke highlights the spoken word; Bold is capitals
  with an outline.
- `aspect`: `9:16` for TikTok, Shorts and Reels; `1:1` or `4:5` for feed posts; `16:9` for YouTube.
- `words`: 1 to 10 words per caption. 1 to 3 suits fast Shorts.
- `lang`: the spoken language code for anything not in English.
- `fast`: `deadspace` (pauses), `fillers` (um, uh, stutters), `retakes` (keeps the last take), `zoom` (punch-in on
  jump cuts), `norm` (-14 LUFS), or `["all"]`.
- The look, on top of the style, so the captions come out as the user described them: `font` (one of 24, such as
  `Bebas Neue`), `color` (text), `highlight` (the spoken word) and `emphasis` (key words) as hex or a color name,
  `mark` (`color`, `box`, `grow`, `dim`, `reveal`, `none`), `anim` (`pop`, `punch`, `bounce`, `rise`, `slide`,
  `fade`, `focus`, `typewriter`, `none`), `case` (`upper`, `lower`, `as-spoken`) and `size` (50 to 200 percent).
- `voice: true` (`studio_link` only): removes background noise once the words are found.
- `output` (local only): `mp4` burned in, `mov` or `webm` transparent overlay for an editor, `srt` or `vtt`.
- In the studio (the `studio_link` route), Export also offers ASS karaoke subtitles (word-by-word timing for FFmpeg,
  mpv, VLC and Aegisub) and, with Fast edit on, an EDL or FCPXML cut list that rebuilds the cut on the original
  footage in Premiere Pro, DaVinci Resolve or Final Cut Pro (Creator and Pro).

## Examples

- "Caption talk.mp4 for TikTok and cut the pauses" -> `caption_video { path, aspect: "9:16", fast: ["deadspace"] }`
- "I need an overlay for Resolve" -> `caption_video { path, output: "mov" }`
- "Karaoke captions on a Spanish Short" (hosted) -> `studio_link { style: "karaoke", lang: "es", aspect: "9:16" }`
- "Yellow Bebas captions that bounce in, and clean up the noise" -> `studio_link { style: "bold", font: "Bebas Neue",
  highlight: "yellow", anim: "bounce", voice: true }`
