---
name: amqp
description: >-
  AMQP 1.0: exchange messages over the OASIS Advanced Message Queuing Protocol with its type system, links and transfers. Covers AMQP 1.0. Use when exchanging messages with AMQP 1.0. Triggers: AMQP.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# AMQP

OASIS Advanced Message Queuing Protocol (AMQP) Version 1.0, Part 0: Overview OASIS Advanced Message Queuing Protocol (AMQP) Version 1.0

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when exchanging messages with AMQP 1.0.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: AMQP 1.0 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **← 0.1 Introduction.** "Every compliant AMQP process MUST be able to send and receive messages in this standard encoding."
2. **← 0.1.1 Terminology.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this specification are to be interpreted as described in IETF RFC 2119 [ RFC2119 ]."
3. **← 0.2 Conformance.** "A conformant implementation MUST perform protocol negotiation (see section 2.2 ), and then parse, process, and produce frames in accordance with the format and semantics defined in parts 1 through 5 of this specification."
4. **← 0.2 Conformance.** "Conformant implementations MUST NOT require the use of any extensions defined outside this document in order to interoperate with any other conformant implementation."
5. **← 0.2 Conformance.** "Part 1 of this document defines the type system and type encodings that every conformant implementation MUST implement."
6. **← 0.2 Conformance.** "Every conformant implementation of AMQP over TCP MUST implement Part 2."
7. **← 0.2 Conformance.** "A conformant implementation MUST implement Part 2 or a mapping of AMQP to some non-TCP protocol."
8. **← 0.2 Conformance.** "Where an implementation does not allow for a behavior the implementation MUST respond according to the rules defined within Part 2 of the specification."

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

- [AMQP 1.0](https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-overview-v1.0-os.html): OASIS Standard, AMQP 1.0 overview, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.
