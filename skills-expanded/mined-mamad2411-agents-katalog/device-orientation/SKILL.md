---
name: device-orientation
description: >-
  Device Orientation and Motion: This specification defines events that represent the physical orientation and motion of a hosting device. Covers Device Orientation and Motion (build). Use when reading device orientation or motion events. Triggers: deviceorientation, devicemotion.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Device Orientation and Motion

This specification defines events that represent the physical orientation and motion of a hosting device. These events provide web applications with access to orientation and motion data. The specification is designed to be agnostic to the underlying sources of this data, aiming to achieve interoperability across different environments.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading device orientation or motion events.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Device Orientation and Motion (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **1. Introduction.** "Where practically possible, the event should provide the acceleration of the device’s center of mass."
3. **3.2. Device Motion.** "As with device orientation, rotations must use the right-hand convention, such that positive rotation around an axis is clockwise when viewed along the positive direction of the axis."
4. **4. Permissions.** "For the implementation to fall back to absolute orientation data, the "magnetometer" permission must also be granted ."
5. **6.1. deviceorientation Event.** "The alpha attribute must return the value it was initialized to."
6. **6.1. deviceorientation Event.** "The beta attribute must return the value it was initialized to."
7. **6.1. deviceorientation Event.** "The gamma attribute must return the value it was initialized to."
8. **6.1. deviceorientation Event.** "The absolute attribute must return the value it was initialized to."

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

- [Device Orientation and Motion](https://www.w3.org/TR/orientation-event/): Candidate Recommendation Draft, orientation-event CRD-orientation-event-20250212 (Candidate Recommendation Draft, 2025-02-12), checked 2026-10-06.
