---
name: skill-builder
description: Create or refactor creator.skill capabilities when an existing skill cannot cover the required boundary. Maintain concise triggers, shared contracts and meaningful regression cases.
---

# 技能构建技能 (skill-builder)

## Purpose

建立职责明确、可触发、可验证并与三路由及风险门禁一致的可复用技能，而不是增加百科式说明。

## Trigger

- 新能力无法由现有 Skill 合理承担。
- 现有 Skill 需要重构其触发边界、契约或验证方式。
- 纯文案调整或通用 Agent 行为不需要新 Skill。

## Required context

- 当前 `AGENTS.md`。
- 1～2 个职责最接近的现有 Skill 及阶段契约。
- 新能力的触发/非触发场景、输入、输出、合格标准和红线。
- 至少一个正例、一个边界反例和可自动检查的行为用例。

## Workflow

1. 先证明职责不与现有 Skill 重叠，并确定三路由中的位置。
2. 创建 `SKILL.md`、`agents/openai.yaml` 和必要的 `references/stage-contract.md`。
3. `SKILL.md` 使用 Purpose、Trigger、Required context、Workflow、Output、Stop or escalate、References 七个统一章节。
4. 将详细模板、检查表和 Examples 放入阶段契约，入口保持短而明确。
5. 更新 Prompt 用例集、YAML 展示信息和相关文档。
6. 运行结构校验、YAML 解析、Prompt 契约评测、构建与验证。

## Output

- 完整技能目录和职责说明。
- 触发/非触发边界、阶段契约与 Examples。
- `agents/openai.yaml` 展示名、描述和显式引用 `$skill-name` 的默认提示。
- 新增或更新的行为用例和验证证据。

## Stop or escalate

- 职责可由现有 Skill 承担：修改现有 Skill，不新增目录。
- 拟改规则超出已有授权、或触及未授权权限/发布边界：仅暂停依赖该选择的部分。
- 没有可测试边界或只复制通用行为：打回。
- 不得伪造完成/验证或放宽未授权安全边界；用户已授权的风险与审查政策校准应同步更新规则、用例和证据。

## References

执行前读取 [stage-contract.md](references/stage-contract.md)。

授权说明：用户已明确要求本次规则优化时按已有范围执行，不因跨多个 Skill 重复确认。用户保留真实任务测试时，只报告获准的结构/脚本检查，不擅自试跑或声称行为通过。
