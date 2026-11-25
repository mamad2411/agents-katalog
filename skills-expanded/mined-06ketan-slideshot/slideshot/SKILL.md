---
name: slideshot
description: "Use this skill when the user wants to create slide carousels, LinkedIn carousels, Instagram posts, pitch decks, infographics, or presentations — or convert HTML to high-res PNG, WebP, or PDF images. Triggers: 'slides', 'carousel', 'deck', 'presentation', 'render HTML to images', 'LinkedIn post', 'Instagram carousel', 'pitch deck', 'make a slide deck', or any .slide HTML content."
license: MIT
metadata:
  author: ketan-chavan
  version: "4.3.0"
  homepage: https://slideshot.vercel.app
  repository: https://github.com/06ketan/slideshot
compatibility: "Requires Node.js >= 18. Works with Claude Desktop, Cursor, and any MCP-compatible client."
---

# Slideshot — HTML to Slides

Slideshot converts HTML with `.slide` elements into pixel-perfect slide images and documents.

## Quick Reference

| Task | Tool | When to use |
|------|------|-------------|
| Start any slide request | `discover_themes` | **MANDATORY first.** Resets the discovery gate. Returns themes, orientation/format/token-mode catalog, and persisted user preferences. |
| List themes mid-conversation | `list_themes` | Idempotent — does NOT advance the workflow. Use when the user asks "what other themes are there?" |
| Create slides (full HTML) | `create_slides` mode=default | AI writes complete HTML. More creative control, more tokens. |
| Create slides (JSON data) | `create_slides` mode=token_saver | AI sends structured JSON `slides[]`. Server uses built-in templates. Fewer tokens, lighter styling. |
| Iterate on saved deck | `edit_slides` | Token-efficient partial edits — `replace_slide`, `patch_css`, `swap_token`, `patch_class`. Use INSTEAD of regenerating the whole deck for small changes. |
| Render to files | `render_slides` | ONLY after user confirms preview. Requires discover + create first. |
| Diagnose failures | `health_check` | Render fails or Chromium won't launch. |

## MCP Setup

```json
{
  "mcpServers": {
    "slideshot": {
      "command": "npx",
      "args": ["-y", "slideshot-mcp"]
    }
  }
}
```

Add to Claude Desktop config or `.cursor/mcp.json`.

## Workflow (with mandatory STOP points)

1. Call `discover_themes` to get themes, orientations, token modes, and format options
2. **⛔ STOP** — Use ONLY native selector prompts (DO NOT render themes as a separate markdown list). Ask user: theme, topic, orientation, token mode, format. DO NOT ask how many slides — AI decides based on topic depth. WAIT for explicit answers.
3. Show a **data outline** — bullet-point list of proposed slides (e.g. "Slide 1: Cover — ..., Slide 2: Key Stats — ..."). **⛔ STOP** — Ask user: "Does this outline look good, or do you want changes?" WAIT. Loop until confirmed.
4. Based on token mode:
   - **Default**: Call `create_slides` with mode=default, theme, orientation (no html) to get CSS prompt. Generate HTML. Call again with html= to save.
   - **Token Saver**: Call `create_slides` with mode=token_saver, theme, orientation, slides=[structured JSON]
5. **⛔ STOP** — Show saved HTML as code preview artifact using htmlPath. Ask user: "Does this look good? Should I render?" WAIT for confirmation. DO NOT call render_slides in the same turn.
6. If user wants changes: revise and call create_slides again (loop steps 4-5 until approved)
7. User confirms → Call `render_slides` with htmlPath and chosen formats

**Server-enforced gates**: `render_slides` will REJECT the call if `discover_themes` or `create_slides` hasn't been called first.

## Token Modes

| Mode | Tokens | Control | How it works |
|------|--------|---------|-------------|
| `default` | ~6,000-9,000 per deck | Full | AI writes complete HTML+CSS. Maximum flexibility. Use this unless the user explicitly chose token_saver. |
| `token_saver` | ~1,500-3,000 per deck | Limited | AI sends a structured `slides[]` JSON array. Server assembles HTML from per-theme templates that cover all 11 slide types (cover, content, stats, list, steps, comparison, quote, code, cta, timeline, team). Lighter styling and less creative control. |

### Picking a mode

