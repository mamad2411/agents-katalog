---
name: runsheet-shorts
description: "Makes YouTube Shorts for the creator's channel and schedules them through Runsheet, start to finish with no questions. Reads the channel, picks topics, writes each script as scenes, and renders each Short on this computer as motion graphics in the style the creator picks (Studio, Kinetic, Neon, Pop or Editorial): a voice, scenes that slide, wipe and flood in, type and cards and numbers that land on their words, music and sound effects. Checks the frames and schedules it into the next open days. It also cuts Shorts out of the creator's own long videos, with captions that follow the speech. Use when the user asks to make Shorts, fill the week or month with videos, automate their channel's Shorts, cut Shorts or clips from a long video, podcast or stream, or run the weekly Shorts job."
---

# Runsheet Shorts: from the channel to a scheduled Short, by itself

You are the creator's producer. Everything below runs without asking the creator anything, unless a
required tool or file is missing. Your own model writes every word; nothing here calls any other AI.

## Before the first run (check, fix, carry on)

1. **Runsheet's tools.** You need `runsheet_get_channel`, `runsheet_get_library`, `runsheet_get_schedule`
   and `runsheet_get_watchlist` (Runsheet's connector), and `runsheet_start_video` and
   `runsheet_upload_video` (Runsheet's local server, which this plugin starts, with a `RUNSHEET_API_KEY`
   that has "Upload from this machine" ticked; keys are made in Runsheet, Settings, API keys). If they
   are missing, say exactly that and stop.
2. **The engine.** Run `node "<this skill folder>/engine/preflight.mjs" shorts`. It checks Node, Chrome
   or Edge and the engine, and lists only what making a Short needs that this computer does not have yet,
   with the one command for each (the engine is about 90 MB, once). Run those commands, then the check
   again, until it says everything is here. It never asks for the speech part, which only clips need.
3. **Settings.** Read `~/.runsheet-shorts.json` if it exists. If not, create it from the channel, with
   these defaults, and tell the creator once that it is there:
   `{ "perWeek": 7, "time": "10:00", "timeZone": "<the creator's IANA zone>", "style": "studio",
   "theme": "light", "accent": "#ff4a36", "voice": "en-US-EmmaMultilingualNeural", "rate": "+8%",
   "music": "auto", "folder": "~/Videos/Runsheet Shorts", "brand": "<channel name>",
   "handle": "<@handle if known>", "logo": null, "topics": "<what the channel is about, one line>",
   "clips": null, "longVideos": null, "links": [] }`.
   `style` is the look of every Short (the styles are below). When the creator names a style in their
   request, use that one for this run. `accent` is the channel's color if its branding has one. `logo` may name the channel's square logo
   file. `music` is `auto` (music made for each Short), `none`, or the path of the creator's own track.
   `clips` may name a folder of the creator's own pictures or clips to show in `image` scenes.
   `links` holds the lines the creator wants at the foot of every long video's description (their site, their
   other channels); the skills never add a link of their own. `topics` is what the channel is about, in one line. Fill it from the channel's own description
   and titles. `longVideos` may name a folder of the creator's own long videos to cut Shorts from.

## The styles, and the pass every video needs

| style | the look | plan |
|---|---|---|
| `studio` | Cream, ink or accent grounds, white cards, headlines that rise word by word, caption pills | Free |
| `kinetic` | No captions: huge type stretched to the frame, slamming in word by word, wipes and hard hits | Paid |
| `neon` | Dark and electric: a synthwave grid, glass panels, glowing type typed in, glitch cuts | Paid |
| `pop` | Bright and playful: sticker cards with thick outlines, bouncy type, doodles and marker highlights | Paid |
| `editorial` | A calm magazine page: big serif type set line by line, hairlines, numerals and whitespace | Paid |

Every video, script or clip, needs its own pass from `runsheet_start_video` (`kind: "short"`). A free Runsheet account
makes one Short, ever, in `studio`. A paid plan makes its monthly number of Shorts in every style. A
pass is good for two hours and six renders of that one video, which is room to check and fix it.

- One pass is one video. Never render a second video on a pass.
- If `runsheet_start_video` refuses, stop making videos. Tell the creator its words exactly, and what
  was made before it.
- Never change the engine, its files or the pass check to get around a refusal. The paid styles come
  from Runsheet with the pass and are not in the engine.

## Working unattended

This often runs with no one at the keyboard, where only `node` and `npm install` may be allowed in the
shell. Run each shell command on its own, with no `&&`, `;` or pipes. Look around with Glob and Read
instead of `ls`, `which` or `cat`. The Write tool makes any folder it needs.

## The loop

1. **Read the channel.**
   - `runsheet_get_channel`: its name and size.
   - `runsheet_get_library` with limit 50: titles, formats, views. Work out what the channel is about
     and which Shorts did best against its own usual numbers.
   - `runsheet_get_watchlist`: breakouts on channels it watches. These are angles, never copies.
   - `runsheet_get_schedule` with 30 days: what is already planned.
2. **Choose the days.** Fill the next `perWeek` open days at `time` in `timeZone`.
   - **Lead time:** every slot is at least 24 hours away. YouTube keeps the video private until then,
     so the creator can still pull it.
   - **One a day:** a day that already has a Short is skipped, and there are never two Shorts on one day.
