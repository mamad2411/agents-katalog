---
name: edit-image
description: Edits an existing image using natural language instructions via MuAPI. Use when the user wants to modify, change, transform, or retouch an existing image.
---

# Edit Image

Use the MuAPI image editing tools to modify an existing image based on instructions.

## Instructions

1. Ask the user for the image URL or file path if not already provided
2. If the user provides a local file, call `upload_file` first to get a hosted URL
3. Craft a clear editing instruction from the user's request
4. Call the `edit_image` tool with the image URL and editing prompt
5. The tool uses the `flux-kontext-dev` model by default
6. Display the resulting image URL to the user
7. Report the generation cost from the response if available

## Request

$ARGUMENTS

## Notes

- `edit_image` requires an existing image URL — upload local files with `upload_file` first
- Generation is synchronous — the tool polls until complete
- The response includes an `images` array with the edited image URLs
- Cost information is included in `result.cost.amount_usd`
- For generating a brand new image from scratch, use the `generate_image` tool instead