- **Default** when the user wants a polished, distinctive deck or has specific design notes.
- **Token saver** when the user is iterating on content / wants speed / explicitly asks for it.
- For small follow-up tweaks on either mode, prefer `edit_slides` over re-running `create_slides`.

### token_saver JSON shape (high level)

```json
{
  "mode": "token_saver",
  "theme": "branded",
  "orientation": "linkedin",
  "slides": [
    { "type": "cover", "headline": "Title", "subtitle": "Subtitle" },
    { "type": "stats", "title": "Highlights", "cards": [{ "value": "10x", "label": "faster" }] },
    { "type": "cta", "headline": "Follow", "action": "@ketan-chavan" }
  ]
}
```

Each slide type has its own required fields — see `discover_themes` output for the full schema.

## edit_slides — partial edits

| Operation | Required args | What it does |
|-----------|---------------|--------------|
| `replace_slide` | `slideIndex`, `payload`=`<div class="slide">...</div>` HTML string | Swaps one slide block, leaves the rest byte-identical. |
| `patch_css` | `payload`=CSS rules string | Appends rules to the document's last `<style>` block. |
| `swap_token` | `payload`=`{ "--var": "value" }` | Replaces a CSS variable's declared value (root-level token swap). |
| `patch_class` | `slideIndex`, `payload`=`{ add?: "x", remove?: "y" }` | Toggles a class on a specific slide. |

Always show the returned `htmlPath` as a code-preview artifact and STOP — wait for user confirmation before calling `render_slides`.

## Quick-start presets

`discover_themes` returns three presets via `presets[]` and a `usePreset` selector:

- `linkedin-default` → branded theme, 4:5, PDF
- `instagram-square` → terminal-editorial theme, 1:1, PNG+WebP
- `pitch-deck-landscape` → pitch-deck theme, 16:9, PDF+PPTX

If the user picks one, skip the per-question selectors and go straight to topic + outline confirm.

## Persistent preferences

`~/.slideshot/preferences.json` stores `lastTheme`, `lastOrientation`, `lastFormats`, `brandName`, `lastTokenMode`. Each successful `create_slides` and `render_slides` call updates them. The next session's `discover_themes` surfaces them as `default` on the matching selectors.

## Themes (8 variants)

| Variant | Name | Style |
|---------|------|-------|
| `generic` | Clean Minimal | Inter font, white cards, flexible layout |
| `branded` | Ketan Slides | Space Mono monospace, teal/coral accents |
| `instagram-carousel` | Terminal Editorial | Inter 900 + JetBrains Mono, cream + rust, terminal cards |
| `infographic` | Infographic | Data-heavy, DM Sans, stat cards |
| `pitch-deck` | Pitch Deck | Professional, DM Sans, KPI cards |
| `dark-modern` | Dark Modern | Neon accents, glassmorphism, Inter |
| `editorial` | Editorial | Magazine serif, Playfair Display, gold |
| `browser-shell` | Browser Shell | Browser window chrome, Bebas Neue + DM Sans |

## Orientation Presets

| Preset | Dimensions | Use case |
|--------|-----------|----------|
| portrait | 540x675 | Default social/LinkedIn |
| landscape | 1920x1080 | Presentations (16:9) |
| linkedin | 540x675 | LinkedIn carousel PDF |
| instagram | 1080x1080 | Square posts/carousel |
| a4 | 595x842 | Document/print format |
| custom | user-specified | Any size |

## Output Formats

| Format | Best for |
|--------|----------|
| PDF | LinkedIn carousels, sharing, printing |
| WebP | Lightweight web/social images |
| PNG | High-quality images, universal compatibility |

## Slide Types (token_saver mode)

cover, content, stats, list, steps, comparison, quote, code, cta, timeline, team

## HTML Structure (default mode)

```html
<div class="slide" style="width: 540px; height: 675px;">
  <h1>Slide Title</h1>
  <p>Content here</p>
</div>
```

Use Google Fonts via `<link>` tags. Each `.slide` becomes one output page/image.

## CLI Alternative

```bash
npx slideshot ./slides.html --formats png,webp,pdf --scale 4 --out ./output
```

## Web App

Paste HTML and export at [slideshot.vercel.app](https://slideshot.vercel.app).
