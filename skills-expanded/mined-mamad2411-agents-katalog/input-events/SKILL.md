---
name: input-events
description: >-
  Input Events: This specification defines additions to events for text and related input to allow for the monitoring and manipulation of default browser behavior in the context of text editor applications and other applications that deal with text input and text formatting. Covers Input Events Level 2 (track). Use when handling beforeinput and input events. Triggers: Input Events, beforeinput.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Input Events

This specification defines additions to events for text and related input to allow for the monitoring and manipulation of default browser behavior in the context of text editor applications and other applications that deal with text input and text formatting. This specification builds on the UI events spec [ UI-EVENTS ].

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when handling beforeinput and input events.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Input Events Level 2 (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words MAY , MUST , and MUST NOT in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **6.1.2.** "But if a given browser supports an editing operation which potentially leads to a change of the DOM, it MUST dispatch the corresponding beforeinput and input events."
3. **6.1.2.** "The returned StaticRanges MUST cover only the code points that the browser would normally replace, even if they are only part of a grapheme cluster ."
4. **6.2.** "A user agent MUST dispatch this event when the user has attempted to input in a contenteditable element."
5. **6.2.** "A user agent MUST NOT dispatch this event due to events that are not caused by attempted user input, such as system events."
6. **6.2.** "A user agent MUST dispatch this event immediately after the DOM has been updated due to user expressed intention to change the document contents which the browser has handled."
7. **6.2.** "If the browser makes no DOM change, either because the editing host is an EditContext editing host (which does not do automatic DOM changes) or because the user agent concludes that no DOM change is needed, the user agent MUST NOT dispatch this event."
8. **8..** "Event order when using "insertFromPaste" When an "insertFromPaste" beforeinput event is dispatched, it MUST be preceded by a paste [ CLIPBOARD-APIS ] event."

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

- [Input Events Level 2](https://www.w3.org/TR/input-events-2/): Working Draft, input-events-2 WD-input-events-2-20260501 (Working Draft, 2026-05-01), checked 2026-10-06.
