---
name: ai-video-agency-magnific
description: >
  Full-service AI video agency workflow built entirely on the Freepik/Magnific MCP
  connector (no CLI, no separate account). Turns a single reference photo into a
  complete cinematic multi-scene video with consistent character identity:
  character library asset → transformation morph → story scenes → reverse
  transformation. Use this skill whenever the user wants to create an AI video
  story, transform themselves into a character, make a multi-scene/multi-clip
  video, produce a YouTube short or hook, create an ad or brand story from a photo,
  or says things like "make a video of me as X", "tell a story with my photo",
  "create AI clips", "video storytelling", or "KI Video". Also trigger when the
  user provides a portrait/selfie and wants any kind of narrative video from it.
  Adapted from Arnie936/ai-video-agency (Higgsfield CLI edition) for the
  Freepik/Magnific MCP tools — see README.md for source and changelog.
---

# AI Video Agency (Magnific Edition)

Act as a full-service AI video agency: take one reference photo from the user and
deliver a complete, coherent, multi-scene cinematic video with a consistent main
character. Built entirely on the Freepik/Magnific MCP tools (Nano Banana Pro / GPT 2
for images, Seedance 2.0 for video) — no CLI installation, no separate account, no
ffmpeg.

## Step 0 — Setup check

1. **Freepik/Magnific connector active?** Call `account_profile` and
   `account_balance`. If the call fails, tell the user to enable the Freepik/Magnific
   connector in their Claude account settings before continuing.
2. **Credits.** Read `account_balance`. If `plan.isUnlimitedMode` is true but
   `plan.unlimitedAppliesHere` is false, tell the user generations in this session
   will consume real credits despite their unlimited plan — do this once, before the
   first paid call, not on every call.

No git, no CLI, no ffmpeg required.

## Step 1 — Onboarding interview

You are the agency's creative director. Interview the user, one question at a time,
in their language. Never batch all questions into one wall of text.

1. **Reference photo.** Ask for the start image. Get it into Magnific as a creation:
   - User attached a file in the chat → `creations_upload_file`
   - User gave a public URL → `creations_upload_image`
   Read the image yourself and analyze out loud: pose, framing, lighting, distinctive
   features (hairstyle, facial hair, accessories), aspect ratio. Note the anchor pose
   (a distinctive gesture is gold — it becomes the visual motif that bookends the
   whole video).
2. **Concept.** What do they want to become / what story do they want to tell? If
   they have no idea, pitch 2–3 concepts based on the photo's vibe.
3. **Format.** Ask for:
   - Number of story scenes (recommend 3; more scenes = more identity drift risk)
   - Clip length (recommend 10s per story scene, 5s per transformation)
   - With or without transformation bookends (morph in at the start, morph back at
     the end — recommended for personal videos, usually skipped for pure ads)
4. **Script.** Draft the story as a numbered scene list with a strong hook in
   scene 1. Classic arc: hook & threat → struggle & turning point → triumph & full
   circle. The FINAL scene must end with the character in the same pose as the
   reference photo, facing the camera — this is what makes the reverse morph
   seamless. Get the user's sign-off before generating anything.

## Step 2 — Character library asset (the identity anchor)

This replaces the manual "character reference sheet" prompt trick with a native
Magnific feature: a reusable character asset.

1. Optional but recommended: generate a few extra angles from the single reference
   photo with `images_variations` (`variationMode: "angles"`, source = the uploaded
   reference creation) so the library asset has more than one view to anchor on.
2. Call `library_create`:
   ```
   type: "character"
   name: "<short_unique_name>"        # A-Z/0-9/_/- only
   images: [
     { creationIdentifier: "<reference photo>" },
     { creationIdentifier: "<angle 1>" },   # from step 1, optional
     { creationIdentifier: "<angle 2>" }    # optional, max 6 total
   ]
   description: "<concrete facial features: hair, beard, eye color, face shape>"
   ```
