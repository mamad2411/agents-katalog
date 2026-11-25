---
name: xhs-content-review
description: 对小红书品牌内容执行两阶段机器初审。用户要求检查平台安全、食品广告合规、品牌调性、事实与版权，或评价标题封面吸引力、结构清晰度、实用性和视觉节奏，并决定通过或返工时使用。
---

# 小红书内容初审

## 输入

- outputs/ 下对应内容需求文件夹中的全部内容产出（包括 content.md、封面图、内容图）
- 商品事实、核准/禁用宣称、品牌调性
- 平台策略版本
- 可选历史优秀内容基线

先读取 [references/compliance-checklist.md](references/compliance-checklist.md)、[references/quality-rubric.md](references/quality-rubric.md) 和 [references/review-contract.md](references/review-contract.md)。必须先阶段一，再阶段二；阶段一未通过时不得用高质量分掩盖硬错误。

## 阶段一：做得对
1. 运行内容生成 Skill 的确定性校验器，确认标题、正文、图片、标签和高风险词。
2. 检查平台安全、食品广告、事实来源、品牌调性、商品包装一致性、版权/肖像/商标和站外导流。
3. 任一 `blocking` 问题存在即 `failed`。
4. 输出逐项证据和精确修改指令，不使用“再优化一下”之类空话。
5. 失败时生成 `RevisionBrief`，返回给主Agent。

## 阶段二：做得好

仅在阶段一通过后执行：

1. 按标题钩子、封面信息力、结构清晰度、实用性、产品融入、视觉节奏和自然表达评分。
2. 使用 `python3 scripts/review_gate.py` 汇总加权分。
3. 总分至少 80，且任一维度不得低于 65，方可通过。
4. 失败时输出对用户价值最有影响的 1-3 个问题，返回给主Agent。

## 审核纪律

- 合规判断必须引用具体文本、图片编号或商品字段。
- 不把“可能爆”当作质量证据，不保证流量结果。
- 不泄露或记录模型隐藏推理链，只输出审核摘要、证据和判定。
- 审核模型与生成模型可使用不同提示词或模型配置，避免自我确认偏差。

## 输出

严格返回 `InitialReviewResult`。两阶段均通过后状态为 `awaiting_human_review`，将审核报告写入 outputs/ 对应内容需求文件夹中的 review.md。

