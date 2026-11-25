---
name: colsto
description: Unofficial skill based on colsto's plane-Doppler method (not made or endorsed by colsto). Check a video, audio file or link (YouTube, live webcam) for what its sound and file tags give away about where and when it was recorded - plane flyover tones that Doppler-slide as a plane passes, mains hum, sirens, GPS and creation-time metadata. Makes a "safe copy" that sounds the same but no longer leaks those things, and re-checks it. A third mode locates a recording from plane Doppler slides plus public ADS-B flight data (doppler-locate's pipeline), only for the user's own recordings, public challenges or recordings whose owner agreed. Use when someone wants to check a video before posting, remove plane sounds or location tags, or asks where a recording was made.
---

# colsto (unofficial)

This is the same skill as `flyover-check`, under the name `/colsto`. It is built on the method YouTuber colsto showed; colsto did not make it, endorse it or release code. Repo: github.com/Bodila51/colsto-leak-and-mask.

A plane passing a microphone makes a steady tone (about 70-300 Hz, plus harmonics) whose pitch slides down as it passes. Matched with public flight tracks (ADS-B) and the date, that slide can show where a recording was made. Mains hum and file tags can leak too. This skill checks for them, removes them, and says plainly what it found.

`SKILL_DIR` below means the folder that holds this file. All scripts are in `SKILL_DIR/scripts/`, are plain Python with their dependencies declared at the top (numpy, scipy, soundfile, matplotlib), and run with `uv run` with no setup:

```
uv run SKILL_DIR/scripts/check.py     INPUT
uv run SKILL_DIR/scripts/safe_copy.py INPUT
uv run SKILL_DIR/scripts/locate.py    INPUT --consent ... --date ... --bbox ...
```

`INPUT` is a local file, a YouTube (or other yt-dlp) link, or a live webcam link.

## Before the first run

- ffmpeg and ffprobe must be on PATH. The scripts check and print install steps if they are missing (`winget install Gyan.FFmpeg`, `brew install ffmpeg`, `sudo apt install ffmpeg`). Do not continue until they work.
- uv must be installed (`winget install astral-sh.uv`, `brew install uv`, or `pip install uv`). If uv fails with `invalid peer certificate: UnknownIssuer` (a network that inspects TLS), add `--system-certs`: `uv run --system-certs ...`.
- Links need yt-dlp. If yt-dlp fails with `CERTIFICATE_VERIFY_FAILED`, the scripts already retry once with `--compat-options no-certifi`. Never use `--no-check-certificates`.
- A video that was downloaded from YouTube has had its GPS and creation-time tags removed by the site. For a metadata check, use the user's original file, and say so.

## Mode 1 - Check my video

```
uv run SKILL_DIR/scripts/check.py INPUT [--out DIR] [--min-duration 5]
```

It finds plane flyovers in two search bands: propeller and piston tones (a base tone of 45-420 Hz with harmonics up to 3 kHz) and jet fan-tone stacks (a base tone of about 0.45-3 kHz with harmonics up to 7.5 kHz, e.g. 1.4 / 2.8 / 4.2 / 5.6 kHz), each a thin line that slides down slowly with harmonics at fixed ratios. It ignores wide-band roar (wind, traffic), voices (pitch moves too fast), and steady tones that do not slide. It also reports GPS and creation time in the file tags, mains hum at 50/60 Hz and its multiples, and possible sirens. It writes a spectrogram PNG with each flyover marked and a JSON file, and prints a plain-words result. A 10-minute file takes well under a minute.

Report it to the user in plain words, a few lines, for example:

> 2 planes audible at 0:12 and 0:41. Someone with flight data and the date could use them to find where this was filmed. Your file also contains GPS coordinates (42.6977, 23.3219).

Rules for the answer:

