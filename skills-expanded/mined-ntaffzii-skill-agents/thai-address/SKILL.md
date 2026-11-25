---
name: thai-address
description: Use this skill for any task parsing a Thai address into its components (ตำบล/แขวง, อำเภอ/เขต, จังหวัด, รหัสไปรษณีย์) or looking up a province from a postal code or name. Trigger on "แยกที่อยู่", "ที่อยู่ไทย", "รหัสไปรษณีย์", "จังหวัดอะไร", "Thai address parse", "postal code to province". If the address is already cleanly split into labeled fields (e.g. a form with separate province/district inputs), this skill's lookup table is still useful but the parsing half is unnecessary.
---

# Thai Address Parsing

## Overview

Thai addresses order components district-to-city the same broad direction as English (house number → subdistrict → district → province → postal code) but use Thai particle words (ตำบล/แขวง, อำเภอ/เขต, จังหวัด) that a naive English-address parser (split on commas, assume last token is a country) will mishandle — Bangkok uses แขวง/เขต instead of ตำบล/อำเภอ, and the parts can appear with or without abbreviations (ต./อ./จ.). This skill gives a regex-based extractor plus the 77-province reference table.

## When to use

- แยกที่อยู่ไทยเป็นส่วนประกอบ (ตำบล, อำเภอ, จังหวัด, รหัสไปรษณีย์)
- หารหัสไปรษณีย์ 2 หลักแรก → จังหวัด (candidate lookup, not exact 5-digit resolution)
- Matching a province name across Thai/English spelling and with/without "จังหวัด"/"Province" wrapper
- Validating that a claimed province name is one of the real 77

## When NOT to use

- The task needs the exact 5-digit postal code for a specific subdistrict — this skill narrows to province-level candidates from the first 2 digits only; direct the user to Thailand Post's official lookup for the precise code
- The address is non-Thai — use general address parsing instead

## Core knowledge

- Thailand has **77 provinces** (76 + Bangkok). Bangkok uses แขวง (subdistrict) / เขต (district) terminology; every other province uses ตำบล / อำเภอ.
- Postal codes are 5 digits. The **first 2 digits identify a province-level zone** in a well-documented sequential assignment (10 = Bangkok area, 20s = eastern seaboard, 30s-40s = northeast, 50s = north, 60s = lower-north/central, 70s = west, 80s-90s = south). The last 3 digits identify the specific post office/district — this skill does not resolve that level.
- Bangkok and Samut Prakan share the `10` prefix; several other neighboring provinces' outlying districts can carry a prefix that "belongs" to an adjacent province's normal range. Treat a prefix match as a **candidate list**, not a certainty.
- Standard field order in a full Thai address: `[เลขที่/บ้านเลขที่] [หมู่ที่] [ถนน] ตำบล/แขวง[X] อำเภอ/เขต[Y] จังหวัด[Z] [รหัสไปรษณีย์]`.

## Common mistakes

1. Assuming ตำบล/อำเภอ apply to Bangkok addresses — Bangkok uses แขวง/เขต instead.
2. Treating the first 2 postal-code digits as uniquely identifying one province — several pairs (notably Bangkok/Samut Prakan) share a prefix.
3. Matching province names with exact string equality only — fails on "จ.เชียงใหม่", "จังหวัดเชียงใหม่", "Chiang Mai Province", and plain "เชียงใหม่" all referring to the same province.
4. Assuming a mostly-empty parse result means "no address" — it more often means the input didn't use the expected Thai particle words (see Known limitations).
5. Fabricating a precise 5-digit postal code from a province name alone — the province-level prefix does not determine the last 3 digits.

## Code

`parse.py` (uses `provinces.json`, no external dependencies):

- `load_provinces()` → list of `{name_th, name_en, region, postal_prefix}`
- `find_province(name)` → tolerant Thai/English match, handles "จังหวัด"/"จ."/"Province" wrapping
- `postal_prefix_to_provinces(code)` → candidate province list from the first 2 digits
- `parse_thai_address(text)` → `{postal_code, province, district, subdistrict}`

Run `python3 parse.py` for the self-test.

## Known limitations

- `parse_thai_address` is a **structural regex extractor**, not a trained address-parsing model. It requires the Thai particle words (ตำบล/แขวง/อำเภอ/เขต/จังหวัด or their abbreviations) to be present in the text; a plain comma-separated address without those words will parse mostly empty.
- `postal_prefix_to_provinces` resolves to a province-level candidate list from 2 digits only — it cannot give the exact 5-digit code for a specific subdistrict, and a handful of border-area districts use a prefix outside their "home" province's normal range. Verify the exact code against Thailand Post's official lookup before printing it on a real document.
- Province English-name romanization follows one common convention (RTGS-influenced with spaces, e.g. "Buri Ram"); other sources spell some names differently (e.g. "Buriram" one word) — treat spelling variants as equivalent when matching, not as errors.
- `provinces.json`'s `region` field uses one common 6-region grouping; other classifications (e.g. Royal Institute's 4-region scheme) group some Central provinces as "Lower North" instead — don't treat `region` as an official government classification.
