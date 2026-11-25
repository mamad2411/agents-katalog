---
name: gmail-event-email-to-ics
description: Composer — turn a Gmail event-invitation email (attached .ics or body-embedded details) into a verified, maximum-detail .ics file by composing the google-workspace MCP Gmail tools, ics-event-extraction-to-json, and ics-event-generation-from-json.
category: Calendar
layer: composer
---

# Gmail Event Email To ICS Skill (v1) — Composer

> **Skill ID:** `gmail-event-email-to-ics`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../../skill-factory/SKILL.md))

This is the **first half** of the event-email → calendar chain. It owns ONLY the workflow
ordering and normalization decisions that turn a Gmail event-invitation email into a verified,
maximum-detail `.ics` deliverable — every parse and emission is delegated to a base primitive.

The **second half** is [`ics-to-google-calendar-event`](../ics-to-google-calendar-event/SKILL.md):
it consumes this skill's `.ics` deliverable (or any `.ics`) to create a Google Calendar event.

***

## 1. Composition Rationale

This skill is a **composer** — it owns the account preflight, the email triage, the
attachment-vs-body decision, field normalization, the duration policy, and deliverable
placement. It implements NO ICS machinery itself:

| Component | Layer | Role here |
| :--- | :--- | :--- |
| [`ics-event-extraction-to-json`](../ics-event-extraction-to-json/SKILL.md) | Base (script) | Parses a downloaded attachment `invite.ics` into JSON for normalization |
| [`ics-event-generation-from-json`](../ics-event-generation-from-json/SKILL.md) | Base (script) | Emits the verified `.ics` deliverable from the normalized JSON spec (UTC or TZID form) |
| [`google-workspace-mcp-account-switch`](../../mcp/google-workspace-mcp-account-switch/SKILL.md) | Base (procedural) | Conditional — switches the MCP account when the target email belongs to a different identity |
| [`scratch-artifact-naming`](../../general/file/scratch-artifact-naming/SKILL.md) | Base (script) | Resolves the session-scoped landing stem for downloaded attachment intermediates |

The full chain is split at the `.ics` boundary so the generation half is reusable without
Gmail (see C2) and the Gmail half is reusable without calendar creation.

***

## 2. When to Apply

Use when the user asks to **turn an event-invitation email into a calendar file**:

- "make an `.ics` from this webinar invitation"
- "download the invite attached to that email and save it as a calendar file"
- "the event details are only in the email body — build the calendar file"

**Anti-trigger**: if the goal is to create the calendar event itself, continue to
[`ics-to-google-calendar-event`](../ics-to-google-calendar-event/SKILL.md) after this skill's
deliverable exists.

***

## 3. Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| google-workspace MCP tools | `gmail_search`, `gmail_get`, `gmail_downloadAttachment`; `people_getMe` for the account preflight |
| Python 3.10+ | Runs the base scripts (`extract-ics.py`, `generate-ics.py`) with standard-library-only dependencies |
| Session scratch folder | Intermediates (downloaded attachments) land under `<repo>/scratch/<session-id>/` via `resolve-scratch-path.py` |
| Output folder | Deliverables land in the user's chosen folder — never a temp folder |

***

## 4. Workflow (Protocol)

1. **Account preflight** — call `people_getMe` and note the active identity. If the invitation
   email belongs to a different account, compose
   [`google-workspace-mcp-account-switch`](../../mcp/google-workspace-mcp-account-switch/SKILL.md)
   first (`auth_clear` → follow-up call; NEVER batch the two calls).
2. **Search** — `gmail_search` with narrowing queries (`from:`, `subject:`, `newer_than:`);
   select the event-invitation message(s). When several emails describe the same event,
   prefer the one with an attachment.
3. **Read** — `gmail_get` in `full` format; inspect the attachment list and the body.
4. **Extract the source of truth**:
   - **Attachment path** — `gmail_downloadAttachment` to a stem resolved by
     `python3 .agents/skills/general/file/scratch-artifact-naming/scripts/resolve-scratch-path.py --repo <repo> --purpose
     invite-ics-source`
     (append `.ics`); then run
     [`ics-event-extraction-to-json`](../ics-event-extraction-to-json/SKILL.md)
     (`extract-ics.py --input <file> --pretty`).
   - **Body-only path** — extract date, time, duration, timezone, join link, meeting IDs, and
     organizer from the body per §5.
