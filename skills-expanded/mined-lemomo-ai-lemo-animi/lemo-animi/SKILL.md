---
name: lemo-animi
description: Make a stop-motion animated short with lemo-animi in a fixed material style. Prepare and verify the environment first, then ask for all missing choices together, starting with the full style menu. Your first reply names no story, theme, title or project folder; defer every creative decision until each choice is answered or explicitly delegated. Use when the user says "用 lemo-animi 做…" or "make … with lemo-animi", or asks for a stop-motion, claymation or cartoon short (定格动画、黏土动画、动画短片、做个会动的小片子), including a story or character to animate. For photorealism see references/realism.md. Excludes animating a single existing image and editing existing video.
---

# lemo-animi: a stop-motion short from one line

**Image generation makes it look right; code makes it move.** Every style has fixed prompt templates; you only fill the slots (character, action, scene). Assets are transparent PNGs, sliced and composited shot by shot in Python (on twos, anchors, camera, transitions, grading, subtitles). Sound comes from one sound sheet: score, foley, optional narration, mix.

**Read files whole.** A tool output may be cut short: read instruction files over ~120 lines in chunks (`sed -n '1,120p' <file>`, then the rest); never act on a truncated read. Raw logs, long cue lists and review notes: pull out the relevant lines locally (`grep`, `tail`) or read them page by page until every entry is covered; never print encoded data.

## 1. Talking to the user

**Language.** The skill is in English. Talk to the user in the language they write in, whatever it is (questions, options, every progress note between tool calls, review-page replies, report). If nothing shows it (no words from the user and no language set by your own instructions), ask that alone first (item L), then everything else in the chosen language.
- **The film's own text** (narration, subtitles, title and end cards) is Chinese or English: Chinese for a Chinese-speaking user, English for everyone else unless they ask for Chinese; when the user writes neither, the narration question says so. Set it with `init_film.py --lang zh|en` (it goes into `sound.json` `"lang"`, `references/sound.md`).
- **The review page**: `review.py add … --lang <the user's language code>` (zh, en, ja, …): Chinese gets the Chinese page, every other language the English page.
- **Style list**: `animi.py styles --lang zh|en`; for other languages use `en` and translate the one-liners.

| Item | Default and handling |
|---|---|
| Story | May be just a title. **Write the full story yourself** in the story skeleton for its length (directing §1: setup, tries, low point, turn, payoff; beats, side characters, narration); don't ask back. A given plot: follow it, fill the skeleton's missing parts with beats and shots. A character image (their original character, a pet): generate the character sheet from it in this style's material and match every sheet to it. No real faces or franchise characters: steer to an original. |
| Style | Fixed styles only (`animi.py styles`; Chinese name, English name or id). Off the list: say it's experimental; if they insist, `references/new-style.md`. Photorealism: `references/realism.md`. |
| Length | 40 s; options 20 / 40 / 60 s, or any length the user types from 20 s to 2 min. **The final film's length, title and end cards included.** Over 60 s: before starting, tell the user roughly how many images and how long it takes (§3 table). |
| Size | landscape 1920×1080 / portrait 1080×1920 / square 1080×1080. |
| Narration | Off (score + foley, no subtitles). On: lively female or child voice, subtitles in the film's language; bilingual subtitles on request. Needs network (edge-tts sends the narration text to Microsoft): if `sound.py vo` can't connect, request access with the justification it prints; if refused, make the film without narration and say so. Never a local offline voice. |
| Preview | Off: work straight through. On (or the user sent a character image): show character sheets and main backgrounds once on the review page, continue after approval. |
| Title and end cards | Off. On: title and credit come in the same question. No title given: title it from the story and say so in a progress note. Never invent a credit. Each card is 3 s, so the story runs the length minus 6 s. |

**Prepare the environment before asking anything.** Run `sh "$S/setup.sh" check` in the current directory. If anything is missing, immediately run `sh "$S/setup.sh"` to install missing dependencies and samples or wait for an existing install. Tell the user a first install takes about 1.7 GB. It needs the network and writes `~/lemo-animi-env` (Codex: request escalated permission; never point `LEMO_ANIMI_*` at a temp folder to get around it). Wait for the process to finish (§2), then run `check` again. If setup fails or a prerequisite still needs user action, report the specific blocker and resume here after it is resolved (workflow §0): ffmpeg missing → the user installs it (macOS `brew install ffmpeg`, Linux the package manager); in Claude Code, `check` also reports the image tool: neither Codex CLI nor an adapter → the user installs and logs in to Codex (`npm i -g @openai/codex`, then `codex login`); no zsh (some Linux) → the user installs zsh. In Plan mode, if setup requires writes the mode disallows, ask the user to switch to default mode before continuing.

