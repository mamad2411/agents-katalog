---
name: mdx
description: >-
  MDX: write Markdown that imports and renders JSX components. Covers MDX. Use when writing MDX. Triggers: MDX.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# MDX

MDX 3 from the mdx-js project: the MDX syntax (Markdown, JSX, expressions, ESM and interleaving) and how MDX is compiled and used, read from the "What is MDX?" and "Using MDX" documentation sources at the 3.1.1 release tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Author of MDX documents, or an integration that compiles or renders them.
- Target version: MDX (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **MDX syntax.** "The MDX syntax combines markdown with JSX."
2. **MDX syntax § Markdown.** "Indented code does not work in MDX:"
3. **MDX syntax § Markdown.** "Autolinks do not work in MDX."
4. **MDX syntax § Markdown.** "HTML syntax doesn’t work in MDX as it’s replaced by JSX (`<img>` to `<img />`)."
5. **MDX syntax § Markdown.** "Instead of HTML comments, you can use JavaScript comments in braces:"
6. **MDX syntax § Markdown.** "Unescaped left angle bracket / less than (`<`) and left curly brace (`{`) have to be escaped: `\<` or `\{` (or use expressions: `{'<'}`, `{'{'}`)"
7. **MDX syntax § JSX.** "Note that components must be defined."
8. **MDX syntax § Interleaving.** "You can use markdown “inlines” but not “blocks” inside JSX if the text and tags are on the same line:"
9. **How MDX works.** "An integration compiles MDX syntax to JavaScript."

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
- [ ] The document has no indented code, autolinks, HTML comments or unescaped `<` and `{` in text.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `commonmark`, `github-flavored-markdown`, `ecmascript`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [What is MDX?](https://raw.githubusercontent.com/mdx-js/mdx/50aa8df0b027c893dec9f97a2b7c51539e9f1a4b/docs/docs/what-is-mdx.mdx): Documentation, MDX 3.1.1 (commit 50aa8df, released 2025-08-29), checked 2026-10-06.
- [Using MDX](https://raw.githubusercontent.com/mdx-js/mdx/50aa8df0b027c893dec9f97a2b7c51539e9f1a4b/docs/docs/using-mdx.mdx): Documentation, MDX 3.1.1 (commit 50aa8df, released 2025-08-29), checked 2026-10-06.
