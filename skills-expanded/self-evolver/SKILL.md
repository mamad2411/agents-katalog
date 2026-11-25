---
name: self-evolver
description: Merge demonstrated workflow failures and user corrections into evidence-backed rule improvements. Project preferences belong to project-knowledge, not global rule evolution.
---

# 自进化技能 (self-evolver)

## Purpose

把真实纠正、失败和流程摩擦转成可追溯、可验证的规则改进；先积累证据，再用最小补丁消除可复现缺陷。

## Trigger

- 用户明确要求沉淀教训。
- 同类普通信号累计达到 3 次。
- 单次出现安全、隐私、数据损坏、错误发布或越权等严重事件。
- 测试/审查证明规则缺陷，或规则与宿主能力存在可复现冲突。
- 安全检查点发现信号台账存在待处理项。

一次性普通外部故障不是规则信号；只有可复现的流程缺陷才采集。用户明确要求优化时不等待累计阈值。

## Required context

- `EVOLUTION.md`。
- `.creator/evolution/signals.md`（兼容保留并核对旧 `.codex/evolution/signals.md`、`.claude/evolution/signals.md`）；不存在时按模板创建。
- 相关 `AGENTS.md`、Skill、阶段契约和可验证证据。
- 能复现旧行为并验证新规则的 Prompt 行为用例。

## Workflow

1. 使用“关联 Skill + 问题类别”查重并追加证据，不重复建条目。
2. 将普通首次信号标为“观察中”；累计 3 次或严重单次事件转为“待处理”。
3. 先修改、合并或删除现有规则，只有结构无法覆盖时才新增。
4. 每个应用的补丁至少绑定一个失败前可复现、修改后可验证的 Prompt 用例。
5. 运行获准的静态契约和相关行为回归；真实任务测试被用户保留时明确待验证，超出已有授权的政策变更才请求确认。
6. 更新台账状态、改动理由和验证证据。
7. 补丁登记修改文件、被替代规则、新规则和关联用例，供升级时重新评估，不自动回放；源码版本开发可用 Changelog 与开发记录留痕。

## Output

- 更新后的信号台账。
- 被修改、合并或删除的规则及理由。
- 关联行为用例与验证结果。
- 需要用户确认的高风险变化和残余风险。

## Stop or escalate

- 只有理论偏好、个人习惯、一次性普通外部故障或普通产品需求：不得直接进化。
- 信号证据不足但影响主流程或多个 Skill：标为“待确认”。
- 变更会降低审查、隐私、安全或发布标准：必须用户确认。
- 无法构造回归用例：保留信号，不应用补丁。

## References

执行前读取 [stage-contract.md](references/stage-contract.md)。

授权说明：用户已明确要求本次规则优化时按已有范围执行，不因跨多个 Skill 重复确认。用户保留真实任务测试时，只报告获准的结构/脚本检查，不擅自试跑或声称行为通过。
