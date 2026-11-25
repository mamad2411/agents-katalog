---
name: bash-multiline-to-single-line
description: Flatten bash commands that span multiple physical lines via trailing backslash-newline continuations into a single physical line, optionally scoped to a line range. Useful before regex-matching commands against autoApprove patterns or pasting into single-line input fields.
category: Text-Manipulation
---

# Bash Multiline To Single Line Skill (v1) — Base Primitive

Atomic, domain-agnostic primitive that rewrites bash `\<newline>` continuations
to a single physical line. Leading whitespace on each continuation line is
collapsed to exactly one space; all other content (comments, blank lines,
non-continuation lines) is preserved verbatim.

The most common consumer is [command-autoapprove-onboarding](../command-autoapprove-onboarding/SKILL.md):
multi-line `\`-continued commands must be flattened before regex coverage
analysis, since the autoApprove pattern matcher sees the user's command as a
single string at runtime.

***

## 1. CLI Contract (Stable)

Located at [`scripts/bash-multiline-to-single-line.py`](./scripts/bash-multiline-to-single-line.py).

```bash
python3 bash-multiline-to-single-line.py \
  --file PATH \
  [--line-range START END] \
  [--dry-run] \
  [--no-backup]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--file` | ✅ | Path to the input bash file |
| `--line-range` | ❌ | 1-based inclusive range; default = whole file |
| `--dry-run` | ❌ | Print result to stdout, do not save |
| `--no-backup` | ❌ | Skip `.bak` creation (default: backup is created) |

### Output Semantics

- Every occurrence of `\` immediately followed by `\n` (and any leading
  whitespace on the next line) becomes a single space.
- Lines without trailing `\` are preserved byte-for-byte.
- Blank lines, shebangs, and `#` comments are preserved.
- File trailing newline is preserved.

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Success (or dry-run completed, or no continuations in range — no-op) |
| 1 | File missing, IO error, or invalid line range |

***

## 2. Composition Rationale (No Layering)

This is an **atomic primitive** — there is no composer layer above it because
the transformation is intrinsically format-free (operates on byte-level
backslash-newline sequences). Consumers invoke the script directly.

## 3. Consumers

| Consumer | Use case |
| :--- | :--- |
| [command-autoapprove-onboarding](../command-autoapprove-onboarding/SKILL.md) | Flatten user-pasted multi-line commands before regex coverage analysis and pattern matching against `chat.tools.terminal.autoApprove` entries |

***

## 3a. Natural Successors

After flattening, a common follow-up is to sort the resulting one-line
commands by length so the smallest probes come first:

| Successor | Use case |
| :--- | :--- |
| [text-lines-sort-by-length](../text-lines-sort-by-length/SKILL.md) | Sort the flattened commands ascending/descending by physical line length, preserving an optional `# filepath:` / shebang header block |

***

## 4. Language Choice (Python, not PowerShell)

`ai-rule-standardization-rules.md §4` defaults to PowerShell. Python is chosen
here because:

1. The skill operates on Unix-flavored bash scripts whose primary editing
   surfaces are macOS / Linux shells where `python3` is universally present.
2. Precedent: the closest analog [text-block-indent-override](../text-block-indent-override/SKILL.md)
   is Python — keeping the same toolchain reduces cognitive switching.
3. The transformation is a single `re.sub` call; PowerShell offers no
   measurable advantage and would add a runtime dependency on macOS.

***

## 5. Manual Usage Examples

Flatten the whole file (with `.bak` backup):

```bash
python3 .agents/skills/bash-multiline-to-single-line/scripts/bash-multiline-to-single-line.py \
  --file commands-to-onboard.bash
```

Preview a flatten of lines 3–20 only, no write:

```bash
python3 .agents/skills/bash-multiline-to-single-line/scripts/bash-multiline-to-single-line.py \
  --file commands-to-onboard.bash \
  --line-range 3 20 \
  --dry-run
```

***

## 6. Traceability

- Born from the recurring need during `command-autoapprove-onboarding` work to
  collapse user-pasted `\`-continued git / find / grep chains into a single
  line so they could be regex-matched against existing autoApprove patterns
  and audited via `batch-coverage-check.py`.
