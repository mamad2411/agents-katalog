---
name: ics-event-generation-from-json
description: Base primitive — generate an RFC 5545-compliant iCalendar (.ics) file from a JSON event spec via a deterministic script (TEXT escaping, 75-octet UTF-8-safe folding, CRLF, UTC or TZID datetimes with VTIMEZONE templates, VALARM, built-in verification).
category: Calendar
---

# ICS Event Generation From JSON Skill (v1) — Base Primitive

> **Skill ID:** `ics-event-generation-from-json`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../../skill-factory/SKILL.md))

This is the **base skill** of the calendar generation stack. It owns ONLY the deterministic
JSON spec → `.ics` emission logic: RFC 5545 TEXT escaping, 75-octet UTF-8-safe line folding,
CRLF termination, `VTIMEZONE` template insertion, `VALARM` blocks, and structural
self-verification.

It has **no** knowledge of email, Gmail, the google-workspace MCP tools, or any calendar
API — composer skills (and callers) supply the JSON spec; this skill emits verified bytes.

***

## 1. Composition Rationale

This skill is a **base primitive** — it owns ONLY the deterministic spec → `.ics` emission.
It performs no network access, no email parsing, and no calendar mutation.

Composers that invoke this skill:

| Composer | Role |
| :--- | :--- |
| [`gmail-event-email-to-ics`](../gmail-event-email-to-ics/SKILL.md) | Normalizes a Gmail event-invitation email (attached `.ics` or body-embedded details) into this skill's JSON spec, then invokes `scripts/generate-ics.py` to emit the verified deliverable — in either the UTC form (no `VTIMEZONE`) or the TZID form (with `VTIMEZONE`). |

The primitive was extracted because the session's two generator scripts (a UTC variant and a
TZID+`VTIMEZONE` variant) shared identical escaping/folding machinery — inlining it into each
composer would split the SSOT and silently diverge.

**Anti-Duplication**: any skill that must emit an `.ics` file MUST invoke this script rather
than re-implementing RFC 5545 escaping, folding, or `VTIMEZONE` insertion.

***

## 2. Scope & Intent

**Does:** read a JSON spec (UTF-8), validate it, build the `VCALENDAR` logical lines, fold them
to physical lines, verify the result structurally, and write the CRLF-terminated `.ics` file
(creating parent directories as needed).

**Does NOT:**

- Parse `.ics` files — that is [`ics-event-extraction-to-json`](../ics-event-extraction-to-json/SKILL.md) (the inverse operation).
- Fetch email, attachments, or event details from any source — that is the composer layer.
- Call the google-workspace MCP calendar tools or any calendar API — that is the composer layer.
- Convert between timezones — callers supply the local or UTC datetime values; the shipped
  timezone templates carry fixed public transition data.

Given a pinned `uid` + `dtstamp`, output is byte-deterministic.

***

## 3. Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| Python 3.10+ | Standard library only (`argparse`, `datetime`, `json`, `re`, `sys`, `pathlib`) — no pip dependencies; invoke portably as `python3` |
| Spec JSON | UTF-8 file matching the schema in §5 |
| Timezone template (optional) | `scripts/timezones/<name>.template` — public timezone data only |
| No network | The script is fully offline |

***

## 4. CLI Contract (Stable)

Located at [`scripts/generate-ics.py`](./scripts/generate-ics.py).

```bash
python3 scripts/generate-ics.py --spec <spec.json> --output <file.ics> [--no-verify]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--spec` | ✅ | Path to the JSON event spec |
| `--output` | ✅ | Destination `.ics` path (parent directories auto-created; existing file overwritten) |
| `--no-verify` | ❌ | Skip the built-in structural verification (§7) |

**stdout on success:** `VERIFY OK` (unless `--no-verify`) plus a
`bytes=<N>  physical_lines=<M>` line, then `WROTE <path>`.
**Errors:** a single `ERROR: <detail>` line on stderr.

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Success — file written and verified |
| 1 | Spec validation, JSON parse, or IO error |
| 2 | argparse usage error |

***

## 5. Spec JSON Schema

