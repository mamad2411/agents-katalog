---
name: list-indent-consistency
description: >-
  Detects and repairs inconsistent continuation-line indentation under list
  items in markdown files — base primitive consumed by higher-level skills
  that edit or generate markdown documents.
category: General-Utility
---

# List Indent Consistency (v1)

A domain-agnostic base skill that scans markdown files for **continuation-line
indent drift** — where the lines following a list item use a different
indentation depth than sibling items at the same nesting level.  Provides both
detection-only and auto-fix modes.

***

## Composition Rationale

This skill owns a single reusable primitive: **markdown list continuation-line
indent analysis**.  It was extracted as its own base skill because the
deterministic "parse → detect drift → repair" operation is reused by multiple
domains — skill-factory post-edit verification, markdown-generation linting,
git-atomic-commit-construction indent verification, and any other workflow
that edits `.md` files.  Inlining this logic into any single domain skill
would split the SSOT and force each consumer to maintain its own copy.

***

## Composition by Higher-Level Skills

| Composer / Consumer | Composition Mechanism |
| :--- | :--- |
| [`skill-factory` §5.4](../skill-factory/SKILL.md#54-numbered-section-scheme-consistency) | Enforces indent-continuity check after every skill-doc edit. |
| [`skill-factory` §5.8](../skill-factory/SKILL.md#58-style-consistency-discipline-match-the-surrounding-document) | Style-consistency mandate cross-references this skill for automated indent repair. |
| [`markdown-generation`](../markdown-generation/SKILL.md) | Indent-drift warning (§3) delegates detection and repair to this skill. |
| [`git-atomic-commit-construction` §3g](../git-atomic-commit-construction/SKILL.md#3g--post-edit-indent-verification--repair) | Post-edit indent verification protocol delegates to this skill. |

***

## 1. Environment & Dependencies

- **Python 3.12+** — required runtime.  Standard library only (`re`, `argparse`,
  `sys`).  No `pip` dependencies.
- **Verify**: `python3 --version` (must show ≥3.12).

***

## 2. Protocol

1. **Identify the markdown file(s)** — one or more paths to `.md` files, or
   pipe content through stdin.
2. **Run the detection script:**

   ```bash
   # Detect drift (exit 1 if found)
   python3 .agents/skills/general/list-indent-consistency/scripts/detect-list-indent-drift.py \
       path/to/file.md

   # Detect and fix drift in place
   python3 .agents/skills/general/list-indent-consistency/scripts/detect-list-indent-drift.py \
       --fix path/to/file.md

   # Scan all SKILL.md files in the skills tree
   python3 .agents/skills/general/list-indent-consistency/scripts/detect-list-indent-drift.py \
       .agents/skills/**/SKILL.md
   ```

3. **Read the output** — each drift report shows the file path, line number,
   expected indent, and actual indent.
4. **Re-verify** — run detection again without `--fix`; expect exit 0.

### 2.1 Detection Logic

The script operates on these rules:

- **List item** — any line starting with `N. ` (numbered), `- ` (bullet),
  `* ` (bullet), or `+ ` (bullet), optionally preceded by whitespace.
- **Continuation line** — any non-blank, non-list-item line immediately
  following a list item (or another continuation line), indented by at least
  2 spaces.
- **Correct indent** — the most common continuation-line indent among sibling
  list items at the same nesting depth within the same list block.  Siblings
  are items separated by blank lines (loose list) or not (compact list).
- **Drift** — a continuation line whose leading whitespace differs from the
  correct indent for its nesting depth.  A single list item with multiple
  continuation lines at different indents is also flagged as drift.

### 2.2 Repair Logic (`--fix`)

When `--fix` is passed:

1. For each detected drift, rewrite the line's leading whitespace to match
   the correct indent for its nesting depth.
2. Preserve all other content (no trailing whitespace changes, no content
   modifications).
3. Write the modified file in place.
4. Print the list of repaired lines to stdout.
5. Exit 0 (all drift corrected).

***

## 3. Script Reference

**`scripts/detect-list-indent-drift.py`** — the sole script in this skill.

| Argument | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `paths` (positional) | No | `-` (stdin) | One or more markdown file paths.  If omitted, reads from stdin. |
| `--fix` | No | `false` | Repair drift in place.  Without this flag, only detection is performed. |
| `--indent` | No | `auto` | Expected continuation indent (number of spaces).  `auto` derives it from sibling items. |
| `--quiet` | No | `false` | Suppress per-line output; only show summary and exit code. |

### Exit codes

- `0` — no drift found (or `--fix` applied all repairs successfully).
- `1` — drift found (detection mode) or repair failed.

### Output format (detection mode)

```
[<relative-path>] L<line-number>: expected <N> spaces, found <M> spaces
  content: <line content truncated to 80 chars>
---
```

### Output format (`--fix` mode)

```
[<relative-path>] L<line-number>: repaired (<N> → <M> spaces)
---
```

### Example

```bash
# Check a single file
python3 detect-list-indent-drift.py README.md

# Check and fix all SKILL.md files
python3 detect-list-indent-drift.py --fix .agents/skills/**/SKILL.md

# Pipe content through stdin
cat file.md | python3 detect-list-indent-drift.py
```
