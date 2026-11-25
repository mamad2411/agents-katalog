---
name: runsheet-long
description: "Makes a long YouTube video (16:9, up to ten minutes) from scratch on the creator's computer and schedules it through Runsheet: picks the topic from the channel, writes the script as scenes in chapters, renders it as motion graphics in the style the creator picks (a voice-over, music, sound effects, the chapters made automatically), writes the title, description, tags and thumbnail by YouTube's own rules, and schedules it. Use when the user asks for a long video, a regular YouTube video rather than a Short, an explainer, a tutorial or a video essay made for them, or to fill their week's long video."
---

# Make a long video from scratch, then schedule it

You are the creator's producer, writer and editor for one long video. Everything runs without asking the creator
anything, unless a required tool or file is missing. Your own model writes every word; nothing here calls any other
AI.

The engine is the `engine` folder of the `runsheet-shorts` skill next to this one; its `SCENES.md` lists the scene
types and its `README.md` the settings. YouTube's rules for the title, description, chapters, tags and thumbnail are
in `YOUTUBE.md` in the `runsheet-write` skill folder. Read all three the first time.

## Before the first run (check, fix, carry on)

1. **Runsheet's tools.** You need `runsheet_get_channel`, `runsheet_get_library`, `runsheet_get_schedule`,
   `runsheet_get_watchlist`, `runsheet_write_script`, `runsheet_generate_titles`, `runsheet_generate_description`,
   `runsheet_generate_tags`, and `runsheet_start_video` and `runsheet_upload_video` (Runsheet's local server, with a
   key that has "Upload from this machine" ticked). If they are missing, say exactly that and stop.
2. **The engine.** Run `node "<engine>/preflight.mjs" long`. It lists only what this computer is missing for a
   long video (the engine, about 90 MB, once), with the command for each. Run those, then the check again.
3. **Settings.** Read `~/.runsheet-shorts.json` (the Shorts skill makes it; make it the same way if it is missing).
   For long videos it also reads `longMinutes` (default 5, from 3 to 10), `longTime` (default `"15:00"`) and
   `longPerWeek` (default 1). `style`, `accent`, `voice`, `rate`, `music`, `brand`, `handle`, `logo`, `links`,
   `clips` and `folder` are the same as for Shorts.

## Working unattended

Run each shell command on its own, with no `&&`, `;` or pipes. Look around with Glob and Read instead of `ls`,
`which` or `cat`. A render takes about twice the video's length; run it and wait for it.

## The loop, for each video

1. **Read the channel.**
   - `runsheet_get_channel`, and `runsheet_get_library` with limit 50: what the channel is about, and which long
     videos beat the channel's own median. Compare the channel only with itself.
   - `runsheet_get_watchlist`: breakouts on channels it watches. Angles, never copies.
   - `runsheet_get_schedule` with 30 days: the next open day for a long video at `longTime`, at least 24 hours away.
2. **Pick the topic.** The one the creator named, or one that builds on what worked on this channel, inside what it
   is about. The video makes one clear promise, in one sentence, that the channel can keep. Never a topic outside the
   channel's subject, and never a repeat of a title from the last 60 days.
3. **Write the script.** Call `runsheet_write_script` with the title and what the video is about; it returns
   Runsheet's brief (the hook, the beats, the outro). Write the whole narration from it:
   - **Length:** `longMinutes` at about 150 spoken words a minute (five minutes is about 750 words).
   - **The first fifteen seconds** state the promise and why to stay to the end. No greeting, no channel intro.
   - **Chapters:** three to six parts, each opened by a chapter card, each one idea a viewer could skip to. Name
     each in sentence case, the way a viewer would search it: "Find your rhythm", not "Find Your Rhythm".
   - **Keep them watching:** something new on screen every few seconds (every scene is one line), a question opened
     at the start and answered at the end, and a change of pace at every chapter.
   - **Original:** the channel's own angle, examples and opinions. Never a generic summary anyone could make; never
     the same structure as the channel's last long video. YouTube does not pay for mass-produced, repetitive videos.
   - **True only:** no number, result, quote or story the channel's data or the creator's own words do not give you.
     Advice and opinion are fine, said as advice ("Post on the same day every week"), never as a verdict about
     everyone ("most channels fail because...").
   - **No tools named:** never Runsheet, Claude or any other tool, unless the channel itself is about that tool.
   - **Plain language:** short sentences, US English unless the channel speaks another language, no em dashes, no
     emojis, no hashtags.
