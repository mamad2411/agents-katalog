---
name: youtube-transcript
description: Fetch the transcript and metadata of a YouTube video. Use whenever a youtube.com/watch, youtu.be, or youtube.com/shorts URL appears and the user wants the video summarized, quoted, searched, or analysed — or asks "what does this video say".
argument-hint: [youtube-url]
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash, Read
---

Fetch a YouTube video's captions and turn them into plain text.

`yt-dlp` lives in the harness tool environment, not on the default `PATH` for hooks, so always
invoke it by its full path: `~/.claude-lsp-tools/bin/yt-dlp`.

## Steps

1. Extract the video URL from `$ARGUMENTS` or from the user's message. Accept
   `youtube.com/watch?v=`, `youtu.be/`, and `youtube.com/shorts/` forms.

2. Fetch metadata and captions in **one** invocation. YouTube rate-limits aggressively (HTTP 429)
   — do not split this into separate calls, and do not retry in a loop if it fails.

   ```bash
   mkdir -p /tmp/yt-transcript
   ~/.claude-lsp-tools/bin/yt-dlp --skip-download \
     --print "%(title)s | %(channel)s | %(duration_string)s | %(upload_date)s" \
     --write-subs --write-auto-subs \
     --sub-langs "en,en-orig,en-US,en-GB" --sub-format vtt --sleep-subtitles 1 \
     -o "/tmp/yt-transcript/%(id)s.%(ext)s" "<URL>"
   ```

   `--sub-langs` is an explicit list on purpose. The glob `en.*` also matches YouTube's
   auto-*translated* tracks (`en-de-DE` and friends), which downloads a dozen redundant files and
   reliably earns a 429.

3. Pick the best track from `/tmp/yt-transcript/`, in this order — human-written captions are far
   cleaner than auto-generated ones:

   `<id>.en.vtt` → `<id>.en-US.vtt` → `<id>.en-GB.vtt` → `<id>.en-orig.vtt`

4. Strip the VTT to plain text:

   ```bash
   grep -vE '^(WEBVTT|Kind:|Language:|$)' "<file>.vtt" \
     | grep -v -- '-->' \
     | sed -E 's/<[^>]*>//g' \
     | awk '!seen[$0]++'
   ```

   Auto-generated captions carry inline `<00:00:01.234><c>` timing tags and roll each line forward,
   so raw VTT runs ~3x the real content.

5. Clean up: `rm -rf /tmp/yt-transcript` (this will prompt; that is expected).

6. Report the metadata line, then the transcript or your summary of it.

## Constraints

- **The dedupe is lossy.** `awk '!seen[$0]++'` removes *all* repeats, not just adjacent ones,
  because rolling captions repeat non-adjacently. A genuinely repeated line — a chorus, a refrain,
  a repeated phrase — collapses to a single occurrence. Good enough for comprehension and
  summarising; **wrong for verbatim quotation**. If the user wants an exact quote, go back to the
  raw `.vtt` and read the cue directly rather than quoting the cleaned text.
- Auto-generated captions contain transcription errors. This video's own auto track renders
  "A full commitment's what I'm thinking of" as "I feel commitments from what I'm thinking of".
  Attribute quotes to the *captions*, not to the speaker, when only an `-orig` track was available.
- If no captions exist, say so plainly. Do not infer content from the title, description, or
  comments and present it as what the video says.
- If the track retrieved is not English, name the language in your answer.
- Captions carry no speaker labels. Do not invent attributions in multi-speaker videos.

## Known failure modes

- `HTTP Error 429: Too Many Requests` — you have been rate-limited. Report it and stop; do not
  retry. It clears on its own.
- `WARNING: No supported JavaScript runtime could be found` — currently harmless, captions still
  download. yt-dlp has deprecated JS-less extraction, so this may become fatal in a future
  YouTube change; the fix is to install `deno` and it is not needed yet.
- `WARNING: ... no impersonate target is available` — harmless for subtitle downloads.