**Collect the missing film choices together.** Use the checklist below in order, in the user's language. Include only items the user has neither answered nor explicitly delegated. Until all items are settled, keep progress notes to setup and intake. Defer choosing the story, title or style, naming or creating the film folder, reading the style package and drafting the plan.

- **Codex App and interactive CLI, default mode.** Use one `request_user_input_async` call with one entry per missing item in its `questions` array. Each style gets its own option, formatted as “Style name｜One-line description”. Use catalog order. If the user already supplied a story, move the best match to the front and mark only that option “Recommended” in their language. Without a story, leave all styles unranked. Omit `options` for the story to show just the input box. Put the applicable default first for other choices. End the turn immediately after dispatch and wait for the user's reply.
- **Codex Plan mode.** Use one synchronous `request_user_input` call if all missing items fit its limits (up to three questions, two or three options each). Otherwise use the numbered text questionnaire below so the user can answer everything together.
- **Claude Code.** Use consecutive `AskUserQuestion` calls in checklist order, up to four missing items per call and two to four options per item. Collect each batch's response before sending the next, with no production work between calls. When the style menu exceeds four options, put the complete catalog with descriptions in the style question itself. Offer up to three representative styles and “You decide” as buttons. The built-in free-text field accepts any listed style by name or number. For the story, invite the user's own words there. Where buttons are required, offer “You decide” and “Leave open for now” without suggesting plots or titles. Mention once that auto mode (Shift+Tab or `claude --permission-mode auto`) can reduce approval prompts during production; never suggest skipping permissions.
- **Plain text** (`codex exec`, unknown client or no suitable question tool). Put all missing questions in a single final reply, numbered 1, 2, 3… with each question's options numbered or lettered under it, so the user can answer "1: 4, 2: a story…", including the full style menu with descriptions whenever style is open. Invite the user to answer by question number and end the turn. In `codex exec`, the caller can reply with `codex exec resume`.

**Check the answers before starting.** Match submitted answers to the checklist, including any choices supplied earlier. If a submission is partial, ask again for just the unresolved items together. If replies arrive in installments for an open panel, keep the answers already received and let the user finish it. Dispatch acknowledgments, preselection, silence and skipped items supply no answer. Apply a default or choose for the user only when their reply authorizes it.

```
L. Language, only if unknown: ask which language to use after setup, before the film questions.
1. Style: run "$PY" "$S/animi.py" styles --lang zh (or en). Show every style with its one-line description in the user's language. Ask which they want.
2. Story: "What story do you want to tell?" Accept a title or one line in the user's own words. Offer no examples, suggested titles or placeholder options.
3. Length including cards: 40 s (default), 20 s, 60 s, or a typed duration from 20 s to 2 min.
4. Size: landscape (default), portrait or square.
5. Narration: none (default), lively female or child voice. Accept bilingual subtitle requests.
6. Title and end cards: off (default) or on. Invite an optional title and credit in the same answer.
7. Preview characters and backgrounds: off or on (default off, on for a supplied character image).
8. Anything else? Accept wishes, a character image or "none" (default).
```

Once all items are answered, apply any choices the user delegated, read the selected style package and carry the answers into the director's plan. In Plan mode, have the user switch to default mode to make the film with those answers. Work through to delivery with short progress notes and the requested preview.

## 2. Work until it passes

- **Before the director's plan read**: `styles/<id>/STYLE.md`, `references/directing.md`, `references/quality.md`, `references/pitfalls.md`. Other docs at the step that needs them.
- **Long commands**: `setup.sh` (first run), `gen.sh` (up to 10 min per image), full renders and `review.py wait` (30 min) outlast a default tool timeout. Codex: keep polling the running command. Claude Code: its Bash tool stops a command at 10 min, so run `setup.sh`, full renders and `wait` with `run_in_background: true` and carry on when it reports back; give each `gen.sh` call a 600000 ms timeout or run it in the background.
- **Aim to pass, not to be fast**: images and time per length are in the §3 table (40 s: about 20–26 images and an hour or more). Below the asset minimums it is unfinished.
- **A failed check, bad slice or off anchor changes the plan, it doesn't stop you**: look it up in the handling table in `quality.md` (`--allow-edge`, `--clean`, `--group grid` pass after you check the image). Regenerate only real defects (max 3 times per image, one change each time), or split / recompose.
- **The first render is not the delivery.** Watch the whole film through still images: the `selfcheck.py` sheets and consecutive frames at every cut and contact. Clear the `sound.py check` warnings and the render's `liveness` warnings (fix, or list each with its reason in `review.py add --known`). You do not listen yourself (hard rule 14): write "not listened" and check what can be measured (`sound.py check`; each landing or impact sound on the drawing where it lands, `sound.py times` beside the contact frames; stems in `audio/`). Write a verdict with timecodes for each must-pass item in `quality.md`, fix, review again. What you didn't watch or hear is "not checked", never "pass".
- Edit `tools/film.py` one change at a time with the edit tool (Codex: apply_patch); batch string replacement silently hits other places.
- **Permissions the film needs**: the review page (every film) needs a local port, narration needs the network for the voice service; Codex's sandbox counts both as network access, and some Codex permission modes refuse every escalation. Once all choices are answered, before generating anything, test both: `"$PY" -c "import socket; socket.socket().bind(('127.0.0.1', 0))"` for the port, and, with narration, a request to the voice service. If either is refused and can't be escalated, ask the user to allow them, naming both in one message. If it is only refused later, never drop the choice quietly: stop, tell the user what is blocked and how to allow it (in Codex, a permission mode that allows network access or approval requests; then say "continue"), and wait. Go on without it only if the user says so, and say so in the report.
- **Blocked**: permission denied or a tool unavailable (network, quota, system software): finish everything else, report honestly, never work around it. Image generation timeout or rate limit (429): do what doesn't need that image, retry in a few minutes; no placeholders at delivery. Any other image generation error (bad request, unsupported parameter, refused by a gateway) usually comes from the user's own setup: show the exact error, do the work that needs no images, ask how to proceed. Never read credential or config files, never switch image tool or model on your own.

