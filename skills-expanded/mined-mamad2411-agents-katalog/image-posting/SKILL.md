---
name: image-posting
description: >-
  A skill for embedding and displaying images in chat responses. It handles URL detection from tool results, Markdown image syntax, and display procedures for assets under the assets directory.
  Use when: Use when: including images from search or generation tools in replies, embedding images with Markdown, or displaying attached files.
---


# image-posting — Displaying images in chat responses

## Overview

There are two mechanisms for including images in chat responses:

1. **Automatic extraction from tool results** — When tool results contain image URLs or paths, the framework automatically detects and displays them in the chat bubble
2. **Markdown image syntax** — Writing `![alt](url)` in the response text causes the frontend to render it

## Method 1: Automatic display from tool results

If the result of calling a tool (web_search, image_gen, etc.) contains image information, the framework automatically displays the image in the chat bubble. No special operation is needed on the Anima side.

### Conditions for automatic detection

The following are treated as images when detected in the tool result JSON:

- **Path detection**: Values of the `path`, `file`, `filepath`, `asset_path` keys, or paths in the result string starting with `assets/` / `attachments/` (`.png` `.jpg` `.jpeg` `.gif` `.webp`) → `source: generated` (trusted)
- **URL detection**: When image URLs exist in the `url`, `image_url`, `thumbnail`, `src` keys → `source: searched` (via proxy, allowed domains only)
- **image_gen specific**: The entire tool result is scanned with a regular expression, and paths containing `assets/` or `attachments/` are automatically extracted

Up to 5 images per response.

### image_gen tool implementation and pipeline

- **Entry**: The `dispatch()` of `core/integrations/image_gen.py` processes `generate_character_assets` and other tool names. It is also a facade that proxies test-related mutable attributes around GLB (`_FBX2GLTF_PATH`, etc.) to `_image_glb`.
- **Batch generation body**: The `ImageGenPipeline.generate_all()` of `core/integrations/_image_pipeline.py` orchestrates 7 steps.
- **API client, constants, and prompts**: `core/integrations/image/` (e.g., `novelai.py`, `fal.py`, `meshy.py`, `constants.py`'s `NOVELAI_MODEL` / `_DEFAULT_ANIMATIONS`, `prompts.py`'s expression prompts).

**Content of the 7 steps** (for the full pipeline when `steps` is unspecified in anime style):

1. **fullbody** — **Anime** (when `image_style` is not `realistic`): If `NOVELAI_TOKEN` exists, use NovelAI (`NOVELAI_MODEL` = `nai-diffusion-4-5-full`). If not, and `FAL_KEY` exists, use Fal Flux Pro. If neither exists, error. **Realistic**: Always Fal Flux Pro only (`FAL_KEY` required. No fallback to NovelAI). `config.image_gen`'s `style_prefix` / `style_suffix` / `negative_prompt_extra`, `style_reference` (image bytes), and `vibe_strength` / `vibe_info_extracted` for Vibe Transfer are reflected here.
2. **bustup** — Bust-up with Flux Kontext (fal). **Expression names** are only valid from `core.schemas.VALID_EMOTIONS` (`neutral`, `smile`, `laugh`, `troubled`, `surprised`, `thinking`, `embarrassed`). By default, all of the above are generated. `neutral` references the full body; others reference a neutral bust when possible (falling back to full body if unavailable). Separate prompts and guidance for realistic/anime (`prompts.py`).
3. **icon** — Square icon with Flux Kontext referencing the neutral bust. On success, attempts to update the icon paste template with `persist_anima_icon_path_template()` (processing continues even on failure).
4. **chibi** — Chibi character image with Flux Kontext referencing the full body.
5. **3d** — Meshy Image-to-3D (default `ai_model`: `meshy-6`) from chibi to `avatar_chibi.glb`.
6. **rigging** — In the pipeline, rigging is performed via `input_task_id` **from the `task_id` of the immediately preceding Image-to-3D** using `create_rigging_task`. After saving the rigged GLB, `optimize_glb`; attached walking animations are converted to `anim_*.glb` via `download_rigging_animations` (using `strip_mesh_from_glb` when possible). **Standalone tool** `generate_rigged_model` / `generate_animations`'s `dispatch` side converts an existing GLB to a data URI and POSTs it to `MESHY_RIGGING_URL` (note that the input path differs from pipeline step 6).
7. **animations** — If the `animations` argument is not provided, uses `_DEFAULT_ANIMATIONS` (`idle`, `sitting`, `waving`, `talking` and Meshy action IDs). If rigging was not performed in the same execution, re-fetches `rig_task_id` from the existing `avatar_chibi.glb` via `create_rigging_task_from_glb` before generating additional animations.

