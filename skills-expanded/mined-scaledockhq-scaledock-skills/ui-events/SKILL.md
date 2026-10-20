---
name: ui-events
description: >-
  UI Events: This specification defines UI Events which extend the DOM Event objects defined in [DOM] . Covers UI Events (track), UI Events KeyboardEvent key Values, UI Events KeyboardEvent code Values. Use when handling keyboard and mouse UI events. Triggers: UI Events, KeyboardEvent, code, key.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# UI Events

This specification defines UI Events which extend the DOM Event objects defined in [DOM] . UI Events are those typically implemented by visual user agents for handling user interaction such as mouse and keyboard input.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when handling keyboard and mouse UI events.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: UI Events (default, posture track); UI Events (uievents-old) (legacy: read and upgrade, never author); UI Events KeyboardEvent key Values (default); UI Events KeyboardEvent code Values (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.2. Conformance.** "Within this specification, the key words MUST , MUST NOT , REQUIRED , SHALL , SHALL NOT , SHOULD , SHOULD NOT , RECOMMENDED , MAY , and OPTIONAL are to be interpreted as described in [RFC2119] ."
2. **1.2. Conformance.** "A user agent is not required to conform to the entirety of another specification in order to conform to this specification, but it MUST conform to the specific parts of any other specification which are called out in this specification (e.g., a conforming UI Events user agent MUST support the DOMString data type as defined in [WebIDL] , but need not support every method or data type defined in…"
3. **1.2.1. Web browsers and other dynamic or interactive user agents.** "A conforming browser MUST dispatch events appropriate to the given EventTarget when the conditions defined for that event type have been met."
4. **1.2.1. Web browsers and other dynamic or interactive user agents.** "A conforming browser MUST support scripting, declarative interactivity, or some other means of detecting and dispatching events in the manner described by this specification, and MUST support the APIs specified for that event type ."
5. **1.2.1. Web browsers and other dynamic or interactive user agents.** "A browser which does not conform to all required portions of this specification MUST NOT claim conformance to UI Events."
6. **1.2.1. Web browsers and other dynamic or interactive user agents.** "A conforming browser MUST also be a conforming implementation of the IDL fragments in this specification, as described in the Web IDL specification [WebIDL] ."
7. **1.2.2. Authoring tools.** "A content authoring tool MUST NOT claim conformance to UI Events for content it produces which uses features of this specification marked as deprecated in this specification."
8. **1.2.2. Authoring tools.** "A conforming content authoring tool SHOULD provide to the content author a means to use all event types and interfaces appropriate to all host languages in the content document being produced."

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

- [UI Events](https://www.w3.org/TR/uievents/): Working Draft, uievents WD-uievents-20260221 (Working Draft, 2026-02-21), checked 2026-10-06.
- [UI Events KeyboardEvent key Values](https://www.w3.org/TR/uievents-key/): Recommendation, uievents-key REC-uievents-key-20250422 (Recommendation, 2025-04-22), checked 2026-10-06.
- [UI Events KeyboardEvent code Values](https://www.w3.org/TR/uievents-code/): Recommendation, uievents-code REC-uievents-code-20250422 (Recommendation, 2025-04-22), checked 2026-10-06.
