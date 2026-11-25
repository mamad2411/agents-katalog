---
name: learn-platform
description: >
  Discover how to automate a new app or website. Explore UI elements, scrape docs,
  build selector references. Use when: "learn how to automate", "explore the UI of",
  "map the interface", "discover selectors", "build reference for", "what can you do in this app",
  "how does this app work", "explore app".
allowed-tools:
  - mcp__sh__platform_explore
  - mcp__sh__platform_learn
  - mcp__sh__platform_guide
  - mcp__sh__apps
  - mcp__sh__windows
  - mcp__sh__ui_tree
  - mcp__sh__browser_dom
  - mcp__sh__browser_page_info
  - mcp__sh__browser_navigate
  - mcp__sh__screenshot_file
  - mcp__sh__browser_open
  - mcp__sh__memory_recall
  - mcp__sh__memory_save
  - mcp__sh__memory_query_patterns
---

# Platform Discovery & Learning

You are exploring a new app or website to build automation knowledge — discovering UI elements, selectors, keyboard shortcuts, and flows.

## Intelligence Wrapper

Every tool call returns automatic hints. When you navigate to a URL or focus an app, the server auto-loads any matching reference file and injects selector hints, known errors, and strategy suggestions into responses. Watch for `[HINT]`, `[WARNING]`, and `[STRATEGY]` lines.

## Check Existing Knowledge First

Always start with:
```
platform_guide(platform="{name}")
memory_recall(task="explore {name}")
memory_query_patterns(scope="{name}")
```

**Existing reference files** (use these exact names with `platform_guide`):
- Social: `x-twitter`, `instagram`, `linkedin`, `reddit`, `threads`, `youtube`, `discord`
- Design: `figma`, `canva-smoke-test`
- Video: `davinci-resolve-keyboard`, `davinci-resolve-menu-map`, `davinci-resolve-menus-batch1` through `batch4`
- Dev: `codex-desktop`, `n8n`, `devto`, `devpost`
- Google: `google-flow`

If a reference already exists, review it before exploring further. You may not need to re-explore.

## Two Discovery Modes

### Mode 1: Interactive Exploration (`platform_explore`)

Discovers all interactive elements by actively testing them.

**For web apps:**
```
platform_explore(url="https://app.example.com", maxElements=30)
```

What it does:
1. Navigates to the URL
2. Finds all interactive elements (buttons, links, inputs, menus, tabs)
3. Filters out dangerous elements (delete, logout, etc.)
4. Tests each element (click, check what changed)
5. Compiles a reference JSON with working selectors, navigation map, errors

**For native apps:**
```
platform_explore(bundleId="com.example.App")
```

What it does:
1. Launches the app if not running
2. Maps the full AX tree
3. Records all interactive elements (buttons, menus, text fields)
4. Does NOT auto-click native elements (safety)
5. Compiles reference with element roles, titles, paths

**Output**: Saved to `references/{platform}.json`.

### Mode 2: Documentation Scraping (`platform_learn`)

Learns from official documentation without interacting with the app.

```
platform_learn(platform="{name}", url="https://docs.example.com/shortcuts")
```

What it does:
1. Generates likely doc/help URLs from the platform name
2. Navigates Chrome to each URL
3. Extracts text content, keyboard shortcuts (table parsing), CSS selectors
4. Compiles into a reference with shortcuts, features, API endpoints, limitations

Best doc URLs to provide:
- Keyboard shortcuts page
- Getting started / quick start guide
- API documentation
- Accessibility / developer docs

**Output**: Saved to `references/{platform}.json`.

## Manual Exploration Workflow

When the automated tools aren't enough, explore manually:

### For native apps:
1. `apps` → find the target app
2. `focus(bundleId)` → bring to front
3. `ui_tree(pid, maxDepth=3)` → get overview of top-level elements
4. `ui_tree(pid, maxDepth=8)` → deep dive into specific areas
5. `screenshot_file` → visual reference
6. Test interactions: `ui_press`, `menu_click`, `key`
7. Record what works

### For web apps:
1. `browser_navigate(url)` → open the app
2. `browser_dom(selector="button, a, input, [role='button'], [role='tab']")` → all interactive elements
3. `browser_page_info` → page structure
4. Test key selectors with `browser_click`
5. Navigate to different pages, repeat
6. `screenshot_file` at each major section

## Combining Both Modes

For comprehensive coverage:
1. `platform_learn` first → get keyboard shortcuts and documented features
2. `platform_explore` second → discover actual UI elements and test them
3. The results merge into a single reference file

## Output Quality

A good reference file contains:
- **platform**: Name for matching
- **bundleId** or **urlPatterns**: For automatic context loading
- **selectors**: Grouped by feature area (navigation, compose, settings, etc.)
- **flows**: Named step sequences for common tasks
- **errors**: Known issues with context and solutions
- **shortcuts**: Keyboard shortcuts with descriptions

## Save

After exploration:
- The reference is auto-saved to `references/{platform}.json`
- Call `memory_save(task="explored {platform}")` to record the exploration strategy
- The reference is immediately usable by `platform_guide` and the context tracker

$ARGUMENTS
