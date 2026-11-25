---
name: script-to-video
description: Create and revise narrated explainer videos and process devlogs (16:9 YouTube or 9:16 Shorts) using the creator's recordings or local TTS, matched footage, web assets, and browser-rendered motion. Use for a video from a script, fast-paced editorial edits, narration cleanup, or footage and timing revisions to an existing video.
---

# script-to-video — playbook

Tools: `script_to_video/` (Python: Pillow, numpy; Kokoro TTS; Whisper for word timings), `engine/` (Chrome-rendered stage + puppeteer renderer), ffmpeg. Read this file before starting a video. The linked workflows guide the editing agent; the CLI does not automatically perform retake selection, safe human-speech editing, or source-audio drift repair.

## Brief and precedence

Use the latest user direction and approved cut as the baseline. Record aspect ratio, duration, voice source, narrative purpose, style, requested revisions, and protected scenes/audio in the project's edit plan. Ordinary YouTube defaults to 1920×1080, 16:9, 30 fps; Shorts use 9:16. Never inherit an earlier video's format or duration without checking the current brief.

The visual preferences below are this creator's defaults, not universal rules. Explicit requests override them. If asked only for suggestions, give advice and wait for an instruction to edit. An authorized edit should proceed without repeated confirmation.

Read these references when applicable:

* Own recordings, retakes, pause removal, demos with sound, or sync issues: [audio-editing.md](references/audio-editing.md).
* Game/process devlogs, tool screenshots, text layouts, or transition polish: [devlog-direction.md](references/devlog-direction.md).
* Before exporting or revising any delivered video: [revision-and-qa.md](references/revision-and-qa.md).

## 0a. Expectations

Deliver a reviewed first cut, clearly labeled as such when it has not been approved. Finish the requested scope and verification before handing it over; "draft" is not an excuse for broken sync or mismatched footage. Incorporate feedback into versioned revisions, preserving approved sections. Do not prescribe a number of revision rounds.

## 0. What a good one looks like

* Follow the requested opening. For "Hi, it's Iza," keep the screen black through the greeting when requested, then reveal the result. Time visual emphasis to the relevant spoken phrase; established footage can remain on screen.
* **Pictures, not words.** Kinetic text on ~5% of the runtime, on the lines that are the thesis. If a line has no picture, find or make a picture, don't slam a word on it.
* **A specific visual for each idea.** Reuse is purposeful for continuity, callbacks, and before/after comparisons; unrelated repeated filler is the problem.
* Fast-paced means progress, not constant cutting. Short editorial shots can run 2–4 s; coherent gameplay, demonstrations, and complete spoken lines may run much longer. No fixed eight-second ceiling.
* Use deliberate black sparingly. Honor requested greetings, conclusions, and a natural like/comment/subscribe sign-off; do not impose an outro card.
* Keep music below intelligible narration. During a sound demonstration, pause narration and let the original audio play clearly. Mix levels by listening and measurement, not one fixed gain for every source.

## 0b. The human test (do this before the shot plan, it is the shot plan)

This is for people, not for a model. A person watching has one question every second: *what am I looking at, and why?* Go through the script sentence by sentence and write, for each, what the viewer should **see**. Pass `see="..."` to `tl.shot()` so the plan prints with it.

