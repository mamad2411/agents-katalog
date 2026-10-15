---
name: azure-openai-image-gen-skill
description: Generate, edit, or troubleshoot image generation through Azure OpenAI / Microsoft Foundry image model deployments. Use when the user asks for GPT Image, gpt-image-2, gpt-image-1.5, gpt-image-1, Azure OpenAI image generation, deployment-based image APIs, Azure Foundry image model prompts, base64 image outputs, or an Azure-backed alternative to the built-in image_gen tool.
---

# Azure OpenAI Image Generation

Use this skill when the user wants image generation through an Azure OpenAI deployment instead of the built-in `image_gen` tool.

## Workflow

1. Confirm the execution target.
   - For this chat's built-in image tool, use `image_gen`; it may not expose a model/deployment selector.
   - For Azure OpenAI, call the user's deployed image model by deployment name. Do not assume the model name and deployment name are identical.
2. Verify current Azure support before making model-specific claims. Read `references/azure-openai-image-api.md` when the task depends on model availability, parameters, or endpoint shape.
3. Ask for or discover required Azure configuration only when needed:
   - `AZURE_OPENAI_ENDPOINT`, for example `https://my-resource.openai.azure.com`
   - `AZURE_OPENAI_API_KEY` or an Entra ID bearer token
   - `AZURE_OPENAI_DEPLOYMENT`, the deployment name for the image model
   - `AZURE_OPENAI_API_VERSION` for legacy dated APIs, or `v1` endpoint support when available
   - Prefer `~/.config/env/azure-image-gen.env` for local machine credentials; the helper auto-loads it unless `--config-env-file` is provided.
4. Refine the user's image request into a production prompt using `assets/prompt-template.md`.
5. Generate or edit the image with `scripts/generate-image.mjs` when a direct Azure API call is appropriate, or write API code for the user's repo using the same request shape.
6. Save output images as files and report the absolute file paths. Mention parameter or deployment limitations when Azure rejects an option.

## Prompt Rules

Keep model routing outside the prompt when using the API. Set the Azure deployment/API route in code and make the prompt purely about the desired visual result.

Good prompt structure:

```text
Subject: ...
Purpose: ...
Composition: ...
Style: ...
Lighting and color: ...
Text in image: ...
Aspect ratio / dimensions: ...
Quality target: ...
Avoid: ...
```

For GPT Image 2, prefer concrete dimensions that match Azure's current constraints instead of only saying "wide", "square", or "4K".

## Azure Helper

Use the bundled helper for direct generation:

```bash
node scripts/generate-image.mjs \
  --prompt-file prompt.txt \
  --size 1536x1024 \
  --quality high \
  --out ./out
```

Default local env file:

```bash
# ~/.config/env/azure-image-gen.env
AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com"
AZURE_OPENAI_API_KEY="<key>"
AZURE_OPENAI_DEPLOYMENT="<deployment-name>"
AZURE_OPENAI_API_VERSION="2025-04-01-preview"
```

Use `AZURE_OPENAI_BEARER_TOKEN` instead of `AZURE_OPENAI_API_KEY` when testing Entra ID auth. Existing shell environment variables override values loaded from the env file.

The helper writes one `.png` per returned image. If Azure returns a schema or option error, reduce optional fields first; Azure deployments can lag public OpenAI feature flags.

## Reference Images

Use `--image` for reference-image or edit inputs. Repeat it for multiple references:

```bash
node scripts/generate-image.mjs \
  --prompt "Turn these references into a premium toy airplane product render with no text." \
  --image ./reference-plane.png \
  --image ./material-reference.jpg \
  --size 1536x1024 \
  --quality high \
  --out ./out
```

The helper switches from `/images/generations` to `/images/edits` when one or more `--image` flags are provided. GPT image edit inputs can support up to 16 images, but Azure deployment support can vary by model version, region, and API version.

Optional edit flags:

```bash
--mask ./mask.png
--input-fidelity high
--image-field image
```

Use `--image-field image` by default. If a specific Azure preview API rejects multipart image fields, verify the current Microsoft Learn examples before changing the field name.

## Implementation Guidance

- Use deployment names in Azure URLs, not public model IDs, unless the v1 OpenAI-compatible client for that resource explicitly maps `model` to the Azure deployment.
- Prefer API key auth for quick local tasks; use Entra ID for production apps that already have Azure identity plumbing.
- Treat returned images as base64-first. Do not expect URL output for GPT Image series deployments.
- For edits/reference images, use `/images/edits` and multipart form data; verify whether the deployed model and chosen API path support image inputs before writing production code.
- Do not claim `gpt-image-2` is available in every Azure region or subscription. Azure availability depends on access, region, and deployment state.
