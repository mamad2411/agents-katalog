---
name: rdf
description: >-
  RDF: The Resource Description Framework (RDF) is a framework for representing information in the Web. Covers RDF 1.1 Concepts and Abstract Syntax, RDF 1.2 Concepts and Abstract Data Model (build preview), RDF 1.1 N-Triples, RDF 1.2 N-Triples (track preview), RDF 1.1 N-Quads, RDF 1.2 N-Quads (track preview). Use when modeling or serializing RDF. Triggers: RDF 1.1, RDF 1.2.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# RDF

The Resource Description Framework (RDF) is a framework for representing information in the Web. This document defines an abstract syntax (a data model) which serves to link all RDF-based languages and specifications. The abstract syntax has two key data structures: RDF graphs are sets of subject-predicate-object triples, where the elements may be IRIs, blank nodes, or datatyped literals. They are used to express descriptions of resources. RDF datasets are used to organize collections of RDF graphs, and comprise a default graph and zero or more named graphs. RDF 1.1 Concepts and Abstract Syntax also introduces key concepts and terminology, and discusses datatyping and the handling of fragmen

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when modeling or serializing RDF.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RDF 1.1 Concepts and Abstract Syntax (default); RDF 1.2 Concepts and Abstract Data Model (preview, posture build: emit only when the user opts in and the posture is build); Resource Description Framework (RDF): Concepts and Abstract Syntax Level 10 (legacy: read and upgrade, never author); RDF 1.1 N-Triples (default); RDF 1.2 N-Triples (preview, posture track: emit only when the user opts in and the posture is build); RDF 1.1 N-Quads (default); RDF 1.2 N-Quads (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words MUST , MUST NOT , REQUIRED , SHOULD , SHOULD NOT , RECOMMENDED , MAY , and OPTIONAL in this specification are to be interpreted as described in [ RFC2119 ]."
2. **3.2 IRIs.** "IRIs in the RDF abstract syntax MUST be absolute, and MAY contain a fragment identifier."
3. **3.2 IRIs.** "Further normalization MUST NOT be performed when comparing IRIs for equality."
4. **3.3 Literals.** "A literal in an RDF graph consists of two or three elements: a lexical form , being a Unicode [ UNICODE ] string, which SHOULD be in Normal Form C [ NFC ], a datatype IRI , being an IRI identifying a datatype that determines how the lexical form maps to a literal value , and if and only if the datatype IRI is http://www.w3.org/1999/02/22-rdf-syntax-ns#langString , a non-empty language tag as defined by [ BCP47 ]."
5. **3.3 Literals.** "The language tag MUST be well-formed according to section 2.2.9 of [ BCP47 ]."
6. **3.3 Literals.** "Implementations MUST accept ill-typed literals and produce RDF graphs from them."
7. **3.5 Replacing Blank Nodes with IRIs.** "Systems wishing to do this SHOULD mint a new, globally unique IRI (a Skolem IRI ) for each blank node so replaced."
8. **3.5 Replacing Blank Nodes with IRIs.** "Systems that want Skolem IRIs to be recognizable outside of the system boundaries SHOULD use a well-known IRI [ RFC5785 ] with the registered name genid ."

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

- [RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/): Recommendation, rdf11-concepts REC-rdf11-concepts-20140225 (Recommendation, 2014-02-25), checked 2026-10-06.
- [RDF 1.2 Concepts and Abstract Data Model](https://www.w3.org/TR/rdf12-concepts/): Candidate Recommendation Snapshot, rdf12-concepts REC-rdf12-concepts-20140225 (Candidate Recommendation Snapshot, 2026-04-07), checked 2026-10-06.
- [Resource Description Framework (RDF): Concepts and Abstract Syntax](https://www.w3.org/TR/rdf-concepts/): Recommendation, rdf-concepts-10 REC-rdf11-concepts-20140225 (Recommendation, 2004-02-10), checked 2026-10-06.
- [RDF 1.1 N-Triples](https://www.w3.org/TR/n-triples/): Recommendation, rdf11-n-triples REC-n-triples-20140225 (Recommendation, 2014-02-25), checked 2026-10-06.
- [RDF 1.2 N-Triples](https://www.w3.org/TR/rdf12-n-triples/): Working Draft, rdf12-n-triples WD-rdf12-n-triples-20260723 (Working Draft, 2026-09-24), checked 2026-10-06.
- [RDF 1.1 N-Quads](https://www.w3.org/TR/n-quads/): Recommendation, rdf11-n-quads REC-n-quads-20140225 (Recommendation, 2014-02-25), checked 2026-10-06.
- [RDF 1.2 N-Quads](https://www.w3.org/TR/rdf12-n-quads/): Working Draft, rdf12-n-quads WD-rdf12-n-quads-20260612 (Working Draft, 2026-07-23), checked 2026-10-06.