## 3. Workflow (same for every style)

Commands and folders: `references/workflow.md` (also the tools list and the review page). Functions: `references/api.md`.

| Step | What | Read |
|---|---|---|
| 0 | `$S` = absolute path of the adjacent `scripts/` folder. Check the environment, install missing components, wait and verify (§1). Set `$PY` from `sh "$S/setup.sh" python`. Collect all missing choices together (§1). Proceed only when every item is answered or explicitly delegated. | workflow §0 |
| 1 | Style package: `STYLE.md`, `style.json`, `ref/` and `poster.jpg` where present | |
| 2 | **Director's plan** in `production-log.md`: logline, story skeleton with seconds per part, beat sheet, narration, shot list, layered action table, image list | directing |
| 3 | **Timing**: with narration, write it in `sound.json`, `sound.py vo` gives line lengths, shots follow; without, seconds per beat (a beat is 2–4 s and holds several events) | sound |
| 3′ | `"$PY" "$S/init_film.py" <film folder> --style <id> --dur <story seconds> --size <landscape|portrait|square> --name <name> --lang <zh|en>` (creates the folder; run everything after inside it) → write `SHOTS` + `build()` → `film.py lint` | compositing |
| 4 | Images: slot file → `animi.py prompt` → generate. Character sheets and 1–2 key backgrounds first; check palette and character. Codex: built-in image_gen, references in `referenced_image_paths`, `transparent_background: true` for transparent assets, copy from the returned path | prompts, workflow §4 |
| ⏸ | Preview (only if on): register, wait for approval | workflow, review page |
| 4′ | Other backgrounds → `load()` → `film.py board` (open the `board_p*.jpg` pages); shots connect | |
| 4″ | Action sheets, close-up sheets, props, fx; set layers and textures if needed | |
| 5 | `animi.py check` → `slice` → `anchors` | workflow §4 |
| 6 | Real assets into `load()` / `render()`; `put()` applies the style's light; transition assets load from `style.json` | compositing |
| 7 | Sound: score, hits, foley (times per shot, `"shot+0.4"`; per-cell sounds via `foley_rules`) → `sound.py lint` → `build` | sound |
| 8 | lint → stills → full film → contact sheet → consecutive frames → `selfcheck.py` → must-pass items → fix → again; then bookends if on | quality |
| ⏸ | Review page: register, the user writes notes, fix, register again until approved | workflow, review page |
| 9 | Deliver (§5) | |

**Asset minimums** (short of them, the plan is underthought: split the beats again):

Columns are the film length; for other lengths take the nearest column, scaled.

| | 20 s | 40 s | 60 s | 90 s | 2 min |
|---|---|---|---|---|---|
| Shots (typical, never padded) | 2–4 | 5–8 | 6–12 | 9–16 | 12–22 |
| Backgrounds, **each a different view**, not the same composition enlarged | ≥ 2 | ≥ 4 | ≥ 6 | ≥ 8 | ≥ 10 |
| 8-cell action sheets, **one per action** | ≥ 3 | ≥ 5 | ≥ 7 | ≥ 10 | ≥ 13 |
| 2×2 close-up sheets (key reaction, payoff) | ≥ 1 | ≥ 2 | ≥ 3 | ≥ 4 | ≥ 5 |
| Prop / fx sheets | as needed; at least one fx sheet for landings and impacts | same | same | same | same |
| Total images | ~10–14 | ~20–26 | ~30–38 | ~42–52 | ~55–68 |
| Rough time | under an hour | about an hour | 1.5–2 h | 2–2.5 h | 2.5–3 h |

