---
name: deepsearch-transcripts
description: Turns YouTube videos, comments, podcasts, sales videos and video ads into quotable text with its provenance, using published subtitles first and local Whisper as fallback and second opinion. Use for "transcris cette vidéo", "transcribe YouTube", "transcribe podcast", "transcription des pubs", "sous-titres", "VSL transcript", "get the comments", or when research needs people's exact spoken words. Part of In-depth Deep Search.
---

# Transcripts

People say on video what they never write. This skill turns that into text a quote checker can verify.

Read `../_shared/source-access.md`. It needs `yt-dlp` and `ffmpeg`, plus `pip install faster-whisper` for local transcription.

**Paths.** `$IDS` means `<this skill's base directory>/../_shared`. Below, `transcripts.py` stands for `python3 "$IDS/scripts/transcripts.py"`, and the same goes for `ad_media.py` and `bank.py`. Run commands from the dossier folder, `research/<slug>/`.

## Choose the route

| Source | Route | Command |
|---|---|---|
| A YouTube channel | List everything first, then pick | `transcripts.py youtube-list URL --out videos.tsv` |
| YouTube videos | Published subtitles | `transcripts.py youtube-subs ID ID --out notes/transcripts --langs "<lang>,<lang>-orig"` |
| YouTube comments | Top comments | `transcripts.py youtube-comments ID --out notes/comments --max 200` |
| A podcast | List, then pick. Published transcript if the feed has one, otherwise Whisper | `transcripts.py podcast RSS --list`, then `--episodes 0,3 --out notes/transcripts --language <lang>` |
| A landing page | Find what it really embeds | `transcripts.py page-videos URL` |
| Wistia | Published captions | `transcripts.py wistia ID --out notes/transcripts --source-url PAGE_URL` |
| Any video or audio, including Vimeo and Loom | Local Whisper | `transcripts.py media URL_OR_FILE --out notes/transcripts --language <lang>` |
| One key passage | Whisper on a clip, with a wider search | `transcripts.py media URL --start 00:11:50 --duration 45 --accurate --out notes/transcripts` |
| Video ads | From an ad capture | `ad_media.py`, see `deepsearch-ad-intel` |

Find the channel or feed yourself through search. Interviews, testimonials and trade podcasts are the richest sources.

## Rules

1. **Subtitles first, Whisper when it matters.** Local transcription takes minutes on a laptop, so use it for videos with no subtitles and for the sentences your conclusion rests on.
2. **Never correct a transcript.** A quote keeps the words the source produced, errors included. Choose readable passages rather than repairing bad ones.
3. **Keep the label.** Each file has a header: URL, title, date, `KIND` and a note. Carry the label into the report: "automatic subtitles", "local transcription, not corrected".
4. **Check what you quote.** Automatic captions drop words and whole clauses. If a key sentence looks off, transcribe the clip with `--accurate` and compare.
5. **Who is speaking?** A testimonial chosen and published by a seller is a seller's claim. Podcast transcripts can misattribute turns. Flag the doubt.
6. **One owner, one at a time.** A single agent downloads from YouTube per run. Others read `notes/transcripts/`. If you get exit code 3 or 5, stop and report. Never add cookies or rotate anything.
7. **Public content only.** No paid courses, private groups or registration-gated replays.

## Mining a transcript

- Note the timestamp of each passage you keep.
- For a person's story, extract: situation before, with figures; why they acted; what they did, in order; channels; what they say they paid; dated results; difficulties. Mark each as stated by the person, stated by the seller, or absent.
- Search all transcripts for the words you care about: `bank.py lexicon --terms "..." --corpus notes/transcripts`.
- Add usable quotes to the verbatim bank with their URL, so `bank.py verify` can check them against the file.

## Done when

- [ ] Each transcript has a header with its URL and kind
- [ ] Videos without subtitles are in `_no_subtitles.txt`, failures are in `_errors.txt`, and the important ones were transcribed
- [ ] Key quotes had a second pass where the captions looked wrong
- [ ] Any limit met was reported