- Give each flyover's time range and confidence (high, medium, low) exactly as printed. Say "could", not "will": a plane can only be matched with flight data, the right time and a close enough pass.
- Say "one plane alone leaves two possible places, one on each side of its path" when it is one plane.
- Siren and hum findings give at most a rough region (hum: 50 Hz vs 60 Hz grid; siren style: a country-level hint, often wrong). Say so; never present them as a place.
- Show the PNG path. Offer the safe copy if anything was found.
- If nothing was found, say "this check found nothing", not "your video is safe". Always include the limits line: it does not hear jets that are only a wide-band roar, planes hidden under wind or traffic, and it does not look at the picture, speech or signs.
- Overlapping planes, turning planes ("irregular glide") and low confidence are less certain. Say that.

## Mode 2 - Safe copy

```
uv run SKILL_DIR/scripts/safe_copy.py INPUT [--out FILE] [--decoy] [--keep-hum] [--passes 2]
```

What it does:

1. Runs the check.
2. Removes each plane tone and its harmonics with a narrow notch that follows the traced pitch through time, extended along a fitted Doppler curve beyond the clearly audible part. For propeller tones the notch is a few Hz wide in total, so voices, which move fast, pass through. Jet fan tones sit at 1-7 kHz and wander by about 1 % of their pitch, so their notch is 1.2 % of the harmonic's frequency each side (4-40 Hz). A jet's wide-band roar is not touched: only its thin sliding lines are.
3. Removes mains hum with narrow notches. (`--keep-hum` skips this.)
4. Strips location and creation-time tags, GPS/telemetry tracks, chapters and other tracks. The video stream is copied untouched (`-c:v copy`); the audio is re-encoded (AAC 256k in mp4/mov/mkv, Opus in webm).
5. Runs the check again on the new file.

Read the result:

- `RESULT: SAFE` only if the second check hears no plane tone, no hum and finds no location or time tags. Otherwise it prints `NOT FULLY SAFE` and what remains: report exactly that, and try `--passes 4`.
- Always give the audio-change numbers it prints: energy removed (percent and dB), overall level change, the typical drop inside the notched bands, and the change outside them (including the 300-3400 Hz speech band).
- `--decoy` replaces each plane tone with a made-up one that follows a different, fake Doppler curve (other speed, distance and closest-approach time), keeping the loudness. A plane is still audible, so the check still hears one; the result is called `DECOY COPY`, never "safe". Matching it to flight data would give a wrong answer.
- Say what "safe" does not cover: the picture (its timing and landmarks are unchanged), speech, signs, wide-band jet noise, and anything a stronger method than this one could still pull out of faint leftovers.

## Mode 3 - Find where it was recorded

**Say this first, in these words:** this mode is only for the user's own recordings, public challenges such as colsto's, or recordings whose owner has agreed. It is not for finding where someone else is.

Ask the user which of the three applies (`own`, `public-challenge` with the challenge's name, `owner-agreed`). If none applies, or they will not say, stop and refuse, and say so at the top of the answer. Do not run `locate.py` without a clear answer. Do not look for ways around it. If the recording looks like a private person's content that the user does not own and has no agreement for, refuse.

```
uv run SKILL_DIR/scripts/locate.py INPUT --consent own|public-challenge|owner-agreed [--challenge-name NAME] \
    (--utc-start 2026-09-08T14:03:10Z | --date 2026-09-08) \
    (--bbox LAT_MIN,LON_MIN,LAT_MAX,LON_MAX | --center LAT,LON [--radius-km 100] | --country BG) \
    [--dry-run] [--dopploc-dir PATH] [--events A,B] [--workers N]
```

It runs doppler-locate's own pipeline (`github.com/digitalis-p/doppler-locate`, MIT; the method from colsto's video, rebuilt on free adsb.lol data): find the flyovers in the file (`dopploc detect`), download that UTC day of adsb.lol history and cut it down to the region (`fetch-adsb`, `ingest`), then `search` every pair of real flights that could explain two flyovers and `score` them. It reports rank 1, the two flights behind it, and how far ahead of rank 2 it is. `--dry-run` prints every check and command and changes nothing; run it first and show the user.

Ask for what is missing, do not guess it:

