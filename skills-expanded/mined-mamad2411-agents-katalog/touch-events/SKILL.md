---
name: touch-events
description: >-
  Touch Events: The Touch Events specification defines a set of low-level events that represent one or more points of contact with a touch-sensitive surface, and changes of those points with respect to the surface and any DOM elements displayed upon it (e.g. Covers Touch Events. Use when handling touch events. Triggers: Touch Events, touchstart.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Touch Events

The Touch Events specification defines a set of low-level events that represent one or more points of contact with a touch-sensitive surface, and changes of those points with respect to the surface and any DOM elements displayed upon it (e.g. for touch screens) or associated with it (e.g. for drawing tablets without displays). It also addresses pen-tablet devices, such as drawing tablets, with consideration toward stylus capabilities.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when handling touch events.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Touch Events (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words MUST , MUST NOT , REQUIRED , SHOULD , SHOULD NOT , RECOMMENDED , MAY , and OPTIONAL in this specification are to be interpreted as described in [ RFC2119 ]."
2. **WebIDL Conformance.** "A conforming Web Events user agent must also be a conforming ECMAScript implementation of this IDL fragments in this specification, with the following exception: section 4.4.6 of Web IDL requires that IDL attributes are reflected as accessor properties on interface prototype objects."
3. **WebIDL Conformance.** "These data properties must have the same behavior when getting and setting as would be exhibited when invoking the getter and setter of the accessor properties on the platform object."
4. **3. Touch Interface.** "Touch objects are immutable; after one is created, its attributes must not change."
5. **3.1 Attributes.** "When a touch point becomes active, it must be assigned an identifier that is distinct from any other active touch point ."
6. **3.1 Attributes.** "While the touch point remains active, all events that refer to it must assign it the same identifier ."
7. **4. TouchList Interface.** "TouchList objects are immutable; after one is created, its contents must not change."
8. **5. TouchEvent Interface.** "TouchEvent objects are immutable; after one is created and initialized, its attributes must not change."

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

- [Touch Events](https://www.w3.org/TR/touch-events/): Recommendation, touch-events REC-touch-events-20131010 (Recommendation, 2013-10-10), checked 2026-10-06.
