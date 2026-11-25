---
name: ai-ad-editor
description: Turn a finished ad script into a finished short-form video ad (9:16, plus 4:5, 1:1 and 16:9 if wanted) from AI-generated clips, the user's own clip library (UGC), or both - voiceover, shot plan, library clip matching, characters, scene images, AI video clips, talking characters with lip-sync, edit, captions, music, hook variants, quality checks and export. Works with any generation tools - an MCP, built for Kie.ai (images, video and lip-sync) with ElevenLabs for the voiceover, or other APIs, or by hand with copy-paste prompts. Nothing paid runs without your yes. Use when the user says "edit this ad", "make the video", "turn this script into an ad", "video ad from this script", "AI ad editor", "make hook variants", or brings a script (and maybe a voiceover or avatar clip) and wants a finished video ad.
---

# AI Ad Editor

Takes a finished script and makes the finished video ad. The script is never rewritten: the job starts at the voiceover.

**Three ways to get the pictures**, chosen in Step 1:
- **AI:** every clip is generated (images, AI video clips, AI talking avatars). All 10 steps.
- **Library (UGC):** every clip comes from the user's own folder of filmed clips. The skill picks and trims; nothing is generated, so it's free apart from an optional generated voiceover. Steps 6, 7 and 8 are skipped.
- **Mixed:** library first; any line with no good library clip is made with AI, matched to the library footage. Steps 6 to 8 run only for those shots.

`$S` = this skill's `scripts/` folder. Every script runs with `python3` (on Windows, use `python` instead).

---

## Rules

1. **Say it, then wait for a yes.** Before every generation, show what will be made and the full prompt, then wait. On a re-run, show only what changed. "Go ahead and make it all" covers one batch, not the next stage.
2. **Never redo work on your own.** If a result has a problem, say what it is, suggest the fix, and wait.
3. **Choices are buttons.** Use `AskUserQuestion`: 2 to 4 options, one line each, the recommended one first and marked "(Recommended)". Taste and creative choices (music, voice, character, look, pace, hooks, how the product or explanation lines appear) get no recommendation: lay the options out evenly, with the cost next to any option that changes it. If the client has no buttons, use a short numbered list.
4. **Test one, then the rest.** One frame, then 1 or 2 clips, then the batch.
5. **Never touch the voiceover.** No speed change, no cuts inside it, no re-ordering. Clips are cut to fit the voiceover, never the other way round.
6. **Never change clip speed** unless the user asks.
7. **Files, not chat.** Plans and prompts are saved in the project folder. In chat, give a short note of what changed and the file path. Show tables (shot plan, brief summary) in chat; they are short.
8. **Fix only what was flagged.** A revision changes only what the user named. Every change makes a new version number.
9. **Meta-safe visuals.** Nothing graphic or medical on screen (no wounds, needles, blood or surgery), even when the voiceover talks about them. Show the feeling through the person: their face, a pause, a look out of the window.
10. **Soft claims.** Any on-screen text the skill writes makes no cure or disease claims.
11. **Plain words** in every message and prompt.
12. **Costs only when known.** `generate.py` prints the estimate from the provider. Never guess a price. Quote the estimate before every paid run and pass `--yes` only after the user agrees.
13. **API keys never go in chat.** Users add them to their shell profile themselves.
14. **Be a guide, not a form.** Walk the user through one step at a time, like a person sitting next to them:
    - Open every step with where they are and why it matters: `**Step 3 of 10: Voiceover.** The voiceover sets the timing for every shot, so we lock it first.`
    - Ask one decision at a time, with buttons. Never dump a list of settings or a table of tools.
    - End every step with what was done and what comes next: `Done: voiceover approved (0:26). Next: I'll time every word so the cuts land on them.`
    - Explain any term the first time it comes up (start frame, lip-sync, 4:5 safe zone) in one short line.
    - Recommend only where there's a practical right answer (setup, cost, quality, safety). Creative and taste choices are laid out evenly. Always leave room for their own answer.
15. **Any concept, any look.** The skill makes whatever the ad needs: 3D animation, 2D cartoon, motion graphics, cinematic, photoreal phone footage, stop-motion style, anything else. Never assume a look; the user picks it in Step 2.
16. **Their process comes first.** Before anything else, read `house-rules.md` in the working folder if it exists. It holds how this user or team works: how hands-on they want to be, naming, where finished files go, caption style, default look and voice, who approves, things they never do. It overrides this skill's defaults and recommendations. It never overrides rules 5, 12 and 13 (the voiceover is never touched, no paid run without an approved cost, keys never in chat). When the user says something should always or never happen, add it to `house-rules.md` and say so in one line. The blank layout is in `house-rules-template.md`.

