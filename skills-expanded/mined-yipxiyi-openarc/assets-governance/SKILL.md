---
name: assets-governance
description: Use when creating or maintaining OpenArc asset structure under docs/assets for brand files, icons, illustrations, screenshots, and references.
---

# Assets Governance

Use this skill when a repository needs structured asset organization for design, brand, or implementation continuity.

## Goal

Keep assets discoverable and connected to governance docs.

## Recommended Structure

```txt
docs/assets/
  brand/
  icons/
  illustrations/
  screenshots/
  references/
```

## Directory Purpose

- `brand/`: logos and identity assets
- `icons/`: icon systems
- `illustrations/`: illustration references
- `screenshots/`: UI captures
- `references/`: inspiration and competitor references

## Rules

- Do not create abstract-only documentation when concrete assets are available.
- Make `docs/DESIGN.md` and `docs/BRAND.md` reference relevant asset directories.
- Preserve existing asset organization when it is already coherent.
- Avoid moving large asset sets unless the user explicitly asks for migration.
