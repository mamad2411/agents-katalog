---
name: edit-canva
description: >
  Create and edit designs in Canva. Add elements, change text, apply templates, download
  designs, resize, add images. Use when: "edit Canva", "create in Canva", "add text in Canva",
  "download Canva design", "Canva template", "resize design", "change background in Canva".
allowed-tools:
  - mcp__sh__platform_guide
  - mcp__sh__playbook_preflight
  - mcp__sh__browser_open
  - mcp__sh__browser_navigate
  - mcp__sh__browser_click
  - mcp__sh__browser_fill_form
  - mcp__sh__browser_js
  - mcp__sh__browser_dom
  - mcp__sh__browser_wait
  - mcp__sh__screenshot_file
  - mcp__sh__key
  - mcp__sh__click_with_fallback
  - mcp__sh__type_with_fallback
  - mcp__sh__observer_start
  - mcp__sh__observer_status
  - mcp__sh__observer_stop
  - mcp__sh__memory_recall
  - mcp__sh__memory_save
  - mcp__sh__memory_query_patterns
---

# Canva Design Editing

You are editing designs in Canva using ScreenHand's browser automation.

## Intelligence Wrapper

Every tool call returns automatic hints from the server. Watch for:
- **`[HINT]`** lines — selector suggestions from reference files, known working patterns
- **`[WARNING]`** lines — this tool has failed before, here's what went wrong
- **`[STRATEGY]`** lines — suggested next step based on past successful sequences

Always read and follow these hints — they come from verified learnings and curated references.

## Important: Canva Selector Strategy

Canva uses React with dynamically generated class names — **never rely on CSS classes**. Instead use:
- `aria-label` attributes (stable across sessions)
- `data-testid` attributes (when available)
- `role` attributes combined with text content
- `button` + text content matching

## Setup

1. `platform_guide(platform="canva-smoke-test")` — load known selectors. **Note**: The reference is named `canva-smoke-test`, not `canva`.
2. `memory_recall(task="canva {task}")` — recall past strategies
3. `memory_query_patterns(scope="canva")` — check verified learnings (selectors that have worked before)
4. `browser_navigate(url="https://www.canva.com/design/{id}/edit")` — open the design
5. `browser_wait(condition="document.querySelector('[class*=\"editor\"]') !== null")` — wait for editor
6. `observer_start(bundleId="com.google.Chrome")` — start popup/cookie-banner detection for Canva

## Editor Navigation

**Left sidebar tabs** (use `aria-label` to click):
- Templates: `browser_click(selector="[aria-label='Templates']")`
- Elements: `browser_click(selector="[aria-label='Elements']")`
- Text: `browser_click(selector="[aria-label='Text']")`
- Uploads: `browser_click(selector="[aria-label='Uploads']")`
- Photos: `browser_click(selector="[aria-label='Photos']")`

**If selectors fail**: Use `browser_dom(selector="nav button, [role='tab']")` to discover current tab selectors, or use `click_with_fallback(text="Elements")` which tries AX → CDP → OCR automatically.

## Common Operations

### Edit Text
1. Double-click text element on canvas: `browser_click(x, y)` twice (get coords from `browser_dom` or `screenshot_file`)
2. Select all: `key("cmd+a")`
3. Type new text: `browser_fill_form(selector, text)` — types character-by-character like a human

### Add Text
1. Click "Text" in left sidebar
2. Click "Add a heading" / "Add a subheading" / "Add body text"
3. New text appears on canvas — double-click to edit

### Change Background
1. Click on empty canvas area (not on an element)
2. Color picker appears in top toolbar
3. Click color swatch, enter hex value

### Add Element
1. Click "Elements" in left sidebar
2. Search for element type via search bar
3. Click to add to canvas
4. Drag to position, resize handles to scale

### Upload Image
1. Click "Uploads" in left sidebar
2. Click "Upload files" button
3. File dialog opens — navigate and select
4. Drag uploaded image onto canvas

### Resize Design
1. Click "Resize" button in top toolbar via `browser_click` or `click_with_fallback(text="Resize")`
2. Enter new dimensions using `browser_fill_form`
3. Click "Resize" to apply

### Download
1. Click "Share" button (top right): `click_with_fallback(text="Share")`
2. Click "Download"
3. Select format: PNG, JPG, PDF, MP4, GIF
4. Click "Download" button
5. `browser_wait` for download to complete

## Verification

Take `screenshot_file` after each visual change to confirm the edit applied correctly.

## Cleanup

When done:
- `observer_stop()` — stop popup detection
- `memory_save(task="canva: {description}")` — persist the strategy

Canva auto-saves, no explicit save needed.

$ARGUMENTS
