---
name: generic-sensor
description: >-
  Generic Sensor API: This specification defines a framework for exposing sensor data to the Open Web Platform in a consistent way. Covers Generic Sensor API (build), Accelerometer (build), Gyroscope (build), Magnetometer (track), Orientation Sensor (track), Ambient Light Sensor (track), Proximity Sensor (track). Use when reading motion or environment sensors. Triggers: Generic Sensor, Accelerometer, Gyroscope.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Generic Sensor API

This specification defines a framework for exposing sensor data to the Open Web Platform in a consistent way. It does so by defining a blueprint for writing specifications of concrete sensors along with an abstract Sensor interface that can be extended to accommodate different sensor types.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading motion or environment sensors.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Generic Sensor API (default, posture build); Accelerometer (default, posture build); Gyroscope (default, posture build); Magnetometer (default, posture track); Orientation Sensor (default, posture track); Ambient Light Sensor (default, posture track); Proximity Sensor (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **2. Scope.** "This should have little to no effects on implementations, however."
3. **4. Security and privacy considerations.** "Web application developers using these JavaScript APIs should consider how this information might be correlated with other information and the privacy risks that might be created."
4. **4. Security and privacy considerations.** "The potential risks of collection of such data over a longer period of time should also be considered."
5. **4. Security and privacy considerations.** "User agents should not provide unnecessarily verbose readouts of sensors data."
6. **4. Security and privacy considerations.** "Each sensor type should be assessed individually."
7. **4. Security and privacy considerations.** "User agents should consider providing the user an indication of when the sensor is used and allowing the user to disable it."
8. **4. Security and privacy considerations.** "Web application developers that use sensors should perform a privacy impact assessment of their application taking all aspects of their application into consideration."

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

- [Generic Sensor API](https://www.w3.org/TR/generic-sensor/): Candidate Recommendation Draft, generic-sensor CRD-generic-sensor-20260514 (Candidate Recommendation Draft, 2026-05-14), checked 2026-10-06.
- [Accelerometer](https://www.w3.org/TR/accelerometer/): Candidate Recommendation Draft, accelerometer CRD-accelerometer-20260514 (Candidate Recommendation Draft, 2026-05-14), checked 2026-10-06.
- [Gyroscope](https://www.w3.org/TR/gyroscope/): Candidate Recommendation Draft, gyroscope CRD-gyroscope-20260514 (Candidate Recommendation Draft, 2026-05-14), checked 2026-10-06.
- [Magnetometer](https://www.w3.org/TR/magnetometer/): Working Draft, magnetometer WD-magnetometer-20260514 (Working Draft, 2026-05-14), checked 2026-10-06.
- [Orientation Sensor](https://www.w3.org/TR/orientation-sensor/): Working Draft, orientation-sensor WD-orientation-sensor-20260514 (Working Draft, 2026-05-14), checked 2026-10-06.
- [Ambient Light Sensor](https://www.w3.org/TR/ambient-light/): Working Draft, ambient-light WD-ambient-light-20260514 (Working Draft, 2026-05-14), checked 2026-10-06.
- [Proximity Sensor](https://www.w3.org/TR/proximity/): Working Draft, proximity WD-proximity-20260514 (Working Draft, 2026-05-14), checked 2026-10-06.
