---
name: enhancor
description: enhancor lets the user generate any type of video through a guided, conversational workflow using the Seedance 2.0 / Enhancor API, asking the right questions in the right order and delivering the finished video to Telegram so they can create marketing clips, promotional content, or visual assets without navigating complex video production tools.
---

---

## What This Skill Does

This skill enhancor lets the user generate any type of video through a guided, conversational workflow using the Seedance 2.0 / Enhancor API, asking the right questions in the right order and delivering the finished video to Telegram so they can create marketing clips, promotional content, or visual assets without navigating complex video production tools.

## Step 1 — TYPE
**"What type of video do you want to create?"**

### Type A: `text-to-video`
Pure text prompt → video. No images or assets needed.
> *"A man riding a bike through a park at sunset"*

### Type B: `image-to-video`
One or more reference images → video. The image(s) are animated into motion.
> *"Make this product photo come alive with the model holding it"*

---

## Step 2 — MODE (image-to-video only)
**"What generation mode?"**

| Mode | What It Does | Best For |
|------|-------------|----------|
| `ugc` | Influencer/product UGC-style videos | Social ads, product demos, influencer content |
| `multi_reference` | Multiple reference images guide the output | Animating a scene with multiple visual references |
| `extend` | Extend an existing video forward | Continuing a video beyond its original length |
| `multi_frame` | Scene-by-scene control with timed prompts | Cinematic sequences, step-by-step storytelling |
| `lipsyncing` | Lip-sync audio to a character | Talking head videos, dubbed content |
| `voice_clone` | Clone a voice and sync to character | Voiceover with a specific person's voice |
| `first_n_last_frames` | Interpolate between first and last frame | Smooth transitions, animation from sketches |

---

## Step 3 — MODE-SPECIFIC ASSETS

Each mode needs different inputs. I only ask for what your mode requires.

### For ALL image-to-video modes:
**"What reference image(s) do you want to use?"**
- Provide 1 to 9 publicly accessible image URLs
- The more relevant the image is to your prompt, the better the output

### For `ugc` mode specifically:
**"What product and/or influencer images do you want to use?"**
- `products` — Image(s) or short video(s) of your product (up to 9 total combined with influencers+images)
- `influencers` — Image(s) or short video(s) of the person/content creator (up to 9 total combined)
- Reference them in your prompt: `@product_image6`, `@influencer_image9`
- Example prompt: *"The influencer holds up the @product_image6 and smiles at the camera"*

### For `extend` mode:
**"What video do you want to extend?"**
- Provide the existing video URL

### For `multi_frame` mode:
**"Describe each scene segment"**
- For each segment, I'll collect: `prompt` + `duration` (4–15s per segment)
- Example:
  - Segment 1: "Wide shot of a city skyline at dawn" — 5s
  - Segment 2: "Camera pushes in toward the tallest tower" — 4s

### For `first_n_last_frames` mode:
**"What's the first frame?"**
- First frame image URL

**"What's the last frame?"**
- Last frame image URL

### For `lipsyncing` / `voice_clone` mode:
**"What's the audio?"**
- Lip-sync audio URL (the audio to sync to the character)

### Reference media rules (non-ugc modes):
- `images`: up to 9 image URLs
- `videos`: up to 3 video URLs (combined duration must be under 15s)
- `audios`: up to 3 audio URLs (combined duration must be under 15s)
- All URLs must be publicly accessible

---

## Step 4 — PROMPT
**"Describe the video scene"**

Tips for great prompts:
- **Action:** What is the subject doing? *"A man riding a bike"*, *"The product is held up and rotated"*
- **Camera:** How should it move? *"slow zoom in"*, *"pan left to right"*, *"static wide shot"*, *"dolly forward"*
- **Environment:** Where is it? *"sunny park"*, *"modern kitchen"*, *"golden hour light"*, *"urban street"*
- **Mood:** What feeling? *"cheerful"*, *"dramatic"*, *"candid"*, *"cinematic"*
- **UGC mode:** Reference your assets: *"@influencer_image3 picks up the @product_image7 and examines it"*

