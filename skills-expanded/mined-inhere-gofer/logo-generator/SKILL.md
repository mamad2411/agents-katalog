---
name: logo-generator
description: Design original, production-ready logo systems as deterministic SVG and export PNG, ICO, favicon, PWA icons, and local HTML comparison sheets without image-generation APIs or LLM API keys. Use when Codex needs to create or refine a brand mark, wordmark, app icon, browser favicon, logo variants, monochrome logo, or reusable web brand assets directly in a repository.
---

# Logo Generator

Create logos with SVG geometry and local conversion tools. Do not call image-generation APIs, require API keys, copy existing logos, or depend on remote showcase generation.

## Workflow

1. Inspect the product, existing UI tokens, asset conventions, and target surfaces. Ask only for missing choices that materially change the result.
2. State a compact design brief: exact brand text, audience, core metaphor, 3–5 adjectives, required variants, palette, and avoid list.
3. Read [references/design-system.md](references/design-system.md) before drawing. Choose three genuinely different concepts, not parameter variations.
4. Initialize an output workspace:

   ```powershell
   python <skill-dir>/scripts/logo_tool.py init --output <project-dir> --name <brand-name>
   ```

5. Draw monochrome SVG concepts first. Use simple primitives and paths, explicit `viewBox`, accessible `<title>`/`<desc>`, no external resources, no scripts, and no embedded raster images.
6. Validate every concept, create the local comparison sheet, and visually inspect it at 512, 128, 32, and 16px. Use a browser when available.

   ```powershell
   python <skill-dir>/scripts/logo_tool.py validate <project-dir>/concepts/*.svg
   python <skill-dir>/scripts/logo_tool.py showcase <project-dir>/concepts/*.svg --output <project-dir>/showcase.html
   ```

7. Refine one direction, then add color. Deliver at least a symbol-only mark and either a true wordmark or combination mark when requested. A “text-only” version must contain no detached symbol.
8. Export final assets locally:

   ```powershell
   uv run --with pillow python <skill-dir>/scripts/logo_tool.py render <final.svg> --output <exports-dir> --sizes 1024,512,256,128,64,48,32,16 --favicon --app-name <brand-name> --background "#111827"
   ```

9. Re-run validation, inspect the 16/32px outputs, run the consuming project’s build, and report paths, palette, minimum sizes, generation command, and validation results.

## Design gates

- Make the silhouette recognizable in one color before adding palette or effects.
- Keep one primary idea and at most two core elements. Preserve generous negative space.
- Avoid generic AI sparkle, brain, globe, shield, chat bubble, and initials unless the product meaning makes them distinctive.
- Use paths for custom wordmarks. If editable `<text>` is intentionally used, name the font stack and also deliver a path-converted production version.
- Use a dedicated simplified favicon when the full mark does not survive at 16px.
- Preserve transparent backgrounds for normal exports. Give Apple touch icons a solid background.
- Never claim trademark clearance. Flag similarity concerns and recommend a professional search before commercial registration.

## Tool behavior

`logo_tool.py` is deterministic and performs no network or model calls itself. Rendering invokes `npx sharp-cli`; ICO assembly uses Pillow through `uv`. If Node/npm or uv is unavailable, keep the validated SVG deliverables and report the missing local runtime instead of switching to a keyed API.

Do not edit the bundled script during ordinary use. Patch it only when fixing the skill itself.
