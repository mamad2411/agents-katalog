---
name: prompt-optimizer
description: 提问优化器。用户主动请求优化提问/prompt（如「帮我优化提问」「优化这个 prompt」「改写我的问题」）时，先召回相似历史提问、复用 plan-grill 盘问澄清真实需求，再把模糊提问改写为结构化高质量提示词，透明展示供用户确认或修正，确认前不回答原问题；用户显式跳过确认时仍先展示优化稿并标注「未确认假设」，再基于优化稿回答；最后回写 .plan-reviews 形成闭环。仅主动触发，不做发送时自动拦截。
locale: zh-CN
supported_locales: [zh-CN]
depends_on: [plan-grill, historical-recall]
---

# Prompt Optimizer

## 强制入口

命中本 skill 时，**必须先完整阅读** [references/prompt_optimizer.md](references/prompt_optimizer.md) 并按其中条款执行。

- 不得以 preamble、规则摘要或其它二次摘要代替该文件全文。
- 盘问规则**复用 `plan-grill`** 的 interview 子集（PG-000 门控 + PG-001~PG-003 逐一盘问，不复用 PG-004 锁定产出，故不产出 PLAN.md），历史召回**复用 `historical-recall`**（HR-001~HR-005），本 skill 不内联重复这两套规则，只做「澄清 + 改写 + 展示 + 回答 + 回写」这层增量。

## 六条核心规则

- [POPT-001] 触发门控：仅主动触发（`@prompt-optimizer` 或「帮我优化提问」「优化这个 prompt」「改写我的问题」），不做「发送时自动拦截」。
- [POPT-002] 历史召回：改写前针对原始提问 recall 相似历史；历史澄清结论仅作待验证线索，据此跳过盘问须标注「未澄清假设（来源：历史线索）」。
- [POPT-003] 盘问判定与澄清：复用 plan-grill PG-000 门控 + PG-001~PG-003（仅 interview，不产出 PLAN.md），存在阻塞性歧义时先逐一盘问澄清，无歧义直接改写。
- [POPT-004] 改写：宿主 AI 基于「盘问澄清 + 历史线索」把原始提问重写为结构化高质量提示词，并满足改写验收判据。
- [POPT-005] 透明确认与回答：先展示优化后提示词并以「请确认或修正以上优化稿；确认前不回答原问题。」收尾；确认前不回答原问题，确认后基于它回答；用户显式跳过确认时仍先展示优化稿、标注「未确认假设」后基于优化稿作答，改写改变对象或事实前提时不得跳过。
- [POPT-006] 回写闭环：把原始提问、澄清结论、优化后提示词分别归档到 `.plan-reviews/<date-slug>/` 下的 `QUESTION.md` / `CLARIFICATION.md` / `OPTIMIZED.md`（`PROMPT-OPTIMIZATION.md` 仅存一行标题；`OPTIMIZED.md` 容纳确认版 / 修正版 / 豁免确认版）并 `sync` 回灌知识库。

细则见 [references/prompt_optimizer.md](references/prompt_optimizer.md)，规则 ID 真值登记在 [references/rule_index.md](references/rule_index.md)。

## 入口语义

- **主动触发**：用户输入「帮我优化提问」「优化这个 prompt」「改写我的问题」或 `@prompt-optimizer`。
- **不触发**：普通对话、事实查询、代码生成等未请求优化的输入；本 skill 不做「发送时自动拦截」，不参与非优化类任务的执行。

## 与相邻 skill 的分工

| Skill | 分工 |
|-------|------|
| `historical-recall` | 动手前召回 `.plan-reviews/` 历史线索（POPT-002 委托其 `recall`，自身只读） |
| `plan-grill` | 需求盘问（POPT-003 委托其 PG-000 门控 + PG-001~003；仅 interview，不产出 PLAN.md） |
| **prompt-optimizer（本 skill）** | 澄清后改写提问、透明展示、基于优化版回答、回写闭环 |
| `cognitive-reasoning` | 回答环节的论证质量与真值接地（正交约束，不改变本 skill 流程） |