* **A thing** (a hinge, a console, a person) → a clear photo of that exact thing, whole, centred.
* **A mechanism or a change** (the bolt slides, the pins lift, the map loops back) → a diagram, and show the **state change**: two or three frames of the same drawing (`latch_open` → `latch_closed`), not one static picture. If you can't find it, draw it in code; a plain drawing that explains beats a beautiful photo that doesn't.
* **A number** → a counter or the number on screen. **A name** → the face and a chip. **A comparison** → both things side by side, same scale.
* **A claim** ("nobody believed in it") → the source: the article, scrolled to the paragraph.
* **A feeling / the thesis** → black, or the single word.
* If the picture only makes sense *because* of the narration, it is the wrong picture. If a stranger could pause on it and guess the sentence, it is right.
* `tl.write()` reports reuse; review each hit for an intentional callback or continuity before replacing it.
* **Protection padding depends on the format.** 16:9 (YouTube): every image and illustration sits whole and centred with a margin, over a blurred copy of itself; nothing touches the edge. That is the default for `tl.pic()` (86% safe box) and `tl.bg()` (contain + backdrop). Use `fit="cover"` only for wide photos and clips that can lose their edges. 9:16 (Reels, Shorts, TikTok): the opposite. No padding, images fill the phone screen edge to edge; `tl.bg()` defaults to cover and `tl.pic()` to the full width. A letterboxed picture on a phone looks like a mistake. The Timeline picks the mode from its size (`h > w` = portrait) and prints it in the report; override per shot with `fit=` or `safe=`. A slow `zoomTo` push into a detail (a row of the dump, one frame of a sheet) is deliberate and welcome; a wide strip or a tall column left small in the middle of the frame for ten seconds is not. Don't crop into a small image in either mode; a 600 px photo blown up to 1080p is a glitch.
* **No black holes between shots.** A cut that drops to black for a quarter second while the next image fades in reads as a glitch. An image-only shot automatically gets its own blurred copy as a backdrop from frame one (`backdrop=False` on the shot to opt out), so every cut lands on something. Cuts are hard, moves are soft: slide/pop in 0.3 s, never a long fade on a new image.
* A continuation (same image, next shot, new camera move) uses `anim="none"`. The move then **continues** instead of restarting: a push that ended at 1.6× carries on from 1.6×, a new origin is glided to, a background `zin` on the same still keeps pushing. `write()` does this automatically; a zoom that snaps back to 1× on the same picture every few seconds is a tell. A fade or slide on an image that is already on screen reads as a flicker.
* Text appears within a tenth of a second of its word, and it is big: slams ≥ 150 px, chips ≥ 56 px. A word the viewer can't read is worse than no word.
* **The sentence test, shot by shot.** Put the transcript next to the dense sheet and, for every sentence, answer four questions out loud: *Is the thing I am naming on screen right now?* (she says "she jumps": is the character in frame, jumping, not the level scenery). *Is it there at the moment the word is said, not two seconds later?* *Is it whole: not cropped by a push, not hidden at the edge of a clip, not too small to see?* *Would someone with the sound off guess roughly what this sentence is about?* One "no" is a bug, fix it before anyone watches. Miscast pictures (a lock-picking diagram for "the lock", the good walk for "the walk looked wrong", the wrong frames of a clip) are the most common way a video stops making sense, and no report catches them; only this pass does.
* Review the exported opening, demos, transitions, and speech boundaries at playback speed. Contact sheets help catch framing and flashes but cannot prove clean speech or audio sync. A long held shot is only a problem when it stops serving the scene. Report exactly what was inspected; do not claim a full watch/listen from screenshots or transcripts.

## 0c. Fun behaviours (use one or two per video, on the lines that earn it)

* **Word by word.** `tl.words("IT FELL APART.", ins=["@everything", "@falling", "@apart"])` puts the line dead centre and pops each word on its own spoken word. No x/y maths: the engine centres the whole line.
* **The hit.** `tl.shot("the animation", shake="@apart", layers=[...])` jolts the entire picture (background and all) on that word, decaying over half a second. Pair it with the last word of a word-by-word line, a "YOU DIED", a number landing. Never on an ordinary cut.
* **Counter** counting up live to the number as it is said; **flash** (`flash=0`) on a punch cut; **replace-slams** for escalation ("1 YEAR" then "WEEKS."); a **chip** under a face.
* These are punctuation. Three of them in a minute and the viewer stops feeling any of them.

## 1. Script

Write as the creator speaks to one person. Mix sentence lengths and connect thoughts: motivation → choice → attempt → problem → correction → result. Short sentences alone can sound robotic. Read adjacent paragraphs aloud: a new topic needs a reason to follow the previous one. Avoid repetitive "I built / I made / I added" lists and invented excitement. Preserve personal anecdotes and practical tradeoffs that explain decisions; remove filler selectively, especially when explicitly requested.

