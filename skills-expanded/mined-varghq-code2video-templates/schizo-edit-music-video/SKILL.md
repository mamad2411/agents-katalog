---
name: schizo-edit-music-video
description: >-
  Make a 16-second vertical "schizo edit" AI music video with varg: about 70 hard cuts locked to the beat of a
  generated track, AI stills and a few animated clips in one two-colour look, a random effect per shot (duotone
  invert, mirror, kaleidoscope, pixelate, RGB split, glitch band, halo rings, light rays, double exposure, flash)
  and the track title building one letter per cut at the end. One JSON config holds the music prompt, the look
  line, every still and clip prompt and the edit sections; generate.py makes the media on varg, edit.py cuts it
  locally with ffmpeg. Use when the user wants a schizo edit, a fast-cut AI music video or visualizer, a
  hyperpop/breakcore/phonk edit, a "100% AI generated music video in one prompt", a trailer-style teaser for a track,
  or to remake this Halofall example with their own subject, palette and title. Russian triggers: "шизо-эдит",
  "быстрый монтаж под бит", "клип из нейрокартинок", "сделай такой же клип".
metadata:
  author: vargHQ
  version: "1.0.0"
compatibility: >-
  python3, uv (edit.py declares pillow + librosa inline), ffmpeg, curl. A varg API key for new media
  (VARG_API_KEY or ~/.varg/credentials); the Halofall example downloads its media and needs no key or credits.
---

# Schizo-edit music video

A 16 s, 720×1280, 24 fps music video cut at 3–4 shots per beat. Built as **Halofall**: marble statues, portals and
sacred geometry in violet and molten gold, 69 cuts at 89 BPM, about $5.30 of generation. Watch it:
https://s3.varg.ai/files/72c55813-c0fa-4cf2-9f64-ec4f7ed0e7ae/file_14afb4b8189d.mp4

## Render the example (free, ~1 min)

```bash
bash make.command                      # -> out/halofall.mp4
uv run scripts/edit.py examples/halofall.json --project work/halofall --seed 12 --out out/halofall-12.mp4   # another cut
```

## Make a new one

1. **Ask the user for:** the subject world (what the images show), a two-colour palette, the music genre and tempo,
   the track title. Defaults: copy Halofall's structure and change only those four.
2. **Write the config.** Copy `examples/halofall.json` to `examples/<name>.json`. Remove every `url` field (that is
   what makes generate.py generate instead of download). Change:
   - `title` (the letter-by-letter end title; 4–10 letters reads best),
   - `look`: one sentence appended to every still. It is what makes 26 generations look like one video. Palette +
     genre + grain, e.g. `"surreal sacred dark art, deep violet and molten gold palette, high contrast, cinematic
     lighting, film grain, vertical composition"`,
   - `music.prompt`: genre, BPM, "from the very first second (no intro)", "constant high energy". Ask for 20 s,
   - `stills`: 20–30 items, one subject per prompt, no text in the image. Ids are strings,
   - `clips`: 6–8 of the stills to animate (same `id` as the still). One action + one camera move each, things that
     read in 0.2 s: fire, smoke, lightning, sparks, a crowd, falling feathers, a push into a portal,
   - `sections`: which ids each part of the video draws from and which effects it uses (see below).
3. **Price it, then generate in two steps** so the user sees the stills before any video money:
   ```bash
   python3 scripts/generate.py examples/<name>.json --project work/<name> --only stills   # ~$0.07 each
   # contact sheet: ffmpeg -framerate 1 -i work/<name>/img/%02d.jpg -vf "scale=180:-2,tile=9x3" -frames:v 1 sheet.jpg
   python3 scripts/generate.py examples/<name>.json --project work/<name>                  # music + clips
   ```
   Clips: ~$0.42 each (Seedance 2 Mini 5 s), music ~$0.05. To reroll one still, delete its `url` from the config
   and its file in `work/<name>/img/`, then run again; finished items are never regenerated.
4. **Cut:** `bash make.command examples/<name>.json` (or the `uv run scripts/edit.py …` line). Different `--seed` =
   different cut, no new credits.
5. **Check** before handing over: `ffmpeg -i out/<name>.mp4 -vf "fps=4,scale=150:-1,tile=8x8" -frames:v 1 cut.jpg`
   and look at it. Fix repeats or off-palette shots by editing the section pools, not the engine.

## The config's edit part

`sections` are time ranges (`from` in seconds, each runs to the next one). For each:

| field | meaning |
|---|---|
| `shots` | still ids to draw from. A clip with the same id is used 85% of the time, a random 0.2 s of it |
| `fx` | effects to pick from, one per shot: `none scan rings rays neg mirror kaleido pix rgb glitch flash double` |
| `split` | how a beat is divided, e.g. `[0.25,0.25,0.25,0.25]` = 4 cuts. One list is picked per beat |

Halofall's arc: 0–4 s hook (calmer effects), 4–8 s, 8–12 s hardest (mirror, kaleido, pix, glitch), 12–16 s title
section with whole or half beats. `title_from` sets where the title starts; the first shot is always the first id
of section 0 with a flash.

## Rules

- **Make every image, the music and the title new.** When the user brings a reference video, copy its structure
  (length, cut rate, palette, effect vocabulary, title build), never its footage, song, face or name.
- **No text in generated images.** The only text is the title, drawn by edit.py.
- **Spend only after the stills are approved.** Clips are most of the cost; a stills-only edit (empty `clips`)
  costs about $2 and still works because no shot stays longer than 0.35 s.
- **Never commit media.** `work/` and `out/` are gitignored; put finished media on s3.varg.ai and link it.

## Gotchas

- A plain `negate` turns violet/gold into green/blue. The `neg` effect desaturates and maps the ends with `curves`;
  for another palette change the curves in `fx_chain()` (dark end = shadow colour, light end = highlight colour).
- `double` (screen blend) of two violet frames drifts to magenta. Keep it to one or two per section.
- Generated tracks can run out of energy before their length: check the RMS around `duration` and set `duration`
  to where the energy holds.
- If a varg route is down, switch `models` in the config: any 9:16 image model and any image-to-video model work.
  Failed jobs are not billed; re-running retries only the missing items.
