---
name: dev-builder
description: Implement a defined product or maintenance change, integrate results and verify relevant behavior. Use bug-fixer for unknown failure causes; independent review depends on concrete risk.
---

# 开发实施

## Purpose

完成最小完整变更，证明可观察行为并留下下一会话所需的当前事实。

## Trigger

目标、预期行为、范围和验收足够明确；可以是产品短任务、Phase 或非诊断型维护。

## Required context

现状入口、有效需求/设计、相关任务或 Phase、工作区修改、验证入口和授权；只读相关材料。

涉及 UI 时，在实施前按[读取流程](../../../.creator/references/project-design.md)读取项目已采用规范及适用的逐层引用，检查组件/tokens/素材与有效例外。直接开发或维护也不省略；不加载未采纳的设计参考库或用其新版本改写项目规则。无 UI 任务不加载设计手册。

## Workflow

1. 确认路线、规模和具体影响。符合 Phase 条件却缺计划时先补计划，其余短任务直接执行。
2. 核对代码与他人修改，按当前有效契约实施；新决定替代旧规则时先对账，不以代码差异静默改需求。
3. 用针对性行为检查验证；必要构建/测试通过后，有新变更、失败或疑点才重复。
4. 验证后更新受影响现状、需求状态、设计和计划；无影响的入口不机械刷新。
5. 按任务可分离性与收益选择有边界的子代理，明确文件归属并由主会话集成；风险决定独立审查而非是否可委派。R0/R1 不自动审查；轻量维护进入 batch.md，小型产品变更保留需求/短任务。R2 使用 fresh reviewer，尊重用户/宿主限制。
6. 聚焦处理审查发现，有实质修复可再复核，无进展或资源预算用尽时保存恢复检查点。
7. 在安全收尾点使用 project-knowledge 沉淀明确项目准则和受影响现状；撤销能力时关闭失效任务及测试义务，不能把历史未验收项重新列为待办。完成整个已授权目标和必要集成后交接，不因一个子任务结束提前退出。

## Output

实现结果、相关契约与文件、验证结果及适用基线、更新的文档、按需拆分的实施/验证/审查/发布状态和下一步。

## Stop or escalate

未知正确行为影响方案时只暂停相关部分。不能以验证缺口代替完成，也不能因为工具失败或多个文件就自动升 R2。外部动作按已有明确授权边界执行。

## References

交付时读 [stage-contract.md](references/stage-contract.md)；文档、队列及审查细则读[共同契约](../../../.creator/references/workflow-contract.md)。

验证修复或需要判断检查是否有效时读[验证方法](../../../.creator/references/verification.md)；实现或验证 UI 变更时读[项目 UI 实现与验证](../../../.creator/references/project-design.md#verify-the-adopted-design)。
