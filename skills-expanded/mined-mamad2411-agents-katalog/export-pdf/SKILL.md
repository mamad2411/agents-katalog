---
name: export-pdf
description: Export an HTML artifact to PDF via headless Chromium (puppeteer Page.pdf). For multi-slide decks one page per <section>.
argument-hint: <html-path> [output.pdf]
allowed-tools: Read Write Bash(node:*) Bash(realpath:*) Bash(mkdir:*) Bash(which:*) Bash(stat:*) Bash(ls:*)
---

# Export PDF

Produce a PDF from an HTML artifact. Uses puppeteer's `Page.pdf()` which is lossless vector when the source is HTML/CSS/SVG.

**Why puppeteer instead of Chrome DevTools MCP:** the MCP does not expose `Page.printToPDF` directly (only `take_screenshot`, `list_console_messages`, `evaluate_script`, etc.). Using puppeteer via a Node script is deterministic and matches `/export-pptx`.

## Preflight

1. `Bash(which node)` — required
2. `Bash(test -d node_modules/puppeteer && echo yes || echo no)` — if no, tell user `/doctor` or run `npm i -D puppeteer`

## Steps

1. Resolve paths:
   - `$0` = input HTML (required)
   - `$1` = output (default: input with `.pdf` extension)
   - `Bash(mkdir -p $(dirname <output>))` if needed

2. Run export script:
   ```
   Bash(node scripts/export-pdf.mjs "<input>" "<output>")
   ```
   (The script exists at `scripts/export-pdf.mjs`; if missing, write it per the template below.)

3. Report size + path.

## Script template (scripts/export-pdf.mjs)

```js
#!/usr/bin/env node
// Usage: node export-pdf.mjs <input.html> [output.pdf]
import puppeteer from 'puppeteer';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';

const [, , input, output = input.replace(/\.html?$/i, '.pdf')] = process.argv;
if (!input) { console.error('Usage: export-pdf.mjs <input.html> [output.pdf]'); process.exit(1); }

const inAbs = path.resolve(process.cwd(), input);
const outAbs = path.resolve(process.cwd(), output);

const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
const page = await browser.newPage();
await page.goto(pathToFileURL(inAbs).toString(), { waitUntil: 'networkidle0' });

// If it's a deck, set noscale so deck-stage renders at natural dims
const deckDims = await page.evaluate(() => {
  const d = document.querySelector('deck-stage');
  if (!d) return null;
  d.setAttribute('noscale', '');
  return [parseInt(d.getAttribute('width') || '1920', 10), parseInt(d.getAttribute('height') || '1080', 10)];
});

await page.emulateMediaType('print');
const pdfOpts = {
  path: outAbs,
  printBackground: true,
};
if (deckDims) {
  // Deck: one section per page — @media print in deck_stage.js handles page-break
  pdfOpts.width = `${deckDims[0]}px`;
  pdfOpts.height = `${deckDims[1]}px`;
  pdfOpts.pageRanges = '';
} else {
  pdfOpts.format = 'A4';
}

await page.pdf(pdfOpts);
await browser.close();

const stat = await fs.stat(outAbs);
console.log(`wrote ${outAbs} (${(stat.size / 1024).toFixed(1)} KB)`);
```

## Notes

- For decks: deck_stage.js must have `@media print { @page { size: ... } section { page-break-after: always } }` in the global `<style>` it injects — already present.
- For general pages: defaults to A4. To override, user can pass inline CSS `@page { size: letter }` or similar.
- `networkidle0` waits for all network activity to stop — if artifact uses lazy images, bump timeout to 15000ms.
