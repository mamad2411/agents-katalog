---
name: exi
description: >-
  Efficient XML Interchange: This document is the specification of the Efficient XML Interchange (EXI) format. Covers Efficient XML Interchange (EXI) Format 1.0 (Second Edition), Efficient XML Interchange (EXI) Profile for limiting usage of dynamic memory, Canonical EXI. Use when encoding XML as EXI. Triggers: EXI.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Efficient XML Interchange

This document is the specification of the Efficient XML Interchange (EXI) format. EXI is a very compact representation for the Extensible Markup Language (XML) Information Set that is intended to simultaneously optimize performance and the utilization of computational resources. The EXI format uses a hybrid approach drawn from the information and formal language theories, plus practical techniques verified by measurements, for entropy encoding XML information. Using a relatively simple algorithm, which is amenable to fast and compact implementation, and a small set of datatype representations, it reliably produces efficient encodings of XML event streams. The grammar production system and fo

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when encoding XML as EXI.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Efficient XML Interchange (EXI) Format 1.0 (Second Edition) (default); Efficient XML Interchange (EXI) Profile for limiting usage of dynamic memory (default); Canonical EXI (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.2 Notational Conventions and Terminology.** "The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL, when they appear EMPHASIZED in this document, are to be interpreted as described in RFC 2119 [IETF RFC 2119] ."
2. **4. EXI Streams.** "The uri of a NS event with its local-element-ns flag set to true MUST match the uri of the associated SE event."
3. **4. EXI Streams.** "As prescribed by Table B-2 and Table B-11 , [namespace attributes] representing namespace declarations are mapped to NS events and SHOULD NOT be represented by AT events."
4. **4. EXI Streams.** "This also implies that the following AT events SHOULD NOT occur in EXI streams: (1) AT events with qname whose uri is "http://www.w3.org/2000/xmlns/"; (2) AT events with qname which has empty uri ("") and local name either of the form "xmlns" or "xmlns:_", where "_" represents a string with 0 or more characters."
5. **5.2 Distinguishing Bits.** "1 0 Unlike the optional EXI cookie that MAY occur to precede this field, the presence of Distinguishing Bits is REQUIRED in the EXI header."
6. **5.3 EXI Format Version.** "An EXI processor that implements a final version of the EXI format specification is REQUIRED to process EXI streams that have a version field with its first bit set to 0 followed by a version number that corresponds to the version of the EXI specification the processor implements."
7. **5.3 EXI Format Version.** "EXI processors conforming with the final version of this specification MUST use the 5-bit value 0 0000 as the version number."
8. **5.4 EXI Options.** "When EXI Options are present in the header, an EXI Processor MUST observe the specified options to process the EXI stream that follows."

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

- [Efficient XML Interchange (EXI) Format 1.0 (Second Edition)](https://www.w3.org/TR/exi/): Recommendation, exi REC-exi-20140211 (Recommendation, 2014-02-11), checked 2026-10-06.
- [Efficient XML Interchange (EXI) Profile for limiting usage of dynamic memory](https://www.w3.org/TR/exi-profile/): Recommendation, exi-profile REC-exi-profile-20140909 (Recommendation, 2014-09-09), checked 2026-10-06.
- [Canonical EXI](https://www.w3.org/TR/exi-c14n/): Recommendation, exi-c14n REC-exi-c14n-20180607 (Recommendation, 2018-06-07), checked 2026-10-06.
