---
name: project-development-v2-common
description: 项目开发 v2 skill 套件的共享政策和交付契约。当维护、审查、分享或挂载 requirements-workshop-v2、tech-design-v2、implementation-planning-v2、plan-execution-v2 使用的公共文档时使用；当任务涉及 v2 提问策略、交付契约或禁止模拟完成策略时也使用。
---

# 项目开发 v2 公共协议

维护项目开发 v2 流程使用的共享规则。本 skill 不是面向用户的开发阶段，而是四个阶段 skill 的公共政策层。

## 范围

本 skill 维护：

- `references/question-policy.md`
- `references/delivery-contract.md`
- `references/no-simulation-policy.md`

以下阶段 skill 会读取这些引用：

- `requirements-workshop-v2`
- `tech-design-v2`
- `implementation-planning-v2`
- `plan-execution-v2`
- `project-development-review-v2`

## 维护规则

- 跨阶段共用的规则放在这里，不要复制到各阶段 skill。
- 各阶段 `SKILL.md` 保持简短，直接引用这里的文档。
- 当规则影响多个阶段时，更新本 skill。
- 只有阶段专属规则才修改对应阶段 skill。
- 除非同步更新所有下游模板，否则不要改变可追踪契约。

## 引用指南

只读取当前任务需要的文件：

- 修改 agent 如何提问或避免提问时，读 `references/question-policy.md`。
- 修改 ID、状态值、版本目录、交接规则、可追踪性或证据标准时，读 `references/delivery-contract.md`。
- 修改 mock、stub、fallback、验证或完成语言相关规则时，读 `references/no-simulation-policy.md`。
- 修改阶段后审查、跨文档一致性或审查报告结构时，优先修改 `project-development-review-v2`。

## 兼容性

修改本 skill 后，检查这些文件中的引用路径仍然有效：

- `../requirements-workshop-v2/SKILL.md`
- `../tech-design-v2/SKILL.md`
- `../implementation-planning-v2/SKILL.md`
- `../plan-execution-v2/SKILL.md`
- `../project-development-review-v2/SKILL.md`

除非同一次改动更新四个阶段 skill，否则不要移动公共引用文件。
