---
name: datetime-correctness
version: 1.0.0
description: Timezone, DST, and date-arithmetic failure modes — UTC-storage discipline, spring-forward gaps, fall-back ambiguity, epoch/ISO serialization pitfalls, and month/year boundary arithmetic. Use whenever software-engineer handles dates or times across timezones or storage boundaries, and whenever qa-engineer designs boundary or invariant tests touching time. Do NOT use for locale formatting, currency, RTL layout, or translation completeness — those are localization concerns, not datetime correctness.
---

# Datetime Correctness

> Scope note: this is deliberately a narrow, single-hazard skill. It sits alongside `concurrency-and-thread-safety` and `caching-and-invalidation` as one of the classic high-defect-density areas that happy-path testing reliably misses. If those three ever start overlapping in practice, they could fold into one hazards skill — kept separate for now because each fires on a different signal.

## The default rule
Store and compute in UTC; convert to a local timezone only at the point of display or user input. Nearly every datetime bug traces back to a violation of this somewhere in the pipeline — a timestamp stored in local time, a comparison done across two values in different zones, or a "naive" datetime (no timezone attached) that gets treated as if it were unambiguous.

## DST transitions — the two distinct failure shapes
- **Spring-forward gap** — a range of local times that never occurred (clocks jump from 1:59:59 to 3:00:00). A naive datetime constructed inside that gap is invalid, and different libraries resolve it differently (error, silently shift, or silently produce a nonexistent moment) — know which your stack does, don't assume.
- **Fall-back overlap** — a range of local times that occurs twice in the same day. A naive datetime in that range is ambiguous — "2:30 AM" happened twice, and code that doesn't track which occurrence it means can silently pick the wrong one. This especially bites duration calculations: "this event lasted 1 hour" across a fall-back boundary is not simply end-minus-start in local time.

## Serialization pitfalls
- **Epoch timestamps** — confirm seconds vs. milliseconds vs. microseconds explicitly wherever a raw integer crosses a system boundary. A silent factor-of-1000 error here is common and easy to miss in casual review, since the number still looks plausible as *a* timestamp.
- **ISO 8601 strings** — confirm whether the offset/zone is present and preserved through every hop. Some serializers silently drop it, converting a timezone-aware value into a naive one downstream.
- Confirm the same value round-trips through serialize → deserialize without drift. This is a natural metamorphic check (per `qa-engineer`'s technique set) for any datetime crossing a wire or storage boundary.

## Date arithmetic
- "Add one month" is not well-defined at the end of a month (Jan 31 + 1 month = ?) — know and test what your library actually does (clamp to the last valid day, roll over into the next month, or error) rather than assuming.
- Date **ranges** need an explicit, consistent convention for inclusive vs. exclusive endpoints. A report boundary that's inclusive on one end and exclusive on the other is a classic off-by-one, and it's easy to get each individual comparison "right" while the overall range is still wrong.
- Leap years, and far more rarely leap seconds, break arithmetic that assumes a fixed number of days per year or seconds per day — usually only material for high-precision or long-duration calculations, but worth naming as a real (if rare) edge case rather than an urban legend.

## Testing recommendations
- Test explicitly across a DST boundary in a timezone that observes it — not just in UTC or the developer's own local timezone, both of which can silently hide the entire class of bug.
- Test a year boundary and a month-end boundary explicitly for any date-arithmetic logic.
- Test with at least one timezone that has a non-whole-hour offset (several exist) if the system supports arbitrary user timezones — code that assumes whole-hour offsets breaks quietly on these.
- Where `qa-engineer`'s boundary-value analysis is being applied to a date/time input, treat DST transition points and month/year boundaries as boundaries in the formal sense, not just the numeric min/max of the range.
