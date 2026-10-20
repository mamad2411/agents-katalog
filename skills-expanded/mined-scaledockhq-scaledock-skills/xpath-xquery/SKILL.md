---
name: xpath-xquery
description: >-
  XPath and XQuery: XPath 3.1 is an expression language that allows the processing of values conforming to the data model defined in [XQuery and XPath Data Model (XDM) 3.1] . Covers XML Path Language (XPath) 3.1, XML Path Language (XPath) 3.0 (supported), XQuery 4.0 (track preview), XQuery 3.1: An XML Query Language, XQuery 3.0: An XML Query Language (supported), XPath and XQuery Functions and Operators 3.1, XQuery and XPath Data Model 3.1, XQueryX 3.1, XQuery and XPath Full Text 3.0. Use when querying XML with XPath or XQuery. Triggers: XPath 3.1, XQuery 3.1.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# XPath and XQuery

XPath 3.1 is an expression language that allows the processing of values conforming to the data model defined in [XQuery and XPath Data Model (XDM) 3.1] . The name of the language derives from its most distinctive feature, the path expression, which provides a means of hierarchic addressing of the nodes in an XML tree. As well as modeling the tree structure of XML, the data model also includes atomic values, function items, and sequences. This version of XPath supports JSON as well as XML, adding maps and arrays to the data model and supporting them with new expressions in the language and new functions in [XQuery and XPath Functions and Operators 3.1] . These are the most important new feat

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when querying XML with XPath or XQuery.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: XML Path Language (XPath) 3.1 (default); XML Path Language (XPath) 3.0 (supported); XQuery 4.0 (preview, posture track: emit only when the user opts in and the posture is build); XQuery 3.1: An XML Query Language (default); XQuery 3.0: An XML Query Language (supported); XPath and XQuery Functions and Operators 3.1 (default); XQuery and XPath Data Model 3.1 (default); XQueryX 3.1 (default); XQuery and XPath Full Text 3.0 (default). XPath 1.0, XPath 2.0, XQuery 1.0 and XQuery and XPath Full Text 1.0 are legacy. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4 Conformance.** "[ Definition : MUST means that the item is an absolute requirement of the specification.] [ Definition : MUST NOT means that the item is an absolute prohibition of the specification.] [ Definition : MAY means that an item is truly optional.] XPath is intended primarily as a component that can be used by other specifications."
2. **4 Conformance.** "Specifications that set conformance criteria for their use of XPath MUST NOT change the syntactic or semantic definitions of XPath as given in this specification, except by subsetting and/or compatible extensions."
3. **4 Conformance.** "If a language is described as an extension of XPath, then every expression that conforms to the XPath grammar MUST behave as described in this specification."
4. **G Glossary (Non-Normative).** "must MUST means that the item is an absolute requirement of the specification."
5. **G Glossary (Non-Normative).** "must not MUST NOT means that the item is an absolute prohibition of the specification."
6. **I.2.2 Editorial Changes.** "Modified 4 Conformance to use the term MUST NOT ."
7. **W3C Recommendation 21 March 2017.** "Status Update (6 April 2021): Feedback, comments, error reports on this specification should be sent via GitHub https://github.com/w3c/qtspecs/issues or email to public-qt-comments@w3.org ."
8. **1 Introduction.** "")" The productions should be read as follows: A function call consists of an EQName followed by an ArgumentList ."

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

- [XML Path Language (XPath) 3.1](https://www.w3.org/TR/xpath-31/): Recommendation, xpath-31 REC-xpath-31-20170321 (Recommendation, 2017-03-21), checked 2026-10-06.
- [XML Path Language (XPath) 3.0](https://www.w3.org/TR/xpath-30/): Recommendation, xpath-30 REC-xpath-30-20140408 (Recommendation, 2014-04-08), checked 2026-10-06.
- [XQuery 4.0](https://qt4cg.org/specifications/xquery-40/xquery-40.html): Community Group draft, xquery-40-preview REC-xquery-31-20170321 (Community Group draft, 2026-10-05), checked 2026-10-06.
- [XQuery 3.1: An XML Query Language](https://www.w3.org/TR/xquery-31/): Recommendation, xquery-31 REC-xquery-31-20170321 (Recommendation, 2017-03-21), checked 2026-10-06.
- [XQuery 3.0: An XML Query Language](https://www.w3.org/TR/xquery-30/): Recommendation, xquery-30 REC-xquery-30-20140408 (Recommendation, 2014-04-08), checked 2026-10-06.
- [XPath and XQuery Functions and Operators 3.1](https://www.w3.org/TR/xpath-functions-31/): Recommendation, xpath-functions-31 REC-xpath-functions-31-20170321 (Recommendation, 2017-03-21), checked 2026-10-06.
- [XQuery and XPath Data Model 3.1](https://www.w3.org/TR/xpath-datamodel-31/): Recommendation, xpath-datamodel-31 REC-xpath-datamodel-31-20170321 (Recommendation, 2017-03-21), checked 2026-10-06.
- [XQueryX 3.1](https://www.w3.org/TR/xqueryx-31/): Recommendation, xqueryx-31 REC-xqueryx-31-20170321 (Recommendation, 2017-03-21), checked 2026-10-06.
- [XQuery and XPath Full Text 3.0](https://www.w3.org/TR/xpath-full-text-30/): Recommendation, xpath-full-text-30 REC-xpath-full-text-30-20151124 (Recommendation, 2015-11-24), checked 2026-10-06.
- [XPath 1.0](https://www.w3.org/TR/xpath-10/): Recommendation, W3C Recommendation 16 November 1999, checked 2026-10-06.
- [XPath 2.0](https://www.w3.org/TR/xpath20/): Recommendation, W3C Recommendation 14 December 2010, checked 2026-10-06.
- [XQuery and XPath Full Text 1.0](https://www.w3.org/TR/xpath-full-text-10/): Recommendation, W3C Recommendation 17 March 2011, checked 2026-10-06.
- [XQuery 1.0](https://www.w3.org/TR/xquery-10/): Recommendation, W3C Recommendation 14 December 2010, checked 2026-10-06.