**The 10 steps the user sees:** 1 Setup · 2 Brief and look · 3 Voiceover · 4 Timing · 5 Shot plan and hooks · 6 Characters · 7 Start frames · 8 Clips · 9 Edit · 10 Variants, checks and delivery. (The stages below are numbered for this file; always show the user these step numbers.)

---

## Stage 00 — Setup (Step 1 of 10)

Free. Keep it short: the user wants to make an ad, not configure software.

1. Run `python3 $S/check_setup.py` quietly. Don't show its output.
2. **Already set up** (`providers.json` filled): one line, "You're set up with Kie, same as last time." Move on.
3. **First time:** say what's needed in plain words: "To make the images and clips I need one AI generation account. The easiest is a Kie.ai API key: one key and one balance for images, video and lip-sync." Then ask with buttons:
   - **Kie.ai API key (Recommended).** If `KIE_API_KEY` works, confirm "Kie is connected, balance $X" and move on. If not, tell them how to get one and add it to their shell profile.
   - **Another tool I already use.** An MCP they've connected, or another API key. Check it and use it.
   - **No API, I'll run the prompts myself.** Manual mode: you write every prompt, they run it in any app.
4. Save it: `python3 $S/check_setup.py --auto` (or `--set image=api:kie --set video=api:kie --set lipsync=api:kie`, `--set video=mcp:<tool name>`, `--set video=manual:<app>`).
5. **Don't ask about voice, music or lip-sync now.** Each comes up in its own step, only if the ad needs it.
6. **Models are a choice, not a rule.** When clips come up (Step 8), recommend Veo 3.1 Fast as the place to start (good motion, fair price). On Kie, the built-in video models are the Veo 3.1 family (`veo3_lite`, `veo3_fast`, `veo3`), set with `--quality` or `check_setup.py --set video=api:kie:<model id>`. Other video models (Kling, Seedance and so on) need their own few lines in `scripts/providers/kie.py` before they work; through an MCP or by hand, any model the user has works. Same for images: Nano Banana 2 to start, any other image model if they prefer.
7. Only if ffmpeg or faster-whisper is missing, give the one install line `check_setup.py` prints.

**How each mode works from here on.** Every generation goes through `generate.py`:

| Slot mode | What `generate.py` does | What you do |
|---|---|---|
| `api` | Prints the estimate; with `--yes` it makes the file | Quote the estimate, get a yes, re-run with `--yes` |
| `mcp` | Exits with code 3 and prints the prompt and settings | Call that MCP tool with them; save the result to the path it printed |
| `manual` | Exits with code 4 and writes `manual/<name>.md` | Tell the user which file to open; wait for them to drop the result where it says |

Every rule and approval stays the same in every mode. In manual mode, "approve" means approving the prompt before they run it.

---

## Stage 0 — Start

- If the working folder has a project with `state.json`, offer to pick up where it stopped.
- Otherwise, **welcome them first** (before Setup): one short paragraph saying what you'll make together and how it works: "We'll go from your script to a finished ad in 10 steps. I'll explain each one as we go, you approve every step, and nothing that costs money runs without your yes." Then list the 10 step names on one line, and start Step 1.
- **How hands-on?** If `house-rules.md` doesn't say, ask once with buttons and save the answer there:
  - **Approve every step (Recommended for a first ad).** Every gate in this file.
  - **Key steps only.** Approve the brief, the shot plan and hooks, and the final ad. Frames and clips are made without stopping, inside a budget they set now.
  - **Autopilot.** Make the whole ad inside a budget they set now. Stop only if something fails, the budget would be passed, or a choice can't be made from the brief.
  An approved budget counts as the yes for every paid run inside it (`generate.py --yes`). Show the running total at each step.
- **Where do the clips come from?** Ask with buttons (skip if `house-rules.md` says): **AI-generated** / **My own clip library** / **Mixed: my library first, AI for the gaps**. For library or mixed, ask for the folder (a local folder, or a cloud folder they download or connect), then run the Library steps below before Step 5. In library mode tell them the steps they'll see: Setup · Brief · Voiceover · Timing · Pick the clips · Edit · Checks and delivery.
- **Start anywhere.** Ask with buttons what they already have, and start at that step: just a script (Step 2) / a script and voiceover (Step 2, voiceover option 1) / their own shot plan (Step 5: check it, then go on) / their own frames or clips (Step 8 or 9: drop them in `frames/` or `clips/` named by shot id) / a project from before (pick up from `state.json`).
- Then ask with buttons: "Paste your brief" (show the template from `brief-template.md`) or "Ask me the questions" (one question at a time, look first).

