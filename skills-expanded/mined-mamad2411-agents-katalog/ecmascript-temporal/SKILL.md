---
name: ecmascript-temporal
description: >-
  ECMAScript Temporal (ES2027, stage 4): write, review and migrate JavaScript
  date and time code with Temporal.Instant, ZonedDateTime, PlainDate, PlainTime,
  PlainDateTime, PlainYearMonth, PlainMonthDay, Duration and Temporal.Now. Use
  when picking a Temporal type, handling IANA time zones and DST
  (disambiguation compatible, earlier, later or reject; offset use, ignore,
  prefer or reject), calendars (iso8601, withCalendar, monthCode), arithmetic
  with add, subtract, until, since, round and total (largestUnit, smallestUnit,
  roundingMode, relativeTo, balancing), parsing and serializing RFC 9557 IXDTF
  strings with [time zone] and [u-ca=] annotations or RFC 3339 timestamps,
  compare versus equals, Intl.DateTimeFormat and toLocaleString, or replacing
  new Date(), Date.parse and getTimezoneOffset. Targets Temporal (ECMAScript
  2027), posture build; upgrades from ECMAScript Date and from Temporal
  pre-reduction polyfill API code that uses Temporal.Calendar,
  Temporal.TimeZone, getISOFields or withPlainDate.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# ECMAScript Temporal

Temporal is the TC39 date and time API for JavaScript: a `Temporal` namespace (like `Math`) with immutable types for exact time, wall-clock time, time zones, calendars and durations. It reached stage 4 in March 2026 and is expected in ECMAScript 2027. With this skill the agent writes new date and time code against Temporal, reviews it, and migrates `Date` and older Temporal polyfill code.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Section numbers (§ 6.3.37) refer to the Temporal spec draft pinned in Sources. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: writing new code, reviewing code, or migrating code (from `Date`, from a date library, or from an older Temporal polyfill).
- Target version: Temporal (ECMAScript 2027) (default, posture build: write against the stage 4 spec; it is not yet merged into the ECMA-262 draft). ECMAScript Date and the Temporal pre-reduction polyfill API are legacy: read them and upgrade from them, never write new code against them. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check `finished-proposals.md` and the ECMA-262 draft for the merge of Temporal, and update the pins.
- Runtime: whether the target engines ship `Temporal` natively or need a polyfill, and which polyfill version.
- Data: what each value means (an exact moment, a wall-clock reading in a known place, a date with no time zone, a recurring month and day), where its time zone comes from, and the string formats exchanged with other systems.

## Invariants

