---
name: gemini-omni-flash-video-editing
description: Prompting playbook for Gemini Omni Flash, Google's create-anything-from-anything video model. Use when generating or editing short video clips with Omni Flash (also nicknamed "nano banana for video"): conversational editing of existing footage, visual effects, kinetic captions for vertical/shorts content, or text-to-video generation. Covers the four golden editing rules, the six structural prompt dimensions, and the four fix phrases that resolve most bad outputs.
---

# Gemini Omni Flash Video Editing

Prompting playbook distilled from Google Cloud's workshop "Unlocking the future of video editing with AI: introducing Gemini Omni Flash" (https://www.youtube.com/live/oQQUg957xWY). Organized to be used as a cheat sheet during actual editing sessions.

## How to use this skill (human quick start)

1. **Open Google Flow** (https://labs.google/fx/tools/flow), create a New project. If offered, pick the Omni Flash model, set outputs per prompt to 1, and choose your aspect ratio (9:16 for shorts and reels, 16:9 for landscape).
2. **Generating from scratch:** build your prompt from this fill-in template, which covers the six dimensions plus the fix phrases:

   One continuous shot. Location: [where]. Camera: [angle and movement]. Lighting: [light source and mood]. Style: [visual style]. [0-Xs] [what happens first]. [X-Ys] [what happens next]. Audio: [named instruments and tone, or "no audio"]. No dialogue, no subtitles, no logo.

3. **Editing a clip you have:** upload it (10 seconds max), then request exactly one change and always end with "Keep everything else the same." One change per message. After about three edit turns, save the best version, open a fresh session, and continue from that saved clip.
4. **Captions for shorts:** upload your footage plus an image of the text style you want (a lettering sample, a brand asset), and ask for word-by-word dynamic captions matching the transcript.
5. **Longer videos:** generate or edit 10-second keeper clips and chain them on Flow's timeline.
6. **Working with an agent:** tell the agent to read this file first, then have it compose the prompts while you (or it, where access allows) run them in Flow. Mind the Execution surface rule below.

## Execution surface (Kamilla's rule, 2026-08-25)

Run Omni Flash generations on Google-native surfaces covered by existing Google plans: Google Flow (https://labs.google/fx/tools/flow), the Gemini API, or the Gemini Enterprise Agent Platform. Do NOT default to third-party credit-metered providers (Higgsfield or similar) for this model; use one only if Kamilla explicitly approves the spend for that run. Origin of the rule: on 2026-08-25 an agent testing this skill spent Higgsfield credits by default; Kamilla corrected that the whole point of the skill is to use the Google-native access she already has.

## Model spec sheet (as of the 2026-08 session)

- Inputs: text, photos, audio, and existing video clips, all in a single prompt, read simultaneously.
- Output: max 10 seconds, in 1-second increments; chain keeper clips for longer videos.
- Resolution: native 720p today, higher resolutions announced as coming.
- Formats: vertical 9:16 and horizontal 16:9.
- Audio: natively generated with the video (sound effects, music, dialogue).
- Consistency: up to 5 reference images to lock a face, wardrobe, or product line.
- Safety: invisible SynthID watermark plus C2PA metadata on outputs.
- Availability: Gemini Enterprise Agent Platform, the API, and Google Flow.

## Workflow 1: edit existing footage by conversation

1. Upload a clip up to 10 seconds (phone footage, B-roll, an owned brand ad).
2. Ask for exactly one change, naming what to fix and what to preserve.
3. Iterate turn by turn, following the four golden rules.

### The four golden rules

1. **One change per turn.** Multi-part requests cause unintentional collateral edits. Split them.
2. **Always add the preserve clause:** "keep everything else the same." Skipping it gives the model permission to reimagine the whole scene.
3. **Don't repeat the whole prompt.** The model has stateful memory; re-describing the scene invites it to redo everything from scratch.
4. **Re-anchor after roughly three edits.** Max three turns per session for best quality. Save the keeper clip, open a fresh chat, upload it as the new starting point, continue.

## Workflow 2: visual effects

Capabilities demonstrated: full restyling (film noir, claymation, watercolor) with motion preserved; scene relighting (recalculated, not color-filtered); object insertion and removal with clean edges and correct shadows; material transformations; physics-true effects (smoke, fire, gravity); background rebuilds behind a moving subject with no rotoscoping or green screen.

**Graphic-consistency technique:** upload a sticker sheet or style asset alongside the video and prompt "edit this keeping everything the same, add animated motion elements..." The model reasons across both assets and maps the sheet's graphic style onto the moving footage.

## Workflow 3: kinetic captions (shorts and vertical content)

Single-pass generation of: word-by-word captions synced to speech, animated lower thirds, titles in any texture (neon on brick, carved stone), animated brand assets straight from PNG or JPEG, and full vertical 9:16 edits with captions, B-roll, and sound.

**Style-matching technique:** upload an asset image of the desired text style (the demo used a 3D plush alphabet) with the footage and prompt for dynamic captions matching the transcript. The rendered text inherits the asset's material look.

## The prompting playbook

**Cover all six structural dimensions in generation prompts:** camera, style, lighting, location, text, audio.

**Four fix phrases that solve most "why did it do that" problems:**

1. **"One continuous shot."** By default the model plays director and slices clips into multiple cuts; this locks the camera down.
2. **Direct audio precisely.** "Cinematic score" is too vague; name instruments and tone ("melancholic piano"), or command "no audio" for silence. Undirected audio means the model guesses.
3. **Use timestamp brackets** for second-level control: "[0-3s] she walks in. [3-6s] she stops and turns." Controls drops, reveals, and action beats.
4. **Ban what you don't want** with negative rules at the end of the prompt: "no dialogue, no subtitles, no logo."

**Bonus technique:** the model can sync visuals to an uploaded audio track (the demo synced apartment window lights turning on to music), reasoning across video, image, audio, and text inputs in one prompt.

## Verification

Live-tested 2026-08-25 in Google Flow (Kamilla driving, agent-composed prompts): a baseline generation using the six-dimension formula plus fix phrases produced one continuous shot with the three specified words appearing one at a time in the final seconds, matching the playbook's claims.

## Source lineage

- Drive WORKFLOW doc: https://docs.google.com/document/d/1q-WWTtSvMMyOelDJp0c4HLU3F-zli2xeKv0WMaLWGhg/edit
- Drive source transcript: https://docs.google.com/document/d/1ht5V3gFT6Dqawktt4qWk7zrdt2X09tUl44zWA_07MVo/edit
- Source video: https://www.youtube.com/live/oQQUg957xWY
- Adopted as a Baza-registered skill per Kamilla's decision on 2026-08-25 (TODO-2026-08-25 task 27, "YouTube Videos to Workflows").