**Project folder:** `<brand>-<ad name>/` in the working directory:

```
brief.md  state.json  shots.json  words.json  changes.md
inputs/  audio/  characters/  frames/  clips/  manual/  qc/  final/
```

Brand files: `brands/<brand>/kit.md` (product, buyer, logo, look, avoid list) and `brands/<brand>/learnings.md` (feedback that applies to every ad for that brand). Read both at the start of every ad for that brand.

Update `state.json` at the end of every stage: `{"stage": "<name>", "done": [...], "waiting_on": "<what the user needs to do>"}`.

---

## Stage 1 — Brief and look (Step 2 of 10)

**The look comes first, before anything else in the brief.** Ask with buttons: "What should this ad look like?" Options: 3D animated (like an animated feature film) · Photoreal (looks filmed on a phone) · Motion graphics / 2D · Something else (describe it or send a reference). Then write one **look description** in 2 or 3 plain sentences, show it, and get a yes. It's reused word for word in every image and clip prompt, so every shot matches. For photoreal, also read `guides/phone-look-guide.md`.

1. **Check the must-haves:** script, product name, what it is, what it does, product photos, buyer (age, gender, country), their problem, voiceover option. If one is missing, ask for that one only. Never start without all of them. A brand kit that already exists fills the brand fields.
2. **Fill the optional fields with defaults** (the defaults are in `brief-template.md`).
3. **Reference ad:** if one is given, watch it (download, pull frames every second with ffmpeg, transcribe it) and write down its pace (seconds per shot), shot types, caption style and how it opens. Use that as the guide.
4. **Their day:** if the user gave no real moments from the buyer's life, suggest 4 or 5 specific ones (who they're with, what the problem costs them) and let them pick.
5. **Show one summary table:** field, what will be used, "you" or "default". One approval covers it all.
6. Save `brief.md`. Save the brand fields to `brands/<brand>/kit.md`.

⛔ **Gate:** the user approves the brief.

---

## Stage 2 — Voiceover (Step 3 of 10)

Use the option from the brief. If it's missing, ask with buttons.

**1. I have the voiceover.** Copy it to `inputs/vo.mp3` (or `.wav`). Show its length (m:ss).

**2. Generate it.**
- Voice slot. List voices with `python3 $S/generate.py voices` and pick 3 that fit the buyer (age, gender, accent). Offer them with buttons, one line each. On Kie the voices are a fixed list of ElevenLabs v3 voices; a user who wants their own ElevenLabs voices sets `check_setup.py --set voice=api:elevenlabs` with an ElevenLabs key.
- Save the script as plain text (`inputs/script.txt`) and make one take:
  `python3 $S/generate.py voice --text-file inputs/script.txt --out audio/vo.mp3 --voice <id>` (estimate, then `--yes`).
- Show the length. The user listens and approves, or asks for another voice.
- Save the chosen voice: `check_setup.py --voice-id <id>`, so hooks and later ads match.

**3. Talking characters** (people on screen say the lines). Ask with buttons:
- **Same voice all the way through (Recommended):** generate the voiceover first (option 2). Later, each talking shot is made as a normal clip of the person facing the camera, then lip-synced to its part of the voiceover (Stage 7). Exact words, one voice.
- **The video tool makes the voice:** cheaper and faster. Warn the user: the voice can change from clip to clip, and the tool sometimes changes words. Every talking clip is transcribed and any changed word is flagged (Stage 7). There is no voiceover file: the shots file has no `"vo"`, each talking shot sets `"use_clip_audio": true`, and shot lengths come from the lines (about 2.7 spoken words a second). `edit.py` builds the sound from the clips and transcribes it for the captions.

**4. AI talking avatar.** One AI presenter talks to camera for the whole ad, and the avatar video is the voiceover and the main picture. If the user already made the avatar video (in HeyGen or similar), copy it to `inputs/avatar.mp4`. If they have a photo of the presenter (or you make one in Stage 5), make the talking video from the photo and the voiceover. Only the cut-aways are generated as clips:
`python3 $S/generate.py avatar --image inputs/host.png --audio audio/vo.mp3 --out inputs/avatar.mp4 --prompt "<expression, movement, camera>"`

**5. No voiceover (text on screen).** The story is told in on-screen text over music. Each line is one `"type": "text"` shot with its words in `"text"`; its time on screen = its words ÷ 3 per second, at least 1.5s. The card's background is a clip or image (`"source"`) or a plain colour (`"bg": "#1a1a1a"`). The shots file has no `"vo"`.

⛔ **Gate:** the user approves the voiceover (options 1, 2, 3 and 4).

---

## Stage 3 — Timing (Step 4 of 10)

