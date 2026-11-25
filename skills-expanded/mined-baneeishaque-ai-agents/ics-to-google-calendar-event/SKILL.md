---
name: ics-to-google-calendar-event
description: Composer — create a Google Calendar event from an .ics file or JSON event spec by composing ics-event-extraction-to-json, the google-workspace MCP calendar tools, and (on account mismatch) google-workspace-mcp-account-switch.
category: Calendar
layer: composer
---

# ICS To Google Calendar Event Skill (v1) — Composer

> **Skill ID:** `ics-to-google-calendar-event`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../../skill-factory/SKILL.md))

This is the **second half** of the event-email → calendar chain. It owns ONLY the account
preflight, the field mapping, the creation call, and the verification loop that turns an
`.ics` file (or JSON event spec) into a verified Google Calendar event — every parse is
delegated to a base primitive.

The **first half** is [`gmail-event-email-to-ics`](../gmail-event-email-to-ics/SKILL.md): it
produces the `.ics` deliverable this skill consumes.

***

## 1. Composition Rationale

This skill is a **composer** — it owns the account preflight, the ICS → MCP field mapping,
the creation/verification sequence, and the final report. It implements NO ICS parsing itself:

| Component | Layer | Role here |
| :--- | :--- | :--- |
| [`ics-event-extraction-to-json`](../ics-event-extraction-to-json/SKILL.md) | Base (script) | Parses the input `.ics` into JSON; supplies `dtstart.iso` / `dtend.iso` (with local offset) and the unescaped+unfolded `description` |
| [`google-workspace-mcp-account-switch`](../../mcp/google-workspace-mcp-account-switch/SKILL.md) | Base (procedural) | Conditional — switches the MCP account when the target calendar belongs to a different identity |

The chain is split at the `.ics` boundary so this half is reusable for ANY `.ics` source
(downloaded invites, generated files, third-party exports), independent of Gmail.

***

## 2. When to Apply

Use when the user asks to **create a Google Calendar event from an `.ics` file or JSON event
spec**:

- "add this invite to my calendar"
- "create the calendar event for that webinar from the `.ics`"
- "put these event details on my Google Calendar"

**Anti-trigger**: if no `.ics` (or spec) exists yet and the source is a Gmail email, start
with [`gmail-event-email-to-ics`](../gmail-event-email-to-ics/SKILL.md) first.

***

## 3. Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| google-workspace MCP tools | `people_getMe` (account preflight), `calendar_createEvent`, `calendar_getEvent` (verification); `calendar_listEvents` for optional duplicate checks |
| Python 3.10+ | Runs the base script (`extract-ics.py`) with standard-library-only dependencies |
| Input | An `.ics` file, or a JSON event spec following the [`ics-event-generation-from-json`](../ics-event-generation-from-json/SKILL.md) schema |

***

## 4. Workflow (Protocol)

1. **Account preflight** — call `people_getMe` and note the active identity. On mismatch
   (the target calendar belongs to another account), compose
   [`google-workspace-mcp-account-switch`](../../mcp/google-workspace-mcp-account-switch/SKILL.md)
   (`auth_clear` → follow-up call; NEVER batch the two calls) and re-verify the identity.
2. **Parse the input** — for an `.ics` file run
   `python3 .agents/skills/calendar/ics-event-extraction-to-json/scripts/extract-ics.py --input <file.ics> --pretty`;
   for a JSON spec, read it directly (B1 schema). Multiple `VEVENT`s → one calendar event
   each (confirm scope with the user when more than a couple).
3. **Map fields** per §5 — consume `dtstart.iso` / `dtend.iso` directly (they already carry
   the local offset); do NOT recompute timezones.
4. **Create** — `calendar_createEvent` with the mapped arguments; default `calendarId` is the
   primary calendar unless the user specifies another.
5. **Verify** — `calendar_getEvent` on the returned event ID; confirm summary, start, and end
   match the source; on mismatch, report the discrepancy instead of silently retrying.
6. **Report** — event ID, calendar, start/end, and the event link (when the response carries
   one). For batches, report one line per event.

***

## 5. Field Mapping (ICS/JSON → MCP `calendar_createEvent`)

| ICS/JSON field | MCP argument | Notes |
| :--- | :--- | :--- |
| `summary` | `summary` | Verbatim |
| `description` (unescaped + unfolded) | `description` | B2 already unescapes and unfolds — never re-escape |
| `location` | `location` | Verbatim |
| `dtstart.iso` | `start.dateTime` | ISO 8601 with local offset (e.g. `2026-09-26T19:00:00+05:30`) |
| `dtend.iso` | `end.dateTime` | ISO 8601 with local offset |
| `url` | appended to `description` | On its own line (e.g. `Join: <url>`) — no dedicated MCP URL field |
| `organizer` / `attendees` | — | Default NO attendees — do NOT invite the organizer |
| — | `addGoogleMeet` | Default `false` (set `true` only on explicit user request) |

***

## 6. Edge Cases

- **Missing `dtend`** → block a sensible duration only with a stated basis; otherwise stop
  and ask — never guess.
- **Unresolvable TZID** (B2 omits `iso`) → derive `dateTime` from `utc` (with `Z`), or stop
  and ask; never invent an offset.
- **All-day / date-only events** → out of contract for this chain; convert only on explicit
  user instruction, otherwise stop and ask.
- **Duplicate suspicion** → optionally `calendar_listEvents` over the event window before
  creating; report a likely duplicate instead of creating another.
- **Account mismatch** → switch via the base BEFORE creating; verify the identity from the
  `people_getMe` response.
- **Multi-event `.ics`** → one `calendar_createEvent` per event; report per event.
- **Verification mismatch** → report; never blind-retry the creation call.

***

## 7. Prohibited Actions

- Never invite attendees by default — especially not the organizer.
- Never enable `addGoogleMeet` unless the user explicitly asks.
- Never batch `auth_clear` with its follow-up call (dependent sequence).
- Never re-escape description text or recompute timezone offsets — consume B2's
  `description` and `iso` fields as-is.
- Never re-implement ICS parsing in this skill — delegate to the base script.
- Never fabricate a duration, timezone offset, or attendee list absent from the source.

***

## 8. Related Skills

- [`gmail-event-email-to-ics`](../gmail-event-email-to-ics/SKILL.md) — the first half of the
  chain; produces the `.ics` deliverable this skill consumes.
- [`ics-event-generation-from-json`](../ics-event-generation-from-json/SKILL.md) — schema
  reference for JSON-spec input to this skill.
- [`skill-factory`](../../skill-factory/SKILL.md) — §2.0 layering decision governing the
  base/composer split.
- [`redaction-portability`](../../redaction-portability/SKILL.md) — placeholder vocabulary for
  examples and reports.