1. **Pick the type from what the value means** (§ 3 to § 10; docs README). `Instant` is an exact time with no time zone or calendar; `ZonedDateTime` is an exact time in a time zone and calendar; the `Plain` types have no time zone. Never store a wall-clock value as an `Instant`, or an exact time as a `PlainDateTime`.
2. **Temporal objects are immutable** (docs README). `with`, `add`, `round` and the other methods return a new object; assign the result.
3. **Compare with `compare()` and `equals()`, never with `<`, `>` or `==`** (§ 3.3.33, § 6.3.44, § 7.3.25). `valueOf()` throws a `TypeError` on every Temporal type.
4. **`compare()` and `equals()` answer different questions** (§ 3.2.3, § 3.3.27, § 6.2.3, § 6.3.40). `ZonedDateTime.compare` uses only the exact time and `PlainDate.compare` only the ISO date; `equals` also requires the same calendar, and for `ZonedDateTime` the same time zone.
5. **Wall-clock to exact time goes through `disambiguation`** (§ 11.1.12, § 13.7). The default is `compatible`: a skipped time moves forward by the gap and a repeated time takes the earlier instant. Use `reject` where a nonexistent or ambiguous local time must be an error.
6. **An offset that conflicts with the time zone is an error when parsing** (§ 6.5.2, § 13.9). `ZonedDateTime.from` defaults `offset` to `reject`; `with` defaults it to `prefer` (§ 6.3.31). Choose `use` or `ignore` deliberately when stored strings may predate a time zone rule change.
7. **Time zones and calendars are string identifiers** (§ 11.1.8, § 12.1, § 14.6.2). Use IANA names (`"Europe/Amsterdam"`, `"UTC"`) or minute-precision offsets (`"+05:30"`); `"iso8601"` is the only calendar every implementation must support. There are no `Temporal.TimeZone` or `Temporal.Calendar` objects.
8. **Calendar units need a reference point** (§ 7.3.20, § 7.3.21, § 7.2.3, § 7.5.41). `Duration.round`, `total` and `compare` need `relativeTo` when years, months or weeks are involved; `Duration.add` and `subtract` throw a `RangeError` for them.
9. **`ZonedDateTime` arithmetic adds the date part in calendar days and the time part in exact time** (§ 6.5.5). One day across a DST change is 23 or 25 hours; `{ hours: 24 }` is always 24 hours.
10. **Differences use defaults per type** (§ 13.43). `largestUnit` defaults to `day` for `PlainDate` and `PlainDateTime`, `hour` for `PlainTime` and `ZonedDateTime`, `second` for `Instant`, `year` for `PlainYearMonth`; `roundingMode` defaults to `trunc`. `ZonedDateTime.until` with a date unit needs both objects in the same time zone, and every difference needs the same calendar (§ 6.5.9).
11. **Strings follow RFC 9557 with Temporal's restrictions** (§ 13.31, § 13.35). A `ZonedDateTime` string needs a bracketed time zone annotation; an `Instant` string needs `Z` or an offset; `Plain` types reject `Z`. An unknown annotation marked critical (`!`) throws a `RangeError`.
12. **`Intl.DateTimeFormat` does not format `ZonedDateTime`** (§ 15.6.22). Use `zonedDateTime.toLocaleString()`, which formats in the object's own time zone (§ 15.11.8.1). A non-ISO calendar on a `Plain` value must match the formatter's calendar (§ 15.6.15 to § 15.6.19).

## Workflow

1. **Pick the version.** Write against the current line unless the runtime only has an older polyfill; then plan the upgrade.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and no legacy API (Temporal.Calendar, Temporal.TimeZone, `getISOFields`, `withPlainDate`, `epochSeconds`) is in new code.
2. **Model each value with one type.** Map every date and time field in the data to a Temporal type and record where its time zone and calendar come from.
   -> [`references/types.md`](references/types.md)
   ✓ Every value has a type, exact times carry a time zone only when local wall-clock behaviour matters, and `Temporal.Now` calls name the time zone on servers.
3. **Handle time zones, DST and calendars.** Choose `disambiguation` and `offset` for each conversion, and validate external calendar input.
   -> [`references/time-zones-and-calendars.md`](references/time-zones-and-calendars.md)
   ✓ Every wall-clock to exact-time conversion has a chosen `disambiguation`, every parse of a stored `ZonedDateTime` string has a chosen `offset`, and calendars are compared or converted explicitly.
4. **Write the arithmetic.** Use `add`, `subtract`, `until`, `since`, `round` and `total` with explicit units.
   -> [`references/arithmetic-and-rounding.md`](references/arithmetic-and-rounding.md)
   ✓ Every difference sets `largestUnit` (and `smallestUnit` and `roundingMode` when rounding), and every duration with calendar units is rounded or totalled with `relativeTo`.
5. **Parse, serialize and format.** Exchange RFC 9557 or RFC 3339 strings; format for people with `toLocaleString` or `Intl.DateTimeFormat`.
   -> [`references/parsing-and-migration.md`](references/parsing-and-migration.md)
   ✓ Round-trips through `toString()` and `from()` return an equal value, and no code parses localized strings.
6. **Upgrade** (only when asked). Replace `Date` code, or polyfill-era Temporal code, following the upgrade steps for the source line.
   -> [`references/versions.md`](references/versions.md), [`references/parsing-and-migration.md`](references/parsing-and-migration.md)
   ✓ The upgraded code produces the same exact times and wall-clock values as before on the test cases, including a DST gap and a DST overlap.

## Verify before done

