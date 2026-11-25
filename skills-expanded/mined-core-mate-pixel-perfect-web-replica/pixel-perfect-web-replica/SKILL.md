---
name: pixel-perfect-web-replica
description: Recreate public frontend pages locally with high visual fidelity. Use when the user asks Codex or Claude Code to pixel-perfect clone, mirror, study, sandbox, reproduce, or locally run a public website/page; capture its static assets; preserve layout, scroll animations, media, typography, and interactions; compare screenshots; and list replaceable resources for rebranding or customization.
---

# Pixel-Perfect Web Replica

## Core Goal

Build a local sandbox replica of a public frontend page for implementation study. Preserve the page's visible structure, CSS behavior, media assets, typography, scroll effects, and lightweight interactions as closely as legal public access allows. Do not perform unauthorized login, scraping of private data, bypassing, exploit testing, or destructive scanning.

## Default Workflow

1. **Scope the target**
   - Confirm the target URL and intended local output folder.
   - Treat public HTML/CSS/JS/media as the source of truth.
   - If the page requires auth, stop at the public surface unless the user provides authorized local artifacts.

2. **Collect public evidence**
   - Fetch HTML and headers with `curl -L` and `curl -I -L`.
   - Capture desktop and mobile screenshots of the original page before editing.
   - Extract text, links, resources, meta tags, and obvious runtime behavior.

3. **Mirror static resources**
   - Prefer the bundled script:
     ```bash
     python3 <skill_dir>/scripts/mirror_public_page.py <url> <output_dir>
     ```
   - The script downloads the HTML, same-origin referenced assets, CSS `url(...)` assets, favicon/manifest assets when discoverable, and writes resource inventories.
   - If the site uses external build chunks, CSS files, or JS files, inspect and mirror their nested `url(...)` dependencies too.

4. **Make it run locally**
   - Use a static server, not `file://`, so root-relative paths, video, fonts, and fetch behavior match the browser.
   - Default command:
     ```bash
     cd <output_dir>
     python3 -m http.server 8088
     ```
   - If the port is busy, either stop the existing process or use a new port.

5. **Preserve implementation**
   - If the original is a static single page, keep original HTML/CSS/JS first for maximum fidelity.
   - If rebuilding into cleaner source files, preserve exact copy, section order, breakpoints, font loading, media dimensions, timing, easing, and scroll scene thresholds.
   - Do not replace real assets with generic gradients/placeholders unless the asset cannot be obtained; document any such deviation.

6. **Verify visually**
   - Use browser screenshots at the original comparison sizes, at least desktop and mobile.
   - Use `view_image` on original and local screenshots in the same QA pass.
   - Compare at least: logo/header, first viewport composition, typography, media framing, background/gradient, scroll state, mobile crop, FAQ/buttons/links, and footer.
   - Fix missing assets, root paths, broken fonts, video autoplay/crop, and mobile overflow before final.

7. **List replaceable resources**
   - Produce `REPLACEABLE_RESOURCES.md` with path, type, current role, replacement guidance, and gotchas.
   - Produce `resource-inventory.json` with paths, byte sizes, categories, and detected file types.
   - Call out brand assets, fonts, app screenshots/videos, hero media, OG images, legal links, CTA URLs, and copy blocks.

## Local Replica Output Checklist

Every completed replica should include:

- `index.html` or equivalent local entrypoint.
- Local `media/`, `font/`, `fav/`, `og/`, or equivalent asset folders.
- `resources.json` or `resource-inventory.json`.
- `REPLACEABLE_RESOURCES.md`.
- A short run instruction, usually in the final response rather than a separate README unless useful for the project.
- Desktop and mobile local screenshots when practical.

## Fidelity Rules

- Preserve the original page's visible copy unless the user asks for rebranding.
- Preserve original paths when easiest; static servers make root-relative paths work.
- Preserve fonts. If fonts are missing or licensed files cannot be mirrored, use the closest fallback and disclose it.
- Preserve original video dimensions and aspect ratios; phone mockup pages are especially sensitive to crop drift.
- Preserve scroll-driven animation mechanics: `sticky`, `clip-path`, `transform`, `opacity`, `requestAnimationFrame`, video `play/pause`, and resize measurement.
- Avoid "improving" the design during replica work. Improvements belong in a separate modernization pass.

## Safety And Legal Boundaries

- Use only public resources that a normal browser can access.
- Do not bypass auth, paywalls, robots protections, bot defenses, CSP, CORS, or signed URL restrictions.
- Do not collect user data, cookies, tokens, private API responses, or session-specific information.
- For external publication, tell the user to replace copyrighted/brand assets and verify licensing. Local study can keep mirrored public assets for inspection.

## Bundled Resources

- `scripts/mirror_public_page.py`: mirrors a public page and same-origin static assets into a local folder; also writes resource inventories and a replaceable-resource starter file.
- `references/replica-qa.md`: detailed QA checklist for screenshot comparison and common root-relative asset bugs. Read it when visual verification fails or the page has complex scroll animation.
- `references/quality-checklist.md`: general web replica QA checklist for rebuilds that go beyond static mirroring.
