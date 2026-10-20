---
name: nano-tech-diagrams
description: Create and edit tech diagrams via a nano-tech-diagrams MCP server (Nano Banana 2 through Fal AI). Text-to-image, image-to-image, whiteboard cleanup, and 28+ style presets. Requires an externally configured MCP server — this plugin does not ship one. Use when the user wants a technical diagram generated or cleaned up.
allowed-tools: Bash(curl *), Bash(test *), Bash(file *), Bash(mkdir *), Bash(rm *), Read, Write
---

# Nano Tech Diagrams

This skill drives a **nano-tech-diagrams** MCP server to create and transform tech diagrams using Fal AI's Nano Banana 2 model.

## Prerequisite: the MCP server is not bundled

This plugin does **not** ship or configure any MCP server. Before this skill can do anything, the user must have configured, in their coding tool's MCP settings (`.mcp.json` for Claude Code or Cursor, `~/.codex/config.toml` for Codex, `opencode.json` for OpenCode):

1. A **nano-tech-diagrams** server exposing `list_styles`, `list_diagram_types`, `whiteboard_cleanup`, `image_to_image`, and `text_to_image`.
2. If that server runs anywhere other than the local machine, an **S3-compatible object store** server (e.g. MinIO) exposing a presign tool, used for file staging below.

Tool names are namespaced by whatever the user called their server, so they take the shape `mcp__<server-name>__nano-tech-diagrams__*` and `mcp__<store-name>__presign_url`. Resolve the actual names from the tools available in session rather than assuming any particular deployment.

**If neither server is configured, say so and stop.** There is no local fallback — Nano Banana 2 is a hosted model.

## File Staging

Skip this section entirely when the MCP server runs on the same machine as the files and accepts local paths.

When the server runs remotely it cannot read local file paths, and a local-path call fails with `ENOENT`. For any tool that takes an `image_path`, upload the file to the object store and pass a presigned GET URL instead — the MCP accepts `http(s)` URLs directly.

Ask the user for the staging bucket name the first time; do not assume one.

### Staging workflow:
1. **Presign a PUT URL**: `presign_url(bucket="<staging-bucket>", key="staging/<filename>", method="put")`
2. **Upload**:
   ```bash
   curl -sSf -X PUT -T "/local/path/to/image.jpg" "$put_url" \
     || { echo "Upload failed — check the presigned URL has not expired" >&2; exit 1; }
   ```
   `-f` matters: without it curl exits 0 on an HTTP error and the pipeline proceeds with a URL that serves nothing.
3. **Presign a GET URL** for the same key (`method="get"`) and pass it as `image_path` to the MCP tool.
4. Presigned URLs are short-lived (commonly 1 hour; check the `expires` param). If a call fails with a 403 or `SignatureDoesNotMatch`, re-presign rather than retrying the stale URL. Objects in a `*-transient` style bucket typically expire on a lifecycle policy — do not treat staged files as durable storage.

### Batch staging:
For multiple files, repeat the presign-PUT/curl/presign-GET cycle per file (presign calls can be batched), collect the URLs, then call the MCP tools. If any upload fails, record which file and continue with the rest; report the failures at the end.

### When staging is NOT needed:
- `text_to_image` — no input image required
- When `image_path` is already an `http://` or `https://` URL (Fal media, any public host)

## Saving output locally

The MCP returns a `fal.media` URL. If the server has a `download_to` parameter, note that it writes to the *server's* filesystem — which is not the local one when the server is remote. Download the returned URL directly:

```bash
curl -fsSL -o "/absolute/local/path/output.png" "$fal_url" \
  || { echo "Download failed — the fal.media URL may have expired" >&2; exit 1; }
file "/absolute/local/path/output.png"
```

Keep `-f` and verify with `file` before reporting success: without them a expired-link HTML error page lands on disk named `.png` and is reported as a generated diagram.

## Available Tools

| Tool | Purpose |
|------|---------|
| `list_styles` | Show all 28+ visual style presets (key, name, category, default aspect ratio) |
| `list_diagram_types` | Show all diagram type presets (network, flowchart, mind map, etc.) |
| `whiteboard_cleanup` | Clean up a whiteboard photo into a polished diagram |
| `image_to_image` | Transform an existing image into a styled tech diagram |
| `text_to_image` | Generate a diagram from a text description (no input image) |

## Defaults

- **Model**: Nano Banana 2 (baked in, not configurable)
- **Resolution**: 1K (default)
- **Reasoning**: Minimal (default)
- **Output format**: PNG
- **Aspect ratio**: auto (pass as parameter to override)

## Workflow

### For whiteboard cleanup:
1. Stage the image if the server is remote (presign PUT, `curl -T`, presign GET; see "File Staging" above)
2. Optionally ask about style preference — default is `clean_polished`
3. Call `whiteboard_cleanup` with the presigned URL as `image_path`
4. If domain-specific terms are present, pass them as `dictionary_words` for accurate spelling
5. Download the returned `fal.media` URL locally (see "Saving output" above) (see "Saving output" above)

### For image-to-image transformation:
1. Stage the image if the server is remote (presign PUT, `curl -T`, presign GET; see "File Staging" above)
2. Determine what transformation is needed: style change, diagram type conversion, or custom prompt
3. Call `image_to_image` with at least one of: `prompt`, `style`, or `diagram_type`, and the presigned URL as `image_path`
4. Common combos: `style=blueprint` + `diagram_type=network_diagram`
5. Download the returned `fal.media` URL locally (see "Saving output" above)

### For text-to-image generation:
1. Get the user's description of what diagram they want
2. Pick an appropriate `diagram_type` if it matches a preset
3. Pick a `style` if the user has a visual preference
4. Call `text_to_image` — no staging needed (no input image)
5. Download the returned `fal.media` URL locally (see "Saving output" above)

## Style Categories

- **Professional**: clean_polished, corporate_clean, hand_drawn_polished, minimalist_mono, ultra_sleek, blog_hero
- **Creative**: colorful_infographic, comic_book, isometric_3d, neon_sign, pastel_kawaii, pixel_art, stained_glass, sticky_notes, watercolor
- **Technical**: blueprint, dark_mode, flat_material, github_readme, photographic, terminal_hacker, visionary
- **Retro & Fun**: chalkboard, psychedelic, mad_genius, retro_80s, woodcut
- **Language**: bilingual_hebrew, translated_hebrew

## Diagram Types

- **Infrastructure**: network_diagram, cloud_architecture, kubernetes_cluster, server_rack
- **Software**: system_architecture, microservices, api_architecture, database_schema
- **Process**: flowchart, decision_tree, sequence_diagram, state_machine, pipeline
- **Conceptual**: mind_map, wireframe, gantt_chart, comparison_table, org_chart

## Notes

- For batch processing, call tools sequentially to avoid API rate limits
- The `dictionary_words` parameter helps with domain-specific terminology (e.g., ["Kubernetes", "Proxmox", "PostgreSQL"])
- Aspect ratio options: auto, 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9, 9:21
- Resolution options: 0.5K, 1K (default), 2K, 4K
- Staging buckets are usually configured with a short object lifecycle and presigned URLs with a ~1-hour TTL. Both are properties of the user's own deployment, not of this skill — check them if calls start failing mid-batch.
- Every MCP call can fail (rate limit, model error, expired credential). Surface the server's error text to the user rather than retrying blindly; only presigned-URL expiry is worth an automatic re-presign and one retry.