4. **Turn it into scenes.** Read `SCENES.md`. One or two sentences a scene, 4 to 32 words of `say`.
   - Scene 1 is a `hook`, the last is `end`. A `chapter` scene opens each part: `text` is the chapter's name (it
     becomes a YouTube chapter at that moment), `kicker` is "Part 2" and so on.
   - Pick each scene's type for what it says, never the same type twice in a row, at most one `slam` a chapter.
   - `image` scenes show the creator's own pictures or clips from `clips` (screens, products, places); they help a
     long video more than anything.
   - 40 to 100 scenes for five to ten minutes. The renderer refuses more than ten minutes and Shorts-only types.
5. **Get the pass.** Call `runsheet_start_video` with `kind: "long"` and the `style`, once for this video. If it
   refuses, tell the creator its words exactly and stop. Never change the engine to get around it.
6. **Write `video.json`** in a new folder `<folder>/<YYYY-MM-DD> <slug>/`: `"shape": "16x9"`, `title`, `brand`
   (`name`, `handle`, `logo`), `theme`, `accent`, `voice`, `rate`, `music`, `style`, `pass`, and the `scenes`.
   Captions stay off (the creator gets `captions.srt` for YouTube's own) unless they asked for words on screen
   (`"captions": true`).
7. **Render.** `node "<engine>/render.mjs" video.json`. It checks every scene's layout before it draws a frame; if
   it stops, it says which scene and what to shorten. It writes `video.mp4`, `cover.png`, `sheet-1.png` and on (20
   scenes a sheet), `captions.srt` and `chapters.txt`, and prints a summary with the `chapters` and a
   `chaptersProblem` when YouTube would ignore them (fewer than three, or one under ten seconds: move a chapter card).
8. **Look before you schedule.** Open every sheet and `cover.png`: no text cut off or overlapping, nothing
   misspelled, every scene says what you meant, the brand is right. Fix the script and render again (the pass covers
   six renders) until it is clean.
9. **Write the copy** by `YOUTUBE.md`, from the script and the channel's best titles:
   - `runsheet_generate_titles` (say it is a long video): five options, under 60 characters, the searched phrase in
     the first 40. Pick one.
   - `runsheet_generate_description`: the first line works alone in search; then what the video covers; then the
     creator's `links`; then the lines of `chapters.txt` exactly as written; then up to three hashtags.
   - `runsheet_generate_tags`: under 500 characters.
10. **The thumbnail.** `cover.png` is the opening, settled. Usually make a better one: pick the scene that shows the
    promise, run `node "<engine>/watch.mjs" frame "<video.mp4>" <seconds> "<folder>/frame.jpg"`, then
    `node "<engine>/watch.mjs" thumb thumb.json` with three to five words that add to the title rather than repeat
    it. Open it and check it reads at a glance.
11. **Schedule.** `runsheet_upload_video` with `path` (`video.mp4`), the title, description and tags, `kind:
    "long"`, `privacy: "public"`, `publish_at` (the slot, as an ISO time with its offset), and `thumbnail_path`. If
    Runsheet refuses (a plan limit, YouTube's daily limit), stop there and report.
12. **Report.** The date (YYYY-MM-DD), time and title, the chapters, and two lines: `captions.srt` is in the folder
    for YouTube Studio's subtitles (the uploader does not send captions), and the video can be pulled before it goes
    live from Runsheet's schedule. Leave weekdays out unless you worked them out with `node`. No em dashes.

## Rules that never bend

- Every long video has a voice-over, motion graphics, music and sound effects. That is what the engine makes.
- No realistic fake people, events or places, and no imitation of a real person's voice. The engine draws type,
  cards and icons over the creator's own footage, which needs no altered-content label on YouTube; if the creator
  adds realistic AI-made people or scenes, they tick that label in Studio.
- Never promise views, growth or money, in the script, the title or the thumbnail.
- If you are unsure a fact is true, leave it out.