Literal example (fictional data — see
[`scripts/event-spec.example.json`](./scripts/event-spec.example.json)):

```json
{
  "prodid": "-//Example//Event Publisher 1.0//EN",
  "method": "PUBLISH",
  "timezone": {"tzid": "Asia/Kolkata", "template": "asia-kolkata"},
  "event": {
    "uid": "example-webinar-20260926-0001@example.com",
    "dtstamp": "20260926T123931Z",
    "dtstart": {"value": "20260926T190000", "tzid": "Asia/Kolkata"},
    "dtend": {"value": "20260926T203000", "tzid": "Asia/Kolkata"},
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
}
```

| Field | Required | Meaning |
| :--- | :---: | :--- |
| `prodid` | ❌ | `PRODID` value (default `-//ai-suite//ics-event-generation-from-json//EN`) |
| `method` | ❌ | `METHOD` value (default `PUBLISH`) |
| `timezone` | ✅* | `VTIMEZONE` source — required when any datetime uses the `tzid` form |
| `event` | ✅ | Single event object |
| `event.uid` | ✅ | Globally unique event identifier (defaults to empty string — always supply one) |
| `event.dtstamp` | ❌ | `YYYYMMDDTHHMMSSZ`; defaults to current UTC — pin it for reproducible output |
| `event.dtstart` / `event.dtend` | ✅ | Datetime object (forms below) |
| `event.summary` | ✅ | Event title (TEXT-escaped) |
| `event.description` | ❌ | Multi-line text; literal `\n` becomes an escaped newline |
| `event.location` | ❌ | TEXT-escaped |
| `event.url` | ❌ | Emitted verbatim (not TEXT-escaped) |
| `event.organizer` | ❌ | `{"cn": ..., "email": ...}` → `ORGANIZER;CN=<cn>:mailto:<email>` |
| `event.categories` | ❌ | List of strings → single comma-joined `CATEGORIES` line |
| `event.status` | ❌ | e.g. `CONFIRMED` |
| `event.class` | ❌ | e.g. `PUBLIC` |
| `event.transp` | ❌ | e.g. `OPAQUE` |
| `event.alarms` | ❌ | List of `{"action", "description", "trigger"}` objects → one `VALARM` each |

### Datetime Forms

- UTC form: `{"utc": "YYYYMMDDTHHMMSSZ"}` → `DTSTART:20260926T133000Z` (no `TZID`).
- Local form: `{"value": "YYYYMMDDTHHMMSS", "tzid": "<Zone>"}` →
  `DTSTART;TZID=<Zone>:20260926T190000` (requires a `timezone` block; **exactly one** distinct
  `TZID` per calendar across `DTSTART` + `DTEND`).

### Timezone Sources

- `{"tzid": "<Zone>", "template": "<name>"}` loads `scripts/timezones/<name>.template`
  (name must match `[a-z0-9-]+`). The block must span `BEGIN:VTIMEZONE`..`END:VTIMEZONE` and
  declare `TZID:<Zone>`.
- `{"tzid": "<Zone>", "block": "<VTIMEZONE text>"}` accepts a literal block with the same
  span/`TZID` requirements.

***

## 6. Protocol — Emission Order & RFC 5545 Machinery

Canonical emission order (RFC 5545 does not mandate property order; this generator fixes one
order so output is deterministic):

```text
BEGIN:VCALENDAR / VERSION:2.0 / PRODID / CALSCALE:GREGORIAN / METHOD / [VTIMEZONE]
BEGIN:VEVENT / UID / DTSTAMP / DTSTART / DTEND / SUMMARY / DESCRIPTION /
LOCATION / URL / ORGANIZER / CATEGORIES / STATUS / CLASS / TRANSP /
[VALARMs] / END:VEVENT / END:VCALENDAR
```

- **TEXT escaping** (SUMMARY, DESCRIPTION, LOCATION, VALARM DESCRIPTION): backslash → `\\`,
  `;` → `\;`, `,` → `\,`, then CRLF/CR/LF → `\n` (single-pass safe: backslashes are doubled
  first). `URL`, `UID`, `DTSTAMP`, and datetime values are emitted verbatim.