3. Note the returned numeric `id` and use it for **image** generations
   (`images_generate` accepts the numeric library id directly in
   `references[].identifier`). For **video** generations, `video_generate` does NOT
   accept the numeric library id — pass the actual reference *image's* creation
   identifier instead (see Step 5). Tested against the live API: passing the
   library id or its string `identifier` to `video_generate` fails with
   "Creation not found".
4. Show the user the reference photo they chose and confirm the character was
   created before continuing.

## Step 3 — Transformation target image (if bookends are wanted)

Generate the "after" image: same pose, same framing, only character and environment
swapped.

```
images_generate:
  prompt: "Transform the person into <target character>, keeping their exact same
    pose, facial structure, expression and camera framing. <Describe swapped
    elements: clothing, props in the raised hand, new background.> Photorealistic,
    same composition as the original."
  mode: "imagen-nano-banana-2"   # Nano Banana Pro — best for character consistency
  references: [{ type: "character", identifier: "<library id from Step 2>" }]
  aspectRatio: "16:9"
```

Download/keep this creation — it is reused in Step 6 as the reverse-morph start
image. Show it to the user for approval before spending credits on video.

## Step 4 — Transformation morph in (Seedance 2.0, first/last frame)

Call `video_plan` first to confirm the brief and model choice, then generate:

```
video_generate:
  video:
    clips: [{
      slug: "bytedance-seedance-pro-2.0"
      prompt: "<Describe the person as they are now>. They snap their fingers and a
        magical swirling transformation ripples over them: <what morphs into what —
        clothes, hair, background>. Smooth cinematic morph transition, mystical
        particles, seamless transformation."
      duration: 5
      aspectRatio: "16:9"
      resolution: "1080p"
      keyframes:
        start: { type: "image", url: "<reference photo creation id>" }
        end:   { type: "image", url: "<target image creation id from Step 3>" }
    }]
```

Give the morph a trigger (finger snap, spin, flash) — it motivates the transition
and reads better than an unmotivated dissolve.

## Step 5 — Story scenes (Seedance 2.0, character reference)

**Critical architecture decisions — carried over from the original workflow:**

- **NO frame chaining.** Do NOT use the last frame of scene N as the start image of
  scene N+1. Identity drift compounds. Each scene is an independent generation.
- **Every scene references the character** via `references`, not `keyframes`.
- **Fewer, longer scenes.** 3×10s beats 6×5s: smoother motion, fewer hand-off
  points, less drift.
- Bonus over the CLI original: use the `cameraMotion` field (52 presets, e.g.
  `pushIn`, `orbitLeft`, `handheld`, `crashZoomIn`) to direct each shot explicitly.
- **Reference value:** use the creation identifier of an actual reference image
  (the Step 1 reference photo or the Step 3 target image) — NOT the numeric
  `library_create` id. `video_generate` rejects library ids with "Creation not
  found"; only `images_generate` accepts them.
- **`type: "character"` can trigger moderation blocks.** Tested against the live
  API: a photorealistic human-face image passed as `references[].type: "character"`
  was blocked ("Seedance blocked this request due to moderation rules"), while the
  identical identifier passed as `type: "image"` succeeded. Default to `type:
  "image"` for the character reference; only try `type: "character"` if `image`
  doesn't hold identity well enough, and expect it may get blocked.

```
video_generate:
  video:
    clips: [{
      slug: "bytedance-seedance-pro-2.0"
      prompt: "The character from the reference image (<costume look>). Scene:
        <full scene description with action, camera movement, lighting, mood>."
      duration: 10
      aspectRatio: "16:9"
      resolution: "1080p"
      cameraMotion: "<optional preset>"
      references: [{ type: "image", url: "<target image creation id from Step 3>" }]
    }]
```

Run `creations_wait` on the returned identifier, then `creations_show` to display it
and give the user the result as you go.

