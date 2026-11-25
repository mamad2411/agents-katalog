---
name: hook-reel
description: Make a short "hook breakdown" reel from a viral video link. The reel replays the viral video's opening, then an AI voice explains why it worked, with word-timed captions, replays, number cards, a cover picture and a chosen ending. Use when the user says "/hook-reel", "make a hook reel", "hook breakdown", "break down this viral video", "make a reel from this link", "turn this viral video into a reel", "failed version vs good version", "compare these two videos", or pastes an Instagram, TikTok or YouTube Shorts link and wants a breakdown reel. Not for talking-head edits and not for posting.
argument-hint: [video link] [ending: hooks | viral | follow | save | share | like]
---

# Hook Reel

You make hook-breakdown reels by driving the hook-reels engine, a command-line program in the `engine` folder next to this file. The engine downloads the video, records the voice, cuts the edit and renders. You do the part that needs judgment: you watch the frames, write the script, and check the result the way an editor would before the user sees it.

This works in any agent that can run shell commands and look at image files. `SKILL_DIR` below means the folder this file is in.

Read `SKILL_DIR/reference.md` when you need the nine script approaches, the scene types, the two-clip spec or troubleshooting.

## Step 0: set up

Run this first, every time:

```bash
SKILL_DIR/scripts/setup.sh
```

It installs the engine's packages the first time and ends with `OUTPUT=`, `CHECK=` and `ENGINE=` lines. Use the `ENGINE` folder for every command below.

- A line starting with `PROBLEM:` means something is missing. Tell the user what to install and stop.
- In `CHECK`, `voiceKey: false` means the user must add `ELEVENLABS_API_KEY` to `ENGINE/.env` themselves. Never ask for a key in chat and never print `.env`.
- `claude: false`, `telegram: false` and `scoutKey: false` are fine. None of them is needed here.
- Instagram links need the user to be logged into Instagram in Chrome on this computer.

## Step 1: prepare the video

Take the link and the ending from the user's request (`$ARGUMENTS` where your agent fills that in). If no ending is given, use `hooks`.

```bash
cd "$ENGINE" && node_modules/.bin/tsx src/cli.ts prepare "<link>" --ending <ending> --json
```

- It downloads the video and pulls out one frame per second, the scene cuts and any speech. About a minute.
- It prints one JSON line per event. The last is `brief`, with the `jobId`, the path of the brief and the frames folder. On `failed`, read the reason, fix the cause, and run `prepare` again.
- If the link reports no view count, add `--views 2.3m`. Never guess a number: ask the user.
- For a video file already on disk, add `--file /path/video.mp4 --views <count>`.

## Step 2: write the script

Read the brief (`ENGINE/jobs/<jobId>/brief.md`) from top to bottom. It holds the facts about this video, the three approaches on offer for this reel, the earlier reels you must not repeat, and every rule. Then look at **every** frame in `ENGINE/jobs/<jobId>/frames/` in order; the first is second 0. If you cannot view images, say so and stop: a script written without watching the video is worthless.

Decide these before you write:

1. **The payoff.** The second where a first-time viewer understands what the opening leads to. For an ad, that is the second the product or brand is clearly on screen, not the second the scene changes.
2. **The cut.** `hook` starts at 0 and ends two to four seconds after the payoff. Cutting in before the payoff is the worst mistake: the voice says "it was an ad" and the viewer has not seen the ad.
3. **The approach.** Pick the one of the three on offer that fits this video and follow its shape.

Every line must be about this video: what is on screen, at which second, and what the viewer's brain does. If a line could be read over any video, rewrite it.

Give each trigger a tight `moment` of three to six seconds that starts where the thing its lines describe is on screen. The replay under those lines is cut from that moment, so a long or loose one shows the wrong part of the video.

Save the script as `ENGINE/jobs/<jobId>/draft.json` in the shape the brief gives, then hand it in:

```bash
cd "$ENGINE" && node_modules/.bin/tsx src/cli.ts script <jobId> jobs/<jobId>/draft.json
```

The engine checks it (word count, the cut, the view count wording, the approach, the moments). If it lists problems, fix all of them in the draft and hand it in again. Do not move on until it says `Script accepted`.

## Step 3: voice, edit and render

```bash
cd "$ENGINE" && node_modules/.bin/tsx src/cli.ts resume <jobId> --json
```

