---
name: init-brand
description: Create, migrate, or revise an OfficeKit brand identity shared by documents, slides, and videos. Use for logos, palettes, typography, design tokens, brand guidelines, or adding another named identity.
compatibility: Requires an OfficeKit workspace created by setup-office-kit and Python 3.10+ with uv.
metadata:
  author: OfficeKit
  version: "0.2.0"
---

# Initialize an OfficeKit brand

Work in the repository's `.office-kit/` workspace. If it does not exist, use
`setup-office-kit` first. Perform this workflow in the main agent; do not
depend on a client-specific subagent.

## Contract

Each identity lives at `.office-kit/brands/<id>/`:

- `brand.json` is canonical and machine-readable.
- `BRAND.md`, `tokens.css`, and `frame.md` are generated from `brand.json`.
- supplied assets are preserved byte-for-byte under `assets/`.
- a second company, client, or product is a new identity, never an overwrite.

Brand IDs use lowercase letters, digits, and hyphens. The fallback identity is
`[brand].default` in `.office-kit/config.toml`.

## Approval gate

Inspect the user's assets and requirements, then present one concrete proposal:
brand ID, palette roles, typography, logo use, contrast/accessibility, and any
derived assets you intend to create. Wait for explicit approval before writing
brand files. This is the only approval gate in OfficeKit.

Research competitive or accessibility claims directly with tools available in
the host client, only when the identity depends on that evidence. Do not require
an MCP server or another plugin.

## Write and generate

After approval:

1. Preserve supplied assets without modification.
2. Write `.office-kit/brands/<id>/brand.json`.
3. Generate and validate derivatives from `.office-kit/`:

   ```bash
   uv run python scripts/brand/generate.py <id>
   ```

4. If the default changed, edit only `[brand].default` in `config.toml`.
5. Refresh embedded consumers:

   ```bash
   uv run python scripts/document/doc.py refresh --all
   uv run python scripts/video/video.py refresh <video-slug>
   ```

Decks consume `tokens.css` directly and need no refresh. Never hand-edit a
generated derivative. Report the identity path, validation result, preserved
assets, and refreshed projects.
