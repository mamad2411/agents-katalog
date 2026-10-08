# Fram Agent Skill

Fram is a compact media workshop for the terminal, API, and Telegram. The current primary surface is the `fram` CLI, backed by the same typed processing core used by the API and bot.

Use Fram when a user wants to inspect, resize, crop, compress, convert, rotate, flip, blur, grayscale, trim, re-time, or extract media from local image/video files.

## Requirements

- Python 3.11+ for source installs.
- FFmpeg and FFprobe on `PATH` for video work and most metadata/probe flows.
- Prefer the strict CLI commands for automation. Use interactive mode only when the user explicitly wants a TUI.

## Install

From a checked-out repository:

```bash
scripts/install.sh
```

From a Git URL or future package source:

```bash
scripts/install.sh --from git+https://github.com/Sergio-prog/fram.git
```

The script prefers `uv tool install` and falls back to `pipx`, which keeps the global CLI isolated from project environments.

## CLI Basics

Show help:

```bash
fram --help
fram help resize
fram resize --help
```

Inspect media:

```bash
fram info input.jpg
fram info input.mp4
```

If `-o/--output` is omitted, Fram writes a generated output path next to the input. For agent workflows, usually pass `-o` explicitly so the result path is predictable and no existing user file is surprised.

## Image Commands

```bash
fram resize input.jpg 128x128 -o output.jpg
fram crop input.jpg 128x128 --anchor center -o avatar.jpg
fram compress-image input.jpg --quality 80 -o compressed.webp
fram convert input.png webp -o output.webp
fram rotate input.jpg 90 -o rotated.jpg
fram flip input.jpg --horizontal -o flipped.jpg
fram strip-metadata input.jpg -o clean.jpg
fram blur input.jpg --radius 2 -o blurred.jpg
fram grayscale input.jpg -o gray.jpg
```

## Video Commands

```bash
fram cut input.mp4 --start 00:00:05 --end 00:00:12 -o clip.mp4
fram cut input.mp4 --start 5 --duration 10 -o clip.mp4
fram fps input.mp4 24 -o video-24fps.mp4
fram compress-video input.mp4 --crf 24 --preset medium -o smaller.mp4
fram strip-audio input.mp4 -o silent.mp4
fram extract-audio input.mp4 -o audio.m4a
fram extract-frame input.mp4 --at 00:00:05 -o frame.png
fram gif input.mp4 --fps 12 --width 480 -o clip.gif
fram speed input.mp4 2 -o fast.mp4
fram reverse input.mp4 --no-audio -o reversed.mp4
fram grayscale input.mp4 -o gray.mp4
```

## Interactive Mode

```bash
fram
fram input.jpg
fram input.mp4
```

Interactive mode is a Textual TUI with previews when the terminal supports image protocols. It is useful for manual exploration, not for repeatable agent automation.

## Agent Guidance

- Do not edit `.env.*` files unless the user explicitly permits it; `.env.example` is okay.
- Check `fram info` before lossy or timing-sensitive edits when dimensions, duration, FPS, or codecs matter.
- Prefer explicit output paths and avoid overwriting user inputs.
- For destructive-looking operations like compression, stripping metadata, or audio removal, write to a new file unless the user asks otherwise.
- Validate important results with `fram info`, file existence checks, or targeted tests.
- Mention FFmpeg if video commands fail with missing binary, codec, or probe errors.
