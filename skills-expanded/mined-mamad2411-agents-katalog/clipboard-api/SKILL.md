---
name: clipboard-api
description: >-
  Clipboard API: This document describes APIs for accessing data on the system clipboard. Covers Clipboard API and events (track). Use when reading or writing the system clipboard. Triggers: Clipboard API, navigator.clipboard.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Clipboard API

This document describes APIs for accessing data on the system clipboard. It provides operations for overriding the default clipboard actions (cut, copy and paste), and for directly accessing the clipboard contents.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading or writing the system clipboard.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Clipboard API and events (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **6.6. Unsanitized data types.** "These data types MUST NOT be sanitized by UAs: image/png These data types MAY NOT be sanitized by UAs: optional unsanitized data types Optional unsanitized data types are mime type s specified by the web authors that MAY NOT be sanitized by the user agent."
2. **7.2.3. getType(type).** "If the system clipboard contents have changed since read() was called, this MUST fail rather than returning data that does not correspond to the current system clipboard state."
3. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
4. **5.2.1.4. ChangeId Generation.** "Similarly, when a user clears site data, the affected tabs should be refreshed, which causes event listeners to be re-attached and only receive future events with new change IDs."
5. **5.3.1. Event handlers that are allowed to modify the clipboard.** "Synthetic cut and copy events must not modify data on the system clipboard."
6. **5.3.2. Event handlers that are allowed to read from clipboard.** "Synthetic paste events must not give a script access to data on the real system clipboard."
7. **5.3.3. Integration with rich text editing APIs.** "If an implementation supports ways to execute clipboard commands through scripting, for example by calling the document.execCommand() method with the commands "cut", "copy" and "paste", the implementation must trigger the corresponding action, which again will dispatch the associated clipboard event."
8. **5.3.4. Interaction with other events.** "If the clipboard operation is triggered by keyboard input, the implementation must fire the corresponding event that initiates the clipboard operation."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
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

- [Clipboard API and events](https://www.w3.org/TR/clipboard-apis/): Working Draft, clipboard-apis WD-clipboard-apis-20260624 (Working Draft, 2026-06-24), checked 2026-10-06.
