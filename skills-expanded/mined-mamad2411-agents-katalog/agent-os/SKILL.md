---
name: agent-os
description: >
  初始化或更新代码库中的 Agent OS 文档基础设施，包括 `AGENTS.md`、`.agents/guide/`
  与 `.agents/memory/`。适用于建立长期、低上下文成本的 agent 工作流；
keywords:
  初始化 agent-os, 生成 AGENTS.md, 建立 .agents 目录, setup agent os, bootstrap agent environment.
---

# agent-os

为任意代码库建立 AI Agent 操作系统级环境，使 Agent 可长期稳定、低上下文成本地工作。

开始执行前，先阅读 [references/instructions.md](references/instructions.md)；交付前对照 [references/checklist.md](references/checklist.md)；输出格式遵循 [references/output-contract.md](references/output-contract.md)。

## 何时使用

- 新项目首次引入 AI Agent 工作流
- 现有项目 `.agents/` 缺失或需要同步更新
- 需要统一 AGENTS 入口与 guide/memory 基线时

### 常见触发线索

- 用户提到“初始化 agent-os”“生成 `AGENTS.md`”“建立 `.agents/` 目录”
- 用户希望 “setup agent os” 或 “bootstrap agent environment”

## 何时不使用

- 仅修改单个 `.agents/` 子文件时（直接编辑目标文件即可）
- 项目已有完整 Agent OS 且无需变更时

## Inputs

- `codebase`：默认使用 Agent 当前工作目录作为目标代码库根目录，无需显式传入
- `target_language`（可选）：生成 Agent OS 文档时使用的目标语言（如 `zh-CN`、`en-US`）；未显式提供时按语言判定规则自动识别

## Outputs

- `AGENTS.md`（项目根目录，20–40 行入口索引）
- `.agents/guide/*.md`（`execution` / `patterns` / `safety` / `dependencies` / `i18n`）
- `.agents/memory/context.md`
- `.agents/memory/decisions.md`
- `.agents/scripts/`（脚本文件目录）
- `.agents/scripts/outputs/`（脚本与检查结果输出目录）
- `.agents/README.md`（`.agents` 目录说明与 Script First 最佳实践）

## Files

| 文件 | 职责 |
|------|------|
| [references/instructions.md](references/instructions.md) | 完整执行指令（Agent 执行时必读） |
| [references/checklist.md](references/checklist.md) | 输出验收检查清单 |
| [references/output-contract.md](references/output-contract.md) | 产物结构与内容规范 |
| [assets/prompt-template.md](assets/prompt-template.md) | 可直接发送给 Agent 的完整 prompt 模板 |
| [references/bootstrap-empty-repo.md](references/bootstrap-empty-repo.md) | 空项目初始化示例 |
| [references/update-existing-agent-os.md](references/update-existing-agent-os.md) | 增量更新已有 Agent OS 示例 |
