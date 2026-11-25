---
name: vanilla-js-spa-patterns
category: software-development
description: Patterns and pitfalls when editing monolithic vanilla JavaScript SPAs (single-file HTML/CSS/JS). Covers string-concatenation rendering, conditional display, and common JS template bugs.
---

# Vanilla JS SPA Editing Patterns

Use when working with single-file JavaScript SPAs (HTML + inline CSS + inline JS, no framework).

## Core Patterns

### String Concatenation HTML Generation

Most monolithic SPAs build HTML by concatenating strings with `+`. This means:

```javascript
// Standard pattern
var html = '';
html += '<div class="item" onclick="handler(' + id + ')">';
html += '<span>' + name + '</span>';
html += '</div>';
$('container').innerHTML = html;
```

### Conditional Rendering

Use ternary operators inside string concatenation:

```javascript
// Dynamic button label based on status
var btnLabel = status === 'PENDING' ? '审核' : '查看';
html += '<button onclick="action(' + id + ')">' + btnLabel + '</button>';

// Conditional cell content
html += '<td>' + (showScore ? scoreHtml : '--') + '</td>';

// Conditional column header
html += '<th>名称</th>';
html += (showExtra ? '<th>额外列</th>' : '');
```

### Style Matching

When adjusting button/cell sizes, find the existing size pattern first:

```javascript
// Find reference: grep "width:" | grep "btn-sm" | head -5
// Match the same module's button sizes — activity page uses 56px,
// enterprise page uses 90px, user management uses 60px
```

## Common Pitfalls

### The Falsy Empty String Bug

**NEVER** chain `||` after a value that could be an empty string:

```javascript
// BAD — empty string is falsy, falls through to fallback
textbox.value = rc.globalReview || d.reviewComment;
// When globalReview="" and d.reviewComment is raw JSON, textbox shows JSON

// GOOD — explicit empty string default
textbox.value = rc.globalReview || '';
// OR
textbox.value = rc.globalReview !== undefined && rc.globalReview !== null ? rc.globalReview : d.reviewComment;
```

This applies to all falsy-but-valid values: `""`, `0`, `false`.

### Template String Quote Nesting

When building onclick handlers inside string templates, quote nesting depth > 2 will break:

```javascript
// BAD — nested quotes break
html += '<button onclick="doSomething(\'' + val + '\')">';

// GOOD — use data attributes
html += '<button data-id="' + id + '" onclick="handleClick(this)">';
// In handler: var id = el.getAttribute('data-id');
```

### Tab vs Space Indentation

Some projects use `\t` indentation. Always check before editing with `sed -n 'LINE_NUMBERp' file | cat -A` or `grep -c $'\t' file`.

### Post-edit Verification

After any JS change:
```bash
# Extract script block and check syntax
node -e "$(sed -n '/<script>/,/<\/script>/p' index.html | head -c -7 | tail -c +9)" 2>&1
```

Or for the full file:
```bash
# Extract all JS between script tags
grep -oP '(?<=<script>).*?(?=</script>)' index.html | node --check /dev/stdin 2>/dev/null
```

### Read Before Edit

**Always** read the target code section with `read_file` before editing. Do NOT rely on search results alone — they truncate context.

### ⚠️ `read_file` Output Format Gotcha

`read_file` output format is `LINE_NUM|CONTENT`. The `|` after the line number is a **separator**, not file content. When you see:

```
34|| `admin` | 参见
```

The actual file content is `| `admin` | 参见` — the FIRST `|` is the line-number separator. Copying `34||` into a `patch` `old_string` will include the extra pipe and break tables.

**Always verify with `python3 -c "open('file','rb').readlines()[N-1]"` before pasting pipe-heavy content into patch.**

### When `patch` Fails on Pipe-Heavy Content

`patch` struggles with markdown tables (pipes, dashes, varied whitespace). After **2 failures**:

1. Use `grep -nF` or Python to confirm exact bytes
2. **Switch to Python byte-level editing** — not `sed`, not another `patch` attempt:

```python
with open('file', 'rb') as f:
    lines = f.read().split(b'\n')
# Find the line, make the change
lines[N-1] = lines[N-1].replace(b'old', b'new')
with open('file', 'wb') as f:
    f.write(b'\n'.join(lines))
```

This preserves exact spacing, tabs, and special characters. Verify with `git diff` after.

## Canvas Overlay Drawing (bbox + image)

Patterns for dual-canvas comparison views (before/after overlays over one screenshot).

