---
name: product-spec-builder
description: Turn an idea or product change into testable requirements. Use when intended user behavior or scope is unresolved; skip repeated interviews for already confirmed changes.
---

# 需求构建技能 (product-spec-builder)

## Purpose

从用户文字中拆出真实目的、用户、场景、边界和成功条件，形成可验收的产品契约；不要把一句话包装成完整需求。

## Trigger

- 0→1：产品目标、用户、核心场景或首版范围尚未形成。
- 产品变更：新增或改变外部行为，但变更目的、范围、兼容性或验收记录仍缺失/不充分。
- “Bug 修复”实际需要重新定义正确行为。

有效决定已确认目的、外部行为和验收标准时，单一小改直接进入 `dev-builder`，需要阶段计划才进入 `dev-planner`；仅恢复既定行为、内部重构、测试、CI 或文档时不触发。

## Required context

- 用户原始想法、痛点或变更请求。
- 已有 Product Spec、仓库事实、接口和设计材料（如果存在）。
- 已确认约束、参考案例、截图、反例和不可接受结果。
- 当前已知事实、推断和未知项。

## Workflow

1. 先判断 0→1、产品变更或维护执行，不按用户使用的“优化/修复”字眼机械分类。
2. 抽取已知目的、目标用户、核心场景、外部行为、范围和非目标。
3. 只追问必要且未决的体验边界：用户能力、交互/默认行为、兼容性、显著成本、隐私/知识作用范围或缺失授权。已有决定不重问；工程实现与可自行核查的事实直接处理，每轮最多 2 个问题。
4. 信息足够时停止追问，把未知项写成临时假设或明确阻塞。
5. 0→1 生成 Product Spec；产品变更原位修订条款，标明待实现和旧决定替代关系。历史明细按需移出当前正文，不只追加相反声明。
6. 明确且可复用的项目准则交给 project-knowledge 原位沉淀；一次性例外与助手推断不能自动变成长期用户偏好。未决问题只暂停其依赖部分。

## Output

- 路线与依据。
- 已确认事实、临时假设和待确认问题。
- 编号需求 `REQ-*` 与可观察验收标准 `AC-*`。
- `docs/Product-Spec.md` 或项目约定文件；产品变更包含变更 ID、兼容性、迁移、回滚和非目标。

## Stop or escalate

- 无法判断是恢复行为还是重新定义行为：最多追问 2 个关键问题。
- 目标用户、核心场景或成功条件缺失且会改变方案：停止等待确认。
- 依赖未确认的外部接口或业务规则：记录阻塞，不编造答案。
- 产品契约已充分且请求只是维护：转交 `bug-fixer` 或 `dev-builder`。

## References

执行前读取 [stage-contract.md](references/stage-contract.md)。
