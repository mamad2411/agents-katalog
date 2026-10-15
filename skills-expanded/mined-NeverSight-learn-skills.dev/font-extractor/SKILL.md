---
name: font-extractor
description: Extract and download all fonts from a website, organized into ./fonts/<font-family>/ subdirectories. Use this skill whenever the user wants to grab, rip, download, or extract fonts from a website or URL — even if they just say "get the fonts from this site", "download the fonts used on this page", or "what fonts does this website use?". Works with both static and JavaScript-rendered pages.
---

# Font Extractor

Extract all fonts used on a website and save them locally, organized by font family.

## Workflow

0. **Ask** — confirm where to save fonts (default: `./fonts/`)
1. **Download** — find and download all font files from the site
2. **Organize** — run the bundled script to sort them into family subdirectories

The heavy lifting of family detection is done by reading each font file's internal name table — no need to parse CSS family names.

---

## Step 0: Confirm output location

Before downloading, ask the user where they'd like the fonts saved. Default to `./fonts/` if they don't have a preference. Use their chosen path in place of `./fonts/` throughout the remaining steps.

---

## Step 1: Download all font files

Fetch the page HTML and find font file URLs. Use whatever approach gets the job done fastest:

- Parse `<link rel="stylesheet">` tags, fetch each CSS file, extract `url(...)` values from `@font-face` blocks
- Check `<link rel="preload" as="font">` tags
- Search inline `<style>` blocks
- If nothing turns up in CSS, search the JS bundle(s) for font file URLs (SPAs often embed them there)
- If using Claude-in-Chrome (`mcp__claude-in-chrome__*`), `read_network_requests` will catch dynamically loaded fonts

Font file extensions to look for: `.woff2`, `.woff`, `.ttf`, `.otf`, `.eot`

Download every font file URL you find into `./fonts/` (flat). Use `curl -L` with a Referer header matching the page URL — many CDNs require it:

```bash
mkdir -p ./fonts
curl -L -H "Referer: <page-url>" -o "./fonts/<filename>" "<font-url>"
```

Download all unique URLs. Do not deduplicate — different URLs may be different versions or formats of the same font, and the user may want all of them.

---

## Step 2: Organize by family

Run the bundled organize script. It reads each font file's internal metadata to determine its family name, then moves files into `./fonts/<family>/` subdirectories:

```bash
uv run ~/git/agent-skills/font-extractor/scripts/organize_fonts.py ./fonts
```

The script handles everything: reads the font name table, creates family directories, moves files. Fonts whose family can't be read get `Unknown-1`, `Unknown-2`, etc.

---

## Step 3: Report

Show the user what was downloaded:

```bash
find ./fonts -type f | sort
```

Include the family count, file count, and total size.
