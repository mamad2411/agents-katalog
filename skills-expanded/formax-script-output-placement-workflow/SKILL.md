---
name: formax-script-output-placement-workflow
description: Use when adding or modifying generator scripts that write files; keeps generated artifacts out of docs/ and aligns script defaults with ownership paths plus CI gate updates.
---

# Formax Script Output Placement

## Goal

新增或修改“会写文件”的脚本时，避免把机器产物放到 `docs/`。

## Placement Rules

1. `docs/` 只放文档与静态说明素材，不放机器生成基线/报告。
2. 产物就近放到 owner 目录：
   - app 产物 -> `apps/<name>/perf/`
   - repo 级脚本产物 -> `scripts/baselines/`
   - 临时产物 -> `.tmp/`（gitignored）
3. 生成脚本默认输出路径应指向 owner 目录，不指向 `docs/**`。
4. 建议提供 `--output` 或 `--baseline` 覆盖参数（便于 CI 与本地临时切换路径）。

## Minimal Workflow

1. 先定产物 owner 与默认输出目录。
2. 再写脚本和默认路径（owner-local）。
3. 同步更新 README/learning 里的路径引用。

## Checks

- `node ./scripts/check-docs-artifact-placement.mjs`
