---
name: codex-search
description: Codex search wrapper with auto routing. fast=one-shot(no context pollution), balanced=temp session, deep=persistent session for long tasks.
---

# Codex Search

## Modes
- auto: detect task type automatically
- fast: one-shot, no context carry-over
- balanced: temporary session per run, then close
- deep: persistent session for long multi-turn jobs

## Usage
```bash
~/.local/bin/codex-search "搜索：xxx，给来源" "$PWD"
~/.local/bin/codex-search --mode fast "搜索：xxx" "$PWD"
~/.local/bin/codex-search --mode deep "深度任务...FINAL_REPORT_READY" "$PWD"
