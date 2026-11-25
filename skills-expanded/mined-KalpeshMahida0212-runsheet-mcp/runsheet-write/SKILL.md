---
name: runsheet-write
description: "Writes and saves YouTube titles, descriptions, tags, chapters, Shorts hooks, translations and promo posts for the creator's videos with Runsheet, by YouTube's own rules for each field. Runsheet hands over its brief (the rules and the video's facts) and your own model writes the copy, so it costs the creator no Runsheet credits. A paid Runsheet plan writes without a limit; a free account has 5 writes in all, and when they are used the tool says so with the link to Starter: tell the creator exactly that. Use when the user asks for titles, a description, tags, chapters, a hook, translations, or posts for a video, or to fix the copy on a video that is not doing well."
---

# Write a video's copy from Runsheet's brief, then save it to YouTube

Every Runsheet writing tool returns a brief rather than a draft:
- **INSTRUCTIONS:** the exact rules Runsheet holds for that kind of copy.
- **YOUTUBE'S OWN RULES:** the limits and policies YouTube sets for that field.
- **INPUT:** the video's own facts.

Follow both sets of rules to the letter and write the result yourself. `YOUTUBE.md` in this folder has the whole
rulebook, with the reasons; read it the first time. Where the instructions ask for JSON, give the creator
readable text instead.

## Which tool for what

| The creator wants | Brief tool | Saved with |
|---|---|---|
| Titles | `runsheet_generate_titles` (describe the video in `prompt`) | `runsheet_update_metadata` (title) |
| A description | `runsheet_generate_description` | `runsheet_update_metadata` (description) |
| Tags | `runsheet_generate_tags` | `runsheet_update_metadata` (tags) |
| Chapters | `runsheet_generate_chapters` (an outline with real times) | added to the description with `runsheet_update_metadata` |
| A Shorts hook | `runsheet_generate_shorts_hooks` | used in the script or the title |
| Translations | `runsheet_translate_video` (video_id, languages) | `runsheet_set_localizations` |
| Posts for X, LinkedIn, Instagram, Community | `runsheet_repurpose_video` (video_id) | nothing: the creator posts them |
| A script | `runsheet_write_script` | `runsheet_create_idea` notes, or given to the creator |

Find a video's id with `runsheet_get_library` (published) or `runsheet_get_schedule` (planned and scheduled).

## How to work

1. **Know the video.** `runsheet_get_library` or `runsheet_get_schedule` for its title, format and tags. The
   better the `prompt` describes what happens in it (what it shows, who it is for, the payoff, the moments in
   order, Short or long), the better every field.
   - **With the file on this computer** (Claude Code): watch it first with the `runsheet-upload` skill's
     watch step, and write from the transcript and frames. That is the only way to real chapter times.
2. **Know the channel.** From the library, which titles beat the channel's own median for their format, and the
   words its viewers search. Write in that voice; never copy a title's pattern onto every video.
3. **Write each field from its brief.**
   - **Titles:** five options in different approaches, each with its length. Recommend one and say why in a
     line: searchable for a how-to, a question or a problem for a story.
   - **Description:** a first line that works alone in search, then what the video covers, the creator's links,
     chapters, and up to three hashtags last.
   - **Chapters:** only from an outline with real times. No outline, no chapters: say what you need instead.
   - **Tags:** the core phrase, close variants, real misspellings of names, under 500 characters in all.
   - **Each translation:** keep links, timestamps, handles and names exactly as written.
   - **Posts:** end each with the video's link, as the brief says.
4. **Save.** Show the creator the result and save it once they say yes. If they asked you to just do it, save the
   best option and say which one you chose.
5. **A video that is not doing well:** change one thing at a time (the title or the thumbnail), so the creator
   can tell what helped. Ask first if the video might be in a Test & Compare test in YouTube Studio: a change
   through the API would end it.

## Rules

- Only facts from the brief, the video or the creator. No invented numbers, results or quotes.
- A title and thumbnail promise exactly what the video delivers.
- No em dashes, no emojis, and no hashtags inside titles.
- Never add a line or link the creator did not give, and never name Runsheet or Claude in their copy.
- Never promise views.
