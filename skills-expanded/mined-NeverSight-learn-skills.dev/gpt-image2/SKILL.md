---
name: gpt-image2
description: Lightweight GPT Image 2 image generation and editing workflow. Use when Codex needs to configure OpenAI-compatible image API channels, generate or edit images from the command line without Python, print equivalent curl calls, or help users quickly try curated GPT-Image-2 prompt templates.
---

# GPT Image 2

Use the bundled Node.js CLI for lightweight image generation and editing. It has no npm dependencies and supports OpenAI-compatible image endpoints.

## Quick Start

Run commands from this skill folder:

```bash
node scripts/gpt-image2.mjs --help
node scripts/imgbb-upload.mjs --help
```

Configure an API channel:

```bash
node scripts/gpt-image2.mjs config set openai --api-key "$OPENAI_API_KEY" --base-url "https://ai-api.qzsyzn.com/v1" --model "gpt-image-2" --edit-transport generations
node scripts/gpt-image2.mjs config use openai
```

Use `--edit-transport multipart` for the official OpenAI-style `POST /images/edits` multipart flow (default when omitted).

For **unified JSON edit** (`generations`), **do not rely on huge base64 payloads**. Prefer HTTPS URLs:

1. **Default:** local reference files are **uploaded to ImgBB automatically** (built-in API key, stored encrypted in `scripts/imgbb-upload.mjs`). No need to set **`IMGBB_API_KEY`** unless you want your own key—then use **`IMGBB_API_KEY`** or **`--imgbb-key`** (see [ImgBB API](https://api.imgbb.com/)).
2. Or upload first, then edit with URLs only:

```bash
node scripts/imgbb-upload.mjs ./test/image.png
node scripts/gpt-image2.mjs edit --edit-transport generations --image "https://i.ibb.co/..." --prompt "Your edit instruction" --output outputs/edited.png
```

Global install after `npm link`: `imgbb-upload ./photo.png` prints one URL per line.

Use **`--embed-local-base64`** only when you intentionally want data URLs (e.g. offline debugging).

Try a prompt template:

```bash
node scripts/gpt-image2.mjs templates list
node scripts/gpt-image2.mjs try encyclopedia-card --var topic="coffee brewing" --output outputs/coffee.png
```

Query supported resolutions:

```bash
node scripts/gpt-image2.mjs sizes list
node scripts/gpt-image2.mjs sizes list --orientation portrait
```

Generate with a direct prompt:

```bash
node scripts/gpt-image2.mjs generate --prompt "A clean product hero image of a ceramic desk lamp" --size 1024x1024 --output outputs/lamp.png
```

Edit an existing image (`generations` transport uploads local files via ImgBB by default):

```bash
node scripts/gpt-image2.mjs edit --image input.png --prompt "Keep the object unchanged, replace the background with a warm studio setup" --output outputs/edited.png --edit-transport generations
```

Optional: `export IMGBB_API_KEY="..."` or `--imgbb-key ...` to use your own ImgBB key instead of the built-in default.

Print a curl command instead of calling the API:

```bash
node scripts/gpt-image2.mjs generate --template city-poster --var city="Chengdu" --curl
```

## Workflow

1. Use `templates list`, `templates search <query>`, and `templates show <id>` before drafting prompts from scratch.
2. Prefer `try <template-id> --var key=value` for quick experimentation.
3. Use `config set <channel>` for provider-specific API keys, base URLs, and model names. The active channel is used by default.
4. Keep OpenAI-compatible API keys in config or environment variables, not in checked-in files. ImgBB uses a **built-in default** unless you override with `IMGBB_API_KEY` or `--imgbb-key`.
5. Run `sizes list` before choosing `--size`, especially when switching between square, portrait, and landscape output.
6. Use `--dry-run` to inspect the final payload and `--curl` when the user wants shell-native invocation (with ImgBB enabled, dry-run still contacts ImgBB so URLs in the JSON match a live run).
7. If an API call fails once, report the HTTP status and response body. Do not blindly retry without changing prompt, size, channel, or timeout.

## Configuration

Credential precedence:

1. CLI flags: `--api-key`, `--base-url`, `--model`, `--edit-transport`, `--imgbb-key`
2. Active channel in the config file
3. Environment variables: `GPT_IMAGE_API_KEY`, `OPENAI_API_KEY`, `API_KEY`; `GPT_IMAGE_BASE_URL`, `OPENAI_BASE_URL`, `BASE_URL`; `GPT_IMAGE2_EDIT_TRANSPORT` (`multipart` or `generations`); **`IMGBB_API_KEY`** (optional; overrides the built-in ImgBB key when uploading locals for `generations` edit)

The config file defaults to `~/.gpt-image2/config.json`. Override it with `GPT_IMAGE2_CONFIG`.

Useful commands:

```bash
node scripts/gpt-image2.mjs config list
node scripts/gpt-image2.mjs config show
node scripts/gpt-image2.mjs config use <channel>
node scripts/gpt-image2.mjs config set <channel> --api-key "..." --base-url "..." --model "..." [--edit-transport multipart|generations]
```

## Prompt Templates

Templates live in `references/prompts.json`. Keep templates reusable:

- Use `{{variable}}` placeholders for user-specific details.
- Avoid names or likenesses of real private people unless the user explicitly provides appropriate rights and context.
- Prefer complete visual specifications: subject, scene, composition, lighting, style, details, output use.
- Keep new templates as compact patterns rather than copying long community prompts verbatim.

## API Notes

The CLI calls:

- `POST /images/generations` for text-to-image (JSON).
- **Edit mode (default):** `POST /images/edits` with multipart form data (`--edit-transport multipart`).
- **Unified gateways:** same JSON `POST /images/generations` with an `image` array of strings. **Prefer HTTPS URLs:** by default, local files are uploaded via ImgBB (built-in key); only URLs are sent in JSON. Use **`--embed-local-base64`** to force data URLs instead. Optional **`IMGBB_API_KEY`** / **`--imgbb-key`** overrides the default ImgBB key. Use `scripts/imgbb-upload.mjs` for a standalone upload step. Up to 5 reference images; `--mask` is not supported in this mode.

It saves `b64_json` image data when present and can also download a returned `url` for OpenAI-compatible gateways that use URLs.
