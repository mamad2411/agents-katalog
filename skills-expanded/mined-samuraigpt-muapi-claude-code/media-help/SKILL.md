---
name: media-help
description: Helps users explore and choose the best MuAPI models for their media generation needs. Use when the user asks what models are available, wants recommendations, or needs help deciding between image and video generation options.
---

# Media Help

Use the MuAPI model discovery tools to help users understand and choose the right model.

## Instructions

1. Call the `list_models` tool to get the available model categories
2. If the user asks about a specific category, call `model_details` with a specific model name (e.g., `flux-dev`, `kling-master`, `flux-kontext-dev`)
3. Explain the available options clearly, including what each model is best for
4. Recommend the most appropriate model based on the user's needs

## Request

$ARGUMENTS

## Available Models

### Image Generation
- **flux-dev** — Fast, high-quality text-to-image generation (default for `generate_image`)
- **flux-kontext-dev** — Specialized for image editing tasks (used by `edit_image`)

### Video Generation
- **kling-master** — High-quality text-to-video and image-to-video generation (default for `generate_video` and `image_to_video`)

## Other Useful Tools

- `account_balance` — Check the user's current MuAPI balance and account info
- `upload_file` — Upload a local file to MuAPI for use with image editing or image-to-video
- `get_prediction` — Check the status of a previously submitted generation request