# md2xhs — Export Markdown to Xiaohongshu (RedNote) Images

Convert a Markdown file into a series of 3:4 ratio PNG images, formatted for Xiaohongshu (RedNote / 小红书). Each page is automatically paginated — elements are never split across pages.

## Usage

```
/md2xhs <file.md> [output-dir] [--watermark "Your Name"]
```

**Arguments:**
- `file.md` — Path to the Markdown file (required). Supports relative and absolute paths.
- `output-dir` — Directory to save the images (optional). Defaults to the same directory as `file.md`.
- `--watermark "text"` — Watermark text shown in the top-left corner of each image (optional).

**Examples:**
```
/md2xhs note.md
/md2xhs note.md ./images
/md2xhs note.md ./images --watermark "LanLance"
/md2xhs ~/Documents/article.md
```

## Prerequisites

This skill requires the **md2pic CLI** to be installed globally.

**Install via npm:**
```bash
npm install -g md2pic
```

**Verify installation:**
```bash
md2pic --help
```

If `npm` is not available, install Node.js first: https://nodejs.org

## What It Does

1. Parses your Markdown and renders it with full support for:
   - Math formulas (KaTeX: `$...$` inline, `$$...$$` block)
   - Diagrams (Mermaid: flowcharts, sequence diagrams, Gantt charts)
   - Data charts (ECharts: bar, line, pie, etc.)
   - Callout cards (`:::card info`, `> [!note]` Obsidian syntax)
   - Code blocks with syntax highlighting (Prism.js)
2. Splits the content into 3:4 ratio pages — no element is cut in half
3. Adds a watermark signature to the top-left corner of each page
4. Saves each page as a numbered PNG: `md2pic-xhs-{timestamp}-1.png`, `-2.png`, ...

## Implementation

When this skill is invoked:

1. **Parse args** — extract `<file>`, optional `[output-dir]`, and optional `--watermark "text"` from the user's input
2. **Resolve path** — convert the file path to absolute using the current working directory
3. **Check file exists:**
   ```bash
   test -f "<resolved-file>" && echo "exists" || echo "not found"
   ```
   If not found, tell the user: "File not found: `<path>`. Please check the path and try again."
4. **Determine output directory:**
   - If `output-dir` was provided → use it
   - Otherwise → use `dirname` of the input file
5. **Detect browser (macOS fallback):**
   Puppeteer's bundled Chromium may crash on newer macOS versions (25+). Before running the command, probe for a usable browser in this order:
   ```bash
   # 1. System Google Chrome (most common on macOS)
   test -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" && echo "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
   # 2. Chromium via Homebrew
   which chromium 2>/dev/null
   # 3. Google Chrome CLI alias
   which google-chrome 2>/dev/null
   ```
   - If any path is found → store it as `BROWSER_PATH`
   - If none found → leave `BROWSER_PATH` unset (Puppeteer uses its bundled Chromium)
6. **Build the command:**
   - If `BROWSER_PATH` is set, prepend `PUPPETEER_EXECUTABLE_PATH="<BROWSER_PATH>"` to the command
   - Without watermark: `[PUPPETEER_EXECUTABLE_PATH="..."] md2pic "<file>" "<outDir>" --xhs`
   - With watermark: `[PUPPETEER_EXECUTABLE_PATH="..."] md2pic "<file>" "<outDir>" --xhs --watermark "<text>"`
7. **Run the command** using the Bash tool
8. **Handle errors:**
   - If exit code is non-zero and output contains "command not found":
     > ❌ `md2pic` is not installed. Run: `npm install -g md2pic`
   - If exit code is non-zero and output contains "Failed to launch the browser process":
     > ❌ Puppeteer could not launch a browser. See the Troubleshooting section below.
   - If exit code is non-zero for another reason, show the error output to the user
9. **On success** — list the generated files:
   ```bash
   ls "<outDir>"/md2pic-xhs-*.png 2>/dev/null
   ```
10. **Report results** — tell the user how many images were generated and their full paths. Example:
    > ✅ Generated 3 images in `/Users/you/notes/`:
    > - `md2pic-xhs-20260331102817-1.png`
    > - `md2pic-xhs-20260331102817-2.png`
    > - `md2pic-xhs-20260331102817-3.png`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `command not found: md2pic` | Run `npm install -g md2pic` |
| `npm: command not found` | Install Node.js from https://nodejs.org |
| Images are blank or empty | Ensure the Markdown file has content |
| Puppeteer fails to launch Chrome (macOS) | The skill auto-detects system Chrome. If it still fails, verify Chrome is installed at `/Applications/Google Chrome.app`. You can also set the path manually: `PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" md2pic ...` |
| Puppeteer fails to launch Chrome (Linux) | Install Chrome: `apt-get install -y google-chrome-stable`, then the skill will auto-detect it via `which google-chrome` |
| Permission denied on output dir | Check write permissions or choose a different output directory |

## About md2pic

**md2pic** is a zero-build-toolchain Markdown-to-image tool. All rendering happens in a headless browser — no server required, fully offline.

- GitHub: https://github.com/LgoLgo/md2pic
- Web UI: https://lgolgo.github.io/md2pic
- License: Apache-2.0
