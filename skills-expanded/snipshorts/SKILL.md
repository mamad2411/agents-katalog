---
name: snipshorts
description: Turn a long podcast, interview or talk (YouTube link or local video) into vertical Shorts/Reels/TikToks for $0, as a free, open-source OpusClip alternative with no watermark. Claude picks 20-45 s hook-first moments, local tools jump-cut dead air and track the active speaker (or split-screen two people), and a Remotion composition adds punch zooms, word-synced keyword captions, motion graphics, a cold-open rewind and SFX, then writes ready-to-post titles, captions and tags. Use when the user asks to clip, cut or make shorts/reels from a podcast, interview, talk, stream or other long video. An add-on to a make-video project; runs locally on macOS.
license: MIT
author: TheNoumanDev (https://github.com/TheNoumanDev)
---

# snipshorts

Turns a long video into vertical Shorts with only free, local tools. The one exception is the thinking: moment picking, the edit plan and the post copy call a logged-in agent CLI (your subscription, no API key): Claude Code by default, or `SNIPSHORTS_LLM=codex`, `gemini` or any command that reads a prompt on stdin (see `tools/podcast/llm.py`). If you are not Claude Code, set `SNIPSHORTS_LLM` to your own CLI before running the pipeline. Project rules in `AGENTS.md` still apply.

> **Always ask first: how many clips?** When the user gives a link or file to clip, ask how many Shorts they want (offer a default from the length, e.g. "5?"). Then pick exactly that many moments and make exactly those. Never choose the count yourself.

## 0. Set up (once per project)

snipshorts sits on top of a make-video project.

1. If the current folder has no `tools/make-story.sh`, it isn't a video project yet. Set one up with the **make-video** skill first (its §0: it shows the user its download list, about 6 GB, and waits for their OK). If that skill isn't installed, tell the user to install it: in Claude Code `/plugin install make-video@zero-dollar-studio` then `/reload-plugins`; in other agents `npx skills add TheNoumanDev/zero-dollar-studio --skill make-video`.
2. **Tell the user what snipshorts adds, and wait for their OK:**

   | Download | Size | Used for |
   |---|---|---|
   | faster-whisper, yt-dlp, OpenCV (Python packages, into `.venv/`) | ~150 MB | transcripts, fetching the source, face framing |
   | YuNet face detector | 230 KB | finding the speaker (no face recognition) |
   | Whisper `small` weights, on the first transcript | ~480 MB | word-level transcript (Hugging Face cache) |
   | The source video, per episode | depends on length | you need the rights to clip it |

3. On their OK, copy this skill's `template/` folder over the project: `cp -R <skill dir>/template/. <project>/`. It only adds files (`tools/podcast/`, `src/compositions/PodcastShort/`, `podcasts/example/`) and never replaces make-video's.
4. Run `tools/podcast/setup.sh`. It installs the packages, downloads YuNet, registers the `PodcastShorts` folder in `src/Root.tsx` and adds media folders to `.gitignore`. Safe to re-run.
5. Check the agent CLI the pipeline calls works in the shell: `claude --version` by default, or the one `SNIPSHORTS_LLM` names.

**Rights.** Remind the user once: they need the rights to clip the source (their own show, permission, or a solid fair-use case). Clips of other people's footage can draw copyright claims.

## 1. Source and transcript

Make `podcasts/<slug>/source.json` (copy `podcasts/example/source.json`). The slug uses only letters, digits and hyphens, because it becomes the Remotion composition id.

| Field | Meaning |
|---|---|
| `url` | YouTube (or any yt-dlp) link. Each moment is fetched again in 1080p, so the 9:16 crop stays sharp. |
| `local` | The full video on disk. Used for transcription, and as the fallback when there is no `url`. |
| `title`, `channel`, `speakers` | Context for the moment picker and the post copy ("Host A interviews B, author of C"). |
| `language` | `en` by default. Anything else turns on `romanize.py` (captions in Latin script). |
| `jumpcut` | `false` keeps every frame (TV or already-edited footage, shouting matches). |
| `split` | `false` turns off split screens (over-the-shoulder studios). |
| `screen` | `false` keeps faceless shots as a plain centre crop. By default a shot with no face (screen recording, slides, b-roll) shows a wide, readable window that follows the cursor, over a blurred fill. |
| `denoise` | `true` cleans hum, hiss and room noise from the speech (ffmpeg's built-in `afftdn`, no model). For phone or laptop-mic recordings. |
| `captionStyle` | `bold` (default: heavy caps, yellow active word), `bounce` (comic font, words spring in, new colour each page: funny clips), or `clean` (sentence case, soft fade: interviews, serious talk). |
| `grade` | Optional ffmpeg filter chain applied once at the cut, e.g. `eq=contrast=1.06:saturation=1.1`. |
| `watermark` | Optional text (your handle), top-left. Empty means none. |
| `endCard` | Optional `{"title": "Follow for more", "handle": "@you"}` end screen (3.5 s). It breaks the Shorts loop, so leave it `null` for loop-first posts. |
| `people` | Optional, for name tags (§3). |

Download the full episode at 720p for the transcript only:

```bash
.venv/bin/yt-dlp -f "bv*[height<=720]+ba" --merge-output-format mp4 -o podcasts/<slug>/source.mp4 <url>
```

Then get word timestamps into `podcasts/<slug>/words.json`, one of two ways:

- **Whisper (default):** `.venv/bin/python tools/podcast/transcribe.py podcasts/<slug>/source.mp4 podcasts/<slug>/words.json` (faster-whisper `small` on the CPU, ~10 min for a 65 min episode; `--lang hi`, `--model large-v3` for accents and noise; `--prompt "<names, jargon or a few lines in the spelling you want>"`, with `--condition` to keep that style past the first 30 s).
- **Platform auto-captions (instant):** for non-English sources, and English ones too, YouTube's auto-captions carry per-word timings. `.venv/bin/yt-dlp --skip-download --write-auto-subs --sub-langs "<lang>-orig,<lang>" -o podcasts/<slug>/src <url>`, then `.venv/bin/python tools/podcast/vtt_words.py podcasts/<slug>/src.<lang>.vtt podcasts/<slug>/words.json`.

## 2. Make the Shorts

One command runs moments → prep → plan → SFX → render → -14 LUFS master:

```bash
PICK=10 tools/podcast/make-shorts.sh podcasts/<slug>     # shortlist 10 scored moments, then stop (see below)
tools/podcast/make-shorts.sh podcasts/<slug> 5          # 5 clips
PLATFORMS="yt ig tiktok" …                               # also <id>.yt.mp4, .ig.mp4, .tiktok.mp4 with each app's encode settings
POST=1 tools/podcast/make-shorts.sh podcasts/<slug> 5   # …plus the ready-to-post folder
SAMPLE=10 SKIP_MOMENTS=1 ONLY=1 tools/podcast/make-shorts.sh podcasts/<slug> 5   # first 10 s of clip 1, for a quick look
SKIP_MOMENTS=1 ONLY=2 …                                 # redo one clip
SKIP_MOMENTS=1 ONLY=1,4,5 …                             # several clips
SKIP_MOMENTS=1 SKIP_PLAN=1 ONLY=2 …                     # keep the plan, re-render after code changes
SKIP_MOMENTS=1 RENDER_ONLY=1 …                          # re-render everything after a composition change
.venv/bin/python tools/podcast/moments.py podcasts/<slug> --count 5 --append   # more moments, none overlapping
```

| Step | Tool | Output |
|---|---|---|
| Moments | `tools/podcast/moments.py` (agent CLI) | `podcasts/<slug>/moments.json` |
| Prep | `tools/podcast/prepare.py` | `public/podcast-shorts/<id>/source.mp4`, `clip.json` |
| Name tags | `tools/podcast/people.py` (only with `people` refs) | `who` per shot in `clip.json` |
| Latin captions | `tools/podcast/romanize.py` (agent CLI, non-English only) | words in `clip.json` |
| Edit plan | `tools/podcast/plan.py` (agent CLI) | `public/podcast-shorts/<id>/plan.json` |
| SFX | `tools/podcast/sfx.py` (synthesised, no samples) | `public/podcast-shorts/<id>/sfx.wav` |
| Render | Remotion `PodcastShort` (folder "PodcastShorts" in Studio) | `out/podcast-shorts/<slug>/<id>.mp4`, `.sheet.png` |
| Posting kit | `tools/podcast/post.py` (agent CLI, `POST=1`) | `out/podcast-shorts/<slug>/ready-to-post/NN-<name>/`: `video.mp4`, `thumbnail.jpg`, `post.md`, `post.json` |

Clip ids are `<slug>-<n>`. `make-shorts.sh` adds them to `src/compositions/PodcastShort/clips.ts`.

**Let the user choose (recommended).** Run with `PICK=10` (or `moments.py podcasts/<slug> --shortlist 10`): it writes `moments.candidates.json` and prints a numbered table with the total score and the five sub-scores (hook, standalone, emotion, value, payoff), the times, the title, why it works and its first and last words. Show the user that table and ask which to make. Then `moments.py podcasts/<slug> --keep 2,5,7` (add `--append` to keep earlier picks) writes `moments.json` and adds the cold-open teasers, and `SKIP_MOMENTS=1 make-shorts.sh podcasts/<slug> 3` renders them.

**Review every new moment before rendering.** Print its first and last words. The picker sometimes ends on a setup line or a filler ("right and"), and a teaser can flip the speaker's meaning out of context. Fix it by editing `segments` / `start` / `end` in `moments.json` (snap with `moments.find_phrase`), re-pick a teaser with `moments.py podcasts/<slug> --teaser <n>`, then rerun with `SKIP_MOMENTS=1 ONLY=<n>`. The user may also pick moments themselves from a ranked list; write `moments.json` by hand then.

## 3. What each piece decides

- **moments.py**: hook in the first sentence, self-contained, ends on the payoff, 20-45 s; never intros, subscribe asks or sponsor reads. Each pick is scored 0-10 on hook (30%), standalone (25%), emotion (20%), value (15%) and payoff (10%), and `score` is the weighted 0-100 total. The agent returns `first_words`/`last_words`, and the script snaps them to word timestamps (`UNSNAPPED` means check the cut by hand). When the payoff comes too late for one take, a moment has `segments` (setup → turn → payoff, middle skipped); the composition flashes and the SFX whooshes at each splice.
- **Cold open** (on by default): a 2-5 s `teaser` from inside the moment plays first, then a tape rewind ("⏪ HOW IT STARTED") into the story. `--no-teasers` skips it.
- **prepare.py**: silences over 0.45 s between words shrink to 0.12 s (jump cuts; framing alternates 1.0/1.12 at each cut so they read as edits). Faces come from the YuNet detector every 3rd frame. A shot change is a colour-histogram jump, a whole-frame change, or a face-size change held for 3 samples. A shot with two confident, similar-sized faces for ≥ 60% of it becomes **split** (left person on top). Other shots follow the active speaker (lower-face motion minus head motion). `--retrack` redoes tracking on the existing cut.
- **plan.py**: every beat is anchored to a word index, so timing is word-accurate. 5-10 zooms (punch/push), 4-7 graphics (kinetic slam, stat, emoji, callout, quote), 2-5 accent `fx` (spark burst, confetti, smoke puff, glow ring, or an underline/circle/arrow/check drawn on around the captions, `FxLayer.tsx` + `src/components/Fx.tsx`, each with its own sound in `sfx.py`), 8-16 emphasised words, the hook card, and caption `fixes` for misheard words (the original stays in `asr`). The script enforces: nothing over the hook (first 2.6 s) or the rewind, never two graphics at once.
- **Name tags** (optional): name + role slides in on each person's first appearance. Identity comes from **clothing colour under the face, never face recognition**. Once per source: add `people` (`key`, `name`, `role`) to source.json, run `people.py <clip-id> --sheet out/people.jpg`, look at it, then `people.py <clip-id> --label s0.0=host s3.0=guest`. After that, make-shorts.sh names every shot. Only tag people whose identity the user has confirmed. When unsure, drop the tag.
- **House style** (`podcasts/STYLE.md`, optional): the user's standing notes, added to the moment and edit-plan prompts, where they override the defaults. When the user gives feedback that should stick ("fewer zooms", "no emojis", "prefer funny moments"), append a one-line note there and say so.
- **Captions** stay off faces: below the chin, or above the head when the face fills the lower frame. On screen shots they sit under the window.
- **PodcastShort** (`src/compositions/PodcastShort/`): `camera.ts` (crop, zoom, split panels), `Captions.tsx` (3-word pages, active word yellow, emphasis green and bumped), `Overlays.tsx` (graphics), `FxLayer.tsx` (accent effects at the captions), `Rewind.tsx`, `NameTags.tsx`, `Watermark.tsx`, `EndCard.tsx`, `index.tsx` (layers, hook card, progress bar, SFX). Props `watermark`, `endCard` and `captionStyle` override source.json for one render.

## 4. Verify before delivering

1. `.venv/bin/python tools/podcast/trackviz.py <id> out/track.jpg 12`: the yellow 9:16 window must sit on whoever is speaking in single shots. Look at it.
2. Stills at each beat: `npx remotion still <id> out/stills/f<N>.png --frame=<N> --scale=0.4`, hstack them, and look: text size, faces covered, captions against graphics and name tags.
3. The `.sheet.png` from the final MP4, plus loudness: `ffmpeg -i <mp4> -af ebur128 -f null -` (about -14 LUFS).
4. Check every hook card, quote and title for names: keep them neutral unless the speaker is on camera saying the line.

## 5. Deliver

Give the user the MP4s (or the `ready-to-post` folder with `POST=1`), each with its title, caption and tags. `post.py` only writes local files; **never upload or post anything** without the user's explicit approval. Default copy rules (edit `tools/podcast/postrules.py`): hashtags at the end of the YouTube title, at most 100 characters; no description for Shorts; no links anywhere; Instagram/TikTok caption = one hook line + 15-25 hashtags.

## Rules that save hours

- **One render at a time.** The pipeline passes `--timeout=180000 --concurrency=2`.
- A 1080p section fetch can hang (ffmpeg stuck, no timeout). If one clip's prep takes over 5 minutes, check `raw.dl.mp4.part`; kill the stuck ffmpeg and prepare.py falls back or retries.
- A 1080p fetch can fail on rate limits and fall back to the 720p local copy. prepare.py prints a WARNING; check the "WxH" in its output.
- Re-tracking a clip wipes its name tags; prepare.py reruns people.py when references exist.
- Prompt templates use `str.format`: double every literal brace (`{{index, word}}`).
- In Claude Code, `rm` on `$VAR` paths is blocked by the safety check: write `"${VAR:?}"`.

More lessons, and how to add your own: [reference/lessons.md](reference/lessons.md).

## Measured costs (M1 Max, 64 GB)

| Step | Time |
|---|---|
| Word transcript, 65 min episode (faster-whisper small, CPU) | ~10 min |
| moments.py (~10k-word transcript) | ~1 min |
| prepare.py (1080p section fetch + jump cuts + tracking, 45 s clip) | ~70 s |
| plan.py | ~40 s |
| Render 43 s at 1080×1920 | ~2 min 40 s |

---
snipshorts is by [TheNoumanDev](https://github.com/TheNoumanDev), from [zero-dollar-studio](https://github.com/TheNoumanDev/zero-dollar-studio). Its author runs the [@0x45.dev](https://www.youtube.com/channel/UC2ahNqB5F_pp16O27rmlMtA) YouTube channel.
