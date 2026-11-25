---
name: plan-implement
description: Implement a project plan by executing its numbered steps and checking off completed items. Use when the user asks to implement a plan, execute plan steps, run a plan file, or complete tasks from a plan.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Plan Implement

## 适用场景

当用户要求：
- 实施/执行某个 plan 文件
- 完成计划中的部分或全部步骤
- 按编号执行指定步骤

## 参数

1. `plan_file`：plan 文件路径（必填）。
2. `steps`（可选）：步骤编号，多个用逗号或空格分隔。例如 `1,3,5` 或 `1 3 5`。未指定时执行全部未勾选步骤。

## 操作约束

仅在以下范围内操作，超出范围必须先向用户确认：

1. **文件修改范围**：仅修改 `plan_file` 本身（更新 checkbox），以及计划正文中「需要修改的文件」清单列出的文件；不修改清单外的任何文件。
2. **命令执行范围**：仅执行计划步骤「具体工作」中明确列出的命令或操作；不执行计划外的新命令。
3. **危险操作限制**：删除文件、修改系统配置、安装依赖、推送代码、修改 git 历史等操作，执行前必须先向用户确认。
4. **工具最小化**：仅在当前步骤必要时才调用 `allowed-tools` 中声明的工具，不主动调用未声明的工具。
5. **进度可见**：每一步执行前简要说明将要做什么；执行后报告结果与文件变更。

## 工作流程

1. 读取 `plan_file` 文件内容。
2. 解析所有带 checkbox 的编号步骤：
   - 步骤编号以 Markdown 有序列表数字为准。
   - checkbox 形式为 `- [ ]` 或 `- [x]`。
3. 如果指定了 `steps` 参数，仅保留对应编号的步骤。
4. 默认跳过已勾选（`- [x]`）步骤，除非用户明确要求重新执行。
5. 按顺序执行每个待实施步骤：
   - 严格遵循该步骤中"实施方案"的说明。
   - 调用工具前确认符合「操作约束」中的限制。
   - 每一步完成后，将该步骤的 checkbox 从 `- [ ]` 改为 `- [x]`。
   - 保存文件。
6. 若执行过程中出现错误，停止并报错，不再继续后续步骤。
7. 完成所有步骤后，简要汇报执行结果与更新的 checkbox 状态。