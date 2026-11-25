---
name: text-lines-sort-by-length
description: Sort the lines of a text file by physical line length (ascending by default, descending with `--reverse`), with an optional preserved header block and stable tie-breaking. Useful for arranging onboarding command lists, log lines, or any line-oriented artifact from smallest to largest unit.
category: Text-Manipulation
---

# Text Lines Sort By Length Skill (v1) — Base Primitive

Atomic, domain-agnostic primitive that rewrites a text file with its body
lines reordered by physical line length. Sort is **stable** (ties preserve
original relative order), and an optional **header block** of the first
`N` lines is held back from the sort and re-emitted verbatim at the top
(e.g., `# filepath:` markers, shebangs, license preambles).

The originating use case is arranging an
`onboarding`-style bash command list from the shortest probe to the largest
chain, so a human (or downstream `command-autoapprove-onboarding` audit)
can review the easy cases first and the wide multi-flag chains last.

***

## 1. CLI Contract (Stable)

Located at [`scripts/text-lines-sort-by-length.py`](./scripts/text-lines-sort-by-length.py).

```bash
python3 text-lines-sort-by-length.py \
  --file PATH \
  [--output PATH | --in-place [--no-backup]] \
  [--header-lines N] \
  [--reverse] \
  [--drop-blank] \
  [--dry-run]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--file` | ✅ | Path to the input text file |
| `--output` | ❌ | Write sorted output to PATH (mutually exclusive with `--in-place`) |
| `--in-place` | ❌ | Rewrite `--file` in place (creates `.bak` unless `--no-backup`) |
| `--header-lines` | ❌ | Preserve the first N lines verbatim at the top (default: 0) |
| `--reverse` | ❌ | Sort descending (longest first); default is ascending |
| `--drop-blank` | ❌ | Drop blank lines from the sort body (default: keep them) |
| `--dry-run` | ❌ | Print result to stdout regardless of output mode |
| `--no-backup` | ❌ | Skip `.bak` when `--in-place` is used |

### Output Semantics

- Lines are compared by `len(line.rstrip("\n"))`, so a missing trailing
  newline on the final line never perturbs the ordering.
- Python's `sorted(..., key=...)` is **stable**: tied-length lines keep
  their original relative order.
- The first `--header-lines N` lines are NOT sorted and are emitted
  unchanged at the top of the output.
- Original trailing-newline disposition of the input file is preserved.
- Default mode (no `--in-place`, no `--output`) writes to stdout, making
  the script pipe-friendly.

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Success (or dry-run completed) |
| 1 | File missing, invalid `--header-lines`, or `--in-place` + `--output` collision |

***

## 2. Composition Rationale (No Layering)

This is an **atomic primitive** — there is no composer layer above it
because the transformation is intrinsically format-free (operates on
byte-level line records). Consumers invoke the script directly.

The closest sibling primitive,
[bash-multiline-to-single-line](../bash-multiline-to-single-line/SKILL.md),
is its natural **pre-step** when the input contains `\<newline>`-continued
commands: flatten first, then sort by length.

***

## 3. Consumers

| Consumer | Use case |
| :--- | :--- |
| [command-autoapprove-onboarding](../command-autoapprove-onboarding/SKILL.md) | Arrange an `onboarding`-style bash command list (e.g., `commands-to-onboard.bash`) from shortest probe to widest chain so triage starts with the cheap cases |

Any line-oriented artifact — log files, todo lists, CSV column extracts —
qualifies as a downstream consumer; the primitive intentionally makes no
syntactic assumptions about the body.

***

## 4. Language Choice (Python, not PowerShell)

`ai-rule-standardization-rules.md §4` and `skill-factory §2.2.1` default
to PowerShell. Python is chosen here for the same reasons as the sibling
[bash-multiline-to-single-line](../bash-multiline-to-single-line/SKILL.md):

1. The primary editing surface is macOS / Linux shells operating on
   bash-flavoured input, where `python3` is universally present.
2. The transformation is a single `sorted(..., key=len)` call; PowerShell
   offers no measurable advantage and would add a runtime dependency on
   macOS.
3. Keeping the toolchain consistent with neighbouring text-manipulation
   primitives (`bash-multiline-to-single-line`,
   `text-block-indent-override`) reduces cognitive switching.

This is the documented technical justification required by
`skill-factory §2.2.1` for selecting a non-PowerShell language.

***

## 5. Manual Usage Examples

Sort ascending in place, preserving the `# filepath:` header line, with
`.bak` backup:

```bash
python3 .agents/skills/text-lines-sort-by-length/scripts/text-lines-sort-by-length.py \
  --file commands-to-onboard.bash \
  --header-lines 1 \
  --in-place
```

Preview a descending sort to stdout without writing anything:

```bash
python3 .agents/skills/text-lines-sort-by-length/scripts/text-lines-sort-by-length.py \
  --file commands-to-onboard.bash \
  --header-lines 1 \
  --reverse \
  --dry-run
```

Write the sorted result to a sibling scratch file (typical
session-artifact pattern — the originating session of this skill):

```bash
python3 .agents/skills/text-lines-sort-by-length/scripts/text-lines-sort-by-length.py \
  --file commands-to-onboard.bash \
  --header-lines 1 \
  --output commands-to-onboard.sorted.bash
```

***

## 6. When To Use This Skill

Invoke this skill whenever the user asks to:

- "Arrange these commands from smallest to largest."
- "Sort this file by line length."
- "Order this list shortest first / longest first."
- "Create a scratch file with these lines rearranged by size."

Do NOT use this skill for alphabetical / semantic sorting — that belongs
to general `sort(1)` invocations or domain-specific skills such as
[json-deep-sort](../json-deep-sort/SKILL.md).

***

## 7. Traceability

- Born from an onboarding session that needed `commands-to-onboard.bash`
  rewritten to a scratch sibling with the 24 single-line commands ordered
  shortest → longest, so the downstream
  [command-autoapprove-onboarding](../command-autoapprove-onboarding/SKILL.md)
  audit could start with the cheapest probes and end with the widest
  chains. The ad-hoc Python snippet that performed that sort was promoted
  to this skill per `skill-factory §2.2.2` Script Delivery Mandate.
