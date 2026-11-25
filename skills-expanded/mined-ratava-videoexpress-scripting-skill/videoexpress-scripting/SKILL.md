---
name: videoexpress-scripting
description: Plan, script and produce multi-clip videos in VideoExpress (VE) 3.5 and later by PaulPonna.com, where each 3–10 second clip is a start image plus a motion prompt. Covers guided project intake from a concept or script, the Core Bible, the VE multishot prompt format, Create Mode and custom Creative mode styles, clip chaining, Consistent Character references, lip-synced dialogue (in the multishot prompt or the Lipsync HD dialog), production sound, and driving app.videoexpress.ai with Claude in Chrome. Use whenever the user wants to start or run a VideoExpress project, asks for VideoExpress image, video or multishot prompts, asks Claude to operate VideoExpress, or reports VideoExpress problems such as drifting characters or outfits, camera direction flips, stylised clips turning realistic, props changing shape, actions in the wrong place or order, dark scenes, text in footage, background hiss or unwanted music.
metadata:
  version: "2.8.0"
  author: Brent Wesley
---

# VideoExpress Scripting

Produce a production-ready **prompt pack**: a living document that maps a full piece (song, narration, story) onto a sequence of clips, each with a start-image plan and a paste-ready VE multishot prompt. Then support generation: diagnose reported failures, fix them globally, sweep every affected clip.

Two facts drive almost everything in this skill:

1. **The model renders nouns, not intentions.** Every noun, count, simile and stray token is a candidate to appear on screen.
2. **Each generation only knows what it is given.** A chained clip sees one still image (the previous clip's last frame) plus the prompt. It has no memory of the previous clip's motion, of anything that was out of frame, or of earlier prompts. Anything not visible in the opening frame or described in the prompt will be invented.

## Where to read next

Read only what the current step needs. Everything in `references/` is self-contained.

| When you are… | Read |
|---|---|
| Starting a new project, or the user has a concept or script | `references/project-intake.md` — the question system, feasibility check, development tests, brief and Core Bible sign-off |
| Writing or revising character, outfit or location blocks; start images; Consistent Character references; non-human characters | `references/bible.md` |
| Choosing a look, or writing any prompt in a Create Mode or custom style | `references/styles/README.md` (shared recipe and index), then the one style sheet you need |
| Planning a narrated story (stickman videos, fables, children's stories told by a narrator) | `references/narrated-story.md` |
| Writing any video prompt | `references/multishot-template.md` — the tag structure, blank template and worked example |
| Planning the clip grid, chaining, camera moves, or any [ACTION] segment | `references/camera-and-motion.md` |
| Writing [LIGHT AND IMAGE] or [PRODUCTION SOUND], any clip with speech, or point-of-view / HUD shots | `references/light-sound-dialogue.md` |
| Writing or debugging any prompt; the user reports a failure | `references/prompt-rules.md` — how the engine reads a prompt, and the failure → cause → rule table |
| Asked to drive app.videoexpress.ai with Claude in Chrome | `references/browser-workflow.md` — read first, follow step by step |

For a single prompt request mid-project, the usual set is `multishot-template.md` + `prompt-rules.md` + whichever of `bible.md`, `camera-and-motion.md`, `light-sound-dialogue.md` and a style sheet the clip touches. For a reported failure, start with the table in `prompt-rules.md`.

## Workflow

0. **Intake** — run `references/project-intake.md` (after the what's-new questions below, if this is the skill's first use in the conversation): starting point (concept or script), decision checklist with suggestions, feasibility check, any development tests, sign-off on the brief and Core Bible.
1. **Concept** — scenes, motifs, characters, world, and a visual arc mapped to the source's structure (below).
2. **Bible** — locked character blocks, outfit blocks and location blocks, written once and pasted verbatim everywhere (`bible.md`).
3. **Timing** — a clip grid at the tool's clip length, with key hits verified against the real audio by the user (`camera-and-motion.md`).
4. **Prompt pack** — start-image prompts and multishot video prompts for every clip (`multishot-template.md` plus the relevant references).
5. **Generation support** — diagnose reported failures by mechanism, fix them globally, sweep every affected clip (`prompt-rules.md`).

When the script is signed off, start production in the same reply: if Claude operates VE, ask whether to open the VideoExpress tabs in Chrome now, and give the first paste-ready prompt with its settings whoever operates (`references/project-intake.md`, Starting production).

The pack is a living document. Expect many revision rounds as the user generates clips.

**Show it, then ask.** Whenever something needs the user's decision or sign-off (the brief, the Core Bible, the script, the pack or a revised section of it, a start image, a take), put the thing itself in the reply first: the full text of what is being signed off, or for an image or take, which one it is and what a correct one shows. A file path with a summary is not something the user can sign off. For a long pack, show in full the sections that need a decision and list the others by heading with a one-line note each. Then ask with the question tool where there is one (AskUserQuestion in Claude Code, the options widget in the Claude apps), not with a question in prose: one question per decision, and options that are the real choices ("Approve", "Change something (I'll type)", or the candidates to pick from). Ask in plain text with numbered options only where there is no question tool.

## First use in a conversation: what's new

**Language first.** Before the first question, settle the user's language: the language of their first message, or, when it has no words of its own (only the skill's name or slash command), the language they have used earlier in this conversation, in saved memory or custom instructions, or set in the platform. Ask every question from here on in that language, translating the wording quoted below, and keep to it for the whole project (Work in the user's language). If nothing shows a language, use English.

**Translated copy (users who don't work in English).** Once the language is settled and it isn't English, check any persistent memory you can read (Claude's memory, a project memory file) for a "VideoExpress translated prompts" note; if there is one, use it and don't ask. If not, ask once (yes/no, question widget where available), in the user's language: "VideoExpress prompts are always written in English, because VideoExpress doesn't reliably understand other languages. Would you like me to also show each prompt translated into [language], so you can check what it does? You would still paste only the English version." Don't assume from the user's language that they need it: many users read English well. If memory is on, save one line whatever the answer: "VideoExpress translated prompts: yes ([language])." or "VideoExpress translated prompts: no.", and tell the user once: "I'll remember this, so I won't ask next time." Update the note if they change their mind. Without memory, ask once per conversation. On yes, show every image and clip prompt both ways (`multishot-template.md`, Translated copy for reading). This question is asked in development builds too.

**Resuming comes first.** When the first message has no words of its own (only the skill's name or slash command) or asks to carry on, look for a prompt pack before asking anything: one attached to the message, in a Claude Project's files, the working folder, earlier in this conversation, or named in a saved "VideoExpress project" memory note. If you find one, show the "How do you want to start?" card at once with "Continue [project]" as its first option (`references/project-intake.md`, Step 1). When the user picks it, or the first message already asks to continue, follow Resuming a project (below) and hold the what's-new and companion questions until the next prompt has been given; then ask them as usual. When the user picks another option, ask them then, before intake.

The first time this skill is used in a conversation, whatever the user's first message is (a new project, a single prompt, a question about the skill, a reported problem), ask these before anything else, as yes/no questions, one at a time (use the question widget where one is available):

**Development builds skip this.** If this skill's `metadata.version` (in the frontmatter above) ends in `-dev`, skip the what's-new questions altogether: don't ask them and don't save the memory note. Go straight to the user's first message.

**Once per version where memory allows.** First check any persistent memory you can read (Claude's memory, a project memory file) for a note that this version's what's-new questions were already shown. If there is one, skip both questions. If not, ask them; then, if memory is on, save the one-line note "VideoExpress Scripting [version]: what's-new shown." and tell the user once: "I'll remember you've seen this, so I won't ask again for this version." Without memory, or when no note is found, ask as below: asking again is the safe fallback.

1. "VideoExpress Scripting has been updated to version [version]. Would you like a quick summary of what's new?" Take the version from this file's `metadata.version`, without any `-dev` suffix. On yes, read `references/changelog.md` and show its current release notes (the file's opening line says which sections) as a bulleted list: a short heading per version, newest first, then one short bullet per Headline and New item (a version's Fixed items can share one bullet). Never fold the notes into a sentence or a parenthesis.
2. For each **Headline** item in those current release notes that has a question, unless its "Skip if" condition holds: ask its question. On yes, give the install link and say it opens the install steps: for VideoExpress Prompt, https://github.com/ratava/videoexpress-scripting-skill/wiki/Install-VideoExpress-Prompt#claude-desktop (Claude Desktop; the same page covers other platforms).

Then answer the user's first message, or start intake for a new project. If the skill was started with no message of its own (only its name or slash command) and no pack was found (Resuming comes first, above), treat it as a new project: go straight to the "How do you want to start?" card (`references/project-intake.md`, Step 1), as a question card, not a prose menu. When the first message already says what is wanted (an idea, a script, a single prompt, a failed take), act on it without asking what the user wants. Ask the what's-new questions once per conversation, never again later in it.

**Chat or Code.** At the start, after the what's-new questions, check whether you can reach the user's computer by listing or reading a local folder. If you can, you're in Code; say nothing. If you can't (no local file access, only a sandbox), you're in Chat: tell the user once, before anything else, "You're in Chat, so I can't open or save files on your computer. Upload any scripts or images here, and download the pack when it's ready. For a full project, the Code tab in Claude Desktop works with your files."

**Companion products.** On the skill's first use, after the questions above, ask once (yes/no, question widget where available): "Do you have Artistly or CloneVoice.ai? They're PaulPonna's companion products to VideoExpress (sold separately): Artistly makes stronger still images, and CloneVoice.ai makes voices." On no, carry on with VE alone and don't ask again, unless the user later says they've bought one: then offer the key check below and update the saved note. On yes, note which, then:
- If you can operate the user's browser, ask: "Can I check in your browser that its API key is added to VideoExpress?" On yes, check Edit profile (`references/browser-workflow.md`, Linked companion products) and report only whether each key is there, never the key itself. On no, or without browser access, ask the user to look themselves: account name (top right) → **Edit profile** → the Artistly.ai and CloneVoice.ai API key fields.
- A key in the field means the product is linked. If one is missing, tell the user they can paste their own key into that field and click **Save**; never ask them to share the key with you.
- Use Artistly and CloneVoice routes only for a product the user has (Artistly for start images, especially with a style's "Artistly match"; CloneVoice for voice samples and narration). Everything else stays VE-only.
- **Remember the answer for next time.** First check any persistent memory you can read for a "VideoExpress companion products" note; if there is one, skip the question and use it. Otherwise ask, and once answered (and checked, if the user agreed), save one line whatever the answer, a no included: "VideoExpress companion products: Artistly linked, CloneVoice none." Tell the user once: "I'll remember this, so I won't ask next time." Update the note if the user later says they've bought or linked one. Without memory, ask once per conversation.

**Companion product links.** Whenever you tell a user about Artistly, CloneVoice.ai or TalkingPhotos.ai and they don't have it (they said no, or haven't been asked yet), give its link once in that reply, each followed by "(affiliate link: the skill's author earns a commission if you buy)":
- Artistly: https://paykstrt.com/48893/180599
- CloneVoice.ai: https://paykstrt.com/56038/180599
- TalkingPhotos.ai: https://paykstrt.com/52357/180599

Never link a product the user already has, never more than once per product in a reply, and never as a sales pitch: name a product only where it genuinely helps the task, and always say the VideoExpress-only route works without it.

**Name the conversation after the project.** Once a new project has a working title (from the user's idea or the brief), rename the conversation to "[title] · VideoExpress" if you have a tool that renames it (such as Claude Desktop's session title). Otherwise leave the name as it is.

## Concept design

- Design **2–4 recurring motifs** that carry the video (an accent colour, a gesture, a light effect, a returning prop). Motifs give continuity AI generation can't provide on its own.
- Map source structure to a **scene table**: scene → time range → clips → outfit → location → motif state. Escalate motifs across scenes.
- **Key moments deserve visual events.** Big hits or key lines get reveals or bursts of motion, build-ups get stillness so the hit lands, and scene changes land on section boundaries.
- **Give each scene a logical opening.** Establish the character arriving, noticing something, or reacting before the main action.
- Favour what generates reliably: steady camera moves, light changes, drifting atmosphere, one clear subject. Spectacle in the background, performance in the foreground.
- Dialogue is lip-synced two ways (a quoted line in the multishot prompt, or the Lipsync HD dialog; see `light-sound-dialogue.md`). In shots without dialogue, keep mouths closed or out of view so no speech is invented, and never end a clip with something in the mouth or food in a hand if the next clip has dialogue.
- Background interest (vehicles, crowds, city life) is named explicitly and kept at a distance so it never crosses the subject.

## Rules that apply to every prompt

These are the ones that cause the most damage when forgotten. The references hold the detail and the rest.

- **When following a prompt pack, every video prompt starts with its clip reference in square brackets,** exactly as the pack declares it: `[Clip 12]`, or `[Clip 12 TEST 1]` for a test variant. It comes first, before any style anchor or [REFERENCE USE], so every take can be matched to the pack. **Image prompts carry no reference:** VE paints it onto signs, boards and shirts. Rename each saved image tile to its reference (Image 12A) instead. Details in `multishot-template.md`.
- **Work in the user's language; write every prompt in English.** Talk to the user in the language they use with you (or have set): questions, the script, pack notes, headers and explanations. **Every image and video prompt is written in English**, with or without speech: tags, bible blocks, style lines and negatives. Only spoken lines stay in the user's language, in plain double quotes and with "speaking [language] as a native [language] speaker" in each voice. VE's model doesn't reliably understand other languages, and partial translation doesn't work. Write the bible in English and describe each block in the user's language for sign-off. Tell the user why, once; if they ask for prompts in their language, explain instead of switching. If they asked for translated copies (Translated copy, above), show each prompt in English first, then a warning not to use it and the translation. Details in `multishot-template.md` (Language).
- **Bible blocks are pasted word for word.** Paraphrase is drift. When a start image nails the look, the video prompts reuse that image prompt's exact wording, not the bible's older wording.
- **Match the frame, not the plan.** Look at the chained opening frame or accepted start image before writing: describe props, framing and the geometry of obstacles exactly as the frame shows them.
- **Quotation marks mean speech.** Quote each spoken line once, in [ACTION], and quote nothing else. Two speakers per clip, maximum.
- **Positives everywhere except [NEGATIVES].** VE reads every other section as things to include, even with "no", "not" or "never" in front, so state what should exist and what stays still, and put every exclusion in [NEGATIVES], each written with "No" ("No music, no hum"). Lead every segment with the subject's motion. Image prompts have no [NEGATIVES] at all: state each exclusion as its positive ("the rest of the terrace empty", "a blank sign board").
- **Camera: locked unless asked, every move named identically in every clip, every move has a destination, never return to space that has left the frame.** Never write a move relative to another clip. **Locked-off shots: warn first.** VideoExpress has a known fault (confirmed by VE support, November 2026, fix in progress) where the camera can still move in a shot written as locked off. Whenever a scene needs a locked-off camera, tell the user once, before they generate it, that if the camera moves anyway it is this VE fault, not their prompt; then don't keep rewording the camera (`camera-and-motion.md`).
- **A detail holds only at the size VE last drew it.** A push-in that enlarges a face or prop, or a prop that leaves the frame and comes back, makes VE redraw it from text. Start each clip from a start image at its closest framing; a closer shot is a new clip.
- **Chaining: flag detail risk, don't dictate.** A chained clip opens on the take's last frame, and a detail holds only at the size VE last drew it. When a planned chain risks detail drift (a closer framing than the last frame, a pull-away and return, a detailed face or prop small in the last frame), say so once per project or pack section (an episode, say) in that section's Global rules, with the options: keep the framing matched, re-roll the parent, or start from a new start image. How to chain is the user's choice.
- **No counted events. Lettering comes from the start image, never the clip prompt.** VE keeps lettering the start image already shows and garbles text it has to invent. Name a sign's wording in the image prompt, drawn large and well inside the frame; in the clip prompt don't spell or quote it: say the sign keeps exactly the lettering shown in the opening frame, with "No new text, no changing or morphing letters" in [NEGATIVES]. Screens whose content changes, and signs the start image shows blank, are abstract shapes and light (`multishot-template.md`, Text-bearing objects).
- **Effects add light, never replace it.** Keep a key light on the subject; restate brightness in the final segment; never chain from a darkened frame.
- **One [PRODUCTION SOUND] block per segment, with the segment's time label;** a single block after the last segment binds to that segment only and leaves the rest to VE, often as music. **Transient sounds tied to actions; never ask for silence (it renders as rumble and crackle); fit the clip length to the action and speech; close each block with what is heard in that segment.**
- **Stylised looks need the style anchor at the very start of the video prompt** (straight after the clip reference, before [REFERENCE USE]) and in every [LIGHT AND IMAGE], plus anti-realism negatives.
- **Keep "Automatically enhance my video prompt" off.** It rewrites to short prose and drops the bible, time labels and clip reference. Aim to keep video prompts under about 6,000 characters and image prompts under about 2,000, the lengths VE's developers advise (advice, not hard limits; longer has worked); trim repeated style text and negatives first.
- **Turn Consistent Character off** when making start images with no characters (empty environments, point-of-view, inserts). It affects Create Image only; Create Video ignores it.
- **Inspect references the user brings.** A reference image or sheet the user made themselves is checked against the reference sheet standard before any prompt or plan uses it. Tell them you are checking; if it misses a point, say which and why, and ask "Use it as it is" or "Regenerate it" (their own image tool, VE Create Image, or Artistly if they own it). Never keep a problem you noticed to the pack, a memory note or your own reasoning (`bible.md`, References the user brings). Sheets made during the project, regenerations included, get the same check before they go in a slot.
- **Consistent Character check: ask every time.** A clip's characters come from its start image and its prompt only. When the user wants Consistent Character used for a clip, says it is what put a character in a clip, or wants a bible character who isn't in the start image to appear during the clip, stop before writing the prompt or changing the pack: explain in a sentence or two, link the training video ([Consistent Character in VideoExpress](https://youtu.be/CVeYOk7Rkf0)), and ask a two-option question card, **"I am aware, just do it"** or **"Let's change the approach"**. Ask it every time it comes up; one answer never covers the rest of the pack. Never plan either yourself, and never rewrite the pack to say Consistent Character works in video. What each answer leads to: `references/bible.md` (The Consistent Character check).

## The prompt pack document

0. **Progress** (at the very top): last accepted clip and its take, next clip and how it starts (FRESH from image X or CHAIN from clip N), clips left to generate, open issues and any rules added during production, and the date updated. Update it whenever the user accepts a take or a revision changes what comes next; it's what a new conversation reads to resume.
1. **Overview**: scene table (scene, clips, time range, outfit, VE length); prompt format note; references to supply with each clip; paste rule (only text inside code blocks is pasted; headings carry metadata).
2. **Global rules**: the rules above and from the references that apply to this project.
3. **Bible**: character core block, outfit blocks, location blocks, style line.
4. **Per scene**: start images (each with a declared reference such as Image 12A, and a self-contained prompt with no bracketed reference), then per clip — header line (clip reference such as Clip 12 · time range · VE length · FRESH from image X or CHAIN from clip N · role tag) and the full multishot prompt, starting `[Clip 12]`, in a code block.
5. **Edit, timing and QC**: transitions, the per-take QC checklist (in `prompt-rules.md`), open items.

For alternates, add a new tab or section rather than overwriting working clips, and include any adjacent clips that must change to hand off correctly. Keep clip and image references stable once generation starts, since they are what identify the takes; if clips are cut, keep the gaps and note them. Alternates get their own reference (Clip 12B), never a reused one.

## Resuming a project

A project carries over between conversations in its pack, not in memory: memory can be off, differs between platforms and holds only short notes.

- **When the pack is first delivered,** tell the user once to keep the latest pack where you can find it next time (a Claude Project's files, the working folder, or attach it to the first message). If memory is on, save one line: "VideoExpress project: [project], pack in [where]." and update it if the pack moves.
- **To resume,** read the pack's Progress block and the clips around the next one, then confirm in one line ("Back on [project]: Clip 14 accepted, next is Clip 15, CHAIN from Clip 14."). For a chained clip, ask for the last accepted take's final frame or the take itself, and write the next prompt to match what actually rendered. Then give the next prompt in full, paste-ready, with its settings.
- **No Progress block** (an older pack): ask which clip was last accepted, then add the block.
- **No pack found** but the user wants to continue: ask them to attach the latest pack, or add it to the project files. Never rebuild a pack from memory notes or from what you recall of earlier conversations.

## Working style during production

- Users report failures one at a time, often with a frame. Diagnose the **mechanism** (table in `prompt-rules.md`), fix it globally, and sweep every not-yet-generated clip with the same risk.
- Read the frame the user sends: note what actually rendered and write the next prompt to match what exists.
- When the user edits the pack directly, re-read before writing and never overwrite their changes without saying so.
- When the user states a preference ("keep it", "I prefer this look"), treat it as a new rule and apply it everywhere, including rewriting the bible block to match the frame.
- Protect payoff shots: guard their preconditions in every earlier prompt.
- **When the user asks to see a prompt before a run, show the full paste-ready prompt,** then ask to run it. Don't run first.
- **Isolate stubborn failures.** When a problem survives two prompt rounds, stop rewording. Hold a base prompt fixed and run one take per variant, each changing one variable, with a unique reference per variant (`[Clip 12 TEST 1]`, `[Clip 12 TEST 2]`), plus a control take of a previously clean prompt. Record which variables mattered.
- **Know when to stop.** If a sequence has drifted far from the concept, say so and offer to restart the sequence or the project rather than patching clip by clip.

## Operating VideoExpress in the browser

When the user wants Claude to drive app.videoexpress.ai itself rather than just write the pack, read `references/browser-workflow.md` first and follow it step by step. The user approves every start image, take and prompt change; Claude pastes prompts exactly as written, never skips a checkpoint, and leaves drift judgements to the user unless a problem is obvious. Prompt hardening from a generated frame is offered after the first clip is on the timeline, and again after the second if deferred.

Claude only acts while replying and each reply has an action budget, so never wait inside a reply for renders. Submit the takes, confirm they exist, report their positions, and ask straight away which take to keep, saying what it should look like; don't ask whether the renders have finished. Never announce an action ("generating now") without performing it in the same reply.
