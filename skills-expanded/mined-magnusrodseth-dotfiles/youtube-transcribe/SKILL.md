---
name: youtube-transcribe
description: Transcribe YouTube videos and extract key information using yt-dlp, optionally pulling verified screenshots of the video's visual explanations. Use when the user shares a YouTube URL and wants to transcribe it, summarize it, extract key points, take screenshots or frames from it, or dump learnings from a video. Triggers on YouTube links (youtube.com/watch, youtu.be) combined with requests to "transcribe", "summarize", "watch", "extract", "key points", "notes from this video", "screenshots", "frames", or "what does this video say".
---

# YouTube Transcribe

Turn a YouTube video into a note. Two tracks: the **transcript track** (always) and the **frame track** (when the video teaches visually). Requires `yt-dlp` and `ffmpeg`.

## Track 1: Transcript

### 1. Metadata

```bash
yt-dlp --print title --print channel --print duration_string --print description "<URL>"
```

### 2. Subtitles

Manual subs first (punctuated, higher quality), auto-generated as fallback:

```bash
cd "$SCRATCH"   # scratchpad dir, not the vault
yt-dlp --write-sub --sub-lang en --skip-download --sub-format vtt -o "yt" "<URL>"
# nothing written? then:
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt -o "yt" "<URL>"
```

Output: `yt.en.vtt`. Other languages via `--sub-lang no`; list them with `yt-dlp --list-subs "<URL>"`.

### 2b. Fallback when captions return HTTP 429

YouTube's caption endpoint (`timedtext`) has a per-IP quota. Once it trips, every caption request returns `HTTP Error 429`, and retries, sleeps, browser cookies and `curl_cffi` impersonation do not clear it (tested 12.11.2026). The audio CDN is not limited the same way. Do not retry captions. Download the audio and transcribe it locally:

```bash
MODEL="$HOME/.cache/whisper-cpp/ggml-base.en.bin"
[ -f "$MODEL" ] || { mkdir -p "$(dirname "$MODEL")"; curl -sL -o "$MODEL" \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin; }
yt-dlp -f "ba/b" -x --audio-format wav --postprocessor-args "-ar 16000 -ac 1" \
  --extractor-args "youtube:player_client=web_embedded" -o "audio.%(ext)s" "<URL>"
whisper-cli -m "$MODEL" -f audio.wav -otxt -of clean -np -t 8
rm -f audio.wav
```

This writes `clean.txt` directly, so skip step 3's script and go straight to the word-count check. Whisper punctuates, so it often lands above the 190 words-per-minute band. Check that the last line matches the video's ending instead. If `web_embedded` returns 403, try the default client or `tv`. Mark quotes in the note as machine transcription. For non-English audio, use a multilingual model such as `ggml-small.bin` with `-l no`.

### 3. Clean into prose

```bash
python3 <skill_dir>/scripts/vtt.py text yt.en.vtt > clean.txt
```

**Use the script, do not hand-roll a `sed`/`awk` pipeline.** A prior version of this skill inlined `awk '!seen[$0]++'`, and when the skill is invoked with a URL argument the `$0` is interpolated with that URL before the agent reads it, so the dedup silently no-ops and every line comes out doubled. The script also decodes `&lt;b&gt;`-style escaped markup, which a plain tag-stripping `sed` leaves as literal text.

**Then check the transcript is complete before writing anything.** Speech runs roughly 130-190 words per minute, so `wc -w clean.txt` divided by the runtime should land in that band:

```bash
wc -w clean.txt   # expect ~130-190 words per minute of runtime
```

Well under it means content was lost, not that the speaker was slow. Confirm by comparing the last line of `clean.txt` against the last cue in the VTT (`grep -o "^[0-9:.]* --> [0-9:.]*" yt.en.vtt | tail -1`); a transcript ending mid-sentence is the tell.

