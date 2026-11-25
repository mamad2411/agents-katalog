---
name: battery-status
description: >-
  Battery Status API: This specification defines an API that provides information about the battery status of the hosting device. Covers Battery Status API (track). Use when reading battery charge. Triggers: Battery Status, navigator.getBattery.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Battery Status API

This specification defines an API that provides information about the battery status of the hosting device.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading battery charge.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Battery Status API (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words MAY , MUST , and SHOULD in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **3..** "The user agent SHOULD not expose high precision readouts of battery status information as that can introduce a new fingerprinting vector."
3. **3..** "The user agent SHOULD inform the user of the API use by scripts in an unobtrusive manner to aid transparency and to allow the user to revoke the API access."
4. **6.1.1.** "It MUST be set to false if the battery is discharging, and set to true if the battery is charging, the implementation is unable to report the state, or there is no battery attached to the system, or otherwise."
5. **6.1.2.** "It MUST be set to 0 if the battery is full or there is no battery attached to the system, and to the value positive Infinity if the battery is discharging, the implementation is unable to report the remaining charging time, or otherwise."
6. **6.1.3.** "It MUST be set to the value positive Infinity if the battery is charging, the implementation is unable to report the remaining discharging time, there is no battery attached to the system, or otherwise."
7. **6.1.4.** "It MUST be set to 0 if the system's battery is depleted and the system is about to be suspended, and to 1.0 if the battery is full, the implementation is unable to report the battery's level, or there is no battery attached to the system."
8. **6.6.** "Event handlers The following are the event handlers (and their corresponding event handler event types ) that MUST be supported as attributes by the BatteryManager object: event handler event handler event type onchargingchange chargingchange onchargingtimechange chargingtimechange ondischargingtimechange dischargingtimechange onlevelchange levelchange"

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

- [Battery Status API](https://www.w3.org/TR/battery-status/): Working Draft, battery-status WD-battery-status-20241024 (Working Draft, 2024-10-24), checked 2026-10-06.