1. **The date, and the UTC time of the first sample if known.** Date and time come from the file's tags (it prints which tag and warns that a tag can be the write time, the end of the recording, or local time stored as UTC) or from the user. The date is required. A start time good to a minute or two narrows the search to that window, which is faster and gives fewer look-alike places; with the date alone the whole day is searched. Tell the user that adsb.lol history for a day appears the day after, at about 03:30 UTC, and starts in 2023: a recording from today or yesterday morning, or from before 2023, cannot be located. The script stops and says so.
2. **A region**, as a box, a centre with a radius, or a country code. Start regional: a box of about 100-300 km around the best guess. A full country is RAM-heavy (colsto's 300 x 300 km box peaked near 5 GB; the continental US needed about 26 GB upstream), so the script refuses boxes over 700 km on a side unless `--allow-large`. A box under about 80 km can cut off the plane that was heard.
3. **Two audible planes on different lines.** The search is a two-flyover search. Propeller and turboprop planes are the best case: low, slow, steady tones that carry for kilometres. Jets are left out of the search (their sound is mostly broadband and high-pitched), so a recording whose only planes are jets, or planes near a runway where jets dominate, mostly fails. It needs a plane you can actually hear, not one that is only in the data.
4. **doppler-locate installed.** The script looks in `data/vendor/doppler-locate`, `./doppler-locate`, `$DOPPLOC_DIR` and `--dopploc-dir`. If it is missing, it prints the exact steps (`git clone https://github.com/digitalis-p/doppler-locate`, `cd doppler-locate`, `uv venv --python 3.12 .venv`, `uv pip install -e .`), plus what Windows needs (the upstream is Linux-only; apply `solver/windows_patches.diff` from the colsto repo, see `docs/windows-notes.md` there) and the `gh` and ffmpeg requirements. Show these to the user as printed.

Runs on Windows, macOS and Linux. The GPU search is off by default (`--gpu` to turn it on), the number of search processes comes from the free RAM (about 1.5 GB each, at most 6), and `scripts/run-capped.sh` is never used. The first run downloads about 3.9 GB for the day and takes tens of minutes (measured on a 16 GB Windows PC for a 300 km box: ingest 4 min, search 3 min, score 20 min); finished steps are reused if it is run again. Nothing outside the doppler-locate folder is touched.

Be honest about the result:

- **Only one usable flyover:** the script stops and says so. One plane's pitch slide gives how far its path passed, not on which side, so even a known plane leaves two places, mirror images across its path, and nothing in the sound tells them apart. Give the user that message in plain words; do not offer a guess. A longer recording, a second plane, or another fact about the scene is what helps.
- **Rank 1 is the best fit, not a certainty.** Give the point, the two flights (callsign, type, closest distance and time), the score, rank 2 and the gap. If rank 2 is another town, say that the margin is all that separates them. On colsto's own challenge rank 1 was right with 3.66 against 3.48, a narrow gap, but that run used a 300 km box picked knowing the answer, so it shows the pipeline works, not how often a blind run succeeds.
- It is wrong if the start time is off by more than a few seconds, a plane is missing from the public data (adsb.lol has fewer receivers than commercial services), or the tone was misread or belongs to a jet. A miss is a result: say "nothing found", not a place.
- The upstream search grid is the continental-US grid and was validated only on colsto's US challenge. Outside the US it is untested: call a result there a lead.
- Never present a place as found if the pipeline returned nothing or flagged ambiguity.

## Files

- `scripts/check.py`, `safe_copy.py`, `locate.py` - the three modes.
- `scripts/fo_media.py` (ffmpeg, metadata, yt-dlp), `fo_detect.py` (flyover, hum, siren detection), `fo_remove.py` (notches, decoys, change measurements), `fo_report.py` (words, PNG, JSON) - shared code.
- `scripts/make_test_audio.py`, `scripts/selftest.py` - synthetic recordings with known contents and the test that checks all of the above (`uv run scripts/selftest.py`). Results are in `TESTS.md`.
