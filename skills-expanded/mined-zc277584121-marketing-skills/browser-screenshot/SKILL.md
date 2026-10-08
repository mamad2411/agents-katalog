---
name: browser-screenshot
description: Take focused, region-specific screenshots from web pages using a dedicated headed Chrome profile with persistent login state. Navigates to the right page based on user context (URL, search query, social media post), locates the target region via DOM selectors, and crops to a clean, focused screenshot without attaching to the user's daily browser.
---

# Skill: Browser Screenshot

Take focused screenshots of specific regions on web pages — a Reddit post, a tweet, an article section, a chart, etc. — not just a full-page dump.

> **Prerequisite**: `agent-browser` must be installed. This skill uses its own headed Chrome with a dedicated persistent profile; the user's daily Chrome does not need remote debugging.

## Dedicated Browser Profile

Use the same dedicated persistent profile convention as `my-chrome-automation`:

```bash
PROFILE_DIR="${AGENT_BROWSER_PROFILE:-$HOME/.agent-browser-chrome}"
NAMESPACE="${NAMESPACE:-browser-screenshot}"
SESSION="${SESSION:-focused-capture}"

ab() {
  agent-browser --namespace "$NAMESPACE" --session "$SESSION" --headed --profile "$PROFILE_DIR" "$@"
}
```

Run every browser command through `ab`. Do not use `--auto-connect`, generic CDP discovery, or the user's daily Chrome profile. The dedicated profile preserves cookies and login state across tasks while allowing the user's normal Chrome to remain open and untouched.

Choose a descriptive `SESSION` for the task when practical. Do not run multiple tasks against the same profile concurrently; reuse it sequentially to avoid profile-lock conflicts.

If the target site requires login, open it with `ab`, pause for the user to complete login or verification in the dedicated headed window, and then continue with the same profile and session.

### If the Dedicated Profile Is Already Running

A second Chrome launch with the same profile may exit before creating a DevTools endpoint. Never fall back to whichever Chrome happens to be open. Either reuse a known Agent Browser session for this profile, or explicitly attach only to a Chrome process whose command line contains the exact `--user-data-dir=$PROFILE_DIR` value.

On macOS, identify that dedicated process and its local CDP port like this:

```bash
PROFILE_PID="$(ps -axo pid=,command= | awk -v profile="--user-data-dir=$PROFILE_DIR" 'index($0, profile) && index($0, "--remote-debugging-port=") && $0 !~ /Helper/ {print $1; exit}')"
CDP_PORT="$(lsof -nP -a -p "$PROFILE_PID" -iTCP -sTCP:LISTEN | awk 'NR > 1 && $9 ~ /^127\.0\.0\.1:[0-9]+$/ {split($9, parts, ":"); print parts[2]; exit}')"

ab() {
  agent-browser --namespace "$NAMESPACE" --session "$SESSION" --cdp "$CDP_PORT" "$@"
}
```

Require non-empty, unambiguous `PROFILE_PID` and `CDP_PORT` values before attaching. If they cannot be verified, ask the user to close the dedicated automation window and retry. Do not close a browser that this task only attached to.

---

## Overview

This skill handles the full pipeline:

1. **Research** the best page to screenshot (web search, fetch)
2. **Navigate** to the right page in the browser
3. **Locate** the target element/region on the page
4. **Capture** a focused, cropped screenshot of just that region

### Hard Rule: No Full-Screen Screenshots

**NEVER output an uncropped full-viewport or full-page screenshot as a final result.** Full screenshots contain too much noise (nav bars, sidebars, ads, unrelated content) and are unsuitable as article illustrations. Every screenshot MUST be cropped to a focused region.

---

## Step 0: Research — Find and Validate Sources Before Opening the Browser

**The browser is for capturing, not for browsing.** Before opening anything in Chrome, use text-based tools (WebSearch, WebFetch) to find candidate pages, read their content, and decide which ones are actually worth screenshotting.

### Research-First Workflow

