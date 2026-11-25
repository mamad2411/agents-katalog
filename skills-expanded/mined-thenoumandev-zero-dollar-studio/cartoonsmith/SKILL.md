---
name: cartoonsmith
description: Make voiced cartoon episodes with recurring characters for $0. It covers a series bible (characters, voices, sets), turning the user's character sheets into talking rigs (bust + 8 lip-sync mouth shapes + expressions), scene sets, a multi-character script with simple shot direction, then voice, lip sync (Rhubarb), captions, music, Remotion render and an automatic QA gate. Use when the user asks to make a cartoon, animated series, episode, skit or story with recurring or talking characters, to rig a character for lip sync, or to turn character art into an animated show. Add-on to the make-video skill; runs locally on macOS (Apple Silicon).
license: MIT
author: TheNoumanDev (https://github.com/TheNoumanDev)
---

# cartoonsmith

Turns a cast of characters into voiced, lip-synced cartoon episodes using only free, local tools. It's an add-on to a **make-video** project: it reuses make-video's voice, captions, music, render and QA tools, and adds rigs, a series bible and a data-driven episode composition. Follow the project's `AGENTS.md` (animation purity, `sec()`, folder layout).

## 0. Set up (once per project)

1. If the current folder has no `tools/make-story.sh`, it isn't a make-video project yet. Use the **make-video** skill to set one up first (its §0: it shows the user its download list, about 6 GB, and waits for their OK). If that skill isn't installed, tell the user to install it: in Claude Code `/plugin install make-video@zero-dollar-studio` then `/reload-plugins`; in other agents `npx skills add TheNoumanDev/zero-dollar-studio --skill make-video`.
2. **Tell the user what cartoonsmith adds, and wait for their OK:**

   | Download | Size | When |
   |---|---|---|
   | Pillow + Rhubarb Lip Sync | ~10 MB | always |
   | Rosetta 2 (Apple's Intel translator, for Rhubarb) | small | Apple Silicon, if not installed |
   | Real-ESRGAN upscaler | ~45 MB | optional, `WITH_UPSCALE=1`, for small or blurry art |
   | Indic Parler-TTS | ~5 GB | optional, `WITH_PARLER=1`, only for Hindi or other Indian-language voices; English uses make-video's Chatterbox |

   Ask which language the series is in, so you only offer Parler when it's needed.
3. Copy the `template/` folder that sits next to this SKILL.md over the project, without overwriting anything: `cp -Rn <skill dir>/template/. <project>/`. It only adds files (`tools/*`, `src/compositions/_Episode/`, `series/milo-and-rosa/`, `stories/milo-and-rosa-ep01/`).
4. Register the example episode in `src/Root.tsx`:
   ```tsx
   import { calculateEpisodeMetadata, Episode } from "./compositions/_Episode";
   // inside <>…</>:
   <Folder name="Episodes">
     {/* One per episode; size, fps and length come from public/<slug>/episode.json. */}
     <Composition id="MiloRosaEp01" component={Episode} width={1920} height={1080} fps={30} durationInFrames={300}
       calculateMetadata={calculateEpisodeMetadata} defaultProps={{ slug: "milo-and-rosa-ep01" }} />
   </Folder>
   ```
5. On their OK, run `tools/setup_cartoon.sh` with only the extras they chose (about a minute): Pillow plus Rhubarb Lip Sync. The macOS Rhubarb build is Intel-only, so Apple Silicon needs Rosetta 2 (`softwareupdate --install-rosetta`); without Rhubarb, mouths follow loudness only. Extras: `WITH_UPSCALE=1` (Real-ESRGAN), `WITH_PARLER=1` (Indic Parler-TTS, ~5 GB, gated: the user accepts its terms on Hugging Face and runs `hf auth login` first).
6. Prove it works with stand-in art drawn in code, then show the user `out/MiloRosaEp01.mp4` (13 s, about 2.5 minutes):
   ```bash
   .venv/bin/python tools/make_placeholder_cast.py          # art/milo-and-rosa/<id>/faces.png + poses.png
   POSES="apose wave" tools/rig_character.sh milo-and-rosa milo art/milo-and-rosa/milo/faces.png art/milo-and-rosa/milo/poses.png
   POSES="apose wave" tools/rig_character.sh milo-and-rosa rosa art/milo-and-rosa/rosa/faces.png art/milo-and-rosa/rosa/poses.png
   tools/make-episode.sh stories/milo-and-rosa-ep01 MiloRosaEp01
   ```

## 1. Series bible

One per show: `series/<series>/series.json` (copy `series/milo-and-rosa/series.json`). Every episode reads it, so voices and looks stay the same across episodes.

| Field | What |
|---|---|
| `title`, `style` | Show name; one line of art style, reused in every image prompt |
| `characters.<id>` | `name`, `description` (looks, for prompts), `color` (captions), optional `scale` (kids ~0.85) |
| voice fields | Same as make-video's script characters: `exaggeration`, `cfgWeight`, `refVoice` (a clone: **only the user's own voice or someone who agreed**), or `"engine": "parler"` + `speaker` + `style` (§4) |
| `sets.<id>` | `name`, `description` (for prompts), `image` (`"sets/<id>.png"` in `public/<series>/`, or `null`), `wall`/`floor`/`accent` colours for the flat stand-in |

Edit voices in the bible only. `tools/episode_data.py sync` copies them into each episode's `script.json`.

## 2. Character art → talking rigs

The user makes the art with any image tool **they have the rights to use** (for example Gemini's free tier, or their own drawings). Never ship or reuse someone else's characters. Ask for these sheets per character, all in the bible's `style`, **flat 2D, thick dark outlines, plain white background, no text, no shadows on the page**:

1. **Face sheet** (required): a 4×3 grid of the *same* bust (head and shoulders, facing the viewer), identical size and position in every cell, only the mouth or face changing. Reading order:
   - row 1: mouth closed · slightly open with teeth ("ee", most consonants) · open ("eh") · wide open ("aa")
   - row 2: round "oh" · small pucker "oo/w" · top teeth on lower lip "f/v" · tongue behind top teeth "l"
   - row 3: laughing · angry · shocked · sad
2. **Pose sheet** (optional): 2-4 full-body poses, well apart. Include an **A-pose** (arms 30-40° out with a clear gap from the body, legs apart, nothing overlapping): it's what body animation needs next.
3. **Sets**: one painting per set, same style, **no characters**, eye-level, the middle third left fairly plain (characters stand there), at the video's aspect ratio.

Prompt template (fill in from the bible; full version and fixes in [reference/art.md](reference/art.md)):

> Character sheet for an animated show. Style: {style}. Character: {description}. A 4×3 grid of the exact same head-and-shoulders bust facing the viewer, same size and position in every cell, on a plain white background, no text or labels. Row 1 mouths: closed; slightly open showing teeth; open; wide open. Row 2 mouths: round O; small pucker; top teeth on lower lip; tongue behind top teeth. Row 3 faces: laughing; angry; shocked; sad.

Save the sheets to `art/<series>/<id>/faces.png` (and `poses.png`), then:

```bash
POSES="apose wave" tools/rig_character.sh <series> <id> art/<series>/<id>/faces.png [art/<series>/<id>/poses.png]
```

It splits the grid (`tools/split_sheet.py`), optionally upscales 4× (`UPSCALE=1`, `tools/upscale_cuts.sh`), aligns every face on the closed-mouth face and finds the mouth box (`tools/viseme_align.py`), and writes `public/<series>/cast/<id>/bust/` (`base.png`, `mouth-B…H.png`, `laugh/angry/shocked/sad.png`, `rig.json`) and `poses/<name>.png`. **Look at `base.png` and `mouth-D.png`**, and at the printed mouth box: if a cell was framed differently, the head jumps when the mouth changes. Regenerate that sheet rather than fixing it by hand. White clothes vanish into the white page: rerun with `REMBG=1` (needs `rembg`, see `tools/requirements-cartoon.txt`).

## 3. Write the episode script

`stories/<slug>/script.json` (copy `stories/milo-and-rosa-ep01/script.json`): make-video's story format plus `"series": "<series>"`. Leave `characters` empty; it's filled from the bible. Use make-video's length budget (~2.6 words/s plus pauses) and its writing-for-TTS rules.

Per line, besides `speaker`, `text`, `pauseAfter`, `caption`, `emotion`, `pace`:

| Field | Effect |
|---|---|
| `shot.set` | Change set (a new scene; fades in). Lines without it stay on the current set. |
| `shot.framing` | `auto` (default: a scene opens on a two-shot, then alternates close-up and two-shot), `close`, `two`, `group`, `pose` |
| `shot.with` | The other character in a two-shot (default: the last one who spoke) |
| `shot.cast` | Everyone on this set, left to right (default: order of appearance) |
| `shot.pose` | Pose name for `framing: "pose"` (a full-body cut-out that bounces with the voice) |
| `shot.transitionIn` | `cut`, `fade`, `wipe`, `iris` |
| `expression` | The speaker's face for the line (`laugh`, `angry`…) instead of lip sync: for short exclamations |
| `react` | Listeners' faces, e.g. `{ "rosa": "shocked" }`: the cheapest big laugh |

Speaker `"all"` voices every character together and frames a group shot. For a one-off gag shot, copy `src/compositions/_Episode` and add it in `buildShots`.

**Voices.** Without `refVoice`, every character gets Chatterbox's same built-in voice, so tell the user and offer: their own recording per character, people who agreed to be cloned, or Parler's named speakers. For Hindi and other Indian languages use `"engine": "parler"` with a `speaker` from the [model card](https://huggingface.co/ai4bharat/indic-parler-tts), write the lines in the native script, and put the Roman version in `caption`. Never use macOS `say` voices (their licence forbids commercial use).

## 4. Make it

Register the episode in `Root.tsx` (one `<Composition>` like §0, with its `slug`), then:

```bash
tools/make-episode.sh stories/<slug> <CompositionId>   # check → voice → lip sync → captions → music → render → master → QA
SKIP_VOICE=1 tools/make-episode.sh …                   # iterate on visuals (keeps the lip sync)
SAMPLE=15 tools/make-episode.sh …                      # first 15 s for approval
```

`tools/episode_data.py sync` stops early on a missing character, set, face or pose. Characters without a rig yet show as a labelled stand-in, so the edit can be checked before the art exists.

## 5. Verify and deliver

Do make-video's §4 checks (QA report, WER > 0.2 lines, contact sheet of stills, frames from the MP4, a fresh critic). For cartoons also check:
- **Mouths move and match**: tile the mouth area over one line (`ffmpeg -ss <s> -t 2 -i out/<Id>.mp4 -vf "fps=5,crop=…,tile=6x2" -frames:v 1 out/stills/mouths.png`).
- Every speaker is on screen when they talk, and reactions land on the listener.
- Captions are readable over the busts (≥ 54 px at 1080 wide on phones).

Then deliver like make-video's §5. **Never post or upload anything without explicit approval**, and remind the user to tick YouTube's "altered or synthetic content" label for cloned voices.

## Measured costs (M1 Max, 64 GB)

| Step | Time |
|---|---|
| Placeholder cast + two rigs | ~8 s |
| Voice, 4 lines, cold (Chatterbox load + take check) | ~85 s |
| Lip sync (Rhubarb), 4 lines | ~6 s |
| Render 1920×1080, 13 s | ~37 s |
| Full example from scratch | ~2.5 min |
| Parler, one line, 2 takes | ~40 s including model load |

Lessons from real episodes, and how to add your own: [reference/lessons.md](reference/lessons.md).

**Coming next:** body motion from the A-pose (AnimatedDrawings + MediaPipe Pose) and AI action shots.

---
cartoonsmith is from [zero-dollar-studio](https://github.com/TheNoumanDev/zero-dollar-studio), by [TheNoumanDev](https://github.com/TheNoumanDev), who runs the [@0x45.dev](https://www.youtube.com/channel/UC2ahNqB5F_pp16O27rmlMtA) YouTube channel.