For a process video, explain how the work happened, not only what the finished game contains. Attribute coding, image generation, animation, music, and voice to the tools actually used. Do not invent capabilities or release claims. Separate working features from ideas for future improvements. Honor the requested greeting and outro in the creator's voice. Use word count only as a rough estimate; measure the actual read and allow time for demonstrations.

## 1a. Retention (the shape that keeps people watching)

Show convincing proof early, after a requested short greeting. For a game reveal, let viewers follow title entrance → menu → intro → gameplay when that sequence is requested. Use varied moments from the game with enough time to understand each action, rather than disconnected flashes.

Establish the experiment and a specific question the process will answer. Use failures, corrections, before/after reveals, and completed demos to renew interest where the story calls for them. Do not interrupt a meaningful action to hit a cut-rate quota. Close the question with the actual result, honest limitations, and the requested sign-off. Add chapters at meaningful sections, not at every edit; regenerate them after timing changes. These are editorial choices, not guaranteed algorithm or retention outcomes.

## 2. Voice

Use the creator's recordings when supplied; do not replace or regenerate their voice without a request. Before editing them, read [audio-editing.md](references/audio-editing.md): resolve later retakes, clean the narration lane conservatively, and tighten pauses without cutting speech. Never blanket-run silence removal on the mixed soundtrack.

When synthetic narration is requested, use `script-to-video voice script.txt work/narration.wav --voice am_puck` (male) / `af_bella` (female). The current Kokoro helper defaults to speed 1.06, sentence gaps 0.12 s, and paragraph gaps 0.30 s. These are configurable TTS settings, not safe edit rules for human speech. Preview a paragraph, adjust to the brief, then measure the generated read.

## 3. Align

`script-to-video align work/narration16.wav work/` → `words.json` + `sentences.txt`. Read `sentences.txt` before planning: every shot is anchored to a phrase in there. Whisper misspells things ("Medium" for median, "3" for three); anchors accept alternatives: `"three|3"`.

Align the selected, cleaned narration. Word timestamps guide visual anchors, not surgical audio cuts: quiet consonants and phrase endings can fall outside ASR boundaries. After cuts, regenerate timings or apply the same verified time map to every dependent track.

## 4. Shot plan (on paper, before code)

For every sentence: one visual. Sources, in order of preference:
1. **A clip** (screen recording, gameplay, a demo) → `assets.clip_frames()`.
2. **A real photo or diagram**: Wikimedia Commons via `assets.commons_fetch()` (licence recorded in a manifest, write the attribution file for the description).
3. **An article/page screenshot**: `assets.capture()` (scroll to the paragraph, then `zoomTo` into it in the timeline).
4. **A made image**: `assets.text_card()` for terminal output or a quote, a chart drawn with Pillow, a diagram.
5. **A word** — last resort, for the thesis line.

Use supplied joke beats and editorial judgment within the brief; do not require a new approval for routine reversible choices. Favor contextual visual humor over meme filler. For source selection, latest-asset verification, terminal corrections, comments, and logos, read [devlog-direction.md](references/devlog-direction.md).

## 5. Timeline

```python
tl = Timeline("work/words.json", w=1920, h=1080)          # or w=1080, h=1920 for reels
tl.shot(0.0)                                                # black until the first word
tl.shot("hinge", bg=tl.bg("hinge.jpg", kb="zin"))           # shot starts when "hinge" is spoken
tl.shot("pin tumbler", layers=[tl.I("lock_diagram.png", 200, 80, 1500, anim="slideU", plain=True,
                                     zoomTo=1.6, origin="60% 40%")])
tl.shot("Linus Yale", layers=[tl.I("yale.jpg", 700, 100, 520, rot=-3), tl.C("LINUS YALE, 1861", 720, 900, i=tl.rel("1861"))])
tl.shot("a shape test", layers=[tl.T("A SHAPE TEST.", 380, 420, fs=170, rot=-2, i=tl.rel("shape test"))])
tl.write("work/timeline.js")
```

