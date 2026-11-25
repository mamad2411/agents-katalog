name: video-study-notes
description: >
  Turn a lecture or training video into a clean transcript and a study note.
  Downloads captions with uvx yt-dlp, strips WebVTT noise, and writes a
  Markdown summary of the material worth learning. Use when the user runs
  /video-study-notes, or asks to transcribe, clean, or summarize a YouTube
  link, a list of video URLs, or a file that contains them.
---

# Video study notes

Work one video at a time. Cybersecurity training is the usual material. The same steps apply to any lecture.

## Inputs

A URL, several URLs, or a file that contains them. An optional focus sentence from the user ("only the Burp setup", "commands and pitfalls"). When the user gives no focus, decide from the material what a student would need to reuse later.

## Fetch and clean

Run the scripts. Do not reimplement them in the chat.

```bash
python3 <skill-dir>/scripts/fetch_transcript.py URL --out <dir>
python3 <skill-dir>/scripts/fetch_transcript.py --from-file <file> --out <dir> --limit N
```

`<skill-dir>` is the directory of this SKILL.md. Default `--out` is `/tmp/video-study-notes`. Each URL is a separate `uvx yt-dlp` run. The script writes:

- `<dir>/<video-id>/*.vtt` raw captions
- `<dir>/<video-id>/transcript.txt` plain text, with a `[HH:MM:SS]` line every five minutes
- `<dir>/<video-id>/chunks/*.txt` pieces of about 2500 words

`--list` prints the URLs from a file and downloads nothing. Use it to confirm a set before a long run.

If subtitles already exist, clean only that file:

```bash
python3 <skill-dir>/scripts/clean_vtt.py INPUT.vtt OUTPUT.txt --chunk-dir DIR
```

## Read

Read `transcript.txt` when it is short. Read the chunk files when it is not. Do not paste the transcript into the study note or into the repository unless the user asks for the raw text.

## Write the study note

Keep definitions, models, steps, commands, tool settings, numbers, and the conditions where they apply. Drop greetings, audio checks, chat logistics, waiting, and jokes that do not carry a fact. When the user named a focus, keep only what serves it, and say so at the top.

Shape the note for later study:

- title and source URL
- the focus, or one sentence on what the video teaches
- sections by topic
- commands and payloads in fenced blocks
- a short list of what was left out as non-substantive

Write the note where the user asked. If they did not, put it next to the transcript as `study-note.md` inside that video's output directory.
