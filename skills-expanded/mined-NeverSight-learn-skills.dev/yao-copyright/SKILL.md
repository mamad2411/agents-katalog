---
name: yao-copyright-skill
description: Use when adding or auditing Yao copyright comment headers for an agent skill package, especially SKILL.md, README.md, references, prompts, templates, examples, scripts, YAML, or TOML files.
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-copyright-skill
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao Copyright Skill

## Overview

Add copyright comment headers to a specified skill package without breaking route metadata, executable shebangs, or strict data formats.

## When To Use

Use this when the user asks to:

- 给某个 Skill 增加版权注释、版权声明、作者注释
- 批量处理 `SKILL.md`、`README.md`、`references/`、`prompts/`、`templates/` 或 `examples/`
- audit whether a skill package already has Yao copyright comments
- add headers to scripts or YAML/TOML configs while skipping JSON and lock files

Do not use this for legal drafting, license selection, or visible website footer copy unless the user explicitly asks for that output.

## Workflow

1. Identify the target skill directory. If the user only names a skill, resolve its installed path before editing.
2. Read `references/copyright-comment-policy.md` for target files, skip rules, and comment styles.
3. Run a dry run first:

```bash
python3 scripts/add_copyright_comments.py /path/to/target-skill --dry-run
```

4. Apply the core Markdown pass unless the user requested a broader scope:

```bash
python3 scripts/add_copyright_comments.py /path/to/target-skill
```

5. For scripts and YAML/TOML configs, use the full scope:

```bash
python3 scripts/add_copyright_comments.py /path/to/target-skill --scope all
```

6. Verify with `git diff` or a targeted file read. Confirm `SKILL.md` frontmatter still starts at line 1.

## Defaults

- `Project` defaults to the target skill directory name.
- `Date` defaults to `2026-05-16`.
- `Author` defaults to `姚金刚`.
- `X` defaults to `https://x.com/yaojingang`.
- JSON, lock files, generated files, caches, build outputs, and `reports/` are skipped.

## Output Contract

Report which files changed, which files were skipped because they already had a notice, and any files deliberately left untouched because comments would be unsafe.
