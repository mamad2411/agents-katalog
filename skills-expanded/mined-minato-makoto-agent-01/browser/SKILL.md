---
name: browser
description: Control a Chromium browser through Playwright for navigation, interaction, extraction, screenshots, and JS evaluation.
module: builtin_tools.browser_tools
tools:
  - browser_navigate
  - browser_click
  - browser_type
  - browser_screenshot
  - browser_get_content
  - browser_evaluate
  - browser_wait
  - browser_scroll
  - browser_select
  - browser_reset_context
  - browser_close
---

# Browser Skill

Automates a real browser session with persistent page context across calls.

## Prerequisites

1. Install dependency: `pip install playwright`
2. Install browser: `playwright install chromium`

## Tool contracts

### `browser_navigate`
- Required: `url` (string)
- Returns: `{title, url}` after navigation

### `browser_click`
- Optional locators: `selector`, `role` + `name`, `text`
- Rule: provide at least one locator

### `browser_type`
- Required: `text_to_type` (or backward-compatible `text`)
- Optional locators: `selector`, `role` + `name`, `text`, `name`

### `browser_screenshot`
- Optional: `full_page` (boolean, default `false`)
- Returns file path under `workspace/screenshots`

### `browser_get_content`
- Optional: `selector`, `mode`
- `mode`: `text` (default) or `accessibility`

### `browser_evaluate`
- Required: `js_code`
- Use only for deterministic, task-related page inspection/manipulation

### `browser_wait`
- Optional locators: `selector`, `role` + `name`, `text`
- Optional: `timeout` in milliseconds (default `10000`)

### `browser_scroll`
- Required: `direction` (`up` or `down`)
- Optional: `amount` pixels (default `500`)

### `browser_select`
- Required: `selector`, `value`

### `browser_reset_context`
- No arguments
- Recreates browser context/page for clean test isolation

### `browser_close`
- No arguments
- Closes persistent browser resources
