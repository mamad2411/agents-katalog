---
name: goal-writer
description: Write a bounded, recoverable Goal with measurable acceptance only when the user explicitly requests a persistent or long-running goal. Never create unlimited retry loops.
---

# Goal 编写技能 (goal-writer)

## Purpose

把长期任务写成 Agent 能自主执行、明确停止、失败后恢复并用证据验收的单一 Goal。

## Trigger

- 仅当用户明确要求持久或长期 Goal（如持续执行、托管）时启用。
- 任务耗时较长、需要多个工具调用或宿主可自动执行，本身不触发本技能。
- 普通单轮任务不需要额外 Goal 文件。

## Required context

- 唯一目标、范围和非目标。
- 当前状态、依赖、授权与可用资源。
- 可观察完成标准和验收证据。
- 最大重试/复审边界、中断条件和恢复入口。

## Workflow

1. 将愿望改写为单一、有限、可完成的目标。
2. 写出可观察完成标准和可复现验收方式。
3. 明确授权边界、最大重试次数、reviewer 收敛条件和外部依赖。
4. 规定容量、网络、工具或宿主故障时的中断状态与恢复检查点。
5. 检查 Goal 不会通过“永远继续”“不断生成 reviewer”等文字制造无限循环。

## Output

- 可直接发送给 Agent 的 Goal 块。
- 目标、范围/非目标、完成标准、验收方式。
- 停止条件、失败条件、重试上限和恢复方式。
- 需要用户先授权或决策的事项。

## Stop or escalate

- 目标包含互相依赖的多个大型结果：拆分后再输出。
- 完成标准不可观察或依赖未确认信息：停止并指出缺口。
- 用户要求无限重试、无限审查或规避容量/权限限制：改写为有界目标并明确说明。
- 必须扩大外部权限才能执行：请求用户授权，不自行扩权。

## References

执行前读取 [stage-contract.md](references/stage-contract.md)。
