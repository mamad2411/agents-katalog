---
name: ckm:brand
description: "Brand engine: voice, visual identity, consistency, guidelines. Actions: update, review, create brand assets."
---

# Brand

Identity, voice, and asset management.

## Workflow & Sync
- **Sync**: Edit `docs/brand-guidelines.md` -> `node scripts/sync-brand-to-tokens.cjs`.
- **Injection**: `node scripts/inject-brand-context.cjs [--json]` (for prompts).
- **Validation**: `node scripts/validate-asset.cjs <path>`; `node scripts/extract-colors.cjs <image|--palette>`.

## Files
- **Source**: `docs/brand-guidelines.md`.
- **Outputs**: `assets/design-tokens.json`, `assets/design-tokens.css`.

## Reference Index
- **Strategy**: `voice-framework.md`, `messaging-framework.md`, `visual-identity.md`.
- **Specs**: `color-palette-management.md`, `typography-specifications.md`, `logo-usage-rules.md`.
- **QC**: `consistency-checklist.md`, `approval-checklist.md`, `asset-organization.md`.
- **Tools**: `scripts/validate-asset.cjs`, `scripts/extract-colors.cjs`.

## Subcommands
`update`: Sync brand to design systems (`references/update.md`).
`starter`: `templates/brand-guidelines-starter.md`.
