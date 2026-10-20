---
name: web-midi
description: >-
  Web MIDI API: Some user agents have music devices, such as synthesizers, keyboard and other controllers, and drum machines connected to their host computer or device. Covers Web MIDI API (track). Use when talking to MIDI devices. Triggers: Web MIDI, MIDIAccess.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Web MIDI API

Some user agents have music devices, such as synthesizers, keyboard and other controllers, and drum machines connected to their host computer or device. The widely adopted Musical Instrument Digital Interface (MIDI) protocol enables electronic musical instruments, controllers and computers to communicate and synchronize with each other. MIDI does not transmit audio signals: instead, it sends event messages about musical notes, controller signals for parameters such as volume, vibrato and panning, cues and clock signals to set the tempo, and system-specific MIDI communications (e.g. to remotely store synthesizer-specific patch data). This same protocol has become a standard for non-musical us

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when talking to MIDI devices.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Web MIDI API (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words MUST and SHOULD in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **2. Conformance.** "Implementations that use ECMAScript to implement the APIs defined in this specification MUST implement them in a manner consistent with the ECMAScript Bindings defined in the Web IDL specification [ WEBIDL ], as this specification uses that specification and terminology."
3. **4.3.** "Requesting MIDI access SHOULD prompt the user for access to MIDI devices, particularly if System Exclusive access is requested."
4. **4.3.** "When the requestMIDIAccess () method is called, the user agent MUST run the following steps: Let promise be a new Promise object and resolver be its associated resolver."
5. **5.3.** "This event handler , of type MIDIConnectionEvent , MUST be supported by all objects implementing the MIDIAccess interface."
6. **5.3.** "Whenever a previously unavailable MIDI port becomes available for use, or an existing port changes the state attribute, the user agent SHOULD run the following steps: Let port be the MIDIPort corresponding to the newly-available, or the existing port."
7. **5.4.** "The User Agent MUST ensure that the id is unique to only that port."
8. **5.4.** "The User Agent SHOULD ensure that the id is maintained across instances of the application - e.g., when the system is rebooted - and when a device is removed from the system."

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

- [Web MIDI API](https://www.w3.org/TR/webmidi/): Working Draft, webmidi WD-webmidi-20250121 (Working Draft, 2025-01-21), checked 2026-10-06.
