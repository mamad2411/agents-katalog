---
name: citation-cff
description: >-
  Citation File Format: write CITATION.cff files that tell people how to cite software and datasets. Covers Citation File Format. Use when writing a CITATION.cff file. Triggers: CFF, CITATION.cff.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Citation File Format

The Citation File Format (CFF) schema version 1.2.0 from the citation-file-format project: the file name and structure, the top-level keys, credit redirection and the reusable definitions, read from the schema guide at the 1.2.0 release tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Author of a CITATION.cff file, or a tool that writes, validates or reads one.
- Target version: Citation File Format (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **General structure of a CITATION.cff file.** "must be named `CITATION.cff` (note the capitalization);"
2. **General structure of a CITATION.cff file.** "are valid YAML 1.2"
3. **Minimal example.** "A minimal example of a valid `CITATION.cff` file, that contains only the required keys, could look like this:"
4. **Valid keys § cff-version.** "The Citation File Format schema version that the `CITATION.cff` file adheres to for providing the citation metadata."
5. **Valid keys § date-released.** "Format is 4-digit year, 2-digit month, 2-digit day of month, separated by dashes."
6. **Valid keys § license.** "When there are multiple licenses, it is assumed their relationship is OR, not AND."
7. **Definitions.** "`definitions` and its subkeys like `definitions.alias` or `definitions.entity.alias` should not be used as keys in `CITATION.cff` files:"
8. **Definitions § definitions.date.** "Note to tool implementers: it is necessary to cast YAML `date` objects to `string` objects when validating against the schema."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] The file is named `CITATION.cff`, is valid YAML 1.2 and has `cff-version: 1.2.0`.
- [ ] Dates use the 4-digit year, 2-digit month, 2-digit day format, separated by dashes.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `yaml`, `reuse`, `semver`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Guide to Citation File Format schema version 1.2.0](https://raw.githubusercontent.com/citation-file-format/citation-file-format/396f738fb025b1d8acdb02a56ffc923f95dc8999/schema-guide.md): Release, CFF 1.2.0 (commit 396f738, released 2021-08-09), checked 2026-10-06.
