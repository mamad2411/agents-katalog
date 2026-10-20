---
name: rif
description: >-
  RIF: This document, developed by the Rule Interchange Format (RIF) Working Group , specifies RIF-Core, a common subset of RIF-BLD and RIF-PRD based on RIF-DTB 1.0. Covers RIF Core Dialect (Second Edition), RIF Basic Logic Dialect (Second Edition), RIF Production Rule Dialect (Second Edition). Use when exchanging rules. Triggers: RIF, Rule Interchange Format.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# RIF

This document, developed by the Rule Interchange Format (RIF) Working Group , specifies RIF-Core, a common subset of RIF-BLD and RIF-PRD based on RIF-DTB 1.0. The RIF-Core presentation syntax and semantics are specified by restriction in two different ways. First, RIF-Core is specified by restricting the syntax and semantics of RIF-BLD, and second, by restricting RIF-PRD. The XML serialization syntax of RIF-Core is specified by a mapping from the presentation syntax. A normative XML schema is also provided.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when exchanging rules.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RIF Core Dialect (Second Edition) (default); RIF Basic Logic Dialect (Second Edition) (default); RIF Production Rule Dialect (Second Edition) (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **11 Appendix: RIF Media Type Registration.** "RIF consuming systems SHOULD implement reasonable defenses against these attacks."
2. **1 Overview.** "However, it should be kept in mind that RIF is designed to enable interoperability among rule languages in general, and its uses are not limited to the Web."
3. **2.4 Annotations and Documents.** "The frame formulas that are allowed as part of an annotation must be syntactically correct for RIF-Core."
4. **7 Conformance Clauses.** "A conformant Core consumer must reject any document containing features it does not support."
5. **11 Appendix: RIF Media Type Registration.** "Before being installed on systems which consume untrusted RIF documents, these external functions should be closely reviewed for their own vulnerabilities and for the vulnerabilities that may occur when they are used in unexpected combinations, like "cross-site scripting" attacks."

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

- [RIF Core Dialect (Second Edition)](https://www.w3.org/TR/rif-core/): Recommendation, rif-core REC-rif-core-20130205 (Recommendation, 2013-02-05), checked 2026-10-06.
- [RIF Basic Logic Dialect (Second Edition)](https://www.w3.org/TR/rif-bld/): Recommendation, rif-bld REC-rif-bld-20130205 (Recommendation, 2013-02-05), checked 2026-10-06.
- [RIF Production Rule Dialect (Second Edition)](https://www.w3.org/TR/rif-prd/): Recommendation, rif-prd REC-rif-prd-20130205 (Recommendation, 2013-02-05), checked 2026-10-06.