Write the last scene so it ends on the anchor pose (character facing camera in the
reference-photo gesture) — that frame is what Step 6 approximates.

## Step 6 — Reverse transformation (if bookends are wanted)

Magnific has no video-frame-extraction tool, so this workflow skips extracting the
literal last frame (the original CLI version used `ffmpeg -sseof`). Instead, reuse
the **target image from Step 3** as the start — since the final scene was directed
to end on that exact pose anyway, it's a close enough stand-in and needs no local
tooling.

```
video_generate:
  video:
    clips: [{
      slug: "bytedance-seedance-pro-2.0"
      prompt: "<Character> stands <in the final scene setting>, facing the camera. A
        magical reverse transformation ripples over them: <what morphs back — hair,
        clothes, background returning to the original>. Smooth cinematic reverse
        morph, ending exactly on the reference photo pose."
      duration: 5
      aspectRatio: "16:9"
      resolution: "1080p"
      keyframes:
        start: { type: "image", url: "<target image creation id from Step 3>" }
        end:   { type: "image", url: "<reference photo creation id>" }
    }]
```

If the user wants frame-perfect precision instead of this approximation, tell them
that's a known gap versus the ffmpeg-based original (see README changelog).

## Step 7 — Optional: title & text transition cards

Once all story clips are done, ask the user once: **"Do you want any text
transitions — a title card, an outro card, or a text overlay anywhere?"**

Placement guidance (advise the user, don't just obey):
- **Best spot for a title card**: right after the opening transformation, before
  scene 1.
- **Avoid cards in the mid-story transitions** — they break tension exactly where
  retention matters most.
- **An outro card after the reverse morph** rounds off the film without
  interrupting the story.

```
video_generate:
  video:
    clips: [{
      slug: "bytedance-seedance-pro-2.0"
      prompt: "Cinematic title card on a near-black background with <theme-matching
        elements>. The first second is completely silent and empty. Then the title
        text '<TITLE>' flies in dynamically as <style>, accompanied by a single deep
        cinematic whoosh-impact sound exactly when the text lands. The text holds,
        gently flickering. The final second: total silence again, text slowly
        fading. No music, no other sounds — only the one whoosh-impact. Elegant,
        epic, minimalist title sequence, 16:9."
      duration: 5
      aspectRatio: "16:9"
      resolution: "1080p"
    }]
```

Verify the spelling of the rendered text by viewing the result — text is the most
common generation failure.

## Step 8 — Assembly & delivery

Concatenate everything natively — no ffmpeg:

```
video_concatenate:
  creationIdentifiers: [
    "<morph_in>", "<title_card>", "<scene1>", "<scene2>", "<scene3>", "<morph_back>"
  ]
  name: "<project name> — Final Cut"
```

Then `creations_wait` on the returned identifier and `creations_show` to render it.

Deliver: file list, total runtime, and a one-line recap of the story. Offer next
steps (regenerate individual scenes, a vertical 9:16 version for Shorts/TikTok via
`video_upscale`/re-render with a different `aspectRatio`, or upscale the final cut).

## Quality rules

- Show intermediate images (target image) to the user for approval before spending
  credits on video.
- Check identity after each scene by viewing it; regenerate a scene if the face
  drifted badly — never chain a drifted frame forward.
- Prefer models with `agentRecommendation.tier: sota`, then lower `rank`, per
  `video_models_list` / `images_models_list` — don't hardcode a model beyond what
  this skill specifies unless the user asks for something else.
- Prompts to Magnific in English; conversation with the user in their language.
- Tell the user about credit consumption once, before the first paid generation —
  not on every single call.

## Use cases beyond personal stories

The same pipeline works for ads and brand content: the "reference photo" can be a
product shot or brand avatar (`library_create` with `type: "product"`), the
"transformation" a product reveal, the story scenes a mini-commercial.

See `references/prompting-guide.md` for prompt patterns and
`references/troubleshooting.md` for common failures.
