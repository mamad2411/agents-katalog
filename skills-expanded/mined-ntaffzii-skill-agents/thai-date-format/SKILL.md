---
name: thai-date-format
description: Use this skill for any task converting between Buddhist Era (พ.ศ.) and Common Era (ค.ศ.) years, or formatting a date the way a Thai document, business, or casual context expects. Trigger on "แปลงปี พ.ศ.", "แปลง ค.ศ.", "วันที่แบบไทย", "วันที่ราชการ", "เลขไทย", "Thai date", "BE to CE", "Buddhist Era", or any date that mixes a 4-digit year starting with 25xx with a request to write or read it in Thai. If the task is just generic date-string formatting with no Thai era or numeral involved, plain ISO/locale formatting is enough — this skill is not needed.
---

# Thai Date Format (พ.ศ. ↔ ค.ศ.)

## Overview

Thai documents, forms, and casual writing use the Buddhist Era (พุทธศักราช, พ.ศ. = ค.ศ. + 543), not the Common Era Claude defaults to. A model without this skill routinely writes `2025` in a Thai government letter (should be `๒๕๖๘` or `2568`), or converts a Thai year by guessing instead of the fixed +543 offset. This skill gives the exact offset, the three common display styles, and Thai numeral rendering.

## When to use

- แปลงปี 2568 (พ.ศ.) เป็น ค.ศ., or the reverse
- เขียนวันที่แบบราชการ / business / casual ในเอกสารไทย
- Formatting a date for a Thai form, invoice, resume, or letter (often needed together with `thai-invoice` or `thai-government-form`)
- Rendering a number using Thai digit glyphs (๐-๙), e.g. for a formal document or engraving
- Parsing a Thai-formatted date string back into a usable date value

## When NOT to use

- The task is pure English/ISO date handling with no Thai era or numeral involved
- The task needs Thai lunar/astrological calendar dates (Thai solar calendar with BE offset is a different system from the lunar calendar used for Buddhist holy days) — flag this distinction to the user rather than guessing a lunar date

## Core knowledge

- **Offset**: `BE = CE + 543`. Example: 2025 CE = 2568 BE. This is a fixed arithmetic offset for the modern calendar.
- **Historical caveat**: Thailand moved New Year's Day from 1 April to 1 January starting BE 2484 (1 Jan 1941 CE). For any date **on or after 1 Jan 1941**, the fixed `+543` offset holds for the whole year. For dates before that, Jan-Mar fell in the *previous* BE year under the old calendar — this skill does not model that historical edge case; flag it if a user asks about a pre-1941 date.
- **Display styles**:

  | Style | Example | Where used |
  |---|---|---|
  | Formal (ราชการ) | `16 พฤษภาคม 2568` | Government letters, official documents, formal invitations |
  | Business | `16 พ.ค. 68` | Invoices, receipts, business correspondence |
  | Casual | `16/5/68` | Chat, informal notes, UI date pickers |
  | ISO/CE | `2025-05-16` | Machine interchange, APIs, databases — never show this to a Thai reader as "the date" without conversion |

- **Thai numerals (๐๑๒๓๔๕๖๗๘๙)**: optional glyph set, mostly used in royal/ceremonial documents, some government forms, and stylized design. **Default to Arabic numerals (0-9)** even in Thai-language text — that is the actual norm in everyday Thai documents; only switch to Thai digits when the user asks or the context is clearly ceremonial/formal government.
- **Month names**: use the full form (มกราคม, กุมภาพันธ์, ...) for formal style, abbreviated form (ม.ค., ก.พ., ...) for business style — see `convert.py:THAI_MONTHS_FULL` / `THAI_MONTHS_ABBR` for the full list.

## Common mistakes

1. Writing the CE year in a Thai formal document instead of converting to BE.
2. Getting the offset backwards (subtracting 543 from a CE year instead of adding).
3. Defaulting to Thai numeral glyphs everywhere — most real Thai documents use Arabic digits.
4. Truncating the BE year to 2 digits without checking the style calls for it (formal style always uses the full 4-digit BE year).
5. Confusing the Buddhist Era solar calendar (fixed +543 offset, same months as CE) with the Thai lunar calendar used for religious holidays — they are not interchangeable.
6. Applying the +543 offset to a pre-1941 date without accounting for the old April New Year.

## Code

`convert.py` — no dependencies, pure stdlib:

- `ce_to_be(ce_year)` / `be_to_ce(be_year)` — year offset conversion
- `to_thai_digits(value)` / `from_thai_digits(text)` — Arabic ↔ Thai numeral glyphs
- `ThaiDate.from_date(date).format(style="formal"|"business"|"casual"|"iso_ce", numerals="arabic"|"thai")`
- `format_date(date, style=..., numerals=...)` — convenience wrapper

Run `python3 convert.py` for the self-test.

## Known limitations

- Does not model the pre-1941 Thai New Year date shift (see Core knowledge above).
- Does not handle the Thai lunar calendar (religious holiday dates like Songkran-adjacent lunar observances need a separate lunar-calendar lookup, not this offset).
- Checked against the standard `CE + 543` Buddhist Era rule, which is stable and not subject to legislative change — no re-verification cadence needed for the offset itself, but month-name spelling conventions should be spot-checked against a current Royal Institute Dictionary source if used in a legal document.
