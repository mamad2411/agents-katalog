---
name: stock-source
description: Find and license stock imagery via the Unsplash connector (or other libraries) with proper attribution and commercial-use checks. Use when you need real photography rather than AI generation.
---

# stock-source

Real, licensable photos sourced and credited correctly.

## Process
1. **Define the shot:** subject, mood, orientation, colour, where it'll be used (web/print/social), commercial?
2. **Search** via the **Unsplash connector** (or Pexels/Getty as needed). Shortlist a few that fit the direction.
3. **Check the license:** Unsplash is free incl. commercial with conditions; some libraries require a paid
   license for commercial use - confirm before client work.
4. **Record attribution** ("Photo by X on Unsplash") even where not strictly required - the `license-guard`
   hook flags missing attribution.
5. **Download + name + optimize** (hand to `asset-export`).

## Output
- The selected image(s) from the connector, the license/attribution, and the optimized export.

## Guardrails
- Confirm commercial rights for client work; record source + license in the asset manifest.
- Don't present a photo as licensed if you haven't checked its terms.
