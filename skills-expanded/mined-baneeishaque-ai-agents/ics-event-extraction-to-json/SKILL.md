---
name: ics-event-extraction-to-json
description: Base primitive — parse an iCalendar (.ics) file into a JSON event spec via a deterministic script (line unfolding, TEXT unescaping, parameter parsing, multi-VEVENT and VALARM support, zoneinfo-derived UTC/ISO datetime forms).
category: Calendar
---

# ICS Event Extraction To JSON Skill (v1) — Base Primitive

> **Skill ID:** `ics-event-extraction-to-json`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../../skill-factory/SKILL.md))

This is the **base skill** of the calendar extraction stack. It owns ONLY the deterministic
`.ics` → JSON parsing logic: physical-line unfolding, RFC 5545 TEXT unescaping, property and
parameter parsing, multi-`VEVENT` handling, `VALARM` nesting, and `zoneinfo`-derived `utc` /
`iso` datetime forms.

It has **no** knowledge of email, Gmail, the google-workspace MCP tools, or any calendar
API — callers supply the `.ics` bytes; this skill emits a JSON document on stdout.

***

## 1. Composition Rationale

This skill is a **base primitive** — it owns ONLY the deterministic `.ics` → JSON parse.
It performs no network access, no generation, and no calendar mutation.

Composers that invoke this skill:

| Composer | Role |
| :--- | :--- |
| [`gmail-event-email-to-ics`](../gmail-event-email-to-ics/SKILL.md) | Parses a downloaded attachment `invite.ics` into JSON, normalizes the event fields, then re-emits a maximum-detail `.ics` via [`ics-event-generation-from-json`](../ics-event-generation-from-json/SKILL.md). |
| [`ics-to-google-calendar-event`](../ics-to-google-calendar-event/SKILL.md) | Parses an input `.ics`, maps the JSON fields onto google-workspace MCP `calendar_createEvent` arguments (consuming `dtstart.iso` / `dtend.iso` directly), then verifies via `calendar_getEvent`. |

The primitive was extracted because every future calendar workflow (email-to-calendar,
calendar sync, invite audits) needs the same robust parse — the session's extraction
incidents (folding and escaping edge cases) are hardened here once.

**Anti-Duplication**: any skill that must read an `.ics` file MUST invoke this script rather
than re-implementing unfolding, unescaping, or datetime derivation.

***

## 2. Scope & Intent

**Does:** read a `.ics` file (UTF-8), unfold physical lines, parse content lines into
properties/parameters, assemble the calendar header, the timezone `TZID` list, and the event
list (with nested `VALARM`s), and print the JSON document on stdout.

*Does NOT:*

- Generate `.ics` files — that is [`ics-event-generation-from-json`](../ics-event-generation-from-json/SKILL.md) (the
  inverse operation).
- Fetch email, attachments, or event details from any source — that is the composer layer.
- Call the google-workspace MCP calendar tools or any calendar API — that is the composer layer.
- Expand recurrence rules (`RRULE`/`RDATE`/`EXDATE`) or surface `ATTENDEE` lists — out of
  the contract (a recurring master event parses as a single event with its stated datetimes).

***

## 3. Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| Python 3.10+ | Standard library only (`argparse`, `datetime`, `json`, `re`, `sys`, `pathlib`, `zoneinfo`) — no pip dependencies; invoke portably as `python3` |
| Timezone database | `zoneinfo` resolves `TZID` values against the system tz database; when a zone is unresolvable, `utc`/`iso` are omitted (the `value`/`tzid` fields are always kept) |
| No network | The script is fully offline |

***

## 4. CLI Contract (Stable)

Located at [`scripts/extract-ics.py`](./scripts/extract-ics.py).

```bash
python3 scripts/extract-ics.py --input <file.ics> [--pretty]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--input` | ✅ | Path to the `.ics` file |
| `--pretty` | ❌ | Pretty-print the JSON (2-space indent); default is compact single-line JSON |

**stdout:** the JSON document only (no diagnostic noise).
**Errors:** a single `ERROR: <detail>` line on stderr.

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Success — JSON document printed |
| 1 | Parse or IO error |
| 2 | argparse usage error |

***

## 5. Output JSON Schema

Shape (fictional values):

