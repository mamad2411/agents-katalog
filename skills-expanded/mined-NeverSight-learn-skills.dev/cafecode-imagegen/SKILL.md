---
name: cafecode-imagegen
description: Generate or reference-edit raster images through OpenAI-compatible CafeCode endpoints, decode b64_json or image URLs, and save verified image files. Use when Codex needs CafeCode image generation, image-grounded edits, exact prompt/request reuse, sprite references, animation source strips, or repeated image generation without exposing API keys.
---

# CafeCode Imagegen

Use the bundled `scripts/generate_image.py` script for image generation through the Neko-compatible endpoint. The script keeps the prompt unchanged, supports either a prompt file or a complete request JSON, writes images atomically, and never prints authentication headers.

## Configuration

- Default endpoint: `https://neko.cafecode.work/v1/images/generations`
- Reference-image endpoint: `https://neko.cafecode.work/v1/images/edits`, selected automatically when `--reference` is present.
- Authentication: add the top-level field `cafecode-imagegen-key` to `~/.codex/config.toml`; the script sends it as `Authorization: Bearer ...`. `CAFECODE_IMAGE_API_KEY` remains an environment fallback. Do not use `OPENAI_API_KEY` implicitly because this endpoint is third-party.
- Output directory: optionally set the top-level field `cafecode-imagegen-output-dir` in `~/.codex/config.toml`. Use an absolute path, a `~` path, or a path relative to the current working directory.
- The endpoint may be overridden with `--endpoint`.
- HTTPS is required by default. Use `--allow-http` only for a deliberately local test server.

## Quick Start

Generate from a prompt file:

```powershell
$PYTHON = "C:\\path\\to\\python.exe"
& $PYTHON "$env:CODEX_HOME\\skills\\cafecode-imagegen\\scripts\\generate_image.py" `
  --prompt-file .\\prompt.txt `
  --out .\\image-output\\image.png `
  --size 1024x1024 `
  --output-format png
```

Submit an existing request unchanged except for explicit CLI overrides:

```powershell
& $PYTHON "$env:CODEX_HOME\\skills\\cafecode-imagegen\\scripts\\generate_image.py" `
  --request-file .\\request.json `
  --out .\\image-output\\image.png
```

Use `--dry-run` to inspect the final request without making a network call. Use `--all` when the response contains multiple images; otherwise the first item is saved to the requested output path.

Ground generation with one or more images:

```powershell
& $PYTHON "$env:CODEX_HOME\\skills\\cafecode-imagegen\\scripts\\generate_image.py" `
  --prompt-file .\\row-prompt.txt `
  --reference .\\canonical-base.png `
  --reference .\\previous-row.png `
  --out .\\image-output\\row.png
```

Each reference is sent as `images[].image_url` using a local data URL. Dry-run output redacts the base64 bytes.

Output precedence is `--out`, then `--output-dir`, then `cafecode-imagegen-output-dir`, then the built-in `image-output` directory. If `--out` is omitted, use the file name `image.<format>`; with `--all`, additional images use names such as `image-1.png`.

## Workflow

1. Put the authoritative prompt in a UTF-8 text file when it is long or must be reused. Do not ask the script to rewrite or summarize it.
2. Prefer `--request-file` when the caller already has a complete JSON body. Prefer `--prompt-file` when model, size, and output options should be controlled by the command. Add repeated `--reference` arguments when visual identity or continuity must be grounded.
3. Read the key from the top-level `cafecode-imagegen-key` field in `~/.codex/config.toml`. Use `CAFECODE_IMAGE_API_KEY` only as a temporary or CI fallback. Never put credentials in prompts, request JSON, scripts, or skill files.
4. Run `--dry-run` first for a new request. Confirm the endpoint, model, size, and output format before paying for generation.
5. After generation, inspect the saved image. For chroma-key sprite work, keep the generated source intact and perform background removal in the consuming workflow.
6. For repeated jobs, invoke one process per image or from a parent script; keep prompts and output paths explicit so generated assets can be traced to their source request.

Expected configuration:

```toml
cafecode-imagegen-key = "your-key"
cafecode-imagegen-output-dir = "~/Pictures/CafeCode"
```

Use `--config-file` to read another TOML file, `--config-key` to select another API-key field, or `--output-dir-config-key` to select another output-directory field. The script never prints the key.

## Request Behavior

With `--prompt` or `--prompt-file`, the script creates a body containing `model`, `prompt`, `size`, `output_format`, optional `quality`/`moderation`, and `images` when references are provided. With `--request-file`, it loads a JSON object and applies only explicit overrides/references. The response parser accepts:

- `data[*].b64_json` containing base64-encoded image bytes;
- `data[*].url` containing an image URL to download;
- a top-level `b64_json` or `url` for simple compatible servers.

For URL responses, the script downloads the image with a browser-compatible `User-Agent` and image `Accept` header. CafeCode currently serves generated image URLs through a Cloudflare-protected CDN that rejects Python urllib's default user agent. Do not remove the browser headers, and do not forward the CafeCode API key to the returned third-party image host.

The script retries timeouts, HTTP 408/425/429, and HTTP 5xx responses with bounded exponential backoff. It fails fast on other status codes, malformed JSON, missing image data, invalid base64, or unsupported URL schemes.

## Sprite Generation Notes

When used with `$hatch-pet`, generate the base reference and each animation strip as separate requests. Keep the exact pet identity prompt and attach any grounding image paths in the calling workflow. Do not ask the endpoint for a complete atlas when the consuming skill requires deterministic atlas assembly. Preserve original PNG outputs for QA before any chroma-key cleanup.