- **Options 1, 2, 4 and the same-voice route of 3:** `python3 $S/transcribe.py <vo or avatar file> <project> --script inputs/script.txt`. This writes `words.json` (every word with its time) and `shots_draft.json` (one draft shot per idea, none longer than the video slot's `max_seconds`). The times come from Whisper; the words come from the script: words that line up one for one are fixed automatically, and any line it prints as `CHECK BY HAND` you fix in `words.json` yourself.
- **Option 5:** build `words.json` from the reading speed.

---

## Library (UGC and mixed modes)

Runs once per library, then only for new clips. Free.

1. **Index:** `python3 $S/library.py index <folder>`. It reads every clip's length and shape and saves 4 frames from each into `<folder>/_index/`. Re-run it when clips are added; it only processes new ones.
2. **Look and tag:** `python3 $S/library.py sheet <folder> --page N` makes one image of 12 clips × 4 frames. Look at every page and tag each clip in plain words: who is in it (age, gender), what they do, where, the mood, and whether the product shows: `python3 $S/library.py tag <folder> <clip> "<tags>"`. File names often describe the clip; still check the frames. Note which of the 4 frames is the best moment, so you can set `in`.
3. **Licence check (once):** ask whether the clips are cleared for use in ads. If they aren't sure, say so in the final README.
4. **Fit check (before planning, every ad):** read the script next to the library tags and estimate how many lines have a clip that really shows them (the right kind of person, the right action or place). If it's under half, say so plainly before the shot plan, with the reason in one line (what the clips show vs what the script is about), and ask with buttons, with no recommendation (one option costs money, the others don't): **Switch to mixed: the lines with no good clip are made with AI, about $X** (lines × the clip price, plus a frame each) / **Library only: free, using the closest clips, marked in the plan** / **Add clips to the library first**. In mixed mode the same check tells the user up front how many AI shots and roughly what they'll cost.
5. **Repeats:** `library.py find` ranks clips used in earlier ads lower. Ask once whether to avoid clips used in recent ads; after the final, run `library.py used <folder> <clip> <project>` for every clip in the ad.

## Stage 4 — Shot plan and hooks (Step 5 of 10)

### Before I plan the shots

One quick round, one question at a time with buttons. These are creative choices, so no option is marked as recommended; each has a default (listed first) that's used if the user says "use the defaults" at any point.

**Only ask what fits this ad.** The list below is a menu, not a script. Read the script, product and look first, then pick the questions that change the shots for *this* ad, and word them in its world (its niche, its character, its product). Skip anything the brief already answered and anything that doesn't apply: no ingredient question when the script names no ingredients, no "who is the main character" for a faceless motion-graphics ad, no "how time passes" without a timeline. Usually 3 to 5 questions, never all 9 by default. Add a question that isn't on the list if this ad needs it.