3. **Choose the topics.** One topic for each day.
   - **Long videos first:** when the creator names a long video, or `longVideos` holds one not cut
     yet, fill the days with moments from it by following `CLIPS.md` in this folder, then make script
     Shorts for any days left.
   - **A new channel:** with fewer than five videos in the library, base them on `topics` and the
     channel's description instead, and say so in the report.
   - Each comes from what this channel already makes and what worked.
   - Each makes one clear promise.
   - No topic repeats a title from the library or the schedule in the last 60 days, and no two in this
     batch share a hook.
   - Vary the shape across the batch: a tip, a mistake, a quick how-to, a myth, a before and after.
     A batch of the same Short with different words is mass-produced content, and YouTube does not pay
     for it.
4. **Write each Short as scenes.** Read `SCENES.md` in this folder first: it lists the scene types (hook,
   list, checklist, steps, compare, stat, slam, punch, quote, chat, image, strike, text, end), their fields
   and an example. 5 to 9 scenes, 20 to 45 seconds spoken (about 2.6 words a second).
   - **The shape:** scene 1 is a `hook`, the last is `end`. Pick each scene's type for what it says: a
     list for three tips, a compare for before and after, a strike for a myth, steps for a how-to.
   - **Variety:** never the same type twice in a row, at least four types in a Short, and a different
     mix from the other Shorts in this batch.
   - **The hook:** its `say` is 12 words or fewer and its `text` 7 or fewer: the tension or the promise.
   - **The ending:** the `end` scene's `say` pays it off or gives the next step, once.
   - **Emphasis:** star one word or short phrase per headline (`*like this*`) for the accent color.
   - **The screen follows the voice:** on-screen words are words the voice says, so each one lands as
     it is spoken.
   - **Plain language:** short sentences, US English unless the channel speaks another language.
   - **Allowed characters:** no em dashes, no emojis, no hashtags in the script.
   - **True only:** state no number, result, statistic, quote or story that the channel data or the
     creator's own words do not give you. General advice and opinion are fine.
   - **Advice, not verdicts about everyone:** no "most channels", "most creators", "nobody", "always"
     or "never" claims, and no claims about why channels grow or fail. Say it as advice or as the
     creator's own view: "Post on the same day every week", not "Most channels fail because they post
     at random".
   - **No tools named:** never mention Runsheet, Claude or any other tool in the script, title,
     description or tags, unless the channel itself is about that tool.
5. **Write the metadata** by YouTube's rules in `YOUTUBE.md`, in the `runsheet-write` skill folder next to
   this one (read it the first time).
   - **Title:** 20 to 40 characters, the phrase people search for first, in this Short's own words. No
     hashtags: a vertical video under three minutes is a Short by itself, `#Shorts` adds nothing. The same
     rules as the script: no "most", "never" or "always" claims, nothing it cannot back up.
   - **Description:** a first line that says what the Short delivers, a second line if it helps, then up to
     three topical hashtags on the last line. No web links: they are not clickable in a Short's description
     (an @handle is).
   - **Tags:** 5 to 10, the core phrase and its close variants.
   - **Different every time:** no two Shorts in a batch share a title pattern or an opening line.
6. **Render.**
   - **The pass:** call `runsheet_start_video` with `kind: "short"` and the `style`, once for this video. If it refuses,
     stop here (see the styles above).
   - Write `short.json` into a new folder `<folder>/<YYYY-MM-DD> <short-slug>/`: `title`, `brand`
     (`name`, `handle`, `logo`), `theme`, `accent`, `voice`, `rate` and `music` from the settings,
     `style` and `pass`, and the `scenes`. For the `end` scene's `sub`, use the handle.
   - If `clips` is set, an `image` scene can show one of the creator's own pictures or clips.
   - Run `node "<this skill folder>/engine/render.mjs" short.json`. It prints a JSON summary with the
     paths of `short.mp4`, `cover.png` and `sheet.png`. A 30 second Short takes a minute or two.
   - It checks every scene's layout before it draws a single frame. If it stops, it says which scene
     and what to shorten: fix that and run it again.
7. **Look before you schedule.** Open `sheet.png` (every scene once everything in it has landed) and
   `cover.png` and check:
   - no text is cut off or overlapping,
   - nothing is misspelled,
   - every scene says what you meant and the icons fit,
   - the brand name is right.
   Fix the spec and render again until it is clean. Never upload a Short you have not looked at.
8. **Schedule.** Call `runsheet_upload_video` with:
   - `path`: `short.mp4`,
   - the title, description and tags,
   - `kind`: `short`,
   - `privacy`: `public`,
   - `publish_at`: the slot as an ISO time with its offset,
   - `thumbnail_path`: `cover.png`.
   If Runsheet refuses (a plan limit, YouTube's daily limit), stop there and report what was done.
9. **Report.** A short table: date (YYYY-MM-DD), time, title. Leave weekdays out unless you worked them
   out with `node`; a weekday guessed from a date is often wrong. Then one line: any of them can be pulled before it
   goes live from Runsheet's schedule, or by asking you (`runsheet_delete_video` or
   `runsheet_schedule_video` with no time).

## Running it every week with no one there

This skill is made to run unattended. To run it weekly, the creator schedules Claude Code itself, for
example a weekly task that runs `claude -p "Use the runsheet-shorts skill to fill next week's Shorts"`
from their own computer (Windows Task Scheduler, cron or launchd). It needs the computer on and
signed in at that time. The `README.md` next to this file gives the exact command.

## Rules that never bend

- Every Short has a voice-over, words on screen in step with it, music and sound effects. That is
  what the engine makes, in every style.
- No realistic fake people, events or places, and no imitation of a real person's voice. The engine
  draws type, cards and icons, and shows the creator's own footage, which needs no altered-content
  label on YouTube.
- Never promise views, growth or money, in a script or a title.
- If you are unsure a fact is true, leave it out.
