---
name: image2
description: Generate and edit images through the local Image2 service with the active user-configured image provider. Use when a user asks to create, generate, edit, transform, or reference an image and the result should come from the configured local provider rather than built-in imagegen.
---

# Local Image2

Use the local Image2 service as the primary image-generation path. Do not use the built-in `imagegen` tool.

## Workflow

1. Optimize the user's prompt while preserving intent. Make subject, action, composition, viewpoint, style/material, lighting, palette, aspect ratio, and constraints explicit. Do not invent text, logos, people, or objects. For edits, state what must be preserved and what must change.
2. Prefer the installed global CLI when available: `%CODEX_HOME%\skills\image2\Image2CLI.exe --prompt "..."`. The installer places a non-secret `image2-client.json` beside it so the CLI knows the service, token, output directory, and launcher. If the packaged CLI is unavailable, use the project `image2_cli.py` with its absolute path.
3. The local backend uses the active provider selected in the HTML console. There is no default provider; if setup is incomplete, direct the user to the local API settings instead of attempting a real request.
4. If the local service is unavailable, let the configured CLI launcher start it and retry once. For a restricted Codex sandbox, request one host-approved network-enabled execution for the service process before a real provider request. Keep the service on `127.0.0.1`.
5. For a public reference image URL, add `--image-url "https://..."`. For a local attachment, add `--image-path "C:\path\to\image.png"`, repeating it for multiple images up to eight.
6. Inspect the CLI JSON response, read the returned local output path, and include the generated image in the conversation. Briefly report the optimized prompt and active provider.

## Simulation

For a requested safety check or dry run, use `--dry-run`. Confirm the active provider model, route, request body mode, size, and quality, then stop before the final provider request. A dry run must not call an external provider or consume image quota.

## Security

- Never print, copy, or place an API key in HTML, JavaScript, prompts, shell arguments, logs, or conversation output.
- Provider keys are entered through the local console and stored by the backend in the operating-system credential store. The frontend only receives a configured/not-configured flag.
- Keep the service bound to `127.0.0.1`; never expose it on `0.0.0.0`.
- Treat custom provider URLs and reference image URLs as untrusted input. Use the backend validation and do not bypass its limits.
- If a provider reports an outbound-network failure, stop retrying in the restricted sandbox, request one approved network-enabled service execution, and retry only once after approval.
