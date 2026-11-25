---
name: podcast-summary
description: Turn a podcast or interview link into an animated summary video for $0, locally. Whole-sentence clips of the speakers' real voices are cut from the episode (word-snapped, silence-walked, Whisper-checked), and on screen each speaker's real photo cut-out is animated into a talking face from their own voice (JoyVASA + LivePortrait), or shown with their real mouth shapes, or drawn as a code-built mascot. Word-synced captions, a big topic title per scene, stat/ranking/list cards, real stills from the episode, an optional host reaction cam, a cast intro, a -14 LUFS master, a two-face thumbnail and ready-to-post copy. Ships a 2-6 min 16:9 summary and/or a 9:16 Short. Use when the user asks for a podcast summary, recap, animated summary, "toon" or mascot version of a podcast, interview or chat show. An add-on to a make-video project with the snipshorts tools; runs on macOS.
license: MIT
author: TheNoumanDev (https://github.com/TheNoumanDev)
---

# podcast-summary

A podcast link becomes a 2-6 minute 16:9 summary (and/or a 60 s Short) told in the speakers' **own voices**: short, whole-sentence clips cut from the episode, played over an animated stand-in for each person, with your commentary as text only. Every tool is free and local. The only model calls are Hindi → Roman caption transliteration (snipshorts' `tools/podcast/llm.py`: Claude Code by default, or `SNIPSHORTS_LLM`) and your own story picking. Project rules in `AGENTS.md` still apply.

> **Two rules, every run.**
> 1. **AI-animated real faces must be disclosed.** On YouTube set *Altered or synthetic content* to **Yes** (Instagram/TikTok: add the AI label), and say it in the description. kit.py marks `post.json` `"synthetic": true` and puts a warning at the top of `post.md`.
> 2. **Never pitch-shift, speed up or disguise anyone's voice**, and **credit the show by name** (end card, description, pinned comment). It is their real voice or nothing. No source links in the copy (snipshorts' post rules strip them), but the show's name is always there.

| Piece | Where |
|---|---|
| Cut + caption builder | `tools/summary/build.py` (`summaries/<slug>/script.json` → `public/summary/<slug>[-short]/` audio.wav, stills, manifest.json) |
| Composition | `src/compositions/PodcastSummary/index.tsx` (`PodcastSummary`, reads the manifest); register ids in `summaries.ts` |
| People on screen | `MascotKit.tsx`: `cast[who].look` → real photo (AI face or real mouths) or a code-drawn mascot |
| Real mouth shapes / cut-out | `tools/summary/photomouths.py` (YuNet + rembg) |
| AI talking face | `tools/summary/aiface.py` (JoyVASA + LivePortrait, set up with `setup-aiface.sh`) |
| Intro portraits | `tools/summary/faces.py` |
| Cards, end screen, host cam | `Cards.tsx`, `Host.tsx` (colours in `brand.ts`) |
| Thumbnails | `DuoThumb.tsx` (host left, guest right, title in the middle), `ProThumb.tsx` (one face, 3 layouts) |
| Master | `tools/summary/master.py` (one fixed gain to -14 LUFS) |
| Posting kit | `tools/summary/kit.py` + snipshorts' `tools/podcast/postrules.py` |

## 0. Set up (once per project)

1. podcast-summary needs a make-video project with the snipshorts tools. No `tools/make-story.sh`: set one up with the **make-video** skill (its §0). No `tools/podcast/`: add them with the **snipshorts** skill (its §0, steps 2-4). If either skill isn't installed: in Claude Code `/plugin install make-video@zero-dollar-studio` (or `snipshorts@…`) then `/reload-plugins`; in other agents `npx skills add TheNoumanDev/zero-dollar-studio --skill <name>`.
2. **Tell the user what this adds, and wait for their OK:**

   | Download | Size | Used for |
   |---|---|---|
   | rembg, onnxruntime, scipy (into `.venv/`) | ~100 MB | cutting people out of frames |
   | rembg `isnet-general-use` model, on first use | ~180 MB | the cut-out (Apache-2.0) |
   | *Optional* AI talking face: JoyVASA + LivePortrait + hubert weights, torch 2.3.1 | ~1.4 GB weights + ~2 GB packages | natural lip sync from the real voice |
   | The episode, per summary | depends on length | you need the rights to use it |

3. On their OK: `cp -R <skill dir>/template/. <project>/` (adds `tools/summary/`, `src/compositions/PodcastSummary/`, `summaries/example/`; replaces nothing), then `tools/summary/setup.sh`. For AI faces also `tools/summary/setup-aiface.sh` (patched so InsightFace, which is non-commercial, is never downloaded or loaded).