1. **WebSearch** to find candidate pages for the topic
2. **WebFetch** each candidate to read its text content — check if it has the information/visual you need
3. **Evaluate**: Is this page worth a screenshot? Does it have a clear, focused region that would work as an illustration?
4. **Only then** open the browser to capture the screenshot

This saves significant time — most candidate pages won't be worth screenshotting, and you can eliminate them without the overhead of browser navigation.

### When to Use Browser-First Instead

Skip the WebSearch/WebFetch phase and go directly to Chrome browsing when:

- **The target platform requires login** — Reddit, LinkedIn, X/Twitter, and other social platforms often gate content behind login walls. Use the dedicated profile directly so its saved login state can be reused.
- **The user specifies a platform with a clear search need** — e.g., "find a Reddit post about X" or "screenshot a tweet about Y". Go straight to the platform's search in Chrome.
- **WebFetch returns blocked/incomplete content** — some sites aggressively block non-browser requests. If you get a 403, a CAPTCHA page, or stripped content, switch to Chrome.

In these cases, Chrome browsing replaces WebSearch — navigate to the platform's search page, browse results, and evaluate pages visually before deciding what to screenshot.

### Page Selection Strategy

The right page depends on the context of the article and how recent/notable the subject is:

| Subject Type | Best Page to Find | How to Find It |
|--------------|-------------------|----------------|
| **New model/feature launch** (< 6 months) | Official blog post announcing it | WebSearch `"<model name>" site:<vendor-domain> blog` |
| **Established product** (> 6 months) | Product landing page or docs overview | WebSearch `"<model name>" official page` |
| **Open-source model** | HuggingFace model card or GitHub repo | Direct URL: `huggingface.co/<org>/<model>` |
| **API service** | API documentation page | WebSearch `"<service name>" API docs` |

> **Note**: This table lists common subject types but is **not exhaustive**. Apply the same research-first strategy to any subject type — find the most authoritative and visually clean source page for the topic at hand.

### What Makes a Good Screenshot Source

**Core principle: Less is more. Focus on content, not chrome.**

A good screenshot source contains a **focused, self-contained piece of information** — a paragraph of text, a key quote, a data table, a diagram. It should NOT be a busy page full of buttons, navigation, sidebars, and interactive elements.

- **Prefer**: A section of a blog post with a clear heading and 1-2 paragraphs of text. A single chart or diagram. A model card header with name and description. A quote or key finding.
- **Avoid**: Full landing pages with CTAs and navigation. Dashboard views with multiple panels. Pages dominated by UI controls (buttons, dropdowns, forms) rather than readable content.
- **Official blog posts** are ideal: they have hero images, prominent titles, and concise descriptions designed for sharing
- **Product landing pages** can work but only if you crop to the hero section — ignore the rest
- **HuggingFace model cards** are reliable for open-source models: consistent layout, model name + description always at top
- **API docs** are acceptable fallback: show the product name and key specs

> **Rule of thumb**: If the region you plan to capture contains more interactive UI elements (buttons, links, nav items) than readable text content, it's a bad crop. Find a more content-rich region, or pick a different page entirely.

### Pre-Flight URL Validation

Before opening in the browser, validate URLs with WebFetch (lightweight HEAD/GET) to avoid wasting time on 404s or redirects:

```
WebFetch: <candidate-url>
→ Check status code, title, and content snippet
→ If 404 or redirect to unrelated page, try next candidate
```

### Region Selection Strategy

Think about **what the article reader needs to see** in this screenshot:

| Article Context | What to Capture | Target Region |
|-----------------|----------------|---------------|
| Introducing a model in a lineup | Model name + key tagline/description | Blog hero section or HF model card header |
| Comparing capabilities | Feature highlights or spec table | Blog section showing specs/features |
| Discussing a specific feature | The feature description | Relevant section heading + 1-2 paragraphs |
| Showing a product/service | Brand identity + value prop | Landing page hero (title + subtitle + visual) |

