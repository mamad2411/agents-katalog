---
name: workbench-ui
description: Use when editing the HTML workbench (src/render/html.ts). Covers the template-literal escaping trap, the UI conventions, and how to verify against real data before claiming done.
---

The workbench is ONE template-literal string emitting a self-contained page (embedded JSON, vanilla JS, no CDN).

**Escaping trap (breaks the page silently):** inside the emitted `<script>`, every backslash needs doubling for the outer literal - `\\n` not `\n`, `\\"` not `\"`, and regex character classes like `/[/]/` instead of escaped slashes. A single unescaped backslash produces a blank page with a console error.

**Conventions:**
- All user-visible strings live in the `T` object, English only.
- One signal, one cue: risk is the red left edge (high only), category is the small colored label, relationships are chips under the text. Never stack a second cue for the same fact.
- Negative/actionable info goes in the drawer's needs-attention block; healthy states fold into collapsed `<details class="dsec">` sections.
- Benign categories render muted; only silent (red) should pull the eye.

**Verify (required before done):**
1. `npm run build && npm test`.
2. Render real data - a repo with a populated `.wdd/` (not synthetic fixtures), via `wdd review --html` or a small node script importing `dist/render/html.js`.
3. Serve over http (file:// is blocked for MCP browsers), open with Playwright: assert **zero console errors**, click through a decision drawer, screenshot and actually look at it.
4. Clean up: temp server, screenshots, scratch scripts.
