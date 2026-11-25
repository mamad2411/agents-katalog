---
name: scriptorium-epub-tools
description: >-
  Reference guide for the EPUB build pipeline toolchain. Use when: understanding
  what external tools are needed, asking why Mermaid or code blocks are rendered
  the way they are, troubleshooting EPUB rendering issues, or deciding whether to
  install mmdc. Covers mmdc, Puppeteer, highlight.js, and Node.js built-ins — what
  each tool does, what problem it solves, and when it is required vs optional.
license: MIT
---

# EPUB Build Toolchain

`scripts/build-epub.js` is designed around a **zero-required-npm-dependency** core,
with optional tools that progressively enhance the output.

---

## Tool Map

```
Node.js ≥18 (required)
    └── system zip (required)
    └── mmdc — @mermaid-js/mermaid-cli (optional, global install)
           └── Chromium — bundled with mmdc via Puppeteer
                    └── highlight.js — loaded via CDN at render time
```

---

## Tool Details

### 1. Node.js ≥ 18 + system `zip`

| Attribute | Value |
|-----------|-------|
| **Required** | ✅ Yes (core) |
| **Install** | Already on macOS/Linux; Windows: WSL or Git Bash |
| **What it does** | Generates all XHTML chapters, OPF/NAV/NCX documents, cover SVG; packages everything with `zip` |
| **npm deps** | None — uses only `fs`, `path`, `os`, `crypto`, `child_process` |

---

### 2. mmdc (`@mermaid-js/mermaid-cli`)

| Attribute | Value |
|-----------|-------|
| **Required** | ⚪ Optional (graceful fallback) |
| **Install** | `npm install -g @mermaid-js/mermaid-cli` |
| **Detected at** | Startup via `which mmdc`; stored in `MMDC_PATH` |
| **What it does** | Renders ` ```mermaid ``` ` code blocks to **PNG** images before EPUB is built |
| **Why PNG not SVG** | EPUB readers apply their own CSS to SVG `<foreignObject>` HTML, causing text to appear white or invisible. PNG is rasterised by Chromium — colours are baked in, the reader cannot interfere. |
| **Fallback** | Mermaid block is preserved as `<pre class="mermaid-source">` with an install hint |

**Config used with mmdc:**
```json
{
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#C8E6FA", "primaryTextColor": "#111111",
    "secondaryColor": "#D4EDDA", "secondaryTextColor": "#111111",
    "lineColor": "#444444", ...
  }
}
```
`theme:'base'` prevents headless Chrome's dark-mode from overriding node fill colours.

---

### 3. Puppeteer (bundled with mmdc)

| Attribute | Value |
|-----------|-------|
| **Required** | ⚪ Optional (auto-detected from mmdc) |
| **Install** | Automatic — bundled at `.../@mermaid-js/mermaid-cli/node_modules/puppeteer` |
| **Detected at** | Startup: `fs.realpathSync(MMDC_PATH)` → resolve symlink → find sibling `node_modules/puppeteer` |
| **What it does** | Runs a headless Chromium session to syntax-highlight code blocks |
| **Stored in** | `PUPPETEER_DIR` constant |

**Detection code:**
```js
const PUPPETEER_DIR = (() => {
  if (!MMDC_PATH) return null;
  try {
    const real = fs.realpathSync(MMDC_PATH);         // resolve symlink
    const p = path.join(path.dirname(path.dirname(real)), 'node_modules', 'puppeteer');
    return fs.existsSync(path.join(p, 'package.json')) ? p : null;
  } catch { return null; }
})();
```

**Why a child process?**
The build script is synchronous; Puppeteer is async. A child `node` process runs the
async Puppeteer session and writes `results.json`. The parent reads it after the child exits.

**Why `page.goto('file://')` not `page.setContent()`?**
In the bundled Puppeteer version, `setContent()` leaves `document.body === null` in
subsequent `evaluate()` calls. Loading a local HTML file via `file://` URL works correctly.

