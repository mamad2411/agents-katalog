---
name: agent-task-lifecycle
description: >
  初始化或维护代码库中的 task 生命周期能力，包括任务识别、切换保护、目录化 task
  跟踪模板与归档规则。适用于建立 task tracking、task switch guard、one-task-one-stream 并行规则（每任务独立会话/工作目录）或 tasks 归档流程；
keywords: 初始化 task 生命周期, 建立 tasks 规范, 任务切换保护, setup task lifecycle, task switch guard.
---

# agent-task-lifecycle

为任意代码库补齐 Agent 的 task 生命周期能力，确保任务识别、任务切换与归档流程可执行、可追踪；复杂任务统一使用目录结构，并以 `context.md`、`plan.md`、`progress.md`、`decisions.md` 作为标准文件；如任务需要脚本或输出落盘，可在任务目录内按需创建 `scripts/` 与 `scripts/outputs/`。

本 skill 负责 task 生命周期治理（任务识别、切换保护、记录与归档），不负责创建或切换 git 分支/worktree；分支与 worktree 由用户自行创建并切换到目标工作目录后再继续执行。

开始执行前，先阅读 [references/instructions.md](references/instructions.md)；交付前对照 [references/checklist.md](references/checklist.md)；输出格式遵循 [references/output-contract.md](references/output-contract.md)。

## 何时使用

- 需要引入 Task Identification First 与 Task Switch Guard
- 需要强制“每个新任务都以新并行线程开始”（one-task-one-stream，线程由用户准备）
- 需要生成目录化 task 模板与 tasks / archive 生命周期目录
- 需要统一复杂任务的记录与归档规范

### 常见触发线索

- 用户提到“初始化 task 生命周期”“建立 tasks 规范”“任务切换保护”
- 用户提到“同时开多个任务但避免冲突”“新任务必须新线程”
- 用户希望 “setup task lifecycle” 或 “task switch guard”

## 何时不使用

- 仅需维护与 task 无关的仓库文档或单个非 task 规则文件时
- 项目已有完整且无需变更的 task 生命周期规则时

## Inputs

- `codebase`：默认使用 Agent 当前工作目录作为目标代码库根目录，无需显式传入
- `target_language`（可选）：生成 task 生命周期文档时使用的目标语言（如 `zh-CN`、`en-US`）；未显式提供时按语言判定规则自动识别

## Outputs

- `.agents/templates/task-template.md`
- `.agents/tasks/README.md`
- `.agents/tasks/index.md`（可选，用于 task 与会话/工作目录映射）
- `.agents/tasks/archive/`
- `.agents/guide/execution.md`（追加 task 生命周期规则）
- `.agents/memory/decisions.md`（记录 task 规则相关决策）

## 默认隔离策略（内置）

- 每个新任务必须在独立线程中执行（独立会话 + 独立工作目录）。
- 分支与 worktree 由用户自行创建并切换；本 skill 不自动执行 `git branch` / `git worktree` 操作。
- 任务切换时，不在当前目录直接实现新任务；应先提示用户完成切换，再继续在新目录执行。

## Files

| 文件 | 职责 |
|------|------|
| [references/instructions.md](references/instructions.md) | 完整执行指令（Agent 执行时必读） |
| [references/checklist.md](references/checklist.md) | 输出验收检查清单 |
| [references/output-contract.md](references/output-contract.md) | 产物结构与内容规范 |
| [assets/prompt-template.md](assets/prompt-template.md) | 可直接发送给 Agent 的完整 prompt 模板 |
| [references/bootstrap-empty-repo.md](references/bootstrap-empty-repo.md) | 首次建立 task 生命周期示例 |
| [references/update-existing-agent-task-lifecycle.md](references/update-existing-agent-task-lifecycle.md) | 增量更新 task 规则示例 |

