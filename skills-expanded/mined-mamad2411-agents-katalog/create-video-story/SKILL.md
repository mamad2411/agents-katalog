---
name: create-video-story
description: Build a video from a story outline — scenes, images, voice, and subtitles end to end
argument-hint: "[topic]"
related:
  - gen-media
  - gen-voice
  - gen-subtitle-video
  - follow-lib-remotion
  - enhance-prompt
  - report

---

## Goal

Create a short video from a story outline, covering story structure, scene details, images, video, voice, and subtitles

## Scope

- For short story outlines such as social media videos, story reels, promotional clips
- Ask the user about style, orientation, and length
- Build the story structure, character personalities, and hooks
- Detail each scene: sound, gestures, background, facial expression, mood, and more
- Generate an image per scene, calling `/gen-media-image-character` for character consistency
- Generate video from images/prompts and create subtitles

## Execute

### 1. Interview

> Goal: Collect the video requirements

1. Take `topic` from the user
2. Ask for `style`, e.g. `anime`, `realistic`, `cinematic`, `motion-graphics`
3. Ask for `orientation`, e.g. `portrait (9:16)`, `landscape (16:9)`, `square (1:1)`
4. Ask for `duration` or the number of scenes (default 5 scenes)
5. Ask for `tone`, e.g. `funny`, `dramatic`, `educational`, `emotional`
6. Ask for the target audience if needed

### 2. Build Story

> Goal: Create the story outline and characters

1. Write a short hook that grabs attention in the first 3 seconds
2. Define the protagonist and supporting characters
3. Define each character's personality, visual traits, and color palette
4. Build the story beats: setup, conflict, climax, resolution
5. Fit the outline to the number of scenes

### 3. Design Scenes

> Goal: Plan the details of each scene

1. For each scene specify:
   - scene number and duration
   - location/background
   - camera angle and camera movement
   - character gestures and pose
   - facial expression
   - mood/atmosphere
   - sound effects or voiceover
   - subtitle text
   - transition to the next scene
2. Keep the scene brief as a list/table
3. Use `/report` to present it

### 4. Generate Characters

> Goal: Create reference images of the main characters

1. For each main character call `/gen-media-image-character`
2. Pass the character brief, style, aspect-ratio, output path
3. Keep the character anchor image and prompt anchor
4. Verify the character images stay consistent with each other

### 5. Generate Scene Images

> Goal: Create an image for each scene

1. For each scene compose the prompt from:
   - the character anchor and reference image
   - scene setting, pose, expression, camera angle
   - lighting, mood, style
2. Call `/gen-media-ai-images` or `/gen-media-image-character` depending on the scene
3. Save each scene image with a sequential name, e.g. `scene-01.png`
4. Verify each file is larger than 0 bytes

### 6. Generate Voice

> Goal: Create the speech/narration audio

1. Collect the script or narration from each scene
2. Ask the user for language/voice; auto-detect if unspecified
3. Call `/gen-voice` with text, voice, output path
4. Keep per-scene audio or merge into one file with `ffmpeg`

### 7. Generate Video

> Goal: Produce the video from images and audio

1. Choose the video method:
   - call `/gen-media-ai-videos` from a prompt or image sequence
   - use `/follow-lib-remotion` for programmatic rendering
2. Specify duration, aspect-ratio, and fps
3. Verify the video file is larger than 0 bytes
4. If a paid provider is used, tell the user first

### 8. Generate Subtitle

> Goal: Create subtitles for the video

1. If the video exists, call `/gen-subtitle-video` to transcribe
2. If a script comes first, build a `.srt` with timestamps from scene durations
3. Check the cue count and syntax
4. Save the `<video>.srt` file

### 9. Validate

> Goal: Check the video is complete

1. Verify the video duration matches the plan
2. Verify the scene image count matches the scene list
3. Verify subtitle cues match the audio
4. Report outputs, scene summary, tools used

### 10. Report

> Goal: Summarize the results

1. Use `/report` to show scenes, durations, output paths
2. State the video path, subtitle path, voice path
3. State the provider/model used
4. On failure, show the error and suggest a fallback

## Rules

### 1. Ask Before Paid Generation

- If a paid provider is needed, ask the user first
- Never hardcode API keys
- Use environment variables or ask the user

### 2. Consistency

- Use `/gen-media-image-character` to create character references first
- Keep the prompt anchors and seeds of characters in context
- Change only pose/expression/background between scenes

### 3. No Overwrite

- Never overwrite existing files without asking
- Use indexed file names such as `scene-01.png`, `scene-02.png`
- Create the output directory if needed

### 4. Reasonable Defaults

- default duration = 5 scenes
- default orientation = `portrait (9:16)`
- default style = `realistic` or `anime` depending on the target platform
- default output format = `.mp4`

- Use /enhance-prompt if needed

## Expected Outcome

- A complete short video with images, audio, and subtitles
- A summary table of all scenes
- A report of output paths, provider, model, duration
- On failure, a fallback plan