* **Two cursors.** `shot(phrase)` moves the search cursor forward (monotonic). `tl.at()` / `tl.rel()` look up from the current shot without moving it. Using one cursor for both once matched a repeated word 100 s later and froze two shots.
* Layer `in` = seconds after the shot start; `tl.rel("word")` gives it. Elements appear on their word. `rel()` returns a marker that `shot()` resolves inside the shot it lands in (the layers are built before `shot()` runs, so a number computed early would be relative to the previous shot and the text lands a second late).
* Camera moves: `kb` = zin / zout / panL / panR / panD / panU / punch / still. `zoomTo` + `origin` = slow push into a paragraph or a detail (never highlight boxes).
* Editorial text: Impact Regular, white uppercase, zero extra letter spacing, black outline painted behind the fill. Arial Black or Anton are fallbacks. Keep small asides text-only and preserve the image position. Direct corrections use a Mac terminal-style window beside the visual; see the devlog reference. Rotation and pop-in are optional emphasis, not defaults for every line.
* **A clip must show the moment the words describe.** `tl.clip("play1", offset=1.0)` starts the clip 1 s in, so "when she jumps" lands on the jump, not on whatever is at the top of the file. Look at the clip's contact sheet and pick the second. If the subject is near the edge of the frame, `kb="still"`: a contained clip is never cropped by more than 6%, but 6% is enough to lose a sprite at the border.
* Clips: `tl.clip("name")` as background, `tl.G("name", x, y, w)` as a layer. Frames are pre-extracted, deterministic. A state sequence (open → closed) gets `"hold": true` in gifmeta so it plays once and stays on the last frame instead of looping.
* `write()` prints word-slam share, shots over 8 s, missing anchors, reuse, and order problems. Fix missing anchors and unintended order errors. Treat duration, reuse, and text-share reports as review prompts; record intentional demos or callbacks rather than cutting them to silence a warning.

## 6. Render, sound, encode, audit

`script-to-video build build.py` does: render → sfx → encode → audit. Or step by step. Partial re-renders: `render work/ --start F --end F` (frame = t × 30), then re-encode.

Read [revision-and-qa.md](references/revision-and-qa.md) before export. Inspect contact sheets for framing, frozen footage, overlapping text, hidden HUDs, and accidental repetition; review motion and sound in the actual exported file as well. Render completion alone is not verification.

**Never overwrite a delivered mp4.** Bump the version. Overwriting a file someone has open kills their playback mid-video and they'll report "it stopped at 1:09".

## 7. Gotchas

* Tall images in a 16:9 stage: fit to height first (w = img_w × 1040 / img_h), then zoom. A tall image at full width gets its bottom cut off.
* Wide text rows overlap: measure. Three words at 150 px need ~1900 px. Drop to 130 and spread.
* Use `ffmpeg -y` for disposable intermediates or a fresh versioned output path, never to replace a delivered file.
* Chrome file:// is fine for the stage, but the renderer serves the work dir over http on port 8722 so gif frames preload.
* Puppeteer captures ~8–20 fps in real time; record the real fps into GIFMETA for clips captured live.
* Wikimedia: use curl with a User-Agent; python's urllib has broken certs on some Macs. Record licences.
* Check disk space before rendering, including temporary streams and final mux/faststart space. Delete only proven obsolete scratch caches after checking active timeline/concat references. Preserve originals, current edit sources, and delivered versions.
* When the user says "it doesn't hit" without specifics, check in order: sound design, pacing, image specificity, sameness of animation.
* When the user says "transitions look glitchy": look for cuts to black between shots (missing backdrop), a fade on an image already on screen (use `anim="none"`), a clip that loops instead of holding, a pop on a huge image (use slideU), or a flash on an ordinary cut.
* When the user says "too many words": they are right. Replace slams with pictures until the share is ≤ 5–10%.
