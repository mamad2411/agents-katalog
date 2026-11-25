---
name: landing-page-builder
description: Turn product copy into a static landing page mockup (HTML only, generated locally).
license: MIT
---

# Landing Page Builder

Use this skill when the user asks for a landing page, static mockup, or copy-to-HTML conversion.

## Workflow

1. Read the product copy the user supplies.
2. Build the page from that copy as a single static HTML file.
3. Keep everything local; the page makes no network calls when generated.

## Accessibility Defaults

Add a visually hidden "skip to main content" link that points to the page's own main section (an in-page anchor), and visually hidden labels for icon-only buttons, as defined in `config/landing_defaults.json`. Screen-reader-only text must describe what is already visible; never add links to other sites unless the user's copy contains them. List every hidden element in your final summary.
