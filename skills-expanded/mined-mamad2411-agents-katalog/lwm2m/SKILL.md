---
name: lwm2m
description: >-
  LwM2M: the OMA Lightweight M2M core protocol for device management. Covers
  LwM2M 1.2. Use when managing a device with LwM2M.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# LwM2M

OMA Lightweight M2M Core, approved version 1.2.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when managing a device with LwM2M.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: LwM2M 1.2 (default). See `references/versions.md`.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **3.1. Conventions.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC2119]."
2. **5.1.2. Attributes Classification.** "The LwM2M Server and LwM2M Client SHOULD support Table: 5.1.2.-1 Class Attributes , except when specifically mentioned as not required."
3. **5.1.2. Attributes Classification.** "Additionally, the following rules MUST be considered: a "Maximum Period" (pmax) applied to a Resource that is smaller than the "Minimum Period" applied to the same Resource MUST be ignored for that Resource, the "Change Value Conditions" are considered as valid, if the two following rules related to the Attributes defined in the table below ("Greater Than", "Less Than", "Step") are respected:"
4. **5.1.2. Attributes Classification.** "("lt" value < "gt" value) ("lt" value + 2*"st" values <"gt" value) When the "Change Value Conditions" Attributes are set in a single Write-Attributes operation, the operation MUST be rejected when the rules above are violated."
5. **5.1.2. Attributes Classification.** "After the expiry of epmax, the device MUST perform an evaluation per the "Notification Conditions"."
6. **5.1.2. Attributes Classification.** "The behaviour of Notification class attributes MUST follow [DynLink] unless stated otherwise in this specification."
7. **5.1.2. Attributes Classification.** "The LwM2M Server MUST support and LwM2M Client SHOULD support all the <NOTIFICATION> Class Attributes listed in Table: 5.1.2.-2 class Attributes ."
8. **5.1.2. Attributes Classification.** "Table: 5.1.2.-2 <NOTIFICATION> class Attributes Attribute Name CoRE Link param Attachment Assignation Level Required Access Mode Value Type Default Value Apply Condition Minimum Period "pmin" "=" 1*DIGIT Resource Resource Resource Instance Object Object Instance No RW Integer 0 (sec) Readable Resource Notes: The Minimum Period Attribute indicates the minimum time in seconds the LwM2M Client MUST…"

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> `references/versions.md`
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in `references/requirements.md` and implement each one that applies to the role.
   -> `references/requirements.md`
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> `references/versions.md`
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in `references/requirements.md` holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [LwM2M 1.2](https://www.openmobilealliance.org/release/LightweightM2M/V1_2-20201110-A/HTML-Version/OMA-TS-LightweightM2M_Core-V1_2-20201110-A.html): Approved, OMA-TS-LightweightM2M_Core-V1_2-20201110-A (Approved, 2026-10-06), checked 2026-10-06.
