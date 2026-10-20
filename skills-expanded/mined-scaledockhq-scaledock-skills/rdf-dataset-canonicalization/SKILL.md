---
name: rdf-dataset-canonicalization
description: >-
  RDF Dataset Canonicalization (RDFC-1.0): RDF [ RDF11-CONCEPTS ] describes a graph-based data model for making claims about the world and provides the foundation for reasoning upon that graph of information. Covers RDF Dataset Canonicalization. Use when canonicalizing an RDF dataset for hashing or data integrity. Triggers: RDFC-1.0, RDF dataset canonicalization, URDNA2015.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# RDF Dataset Canonicalization (RDFC-1.0)

RDF [ RDF11-CONCEPTS ] describes a graph-based data model for making claims about the world and provides the foundation for reasoning upon that graph of information. At times, it becomes necessary to compare the differences between sets of graphs, digitally sign them, or generate short identifiers for graphs via hashing algorithms. This document outlines an algorithm for normalizing RDF datasets such that these operations can be performed.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when canonicalizing an RDF dataset for hashing or data integrity.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RDF Dataset Canonicalization (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words MUST , MUST NOT , and SHOULD in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **2. Conformance.** "The algorithms in this specification are normative, because to consistently reproduce the same canonical identifiers, implementations MUST strictly conform to the steps outlined in these algorithms."
3. **3.1 Terms defined by this specification.** "Implementations MUST support a parameter to define the hash algorithm , MUST support SHA-256 and SHA-384 [ FIPS-180-4 ], and SHOULD support the ability to specify other hash algorithms."
4. **4.4.3 Algorithm.** "Implementations MUST defend against potential denial-of-service attacks by raising suitable exceptions and terminating early."
5. **5. Serialization.** "When serializing quads in canonical n-quads form , components which are blank nodes MUST be serialized using the canonical label associated with each blank node from the issued identifiers map component of the canonicalized dataset ."
6. **A. A Canonical form of N-Quads.** "Canonical N-Quads has the following additional constraints on layout: White space MUST NOT be used except after subject , predicate , object , and graphLabel , each of which MUST be a single space (code point U+0020 )."
7. **A. A Canonical form of N-Quads.** "Literals with the datatype http://www.w3.org/2001/XMLSchema#string MUST NOT use the datatype IRI part of the literal , and are represented using only STRING_LITERAL_QUOTE ."
8. **A. A Canonical form of N-Quads.** "HEX MUST use only digits ( [0-9] ) and uppercase letters ( [A-F] )."

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

- [RDF Dataset Canonicalization](https://www.w3.org/TR/rdf-canon/): Recommendation, rdf-canon REC-rdf-canon-20240521 (Recommendation, 2024-05-21), checked 2026-10-06.