A prop acting alone (a lamp lights itself, a boat drifts) is prop images + fx sheets, not an action sheet.

## 4. Hard rules (details in the docs named)

1. **Fixed styles only**: every prompt from `animi.py prompt`, no style text of your own; compositing parameters from `animi.style_preset` / `animi.finish`; no hand grading.
2. **Transparent assets**: character, action and close-up sheets, props, fx are transparent PNGs; backgrounds are opaque and never contain the hero.
3. **Timing before shots**: narration lengths (or seconds per beat) first; cut between lines, inside actions or on music sections.
4. **Cut only for a reason; no zoom cuts** (directing §3): new place, a true close-up (hero > 2× the previous shot), or a real change of view for a reaction; otherwise one shot, pushing in slowly. Every shot has `place` and `view`; one place, one set (other views generated from its main background). `shots_lint` must pass.
5. **Hero big enough** (share of the short side, directing §3): wide ≥ 30%, opening and payoff wides ≥ 33%, medium ≥ 40%, medium-close ≥ 60% and full body; extreme-wide ≥ 15%, route only, at most 2, never opening or payoff; adjacent same-size shots within 1.3×.
6. **Always something happening, nothing shaking** (directing §4–5, compositing §5): a new event every 1–1.5 s, three layers moving; no per-drawing jitter or flicker; no swaying while standing; holds over 2 s are live through a local detail, idle breathing, a side character or the environment (camera motion alone doesn't count); pose to pose with anticipation and settle; no action replayed unchanged a third time; cycles ≤ 6 s, two- or three-cell loops ≤ 3 s.
7. **Effects and environment changes are generated images**, never code-drawn shapes; code may only relight (`char_light`, `warm_glow`, `darken`, `light_flood`, `self_glow`).
8. **Same character throughout**: every sheet from the character sheet as reference, one scale (`A.scale_ref`), placed by anchor; poses, facing and held objects connect across sheet changes and cuts.
9. **The image model never draws text, logos, real faces or franchise characters.** Text is set by code in Source Han Sans Bold, flat colour, style only on the plate. Cards: title ≥ 200 px, strip ≥ 60 px, credit ≥ 48 px (at 1080); narration subtitles use the style's `subtitle.size`, always at the bottom.
10. **Every action has a sound**: landings, impacts, tosses, catches in `foley`; key actions hit the music; silence before the twist (`references/sound.md`).
11. **Draw the payoff into the artwork**: character and object generated together, given a close shot; never pasted on in code; the object's path stays continuous across cuts.
12. **Self-review frame by frame**: `"$PY" "$S/selfcheck.py" out/<name>.mp4 --style <style>` in the film folder, against `quality.md` §2; fix and run again.
13. **A whole story** (directing §1): the skeleton for the film's length, every part with its seconds in the director's plan and caused by the part before; the want is set up before the first try and answered by the payoff.
14. **Only text and still images go into your own input; never audio or video.** Never attach, embed, base64-encode or open a sound or video file in a way that adds it to the conversation (an audio helper, `input_audio`, a media viewer, a data URL). This covers short clips, single stems and transcoded copies too, in tool results and in child-agent inputs. Many models have no audio input: the request fails with "Audio input is not available", and the item can stay in the history so that later text-only messages fail as well. Never probe whether audio works by sending a sample. Run media tools on the files locally and bring back only numbers, paths or extracted stills: check sound with `sound.py check` and `sound.py times`, look at video as extracted frames and `selfcheck.py` sheets. Playback is the user's: on the review page, or a local path you give them.

## 5. Delivery

- The film: `out/<name>.mp4`, or with cards `out/<name>-bookends.mp4` + `.srt` (that one is the film: register and deliver it); `<name>.srt` if narrated without cards; `out/contact.jpg`; `production-log.md`. Run `sound.py check` on exactly the file you deliver, after any cards are added, and quote its numbers and length. `<name>` = `NAME` in `film.py` = `name` in `sound.json`.
- **The last message is the report**, in the user's language, written out in full with all five numbered parts in this order, even where the app favours short replies. A link to `production-log.md` never replaces a part; item 3 lists every must-pass item on its own line.
  1. Title and logline; style; length and size; shots.
  2. Images: total, and backgrounds / action sheets / close-up sheets / props / fx; how many regenerated.
  3. Must-pass items (`quality.md` §3): one line each, pass / fixed / known issue / not checked. For sound, two separate lines: what was measured (loudness, true peak, dead air, cue times against contact frames) and "Listening: not listened by the agent".
  4. What you're least happy with, and anything not done (no network, no audio check…).
  5. Where the film and the review page are.
