---
name: arabic-rtl
description: Build, review, and fix interfaces for Arabic and other right-to-left languages correctly. Use whenever code, UI, copy, or data will be shown to Arabic (or Hebrew, Persian, Urdu) users — layouts and styling in Flutter, web/CSS/Tailwind, React Native, Android/Compose, or iOS/SwiftUI; translating or writing Arabic UI text; formatting numbers, dates, or currency for Arab locales; handling phone/email inputs and mixed Arabic/English text; or implementing Arabic search. Also use when reviewing an existing app for RTL bugs.
---

# Arabic & RTL

RTL support is not "flip the screen". Most bugs come from physical directions (`left`/`right`) hardcoded in code, text treated as if Arabic were English with different letters, and numbers/dates formatted without a locale. Apply the rules below by default whenever the target audience reads Arabic, even if the user did not mention RTL.

## Core rules

1. **Never use physical directions for layout.** Use `start`/`end` (logical) everywhere: padding, margin, alignment, positioning, borders, radius, text alignment. Physical `left`/`right` only for things that must not mirror (see rule 3).
2. **Set direction once, at the root**, from the locale: `<html lang="ar" dir="rtl">`, Flutter `MaterialApp` with Arabic localization delegates, `android:supportsRtl="true"`. Do not sprinkle manual direction overrides through the tree.
3. **Mirror what expresses direction, keep what doesn't.**
   - Mirror: back/forward arrows, chevrons, send/reply icons, list bullets, progress bars, sliders, steppers, carousels/pagers, swipe gestures, slide-in animations, drawers/side sheets, text-with-icon order.
   - Do not mirror: logos, media playback controls (play, fast-forward), clocks, checkmarks, numbers, phone numbers, code, maps, photos, icons depicting real objects (camera, search magnifier, headphones).
4. **Isolate LTR content inside Arabic text.** Phone numbers, emails, URLs, usernames, code, and Latin product names must be wrapped in a direction isolate, otherwise punctuation and digits jump around. Inputs for phone, email, URL, passwords, and OTP codes are always LTR. User-generated content uses automatic direction detection (`dir="auto"`).
5. **Typography for Arabic script:**
   - Use a font with real Arabic glyphs (e.g. IBM Plex Sans Arabic, Noto Sans/Kufi Arabic, Cairo, Tajawal, Almarai, Readex Pro). Never rely on the system fallback.
   - Line height ≥ 1.5 (1.6–1.8 for body text); Arabic has tall ascenders and deep descenders that clip in tight boxes.
   - `letter-spacing: 0` always — tracking breaks letter connections.
   - No italics (synthetic slant looks broken) and no uppercase transforms (Arabic has no case). Emphasize with weight or color.
   - Do not truncate fixed-width text boxes sized for English; let them grow or use start-aligned ellipsis.
6. **Numbers, dates, and currency go through the locale formatter**, never string concatenation. Decide Western digits (0–9) vs Arabic-Indic (٠–٩) per product and apply it consistently — the Maghreb (Libya, Tunisia, Algeria, Morocco) uses Western digits; Egypt, the Levant, Iraq, and the Gulf often use Arabic-Indic. **Always normalize digits in user input to ASCII before validating or parsing** — users type ٠١٢٣ and validation silently fails.
7. **Currency decimals vary:** LYD, KWD, BHD, OMR, JOD, and TND have 3 decimal places; IQD is shown with none. Never hardcode 2 — let the currency formatter decide.
8. **Arabic has six plural forms** (zero, one, two, few, many, other). Never write `count == 1 ? singular : plural`. Use ICU plural messages.
9. **Never build sentences by concatenation.** Word order, gender, and agreement differ. Use full message strings with placeholders.
10. **Write, don't translate.** Arabic UI copy should read like it was written in Arabic: Modern Standard Arabic unless the brand uses dialect, gender-neutral phrasing (prefer verbal nouns like «تسجيل الدخول» over gendered imperatives like «سجّل دخولك»), Arabic punctuation (، ؛ ؟).
11. **Search must normalize Arabic** (hamza forms of alef, ta marbuta/ha, alef maqsura/ya, diacritics, tatweel, digits) on both the index and the query, or users won't find what they typed.

## Platform references

Read the reference that matches the code you are touching before writing or reviewing it:

- Flutter → [references/flutter.md](references/flutter.md)
- Web: HTML, CSS, Tailwind, React → [references/web.md](references/web.md)
- React Native, Android (Views/Compose), iOS (UIKit/SwiftUI) → [references/native.md](references/native.md)
- Writing or translating Arabic UI text, plurals, glossary → [references/copy.md](references/copy.md)
- Numbers, digits, currency, dates, calendars → [references/numbers-dates.md](references/numbers-dates.md)
- Arabic search and text normalization → [references/search.md](references/search.md)

## Review checklist

When asked to review or audit for RTL/Arabic, check each item and report the file and line of every violation:

- [ ] No physical `left`/`right` in layout code (padding, margin, position, alignment, border, radius, text-align) except for intentionally unmirrored elements.
- [ ] Root direction and locale set from the user's language; Arabic font configured.
- [ ] Directional icons mirror; non-directional icons and media controls don't.
- [ ] Horizontal animations, gestures, drag deltas, and `translateX`/`Offset` values account for direction.
- [ ] Phone/email/URL/OTP/password inputs are LTR; mixed-direction strings are isolated.
- [ ] No letter-spacing, italics, or uppercase on Arabic text; line height is sufficient; nothing clips.
- [ ] Numbers, dates, and currency use locale formatters; digit system is consistent; input digits are normalized before validation.
- [ ] Plurals use ICU plural rules with all Arabic forms; no string concatenation for sentences.
- [ ] Arabic copy is natural, gender-neutral where possible, and uses Arabic punctuation.
- [ ] Search normalizes Arabic text on both sides.
- [ ] The app was actually run in Arabic: drawers open from the right, back arrows point right, lists and pagers scroll in the right direction, progress fills from the right.
