---
name: image-to-video
description: Converts a still image into a video using MuAPI. Use when the user wants to animate an image, bring a photo to life, or turn a picture into a video clip.
---

# Image to Video

Use the MuAPI image-to-video tool to animate a still image into a video clip.

## Instructions

1. Ask the user for the image URL or file path if not already provided
2. If the user provides a local file, call `upload_file` first to get a hosted URL
3. Ask the user for any motion guidance (optional) — e.g. "slow zoom in", "camera pan left", "gentle waves"
4. Call the `image_to_video` tool with the image URL and optional prompt
5. The tool uses the `kling-master` model by default
6. Display the resulting video URL to the user
7. Report the generation cost from the response if available

## Request

$ARGUMENTS

## Notes

- `image_to_video` requires an existing image URL — upload local files with `upload_file` first
- Generation is synchronous — the tool polls until complete and typically takes longer than image generation
- The response includes an `outputs` array with the video URLs
- Cost information is included in `result.cost.amount_usd`
- For generating a video from a text description only (no source image), use `generate_video` instead
