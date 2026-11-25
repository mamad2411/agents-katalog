---
name: ecma-402-intl
description: >-
  ECMA-402 Internationalization API: format numbers, dates, lists and plurals and compare strings with Intl. Covers ECMA-402 2026, ECMA-402 2025 (supported), ECMA-402 2024 (supported), ECMA-402 draft (track preview). Use when formatting numbers, dates or collation with Intl. Triggers: ECMA-402, Intl.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# ECMA-402 Internationalization API

- 6 Identification of Locales, Currencies, Time Zones, Measurement Units, Numbering Systems, Collations, and Calendars 6.1 Case Sensitivity and Case Mapping

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when formatting numbers, dates or collation with Intl.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: ECMA-402 2026 (default); ECMA-402 2025 (supported); ECMA-402 2024 (supported); ECMA-402 draft (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 2.** "A conforming implementation of this specification must conform to ECMA-262, and must provide and support all the objects, properties, functions, and program semantics described in this specification."
2. **§ 2.** "A conforming implementation is not permitted to add optional arguments to the functions defined in this specification."
3. **§ 4.4.** "Furthermore, dynamic changes to these sets must not result in users becoming distinguishable from each other."
4. **§ 6.1.** "No other case folding equivalences are applied."
5. **§ 6.2.3.** "It must not contain a Unicode locale extension sequence."
6. **§ 6.5.** "Implementations that adopt this specification must be time zone aware: they must use the IANA Time Zone Database https://www.iana.org/time-zones/ to supply available named time zone identifiers and data used in ECMAScript calculations and formatting."
7. **§ 6.5.** "For historical reasons, "UTC" must be a primary time zone identifier."
8. **§ 9.1.** "It must include the value returned by DefaultLocale."
9. **§ 9.2.1.** "If IsWellFormedLanguageTag(tag) is false, throw a RangeError exception."
10. **§ 10.3.3.2.** "String values must be interpreted as UTF-16 code unit sequences as described in ECMA-262, 6.1.4, and a surrogate pair (a code unit in the range 0xD800 to 0xDBFF followed by a code unit in the range 0xDC00 to 0xDFFF) within a string must be interpreted as the corresponding code point."
11. **§ 16.1.3.** "If IsWellFormedCurrencyCode(currency) is false, throw a RangeError exception."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [ECMA-402 2026](https://tc39.es/ecma402/2026/): ECMA-402 edition, ECMA-402 2026 (ECMA-402 edition, 2026), checked 2026-10-06.
- [ECMA-402 2025](https://tc39.es/ecma402/2025/): ECMA-402 edition, ECMA-402 2025 (ECMA-402 edition, 2025), checked 2026-10-06.
- [ECMA-402 2024](https://tc39.es/ecma402/2024/): ECMA-402 edition, ECMA-402 2024 (ECMA-402 edition, 2024), checked 2026-10-06.
- [ECMA-402 draft](https://tc39.es/ecma402/): Editor's draft, tc39.es/ecma402 (Editor's draft, 2026-10-06), checked 2026-10-06.
