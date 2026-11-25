---
name: json-block-indent-override
description: Composer — re-indent lines inside a top-level JSON key's block with auto-quoted target keys and json.loads validation. Pipes through text-block-indent-override.
category: Text-Manipulation
---

# JSON Block Indent Override Skill (v1) — Composer

This is a **composer skill** that adds JSON awareness on top of the
[text-block-indent-override](../text-block-indent-override/SKILL.md) base primitive.

It accepts a top-level JSON key, builds the JSON-shaped block pattern, auto-quotes target sub-keys
so callers do not face shell-quoting hell, runs `json.loads` after rewriting, and rolls back to the
backup on parse failure.

***

## 1. Composition Rationale

The base skill knows nothing about JSON — it just rewrites regex-matched blocks. This composer adds:

| Concern | Without composer | This composer |
| :--- | :--- | :--- |
| **Block pattern** | Caller writes `"key":\s*\{.*?\n\}` with DOTALL quirks | Caller passes bare `--key files.associations` |
| **Sub-key quoting** | Caller passes `--target-line-prefix '"approve"'` (shell-escape pain) | Caller passes `--target-keys approve`; composer wraps in `"..."` |
| **Post-write validation** | Caller runs `jq empty` manually | Composer runs `json.loads`; rolls back on failure |
| **Error messages** | "Pattern matched 0 blocks" | "JSON key 'foo' not found at top level" (future) |

***

## 2. CLI Contract

Located at [`scripts/json-block-indent-override.py`](./scripts/json-block-indent-override.py).

```bash
python3 json-block-indent-override.py \
  --file PATH_TO_JSON \
  --key  TOP_LEVEL_KEY \
  --from-spaces N \
  --to-spaces   M \
  [--target-keys sub-key-1 sub-key-2 ...] \
  [--dry-run]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--file` | ✅ | Path to JSON file |
| `--key` | ✅ | Top-level JSON key whose block to re-indent |
| `--from-spaces` | ✅ | Current leading-space count of lines to change |
| `--to-spaces` | ✅ | Replacement leading-space count |
| `--target-keys` | ❌ | Only re-indent lines whose sub-key matches one of these (composer auto-quotes) |
| `--dry-run` | ❌ | Print rewritten block, do not save |

### Behaviour

1. Builds block pattern: `"<key>":\s*\{.*?\n[ \t]*\}` (DOTALL applied by base).
2. Creates a `.bak` copy (composer-owned, so rollback is possible).
3. Invokes the base script with `--no-backup` (avoids double-backup).
4. After base returns success, runs `json.loads` on the file.
5. On JSON parse failure → restores from `.bak` and exits non-zero.
6. On success → leaves `.bak` in place for manual rollback if needed.

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Success (or dry-run completed) |
| 1 | Base failure, JSON parse failure (rolled back), or invalid args |

***

## 3. Path Resolution to Base Skill

The composer resolves the base script via a `__file__`-anchored path:

```python
BASE_SCRIPT = os.path.normpath(os.path.join(
    SCRIPT_DIR, "..", "..", "text-block-indent-override", "scripts",
    "text-block-indent-override.py",
))
```

This works regardless of the caller's `cwd` and complies with the **Portable Anchored Paths**
mandate. The composer verifies the base script exists and exits with a clear error if it is
missing, per the **Layered Composition Mandate**.

***

## 4. Composition by Higher-Level Skills

| Composer | Domain | Adds on top of JSON awareness |
| :--- | :--- | :--- |
| [vscode-settings-indent-override](../vscode-settings-indent-override/SKILL.md) | VS Code `settings.json` | Profile paths, known keys, post-promotion workflow, SSOT-symlink awareness |

***

## 5. Related Skills

- [text-block-indent-override](../text-block-indent-override/SKILL.md) (base)
- [vscode-settings-indent-override](../vscode-settings-indent-override/SKILL.md) (downstream composer)
- [vscode-settings-promotion](../vscode-settings-promotion/SKILL.md) (sibling — promotes settings;
  composer below chains *promote → indent override*)
