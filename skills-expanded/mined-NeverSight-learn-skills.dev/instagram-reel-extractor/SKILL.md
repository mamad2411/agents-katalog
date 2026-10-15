---
name: instagram-reel-extractor
description: Extract transcript, metadata, music, and key frames from Instagram Reels. Use when the user shares an Instagram Reel URL (instagram.com/reel/, instagram.com/p/) and wants the script/transcript, video details, creator info, view counts, comments, music used, or any data from the reel. Also use when the user wants to analyze, repurpose, or reference an Instagram video's content.
---

# Instagram Reel Extractor

Extract the spoken transcript, metadata, music, comments, and key frames from an Instagram Reel.

## Prerequisites

The following must be installed on the user's machine:

- **yt-dlp** — `brew install yt-dlp`
- **ffmpeg** — `brew install ffmpeg`
- **Python packages** — `pip3 install openai-whisper ShazamAPI`

Or run the setup script: `bash setup.sh`

If any dependency is missing, tell the user which ones to install before proceeding.

## Usage

Run the extraction script with the Reel URL:

```bash
python3 scripts/extract_reel.py "REEL_URL"
```

Save the extraction to a specific directory:

```bash
python3 scripts/extract_reel.py "REEL_URL" --save-dir ~/notes/reels
```

For better transcription accuracy (slower, uses more memory):

```bash
python3 scripts/extract_reel.py "REEL_URL" --whisper-model small
```

For raw JSON output:

```bash
python3 scripts/extract_reel.py "REEL_URL" --json
```

Skip frame extraction (faster, audio/metadata only):

```bash
python3 scripts/extract_reel.py "REEL_URL" --no-frames
```

Adjust frame interval (default every 2 seconds):

```bash
python3 scripts/extract_reel.py "REEL_URL" --frame-interval 1.0
```

## What Gets Extracted

- **Original URL** — link back to the source reel (always included)
- **Creator** — username and handle
- **Metrics** — likes, comments count (as of extraction date)
- **Music** — song title, artist, album, genre, Shazam link (via audio fingerprinting)
- **Caption** — the original post caption
- **Hashtags** — all tags from the post
- **Top Comments** — comment text with author and like count
- **Duration** — video length
- **Upload date**
- **Transcript** — full spoken text from the audio, with timestamps
- **Language** — auto-detected language of the speech
- **Key frames** — screenshots extracted every N seconds, saved as JPGs with timestamps

## Output

The script outputs a structured markdown summary with the original reel URL at the top. Present this to the user as-is — do not modify the transcript text itself, though you can clean up line breaks and paragraph flow for readability.

The frame images are saved to a `frames/` subdirectory inside the working directory. When presenting the extraction, use the Read tool to view the frame images so you can describe what's happening visually at each timestamp (talking head, B-roll, text overlay, product shot, etc.).

When `--save-dir` is provided, the extraction is automatically saved as `<creator>-reel-<upload_date>.md`. If a file already exists, a number is appended (e.g., `garyvee-reel-2026-04-08-2.md`).

## Configuring a Default Save Location

To always save extractions to a specific folder, tell Claude: "save reel extractions to ~/my/folder". Claude will pass `--save-dir` automatically on future runs.

## Whisper Model Sizes

| Model  | Speed    | Accuracy | Memory  |
|--------|----------|----------|---------|
| tiny   | Fastest  | Lower    | ~1 GB   |
| base   | Fast     | Good     | ~1 GB   |
| small  | Moderate | Better   | ~2 GB   |
| medium | Slow     | Great    | ~5 GB   |
| large  | Slowest  | Best     | ~10 GB  |

Default is `base` — a good balance for short-form reel content. Suggest `small` if the user reports transcription quality issues.

## Troubleshooting

- **Login required errors**: Some reels may require authentication. Pass `--cookies-from chrome` (or `firefox`) to use browser cookies.
- **No speech detected**: The reel may be music-only or use on-screen text instead of speech. Let the user know.
- **Slow transcription**: Whisper runs on CPU by default. On Apple Silicon Macs, it uses the Neural Engine automatically. For faster runs, suggest the `tiny` model.
- **Music not identified**: Shazam works best with distinct background music. Speech-heavy reels with no music will return no match.
