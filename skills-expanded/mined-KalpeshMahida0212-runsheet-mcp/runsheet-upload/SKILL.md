---
name: runsheet-upload
description: "Uploads a finished video from this computer to YouTube through Runsheet, with everything written from the video itself and by YouTube's own rules: watches it locally (hears every word with Whisper, looks at frames across it), then writes the title, the description with chapters at the real moments, tags and hashtags, makes a thumbnail from its best frame, and schedules it. Nothing is sent anywhere but the words it writes and the upload. Use when the user asks to upload, post or schedule a video file or a folder of videos, or to write a title, description, chapters, tags or a thumbnail for a video on their computer."
---

# Upload a finished video, with its copy written from what is in it

You are the creator's producer for a video they made themselves. Watch it first, write from what you saw and
heard, then upload it. Your own model writes every word; nothing here calls any other AI.

YouTube's rules for every field are in `YOUTUBE.md`, in the `runsheet-write` skill folder next to this one. Read
it before you write anything. Runsheet's brief tools hand the same rules over with each brief.

## Before the first run (check, fix, carry on)

1. **Runsheet's tools.** You need `runsheet_get_channel`, `runsheet_get_library` and `runsheet_get_schedule`, the
   brief tools `runsheet_generate_titles`, `runsheet_generate_description`, `runsheet_generate_tags` and
   `runsheet_generate_chapters`, and `runsheet_upload_video` and `runsheet_list_local_videos` (Runsheet's local
   server, with a key that has "Upload from this machine" ticked). If they are missing, say exactly that and stop.
2. **The engine** is the `engine` folder of the `runsheet-shorts` skill next to this one. Before the first
   video, run `node "<engine>/preflight.mjs" watch "<video>"`. It lists only what watching this video needs
   that the computer does not have yet, with the command for each: the engine (about 90 MB), and the speech
   part (about 760 MB with its model) only when the video has a sound track. Run what it lists, then the check
   again, until it says everything is here.
3. **Settings.** Read `~/.runsheet-shorts.json` if it exists, for `timeZone`, `time`, `accent` and `links` (the
   lines the creator wants at the foot of every long video's description). Without it, use the creator's time
   zone, 10:00, `#ff4a36` and no links.

## Working unattended

Run each shell command on its own, with no `&&`, `;` or pipes. Look around with Glob and Read instead of `ls`,
`which` or `cat`.

## The loop, for each video

1. **Find it.** The file the creator named, or every video in the folder they named
   (`runsheet_list_local_videos` lists them with their shape and length).
2. **Watch it.** Run `node "<engine>/watch.mjs" look "<video>"`. Add `--language es` (or the channel's language
   code) when you know it is not English. It prints the paths of:
   - `transcript.txt`: every sentence with when it starts and ends,
   - `frames.png`: frames across the video, at the times the summary lists,
   - `video.json`: its length, its shape, and whether YouTube will treat it as a Short (`short`).
   Read the whole transcript and look at the frames. Fix words the speech engine misheard by how they sound and
   by what is on screen or in the channel ("clot" is "Claude", "run sheet" is "Runsheet"). Check every name and
   number against the screen. Never copy text from a slide in place of what was said.
3. **Know the channel.**
   - `runsheet_get_channel` for its name.
   - `runsheet_get_library` with limit 50: which titles beat the channel's own median for their format, how they
     are shaped, and the words its viewers search. Compare the channel only with itself.
   - `runsheet_get_schedule` with 30 days, for the next open day.
4. **Write the copy.** Describe the video in plain words from what you watched: what it shows, who it is for,
   the payoff, Short or long, and the moments in order with their times. Pass that as `prompt` to each brief
   tool, and write from its instructions and YouTube's rules.
   - **Title** (`runsheet_generate_titles`): five options in different approaches, each with its length. A long
     video: under 60 characters, the searched phrase in the first 40. A Short: 20 to 40. Searchable for a
     how-to or a review; a real question or problem for a story. Pick one and say why in a line.
   - **Description** (`runsheet_generate_description`): a first line of 100 to 150 characters that says what
     the video delivers with the title's main phrase; then what it covers; then the creator's `links` (long
     videos only: links in a Short's description are not clickable); then the chapters; then up to three
     topical hashtags on the last line. Nothing the creator did not give, and no Runsheet or Claude anywhere.
   - **Chapters** (`runsheet_generate_chapters`, long videos with distinct parts): pass the real moments with
     their times from `transcript.txt`. `0:00` first, at least three, in order, each at least ten seconds. No
     chapters for a Short or a video with one continuous part.
   - **Tags** (`runsheet_generate_tags`): the core phrase, close variants and real misspellings of names in the
     video, under 500 characters in all.
5. **Make the thumbnail.**
   - From `frames.png`, choose the moment with one clear subject: a face with a strong expression, or the
     result the video promises. Not a frame that already has text on it, and never one that shows anything
     private: an email address, a key, a phone number, a customer's name. Screen recordings show these often.
   - Run `node "<engine>/watch.mjs" frame "<video>" <seconds> "<watch folder>/frame.jpg"` and look at it.
   - Write `thumb.json` in the watch folder: `image`, `text` (three to five words that add to the title rather
     than repeat it, one `*word*` starred for the accent), `accent` from the settings, `side` (left or right:
     wherever the subject is not), `focus` if the subject is off center, and `out`. A Short gets `"shape":
     "9x16"`. Run `node "<engine>/watch.mjs" thumb "<watch folder>/thumb.json"`.
   - Open it and check: the words read at a glance, the subject is clear of them, nothing is misleading. If it
     refuses the words as too small, use fewer.
6. **Look before you upload.** The title, the description's first line, the chapters and the thumbnail
   together: every name spelled right, every claim something the video says, nothing promised it does not
   deliver.
7. **Upload.** Only when the creator asked for it (upload, post, schedule). Call `runsheet_upload_video` with:
   - `path`, `title`, `description`, `tags`,
   - `privacy`: what the creator said; if they named a time, `public` with `publish_at` (an ISO time with its
     offset, at least an hour away); if they said nothing, `private`,
   - `thumbnail_path`: the thumbnail. YouTube may refuse a custom cover on a Short through the API; the uploader
     says so, and the creator can set it in Studio.
   If they only asked for the copy, stop at step 6 and give it to them.
8. **Keep a record.** Write `metadata.json` in the watch folder: the title, description, tags, chapters,
   thumbnail path and, once uploaded, the video's id and time.
9. **Report.** For each video: the title, its publish time (YYYY-MM-DD HH:MM and the zone) or "private draft",
   and one line on why that title. Write it with commas and periods: no em dashes, here either. Leave weekdays out unless you worked them out with `node`. Add a line when
   one applies:
   - The uploader marks every video "not made for kids". If this one is made for kids, the creator changes it in
     Studio before it goes out.
   - If the video shows realistic AI-made people, places or events, the creator ticks "altered or synthetic
     content" in Studio.
   - A Short cut from a long video: link it to the full video in Studio (the related video setting).

## Rules that never bend

- Only what is in the video, the channel's own data or the creator's words. No invented numbers, results,
  quotes or promises, in any field.
- A title and thumbnail promise exactly what the video delivers.
- No em dashes anywhere, in the copy or in your report; no emojis in titles; hashtags only at the end of the
  description.
- Never the same title pattern or opening line for two videos.
- The video goes from this computer straight to YouTube. Do not send the file, the transcript or the frames
  anywhere else.