---

### 4. highlight.js (CDN, loaded per build)

| Attribute | Value |
|-----------|-------|
| **Required** | ⚪ Optional (only when Puppeteer available) |
| **Install** | None — loaded via CDN: `cdnjs.cloudflare.com/…/highlight.js/11.9.0/…` |
| **What it does** | Syntax-highlights code blocks; `atom-one-dark` theme |
| **Output** | Inline `style="color:rgb(…)"` attributes on every token span |

**Why inline styles (not CSS classes)?**
CSS class-based syntax highlighting (`hljs-keyword`, `hljs-string`, etc.) requires a
stylesheet to be applied. EPUB readers may strip or override external stylesheets.
Inline `style` attributes are always applied — guaranteed correct colours everywhere.

**Extraction pattern:**
```js
// Inside page.evaluate():
hljs.highlightElement(el);
el.querySelectorAll('[class]').forEach(span => {
  const cs = window.getComputedStyle(span);
  let s = '';
  if (cs.color) s += 'color:' + cs.color + ';';
  if (cs.fontStyle !== 'normal') s += 'font-style:' + cs.fontStyle + ';';
  if (cs.fontWeight !== '400')   s += 'font-weight:' + cs.fontWeight + ';';
  if (s) span.setAttribute('style', s);
  span.removeAttribute('class');   // remove class — rely on inline style only
});
```

---

## Batch Rendering Architecture

All code blocks in a book are rendered in **one** Chromium session (not one per block).
Browser startup (~3s) is paid once; subsequent blocks cost ~1s each.

```
build()
  │
  ├── Phase 1: mdToXhtml() for each chapter
  │     Code blocks → placeholder tokens (\x00CBID:cb-N\x00)
  │     Collected in pendingCodeBlocks[]
  │
  ├── Phase 2: batchRenderCodeBlocks()
  │     Write tasks.json + init.html + runner.js to tmpDir
  │     execSync('node runner.js')   ← one browser session
  │       ├── page.goto('file://init.html')   ← loads hljs from CDN
  │       ├── for each task: evaluate() → extract inline-styled HTML
  │       └── write results.json
  │     Read results.json → populate codeRenderResults{}
  │
  └── Phase 3: write chapter XHTML files
        Replace \x00CBID:cb-N\x00 → <pre class="highlighted"><code>…</code></pre>
```

---

## Config Options

In the user-editable CONFIG section of `build-epub.js`:

| Option | Default | Description |
|--------|---------|-------------|
| `RENDER_CODE_AS_PNG` | `false` | `false` = inline-styled HTML (text copyable). `true` = PNG screenshot (carbon-style, text NOT copyable) |

---

## Capability Matrix

| Feature | No tools | mmdc only | mmdc + Puppeteer |
|---------|----------|-----------|-----------------|
| Markdown → XHTML | ✅ | ✅ | ✅ |
| Cover SVG | ✅ | ✅ | ✅ |
| Mermaid diagrams | `<pre>` fallback | ✅ PNG | ✅ PNG |
| Code syntax highlight | Plain `<pre><code>` | Plain `<pre><code>` | ✅ Inline styled |
| Code as PNG | ❌ | ❌ | ✅ (opt-in) |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Mermaid text white / invisible in EPUB | SVG `<foreignObject>` CSS overridden by reader | Use PNG output (`-o diagram.png`) — already default |
| Code blocks have no colour | Puppeteer not found | Install `mmdc` globally; Puppeteer comes with it |
| `document.body is null` error | `page.setContent()` bug in bundled Puppeteer | Use `page.goto('file://')` — already implemented |
| Build slow (many code blocks) | Multiple Chrome launches | Batch renderer uses one session — already implemented |
| CDN unreachable (offline) | highlight.js CDN blocked | Code blocks fall back to plain `<pre>` gracefully |
