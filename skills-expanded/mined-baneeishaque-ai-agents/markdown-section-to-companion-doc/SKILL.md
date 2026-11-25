---
name: markdown-section-to-companion-doc
description: Base primitive — move a named `## Section` out of a markdown document into a sibling companion file (`<NAME>.md`), replacing it with a pointer paragraph. Domain-agnostic; idempotent check/split/dry-run modes.
category: Text-Manipulation
---

# Markdown Section to Companion Doc Skill (v1) — Base Primitive

> **Skill ID:** `markdown-section-to-companion-doc`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../../skill-factory/SKILL.md))

This is the **base skill** of a 2-layer section-separation stack. It owns ONLY the generic primitive of
extracting a named `## Section` from any markdown document into a sibling companion file, leaving behind
the heading plus a pointer paragraph.

It is **domain-agnostic**: it has no knowledge of skill metadata, changelogs, traceability records, or any
specific document genre. Composer skills supply the section names, pointer text, and companion filenames.

***

## 1. CLI Contract (Stable)

Located at [`scripts/split-section.py`](./scripts/split-section.py).

```bash
python3 split-section.py --doc PATH --section NAME (--check | --split | --dry-run)
                        [--pointer TEXT] [--companion-name FILENAME]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--doc` | ✅ | Path to the markdown document |
| `--section` | ✅ | Section name to move (matches a `## <NAME>` heading, ATX level 2) |
| `--check` | ✅* | Report whether the section is INLINE (body content present) or external; exit 1 if inline |
| `--split` | ✅* | Extract the inline section body into the companion file; replace source block with heading + pointer |
| `--dry-run` | ✅* | Print the planned companion file and source replacement; write nothing |
| `--pointer` | ❌ | Pointer paragraph placed under the retained heading (default: `See [<companion>.md](<companion>.md).`) |
| `--companion-name` | ❌ | Companion filename (default: `<Section>.md`) |

*Exactly one of `--check` / `--split` / `--dry-run` is required.

### Output Semantics

- The section boundary is the `## <NAME>` heading through the last line before the next `##` (or higher)
  heading — i.e., `###` / `####` subheadings inside the section stay with the section body.
- `--split` moves the body (leading/trailing blank lines stripped) into
  `<companion>` with title `# <Section> — <doc-stem>`, where `<doc-stem>` is the source file's parent
  directory name for `SKILL.md` / `AGENTS.md` sources, otherwise the source file stem.
- The source section block is replaced by the retained heading, a blank line, and the pointer paragraph,
  plus a single blank-line separator before the following content. Everything outside the replaced block
  is byte-identical.
- A section whose body is **pointer prose** is treated as **already external**: the first non-empty
  line starts with `See [X.md` (markdown link to a companion `.md` file — backtick-quoted link
  styles allowed) and the body contains no structured content (bullets, numbered items, table rows,
  fenced code blocks). Wrapped prose continuation lines are allowed. `--check` exits 0 and `--split`
  is a no-op (idempotent).
- A section that is absent is treated as **compliant**: `--check` exits 0; `--split` exits 1 with an
  error (a split is only possible for a section that exists inline).

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Success / no-op / compliant (section absent or already external) |
| 1 | Inline section found (`--check`) / section not present (`--split`) |
| 2 | Usage or IO error |

***

## 2. Composition by Higher-Level Skills

| Composer | Domain | Adds |
| :--- | :--- | :--- |
| [skill-doc-metadata-separation](../skill-doc-metadata-separation/SKILL.md) | Skill docs | Audits `Changelog` / `Traceability` sections across one skill or the whole library; maps sections to `CHANGELOG.md` / `TRACEABILITY.md` companion names; batches base invocations; re-verifies compliance |

***

## 3. Design Notes

- **No document-genre awareness**: Deciding which sections are "information, not instructions" and what
  pointer text to use is a composer concern. This script only moves bytes.
- **No markdownlint hook**: The caller verifies markdown validity after the split; the script returns
  success as long as the section was found and files were written.
- **Deterministic**: Same input + same flags → same output. `--check` output is greppable
  (`INLINE  <path>: '<section>' at lines N-M`), so composers can parse violations programmatically.
- **Idempotent by design**: Re-running `--split` on an already-external section is a no-op, so composer
  loops over many files can be re-run safely.

***

## 4. Manual Usage Example (Non-Composer)

To extract the `## Traceability` section of any markdown doc into `Traceability.md`:

```bash
python3 .agents/skills/markdown-section-to-companion-doc/scripts/split-section.py \
  --doc docs/example.md --section Traceability --split
```

This is shown only to illustrate the contract — most callers should use a composer skill.

***

## 5. Related Skills

- [skill-doc-metadata-separation](../skill-doc-metadata-separation/SKILL.md) — the composer that applies this
  primitive to skill `Changelog` / `Traceability` sections library-wide.
- [text-block-indent-override](../../text-block-indent-override/SKILL.md) — sibling base primitive for in-place
  re-indenting of delimited blocks (complementary: this skill relocates, that one re-indents).

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
