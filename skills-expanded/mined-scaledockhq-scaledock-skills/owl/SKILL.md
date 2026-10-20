---
name: owl
description: >-
  OWL 2: The OWL 2 Web Ontology Language, informally OWL 2, is an ontology language for the Semantic Web with formally defined meaning. Covers OWL 2 Web Ontology Language Structural Specification and Functional-Style Syntax (Second Edition), OWL 2 Web Ontology Language Direct Semantics (Second Edition), OWL 2 Web Ontology Language Document Overview (Second Edition). Use when writing an OWL ontology. Triggers: OWL 2, Web Ontology Language.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OWL 2

The OWL 2 Web Ontology Language, informally OWL 2, is an ontology language for the Semantic Web with formally defined meaning. OWL 2 ontologies provide classes, properties, individuals, and data values and are stored as Semantic Web documents. OWL 2 ontologies can be used along with information written in RDF, and OWL 2 ontologies themselves are primarily exchanged as RDF documents. The OWL 2 Document Overview describes the overall state of OWL 2, and should be read before other OWL 2 documents. The meaningful constructs provided by OWL 2 are defined in terms of their structure. As well, a functional-style syntax is defined for these constructs, with examples and informal descriptions. One c

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when writing an OWL ontology.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: OWL 2 Web Ontology Language Structural Specification and Functional-Style Syntax (Second Edition) (default); OWL 2 Web Ontology Language Direct Semantics (Second Edition) (default); OWL 2 Web Ontology Language Document Overview (Second Edition) (default). OWL Web Ontology Language Semantics and Abstract Syntax is legacy: the 10 February 2004 Recommendation says OWL 2 is the new version. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1 Introduction.** "The italicized keywords MUST , MUST NOT , SHOULD , SHOULD NOT , and MAY are used to specify normative features of OWL 2 documents and tools, and are interpreted as specified in RFC 2119 [ RFC 2119 ]."
2. **2.1 Structural Specification.** "Duplicates SHOULD be eliminated when ontology documents written in such syntaxes are converted into instances of the UML classes of the structural specification."
3. **2.2 BNF Notation.** "The following characters are called delimiters : = (U+3D) ( (U+28) ) (U+29) < (U+3C) > (U+3E) @ (U+40) ^ (U+5E) Given an input sequence of characters, an OWL 2 implementation MUST exhibit the same observable behavior as if it applied the BNF grammar rules to the sequence of terminal symbols obtained from the input as follows."
4. **2.2 BNF Notation.** "If there is no match, the input SHOULD be rejected."
5. **2.2 BNF Notation.** "If there is no match, the input SHOULD be rejected; otherwise, p is moved to the first character after the match (and thus the match is discarded)."
6. **2.3 Integers, Characters, Strings, Language Tags, and Node IDs.** "Each character MUST match the Char production from XML [ XML ]."
7. **2.4 IRIs.** "Each IRI MUST be absolute (i.e., not relative)."
8. **2.4 IRIs.** "If a concrete syntax uses this IRI abbreviation mechanism, it SHOULD provide a suitable mechanism for declaring prefix names."

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

- [OWL 2 Web Ontology Language Structural Specification and Functional-Style Syntax (Second Edition)](https://www.w3.org/TR/owl2-syntax/): Recommendation, owl2-syntax REC-owl2-syntax-20121211 (Recommendation, 2012-12-11), checked 2026-10-06.
- [OWL 2 Web Ontology Language Direct Semantics (Second Edition)](https://www.w3.org/TR/owl2-direct-semantics/): Recommendation, owl2-direct-semantics REC-owl2-direct-semantics-20121211 (Recommendation, 2012-12-11), checked 2026-10-06.
- [OWL 2 Web Ontology Language Document Overview (Second Edition)](https://www.w3.org/TR/owl2-overview/): Recommendation, owl2-overview REC-owl2-overview-20121211 (Recommendation, 2012-12-11), checked 2026-10-06.
- [OWL Web Ontology Language Semantics and Abstract Syntax](https://www.w3.org/TR/owl-semantics/): Recommendation, W3C Recommendation 10 February 2004, checked 2026-10-06.
