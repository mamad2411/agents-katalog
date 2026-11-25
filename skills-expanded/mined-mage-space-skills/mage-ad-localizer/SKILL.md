---
name: mage-ad-localizer
description: |
  Localize static ads into other languages and markets with Mage: translate
  every line of on-image text naturally (not word for word), keep the offer,
  brand voice, product, logo, fonts, and layout, and adjust line breaks,
  number and currency formats, and right-to-left layouts so each version
  reads as native. Uses GPT Image 2.5 Flare for precise text replacement.
  Use when: "translate this ad", "localize this ad", "Spanish and German
  versions", "adapt this ad for Japan", "make this ad in French", "ad in
  Arabic", "international versions of my ad", "market-specific ad copy".
  NOT for: new creative variations (use mage-ad-multiplier), resizing for
  placements (mage-ad-resizer), translating video voiceovers, or documents
  and websites.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Ad Localizer

Make native-feeling versions of a static ad for other languages and markets. You write the translations; Mage replaces the text in the image while the product, logo, layout, and design stay put.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **The ad is a link:** an https URL of the image file, a data URL under about 3 MB, or an upload from disk (`create_upload`). Files attached to the chat never reach Mage.

## UX rules

1. **Show the copy before generating.** Present a table of the source lines and each language's version, with the total price, and wait for approval or edits. Brand teams often have approved copy: accept theirs as is.
2. Translate meaning and tone, not words: the offer must stay the same offer, the voice the same voice.
3. Never translate the brand name, product names, or trademarked taglines unless the user says to. Keep legal text, and flag it: it may need a local legal review.
4. Deliver one labeled link per language. Links expire after 30 days.
5. Reply in the user's language; the ad copy is in the target language.

## Workflow

1. **Transcribe** every line of text in the ad, in reading order, with its role: headline, subline, body, CTA, price, legal, label.
2. **Translate** each line per target language with `references/localization-notes.md`: length, line breaks, formats, script. Mark lines that must stay as they are (brand, product name).
3. **Approve.** Show the copy table and the total Gems; wait for a yes.
4. **Generate** one image per language with GPT Image 2.5 Flare (`gpt_image_2`, `gpt-image-2.5-flare`), the original in `image`, the original's `aspect_ratio`, `resolution: "2K"`:

   ```
   Localize the ad in @image1 into <language> for <market>. Replace each text
   line exactly as follows, keeping its font style, weight, color, size, and
   position:
   "<source line 1>" → "<translation 1>"
   "<source line 2>" → "<translation 2>"
   "<CTA>" → "<translated CTA>"
   Keep "<brand name>" unchanged. Do not change the product, its packaging
   text, the logo, the imagery, or the layout. Adjust line breaks so the text
   fits the same areas.
   ```

   For right-to-left languages, add: "Mirror the text alignment to right-to-left; keep the product and logo where they are."

5. **Price and wait:** `get_model`, `estimate_cost` per language, `generate` each (new UUID `idempotency_key`), `get_request` with `wait_seconds: 120`.
6. **Proofread** each result if you can see it, character by character against the approved copy, including accents and diacritics. Regenerate once for any mistake, quoting the failed line.

Product packaging text is part of the product: leave it in the source language unless the user supplies localized packaging.

## Deliver

```text
Localized ads ready:
- Spanish (Spain): https://…
- German: https://…
```

List any lines left untranslated on purpose (brand, legal) and anything that needs a native reviewer.

## References

- `references/localization-notes.md`: text expansion, line breaks, scripts, number and currency formats, and cultural checks by language.
