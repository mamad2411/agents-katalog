---
name: built-in-temporal-types
description: Require built-in or standard-library temporal types for dates, times, datetimes, and related values. Use when an agent needs to create, modify, review, or interpret temporal fields, parameters, return types, persistence mappings, serializers, parsers, or API contracts. When timezone semantics matter, use a representation that preserves a geographic timezone such as an IANA zone ID and not merely a fixed UTC offset.
---

# Built-In Temporal Types

## Goal

Represent temporal values with built-in or standard-library temporal types that match their real meaning.

Use `date`-like types for calendar dates, `time`-like types for wall-clock times, and `datetime`-like types for date-and-time values. Do not represent temporal values as generic strings, numbers, or loose objects when the language or standard library already provides an appropriate temporal type.

When timezone semantics matter, use a representation that preserves a geographic timezone, such as an IANA timezone like `America/Mexico_City` or `Europe/Berlin`. A fixed offset such as `-06:00` or `+01:00` is not a geographic timezone and is not enough to model daylight saving time transitions.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines date, time, datetime, timestamp, schedule, deadline, or recurrence fields
- defines temporal parameters or return types
- parses or serializes temporal values
- maps temporal values to persistence or transport boundaries
- calculates or compares temporal values
- stores or exposes timezone information
- models business or integration concepts that depend on calendar or clock semantics

## Temporal Type Rule

1. Use the most precise built-in temporal type the stack provides for the actual meaning of the value.
   - Use a date-only type for calendar dates without a clock time.
   - Use a time-only type for wall-clock times without a date.
   - Use a datetime type for values that include both date and time.
   - Do not collapse these meanings into one generic text type when built-in temporal types exist.

2. Preserve geographic timezone semantics when timezone matters.
   - Use a built-in or standard-library representation that can carry a geographic timezone when the stack provides one.
   - Prefer timezone identifiers with real timezone rules, such as IANA zone IDs.
   - Do not treat a numeric UTC offset as an equivalent replacement for a geographic timezone.

3. If the stack separates the instant from the timezone identifier, keep both explicitly.
   - Use the built-in temporal type for the timestamp or datetime value.
   - Store the geographic timezone as an explicit timezone identifier, typically an IANA zone string, when that is how the stack preserves timezone rules.

4. Keep offsets as boundary details, not as the source of timezone truth.
   - Offsets may appear in serialized formats or protocol payloads when required by the boundary.
   - Do not use the offset alone as the durable representation of a timezone-aware business value.

## Detection Workflow

1. Determine the real temporal meaning first.
   - Identify whether the value is a calendar date, a wall-clock time, a datetime, an instant, a schedule, or a timezone-aware business timestamp.
   - Check whether the value must survive timezone conversions or daylight saving time transitions correctly.

2. Detect built-in temporal support in the stack.
   - Identify the native or standard-library temporal types available in the language.
   - Follow the project's established conventions for importing, constructing, storing, and serializing those types.

3. Trace timezone semantics end to end.
   - Identify where timezone information enters the system.
   - Identify whether the code preserves a geographic timezone ID or only an offset.
   - Verify that timezone-aware values keep the information needed to reproduce the correct local time across daylight saving time changes.

## Writing or Changing Temporal Code

1. Match the type to the meaning.
   - Choose the built-in temporal type that matches the actual semantics of the field or parameter.
   - Avoid using a datetime where only a date or time is intended.

2. Keep timezone-aware values explicitly geographic.
   - Use a zoned datetime built-in when the stack supports it.
   - If the stack does not provide a single built-in zoned type, keep the built-in temporal value together with a geographic timezone identifier.

3. Keep parsing and serialization explicit.
   - Parse external strings into built-in temporal types as early as practical.
   - Serialize back to boundary formats only at the boundary.
   - Preserve the geographic timezone identifier whenever the value is meant to remain timezone-aware.

4. Protect daylight saving time correctness.
   - Verify that recurring local times, deadlines, schedules, and user-facing times still resolve correctly when daylight saving time rules change the offset.
   - Do not assume the current offset is enough to reconstruct future or past local times in a geographic region.

## Review Questions

When reading or reviewing code, ask:

- What real temporal concept does this value represent: date, time, datetime, instant, or timezone-aware local time?
- Is the code using a built-in or standard-library temporal type that matches that meaning?
- If timezone matters, is a geographic timezone preserved?
- Is the code relying on an offset where a real timezone identifier is required?
- Would changing this code risk losing daylight saving time correctness or collapsing a temporal type into a generic string?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which temporal values or types were identified or changed
- state which built-in or standard-library temporal types were used, and why
- state how geographic timezone handling was implemented or preserved
