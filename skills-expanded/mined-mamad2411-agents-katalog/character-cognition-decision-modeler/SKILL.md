---
name: character-cognition-decision-modeler
description: Use when a novel, screenplay, game narrative, or character analysis needs a detailed model of how a character notices information, explains causes, handles uncertainty, weighs risk and loss, applies heuristics, changes evidence thresholds, or makes a specific high-stakes decision.
---

# 人物认知决策建模师

建立“人物怎样知道并选择”的可验证模型。输出认知模型与决策指纹，不评判智力，也不替主 worker 决定整个人物或剧情。

## 输入

- 一个明确的决定、误判、调查、谈判或行动阈值。
- 人物当时实际知道和不知道的信息。
- 可用文本证据、作者决定、关系与权力情境。
- 目标媒介与弧线阶段。

## 输出

- 注意过滤、心智模型、因果归因、证据阈值和不确定性语言。
- 选项表：人物感知的收益、损失、概率、身份与关系代价。
- 默认启发式、行动阈值、预测选择和决策声音。
- 替代解释、证伪场景和返回主 worker 的 handoff。

格式读取 `../character-intelligence-router/references/internal-facet-output-templates.md` 的“认知模型与决策指纹”。机制需要深化时读取 `../character-intelligence-router/references/cognition-decision-and-uncertainty.md`；领域边界读取 `../character-intelligence-router/references/character-intelligence-ontology.md`。

## 工作流

1. 把任务收窄为一个承重决定，记录人物当时真实可用的信息，禁止使用作者全知信息。
2. 先写观察：他注意、追问、遗漏、重复和如何表达确定性。
3. 建模其当前心智模型、因果归因和对其他行动者意图的假设。
4. 列出选项在人物眼中的收益、损失、概率、身份与关系代价，而不是客观最优值。
5. 识别启发式、时间视野、沉没成本、行动阈值和可修正规则。
6. 预测第一反应与最终选择；至少保留一个合理替代解释。
7. 设计反证、陌生领域或身份威胁场景，验证该模型是稳定机制还是偶然表现。
8. 将可用结论 handoff 给人物设计、压力测试、对白或 writer；不直接写完整成稿。

## 选择原则

- “聪明”不是产物；必须说明人物在哪种环境中用什么模型有效。
- 同一人物可在不同领域拥有不同证据阈值和风险偏好。
- 错误优先检查信息、模型、激励、身份和权力，不急着归因为性格缺陷。
- 元认知必须通过下一次选择规则变化证明，不能只靠自我解释。

## 边界

- 不进行 IQ、神经认知、精神疾病、说谎或危险性判断。
- 不把认知偏误当固定缺陷或道德问题。
- 不使用流行心理学标签替代证据。
- 每次只建模一个主要决定；多个独立决定应分别输出或回到 router。

## 验证

- 输入信息与作者全知信息已分离。
- 预测选择可以由注意、模型、阈值和代价共同解释。
- 至少包含一个替代解释和一个证伪场景。
- 产物会改变场景选择、对白确定性或行动节奏，而非只增加术语。
