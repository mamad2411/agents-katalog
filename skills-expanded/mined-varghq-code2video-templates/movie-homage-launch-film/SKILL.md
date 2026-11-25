---
name: movie-homage-launch-film
description: >-
  Make a 45-60 s cinematic launch film for a product, built as an homage to one iconic movie scene, the way varg
  made "I know how" for varg.ai/how-to (The Matrix "I know kung fu" scene: an operator loads a skill into an
  android, it says "I know how to make a music video", "Show me", and it makes one). Original characters, a
  three.js previz with a styled look first, Seedance 2.5 video-to-video per location, on-camera lip-synced lines,
  a music video with a real song inside the film, and every non-AI part (real product UI, a live site scroll demo,
  word-by-word subtitles, the end card from the product's own hero) made in code with HyperFrames. Use when someone
  asks for a launch film, announcement trailer, cinematic product teaser, "make a video inspired by <movie>", a
  movie homage or parody ad, or "make a video like I know how".
license: MIT
metadata:
  author: vargHQ
  version: "1.0.0"
---

# Movie-homage launch film ("I know how")

The example in `example/` is the real film: https://s3.varg.ai/files/194b94d0-58ff-4e8b-91de-4f1959d04013/file_291d768132f5.mp4
(47 s, 16:9, 1080p). `bash make.command` re-renders it from code with no credits. Every prompt is in `PROMPTS.md`.

**Cost of the example:** about $12 for the first cut, about $24 with two rounds of director's notes, on varg.
**Time:** a working day, most of it waiting for video jobs (3-10 min each).

## 1. Ask before anything (one message)

1. The product and the one thing it teaches or does. The film's "loaded skill" moment is that thing.
2. The movie and the single scene to homage. Pick a scene with an instant transformation and a short line people
   know ("I know kung fu", "Show me"). One film, one scene.
3. Format and length: 16:9 for X/YouTube/landing pages, 9:16 for Reels; 40-60 s.
4. Brand kit: colours, fonts, logo SVG, the product's live URL (for the UI insert and the site-scroll demo).
5. Budget ceiling. Quote it from `estimate_cost` on one real request, never from memory.

## 2. Rules for an homage

- Original characters, names and wardrobe. No actors' likenesses, no footage, logos or title cards from the film.
- Change the film's signature colour to the brand's (The Matrix green became varg ember `#FF5315` on `#070708`).
- Keep the rhythm of the scene, not its pixels: the setup, the instant load, the line, the proof, the tag.

## 3. The story pattern (47 s, 14 shots)

| time | beat | source |
|---|---|---|
| 0-4 | wide establishing: the lab, the operator, the agent in the chair | AI (previz → Seedance) |
| 4-6.5 | insert: hands typing | AI |
| 6.5-10.5 | the real product UI: the search and its real answer | code (HyperFrames) |
| 10.5-12.5 | the agent, eyes closed, light sweeps the face | AI |
| 12.5-15.5 | the load: real product previews + the steps flashing, progress bar | code + real previews |
| 15.5-18.5 | eyes open: "I know how to make a music video." (inner voice) | AI + VO |
| 18.5-21 | operator, on camera: "Show me." | AI + lip-sync |
| 21-23 | the construct: white void, one bar, a slate ("TAKE 1") | AI + code |
| 23-32 | the proof: a real music video, one shot per bar, lyrics in code | AI + song + lip-sync |
| 32-34.5 | operator, on camera: "What else?" | AI + lip-sync |
| 34.5-38.5 | product demo: the live site scrolling in a browser window | recorded from the real site |
| 38.5-41 | the agent turns to the lens: "Just ask." | AI + VO |
| 41-47 | end card rebuilt from the product's own hero | code |

The full storyboard with picture/action/camera per shot: `example/storyboard.json`. Characters, colour script,
lines: `example/treatment.md`.

## 4. Pipeline (in this order)

Load these skills first; each step names its source of truth:

- `varg-ai` (models, prices, API). **Run its version check first**: an old copy pointed at outdated models.
  Model ids come from https://varg.ai/models/llms.txt or `varg-ai/references/models.md`, never from memory.
- `varg-previz` (`npx skills add vargHQ/skills --skill varg-previz`; its app and scripts are also in this repo,
  `../varg-previz/`): story → anchors → three.js previz → Seedance v2v packs.
- `varg-music-video` (`npx skills add vargHQ/skills --skill varg-music-video`; its scripts are in this repo,
  `../varg-music-video/scripts/`): song map, beat grid, stills first, lip-sync.
- `hyperframes` (edit, captions, inserts, render).
- How-to pages: https://varg.ai/how-to/make-an-ai-short-film.md and https://varg.ai/how-to/make-an-ai-music-video.md

1. **Storyboard.** Write `storyboard.json` (schema in `varg-previz/references/threejs-previz.md`): id, start, end,
   scene, set, subject, camera words ("MCU, 3/4 left, slow push in"), picture, action (written for the video model),
   line, source (`gen` / `code`).
2. **Anchors.** One character sheet per character on a neutral grey background (front, 3/4, profile, back, face
   close-up), `gpt_image_2_5` or `nano_banana_2_1`. Give a character without a mouth (an android with sculpted lips)
   an inner voice: no lip-sync needed.
3. **three.js previz** (`python3 ../varg-previz/scripts/new_previz.py <project> --aspect 16:9`). Build one set per
   location in `js/sets.js`, animate shots in `js/shots.js`. Copy `example/previz/js/look.js` and wire the
   **Styled look** (procedural textures, materials from the sheets, practical lights; `Y` toggles, `?look=styled`)
   so the director approves the look and the blocking before money is spent. The **Grey look** is what goes to
   Seedance: it copies colour. Check every shot headless (`app.exportFrame(id, t)`), render a styled animatic of the
   whole cut with the edit on top. Example sets: loft, construct, street in `example/previz/js/sets.js`.
4. **Master plates from the previz.** Image-edit a Styled previz render with the sheets ("keep the camera and the
   geometry exactly; mapping: mannequin = the android from image 2 …"). Text-only plates drift (the example's
   android sank into the floor). One plate per location.
5. **Seedance 2.5 video-to-video, one run per location** (`varg-previz/references/seedance-v2v.md`): `pack.json`
   (`example/seedance/pack.json`), `build_pack.py --check`, capture grey clips, build, estimate, test ONE run, then
   the rest. Route `byteplus:dreamina-seedance-2-5-260628`, 720p, billed ≈ 28 credits/s. Check every result: scene
   cuts at the planned frames (`ffmpeg select='gt(scene,0.2)'`), no pass-through, every character still themselves.
6. **Fallbacks that were needed.** BytePlus can be down (401 "API key status is not active") → `fal:bytedance/
   seedance-2.5/reference-to-video` (≈ 47 credits/s). fal refuses photoreal face references → face close-ups on
   `kling_v4` image-to-video from a still (63 credits per 4 s). A light-grey previz head can turn a human bald:
   name the human traits ("a real human woman with silver hair and glasses, no android in frame") in the run notes.
7. **Dialogue on camera.** Voice the line (`eleven_v4`, audio tags in brackets), cut the shot exactly as it plays
   in the edit, lay the line at its offset in a silent track of the same length, run `sync_v3` (video + audio).
   Keep the lip-synced clip's audio in the edit.
8. **The music video inside the film** (the part that looked like slop in the first cut). A real song with vocals
   (`lyria_3_5` or `eleven_music_v2_5`, lyrics in the prompt, exact BPM). Word times with Whisper. One shot per bar,
   hard cuts on the downbeat, no world-morph inside a clip, one camera move per shot, tight framing. Stills first
   (`gpt_image_2_5`), then animate; lyrics drawn in code inside the frame; `sync_v3` only on singing shots, on the
   song slice of exactly the seconds the shot plays. Put the AI in the crew (the android behind the camera) rather
   than in an effect. Refs that work: @anabology (20M views, agent-made, lyrics in the world), @obie (method
   open-sourced as github.com/obie/slopcore), @Kiber_Alla (one-take performance + exact audio slice).
9. **Score.** The music model ignores timestamps in long prompts: make separate cues (tension, the song, the
   ending) and cut between them; duck under every line with a `data-automation` volume lane.
10. **Edit everything that is not AI in code** (`example/edit/index.html`, HyperFrames, one composition):
    - the product's real UI with its real data (the terminal prints the real `/v2/skills/search` answer,
      `example/edit/data/search.json`);
    - the loading montage of real product previews;
    - the product demo: record the live site with `bun record-site.mjs <frames-dir>` (playwright, frame by frame,
      eased scroll), show it in a browser window;
    - word-by-word subtitles (`data-words` = spoken times), the AI character's lines marked with a brand chip;
    - the end card rebuilt from the product's own hero: read the live markup (badge gradient, colours, font sizes)
      with playwright instead of guessing; the example copies the varg.ai/how-to "How to" liquid-metal pill;
    - the brand's fonts (varg: Aeonik for display, Inter for body, Fragment Mono for code, from vargHQ/app);
    - scope bars, film grain, a white pop on the cut to the construct.
    Pin the CLI (`npx hyperframes@<version>`), run `hyperframes check`, snapshot key frames, render.
11. **Final QA.** Transcribe the finished mix (whisper) and check every line and lyric lands where planned; look at
    a frame per shot; report what each step was billed (`get_job_cost`), including discarded takes.

## 5. Files in this folder

| path | what |
|---|---|
| `make.command` | downloads the example's finished clips (`example/assets.json`) and renders the edit → `out/i-know-how.mp4` |
| `PROMPTS.md` | every prompt of the example, verbatim, with model and result |
| `record-site.mjs` | records a smooth scroll of a live site as 24 fps frames (the product demo) |
| `example/storyboard.json`, `example/treatment.md` | the story, shots, characters, colour script, lines |
| `example/previz/` | the three.js previz with the Styled look (`js/look.js`, `js/sets.js`, `js/shots.js`); copy `vendor/` from `../varg-previz/templates/previz/vendor/` |
| `example/seedance/` | the Seedance pack, prompts, requests and job ids |
| `example/edit/index.html` | the HyperFrames edit: inserts, subtitles, lyrics, demo window, end card, mix |
