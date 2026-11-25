---
name: text-block-indent-override
description: Base primitive — locate a delimited block in a text file by regex and re-indent specific lines inside it from N spaces to M spaces. Domain-agnostic.
category: Text-Manipulation
---

# Text Block Indent Override Skill (v1) — Base Primitive

This is the **base skill** of a 3-layer indent-override stack. It owns ONLY the generic primitive of
locating a regex-matched block in any text file and re-indenting specific lines inside it.

It is **domain-agnostic**: it has no knowledge of JSON, YAML, TOML, or any specific configuration
syntax. Composer skills supply the block-pattern.

***

## 1. CLI Contract (Stable)

Located at [`scripts/text-block-indent-override.py`](./scripts/text-block-indent-override.py).

```bash
python3 text-block-indent-override.py \
  --file PATH \
  --block-pattern REGEX \
  --from-spaces N \
  --to-spaces   M \
  [--target-line-prefix STR1 STR2 ...] \
  [--dry-run] \
  [--no-backup]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--file` | ✅ | Path to the input text file |
| `--block-pattern` | ✅ | Regex matching the entire delimited block (DOTALL applied) |
| `--from-spaces` | ✅ | Current leading-space count to match |
| `--to-spaces` | ✅ | Replacement leading-space count |
| `--target-line-prefix` | ❌ | If set, only rewrites lines whose content **after** the from-spaces prefix starts with one of these literal strings |
| `--dry-run` | ❌ | Print rewritten block(s), do not save |
| `--no-backup` | ❌ | Skip `.bak` creation (default: backup is created) |

### Output Semantics

- Lines fully outside any matched block: **untouched**.
- The first and last line of each matched block (the delimiter lines): **untouched**.
- Inner lines starting with exactly `--from-spaces` spaces: replaced with `--to-spaces` spaces +
  remaining text.
- If `--target-line-prefix` is set: only inner lines whose post-prefix content begins with one of
  the listed strings are rewritten.

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Success (or dry-run completed) |
| 1 | Pattern not found, IO error, invalid regex, or invalid args |

***

## 2. Composition by Higher-Level Skills

| Composer | Domain | Adds |
| :--- | :--- | :--- |
| [json-block-indent-override](../json-block-indent-override/SKILL.md) | JSON config files | Builds the JSON block pattern from a top-level key; auto-quotes target keys; validates result with `json.loads`; rolls back on parse failure |
| [vscode-settings-indent-override](../vscode-settings-indent-override/SKILL.md) | VS Code `settings.json` | Indirect — composes via `json-block-indent-override`. Knows VS Code profile paths and common keys |

***

## 3. Design Notes

- **No format awareness**: Inlining JSON-pattern construction into this base would violate the SSOT
  contract. Composers must build their own block patterns and pipe them through `--block-pattern`.
- **No validation hook**: Format-specific validation (e.g. `json.loads`, `yaml.safe_load`) belongs
  to composers — this script returns success as long as the regex matched and the file was written.
- **DOTALL by default**: Matches multi-line values (e.g. JSON string values containing literal
  `\n`). Composers do not need to add the `(?s)` flag.

***

## 4. Manual Usage Example (Non-Composer)

To re-indent inner keys of a YAML block 2 spaces deeper:

```bash
python3 .agents/skills/text-block-indent-override/scripts/text-block-indent-override.py \
  --file config.yaml \
  --block-pattern '^my_section:\n(?: {2}.*\n)+' \
  --from-spaces 2 --to-spaces 4
```

This is shown only to illustrate the contract — most callers should use a composer skill.