1. **Who is the main character?** Age, job, life (if the brief didn't say).
2. **Real moments from their day.** Where the problem hits hardest, and who's there. Suggest 4 or 5 and let them pick.
3. **Who's in their life?** Partner, kids, friends, colleagues: shots with other people land harder.
4. **Tone of the low point.** Funny and relatable, or serious.
5. **How the explanation or ingredient lines look.** Simple animation inside the body / a visual metaphor / lifestyle only.
6. **How the product appears.** Only the product itself early, with branded packaging near the end / packaging from the start.
7. **How time passes** (for "week 1, week 2" scripts). On-screen labels, or only through the voiceover and how they look.
8. **Pace.** A cut every 2 to 3 seconds / one shot per line. Show the number of clips and the cost next to each.
9. **Rough cost.** Number of clips × the clip price, plus images. Offer stills with a slow zoom for some shots if they want it cheaper.

### The shot plan

Start from `shots_draft.json`. Show one table:

| Shot | Time | Line | What we see | Type | Source |
|---|---|---|---|---|---|

**Source** is `AI` or `Library: <clip> @ <in seconds>`. In library and mixed mode, fill it like this for every line:
1. `python3 $S/library.py find <folder> "<the line, or what we should see>"` and look at the frames of the top matches.
2. **Good match** (shows what the line says, the right kind of person, no clash with the shots around it): use it, with `in` set to the best moment. The shot is `"type": "library"`, `"source": "<folder>/<clip>"`.
3. **No good match:** library mode: use the closest clip and mark the row `closest match` so the user sees it. Above the table, give the count ("9 of 22 lines have a good clip; the other 13 use the closest one"). Mixed mode: mark the row `AI` with its cost, and add it to the list of shots Steps 6 to 8 will make.
4. The user can flip any row ("use AI for s05", "find a library clip for s09").
5. Library rules: don't use the same clip twice in a row; don't reuse the same moment of a clip; keep one main person where the story has one main character; vertical clips are best (horizontal ones are cropped to the middle, so check the person stays in frame).

**Types:** `clip` (generated from a start frame), `talking` (clip + voice, option 3), `image` (a still with a slow push-in: product photo, end card), `avatar` (the AI talking-avatar video from option 4), `text` (a text card, option 5).

**Self-check before showing it:**
- Every shot shows what its line says, clearly enough that someone watching on mute follows the story from the pictures and captions.
- One timeline, in order: the past first, then forward. No jumping back and forth.
- No camera angle twice in a row. Vary: wide, overhead on the hands, front close-up, profile, over the shoulder, low angle, extreme close-up.
- Real moments from this buyer's life, ideally with other people (the partner who notices, the friend, the grandchild). Not stock moments like typing on a laptop or writing a list. Ask: would someone with this problem think "that's literally me"?
- Close-ups on the big emotional moments (the low point, the relief, the win).
- Early product shots show only the product itself (a capsule in a palm); branded packaging comes near the end or when the brand is named.
- Screens face the character, not the viewer. Show what's on a screen only over the shoulder or in a hand-and-phone close-up.
- Meta-safe.
- The explanation lines are shown the way the brief chose (simple 3D animation, a visual metaphor, or lifestyle only).

### The hooks

The user controls the hooks. If the brief settled them, use that. Otherwise ask with buttons: **"How do you want to handle hooks?"**

| Option | What happens |
|---|---|
| I'll write my own hook lines | The user pastes 1 or more opening lines |
| Same opening line, different visuals | The user describes each visual, or picks from suggestions |
| Suggest some for me | 3 to 5 hook lines or visuals, each with its angle (emotion, curiosity, visual metaphor). The user keeps, edits or deletes each one |
| Just 1 hook | The script's first line |

Each hook gets a card:
- **Hook line** (spoken or on-screen text)
- **What we see**, shot by shot, for the first 3 to 5 seconds
- **Join:** how it flows into the main ad's next line with no jump. Read the hook line followed by line 2 out loud in your head; if it doesn't follow, fix the hook, never line 2.

A new hook line needs its own voiceover: their own file, or generated with the same voice and settings as the main voiceover so the join can't be heard. Each hook is planned in its own file, `shots_hook<letter>.json` (with `"vo": "audio/vo_hook<letter>.mp3"` and its own `words` file). The main ad's clips are reused.

Any part of any hook can be changed without touching the rest. Adding a hook later is a new card; the main ad is not rebuilt.

Save `shots.json` (and the hook files).

⛔ **Gate:** the user approves the shot plan and every hook card. This is the most important gate. Changes here are free.

---

## Stage 5 — Characters (Step 6 of 10)

**Library mode: skip this step.** **Mixed mode:** make sheets only for people in the AI rows, and when that person is someone from the library footage, make the sheet from their best library frame (`--ref <folder>/_index/frames/<frame>.jpg`, "the same person as the attached photo") so the AI shots match. **Also skip this step** when no person appears in more than one shot (motion graphics, text-only, product-only ads). Say so in one line and go to Step 7.

1. Use the **look description** approved in Step 2 word for word in every sheet prompt.
2. Offer **3 different people** who all fit the buyer: vary ethnicity, hair, age within the range, outfit. Never 3 takes of the same person. One character sheet each, written to one jobs file so the user sees one cost and approves once:
   `python3 $S/generate.py images <project>/characters_jobs.json` with `[{"prompt": "<sheet prompt A>", "out": "characters/option_a.png", "aspect": "16:9"}, ...]`. Keep jobs files in the project folder: the paths inside are read from the jobs file's own folder.
   Sheet prompt: "<look> character sheet. One person shown 4 times on a plain light-grey background: face close-up, full body front, full body three-quarter left, full body three-quarter right. Neutral expression. <age, face, skin, hair, build, outfit, small details>. Same person in all 4 views. No text, no logos."
3. The user picks one. That sheet becomes `characters/master.png`.
4. **Every other version of that person** (struggling, recovered, younger) is an **edit of the master**, never a new prompt:
   `--ref characters/master.png --prompt "Edit the attached sheet. Keep the face, features and proportions identical. Change only <what changes>."`
5. A user's own photo of the presenter or character replaces the sheet.
6. Other people who appear more than once (partner, friend) get their own sheet the same way.

⛔ **Gate:** the user picks the main character and approves every other sheet.

---

## Stage 6 — Start frames (Step 7 of 10)

One frame per `clip` and `talking` shot (library mode: skip this step; mixed mode: the AI rows only, in the look of the library footage, which is usually the photoreal phone look in `guides/phone-look-guide.md`).

- Attach **exactly one** character sheet per frame (two sheets blend the faces): `--ref characters/<stage>.png`. Add a place reference if there is one. Prompts say "exactly as the attached sheet" and never describe the face again.
- Reuse the first approved frame of a place as the reference for later shots there.
- **Product shots:** the character using the product (holding it, taking it). Attach the master sheet, an approved frame of them, and a clean product photo. Spell out the big label text. Use `--quality best` for these. Check the brand name is spelled right.
- **4:5 safe zone:** every face, product and key prop sits between 15% and 85% of the frame height. Write it into every prompt: "full-bleed vertical image that fills the whole frame edge to edge, no borders, no bands, no letterbox; the faces and hands are in the middle of the frame, with the scene continuing above and below them". Never write "the top and bottom are background only": image models read it as empty bands. Check every frame for bands before showing the grid. `generate.py image` also checks each tall frame by itself: if it looks letterboxed it remakes it once on the best model (the first take is kept as `<name>_banded.png`) and prints a CHECK line if it still looks off.
- **Talking shots:** the person faces the camera, mouth closed and about to speak, front or slightly to one side, no hands in front of the face.
- One clear action per frame. Describe camera position, the action and the light.

Make the first frame as a test (`generate.py image`). After a yes, put the rest in one jobs file and make them in one run with one cost: `python3 $S/generate.py images <project>/frames_jobs.json` (each job: `prompt`, `out`, `refs`, optional `quality`; keep the jobs file in the project folder). Show all frames in one grid image (ffmpeg tile) with shot ids.

**Self-check before showing the grid:** 4:5 safe zone, no angle repeated back to back, enough close-ups on the emotional moments, the person's state matches the line (tired vs rested, messy room vs tidy), no strange props, hands and product held in a way that makes physical sense.

⛔ **Gate:** the user approves the frames.

---

## Stage 7 — Clips (Step 8 of 10)

Library mode: skip this step. Mixed mode: the AI rows only.

1. Write each clip's `video_prompt` in `shots.json`: the camera, the movement, one action, the light, in plain words. For `talking` shots made by the video tool, put the exact line in quotes: `she looks at the camera and says: "<line>"`.
2. Run `python3 $S/generate.py clips <project>` for the estimate. Make 1 or 2 test clips first (`--only s01 s02`), then the rest after a yes. It skips clips that already exist; `--only` remakes the named ones and keeps the old take as `<id>_prev.mp4`.
3. **Check every clip yourself** before showing anything: `python3 $S/contact_sheet.py <project>` writes `qc/contact_sheet.jpg`. Look for warped hands, the face changing, objects changing shape, text appearing, the wrong product. For any clip it flags with a frozen start, set `"in": <seconds>` on that shot so the edit starts after it.
4. **Talking shots:**
   - **Same-voice route:** cut each talking shot's part out of the voiceover (`audio/<id>.mp3`, using the times in `words.json`), then
     `python3 $S/generate.py lipsync --video clips/<id>.mp4 --audio audio/<id>.mp3 --out clips/<id>_talk.mp4`
     and point the shot at the lip-synced file with `"clip": "clips/<id>_talk.mp4"`. Use the part of the clip where the person faces the camera (cut it out first if they only turn to the camera partway through).
   - **Video-tool-voice route:** transcribe every talking clip and compare it with its line. Any changed word is flagged to the user with the clip id; the user decides whether to remake it.
5. Show the user the contact sheet and the list of clips you suggest remaking, with the reason for each. Remake only on a yes.
6. Veo sometimes refuses a clip with "unable to generate audio". `generate.py` retries by itself (without the no-audio line, then on the other Veo models; refused tries aren't charged) and notes which model made it. If every try is refused, reword the prompt as below.
7. If a clip is blocked (usually a safety filter on a person + a medical detail), soften the prompt and say what you changed. If credit runs out, stop, say so, and offer to finish the edit with the start frames as stills for the missing shots.

⛔ **Gate:** the user approves the clips (or says they don't need to see them).

---

## Stage 8 — Edit (Step 9 of 10)

1. **Music (always ask, never default to none).** Before the first edit, ask with buttons, with no option marked as recommended (music is taste): "Music under the ad?" Attach a track / Two tracks, switching at a line / Make a backing track for this concept / No music. "Make a backing track" writes a short mood prompt from the concept and makes 2 instrumental takes with Suno through Kie (`generate.py music --prompt "..." --out inputs/music.mp3`, about 6¢); the user picks one. Without Kie, it uses whatever music tool fills the music slot; otherwise write a short music prompt (mood, tempo, instruments, "instrumental, no vocals") for them to run in any music app and drop the file into `inputs/`. Save the answer to house rules so the next ad asks only to confirm.
2. `python3 $S/edit.py <project> --preview` for a fast low-res check, then `python3 $S/edit.py <project>` for the full export.
3. What the edit does: cuts every clip to its exact slot, frame-accurate, at 1080x1920; the voiceover is the only voice (or, on the talking-characters route where the video tool makes the voice, the clips' own voices); music sits under it and dips automatically while someone speaks (`"duck": false` turns that off); captions from `words.json`; end card if picked.
4. **Captions** use the preset from the brief:
   - **Bold:** full capitals, 1 line, the current word highlighted; long words shrink to fit
   - **Clean:** lower case, up to 2 lines
   - **None**
   - Never 3 lines. Captions sit in the middle of the frame, or just below the main face or object when that is in the middle. Never at the top, and always above the platform's bottom buttons.
5. **Then always** run `python3 $S/verify_vo.py <project> final/*.mp4`. It checks the final's sound against the voiceover and every word. Never deliver a file that fails it.
6. Save `final/<brand>_<ad>_hookA_9x16_v1.mp4`, a new version number for every change.

⛔ **Gate:** the user reviews the final.

---

## The shots file

`shots.json` (and one `shots_hook<letter>.json` per extra hook) is the plan every script reads:

```json
{
  "vo": "audio/vo.mp3",
  "words": "words.json",
  "quality": "standard",
  "shots": [
    {"id": "s01", "start": 0.0, "end": 2.4, "type": "clip", "text": "<the line>", "visual": "<what we see>",
     "frame": "frames/s01.png", "video_prompt": "..."},
    {"id": "s02", "start": 2.4, "end": 4.8, "type": "talking", "clip": "clips/s02_talk.mp4", "in": 2.4},
    {"id": "s03", "start": 4.8, "end": 7.0, "type": "image", "source": "inputs/product.jpg", "caption_pos": "low"},
    {"id": "s04", "start": 7.0, "end": 9.0, "type": "avatar", "source": "inputs/avatar.mp4"},
    {"id": "s05", "start": 9.0, "end": 11.0, "type": "text", "text": "<on-screen words>", "bg": "#1a1a1a"}
  ],
  "music": {"file": "inputs/music.mp3", "volume": 0.12},
  "endcard": {"image": "frames/endcard.png", "seconds": 3},
  "captions": {"preset": "bold"}
}
```

- Shots touch end to end (each `start` = the previous `end`). The last shot runs to the end of the voiceover by itself.
- `in`: where to start inside the clip (skips a frozen start). For `avatar` it defaults to the shot's `start`, so the avatar stays in sync.
- `clip`: use a different file than `clips/<id>.mp4` (a lip-synced take).
- `"type": "library"` with `"source": "<library folder>/<clip>"` plays a clip from the user's library from `in` seconds (default 0). Its own sound is muted unless `use_clip_audio` is set. Horizontal clips are cropped to the middle of the frame.
- `on_screen`: extra words shown on any shot (an offer, a label). `text_pos` moves them (0.5 = middle).
- `use_clip_audio`: keep the clip's own sound (the video tool's voice).
- `quality` per shot or for the whole file: `draft`, `standard` (default) or `best`.
- A shot with no clip yet plays its start frame as a still, so an edit can always be made.
- `captions`: `{"preset": "bold"}`, `{"preset": "clean"}`, `{"preset": "none"}` or `false`. Extra keys override the preset: `size`, `font`, `font_file`, `colour`, `highlight`, `max_words`.
- `music.volume` 0.08 to 0.15 sits under a voice; text-only ads can go up to 0.3. The music dips under speech by itself; `"duck": false` keeps it level.
- **Two music tracks:** `"music": {"file": "inputs/song1.mp3", "file2": "inputs/song2.mp3", "switch_at": 31.2}` switches tracks at that second (pick the second from `words.json`). `volume2` sets the second track's level.

---

## Stage 9 — Variants (Step 10 of 10)

From the brief:

- **Hooks:** `python3 $S/generate.py clips <project> --shots shots_hookB.json` makes only that hook's new clips, then `python3 $S/edit.py <project> --shots shots_hookB.json` cuts that version.
- **Sizes:** `python3 $S/variants.py <project> --sizes 4x5 1x1 16x9`. The 4:5 safe zone makes 4:5 and 1:1 work without losing faces.
- **Shorter cuts (15s, 30s):** suggest which lines to keep and show the shorter script; cut only after a yes. Shorter cuts need a voiceover recorded for that length (or option 5); the voiceover is never cut mid-sentence.

Run `verify_vo.py` on every variant.

---

## Stage 10 — Checks and delivery (end of Step 10)

1. `python3 $S/qc.py <project>` runs every check on every file in `final/`: size and shape, H.264 and AAC, sound runs the full length, no black picture, frozen picture flagged, length and file size for the platform, and the voiceover check. It does not check captions: look at a few frames yourself to make sure no caption covers a face or sits under the app's buttons.
2. Fix anything that fails before sending.
3. Write `final/README.md`: every file made, which tools made it, the cost where known, and anything missing or replaced with a still.
4. Send the finals to the user. If a Drive or Dropbox tool is connected and the user wants it, upload them there.

---

## Revisions (working with the user as their editor)

The user watches the draft and gives notes like they would to an editor. This step is a loop: draft → notes → plan → v2 → notes, until they're happy.

**1. Every draft goes out with a shot map.** After each edit run `python3 $S/shot_map.py <project> final/<draft>.mp4`. It makes one image of every shot with its time, id and line (`final/<draft>_shotmap.jpg`). Send the draft and the shot map together, and say: "Give notes any way you like: a time (0:23), a line ('when she says carpet'), or a description ('the bathroom bit')."

**2. Turn every note into a shot.** Match times to shots with the shots file, lines with `words.json`, and descriptions with the shot map. If a note could mean two shots, ask which, with the two thumbnails.

**3. Sort the notes into free and paid, and show the plan before changing anything:**

| Free (edit only, instant) | Paid (makes something new) |
|---|---|
| Swap a shot for another existing clip or frame | A new clip or frame |
| Trim, extend, move or reorder shots | A new character look |
| Skip a frozen or bad start (`in`) | A new voiceover or hook line |
| Caption size, position, style, a word fixed | A new music track |
| Music on/off, louder/quieter, the switch point | |
| Text on screen, end card, size versions | |

Show it as one short list: "6 notes: 5 free, 1 needs a new clip (about 33¢). Go?" Free changes need no yes when the user is on key steps or autopilot; paid ones follow the hands-on setting and budget.

**4. Change only what the notes name.** Everything else stays exactly as it was (same clips, same timings). Save the next version (`_v2`, `_v3`).

**5. Send v2 with a change list**, so they only re-watch what changed: "0:23 s08 clip swapped · captions moved lower · music quieter". Also write it to `changes.md`. Send a new shot map only if shots moved.

**6. Spot rules, not just fixes.** If a note sounds like it applies to every ad ("never put captions over faces", "always cut faster in the hook"), offer to save it to `house-rules.md` (or `brands/<brand>/learnings.md` for one brand). One line, only with a yes.

**If the voiceover changes** (a new take, a line rewritten): re-run `transcribe.py` on the new file, move each shot's start and end to its line's new times, keep every clip, and send the new draft with a shot map. Only shots whose line was rewritten need new visuals.

---

## Batch mode

When the user brings several briefs at once (a doc or a folder):

1. Stage 00 once.
2. Stages 1 to 4 for every ad, then show all the shot plans together for one approval.
3. Build the ads one after another. Keep `batch-status.md` up to date: each ad's stage (planned, frames, clips, edited, checked, delivered) and anything waiting on the user.

---

## Common problems and the rule that prevents them

| Problem | Prevention |
|---|---|
| Voiceover has gaps or drifts out of sync | The voiceover is never touched; `verify_vo.py` on every final |
| The character's face changes between shots | One master sheet; every version is an edit of it; one sheet per frame |
| Voice changes between talking clips | Generate the voiceover once, then lip-sync |
| The video tool changes the spoken words | Transcribe every talking clip and flag changes; or use lip-sync |
| Brand name misspelled on the product | Real product photo attached; best quality; check every product frame |
| Faces or product cut off in 4:5 feeds | 4:5 safe zone in every prompt, checked on every frame |
| The ad feels generic | Real moments from the buyer's day, with other people |
| Same shot feel twice in a row | No angle repeated back to back |
| Captions cover the face or sit under the app's buttons | Caption presets with safe positions |
| Clip blocked by a safety filter | Soften the prompt (often a person + a medical detail), retry once, then ask |
| Veo says it was "unable to generate audio" | Reword the clip prompt: no brand names or written words, nothing that sounds like talking (ask, say, tell). Not charged |
| Provider busy | `generate.py` waits and retries by itself; failed jobs are normally not charged |
| Credit runs out halfway | Stop, say so, finish with stills for missing shots, list them in the README |
| Clip opens on a frozen or storyboard frame | The contact sheet check; start the cut after it |
