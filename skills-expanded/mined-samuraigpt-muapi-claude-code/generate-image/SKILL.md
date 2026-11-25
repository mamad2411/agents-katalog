---
name: generate-image
description: Generates images from text prompts using MuAPI. Use when the user asks to create, generate, or make an image, picture, illustration, or artwork from a text description.
---

# Generate Image

Use the MuAPI image generation tools to create images from text prompts.

## Instructions

1. Take the user's request and craft an effective image generation prompt
2. Call the `generate_image` tool with the prompt
3. The tool uses the `flux-dev` model by default and waits for completion
4. Display the resulting image URL to the user
5. Report the generation cost from the response if available

## Request

$ARGUMENTS

## Notes

- Generation is synchronous — the tool submits the request and polls until complete
- The response includes an `images` array with the output URLs
- Cost information is included in `result.cost.amount_usd`
- If the user wants to edit an existing image instead, use the `edit_image` tool with the `flux-kontext-dev` model