- **Folding**: each logical line is folded to physical lines of ≤ 75 octets; continuation
  lines begin with a single space, which counts toward the limit (content budget 74). Splits
  are UTF-8 safe — a multi-byte character is never divided across physical lines.
- **Termination**: physical lines joined with CRLF plus a trailing CRLF; never a bare LF.
- **Optional properties** are omitted when absent; `VALARM` defaults are
  `ACTION:DISPLAY` / `TRIGGER:-PT15M`.

***

## 7. Built-in Verification

Runs by default (`--no-verify` skips it; the file is still written). Any failure raises before
the file is written:

1. No bare LF — every line ending is CRLF.
2. No physical line exceeds 75 octets.
3. Unfold round-trip — unfolding the physical lines reconstructs the logical lines exactly.
4. Required tokens present (`BEGIN/END:VCALENDAR`, `BEGIN/END:VEVENT`, `UID:`, `DTSTAMP:`,
   `DTSTART`, `DTEND`, `SUMMARY:`).
5. Exactly one `VEVENT`.
6. `VTIMEZONE` present iff a `tzid` datetime form is used, and its `TZID` matches.

***

## 8. Edge Cases

- **TZID without `timezone`** → error; **more than one distinct TZID** across datetimes →
  error (single timezone per calendar).
- **Template name invalid** (outside `[a-z0-9-]+`) or **template missing** → error; a block
  not spanning `BEGIN:VTIMEZONE`..`END:VTIMEZONE` or not declaring the matching `TZID` →
  error.
- **`dtstamp` default** is "now" — output is not reproducible unless pinned; pin `uid` +
  `dtstamp` for byte-parity comparisons.
- **Output parent directories** are auto-created; an existing file is overwritten silently.
- **`--no-verify`** still writes the file — use it only for deliberate structural experiments.
- **Timezone template data** is fixed public transition data; the shipped
  `asia-kolkata.template` carries a pinned `LAST-MODIFIED`. Update template content
  deliberately, never ad hoc.
- **Folding near multi-byte characters** (e.g. emoji in a description) is exercised by the
  verification's octet check — keep descriptions ASCII-safe when byte-parity matters.

***

## 9. Prohibited Actions

- Never hand-edit a generated `.ics` — change the spec and regenerate.
- Never re-implement escaping/folding/`VTIMEZONE` insertion in a composer — invoke this
  script (Anti-Duplication).
- Never ship personal data in specs or templates — examples use fictional placeholders only
  (see [`redaction-portability`](../../redaction-portability/SKILL.md)); timezone templates
  carry public timezone data only.
- Never use the `dtstamp` default for deliverables where reproducibility is expected.

***

## 10. Script Reference

| Artifact | Role |
| :--- | :--- |
| [`scripts/generate-ics.py`](./scripts/generate-ics.py) | Entry point — spec → verified `.ics` |
| [`scripts/timezones/asia-kolkata.template`](./scripts/timezones/asia-kolkata.template) | Public `VTIMEZONE` data for `Asia/Kolkata` (fixed +05:30, no DST) |
| [`scripts/event-spec.example.json`](./scripts/event-spec.example.json) | Fictional example spec (TZID form + `VALARM`) |

Example (self-anchored path):

```bash
python3 .agents/skills/calendar/ics-event-generation-from-json/scripts/generate-ics.py \
  --spec .agents/skills/calendar/ics-event-generation-from-json/scripts/event-spec.example.json \
  --output scratch/example.ics
```

***

## 11. Related Skills

- [`ics-event-extraction-to-json`](../ics-event-extraction-to-json/SKILL.md) — sibling base; the
  inverse operation (parse `.ics` back into a JSON spec), used for round-trip verification.
- [`skill-factory`](../../skill-factory/SKILL.md) — §2.0 layering decision and script authoring
  mandates governing this skill.
- [`redaction-portability`](../../redaction-portability/SKILL.md) — placeholder vocabulary for
  spec examples and shipped artifacts.
