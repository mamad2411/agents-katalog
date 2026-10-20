---
name: reuse
description: >-
  REUSE: add machine-readable copyright and license information to every file in a project. Covers REUSE. Use when adding machine-readable license information. Triggers: REUSE, SPDX-License-Identifier.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# REUSE

The REUSE Specification version 3.3 (2024-11-14) from the Free Software Foundation Europe: License Files in `LICENSES/`, comment headers and `.license` files, `REUSE.toml`, the deprecated DEP5 file, the order of precedence and the format of Copyright Notices, read from the specification source in the reuse-website repository.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Project maintainer adding licensing information, or a tool that lints or reads it.
- Target version: REUSE (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **License Files.** "A Project MUST include a License File for every license under which Covered Files are licensed."
2. **License Files.** "Each License File MUST be placed in the `LICENSES/` directory in the root of the Project."
3. **License Files.** "The name of the License File MUST be the SPDX License Identifier of the license followed by an appropriate file extension (example: `LICENSES/GPL-3.0-or-later.txt`)."
4. **License Files.** "The `LICENSES/` directory MUST NOT include any other files."
5. **Licensing Information.** "Each Covered File MUST have Licensing Information associated with it."
6. **Comment headers.** "For Uncommentable Files, the comment header that declares the file's Licensing Information MUST be in an adjacent text file of the same name with the additional extension `.license` (example: `cat.jpg.license` if the original file is `cat.jpg`)."
7. **Comment headers.** "The comment header MUST contain one or more Copyright Notices and one or more `SPDX-License-Identifier` tag-value pairs."
8. **REUSE.toml.** "Licensing Information MAY be associated with a file through a `REUSE.toml` file, which MUST be a valid TOML file."
9. **Order of precedence.** "If a Commentable File contains Licensing Information but also has an adjacent `.license` file, then the Licensing Information defined in the `.license` file takes precedence, and the Commentable File's contents are ignored."
10. **Format of Copyright Notices.** "The Copyright Notice MUST contain the name of the copyright holder."

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
- [ ] Every license used in any SPDX License Expression has a plain-text file in `LICENSES/`, and `LICENSES/` holds nothing else.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `spdx`, `citation-cff`, `editorconfig`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [REUSE Specification – Version 3.3](https://raw.githubusercontent.com/fsfe/reuse-website/82e32ee2de33979c46ca688a9dde52c709aff73e/site/content/en/spec-3.3.md): Specification, Version 3.3, 2024-11-14 (reuse-website commit 82e32ee), checked 2026-10-06.
