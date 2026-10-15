---
name: buda-youtube-to-script
description: >-
  Use this skill whenever the user provides a YouTube or other video URL and
  asks to create, generate, rewrite, repurpose, summarize into, or get a new
  talking script, voiceover script, or short-form video script. Trigger
  strongly when this skill is selected and the user sends only a video URL,
  or on phrases like "get new talking script", "rewrite this video as
  a script", "turn this YouTube video into a voiceover", or when the user
  gives a video URL plus an angle or prompt. This skill is fully
  self-contained — it downloads the source video and audio with
  the bundled yt-dlp helper, transcribes the audio with Whisper, reads the
  bundled assets/talking-script-template.md, then produces a new
  template-based talking script. No other skill needs to be installed.
---

# YouTube to Talking Script

Turn a video URL into a new talking script by downloading the source video and audio, transcribing it, and rewriting the content into the user's requested angle.

This skill is self-contained. It does NOT depend on any separate downloader skill. The yt-dlp download logic ships with this skill at `scripts/download-audio.sh`, and the output template ships at `assets/talking-script-template.md`.

Important default: for Buda demos and script-generation tasks, keep the source video as a user-facing artifact together with the MP3, transcript, and final script.

## Default behavior

Unless the user says otherwise:

- Output language: English
- Script style: short-form talking script suitable for Red Note / TikTok / YouTube Shorts
- Target length: 60–90 seconds
- Rewrite mode: creative repurposing, not a literal translation or transcript summary
- Preserve the source video's core idea, but make the final script natural for a human to speak
- Include a strong 0–3 second hook
- Save all artifacts under `/agent/outputs/talking-scripts/<safe-title-or-id>-<YYYYMMDD-HHMMSS>/`
- By default keep the downloaded source video, MP3 audio, transcript, and final script

## Inputs to extract from the user

Required:

- Video URL

Optional:

- Angle / prompt, for example: `get new talking script`, `for entrepreneurs`, `make it 60 seconds`, `Red Note style`, `focus on how AI tools boost efficiency`
- Target platform
- Target audience
- Target duration
- Output language
- Whether to include timestamps, subtitles, or title ideas

If the user gives only a URL, proceed with the defaults. Do not ask unnecessary clarification questions.

## Workflow

### 1. Prepare a task folder

Create a durable output directory, not scratch files in `/agent` root.

```bash
mkdir -p /agent/outputs/talking-scripts
WORKDIR="/agent/outputs/talking-scripts/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$WORKDIR"
```

If possible, use `yt-dlp --print title` or `yt-dlp --print id` to create a more descriptive folder name. Sanitize names so they are safe as file paths.

### 2. Verify dependencies

```bash
which ffmpeg || echo "ffmpeg missing — install with: brew install ffmpeg"
```

You normally do NOT need to install yt-dlp manually. The bundled download script resolves `yt-dlp` in this order:

1. `yt-dlp` on PATH
2. `/agent/.local/bin/yt-dlp`
3. If still missing, it auto-installs into a dedicated venv at `/agent/.local/venvs/yt-dlp` and symlinks `/agent/.local/bin/yt-dlp` — this persists across sandbox restarts.

Auto-install needs `python3` (or `python`) available, which the Buda sandbox provides by default. `ffmpeg` is required for MP3 extraction and is also preinstalled.

### 3. Download source video and audio with the bundled helper

Keep both source video and MP3 audio as user-facing artifacts. Use the bundled script. Resolve its path against this skill directory:

```text
/space/.agents/skills/buda-youtube-to-script/scripts/download-audio.sh
```

```bash
bash /space/.agents/skills/buda-youtube-to-script/scripts/download-audio.sh \
  -o "$WORKDIR" --video \
  "VIDEO_URL"
```

The helper:

- Saves the source video to `$WORKDIR/video/` when `--video` is used
- Saves the MP3 to `$WORKDIR/audio/`
- For YouTube, tries `--cookies-from-browser chrome` first, then automatically retries without cookies
- For non-YouTube sites, tries without cookies first, then retries with cookies

If you prefer to run yt-dlp directly instead of the helper, the equivalent command is:

```bash
yt-dlp \
  --cookies-from-browser chrome \
  -P "$WORKDIR/audio" \
  -o "%(title).180B [%(id)s].%(ext)s" \
  -x --audio-format mp3 \
  "VIDEO_URL"
```

Retry without `--cookies-from-browser chrome` if the browser profile is unavailable.

### 4. Video fallback

If the video was not downloaded in the first pass, or if the UI should show a video artifact, pull the full video:

