---
name: multimodal-architecture
description: >-
  Multimodal Architecture: This document describes a loosely coupled architecture for multimodal user interfaces, which allows for co-resident and distributed implementations, and focuses on the role of markup and scripting, and the use of well defined interfaces between its constituents. Covers Multimodal Architecture and Interfaces. Use when composing a multimodal interaction. Triggers: MMI Architecture.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Multimodal Architecture

This document describes a loosely coupled architecture for multimodal user interfaces, which allows for co-resident and distributed implementations, and focuses on the role of markup and scripting, and the use of well defined interfaces between its constituents.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when composing a multimodal interaction.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Multimodal Architecture and Interfaces (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1 Conformance.** "The key words MUST , MUST NOT , REQUIRED , SHALL , SHALL NOT , SHOULD , SHOULD NOT , RECOMMENDED , MAY , and OPTIONAL in this specification are to be interpreted as described in [IETF RFC 2119] ."
2. **5.2.1 The Interaction.** "Manager All life-cycle events that the Modality Components generate MUST be delivered to the Interaction Manager."
3. **5.2.1 The Interaction.** "All life-cycle events that are delivered to Modality Components MUST be sent by the Interaction Manager."
4. **5.2.1 The Interaction.** "If the Interaction Manager does not contain an explicit handler for an event, it MUST respect any default behavior that has been established for the event."
5. **5.2.1 The Interaction.** "If there is no default behavior, the Interaction Manager MUST ignore the event."
6. **5.2.4.1 The Event Transport.** "We place the following requirements on all transport mechanisms: Events MUST be delivered reliably."
7. **5.2.4.1 The Event Transport.** "In particular, the event delivery mechanism MUST report an error if an event can not be delivered, for example if the destination endpoint is unavailable."
8. **5.2.4.1 The Event Transport.** "Events MUST be delivered to the destination in the order in which the source generated them."

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

- [Multimodal Architecture and Interfaces](https://www.w3.org/TR/mmi-arch/): Recommendation, mmi-arch REC-mmi-arch-20121025 (Recommendation, 2012-10-25), checked 2026-10-06.
