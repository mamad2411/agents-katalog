---
name: github-flavored-markdown
description: >-
  GitHub Flavored Markdown: parse and write GFM with tables, task lists, strikethrough and autolinks. Covers GitHub Flavored Markdown. Use when parsing GitHub Flavored Markdown. Triggers: GFM, GitHub Flavored Markdown.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# GitHub Flavored Markdown

non-whitespace character after the list marker. However, that is not quite right.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when parsing GitHub Flavored Markdown.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: GitHub Flavored Markdown (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **GitHub Flavored Markdown Spec.** "The idea is that a Markdown-formatted document should be publishable as-is, as plain text, without looking like it’s been marked up with tags or formatting instructions."
2. **GitHub Flavored Markdown Spec.** "It is natural to think that they, too, must be indented four spaces, but Markdown.pl does not require that."
3. **GitHub Flavored Markdown Spec.** "What should we do with a list like this?"
4. **GitHub Flavored Markdown Spec.** "For example, how should the following be parsed?"
5. **GitHub Flavored Markdown Spec.** "2.3 Insecure characters For security reasons, the Unicode character U+0000 must be replaced with the REPLACEMENT CHARACTER ( U+FFFD )."
6. **GitHub Flavored Markdown Spec.** "The opening sequence of # characters must be followed by a space or by the end of line."
7. **GitHub Flavored Markdown Spec.** "The optional closing sequence of # s must be preceded by a space and may be followed by spaces only."
8. **GitHub Flavored Markdown Spec.** "However, the space was required by the original ATX implementation , and it helps prevent things like the following from being parsed as headings: Example 34 #5 bolt #hashtag <p>#5 bolt</p> <p>#hashtag</p> This is not a heading, because the first # is escaped: Example 35 \## foo <p>## foo</p> Contents are parsed as inlines: Example 36 # foo _bar_ \*baz\* <h1>foo <em>bar</em> _baz_</h1> Leading…"

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

- [GitHub Flavored Markdown](https://github.github.com/gfm/): Specification, GitHub Flavored Markdown, fetched 2026-10-06 (Specification, 2026-10-06), checked 2026-10-06.
