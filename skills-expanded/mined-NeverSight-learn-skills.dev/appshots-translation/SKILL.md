---
name: appshots-translation
description: >
  AI translation and per-locale customization for App Store screenshots.
  Includes text expansion factors, font recommendations per language,
  and a verification workflow to catch overflow issues.
---

# App Screenshots Translation

Multi-language screenshot translation with AI or manual input, per-locale layout customization, and quality verification.

## Why Localize?

Apple reports that localized screenshots can increase downloads by **up to 4×**. Localization goes beyond text translation — it includes font selection, layout adjustment, and cultural adaptation.

## AI Translation Workflow

```bash
# 1. Set context for better, more relevant translations
appshots translate set-prompt --prompt "Habit tracking & productivity app for iOS"

# 2. Get all text overlays from all designs (useful for review)
appshots --json translate get-texts

# 3. AI-translate to multiple locales at once
appshots translate all --from en --to ja,ko,de,fr,es,pt,zh

# 4. Preview each locale in the editor
appshots translate preview --locale ja
```

## Text Expansion Reference

English is one of the most compact languages. Always design with expansion room:

| Language | Expansion | Key Challenge | Fix |
|----------|----------|---------------|-----|
| **German (de)** | **+30-40%** | Long compound words | `--font-size 72` (reduce ~20%) |
| **Finnish (fi)** | **+30-40%** | Very long words | `--font-size 70` |
| **French (fr)** | +15-25% | Articles lengthen | `--font-size 80` |
| **Spanish (es)** | +15-20% | Slightly longer | Minor reduction |
| **Portuguese (pt)** | +15-25% | Similar to French | Minor reduction |
| **Hindi (hi)** | +20-30% | Devanagari spacing | `--font-size 72` |
| **Japanese (ja)** | Same or shorter | Needs CJK font | `--font "Noto Sans JP"` |
| **Korean (ko)** | Same or shorter | Needs CJK font | `--font "Noto Sans KR"` |
| **Chinese (zh)** | -10-30% shorter | Needs CJK font | `--font "Noto Sans SC"` |
| **Arabic (ar)** | Varies | RTL layout | May need `--x` / position flip |
| **Thai (th)** | Varies | Tall stacking marks | Consider `--font-size` increase |

## Per-Locale Style Overrides

When a locale's text doesn't fit, override the font, size, or position for that specific locale:

```bash
# Reduce font size for German (text too long)
appshots translate override-overlay --locale de \
  --overlay-id <id> --font-size 72

# Use CJK font for Japanese
appshots translate override-overlay --locale ja \
  --overlay-id <id> --font "Noto Sans JP" --font-size 80

# Use CJK font for Korean
appshots translate override-overlay --locale ko \
  --overlay-id <id> --font "Noto Sans KR"

# Reposition text for Arabic (RTL)
appshots translate override-overlay --locale ar \
  --overlay-id <id> --x 50 --y 100

# Multiple properties at once
appshots translate override-overlay --locale de \
  --overlay-id <id> \
  --font "Inter" --font-size 70 \
  --width 900 --scale 0.9
```

### Override Properties

| Option | Description |
|--------|-------------|
| `--font` | Google Font name (e.g., "Noto Sans JP") |
| `--font-size` | Font size in points |
| `--x`, `--y` | Position override |
| `--scale` | Scale factor |
| `--rotation` | Rotation |
| `--width` | Text box width |
| `--color` | Text color (hex) |
| `--font-weight` | Weight index (0-8) |

## Per-Locale Screenshot Images

Some locales need different app screenshots (localized UI):

```bash
appshots translate set-locale-image --locale ja --file /path/to/ja_screenshot.png
appshots translate set-locale-image --locale ko --file /path/to/ko_screenshot.png
```

## Manual Translation

```bash
# Edit a single overlay's translation
appshots translate edit --locale ja --overlay-id <id> --text "習慣トラッカー"

# Bulk apply translations (JSON: overlayId → text)
# For multi-screenshots, key format is "designIndex:overlayId"
appshots translate apply-manual --locale ja \
  --translations '{"0:<overlayId>":"翻訳テキスト","1:<overlayId>":"テキスト2"}'
```

## Post-Translation Verification Workflow

**This is the most critical step. Always verify every locale visually.**

```bash
# Check worst offenders first (German = usually longest)
appshots translate preview --locale de
# → Is text cut off? Does it wrap properly? Readable?

# Check CJK rendering
appshots translate preview --locale ja
# → Is the CJK font applied? Glyphs correct?

appshots translate preview --locale ko
appshots translate preview --locale zh

# Check RTL if applicable
appshots translate preview --locale ar

# Check remaining locales
appshots translate preview --locale fr
appshots translate preview --locale es
appshots translate preview --locale pt

# Fix any issues found
appshots translate override-overlay --locale de --overlay-id <id> --font-size 70

# Clear preview when done
appshots translate preview --locale none

# Save with all translations
appshots multi save-design --name "My Screenshots" --override
```

## Per-Locale Export

Export separate screenshot sets per locale:

```bash
for locale in ja ko de fr es pt zh; do
  appshots translate preview --locale $locale
  appshots editor export-all --dir ~/Desktop/screenshots/$locale
done
appshots translate preview --locale none
```

## Remove a Locale

```bash
appshots translate remove-locale --locale ko
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `translate state` | Translation state & locale statuses |
| `translate get-texts` | Get all texts from all designs |
| `translate all --from en --to ja,ko` | AI-translate to targets |
| `translate preview --locale ja` | Preview locale in editor |
| `translate edit` | Edit single translation |
| `translate apply-manual` | Bulk manual translations |
| `translate remove-locale` | Remove all translations for locale |
| `translate set-prompt` | Set AI context prompt |
| `translate override-overlay` | Per-locale style override |
| `translate set-locale-image` | Per-locale screenshot image |
