---
name: csvw
description: >-
  CSV on the Web: Tabular data is routinely transferred on the web in a variety of formats, including variants on CSV, tab-delimited files, fixed field formats, spreadsheets, HTML tables, and SQL dumps. Covers Model for Tabular Data and Metadata on the Web, Metadata Vocabulary for Tabular Data, Generating JSON from Tabular Data on the Web, Generating RDF from Tabular Data on the Web. Use when describing or converting tabular data. Triggers: CSVW, tabular data.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# CSV on the Web

Tabular data is routinely transferred on the web in a variety of formats, including variants on CSV, tab-delimited files, fixed field formats, spreadsheets, HTML tables, and SQL dumps. This document outlines a data model, or infoset, for tabular data and metadata about that tabular data that can be used as a basis for validation, display, or creating other formats. It also contains some non-normative guidance for publishing tabular data as CSV and how that maps into the tabular data model. An annotated model of tabular data can be supplemented by separate metadata about the table. This specification defines how implementations should locate that metadata, given a file containing tabular data

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when describing or converting tabular data.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Model for Tabular Data and Metadata on the Web (default); Metadata Vocabulary for Tabular Data (default); Generating JSON from Tabular Data on the Web (default); Generating RDF from Tabular Data on the Web (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words MAY , MUST , MUST NOT , SHOULD , and SHOULD NOT are to be interpreted as described in [ RFC2119 ]."
2. **4. Tabular Data Models.** "String values within the tabular data model (such as column titles or cell string values) MUST contain only Unicode characters."
3. **4.1 Table groups.** "A group of tables MUST have one or more tables."
4. **4.2 Tables.** "A table MUST have one or more columns and the order of the columns within the list is significant and MUST be preserved by applications."
5. **4.2 Tables.** "A table MUST have one or more rows and the order of the rows within the list is significant and MUST be preserved by applications."
6. **4.3 Columns.** "A column MUST contain one cell from each row in the table."
7. **4.3 Columns.** "The order of the cells in the list MUST match the order of the rows in which they appear within the rows for the associated table ."
8. **4.3 Columns.** "required — a boolean that indicates that values of cells in this column MUST NOT be empty."

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

- [Model for Tabular Data and Metadata on the Web](https://www.w3.org/TR/tabular-data-model/): Recommendation, tabular-data-model REC-tabular-data-model-20151217 (Recommendation, 2015-12-17), checked 2026-10-06.
- [Metadata Vocabulary for Tabular Data](https://www.w3.org/TR/tabular-metadata/): Recommendation, tabular-metadata REC-tabular-data-model-20151217 (Recommendation, 2015-12-17), checked 2026-10-06.
- [Generating JSON from Tabular Data on the Web](https://www.w3.org/TR/csv2json/): Recommendation, csv2json REC-tabular-data-model-20151217 (Recommendation, 2015-12-17), checked 2026-10-06.
- [Generating RDF from Tabular Data on the Web](https://www.w3.org/TR/csv2rdf/): Recommendation, csv2rdf REC-tabular-data-model-20151217 (Recommendation, 2015-12-17), checked 2026-10-06.