- It takes 3 to 6 minutes. Run it in the background if your agent can, and wait for it; do not poll.
- The stages are voice, plan, render, deliver. It ends with `done` (with the file) or `failed` (with the stage and reason).
- The voice stage costs ElevenLabs credits each time it runs. Do not re-run it without a reason.
- On `failed`, fix the cause and run the same `resume` command again; finished stages are kept.

## Step 4: check it like an editor

Look at the reel before you tell the user it is ready. Make a sheet of frames from the finished file and open it:

```bash
ffmpeg -y -v error -i "<file>" -vf "fps=1/2,scale=200:-1,tile=8x4" "$ENGINE/jobs/<jobId>/sheet.jpg"
```

Check that the opening runs until the payoff is on screen, captions are readable, footage is not stretched, any reaction clips fit their lines, and the ending matches the one asked for.

You cannot hear the reel. Say so, and ask the user to play it once.

## Step 5: fix and redo

- **Changed spoken words** (`stat`, `intro`, `triggers`, `formula`): edit the draft, hand it in again with `script`, then `resume`. This records the voice again.
- **Changed only the cut or a trigger's `moment`**: edit the draft, hand it in with `script`, then skip the voice and resume:

```bash
cd "$ENGINE" && echo '{"stage":"voice","state":"done"}' > jobs/<jobId>/status.json && node_modules/.bin/tsx src/cli.ts resume <jobId> --json
```

- A new delivery never overwrites the old file; it gets `-2` in its name.

## Step 6: hand it over

Tell the user, in this order: where the reel is (the `file` from the `done` event), that its cover is next to it as `<name>-cover.png`, the caption to paste (`ENGINE/jobs/<jobId>/caption.txt`), which approach and ending it used, and what you could not check (the sound).

## Two-clip comparison reels

For "this version got X views, this one got Y" reels: one clip plays untouched and gets a label, the second clip plays and gets a label, then the voice explains the difference. Write a spec file and run:

```bash
cd "$ENGINE" && node_modules/.bin/tsx src/cli.ts compare /path/to/spec.json
```

The spec format and a full example are in `reference.md`. You write the lines yourself here. Find the clean, untouched range of each clip by looking at frames of the file; never include a stretch that has someone else's captions or logo on it.

## The editing rules

These are what make the reels good. The engine follows them; you check them.

1. **Opening.** The source plays untouched, with its own sound, from second 0 until two to four seconds after the payoff. Up to 35 seconds.
2. **First line.** The voice comes in on the frozen last frame with the view count stacked up word by word, in the shape of the chosen approach ("This video pulled over 6.8 million views, and surprisingly, it was an ad for…").
3. **Approach.** One of nine, drawn at random from three the last reels did not use, so two reels in a row never have the same outline.
4. **Voice.** Pauses are cut out and the audio runs at 1.15 times speed: fast like a creator, never chipmunk fast.
5. **Captions.** Word-timed, white, uppercase. Either one word at a time or a phrase building up. No sound effect on every caption.
6. **Pictures under the voice.** Replays of the exact moment being described, small clip cards, black text cards, and number cards for "Number one, …".
7. **Reaction clips.** Only if the user has added clips to `ENGINE/assets/reactions` (none ship with the engine). At most three per reel, each one once, only where the line calls for it: confused on a question, shocked on danger, mind-blown on a twist, thinking on what the brain expects. Never over full-screen footage.
8. **Music.** Only if the user has saved a track as `ENGINE/assets/music/bed.mp3` (none ships). One bed, quiet (14 percent), starting with the voice. Without it the reel has the voice and sound effects, and the user can add a sound in the app when posting.
9. **Ending.** `hooks` and `viral` ask for a comment keyword over a blurred hooks document. `follow`, `save`, `share` and `like` show that button being tapped.
10. **Cover.** Black, pale blue hand-drawn text: "THIS AD HIT / 13 MILLION / VIEWS USING THESE".

## Critical rules

1. Run `setup.sh` first and use the `ENGINE` it prints. Never assume the folder.
2. Never read, print or ask for the contents of `.env`. The user edits it themselves.
3. Never invent a view count, a product name or a detail that is not in the frames or the speech.
4. Never mirror the source video.
5. Never copy another creator's script word for word. Keep the points, write your own sentences.
6. Never post or upload the reel anywhere. It is saved to the output folder and the user posts it.
7. Do not re-run the voice stage to fix something that a re-plan would fix.
8. Do not call a reel done until you have looked at its frames.
9. The source footage is another creator's work, and so is any music or reaction clip the user adds that they did not make. The engine credits the source account on screen; keep that on. If the user asks about risk, say so plainly.

With no link, ask for one.
