---
name: sparql
description: >-
  SPARQL: query and update RDF graphs with the SPARQL query language, protocol and update language. Covers SPARQL 1.1 Query Language, SPARQL 1.1 Protocol, SPARQL 1.1 Update, SPARQL 1.2 Query Language, SPARQL 1.2 Protocol and SPARQL 1.2 Update. Use when querying RDF with SPARQL. Triggers: SPARQL 1.1, SPARQL 1.2.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.1"
  kind: standard
---

# SPARQL

RDF is a directed, labeled graph data format for representing information in the Web. This specification defines the syntax and semantics of the SPARQL query language for RDF. SPARQL can be used to express queries across diverse data sources, whether the data is stored natively as RDF or viewed as RDF via middleware. SPARQL contains capabilities for querying required and optional graph patterns along with their conjunctions and disjunctions. SPARQL also supports aggregation, subqueries, negation, creating values by expressions, extensible value testing, and constraining queries by source RDF graph. The results of SPARQL queries can be result sets or RDF graphs.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when querying RDF with SPARQL.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: SPARQL 1.1 Query Language (default); SPARQL Query Language for RDF (legacy: read and upgrade, never author); SPARQL 1.1 Protocol (default); SPARQL Protocol for RDF (legacy: read and upgrade, never author); SPARQL 1.1 Update (default). SPARQL 1.2 Query Language, SPARQL 1.2 Protocol and SPARQL 1.2 Update are Working Draft previews (posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.2 Multiple Matches.** "This is a basic graph pattern match ; all the variables used in the query pattern must be bound in every solution."
2. **2.4 Blank Node Labels in Query Results.** "An application writer should not expect blank node labels in a query to refer to a particular blank node in the data."
3. **5 Graph Patterns.** "More complex graph patterns can be formed by combining smaller patterns in various ways: Basic Graph Patterns , where a set of triple patterns must match Group Graph Pattern , where a set of graph patterns must all match Optional Graph patterns , where additional patterns may extend the solution Alternative Graph Pattern , where two or more possible patterns are tried Patterns on Named Graphs ,…"
4. **6 Including Optional Values.** "Basic graph patterns allow applications to make queries where the entire query pattern must match for there to be a solution."
5. **6.1 Optional Pattern Matching.** "The entire optional graph pattern must match for the optional graph pattern to affect the query solution."
6. **10.1 BIND: Assigning to Variables.** "The variable introduced by the BIND clause must not have been used in the group graph pattern up to the point of use in BIND ."
7. **11.1 Aggregate Example.** "It should be noted that as per functions , aggregate expressions are required to be aliased (again, similar to the BIND clause, using the keyword AS ) in order to project them from queries or subqueries."
8. **13.2 Specifying RDF Datasets.** "The FROM and FROM NAMED keywords allow a query to specify an RDF dataset by reference; they indicate that the dataset should include graphs that are obtained from representations of the resources identified by the given IRIs (i.e."

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

- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/): Recommendation, sparql11-query REC-sparql11-query-20130321 (Recommendation, 2013-03-21), checked 2026-10-06.
- [SPARQL Query Language for RDF](https://www.w3.org/TR/rdf-sparql-query/): Recommendation, sparql10-query REC-rdf-sparql-query-20080115 (Recommendation, 2008-01-15), checked 2026-10-06.
- [SPARQL 1.1 Protocol](https://www.w3.org/TR/sparql11-protocol/): Recommendation, sparql11-protocol REC-sparql11-protocol-20130321 (Recommendation, 2013-03-21), checked 2026-10-06.
- [SPARQL Protocol for RDF](https://www.w3.org/TR/rdf-sparql-protocol/): Recommendation, sparql10-protocol REC-rdf-sparql-protocol-20080115 (Recommendation, 2008-01-15), checked 2026-10-06.
- [SPARQL 1.1 Update](https://www.w3.org/TR/sparql11-update/): Recommendation, sparql11-update REC-sparql11-update-20130321 (Recommendation, 2013-03-21), checked 2026-10-06.
- [SPARQL 1.2 Query Language](https://www.w3.org/TR/sparql12-query/): Working Draft, W3C Working Draft 04 October 2026, checked 2026-10-06.
- [SPARQL 1.2 Protocol](https://www.w3.org/TR/sparql12-protocol/): Working Draft, W3C Working Draft 23 July 2026, checked 2026-10-06.
- [SPARQL 1.2 Update](https://www.w3.org/TR/sparql12-update/): Working Draft, W3C Working Draft 12 June 2026, checked 2026-10-06.
