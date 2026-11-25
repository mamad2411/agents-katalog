---
name: device-memory
description: >-
  Device Memory API: This document defines a HTTP Client Hint header and a JavaScript API to surface device capability for memory (device RAM) in order to enable web apps to customize content depending on device memory constraints. Covers Device Memory API Level 1 (track). Use when reading approximate device memory. Triggers: deviceMemory, Device Memory.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Device Memory API

This document defines a HTTP Client Hint header and a JavaScript API to surface device capability for memory (device RAM) in order to enable web apps to customize content depending on device memory constraints.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading approximate device memory.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Device Memory API Level 1 (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **2. Computing device memory value.** "The range between the upper and the lower bounds should include the majority of device memory values but exclude rare device memory values to mitigate device fingerprinting."
3. **3. Sec - CH - Device - Memory (Client Hint) Header Field.** "The ABNF (Augmented Backus-Naur Form) syntax for the `Sec - CH - Device - Memory` header field is as follows: Sec-CH-Device-Memory = sf-decimal The `Sec - CH - Device - Memory`'s value should be set to the user agent ’s deviceMemory ."
4. **4.1. JavaScript examples.** "Note: The web application should consider how to handle browsers that do not support the API: either by enabling by default, or disabling by default."
5. **5. Security & privacy considerations.** "These bounds should be reviewed over time as commonly used device memory characteristics change."
6. **5. Security & privacy considerations.** "Device type should be taken into account when defining these bounds since mobile devices typically have different characteristics than desktops and laptops."
7. **Conformant Algorithms.** "Requirements phrased in the imperative as part of algorithms (such as "strip any leading space characters" or "return false and abort these steps") are to be interpreted with the meaning of the key word ("must", "should", "may", etc) used in introducing the algorithm."

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

- [Device Memory API](https://www.w3.org/TR/device-memory-1/): Working Draft, device-memory-1 WD-device-memory-1-20260330 (Working Draft, 2026-03-30), checked 2026-10-06.
