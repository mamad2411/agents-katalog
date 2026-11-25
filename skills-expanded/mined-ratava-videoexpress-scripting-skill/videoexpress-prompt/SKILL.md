---
name: videoexpress-prompt
description: A question-by-question wizard that writes one paste-ready VideoExpress (VE) 3.5+ prompt, or a matched pair - a start image, a video clip, or an image plus its clip - or improves an image or clip prompt the user already has. Walks through look and style (with links to the Creative mode style catalogue), what happens, dialogue, sound, camera, light and image, and negatives, applying the same prompt rules, multishot format, styles, Consistent Character advice and lip-sync methods as the VideoExpress Scripting skill. Use when the user wants a single VideoExpress image or clip prompt, a one-off shot, or help fixing one prompt. For a multi-clip video, a script, a prompt pack, chaining across clips or operating VideoExpress in the browser, use videoexpress-scripting instead.
metadata:
  version: "1.4.0"
  author: Brent Wesley
---

# VideoExpress Prompt

A wizard for **one shot**: a start-image prompt, a video-clip prompt, or an image-and-clip pair, written to the same rules as the VideoExpress Scripting skill. No project, no bible document, no prompt pack. Each step asks about one aspect of the prompt, suggests an answer, and moves on.

Two facts drive every prompt:

1. **The model renders nouns, not intentions.** Every noun, count, simile and stray token is a candidate to appear on screen.
2. **Each generation only knows what it is given.** A clip sees one still image plus the prompt. Anything not visible in the opening frame or described in the prompt will be invented.

## Read before writing

The rules live in `references/`, shared word for word with VideoExpress Scripting. This file doesn't restate them.

- **Always:** `references/multishot-template.md` (tag order, template, worked example) and `references/prompt-rules.md` (how the engine reads a prompt; the failure → cause → rule table).
- **Step 1, Look:** `references/styles/README.md` (index, image-prompt recipe, video pattern), then the one style sheet chosen. Characters, start images and Consistent Character: `references/bible.md`.
- **Steps 2 and 5, action and camera:** `references/camera-and-motion.md`.
- **Steps 3, 4 and 6, dialogue, sound, light:** `references/light-sound-dialogue.md`.

The references were written for multi-clip projects. For one shot, read them this way: the "bible blocks" are the character, outfit and location descriptions written once in this wizard and reused word for word in both prompts of a pair; the clip reference is a short label (below); clip grids, chaining between clips, the pack document and `browser-workflow.md` don't apply.

## How to ask

- **One step per turn, as tappable question cards.** One to three questions per card, two to four short options each, plus "You choose" and "Something else (I'll type)" where the answer is open.
- **Suggest, then ask.** Lead every step with a one-line recommendation based on what the user has said and on what VE does well.
- **Never ask what's already answered.** Pull answers from the user's message, image or existing prompt first. Show what was taken from it and ask only for confirmation or changes.
- **Keep a running summary.** After each step, show a short "so far" list so the user can correct anything.
- **Let the user skip ahead.** "You choose" or "just write it" fills the remaining steps with the suggested defaults, and says what they were.

## First use in a conversation: what's new