### Retina / devicePixelRatio

```javascript
const dpr = window.devicePixelRatio || 1;
canvas.width = Math.max(1, Math.round(cssW * dpr));
canvas.height = Math.max(1, Math.round(cssH * dpr));
canvas.style.width = cssW + 'px';
canvas.style.height = cssH + 'px';
const ctx = canvas.getContext('2d');
ctx.setTransform(dpr, 0, 0, dpr, 0, 0); // draw in CSS-pixel space; resets cleanly on resize
```

### Contain-fit transform for normalized bboxes

Backends usually return bboxes normalized to [0,1]. Map to canvas pixels preserving aspect ratio:

```javascript
function getTransform() {
  const scale = Math.min(cw / imgW, ch / imgH);
  return { drawW: imgW * scale, drawH: imgH * scale,
           offX: (cw - imgW * scale) / 2, offY: (ch - imgH * scale) / 2 };
}
// bbox [x1,y1,x2,y2] → {x: x1*drawW+offX, y: y1*drawH+offY, w: (x2-x1)*drawW, h: (y2-y1)*drawH}
```

- **Defensive**: if all bbox values > 1.5, assume pixel coords and divide by imgW/imgH first.
- Skip boxes with `w <= 0.5 || h <= 0.5` before `strokeRect` (backend may emit x2<=x1).
- Dashed proposal boxes: `ctx.setLineDash([6, 4])` … reset with `ctx.setLineDash([])` after the loop.
- Size BOTH canvases identically (contain-fit of the same image) so left/right stay aligned.

## Async Render Race Guard

Rapid navigation (case switching, upload) fires overlapping fetches; a stale response must not overwrite a newer one:

```javascript
const reqId = ++state.reqId;          // capture BEFORE any await
const resp = await fetch(url);
if (reqId !== state.reqId) return;    // stale — discard
const data = await resp.json();
if (reqId !== state.reqId) return;
```

Check after **every** await, not just the last. Clear `state.currentData`/image synchronously at render start so stale draws can't show wrong content.

## Browser Smoke Test Without a Backend

Verify a single-file SPA end-to-end before the backend exists: serve the dir with `python3 -m http.server`, then inject mocks in page context via browser_console. Full working recipe + assertion snippets: `references/canvas-overlay-spa-testing.md`. Essentials:

- Override `window.fetch` → `Promise.resolve(new Response(JSON.stringify(mock), {status:200, headers:{'Content-Type':'application/json'}}))`.
- `img.src` loads bypass `fetch` — subclass `window.Image` to swap screenshot URLs for a canvas-generated data URL.
- Trigger top-level functions directly (classic-script function declarations are global).
- Assert canvas drawing by counting pixels near target RGB via `getImageData` (sampling ONE point can land inside a box — counting is robust).
- Mock 400/500 responses to test the error path: error bar shows, no white screen.
- After every smoke test, check `browser_console` for `js_errors: []`.

## Pitfalls

### await in a non-async function → SyntaxError

`node --check` catches it — but only if you run it. When a handler needs `await` (e.g. `handleUploadFile` calling `loadImage`), declare it `async function` even if the event listener ignores the returned promise.

### Reusable label helpers with min-height guards

A `drawLabel(ctx, r, ...)` that bails when `r.h < 12` silently skips score/tag labels anchored to a zero-height rect (e.g. `{x, y: r.y + r.h, w, h: 0}` for below-the-box placement). Anchor labels inside the box, or write a dedicated score-label helper for bottom-anchored tags (guard on width only).

### Empty-state overlay gating on key presence

During upload-preview the data object may lack `vlm_elements` entirely; `data.vlm_elements || []` then triggers "no elements" overlay text on the canvas. Gate empty-state hints on `Array.isArray(data.vlm_elements)`: key present + empty array = real result (show hint); key missing = preview/in-flight state (show nothing).

## Batch File Updates

When the same change applies to multiple copies of index.html (project root + backend static):

```python
# Use Python to apply identical changes to both files
for f in ['/path/to/index.html', '/path/to/backend/static/index.html']:
    with open(f) as fh:
        content = fh.read()
    content = content.replace(old_string, new_string)
    with open(f, 'w') as fh:
        fh.write(content)
```

## Commit Pattern

After UI changes, commit with descriptive messages:
```
fix: 审核意见为空时不显示原始JSON
feat: 按状态动态显示按钮文案
fix: 待审核条目认定评分显示--
```