**Ask first:** the cut(s) (16:9 summary, 9:16 Short, or both; do what was asked) and the user's handle for the end card. **Rights:** remind them once that summaries of someone else's show can draw claims; keep clips short and transformative, and credit the show.

## 1. Fetch → `podcasts/<slug>/`

```bash
Y=.venv/bin/yt-dlp; U="<url>"
$Y --skip-download --print "%(title)s | %(channel)s | %(duration)s s | %(language)s" "$U"
$Y --skip-download --write-auto-subs --sub-langs "en,en-orig" --sub-format vtt -o podcasts/<slug>/src "$U"   # Hindi: "hi,hi-orig"
$Y -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]" --merge-output-format mp4 -o podcasts/<slug>/source.mp4 "$U"
.venv/bin/python tools/podcast/vtt_words.py podcasts/<slug>/src.en-orig.vtt podcasts/<slug>/words.json
```

- No captions or HTTP 429: transcribe locally, `.venv/bin/python tools/podcast/transcribe.py podcasts/<slug>/source.mp4 podcasts/<slug>/words.json` (snipshorts).
- If the download comes down video-only (no merge), fetch `-f ba[ext=m4a]` separately and mux with `ffmpeg -i v.mp4 -i a.m4a -c:v copy -c:a aac source.mp4`.
- A `&t=` in the link marks the moment the user wants: build the Short around it. For a long episode fetch only a window (`--download-sections "*480-1500" --force-keyframes-at-cuts`) and note the offset.

## 2. Pick the story

Read the whole transcript in ~30-45 s chunks, then print word timings only around your picks.
- **Long cut:** 6-13 scenes, 2-6 min. Open on the strongest one-liner, then who the guest is, then the episode in order, close on the payoff.
- **Short:** one question → answer arc in ≤ 60 s of voice, 2-4 scenes, hook first.
- **Every line must make sense on its own.** A line starting with So/But/Because/Then or a pronoun needs its lead-in. Read 30 s past every out point and finish the thought; never end a scene on a list or a setup.
- **Who speaks:** captions don't say. Check a frame per line (close-ups, not wide shots) and the conversation's logic; pitch can't separate two similar voices.

## 3. The people on screen

Default: **real photos animated by AI**. Per person (`<who>` = the cast id):

```bash
.venv/bin/python tools/summary/photomouths.py <slug> <who> podcasts/<slug>/source.mp4 <t> auto   # check sheet.jpg
.venv/bin/python tools/summary/faces.py <slug> <who> podcasts/<slug>/source.mp4 <t>              # intro portrait
```

Put the printed `photo` block in `cast[who].look.photo`. photomouths alone gives real mouth shapes switched by loudness (`levels`). For the AI face, after step 5's first build:

```bash
W=work/aiface/<slug>/<who>
.venv/bin/python tools/summary/aiface.py prep public/summary/photos/<slug>/<who>/mouth0.png $W
.venv/bin/python tools/summary/aiface.py voice <slug> <who> $W
AIFACE_CALM=0.3 .venv/bin/python tools/summary/aiface.py run $W $W/voice.wav     # slow: run in the background
.venv/bin/python tools/summary/aiface.py frames $W $W/out/<file>.mp4 <slug> <who>
.venv/bin/python tools/summary/aiface.py block <slug> <who> $W                     # → cast[who].look.photo.ai
```

Then rebuild (step 5). Set `"synthetic": true` in script.json.
- Base time: the person talking in **their own** close-up, eyes open, hands away from the chin; a medium shot keeps the shirt (a tight close-up on a black set loses it).
- At `AIFACE_CALM=1` real faces go wide-eyed; 0.3 keeps them natural with full lip motion.
- Re-cut after AI faces? `aiface.py incr` reuses frames of unchanged lines and voices only the changed ones (→ `ai-<tag>`).
- **Drawn mascots** instead (only when asked): a `look` without `photo` (`skin`, `hair`, `style`, `beard`, `glasses`, `top`, `topStyle`, …, see `MascotKit.tsx`), drawn from this episode's frames, not from memory. Hand-drawn ones go in `MASCOTS` (`Mascots.tsx`). Check everyone before building: add `{ id: "summary-cast-preview" … }` props `{"cast": [...], "looks": {...}}` and `npx remotion still summary-cast-preview out/summary/<slug>/cast.png --props=…`.

## 4. `summaries/<slug>/script.json`

Copy `summaries/example/script.json`. The fields:

