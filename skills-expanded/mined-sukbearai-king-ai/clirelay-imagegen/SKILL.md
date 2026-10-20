---
name: clirelay-imagegen
description: "Generate and save raster images through the configured CliRelay OpenAI-compatible image endpoint using CLIRELAY_API_KEY and gpt-image-2. Use when the user explicitly asks to use CliRelay, gpt-image-2, or this custom image service. Prefer the system image-generation skill for ordinary image requests that do not require CliRelay."
---

# CliRelay ImageGen

Generate one local image through:

```text
POST http://154.23.172.163:8317/v1/images/generations
Authorization: Bearer $CLIRELAY_API_KEY
```

The endpoint is plain HTTP. The prompt and bearer token are not protected by TLS while in transit. Do not call it unless the user has explicitly chosen this CliRelay service and accepts that transport risk. Never print, persist, or place `CLIRELAY_API_KEY` in command arguments, prompt files, logs, source files, or generated metadata.

## Generate

1. Resolve an exact output path. Do not overwrite an existing file.
2. Put only the image prompt in a private temporary UTF-8 file. Do not put credentials in it.
3. Optionally run `--dry-run`; it validates inputs and prints only prompt length and SHA-256, without reading the API key or making a network request.
4. A direct user request to generate an image through this skill authorizes one API generation. Retries, variations, or additional images require a new request or confirmation because they may consume more quota.
5. Run the generator with the explicit insecure-transport acknowledgement:

```bash
node <skill-dir>/scripts/generate.mjs \
  --allow-insecure-http \
  --prompt-file <private-prompt-file> \
  --output <absolute-output.png>
```

Optional request controls:

```bash
--model gpt-image-2 --size 1024x1024 --quality high
```

Keep `n=1`; run separate explicitly authorized requests for additional images. The script reads `CLIRELAY_API_KEY` from its environment. If the variable is missing, ask the user to start a fresh shell/session that inherits it; never inspect or echo the value.

The script accepts either `data[0].b64_json` or `data[0].url`, saves the image atomically with mode `0600`, and prints JSON containing only the output path, byte count, model, size, quality, and response source.

## Verify and Deliver

- Confirm the output is a non-empty regular file.
- Use the available local image-viewing tool to inspect the generated image when visual verification is useful.
- Return the local image artifact to the user and state the exact model/size/quality actually requested.
- Delete the temporary prompt file after the request.
- On an API failure, report the redacted HTTP error once. Do not automatically retry or fall back to another paid image provider.
