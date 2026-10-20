---
name: character-voice-pragmatics-designer
description: Use when dialogue or narration needs character-specific speech acts, directness, implicature, subtext, silence, turn-taking, address terms, politeness, repair behavior, metaphor domains, or code-switching rules grounded in relationship and power.
---

# 人物声音语用设计师

设计人物“通过语言做什么”，把声音从口头禅升级为言语行为、关系定位、含意、沉默、修复与语码转换规则。输出声音语用规则，不直接拥有完整场景成稿。

## 输入

- 场景中的沟通目标、关系、权力、共同知识和禁语。
- 人物样本文本或作者决定。
- 目标媒介、时代、地域、阶层、职业和语言情境。
- 需要区分的角色或需要修复的对白问题。

## 输出

- speech act、字面内容、预期含意、不可直说内容。
- 直接度、面子策略、轮次、沉默、回避、称谓和修复规则。
- 词汇/隐喻域、语码转换、身体—声音配合。
- 安全、地位威胁、亲密、欺骗四种对比短句和证伪场景。

格式读取 `../character-intelligence-router/references/internal-facet-output-templates.md` 的“声音语用与潜台词规则”。机制读取 `../character-intelligence-router/references/voice-pragmatics-and-subtext.md`。

## 工作流

1. 先写人物想通过说话完成的行动：请求、拒绝、承诺、威胁、试探、遮蔽、修复或夺权。
2. 写双方共享与不共享的信息，确保潜台词有可推断前提。
3. 根据关系、地位和风险选择直接或间接表达。
4. 定义人物怎样开始、打断、结束、回避、沉默和要求解释。
5. 定义称谓、确定性词、句法、隐喻来源、禁语和语码转换触发。
6. 写对方如何理解、误解或拒绝理解，确保交流改变状态。
7. 生成少量对比短句用于验证，不模仿受版权保护角色的大量原对白。
8. 把规则 handoff 给 `screenplay-scene-writer`、`chinese-novel-chapter-writer` 或对应 writer 成稿。

## 选择原则

- 声音差异来自世界分类、关系策略和风险管理，不只是用词怪癖。
- 潜台词必须改变信息、权力、关系或行动。
- 同一人物对上、对下、亲密和陌生对象可以显著不同。
- 方言、语码和礼貌必须基于具体文化材料，不做刻板表演。

## 边界

- 不复制或高度仿写受版权保护角色的长段对白。
- 不把方言拼写、口吃、残障或第二语言当笑料。
- 不为现实操控、欺骗、胁迫或极化设计优化话术。
- 不替 writer 输出完整章节或剧本场景。

## 验证

- 每条承重规则对应沟通目标和关系位置。
- 潜台词具有共同知识与可推断路径。
- 对比短句在去掉人物名后仍有可解释差异。
- 沉默、称谓或语码转换会产生明确关系后果。
