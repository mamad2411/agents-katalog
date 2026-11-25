---
name: hci-rtl-localization
description: Designs and fixes right-to-left and multilingual user interfaces for Persian, Arabic, Hebrew and Urdu. Use whenever the user builds or reviews a UI that must support RTL or mixes languages, sees layouts break when switching direction, wonders what to mirror, how to handle bidirectional text, Persian or Western digits, Jalali dates, fonts and line height, or logical CSS properties, even if they only say "my app looks wrong in Persian". Scans code for physical left and right layout, suggests logical equivalents, and gives a testing checklist.
---

# hci-rtl-localization

Make an interface feel native to right-to-left readers, not just mirrored. Covers layout, bidirectional text, numbers, dates, fonts, forms, platform APIs and testing.

```
hci-rtl-localization/
├── SKILL.md
├── scripts/
│   └── check_rtl_css.py          finds physical left and right layout, RTL traps; optional safe renames
└── references/
    └── rtl-guide.md              what to mirror, logical properties, bidi, numbers, typography, platforms, tests
```

## When to use

- Adding Persian, Arabic, Hebrew or Urdu support to an existing app or site
- A layout, icon, animation or gesture looks wrong in RTL
- Mixed Persian and English text shows punctuation or numbers in the wrong place
- Choosing fonts, line height, digits, date formats or sorting for an RTL audience
- Reviewing a design or code for localization readiness

## Workflow

1. **Find the languages and platform**: which RTL languages, web or mobile framework, and whether English or other LTR content appears inside RTL text.
2. **Scan the code**: `python3 scripts/check_rtl_css.py src/`. For web code it reports physical margins, paddings, borders, offsets, text alignment and floats with the logical replacement, plus traps like letter-spacing, uppercase, italics, horizontal translation and an `<html lang="fa">` without `dir`. For mobile use the platform notes in the guide.
3. **Apply safe renames**: `python3 scripts/check_rtl_css.py src/ --write-fixed` writes `*.logical.css` copies with exact logical equivalents (margin, padding, border, text-align, float). Review the diff before replacing files. Offsets such as `left: 50%` with `translateX` are left alone on purpose.
4. **Decide what to mirror** using the table in the guide: flow and direction icons yes; logos, check marks, media controls, photos no.
5. **Handle bidirectional text**: `dir` and `lang` on the root, `dir="auto"` or `<bdi>` for user content, LTR islands for codes, URLs and phone numbers, full-sentence messages instead of concatenation.
6. **Set numbers, dates and type**: choose Persian or Western digits per context and accept both on input, use `Intl` formatters, offer the Jalali calendar where relevant, use a font with full Persian support and a line height of about 1.6 to 1.9 (`persian-text-processing` and `persian-dates` cover the details).
7. **Test in RTL** with the checklist: forced RTL mode, mixed strings, long text, 200 percent text size, screen reader order, and review by a native reader. A scan cannot see rendered results, so say what you could not verify.

## Rules

- Prefer logical properties and start and end APIs over left and right, so one stylesheet serves both directions
- Mirror direction, not meaning: do not mirror logos, check marks, clocks or media controls
- Never concatenate translated fragments, and never put text inside images
- Keep codes, numbers and URLs left-to-right in their own elements
- Do not use letter-spacing, uppercase or italics on Persian or Arabic text
- Accept both digit styles and both Arabic and Persian letter forms on input, and normalize before validating or searching
- Do not guess translations; ask for approved strings and a native reviewer

## What to report back

| Field | Content |
|-------|---------|
| Scope | languages, platform, files scanned |
| Findings | rule, location, replacement |
| Design decisions | what is mirrored and what is not, digits, calendar, font |
| Not verified | rendered layout, gestures, screen reader order |
| Test plan | the RTL checklist items to run |

## Related skills

- `persian-text-processing`: normalize letters, digits and half spaces
- `persian-dates`: Jalali calendar logic
- `hci-react-native`, `hci-flutter`, `hci-android-native`, `hci-ios-swiftui`, `hci-web-accessibility`: platform specifics
- `document-conversion`: right-to-left documents and PDFs
