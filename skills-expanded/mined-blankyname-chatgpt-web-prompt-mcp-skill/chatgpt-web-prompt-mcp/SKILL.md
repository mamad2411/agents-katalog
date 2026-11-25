---
name: chatgpt-web-prompt-mcp
description: "Use the local ChatGPT Web prompt-forwarding MCP bridge: submit prompts and reference images to an already-open real Chrome ChatGPT tab via CDP."
version: 1.0.0
author: Hermes Agent + user workflow
license: MIT
metadata:
  created_by: agent
  tags: [mcp, chatgpt, image-generation, telegram, claude-code, browser-automation]
---

# ChatGPT Web Prompt MCP Bridge

Use this when the user wants to send image-generation prompts (optionally with local reference images) into ChatGPT Web through a real Chrome window, without downloading generated images.

## Current install

Primary ChatGPT Web prompt-forwarding MCP server path:

```bash
~/.hermes/chatgpt-web-prompt-mcp/server.mjs
```

Legacy Claude MCP bridge path, now updated as a compatibility wrapper:

```bash
~/.hermes/scripts/hermes_image_mcp.py
```

The legacy `hermes-image` bridge now exposes both the original Hermes `generate_image` flow and ChatGPT Web tools:

```text
generate_image
image_backend_status
submit_image_prompt
get_latest_generated_images
download_latest_generated_images
```

Hermes MCP server config name:

```text
chatgpt_web_prompt
```

Hermes tool name after restart/discovery:

```text
mcp_chatgpt_web_prompt_submit_image_prompt
```

Claude Code server command:

```bash
node ~/.hermes/chatgpt-web-prompt-mcp/server.mjs
```

## Required runtime state

A real Google Chrome window must be open with CDP enabled and logged into ChatGPT:

```bash
npm run login
```

This starts Chrome with:

```text
CDP endpoint: http://127.0.0.1:9222
profile dir: ~/chrome-chatgpt-debug
```

Keep that Chrome window open while using the tool.

## Hermes gateway / Telegram usage

The MCP server is configured in `~/.hermes/config.yaml` as `mcp_servers.chatgpt_web_prompt`. MCP tools are discovered at process startup, so if Telegram gateway or a Hermes session cannot see the tool, restart the gateway / start a new session.

Expected tool name in Hermes:

```text
mcp_chatgpt_web_prompt_submit_image_prompt
```

Natural-language trigger examples for Telegram:

- "Через chatgpt web prompt mcp отправь промпт: ... preset poster"
- "Используй mcp_chatgpt_web_prompt_submit_image_prompt с reference_image_paths [...]"

## Claude Code integration

Preferred MCP server name for Claude Code:

```text
chatgpt-web-prompt
```

Tool names inside Claude for the preferred server:

```text
submit_image_prompt
get_latest_generated_images
download_latest_generated_images
```

The older configured Claude MCP server is:

```text
hermes-image
```

It has been updated as a compatibility bridge and now exposes:

```text
generate_image
image_backend_status
submit_image_prompt
get_latest_generated_images
download_latest_generated_images
```

So Claude can use either `chatgpt-web-prompt.submit_image_prompt` or `hermes-image.submit_image_prompt` depending on which MCP server is visible in that session.

Configure Claude Code with:

```bash
claude mcp add chatgpt-web-prompt \
  -- node ~/.hermes/chatgpt-web-prompt-mcp/server.mjs
```

Or JSON config:

```json
{
  "mcpServers": {
    "chatgpt-web-prompt": {
      "command": "node",
      "args": ["~/.hermes/chatgpt-web-prompt-mcp/server.mjs"],
      "env": {
        "CHATGPT_WEB_CDP_ENDPOINT": "http://127.0.0.1:9222"
      }
    }
  }
}
```

In Claude Code, reference images must be local files. If the user provides/creates an image, Claude should save or locate it on disk first, then call `submit_image_prompt` with `reference_image_paths` containing absolute paths. Preferred paths are under `~/...` because Chrome runs as macOS user `the Chrome user`.

Claude Code tools exposed by this server:

```text
submit_image_prompt
get_latest_generated_images
download_latest_generated_images
```

### Send prompt + reference images

```text
Use the chatgpt-web-prompt MCP tool `submit_image_prompt`.
Prompt: "Create a sticker character in this brand style."
Preset: square
Reference images: /absolute/path/to/reference.png
```

Tool call shape Claude should produce:

```json
{
  "prompt": "Create a sticker character in this brand style.",
  "preset": "square",
  "reference_image_paths": [
    "/absolute/path/to/reference.png"
  ],
  "submit": true
}
```

If Claude only has an image attachment but no path, instruct it to first write/copy the image into a local file such as:

```text
~/Desktop/<project>/references/<name>.png
```

then pass that path in `reference_image_paths`.

### Let Claude see generated images

After ChatGPT Web generates images, Claude can call:

```json
{
  "max_images": 4,
  "include_image_content": true,
  "save": true,
  "save_dir": "~/Downloads/chatgpt-images"
}
```

using tool:

```text
get_latest_generated_images
```

This returns:

- a JSON text summary with dimensions, mime type, byte size, and saved paths;
- MCP `image` content items, so Claude Code can visually inspect the generated images immediately;
- saved files under `save_dir` when `save=true`.

If Claude only needs files and does not need to inspect pixels, use:

```text
download_latest_generated_images
```

with:

```json
{
  "max_images": 4,
  "save_dir": "~/Downloads/chatgpt-images"
}
```

Typical Claude Code workflow:

1. Call `submit_image_prompt` with prompt and optional `reference_image_paths`.
2. Wait until ChatGPT Web visibly finishes generation.
3. Call `get_latest_generated_images` to see the results and save them.
4. If needed, call `submit_image_prompt` again with revision instructions.

## Tool arguments

```json
{
  "prompt": "image prompt text",
  "preset": "poster",
  "aspect_ratio": "portrait",
  "reference_image_paths": ["/absolute/path/to/ref.png"],
  "submit": true,
  "prefix": "Generate an image from this prompt.",
  "cdp_endpoint": "http://127.0.0.1:9222"
}
```

- `prompt` is required.
- `preset` is preferred and overrides the basic aspect-ratio instruction.
- `aspect_ratio` is backward-compatible fallback: `landscape`, `square`, `portrait`.
- `reference_image_paths` is optional, local absolute paths readable by macOS user `the Chrome user`; max 10 images.
- `submit=false` uploads refs and inserts prompt without pressing Enter.
- `prefix` defaults to `Generate an image from this prompt.`; for exact user-authored prompts, set `prefix` to an empty string if the wrapper should not prepend its own instruction.

## Exact-prompt forwarding pattern

When the user asks to "send this prompt" and especially when the prompt already contains its own parameters, do **not** use the default `prefix` / `preset` behavior unless the user requested it: `send_prompt.mjs` prepends text such as "Generate an image..." and aspect-ratio instructions, which can unintentionally change the prompt. For exact forwarding:

1. Save the user's prompt verbatim to a temp `.txt` file to preserve line breaks and avoid shell quoting problems.
2. Ensure reference images are absolute paths readable by Chrome's macOS user. If the attachment is under `~/.hermes/desktop-attachments/`, copy it into the working project folder under `~/...` and use that copy.
3. Connect to Chrome CDP (`http://127.0.0.1:9222`), upload the reference via the last `input[type="file"]`, wait a few seconds for thumbnail/upload preparation, insert the exact prompt text into the composer, and press Enter.
4. Report the ChatGPT conversation URL, submitted status, reference image path, and prompt character count.

This direct Playwright pattern is preferred over the MCP wrapper for exact user-authored prompts because it avoids automatic prompt rewriting while still using the same real Chrome/CDP bridge.

Available presets:

```text
landscape, square, portrait, widescreen, ultrawide, story, poster,
book_cover, banner, profile, thumbnail, product
```

## Troubleshooting

Detailed Claude Code tool-visibility notes live in `references/claude-code-visibility.md`.

- Tool not found in Telegram: restart gateway (`hermes gateway restart` or `/restart` from gateway if available) because MCP discovery happens at startup.
- Claude Code says it only sees the old tool list: restart Claude Code completely. MCP stdio servers are spawned and tool schemas are cached at Claude startup; editing `server.mjs` does not update a running Claude session. Kill stale `node ~/.hermes/chatgpt-web-prompt-mcp/server.mjs` processes if needed, then start Claude again.
- Claude Code launched with `--allowed-tools` may hide this server unless the tools are explicitly allowed. Allow names are typically:
  - preferred server:
    - `mcp__chatgpt-web-prompt__submit_image_prompt`
    - `mcp__chatgpt-web-prompt__get_latest_generated_images`
    - `mcp__chatgpt-web-prompt__download_latest_generated_images`
  - legacy `hermes-image` compatibility server:
    - `mcp__hermes-image__generate_image`
    - `mcp__hermes-image__image_backend_status`
    - `mcp__hermes-image__submit_image_prompt`
    - `mcp__hermes-image__get_latest_generated_images`
    - `mcp__hermes-image__download_latest_generated_images`
- Verify the MCP server itself exposes all tools with a `tools/list` smoke test; current expected tools are `submit_image_prompt`, `get_latest_generated_images`, and `download_latest_generated_images`.
- Chrome not connected: run `npm run login`, log into ChatGPT, keep the Chrome window open.
- Reference upload fails: confirm the file path is absolute and under `~/...`, and that ChatGPT UI supports attachments in the current chat/model.
- Do not use the old Playwright Firefox/Nightly flow; it triggered CAPTCHA loops. This bridge uses real Chrome CDP.