This is not hypothetical. `cmd_text` used `re.findall(r"[^.!?]*[.!?]+", text)`, which only returns chunks *ending* in punctuation and silently discards the tail after the final one. Auto-captions carry almost no punctuation, so the pathological case is a **single stray period**: it stops the `or [text]` fallback from firing while truncating everything after it. On a 19:40 video whose only period came from "...seagull grade 3." at the 10-minute mark, 51% of the transcript vanished and the output still read as a complete, plausible transcript. Fixed in `vtt.py`, but keep the check: a half-transcript is invisible in the output and produces a confidently wrong note.

### 4. Write the note

Summarise in your own words, quote the handful of lines you actually cite, and link into related notes. **Do not paste the entire transcript into the note.** It bloats the vault, and the synthesis is the thing worth keeping. Keep `clean.txt` in the scratchpad for the duration of the writing, then let it go.

## Track 2: Frames

Worth doing when the video explains things **visually**: diagrams, on-screen equations, side-by-side comparisons, UI walkthroughs, charts. Skip for talking-head interviews and podcasts, where frames add nothing.

### 1. Download the video

```bash
yt-dlp -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]" -o "video.mp4" "<URL>"
```

Run it in the background for anything over ~10 minutes; a 29-minute 1080p video is roughly 160 MB and takes a minute or two.

### 2. Map concepts to timestamps

Pick the phrases the speaker says *at* each visual moment, then look them up:

```bash
python3 <skill_dir>/scripts/vtt.py find yt.en.vtt \
    "the blades of the pupil" "more grain in the Iso 800" "Priority Modes exist in the center"
```

Prints `00:03:30 | the blades of the pupil diaphragm opening and closing.` for each hit, and reports misses on stderr so a silent miss cannot be mistaken for a match.

### 3. Extract candidates

Seek a beat or two **after** the phrase; a graphic usually appears as it is being explained, not on the first syllable.

```bash
mkdir -p frames
while IFS='|' read -r ts name; do
  ffmpeg -loglevel error -ss "$ts" -i video.mp4 -frames:v 1 -q:v 2 "frames/$name.jpg" -y
done <<'EOF'
00:03:32|aperture-blades-diaphragm
00:10:14|iso-125-vs-800-grain
EOF
```

Descriptive kebab-case names describing the *content*, never `frame-01`.

### 4. LOOK at every frame before shipping it

**This step is mandatory and is the whole point.** Read each extracted image and confirm it actually shows what the transcript implied. Expect roughly one in five to miss: video cuts away, the graphic has not appeared yet, or the speaker is describing a result rather than showing the control.

For each candidate: keep it, re-extract at a shifted timestamp, or drop it.

**Never ship an unverified frame, and never caption a frame with a claim it does not support.** A wrong screenshot is worse than no screenshot, because a caption lends it false authority. If a concept resists capture after a retry or two, drop it and say so rather than approximating.

### 5. Save and embed

Into a per-video subdirectory, then embed each frame at the exact claim it supports, with a timestamp in the caption:

```markdown
![[three-exposure-tiers.jpg]]
*The three prints he opens with (00:10): underexposed, correct, creatively correct.*
```

For an Obsidian vault: `Attachments/<Video Title - Channel>/`.

### 6. Clean up

```bash
rm -f video.mp4        # the big one; do not leave 160 MB in the scratchpad
```

## Environment notes

- Works in **Claude Code on the web/mobile** as well as locally, provided the environment's setup script installs `yt-dlp` and `ffmpeg` and YouTube is on the domain allowlist. Reading frames back uses ordinary image reading, which cloud sessions support.
- A `403` on the CONNECT verb in cloud is often a **transient proxy failure, not an allowlist error**. Re-run once before debugging configuration; an allowlist rejection fails deterministically every time.
- `yt-dlp` version warnings are safe to ignore. If extraction breaks oddly, update it first, since YouTube changes break old versions regularly.
- Auto-generated subs lack punctuation and speaker labels; infer from context and say so in the note if the quotes are reconstructed.
- Do all downloading and extraction in a scratchpad directory. Only verified, named frames belong in the vault.
