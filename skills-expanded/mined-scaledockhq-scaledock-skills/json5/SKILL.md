---
name: json5
description: >-
  JSON5: parse and write JSON5, the JSON superset with comments, trailing commas and unquoted keys. Covers JSON5. Use when parsing JSON5. Triggers: JSON5.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# JSON5

The JSON5 Data Interchange Format, version 1.0.0, by Aseem Kishore and Jordan Tucker: values, objects, arrays, strings and escapes, numbers, comments, white space, and the parser and generator conformance rules, read from the Ecmarkup source of spec.json5.org.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: JSON5 parser or generator, or an author of JSON5 documents.
- Target version: JSON5 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 2 Values.** "A JSON5 value must be an object, array, string, or number, or one of the three literal names true, false, or null."
2. **§ 3 Objects.** "The names within an object should be unique."
3. **§ 5 Strings.** "The same quotation mark that begins a string must also end the string."
4. **§ 5.1 Escapes.** "A reverse solidus followed by the lower case letter `x` must be followed by two hexadecimal digits."
5. **§ 5.1 Escapes.** "A reverse solidus followed by the lower case letter `u` must be followed by four hexadecimal digits."
6. **§ 5.1 Escapes.** "A decimal digit must not follow a reverse solidus followed by a zero."
7. **§ 5.2 Paragraph and Line Separators.** "JSON5 generators should escape these code points in strings."
8. **§ 7 Comments.** "Multi-line comments cannot nest."
9. **§ 10 Parsers.** "A JSON5 parser must accept all texts that conform to the JSON5 grammar."
10. **§ 11 Generators.** "The resulting text must strictly conform to the JSON5 grammar."

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
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `json`, `ecmascript`, `unicode`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [The JSON5 Data Interchange Format (src/index.html)](https://raw.githubusercontent.com/json5/json5-spec/d77331d96bc6b74622703e5d009d6124072f04dd/src/index.html): Specification, Version 1.0.0 (json5-spec commit d77331d, 2023-05-15), checked 2026-10-06.