- [ ] No Temporal value is compared with `<`, `>`, `==` or `===`, sorted without `compare`, or used where a number is expected.
- [ ] Every `PlainDateTime.toZonedDateTime`, `ZonedDateTime.from` and `with` call that can hit a DST transition has a deliberate `disambiguation`, and `from` on stored strings a deliberate `offset`.
- [ ] Every `Duration.round`, `total` or `compare` over years, months or weeks passes `relativeTo`.
- [ ] Every difference sets `largestUnit` when the default for its type is not what the caller wants.
- [ ] Strings parsed into `Plain` types have no `Z`; `ZonedDateTime` strings carry a `[time zone]` annotation.
- [ ] `ZonedDateTime` values are formatted with `toLocaleString`, not passed to `Intl.DateTimeFormat.prototype.format`.
- [ ] No removed pre-2024 API is used; `calendarId` and `timeZoneId` are read instead of `calendar` and `timeZone` objects.
- [ ] Conversions to `Date` go through `epochMilliseconds` and note the loss of sub-millisecond precision.

## Reference index

- **`references/versions.md`**: the three version lines with status, which to use, what changed, and upgrade steps from `Date` and from pre-reduction polyfills. Load for steps 1 and 6.
- **`references/types.md`**: each type, its fields and conversions, `Temporal.Now`, constructors versus `from`, and comparison. Load for step 2.
- **`references/time-zones-and-calendars.md`**: time zone identifiers, DST `disambiguation` and `offset` options, transitions, calendars and month codes. Load for step 3.
- **`references/arithmetic-and-rounding.md`**: `add`, `subtract`, `until`, `since`, `round`, `total`, units, rounding modes, balancing and duration limits. Load for step 4.
- **`references/parsing-and-migration.md`**: RFC 9557 and RFC 3339 strings, `toString` options, `Intl.DateTimeFormat`, and `Date` migration recipes. Load for steps 5 and 6.

## Related skills

For localized messages that embed formatted dates and times, use the `messageformat` skill: `npx skills add ScaleDockHQ/scaledock-skills --skill messageformat`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Temporal proposal specification](https://tc39.es/proposal-temporal/): Stage 4 Draft, July 27, 2026, checked 2026-10-05.
- [Temporal documentation](https://tc39.es/proposal-temporal/docs/): proposal documentation and cookbook, main branch at commit e8cc03f (2026-07-27), checked 2026-10-05.
- [Temporal cookbook](https://tc39.es/proposal-temporal/docs/cookbook.html): proposal documentation, main branch at commit e8cc03f (2026-07-27), checked 2026-10-05.
- [tc39/proposal-temporal](https://github.com/tc39/proposal-temporal): Stage 4, README at commit e8cc03f (2026-07-27), checked 2026-10-05.
- [TC39 finished proposals](https://github.com/tc39/proposals/blob/main/finished-proposals.md): Temporal finished, expected publication year 2027, commit ee92ecf (2026-09-29), checked 2026-10-05.
- [ECMA-262 draft](https://tc39.es/ecma262/): Draft ECMAScript 2027, October 3, 2026, does not yet contain Temporal, checked 2026-10-05.
- [ECMAScript 2026 Language Specification](https://tc39.es/ecma262/2026/): ECMAScript 2026, 17th edition, used for the Date line, checked 2026-10-05.
- [ecma262 pull request #3966: Temporal stage 4, round 2](https://github.com/tc39/ecma262/pull/3966): open, updated 2026-09-24, checked 2026-10-05.
- [Temporal proposal polyfill changelog](https://raw.githubusercontent.com/tc39/proposal-temporal/main/polyfill/CHANGELOG.md): changelog up to 0.9.0, main branch at commit e8cc03f, checked 2026-10-05.
- [@js-temporal/polyfill changelog](https://raw.githubusercontent.com/js-temporal/temporal-polyfill/main/CHANGELOG.md): changelog, 0.5.0 (TC39 changes from May 2023 to March 2025), checked 2026-10-05.
- [TC39 meeting notes, 12 June 2024](https://github.com/tc39/notes/blob/HEAD/meetings/2024-06/june-12.md): Temporal stage 3 update and scope reduction, checked 2026-10-05.
- [RFC 9557: Date and Time on the Internet: Timestamps with Additional Information](https://www.rfc-editor.org/rfc/rfc9557): Proposed Standard, April 2024, checked 2026-10-05.
- [RFC 3339: Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/rfc/rfc3339): Proposed Standard, July 2002, updated by RFC 9557, checked 2026-10-05.