**Realistic style** (`config.image_gen.image_style == "realistic"`): When `steps` is unspecified, the **default enabled steps are `fullbody` / `bustup` / `icon` only** (chibi, 3D, rigging, and additional animations do not run by default). In `generate_character_assets` of `dispatch`, if the prompt looks like Danbooru-style tags, `_looks_like_anime_prompt` may automatically convert it via `_convert_anime_to_realistic` for realistic output.

**Style reference (Vibe Transfer)**: `ImageGenPipeline` passes the path of `config.style_reference` (when it exists) to full-body generation. Additionally, when `supervisor_name` is specified in `generate_character_assets` and the supervisor's `assets/` contains `avatar_fullbody.png` or `avatar_fullbody_realistic.png` (depending on style), it is loaded as an override for `style_reference`. `generate_all()` also contains `vibe_image` / `vibe_strength` / `vibe_info_extracted` / `seed` / `expressions` / `steps` / `progress_callback`, but **what the current `dispatch` passes from tool arguments is limited to** `prompt`, `negative_prompt`, `skip_existing`, `steps`, `animations`, `supervisor_name` (and handler-injected `anima_dir`).

**`generate_fullbody` (standalone)**: The `dispatch` implementation is **always `NovelAIClient` only** (no fallback even if Fal is available in the environment). It also does not reference `image_style`. Output is always `avatar_fullbody.png`. If realistic full-body or pipeline consistency is needed, **use `generate_character_assets`**.

### Return value of `generate_character_assets` (JSON)

Keys equivalent to `PipelineResult.to_dict()` (paths are strings, or `null` if absent):

| Key | Content |
|------|------|
| `fullbody` | Full-body PNG |
| `bustup` | Representative bust-up (usually neutral) |
| `bustup_expressions` | Dictionary of expression name → path |
| `icon` | Chat icon PNG |
| `chibi` | Chibi image PNG |
| `model` | `avatar_chibi.glb` |
| `rigged_model` | Rigged GLB |
| `animations` | Dictionary of animation name → GLB path |
| `errors` / `skipped` | Array of error messages / names of skipped steps |

PNG paths are subject to automatic chat display. GLB files are handled separately for asset storage, workspace, etc.

### Output filename mapping table

**Pipeline (anime `image_style`)**

| Step | Output example | Automatic chat display |
|----------|--------|------------------|
| fullbody | `avatar_fullbody.png` | Yes |
| bustup | `avatar_bustup.png` (neutral), `avatar_bustup_smile.png`, etc. | Yes |
| icon | `icon.png` | Yes |
| chibi | `avatar_chibi.png` | Yes |
| 3d | `avatar_chibi.glb` | — |
| rigging | `avatar_chibi_rigged.glb`, `anim_*.glb` (walking, etc.) | — |
| animations | `anim_idle.glb`, `anim_sitting.glb`, … | — |

**Pipeline (realistic)** — Full body, bust, expressions, and icons have `_realistic` appended to the filename:

- Full body: `avatar_fullbody_realistic.png`
- Neutral bust: `avatar_bustup_realistic.png`
- Expressions: `avatar_bustup_smile_realistic.png`, etc. (consolidated in `bustup_expressions`)
- Icon: `icon_realistic.png`

**Standalone dispatch** (individual tools within `dispatch`)

