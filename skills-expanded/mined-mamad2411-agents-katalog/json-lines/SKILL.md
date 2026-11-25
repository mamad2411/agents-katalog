---
name: json-lines
description: >-
  JSON Lines: This page describes the JSON Lines text format, also called newline-delimited JSON. Covers JSON Lines. Use when reading newline-delimited JSON. Triggers: JSON Lines, NDJSON.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# JSON Lines

The JSON Lines text format (newline-delimited JSON) documented at jsonlines.org: its three requirements (UTF-8, one JSON value per line, `\n` as line terminator) and its conventions, read from the page source in the wardi/jsonlines repository.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Writer or reader of JSON Lines files or streams.
- Target version: JSON Lines (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **1. UTF-8 Encoding.** "Like the JSON standard a byte order mark (U+FEFF) must NOT be included."
2. **2. Each Line is a Valid JSON Value.** "The most common values will be objects or arrays, but any JSON value is permitted."
3. **2. Each Line is a Valid JSON Value.** "e.g. null is a valid value but a blank line is not."
4. **3. Line Terminator is '\n'.** "This means '\r\n' is also supported because surrounding white space is implicitly ignored when parsing JSON values."
5. **3. Line Terminator is '\n'.** "If a line terminator follows the last JSON value in a file, it must be the last byte in the file."
6. **Conventions.** "JSON Lines files may be saved with the file extension .jsonl."

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
- [ ] Each line holds exactly one JSON value; there are no blank lines and no byte order mark.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `json`, `csv`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [JSON Lines (jsonlines.org index.md)](https://raw.githubusercontent.com/wardi/jsonlines/d5ba812c995afc83d8a3b29f0a7f1b7cf0bf17fb/index.md): Documentation, jsonlines.org source, commit d5ba812 (2026-09-26), checked 2026-10-06.
