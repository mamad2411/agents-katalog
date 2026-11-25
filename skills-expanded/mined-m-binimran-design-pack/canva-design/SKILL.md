---
name: canva-design
description: Create or edit a branded layout in Canva via the connector - from a brand template, then export. Use for social posts, flyers, decks, and marketing collateral that should stay on-brand and fast.
---

# canva-design

Fast, on-brand layouts using the **Canva connector** and your brand template/kit.

## Process
1. **Start from a brand template** (or brand kit) so colours/type/logo are already correct - don't rebuild from scratch.
2. **Brief the layout:** purpose, dimensions/platform, headline + supporting copy, imagery, CTA.
3. **Generate/assemble** via the Canva connector; place copy and imagery; keep hierarchy clear.
4. **Apply brand kit** (colours, fonts, logo with correct clear space).
5. **Export** the right format/size (hand to `asset-export`); note any AI/stock licensing.

## Output
- The Canva design (confirm the connector created/updated it) + export, with the brief it fulfills.

## Guardrails
- Stay on-brand (the `brand-compliance-reviewer` agent checks); don't introduce off-brand colours/fonts.
- Don't claim a design exists in Canva unless the connector returned it.
- Respect Canva element licensing for commercial use.