- **`cast`**: order = left-to-right seats. Two people: one each side. More: an even row on 16:9; on 9:16 only the speaker and whoever they last spoke with (`listener` for a lone speaker).
- **`scenes[].lines`**: `[who, in, out, "optional caption override"]`, rough times in source seconds.
  - The out point is the **end** of the last word (or its start + 0.08), never its start.
  - Overrides must match the audio word for word, fillers included; tidied captions read as out of sync. They're aligned to Whisper's word times.
  - A one-word interjection over the other speaker gets misheard: drop it. A host aside inside a guest's line goes in its own line.
- **`topic`**: every scene gets one, the big heading at the top (16:9). `*word*` = yellow.
- **`card`**: `stat` / `ranking` / `list` (`Cards.tsx`). `line` + `at` = seconds into that line. Keep a stat's `big` to one short word or number (~8 characters); the rest goes in `label`/`sub`.
- **`context`**: one line of background, shown under the topic for 4 s.
- **`react`, `comment`, `cues`**: your reaction cam and text bubbles. `cues` = `[[line, seconds into it, react, comment]]`. Without a `host` only the bubbles show. With `"host": {"dir": "host", "faces": ["smile", "laugh", "shocked", "thinking"]}`, the cam shows **your own** images from `public/host/<face>.png`.
- **`short: true`** puts a scene in the Short; **`shortLines`** trims it.
- **`stillAt`**: the real frame flashed at the scene start. Check it for the show's own overlays (subscribe pop-ups, ads).
- **`faces`, `intro`, `introShort`**: the cast intro, each real portrait flipping to its animated card.
- **`lang: "hi"`**: Devanagari captions → Roman Hinglish in one agent call, cached in `roman.json`. Add `names` for spelling, `fix` for slips. `--check` WER reads high because Whisper answers in English, so read the heard text.
- **`endNote`**: the show credit on the end screen. **`handle`**: your channel.

## 5. Cut the real-voice clips

```bash
.venv/bin/python tools/summary/build.py summaries/<slug> --check            # 16:9 cut → public/summary/<slug>/
.venv/bin/python tools/summary/build.py summaries/<slug> --short --check    # 9:16 cut → public/summary/<slug>-short/
```

- build.py snaps rough in/outs to whole words, walks each edge into silence (-40 dBFS for 80 ms) without crossing a neighbour word, adds 30 ms fades, 0.25 s between lines and a soft whoosh between scenes.
- `--check` re-transcribes every clip with Whisper (WER per line). Fix every ⚠️ by moving the in/out, or fix the caption with an override or `fix`.
- When Whisper's word end runs late and a clip catches the next words, end the line one phrase earlier.

## 6. Register, render, master

Add the ids to `src/compositions/PodcastSummary/summaries.ts`: `{ id: "summary-<slug>", slug: "<slug>", wide: true }` and/or `{ id: "summary-<slug>-short", slug: "<slug>-short", wide: false }`.

```bash
npx remotion render summary-<slug> out/summary/<slug>/raw.mp4
.venv/bin/python tools/summary/master.py out/summary/<slug>/raw.mp4 out/summary/<slug>/final.mp4
# Short: summary-<slug>-short → raw-short.mp4 → final-short.mp4
```

Look at stills of the final at 100% (hook, a card, a caption, an AI face mid-word, the end screen) before calling it done.

## 7. Thumbnail and posting kit

**Thumbnail:** a `THUMBS` entry in `summaries.ts`, cut-outs in `public/summary-thumbs/<slug>/` (reuse `mouth0.png`: it keeps the shirt; a `bg.jpg` frame for dark layouts).
- `DuoThumb`: host left, guest right, both facing in, ≤ 6 words in the middle; `inset` keeps text off the faces. Pick frames where they look at each other.
- `ProThumb`: one big expressive face (`fo` / `tweet` / `dark`). Make all three for YouTube's Test & compare.
- Set `"thumb"` (and `"shortThumb"`) in script.json to the ids.

**Posting copy:** `post` (16:9) and `short_post` (Short) in script.json: title with hashtags ≤ 100 characters, description (long only), tags, Instagram caption, pinned comment. **Credit the show by name; say the faces are AI-animated.**

```bash
.venv/bin/python tools/summary/kit.py <slug>    # → out/summary/<slug>/ready-to-post/{wide,short}/
```

Never upload or post anything: the user does that, with the synthetic-content label set.

More lessons: [reference/lessons.md](reference/lessons.md). Add your own to `LESSONS.md` in the project after every run.

## Measured costs (M1 Max, 64 GB)

| Step | Time |
|---|---|
| Local transcript, 25 min episode (mlx Whisper) | ~1 min |
| AI face, per person | ~22 s of compute per second of their speech (275 s of speech ≈ 100 min) |