The screenshot should make the reader think "ah, that's what this model/product is" — not "what am I looking at?"

---

## Step 1: Navigate to the Target Page

### Always Start by Listing Tabs

```bash
ab tab list
```

Check if the page is already open in the dedicated session. Reuse its existing tabs when they have the correct login and page state.

### Navigation by Input Type

| User Provides | Strategy |
|---------------|----------|
| Direct URL | `ab open <url>` |
| Search query | `ab open https://www.google.com/search?q=<encoded-query>` → find and click the best result |
| Platform + topic | Construct platform search URL (see below) → locate target content |
| Vague description | Google search → evaluate results → navigate to best match |

### Platform-Specific Search URLs

| Platform | Search URL Pattern |
|----------|-------------------|
| Reddit | `https://www.reddit.com/search/?q=<query>` |
| X / Twitter | `https://x.com/search?q=<query>` |
| LinkedIn | `https://www.linkedin.com/search/results/content/?keywords=<query>` |
| Hacker News | `https://hn.algolia.com/?q=<query>` |
| GitHub | `https://github.com/search?q=<query>` |
| YouTube | `https://www.youtube.com/results?search_query=<query>` |

### Wait for Page Load

After navigation, wait for content to settle:

```bash
ab wait --load networkidle
```

> **Note**: Some sites (Reddit, X, LinkedIn) never reach `networkidle`. If `open` already shows the page title in its output, skip the wait. Use `wait 2000` as a safe alternative.

---

## Step 2: Locate the Target Region

This is the critical step. The goal is to find a **CSS selector** that precisely wraps the content to capture.

### Primary Method: DOM Selector Discovery

1. **Take an annotated screenshot** to understand the page layout:
   ```bash
   ab screenshot --annotate
   ```

2. **Take a snapshot** to see the page's accessibility tree:
   ```bash
   ab snapshot -i
   ```