```bash
bash /space/.agents/skills/buda-youtube-to-script/scripts/download-audio.sh \
  -o "$WORKDIR" --video \
  "VIDEO_URL"
```

This saves the video to `$WORKDIR/video/`. If audio download failed but video exists, extract audio with `ffmpeg`.

### 5. Transcribe with Whisper

Use the Whisper tool on the downloaded MP3 (or other audio file).

- Use `response_format: text` for a clean transcript, or `verbose_json` if timestamps are useful.
- Use `language` only when obvious or requested. For English videos, `en`; for Chinese videos, `zh`.
- Add a short `prompt` if the video has known jargon, creator names, products, or acronyms.

Save the transcript to:

```text
$WORKDIR/transcript.txt
```

If the tool returns JSON, also save `$WORKDIR/transcript.json`.

### 6. Read the talking script template

Always read the bundled template, resolving the relative path against this skill directory:

```text
/space/.agents/skills/buda-youtube-to-script/assets/talking-script-template.md
```

If this file is missing, recreate this structure in the final answer:

```markdown
# Talking Script: [Short title based on the video]

Source: [YouTube URL]
Estimated length: [Estimated speaking time based on the final script]
Angle: [The specific idea this script will focus on]
Audience: [Who this is for]

## Core Idea

[One sentence that captures the point of the video.]

## Timeline

| Time | Visual / Action | Voiceover | On-screen Text | Notes |
|---|---|---|---|---|

## Full Read-Through

[The complete voiceover script without table formatting.]

## Optional Titles

- [Title option 1]
- [Title option 2]
- [Title option 3]
```

### 7. Generate the new talking script

Use the transcript as source material, but do not simply compress it. Create a new script that fits the user's angle and target audience.

Quality bar:

- Start with a punchy hook in the first timeline row
- Make the voiceover conversational and speakable
- Avoid academic summary language like “this article mainly discusses”
- Prefer concrete examples over vague claims
- Keep sentences short enough for spoken delivery
- Keep the timeline realistic for the target duration
- Include concise on-screen text that works as captions
- Include delivery notes such as pause, emphasis, speed, or facial/action cues
- Include 3 title options with different angles
- Mention the source URL in the `Source` field

Respect the template headings exactly unless the user asks for another format.

### 8. Save outputs

Save at least:

```text
$WORKDIR/talking-script.md
$WORKDIR/transcript.txt
$WORKDIR/audio/<downloaded-file>.mp3
$WORKDIR/video/<downloaded-file>
```

The MP3 is a required output unless the source platform truly prevents audio download. Treat the MP3 as a user-facing artifact that should be previewed in the UI.
The source video is also a user-facing artifact for the Buda demo and should be preserved when possible.

### 9. Report back to the user

Keep the final response concise:

- Say the script is generated
- Provide the saved path
- Mention that the source video, MP3, transcript, and script were saved
- If `talking-script.md` should be previewed, first verify it with the Buda send-file script, then include the returned `[send:...]` marker in the reply
- Verify the downloaded MP3 with the Buda send-file script and include the returned `[send:...]` marker in the reply so the frontend UI shows a file card for the audio

Do not write `[send:...]` manually without verifying the file exists first. Do not paste the entire transcript unless the user asks.

## Failure handling

### Audio download fails

Try in this order:

1. Bundled helper (handles cookies + no-cookies retry automatically)
2. Direct YouTube with `--cookies-from-browser chrome`
3. Direct YouTube without cookies
4. List formats with `yt-dlp -F URL` (or `download-audio.sh --list URL`)
5. Download best audio fallback or, only if needed, a video fallback and extract audio with ffmpeg

### Video download fails

If video was optional for the task, skip it and continue as long as audio/transcript generation succeeded.

If the video is private, members-only, age-restricted, geo-restricted, or unavailable, explain clearly and ask the user for access/cookies or another URL.

### Whisper fails

Check:

- Audio file exists
- File is not zero bytes
- Audio format is supported

If needed, convert audio to a clean MP3:

```bash
ffmpeg -y -i "$AUDIO_FILE" -ac 1 -ar 16000 "$WORKDIR/audio/whisper-ready.mp3"
```

Then retry Whisper.

### Template missing

Use the fallback template shown above and tell the user the original template file was missing.

## Example prompts this skill should handle

- `get new talking script https://www.youtube.com/watch?v=abc123`
- `generate a talking script from this YouTube video https://youtu.be/abc123, angled for AI entrepreneurs`
- `download this video and audio, transcribe it, then write a Red Note talking script using the template: https://youtube.com/watch?v=abc123`
- `turn this video into a 60-second short-form script, make it punchy: https://youtu.be/abc123`
