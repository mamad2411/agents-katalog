---
name: presentation-exchange
description: >-
  Presentation Exchange 2.1: request verifiable credentials with presentation definitions and answer with presentation submissions. Covers Presentation Exchange 2.1.1, Presentation Exchange 2.1.0 (supported). Use when requesting and submitting verifiable presentations. Triggers: Presentation Exchange, presentation_definition.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Presentation Exchange

specification and not yet on a standards track, the concept of “decentralized web nodes”

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when requesting and submitting verifiable presentations.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Presentation Exchange 2.1.1 (default); Presentation Exchange 2.1.0 (supported). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ Presentation Definition.** "Any properties that are not defined below MUST be ignored, unless otherwise specified by a Feature ; id - The Presentation Definition * _MUST_* contain an id property."
2. **§ Presentation Definition.** "The value of this property * _MUST_* be a string."
3. **§ Presentation Definition.** "The string * _SHOULD_* provide a unique ID for the desired context."
4. **§ Presentation Definition.** "The id property * _SHOULD_* be unique within the Presentation Definition itself, meaning no other id values should exist at any level with the same value."
5. **§ Presentation Definition.** "input_descriptors - The Presentation Definition * _MUST_* contain an input_descriptors property."
6. **§ Presentation Definition.** "Its value * _MUST_* be an array of Input Descriptor Objects , the composition of which are described in the Input Descriptors section below."
7. **§ Presentation Definition.** "If present, its value * _SHOULD_* be a human-friendly string intended to constitute a distinctive designation of the Presentation Definition ."
8. **§ Presentation Definition.** "If present, its value * _MUST_* be a string that describes the purpose for which the Presentation Definition 's inputs are being used for."

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

- [Presentation Exchange 2.1.1](https://identity.foundation/presentation-exchange/spec/v2.1.1/): DIF specification, Presentation Exchange v2.1.1, fetched 2026-10-06 (DIF specification, 2026-10-06), checked 2026-10-06.
- [Presentation Exchange 2.1.0](https://identity.foundation/presentation-exchange/spec/v2.1.0/): DIF specification, Presentation Exchange v2.1.0, fetched 2026-10-06 (DIF specification, 2026-10-06), checked 2026-10-06.