```json
{
  "calendar": {"prodid": "-//Example//Event Publisher 1.0//EN", "version": "2.0", "method": "PUBLISH"},
  "timezones": ["Asia/Kolkata"],
  "events": [
    {
      "uid": "example-webinar-20260926-0001@example.com",
      "dtstamp": "20260926T123931Z",
      "dtstart": {"value": "20260926T190000", "tzid": "Asia/Kolkata", "utc": "20260926T133000Z", "iso": "2026-09-26T19:00:00+05:30"},
      "dtend": {"value": "20260926T203000", "tzid": "Asia/Kolkata", "utc": "20260926T150000Z", "iso": "2026-09-26T20:30:00+05:30"},
      "summary": "Example Webinar",
      "description": "Multi-line description.\nSecond line.",
      "location": "Online",
      "url": "https://example.com/webinar",
      "organizer": {"cn": "Example Org", "email": "events@example.com"},
      "categories": ["Webinar"],
      "status": "CONFIRMED",
      "class": "PUBLIC",
      "transp": "OPAQUE",
      "alarms": [{"action": "DISPLAY", "description": "Reminder", "trigger": "-PT15M"}]
    }
  ]
}
```

- `events[].dtstart` / `dtend` always carry `value` (+ `tzid` when the source had a `TZID`
  parameter); `utc` and `iso` are added when derivable (see §6). The `iso` form includes the
  local offset and is consumed directly by the calendar composers.
- Absent properties are omitted from the event object; `alarms` is always present (possibly
  empty).
- `calendar` fields are `null` when the source omits them.

***

## 6. Protocol — Parsing Rules

1. **Unfold**: normalize CRLF to LF, then join continuation lines by removing each `LF +
   single space` pair (bare-LF sources unfold identically).
2. **Unescape TEXT** (SUMMARY, DESCRIPTION, LOCATION, CATEGORIES items, VALARM DESCRIPTION)
   with a single-pass `\\(.)` group replacement mapping `\n`/`\N` → newline and every other
   escaped character to itself — correct for both `\n` and `\\n` sequences.
3. **Parse content lines** as `NAME;PARAM=VALUE:VALUE` — the first `:` splits the value;
   parameters split on `;`. Names and parameter keys are upper-cased.
4. **Assemble**: calendar-level `PRODID`/`VERSION`/`METHOD`; each `VTIMEZONE` contributes its
   `TZID` to `timezones`; each `VEVENT` appends to `events`; each `VALARM` nests inside its
   event under `alarms`.
5. **Datetime derivation**: `YYYYMMDDTHHMMSSZ` values get `utc` (the value itself) and `iso`
   (UTC offset `+00:00`); `YYYYMMDDTHHMMSS` values with a resolvable `TZID` get `utc` and
   `iso` via `zoneinfo` (local offset preserved).
6. **Field mapping**: `ORGANIZER` → `{"cn": <CN param>, "email": <mailto-stripped value>}`;
   `CATEGORIES` → list split on unescaped commas (escaped `\,` stays inside its item);
   `ACTION`/`TRIGGER` map into the current `VALARM`.

***

## 7. Edge Cases

- **Unresolvable `TZID`** → the datetime keeps `value` + `tzid`; `utc`/`iso` are omitted
  (graceful degradation, never an error).
- **Recurring events** — `RRULE`/`RDATE`/`EXDATE` are not expanded; the master `VEVENT`
  parses as a single event with its stated datetimes.
- **`ATTENDEE` lines** are not surfaced (out of the output contract).
- **Multiple `VEVENT`s** → one JSON entry each, in file order.
- **Property line without `:`** or a malformed `;` parameter → `ERROR` on stderr, exit 1.
- **Unicode content** (emoji, non-Latin scripts) survives unfolding and unescaping
  byte-faithfully.
- **Nested `VALARM` outside a `VEVENT`** is ignored (never attached to the wrong event).

***

## 8. Prohibited Actions

- Never re-implement unfolding/unescaping in a composer — invoke this script
  (Anti-Duplication).
- Never treat the output as a complete iCalendar model — recurrence, attendees, and unknown
  properties are intentionally out of contract; extend the script deliberately if a new
  consumer needs them.
- Never commit real invitation files as test fixtures — use fictional placeholder data
  (see [`redaction-portability`](../../redaction-portability/SKILL.md)).

***

## 9. Script Reference

| Artifact | Role |
| :--- | :--- |
| [`scripts/extract-ics.py`](./scripts/extract-ics.py) | Entry point — `.ics` → JSON on stdout |

Example (self-anchored path):

```bash
python3 .agents/skills/calendar/ics-event-extraction-to-json/scripts/extract-ics.py \
  --input scratch/invite.ics --pretty
```

***

## 10. Related Skills

- [`ics-event-generation-from-json`](../ics-event-generation-from-json/SKILL.md) — sibling base;
  the inverse operation (emit `.ics` from a JSON spec), used for round-trip verification.
- [`skill-factory`](../../skill-factory/SKILL.md) — §2.0 layering decision and script authoring
  mandates governing this skill.
- [`redaction-portability`](../../redaction-portability/SKILL.md) — placeholder vocabulary for
  fixtures and shipped artifacts.