**Language first.** Before the first question, settle the user's language: the language of their first message, or, when it has no words of its own (only the skill's name or slash command), the language they have used earlier in this conversation, in saved memory or custom instructions, or set in the platform. Ask every question from here on in that language, translating the wording quoted below, and keep to it for the whole project (Work in the user's language). If nothing shows a language, use English.

**Translated copy (users who don't work in English).** Once the language is settled and it isn't English, check any persistent memory you can read (Claude's memory, a project memory file) for a "VideoExpress translated prompts" note; if there is one, use it and don't ask. If not, ask once (yes/no, question widget where available), in the user's language: "VideoExpress prompts are always written in English, because VideoExpress doesn't reliably understand other languages. Would you like me to also show each prompt translated into [language], so you can check what it does? You would still paste only the English version." Don't assume from the user's language that they need it: many users read English well. If memory is on, save one line whatever the answer: "VideoExpress translated prompts: yes ([language])." or "VideoExpress translated prompts: no.", and tell the user once: "I'll remember this, so I won't ask next time." Update the note if they change their mind. Without memory, ask once per conversation. On yes, show every image and clip prompt both ways (`multishot-template.md`, Translated copy for reading). This question is asked in development builds too.

The first time this skill is used in a conversation, whatever the user's first message is, ask this before anything else, as a yes/no question (use the question widget where one is available):

**Development builds skip this.** If this skill's `metadata.version` (in the frontmatter above) ends in `-dev`, skip the what's-new question altogether: don't ask it and don't save the memory note. Go straight to the user's first message.

**Once per version where memory allows.** First check any persistent memory you can read (Claude's memory, a project memory file) for a note that this version's what's-new question was already shown. If there is one, skip it. If not, ask it; then, if memory is on, save the one-line note "VideoExpress Prompt [version]: what's-new shown." and tell the user once: "I'll remember you've seen this, so I won't ask again for this version." Without memory, or when no note is found, ask as below: asking again is the safe fallback.

"VideoExpress Prompt has been updated to version [version]. Would you like a quick summary of what's new?" Take the version from this file's `metadata.version`, without any `-dev` suffix. On yes, read `references/changelog.md` and show its current release notes (the file's opening line says which sections) as a bulleted list: a short heading per version, newest first, then one short bullet per Headline and New item (a version's Fixed items can share one bullet). Never fold the notes into a sentence or a parenthesis.

Then answer the user's first message. If the skill was started with no message of its own (only its name or slash command), go straight to the Step 0 card, "Do you have something to start from?", as a question card, not a prose menu. When the first message already says what is wanted (an idea, an image, a prompt to improve, a failed take), act on it without asking what the user wants. Ask the what's-new question once per conversation, never again later in it.

**Chat or Code.** At the start, after the what's-new question, check whether you can reach the user's computer by listing or reading a local folder. If you can, you're in Code; say nothing. If you can't (no local file access, only a sandbox), you're in Chat: tell the user once, before anything else, "You're in Chat, so I can't open or save files on your computer. Upload any images here, and copy the prompts from the chat when they're ready. To work with files on your computer, use the Code tab in Claude Desktop."

**Name the conversation after the shot.** Once the shot has a subject (from the user's idea, image or prompt), rename the conversation to "[subject] · VideoExpress Prompt" if you have a tool that renames it (such as Claude Desktop's session title). Otherwise leave the name as it is.

## Companion products

**Companion product links.** Whenever you tell a user about Artistly, CloneVoice.ai or TalkingPhotos.ai and they don't have it (they said no, or haven't been asked yet), give its link once in that reply, each followed by "(affiliate link: the skill's author earns a commission if you buy)":
- Artistly: https://paykstrt.com/48893/180599
- CloneVoice.ai: https://paykstrt.com/56038/180599
- TalkingPhotos.ai: https://paykstrt.com/52357/180599

Never link a product the user already has, never more than once per product in a reply, and never as a sales pitch: name a product only where it genuinely helps the task, and always say the VideoExpress-only route works without it.

## Step 0: what have you got?

Card: **"Do you have something to start from?"** (multi-select)
1. An image (a start image, a frame or a character reference): ask them to attach it
2. An image prompt
3. A clip prompt
4. Starting fresh

Then: **"What do you want out of this?"**
1. A start-image prompt
2. A clip prompt (for an image I have or will make)
3. An image prompt and its clip prompt

**When the user brings something:**
- **An image:** read it before anything else. Note subject, framing, pose, props, environment and light exactly as drawn; the clip prompt must match the frame, not what was intended. Ask whether it's in their VE library already.
- **A prompt:** read it against `prompt-rules.md` and `multishot-template.md`. List what's working and what's at risk (missing tags, exclusions outside [NEGATIVES], quoted non-speech, text-bearing objects described with their text, a single sound block after the last segment, missing style anchor, and so on), in a short list. Pre-fill steps 1–7 from it and run them as confirm-or-change cards. If the user reports a failure with it, start from the table in `prompt-rules.md`.

## Step 1: look

What should it look like?
- **Style.** Link the catalogue so the user can see every style before choosing: [Style catalogue](https://github.com/ratava/videoexpress-scripting-skill/wiki/Styles) (one page and demo clip per style) and the [demo playlist](https://www.youtube.com/playlist?list=PLGPXytdy02o0). Suggest two or three styles from `styles/README.md` that fit the idea (default Cinematic Photoreal), and say whether each is a Create Mode preset or a custom style. Then read that style's sheet.
- **Aspect ratio:** Landscape 16:9 or Vertical 9:16.
- **Characters:** who is in it and what they look like (face, hair, build, outfit, signature accessory), written once as a block per `bible.md`. Ask whether they'll use **Consistent Character**, and whether a reference image of the character is already in the library. If not, offer a reference-image prompt (full length, plain grey background) as an extra image prompt; before writing it, ask how big the character is and explain the size guide beside them on the sheet (`bible.md`, reference sheet standard, point 10). If the user brings a reference they made themselves, inspect it against the reference sheet standard before using it, tell them what it misses and why, and ask "Use it as it is" or "Regenerate it" (their own image tool, VE Create Image, or Artistly if they own it) (`bible.md`, References the user brings). Two reference characters maximum (slot 1 and slot 2); Consistent Character off for shots with no characters. Consistent Character works on the image only. If the user wants it used for the clip, or wants a character who isn't in the start image to appear during the clip, run the Consistent Character check in `bible.md` every time: explain, link the [training video](https://youtu.be/CVeYOk7Rkf0), and ask "I am aware, just do it" or "Let's change the approach" before writing the prompt.
- **Where:** the location, including what is out of frame if the camera will move.

## Step 2: what happens

- **Image only:** the moment captured: subject, position in frame, how much of them is visible, pose and gaze. If a clip will follow, put the subject mid-action so the clip starts moving.
- **Clip:** the action in real time, in sequence. Suggest a length (3–10 s; about one small action per three seconds) and split it into timed `[ACTION t-ts]` segments. Say what stays still. Flag anything on the risky list in `prompt-rules.md` (counted events, actions relative to facing, a prop leaving the frame and returning) with a workaround.

## Step 3: any talking? (clips only)

If yes, ask first: **"Do you have an idea who is speaking and where?"**
- **Yes:** get the details: who speaks (two speakers maximum), where they are (in the scene and in the frame), what they say word for word, and how they sound (age, pitch, texture, accent, pace).
- **No:** offer two or three suggestions built from steps 1 and 2, each naming the speaker, where they are, a short line that fits the clip length, and a voice. The user picks one, adjusts it, or types their own.

Then:
- Recommend the method per `light-sound-dialogue.md`: **in the prompt** (Method A) by default, with or without action between the lines; **Lipsync HD** (Method B) when the user prefers it (it sizes the clip to the audio, but there's no pause between the two speakers and emotion tags such as [laugh] do nothing).
- Method A: one segment per line, sized to it (two short lines: 8 s as 0-4 s and 4-8 s), no pauses written between lines, a line, an action and a line in one clip while they fit 10 s with room to spare (split at the action when it's close); every speaker's face in frame.
- Method B: each actor's line under 100 characters. Output the dialog fields separately (below).

## Step 4: sound (clips only)

Production sound, or Video Only (No Sound)? With sound: suggest short, distinct sounds tied to each segment's action, one `[PRODUCTION SOUND t-ts]` block per segment. Steer away from sustained ambience, pitched tones and any request for silence; exclusions go to step 7.

## Step 5: camera (clips only)

Suggest **locked** unless the shot needs a move. A move is one per segment, named with its direction and physical nature (a push, not a zoom) and its end framing. A move must not enlarge a face or detailed prop beyond the size the opening frame shows it: if the user wants a closer shot, that's a new start image at that framing.

If the user wants the camera locked off, warn them before giving the prompt: VideoExpress has a known fault (confirmed by VE support, November 2026, fix in progress) where the camera can still move in a shot written as locked off. If it moves anyway, it is this fault, not the prompt; re-roll or pick the steadiest take rather than rewording the camera.

## Step 6: light and image

Key light direction and colour, fill or rim, time of day, and the style line from the style sheet (repeated in every segment for a clip). For a custom style, the style anchor opens the prompt. Effects add light, never replace it; keep a key light on the subject.

## Step 7: negatives

Negatives are for clip prompts only. Suggest the list: the style sheet's guards, anti-realism negatives for stylised looks, the clip's specific guards (camera reversing, new characters, face or costume drift, unwanted motion), sound exclusions, and "no text, no letters, no numbers, no logos, no watermark". Every exclusion lives in [NEGATIVES] and nowhere else, each written with "No". Ask what else the user wants kept out.

**Image prompts get no negatives** (`bible.md`, Image prompts carry no negatives). For an image, turn each thing the user wants kept out into the positive it stands for, in the section it belongs to: "the rest of the room empty", "her hands empty", "a blank, unlettered sign board", and show the user where each one went.

## Writing the prompts

- **Label.** Each video prompt starts with a short bracketed label so the library take can be found: `[Clip 1]` by default, or the user's own (`[Clip 1 TEST 1]` for test variants). Nothing goes before it. **Image prompts get no label:** VE paints it onto signs, boards and shirts in the image. Tell the user to rename the saved image in the Media Library instead (right-click its tile → Organize → Rename).
- **Image prompt:** follow the image-prompt recipe in `styles/README.md`, self-contained, with the full character, outfit and location wording inline and the head in frame. Prose or the tagged form in `bible.md` (Tagged start-image prompts) both work; use the one the user prefers.
- **Language:** ask the questions and explain each prompt in the user's language, and write every prompt in English, image or clip, with or without speech: tags, descriptions and negatives (`multishot-template.md`, Language). Only spoken lines stay in the user's language (plain double quotes, "speaking [language] as a native [language] speaker"). Tell the user why once; if they ask for the prompt in their language, explain instead of switching. If they asked for translated copies (Translated copy, above), show the English prompt first, then a warning not to use it and the translation (`multishot-template.md`, Translated copy for reading).
- **Clip prompt:** the tag order in `multishot-template.md`. In a pair, reuse the image prompt's exact character, outfit and location wording, and use the fresh-clip [REFERENCE USE] form. For a clip from the user's image, describe what the image shows.
- **Check before showing:** quotation marks only around spoken lines, once each; sign wording only in an image prompt (a clip keeps the lettering its opening frame shows), screens and anything else lettered described as abstract shapes and light; positives everywhere outside [NEGATIVES]; no [NEGATIVES] and no "no …" phrases in an image prompt; under about 6,000 characters (trim repeated style text and negatives first).

## Delivering

For each prompt, a heading, a short settings list, then the prompt alone in a code block (only the code block is pasted):

- **Image:** aspect ratio · Use Creative mode on · Automatically enhance my image prompt off · Consistent Character on or off, and which image goes in each slot.
- **Clip:** aspect ratio · opening image · Advanced Mode on, **Manual Video Length, sec** ticked and set to the clip's length · Automatically enhance my video prompt off · Video Only (No Sound) off when there is production sound · Lipsync HD Video off unless Method B.
- **Lipsync HD (Method B):** the main prompt holds no dialogue. Set the length **before** ticking Lipsync HD Video (ticking hides the length controls). Then give the dialog's three fields as separate code blocks: **Video Prompt** ("Actor 1 is [description, position], [action while speaking], [voice]. Actor 2 is …"), **Actor 1 Script**, **Actor 2 Script**. Remind the user to check the dialog's Total characters counter matches the lines.

For a pair: generate the image first and pick the best candidate. If what VE drew differs from the prompt (a prop in another place, a different framing), offer a revised clip prompt that matches the frame.

## After generation

- When the user reports a problem, diagnose the mechanism from the table in `prompt-rules.md` and give the **full revised prompt**, never a list of edits. If an image fix changes wording the clip prompt shares, give the clip prompt in full too.
- If a problem survives two rounds, suggest single-variable test takes, each with its own label (`[Clip 1 TEST 1]`, `[Clip 1 TEST 2]`), plus a control take of the last clean prompt.
- If the shot grows into several clips, chaining or a sequence, suggest moving to VideoExpress Scripting.
