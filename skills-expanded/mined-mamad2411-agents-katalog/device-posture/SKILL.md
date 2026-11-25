---
name: device-posture
description: >-
  Device Posture API: This document specifies an API that allows web applications to request and be notified of changes of the posture of a device. Covers Device Posture API (build). Use when reading a foldable device posture. Triggers: Device Posture, devicePosture.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Device Posture API

This document specifies an API that allows web applications to request and be notified of changes of the posture of a device.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading a foldable device posture.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Device Posture API (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4.1.** "The type attribute: Get current device posture When getting the type attribute, the user agent MUST return the value of this 's relevant global object 's associated Document 's internal slot [[CurrentPosture]] ."
2. **6.1.** "Value: continuous | folded Applies to: visual media types Accepts min/max prefixes: No A user agent MUST reflect the applied posture of the web application via a CSS media query [ MEDIAQ ]."
3. **7..** "Reading the posture Every instance of Document has an internal slot [[CurrentPosture]] , which should be initialized when the Document is created, otherwise they MUST be initialized the first time they are accessed and before their value is read."
4. **7..** "The user agent MUST run the device posture change steps with document set to the Document and disallowRecursion set to true to initialize it."
5. **7.1.** "Device makers SHOULD make sure that the physical device postures map correctly to the postures defined by this specification."
6. **7.1.** "Some devices might also lack one or more of the postures due to physical constraints or device design, in which case the device SHOULD make sure that all combinations of angles and device orientation (which can be locked by [ SCREEN-ORIENTATION ] and host OS), as well as device specific signals, maps into one of the defined postures."
7. **8.2.** "Device Posture change When the user agent determines that the screen(s)' fold angle, orientation or device-specific signals have changed for a top-level traversable , it MUST run the device posture change steps with the top-level traversable 's active document ."
8. **14. Conformance.** "The key words MUST and SHOULD in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."

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

- [Device Posture API](https://www.w3.org/TR/device-posture/): Candidate Recommendation Draft, device-posture CRD-device-posture-20260520 (Candidate Recommendation Draft, 2026-05-20), checked 2026-10-06.