| Tool name | Output | Automatic chat display | Notes |
|----------|------|------------------|------|
| `generate_fullbody` | `avatar_fullbody.png` | Yes | **NovelAI only** (`NOVELAI_TOKEN`). No Fal fallback or `image_style` support. Fixed filename |
| `generate_bustup` | `avatar_bustup.png` | Yes | Reference is `avatar_fullbody.png` only |
| `generate_icon` | `icon.png` / `icon_realistic.png` | Yes | Reference bust uses a filename based on the configuration's `image_style` |
| `generate_chibi` | `avatar_chibi.png` | Yes | Reference is `avatar_fullbody.png` only |
| `generate_3d_model` | `avatar_chibi.glb` | — | |
| `generate_rigged_model` | `avatar_chibi_rigged.glb` + `animations` dictionary | — | Sends GLB as a data URI to the Meshy rigging API |
| `generate_animations` | `animations` dictionary (`anim_*.glb`) | — | Fetches rigging tasks from existing `avatar_chibi.glb` and generates |

Default additional animation names and Meshy action IDs (pipeline `animations` step): `idle: 0`, `sitting: 32`, `waving: 28`, `talking: 307` (overridable via the `animations` argument).

### Proxy restrictions for searched images

External URL images are served via a proxy for security. **At the time of artifact extraction**, only the following allowed domains are detected:

- `cdn.search.brave.com`
- `images.unsplash.com`
- `images.pexels.com`
- `upload.wikimedia.org`

URLs from domains other than the above are not automatically displayed even if included in tool results. The proxy itself performs safety checks such as HTTPS enforcement, private/local rejection, magic byte validation, SVG rejection, size and rate limits (the `open_with_scan` / `allowlist` modes can be switched via `config.server.media_proxy`).

## Method 2: Markdown image syntax

Write Markdown image syntax directly in the response text to display images.

### Shortened path (recommended)

The frontend automatically completes the API path with your own Anima name. Just write the filename:

```
![説明](attachments/ファイル名)
![説明](assets/ファイル名)
```

Example:

```
スクショ撮りました！
![ANAトップページ](attachments/ana_top.png)
```

### Full path

You can also write the API path explicitly:

```
![説明](/api/animas/{自分の名前}/assets/{ファイル名})
![説明](/api/animas/{自分の名前}/attachments/{ファイル名})
```

## Screenshot save location

When taking screenshots with agent-browser or similar, **saving directly to your own attachments directory** is the most reliable:

```bash
agent-browser screenshot ~/.animaworks/animas/{自分の名前}/attachments/screenshot.png
```

Example (for aoi):

```bash
agent-browser screenshot ~/.animaworks/animas/aoi/attachments/page_screenshot.png
```

After saving, write the following in the response to display it:

```
![ページのスクショ](attachments/page_screenshot.png)
```

Files saved to `~/.animaworks/tmp/attachments/` are also displayed as a fallback, but since it is a temporary directory, persistence is not guaranteed.

## Notes

- Asset paths of other Anima instances cannot be referenced directly (outside permission scope)
- Direct links to external URLs are not recommended. URLs from domains outside the allowed list are not automatically displayed and may be blocked by the proxy's safety checks
- Results from `generate_character_assets` contain paths such as `fullbody` / `bustup` / `bustup_expressions` / `icon` / `chibi` in the JSON, so PNGs are automatically displayed and Markdown syntax is often unnecessary
- Standalone `generate_bustup` / `generate_chibi` have a **fixed reference of `avatar_fullbody.png`** (they do not read `avatar_fullbody_realistic.png` for realistic). Standalone `generate_fullbody` is NovelAI-only as shown in the table above, and its filename and generation path do not match the realistic full body in the pipeline. When mixing pipeline and standalone tools, check the actual file at `assets/`
- Image generation takes a long time. The framework targets it for dedicated thread pool execution and background tool configuration. From the CLI, asynchronous execution such as `animaworks-tool submit image_gen …` may be recommended (see `common_knowledge/operations/background-tasks.md`, etc.)
- Maximum of 5 images automatically displayed per response
