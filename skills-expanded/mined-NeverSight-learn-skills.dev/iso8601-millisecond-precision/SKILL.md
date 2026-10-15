---
name: iso8601-millisecond-precision
description: Require ISO 8601 textual representations for temporal values. Use when an agent needs to format, serialize, parse, document, review, or define textual date, time, datetime, or timestamp representations in APIs, events, persistence, logs, configuration, or other string-based boundaries. When the textual representation includes a time component, require millisecond precision.
---

# ISO 8601 Millisecond Precision

## Goal

When a temporal value must be represented textually, use ISO 8601.

This skill governs textual formatting and parsing only. It does not require temporal values to be stored internally as strings when the stack provides built-in or standard-library temporal types.

When the textual representation includes a time component, use millisecond precision exactly. For example, use `2026-03-20T14:35:12.123Z`, not a seconds-only form and not a microsecond or nanosecond form.

For date-only values, use the ISO 8601 calendar date form such as `2026-03-20`. Millisecond precision applies to temporal strings that include a time component.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- formats temporal values into strings
- parses textual date, time, datetime, or timestamp values
- defines API, event, message, or persistence contracts that use textual temporal representations
- documents expected textual date or time formats
- compares or validates temporal values represented as strings
- stores temporal values in text-oriented boundaries

## ISO 8601 Rule

1. Use ISO 8601 whenever a temporal value is represented as text.
   - Prefer extended ISO 8601 forms with explicit separators.
   - Do not use locale-dependent, ad hoc, or ambiguous textual date formats.

2. Require millisecond precision for any textual representation that includes a time component.
   - Use exactly three fractional second digits.
   - Do not omit fractional seconds when this rule applies.
   - Do not emit more or fewer than three fractional second digits.

3. Keep timezone or offset markers explicit when the textual value is timezone-aware.
   - Preserve the timezone or offset semantics required by the surrounding code or contract.
   - This skill governs the textual format, not the choice of timezone policy.

4. Keep textual formatting at the boundary.
   - Prefer built-in or standard-library temporal types inside the system when available.
   - Format to ISO 8601 text at APIs, persistence text columns, event payloads, configuration surfaces, logs, or other string-based boundaries.

## Detection Workflow

1. Identify the textual boundary.
   - Find where temporal values are turned into strings or read from strings.
   - Identify whether the boundary expects date-only or time-bearing values.

2. Determine the exact temporal shape.
   - Use date-only ISO 8601 for pure calendar dates.
   - Use time-bearing ISO 8601 with millisecond precision for datetimes, timestamps, and time values that include seconds or subsecond precision.

3. Trace formatting and parsing consistency.
   - Verify that the same textual format is used for both serialization and parsing.
   - Verify that contract documentation and validation logic match the actual emitted format.

## Writing or Changing Textual Temporal Representations

1. Emit ISO 8601 strings explicitly.
   - Use formatting helpers or library routines that produce ISO 8601 output.
   - Make the expected textual shape obvious in serializers, validators, and contract definitions.

2. Enforce exactly three fractional digits when time is present.
   - Normalize formatter settings so textual output always uses millisecond precision.
   - Reject or normalize incoming textual values that do not match the required precision when the contract is under your control.

3. Keep parsing and formatting symmetrical.
   - Ensure emitted strings can be parsed by the same format rules.
   - Avoid silent drift between serializer output and parser expectations.

4. Preserve timezone markers when applicable.
   - Keep `Z`, offsets, or other required timezone designators in the emitted ISO 8601 text when the value is timezone-aware.
   - Do not drop timezone information from a timezone-aware textual representation.

## Review Questions

When reading or reviewing code, ask:

- Is this temporal value being represented as text?
- Is the textual form ISO 8601?
- If the string includes a time component, does it use exactly millisecond precision?
- Do parsing, validation, documentation, and serialization all expect the same textual format?
- Would changing this code risk drifting into a non-ISO or non-millisecond textual representation?

If the answer is yes, apply this skill.

## Report the Outcome

When finishing the task:

- state which textual temporal representations were identified or changed
- state whether the representation is date-only or time-bearing
- state how ISO 8601 formatting and millisecond precision were implemented or preserved