5. **Normalize** — build one JSON spec per event for
   [`ics-event-generation-from-json`](../ics-event-generation-from-json/SKILL.md):
   - multi-email / multi-event input → **one `.ics` per event**, descriptive kebab-case
     filenames (`<organizer-slug>-<event-slug>-<YYYY-MM-DD>.ics`);
   - duration policy — when the email states no duration, block **90 minutes** and note it in
     `DESCRIPTION`;
   - keep the stated timezone (IST / `Asia/Kolkata` when the email states it); use the TZID
     form with the matching template, else a literal `VTIMEZONE` block, else the UTC form;
   - pin `uid` and `dtstamp` for reproducible output.
6. **Generate** — run `generate-ics.py --spec <spec.json> --output <deliverable>.ics`; keep
   the built-in verification enabled.
7. **Verify by reading back** — re-parse the generated file (B2 `extract-ics.py`) and confirm
   summary, start/end (with zone), location, URL, and organizer against the email; report the
   deliverable path(s).

***

## 5. Body-Only Extraction Guidance

| Detail | Typical location | Mapping |
| :--- | :--- | :--- |
| Date + time window | body text (e.g. "7:00 PM – 8:30 PM IST") | `dtstart` / `dtend` (TZID form) |
| Duration | body text, when stated | `dtend − dtstart`; else the 90-minute default + `DESCRIPTION` note |
| Timezone | "IST" / "Asia/Kolkata" / explicit zone | `timezone` + datetime `tzid` |
| Join link | "Join here" / Zoom / Teams URL | `url` (verbatim) |
| Meeting ID / passcode | body text | `DESCRIPTION` only — never in `url` |
| Organizer | email `From:` header or body signature | `organizer {cn, email}` |
| Event title | subject line / body heading | `summary` |

***

## 6. Edge Cases

- **Multiple events in one email** → one spec and one `.ics` per event.
- **Malformed attachment** → fall back to body extraction; note the fallback in the report.
- **Multiple attachments** → use the event invitation; ignore unrelated files.
- **HTML-only body** → read the HTML content from `gmail_get` and extract per §5.
- **No duration stated** → 90-minute block; the `DESCRIPTION` must carry the note — never
  silently invent an end time.
- **Account mismatch** → compose the account-switch base BEFORE reading that account's mail;
  verify the new identity via the `people_getMe` response.
- **`dtstamp`/`uid` not pinned** → output is not reproducible; pin both when the deliverable
  may be compared byte-for-byte.
- **Unknown timezone** → fall back to the UTC form rather than guessing a zone.

***

## 7. Prohibited Actions

- Never fabricate or guess details absent from the email (times, links, IDs, organizer).
- Never omit the duration note when the 90-minute default is applied.
- Never write intermediates or deliverables to temp folders — intermediates go to the
  session scratch folder via `scratch-artifact-naming`; deliverables go to the user's chosen
  folder with descriptive kebab-case names.
- Never put meeting passcodes into the `url` property — `DESCRIPTION` only.
- Never batch `auth_clear` with its follow-up call (dependent sequence).
- Never re-implement ICS parsing/generation in this skill — delegate to the base scripts.

***

## 8. Related Skills

- [`ics-to-google-calendar-event`](../ics-to-google-calendar-event/SKILL.md) — the second half
  of the chain; creates a Google Calendar event from this skill's `.ics` deliverable.
- [`skill-factory`](../../skill-factory/SKILL.md) — §2.0 layering decision governing the
  base/composer split.
- [`redaction-portability`](../../redaction-portability/SKILL.md) — placeholder vocabulary for
  examples and reports.
- [`gmail-poll-for-message`](../../email/gmail-poll-for-message/SKILL.md) — the Gmail IMAP access
  sibling (app-password polling); use it when the invitation must be waited for rather than
  searched on demand.
