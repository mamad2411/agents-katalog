---
name: checkpoint-persist
description: >-
  多步骤 / 多子项长任务的中间结论增量落盘。门控触发（CP-001）：非平凡任务 + 存在 ≥2 个
  需分别产出的子结论 + 子结论需跨轮存活，三条全满足时，每产出一个子结论立即追加写入
  checkpoint 文件，防止上下文超窗 / 压缩导致已产出结论丢失。全局门控，不绑定 plan-grill
  盘问或任何特定 skill，全局适用。
locale: zh-CN
supported_locales: [zh-CN]
---

# Checkpoint Persist

## 强制入口

命中本 skill 时，**必须先完整阅读** [references/checkpoint_persist.md](references/checkpoint_persist.md) 并按其中条款执行。

- 不得以 preamble、摘要或其它二次摘要代替该文件全文。

## 何时加载

- **门控触发（CP-001）**：非平凡任务（构建 / 修改 / 方案 / 迁移 / 审查 / 排障，复用 historical-recall `HR-001` 定义）+ 存在 ≥2 个需分别产出的子结论 + 子结论需跨轮存活，三条全满足才触发；每产出一个子结论立即落盘。
- **跳过**：trivial 任务、单轮可完成、单点子结论、事实查询 / 翻译 / 简单解释 / typo / 小命令 / 纯闲聊。
- **与 historical-recall 的分工**：`historical-recall` 负责「动手前召回历史」（读），本 skill 负责「动手后边做边落盘」（写）；两者是同一套「非平凡」门控下的两个方向，触发定义保持一致。

## 规则索引（owned rule IDs）

本 skill 的契约由下列 `CP-NNN` 规则承载，真值登记在 [references/rule_index.md](references/rule_index.md)。行为门禁 `scripts/validate-skill-behavior.sh` 的 Check 2 校验 ID 集合双向一致（SKILL.md 声明的 ID 均被定义；rule_index.md 中 active 行均被 SKILL.md 声明）。

- [CP-001] 触发门控：非平凡 + ≥2 子结论 + 跨轮存活三条全满足才落盘；trivial / 单轮可完成 / 单点子结论 / 闲聊跳过。
- [CP-002] 落盘对象与粒度：只落「结论 + 关键决策 + 未决问题」，不落对话过程与思考流；最小单元 = 单个子结论。
- [CP-003] 落盘时机：每产出一个子结论立即追加，禁止攒批到末尾；感知上下文将超窗 / 压缩时优先落盘。
- [CP-004] 落盘位置与格式：固定写 `<工作区根>/.plan-reviews/checkpoint/<task-slug>/CHECKPOINT.md`；格式统一，压缩后可按约定路径找回。
- [CP-005] 恢复与生命周期：新轮次先读进行中的 checkpoint 恢复上下文；任务完成（结论已入成品产出）后清理；落盘失败 best-effort 不阻断主任务。