---

## Step 5 — DURATION
**"How long should it be?"**
- Range: 4–15 seconds
- Default: 5 seconds

---

## Step 6 — RESOLUTION
**"What resolution?"**
| Option | Quality | Speed |
|--------|---------|-------|
| `480p` | Standard | Fastest |
| `720p` | HD | Medium |
| `1080p` | Full HD | Slowest (requires `fast_mode: false`) |

---

## Step 7 — ASPECT RATIO
**"What aspect ratio / platform?"**
| Ratio | Best For |
|-------|----------|
| `16:9` | YouTube, standard video |
| `9:16` | TikTok, Reels, Shorts (vertical) |
| `4:3` | Facebook, general video |
| `3:4` | Instagram portrait |
| `1:1` | Instagram Feed square |
| `21:9` | Cinematic ultrawide |

---

## Step 8 — FULL ACCESS
**"Should human faces be allowed?"**
- `true` — Allow human faces to generate (recommended)
- `false` — No human faces

---

## Step 9 — FAST MODE
**"Use fast mode?"**
- `true` — Quick generation (uses faster model)
- `false` — Standard model (required for 1080p)

---

## Step 10 — WEBHOOK (optional)
**"Do you have a webhook URL?"**
- If yes: I include it and the API notifies you when done
- If no: I submit without it and poll for you — same result, just slightly more polling

---

## Step 11 — CONFIRM & GENERATE

I summarize everything and ask: *"Ready to submit?"*

Once you confirm, I:
1. Submit the job to Seedance/Enhancor
2. Poll until `COMPLETED` (typically 30–90 seconds)
3. Send the video + thumbnail directly to Telegram

---

## Quick Decision Tree

```
You want to create a video
├── From text only?
│   └── → TYPE: text-to-video → Step 4 (prompt)
├── From one or more images?
│   ├── Influencer/product social ad?
│   │   └── → TYPE: image-to-video → MODE: ugc
│   ├── Animate a single photo?
│   │   └── → TYPE: image-to-video → MODE: multi_reference
│   ├── Extend an existing video?
│   │   └── → TYPE: image-to-video → MODE: extend
│   ├── Multiple scenes with timed control?
│   │   └── → TYPE: image-to-video → MODE: multi_frame
│   ├── Character talking / lip-sync?
│   │   └── → TYPE: image-to-video → MODE: lipsyncing
│   ├── Voice clone?
│   │   └── → TYPE: image-to-video → MODE: voice_clone
│   └── Animate between two frames?
│       └── → TYPE: image-to-video → MODE: first_n_last_frames
```

---

## Full Asset Reference

| Asset | Modes | Max | Notes |
|-------|-------|-----|-------|
| `images` | non-ugc | 9 | Reference image URLs |
| `videos` | non-ugc | 3 | Combined video duration <15s |
| `audios` | non-ugc | 3 | Combined audio duration <15s |
| `products` | ugc | 9 total | Images or short videos of product |
| `influencers` | ugc | 9 total | Images or short videos of person |
| `first_frame_image` | first_n_last_frames | 1 | First frame URL |
| `last_frame_image` | first_n_last_frames | 1 | Last frame URL |
| `lipsyncing_audio` | lipsyncing, voice_clone | 1 | Audio URL |
| `multi_frame_prompts` | multi_frame | — | Array of {prompt, duration} objects |

---

## API Reference
- **Base URL:** `https://apireq.enhancor.ai/api/enhancor-ugc-full-access/v1`
- **Auth:** `x-api-key` header
- **Key:** stored in `.secrets/enhancor.env`
- **Submit:** `POST /queue`
- **Poll:** `POST /status` with `request_id`

---

## Notes
- All media URLs must be publicly accessible (not behind login or localhost)
- Duration must be 4–15 seconds
- 1080p requires `fast_mode: false`
- Human face generation requires `full_access: true`
- Generation time: typically 30–90 seconds depending on resolution and server load
