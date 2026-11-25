---
name: typescript-import-formatting
description: Convert TypeScript/TSX multi-valued named imports into canonical multiline import blocks.
category: Code-Style
---

# TypeScript Import Formatting Skill (v1)

This skill converts multi-valued named imports in TypeScript and TSX source files into canonical multiline import blocks. It is intended for code style cleanup and readability improvements while preserving default imports, namespace imports, and side-effect imports.

***

## 1. Layering Decision

Per [Skill Factory §2.0](../skill-factory/SKILL.md#20-layering-decision-base-vs-composer), this skill is **Atomic** at v1. The workflow is specific to TypeScript/TSX import formatting and has no reusable primitive that another domain would need.

## 2. Environment & Dependencies

| Requirement | Verification |
| :--- | :--- |
| Python 3.12+ | `python3 --version` |
| Valid TS/TSX file path | `test -f <path>` |
| Skill script | `python3 .agents/skills/typescript-import-formatting/scripts/typescript-import-formatting.py --help` |

No external Python packages are required.

## 3. Trigger Conditions

Invoke this skill when:

1. A TypeScript or TSX file contains named imports with 2 or more specifiers on a single line.
2. The file should be normalized to a multiline named-import style before review, refactor, or PR submission.
3. You want to preserve import semantics while improving readability.

## 4. Operational Procedure

1. Run the formatting script:

```bash
python3 .agents/skills/typescript-import-formatting/scripts/typescript-import-formatting.py \
  --file <path/to/file.tsx>
```

2. If you want to preview the change first, add `--dry-run`.

3. The script rewrites imports such as:

```ts
import { A, B, C } from 'module';
```

into:

```ts
import {
  A,
  B,
  C,
} from 'module';
```

4. If the import already uses multiline named imports or has only one specifier, the skill makes no change.

## 5. Verification

- Validate the script syntax with:

```bash
python3 -m py_compile .agents/skills/typescript-import-formatting/scripts/typescript-import-formatting.py
```

- Run the file's normal TypeScript formatting or linting after the edit.

- Confirm the edited import blocks are multiline and preserve default imports, e.g.:

```ts
import React, {
  useState,
  useEffect,
} from 'react';
```