3. **Identify the target container element**. Look for:
   - Semantic HTML containers: `<article>`, `<main>`, `<section>`
   - Platform-specific components (see [Platform Selectors](#platform-selectors))
   - Data attributes: `[data-testid="..."]`, `[data-id="..."]`

4. **Verify with `get box`** to confirm the element has a reasonable bounding box:
   ```bash
   ab get box "<selector>"
   ```
   This returns `{ x, y, width, height }`. Sanity-check:
   - Width should be > 100px and < viewport width
   - Height should be > 50px
   - If the box is the entire page, the selector is too broad — refine it

5. **If the selector is hard to find**, use `eval` to explore the DOM:
   ```bash
   ab eval "document.querySelector('article')?.getBoundingClientRect()"
   ```

### Platform Selectors

Common container selectors for popular platforms:

| Platform | Target | Typical Selector |
|----------|--------|-----------------|
| Reddit | A post | `shreddit-post`, `[data-testid="post-container"]` |
| X / Twitter | A tweet | `article[data-testid="tweet"]` |
| LinkedIn | A feed post | `.feed-shared-update-v2` |
| Hacker News | A story + comments | `#hnmain .fatitem` |
| GitHub | A repo card | `[data-hpc]`, `.repository-content` |
| YouTube | Video player area | `#player-container-outer` |
| Generic article | Main content | `article`, `main`, `[role="main"]`, `.post-content`, `.article-body` |

> These selectors may change over time. Always verify with `get box` before using.

### Multiple Matching Elements

If the selector matches multiple elements (e.g., multiple tweets on a timeline), narrow it down:

```bash
# Count matches
ab get count "article[data-testid='tweet']"

# Use nth-child or :first-of-type, or a more specific selector
# Or use eval to find the right one by text content:
ab eval --stdin <<'EOF'
const posts = document.querySelectorAll('article[data-testid="tweet"]');
for (let i = 0; i < posts.length; i++) {
  const text = posts[i].textContent.substring(0, 80);
  console.log(i, text);
}
EOF
```

Then target a specific one using `:nth-of-type(N)` or a unique parent selector.

---

## Step 3: Capture the Focused Screenshot

### Method A: Scroll + Viewport Screenshot (Preferred for Viewport-Sized Targets)

Best when the target element fits within the viewport.

```bash
# Scroll the target into view
ab scrollintoview "<selector>"
ab wait 500

# Take viewport screenshot
ab screenshot /tmp/browser-screenshot-raw.png
```

Then crop using the bounding box (see [Cropping](#cropping)).

### Method B: Full-Page Screenshot + Crop (For Any Size Target)

Best when the target might be larger than the viewport or when precise cropping is needed.

```bash
# Take full-page screenshot
ab screenshot --full /tmp/browser-screenshot-full.png

# Get the target element's bounding box
ab get box "<selector>"
# Output: { x: 200, y: 450, width: 680, height: 520 }
```

Then crop (see [Cropping](#cropping)).

### Cropping

Use ImageMagick (`magick` on IMv7, `convert` is deprecated) to crop the screenshot to the target region. Add padding for visual breathing room.

#### Retina Display Handling

**Critical**: On macOS Retina displays, screenshots are captured at 2x resolution. A 1728x940 viewport produces a 3456x1880 image. You MUST account for this:

1. **Detect the scale factor**: Compare viewport size vs actual image dimensions:
   ```bash
   # Check actual image dimensions
   magick identify /tmp/screenshot.png
   # → 3456x1880 means 2x scale on a 1728x940 viewport
   ```

2. **Multiply `get box` coordinates by the scale factor** before cropping:
   ```bash
   # get box returns viewport coordinates: { x: 200, y: 450, width: 680, height: 520 }
   # For 2x Retina, actual image coordinates are:
   SCALE=2
   X=$((200 * SCALE))
   Y=$((450 * SCALE))
   W=$((680 * SCALE))
   H=$((520 * SCALE))
   PADDING=$((16 * SCALE))
   ```

#### Crop Command

```bash
magick /tmp/browser-screenshot-full.png \
  -crop $((W + PADDING*2))x$((H + PADDING*2))+$((X - PADDING))+$((Y - PADDING)) \
  +repage \
  <output-path>.png
```

> **Important**: `get box` returns floating-point values. Round them to integers before passing to ImageMagick.

> **Padding**: Use 12–20px (viewport px). Increase to ~30px if the target has a distinct visual boundary (card, bordered box). Use 0 if the user wants a tight crop.

### Output Path

- If the user specifies an output path, use that
- Otherwise, save to a descriptive name in the current directory, e.g., `reddit-post-screenshot.png`, `tweet-screenshot.png`

---

## Step 4: Verify the Result

After cropping, **read the output image** to verify it captured the right content:

```bash
# Use the Read tool to visually inspect the cropped screenshot
```

If the crop is wrong (missed content, too much whitespace, wrong element), adjust the selector or bounding box and retry.

---

## Fallback: Visual Highlight Confirmation

When DOM-based location is uncertain — the selector might be wrong, multiple candidates exist, or the target is ambiguous — use **JS-injected highlighting** to visually confirm before cropping.

### How It Works

1. **Inject a highlight border** on the candidate element:
   ```bash
   ab eval --stdin <<'EOF'
   (function() {
     const el = document.querySelector('<selector>');
     if (!el) { console.log('NOT_FOUND'); return; }
     el.style.outline = '4px solid red';
     el.style.outlineOffset = '2px';
     el.scrollIntoView({ block: 'center' });
   })();
   EOF
   ```

2. **Take a screenshot** and visually inspect:
   ```bash
   ab screenshot /tmp/highlight-check.png
   ```
   Read the screenshot to check if the red border surrounds the correct content.

3. **If correct**, remove the highlight and proceed with cropping:
   ```bash
   ab eval "document.querySelector('<selector>').style.outline = ''; document.querySelector('<selector>').style.outlineOffset = '';"
   ```

4. **If wrong**, try the next candidate or refine the selector, re-highlight, and re-check.

### When to Use This Fallback

- The page has complex/nested components and you're not sure which container is right
- Multiple similar elements exist and you need to pick the correct one
- The user's description is vague ("that chart in the middle of the page")
- The `get box` result looks suspicious (too large, too small, zero-sized)

---

## Page Preparation: Clean Up Before Capture

Before taking the final screenshot, clean up the page for a better result:

```bash
# Dismiss cookie banners, popups, overlays
ab eval --stdin <<'EOF'
(function() {
  // Common cookie/popup selectors
  const selectors = [
    '[class*="cookie"] button',
    '[class*="consent"] button',
    '[class*="banner"] [class*="close"]',
    '[class*="modal"] [class*="close"]',
    '[class*="popup"] [class*="close"]',
    '[aria-label="Close"]',
    '[data-testid="close"]'
  ];
  selectors.forEach(sel => {
    document.querySelectorAll(sel).forEach(el => {
      if (el.offsetParent !== null) el.click();
    });
  });

  // Hide fixed/sticky elements that overlay content (nav bars, banners)
  document.querySelectorAll('*').forEach(el => {
    const style = getComputedStyle(el);
    if ((style.position === 'fixed' || style.position === 'sticky') && el.tagName !== 'HTML' && el.tagName !== 'BODY') {
      el.style.display = 'none';
    }
  });
})();
EOF
```

> **Use with caution**: Hiding fixed elements might remove important context. Only run this when overlays visibly obstruct the target region.

### Cookie Banners That Won't Dismiss

Some cookie consent banners (e.g., Jina AI's Usercentrics) live in shadow DOM or iframes and cannot be dismissed via JS `click()` or `remove()`. Don't waste time with multiple JS attempts. Instead:

1. **Crop it out** — if the banner is at the top or bottom, simply adjust the crop region to exclude it. This is the fastest and most reliable approach.
2. **Scroll past it** — scroll the target content away from the banner area before capturing.

---

## Viewport Sizing

For consistent, high-quality screenshots, set the viewport before capturing:

```bash
# Standard desktop viewport
ab set viewport 1280 800

# Wider for dashboard/data-heavy pages
ab set viewport 1440 900

# Narrower for mobile-like content (social media posts)
ab set viewport 800 600
```

Choose a viewport width that makes the target content render cleanly — not too cramped, not too stretched.

---

## Troubleshooting

### `get box` returns null or zero-sized
- The selector doesn't match any element. Use `get count "<selector>"` to verify.
- The element may be hidden or not yet rendered. Try `wait 2000` and retry.

### Cropped image is blank or wrong area
- The full-page screenshot coordinates may differ from viewport coordinates. Use `screenshot --full` with `get box` (they use the same coordinate system).
- Check if the page has horizontal scroll — `get box` x values may be offset.

### Target element is inside an iframe
- `get box` and `snapshot -i` cannot see inside iframes.
- Use `eval` to access iframe content:
  ```bash
  ab eval "document.querySelector('iframe').contentDocument.querySelector('<sel>').getBoundingClientRect()"
  ```
  Note: Only works for same-origin iframes.

### `open` succeeded but page content is wrong
- The browser may have switched to a different tab (e.g., a popup or redirect opened a new tab). Always verify after navigation:
  ```bash
  ab eval "document.location.href"
  ```
- If the URL is wrong, use `tab list` to find the correct tab and `tab goto <N>` to switch.

### Screenshot command times out on fonts
- Some pages (e.g., Google developer docs) hang on `document.fonts.ready`. Force-resolve it first:
  ```bash
  ab eval "document.fonts.ready.then(() => 'ok')"
  ```
  Then retry the screenshot.

### Page has lazy-loaded content
- Scroll down to trigger loading before taking the screenshot:
  ```bash
  ab scroll down 1000
  ab wait 1500
  ab scroll up 1000
  ```
