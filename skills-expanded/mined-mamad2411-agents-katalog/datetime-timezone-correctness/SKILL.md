---
name: datetime-timezone-correctness
description: Implements and fixes correct date/time handling — UTC/instant storage, IANA timezone and DST conversion (gaps and overlaps), explicit ISO-8601 parsing/formatting, calendar-vs-elapsed duration math, DST-stable RRULE recurrence, and monotonic-vs-wall-clock duration measurement.
when_to_use: Code stores, parses, compares, adds to, or displays timestamps; or a bug is off-by-an-hour/day, a DST transition, a date-boundary or leap-day error, an ambiguous/nonexistent local time, recurrence/expiry, or wall-clock vs monotonic duration. Distinct from regex-build (validating a date *string's* shape) and message-queue-jobs (scheduling/firing the job, not computing its time).
---

## When to Use

Reach for this skill when the bug or task is about **what a timestamp means**, not how it looks on screen:

- "Reminder fires an hour early/late twice a year" / "off by one hour after the clock change"
- "Event lands on the wrong day for users in another timezone"
- "Token/trial expires a day early" or "expiry compares a naive datetime to an aware one"
- "Picking `datetime.now()` vs `utcnow()`, naive vs aware, or `Date` vs Temporal/Luxon/java.time/chrono"
- "Recurring 9am meeting drifts to 8am / 10am" (DST-unstable RRULE)
- "Elapsed-time metric goes negative or huge" (used wall clock, NTP stepped it)
- "Parsing `01/02/2026` flips day and month" / "`+0000` got dropped on parse"
- Leap-day / leap-second / Feb-29 arithmetic, "add 1 month to Jan 31"

NOT this skill:
- Validating that a *string* matches a date format (regex, positive/negative cases) → regex-build
- Scheduling, enqueuing, retrying, or actually *firing* a job at a time → message-queue-jobs
- Adding type hints so `Aware` vs `Naive` is a compile-time error → type-safety-strict
- Column-level checks that a dataset's date field is non-null/in-range → validate-data-quality
- A concurrency race where two threads read a clock out of order → async-concurrency-correctness

## Steps

1. **Cardinal rule: store and transport an absolute instant; convert to local only at the display edge.** Persist UTC or an offset-bearing instant. Local wall-clock time is for input and output only — never the source of truth.

   | Concept stored | Right type | Wrong type | Example |
   |---|---|---|---|
   | A moment that happened/will happen | UTC instant / `timestamptz` / `Instant` | naive local datetime, "string + separate tz column" | log entry, `created_at`, fired-at |
   | A wall-clock appointment a human set | local datetime **+ IANA zone id** (e.g. `America/New_York`) | UTC instant alone (loses the user's intent across DST law changes) | "9:00am every Mon", future calendar event |
   | A pure date with no time | date-only type (`LocalDate`) | midnight-UTC instant (shifts a day under any offset) | birthday, invoice due date, holiday |
   | Elapsed time / a timeout | monotonic duration (see step 7) | difference of two wall-clock timestamps | request latency, cache TTL countdown |

   Store the **zone id** (`Europe/London`), never a fixed offset (`+01:00`) or abbreviation (`BST`/`CST` — ambiguous, and offset changes at DST). Schema default: `TIMESTAMPTZ` in Postgres, never `TIMESTAMP` (Postgres `timestamp` is naive and silently drops the zone).

2. **Audit naive vs aware; forbid the silent-local default.** Grep the hotspots and replace every implicit-local call:

   | Language | Banned (naive / implicit-local) | Use instead |
   |---|---|---|
   | Python | `datetime.now()`, `datetime.utcnow()`, `datetime.fromtimestamp(ts)`, `datetime.strptime(...)` (naive) | `datetime.now(timezone.utc)`, `datetime.fromtimestamp(ts, tz=ZoneInfo("UTC"))`, attach `ZoneInfo` |
   | JS/TS | `new Date("2026-01-02")`, `Date.parse`, `new Date(y,m,d)`, `getHours()`/`setHours()` | Temporal (`Temporal.ZonedDateTime`, `Instant`) or Luxon `DateTime.fromISO(s,{zone})` |
   | Java | `new Date()`, `Calendar`, `SimpleDateFormat`, `LocalDateTime` for an instant | `Instant`, `ZonedDateTime`, `OffsetDateTime`, `DateTimeFormatter`, `java.time` |
   | Rust | `chrono::Local::now`, `NaiveDateTime` as an instant | `Utc::now()`, `DateTime<Utc>`, `chrono-tz` `Tz` |
   | Go | `time.Parse` without a layout offset | `time.Now().UTC()`, `time.LoadLocation`, RFC3339 layout |

   `utcnow()` is banned because it returns a **naive** datetime tagged nothing — comparing it to an aware one raises `TypeError`, comparing it to another naive one silently treats both as local. A timestamp is correct only when its type carries a zone.

3. **Convert through a real IANA tzdb, and resolve DST gaps and overlaps explicitly — never let the library pick silently.** Use the OS/`tzdata` IANA database (Python `zoneinfo`, JS Temporal/Luxon, Java `java.time`, Rust `chrono-tz`, Go `time/tzdata`). Two wall-clock times per year are not 1:1 with instants:

   - **Spring-forward GAP** — `2026-03-08 02:30 America/New_York` does not exist. Decide: shift forward to `03:30` (calendar apps), or reject. Never let it round to a random instant.
   - **Fall-back OVERLAP** — `2026-11-01 01:30 America/New_York` occurs twice. Decide which: earlier (`fold=0`, first occurrence, larger offset) or later (`fold=1`).

   ```python
   from datetime import datetime, timezone
   from zoneinfo import ZoneInfo
   ny = ZoneInfo("America/New_York")

   wall = datetime(2026, 3, 8, 2, 30, tzinfo=ny)   # gap — does NOT exist
   inst = wall.astimezone(timezone.utc)            # zoneinfo skips ahead silently
   back = inst.astimezone(ny)                       # -> 03:30, NOT 02:30  => round-trip changed it
   assert back != wall                              # detect: round-trip mismatch == gap/overlap hit

   amb = datetime(2026, 11, 1, 1, 30, tzinfo=ny)            # overlap, two instants
   first  = amb.replace(fold=0).astimezone(timezone.utc)    # 05:30Z (EDT)
   second = amb.replace(fold=1).astimezone(timezone.utc)    # 06:30Z (EST)
   assert first != second                                    # 1h apart — pick fold deliberately
   ```
   Detection rule that works in any language: convert local→instant→local; if you don't get the original wall time back, you hit a gap or overlap — handle it, don't ship it.

4. **Parse and format with an explicit format string and explicit offset handling; reject locale/heuristic parsers.** Default wire format is **RFC 3339 / ISO-8601 with offset**: `2026-06-15T13:45:30Z` or `...+07:00`. Rules:
   - Parse with a fixed pattern (`strptime`/`DateTimeFormatter.ofPattern`/explicit layout), never a "smart" parser (`Date.parse`, `dateutil.parser.parse` for machine data — they guess `MM/DD` vs `DD/MM` by locale and flip silently).
   - A timestamp string **without** an offset is incomplete: either require one, or attach a documented zone — never assume the server's local zone.
   - When emitting for machines, always include the offset (`Z` for UTC). For humans, format in their zone with the zone name shown.
   - Date-only fields parse to a date type, not midnight in some zone.

5. **Duration & arithmetic: separate elapsed (fixed) from calendar (variable), and pin the order of operations.**
   - **Elapsed / exact:** add seconds/`Duration`/`timedelta` to an **instant**. `now + 24h` is exactly 86400s and may land on a different wall-clock hour across DST — that is correct for "24 hours from now."
   - **Calendar:** "tomorrow", "+1 day", "+1 month" are zoned wall-clock ops — do them on a `ZonedDateTime`/`LocalDate`, then convert. "+1 day" across spring-forward is 23h of real time, and that is correct for "same time tomorrow."
   - **Month/year overflow:** "Jan 31 + 1 month" must clamp to Feb 28/29, not roll to Mar 3. Use a library that clamps (`java.time` `plusMonths`, Luxon `plus({months:1})`, `dateutil.relativedelta`) — never naïve day-count math.
   - **Day boundaries** ("events on 2026-06-15") are `[startOfDay, startOfDay+1d)` **in the user's zone** converted to instants, then a half-open `>= lo AND < hi` range — never `date(timestamp)` in SQL (that truncates in the server's zone). Always half-open, never `BETWEEN`: its closed upper bound double-counts the next midnight.
   - **Business days / "3 working days":** iterate calendar days in the relevant zone, skip weekends + a holiday set; don't approximate as `+72h`.

6. **Recurrence (RRULE / iCal RFC 5545): expand against the zone, not against fixed offsets, so a recurring local time stays put across DST.** Store the rule with `DTSTART;TZID=America/New_York:20260105T090000` + `RRULE:FREQ=WEEKLY;BYDAY=MO`. Expand each occurrence as a **wall-clock time in that zone**, then convert each to an instant individually — so "every Monday 9:00am" is always 9am local even though its UTC offset shifts at DST. Handle `EXDATE` exclusions and `UNTIL` (which is in UTC per spec). If an occurrence lands in a spring-forward gap, apply the same gap policy as step 3 (shift forward). Never precompute occurrences as fixed-offset UTC instants — they drift an hour after the next DST change.

7. **Clock source: monotonic for elapsed, wall clock for timestamps; assume the wall clock jumps.**

   | Need | Use | Never |
   |---|---|---|
   | Duration / latency / timeout / "has 30s passed" | monotonic clock — `time.monotonic()`, `performance.now()`, `System.nanoTime()`, `Instant::now()` | subtracting two wall-clock timestamps (NTP/leap/DST can step it → negative or huge) |
   | "When did this happen" / persisted time / display | wall clock — `time.time()`/UTC instant | monotonic (meaningless across processes/reboots) |

   Wall clock is not monotonic: NTP slews/steps it, users change it, VMs pause. A duration measured by wall clock can go **negative**. Measure every interval, retry/backoff window, and benchmark with the monotonic source. For leap seconds, prefer a smeared-time NTP source over special-casing `:60`.

8. **Test across the boundaries that break naive code, and migrate off deprecated APIs.** Freeze the clock (`freezegun`, `@sinonjs/fake-timers`, `Clock.fixed`) and parametrize the zone (run the suite under `TZ=UTC` *and* `TZ=America/New_York` *and* `TZ=Pacific/Kiritimati` UTC+14). Cover: spring-forward gap, fall-back overlap, Dec 31 → Jan 1 rollover in a non-UTC zone, Feb 29 leap day, Jan 31 + 1 month, an RRULE crossing a DST date, and a monotonic-vs-wall duration during a simulated clock step. Replace any `SimpleDateFormat`/`utcnow`/`new Date(string)`/`chrono::Local` found in step 2.

## Common Errors

- **`datetime.utcnow()`** — returns naive; downstream it's treated as local and shifts by the server offset. Fix: `datetime.now(timezone.utc)`.
- **`new Date("2026-06-15")`** — JS parses a date-only ISO string as **UTC midnight**, so it prints as the *previous day* west of UTC. Fix: parse with Temporal/Luxon and an explicit zone, or treat as a date type.
- **Storing offset `+01:00` instead of zone id `Europe/London`** — the offset is wrong the other half of the year and can't survive a tzdb law change. Fix: store the IANA id; derive the offset at conversion time.
- **Postgres `TIMESTAMP` (without `TZ`) for an instant** — drops the zone; reads back in the session's `TimeZone`. Fix: `TIMESTAMPTZ`.
- **Comparing naive to aware** — Python raises `TypeError`; some languages compare them as both-local and lie. Fix: normalize both to aware-UTC before comparing.
- **`date_trunc`/`CAST(ts AS date)` for "which day"** — truncates in the server zone, so a 23:30-local event lands on the wrong date. Fix: convert to the user zone first (`ts AT TIME ZONE 'America/New_York'`), then truncate.
- **`+ timedelta(days=1)` expecting "same wall time tomorrow"** — adds exactly 24h; off by an hour across DST. Fix: do the `+1 day` on a zoned/local value, then convert to instant.
- **Jan 31 + 1 month = Mar 3** — naive 30/31-day math overflows February. Fix: a clamping API (`relativedelta`, `plusMonths`, Luxon `plus`).
- **RRULE expanded as fixed-offset UTC** — every occurrence drifts an hour after the next DST change. Fix: expand in the `TZID` zone, convert each occurrence individually.
- **Elapsed time from wall clock** — NTP step makes the delta negative or enormous, poisoning metrics/timeouts. Fix: monotonic clock for all durations.
- **`SimpleDateFormat`/`dateutil.parser.parse`/`Date.parse` on machine data** — locale-dependent `MM/DD` vs `DD/MM` guessing silently swaps day and month. Fix: a fixed explicit pattern.
- **Dropping the offset on parse** — `2026-06-15T08:00:00+07:00` parsed as naive becomes 08:00 in the wrong zone (7h error). Fix: a parser that retains the offset and converts to UTC.

## Verify

- **Round-trip is stable:** parse → store as UTC → format back yields the same instant for a sample including a `+07:00` and a `-05:00` input. No value silently re-zoned.
- **DST gap handled:** constructing `02:30` on the spring-forward date in a DST zone applies the documented policy (shift-forward or reject) — it does not silently produce an arbitrary instant; the local→instant→local round-trip mismatch is detected.
- **DST overlap handled:** the fall-back `01:30` is resolvable to **both** instants via fold/disambiguation, and the code picks one deliberately (asserted 1h apart).
- **Suite green under multiple zones:** the full test run passes under `TZ=UTC`, `TZ=America/New_York`, and `TZ=Pacific/Kiritimati` (UTC+14) — proving no hidden local-zone assumption.
- **Boundary cases pass:** Dec 31→Jan 1 in a non-UTC zone, Feb 29 leap day, Jan 31 + 1 month clamps to Feb, and a weekly RRULE crossing a DST date keeps its local wall time.
- **Duration uses monotonic:** a simulated wall-clock backward step does not produce a negative or absurd elapsed value (proving the monotonic source).
- **Grep clean:** no `utcnow`/`SimpleDateFormat`/`new Date(<string>)`/`chrono::Local`/naive `strptime` remains in instant-handling paths.

Done = every stored/transported timestamp is a zone-carrying instant (UTC) or an explicit local-time-plus-IANA-zone, all parse/format uses an explicit offset-aware format, all durations use the monotonic clock, and the test suite passes under ≥3 timezones across the gap, overlap, leap-day, month-overflow, and recurrence boundaries.
