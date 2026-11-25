---
name: generate-video
description: Generates videos from text prompts using MuAPI. Use when the user asks to create, generate, or make a video, animation, or motion clip from a text description.
---

# Generate Video

Use the MuAPI video generation tools to create videos from text prompts.

## Instructions

1. Take the user's request and craft an effective video generation prompt
2. Call the `generate_video` tool with the prompt
3. The tool uses the `kling-master` model by default and waits for completion
4. Display the resulting video URL to the user
5. Report the generation cost from the response if available

## Request

$ARGUMENTS

## Notes

- Generation is synchronous — the tool submits the request and polls until complete
- The response includes an `outputs` array with the video URLs
- Cost information is included in `result.cost.amount_usd`
- If the user wants to convert an existing image into a video, use the `image_to_video` tool instead
- Video generation typically takes longer than image generation