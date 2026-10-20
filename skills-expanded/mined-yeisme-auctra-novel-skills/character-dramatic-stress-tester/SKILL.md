---
name: character-dramatic-stress-tester
description: Use when testing whether a fictional character's choices, voice, relationships, moral boundary, knowledge use, or transformation remain credible under temptation, loss, betrayal, intimacy, humiliation, danger, status change, time pressure, or other dramatic pressure across novel and screenplay scenes.
---

# 人物戏剧压力测试师

用具体压力验证人物设定能否生成可信选择。它诊断哪里失真、哪里缺少铺垫、哪里需要更高代价，并输出最小修复动作。

## 输入

- 人物档案或人物设计包。
- 场景目标、关系对象、压力源、可用信息、道德边界、前后状态和必须保留的剧情结果。
- 可选：章节/剧本场景、人物弧线节点、对白样例、Auctra review finding。

## 输出

- 压力测试矩阵：压力、触发维度、预测选择、替代选择、代价、后果和置信度。
- 可信度判断：`pass`、`needs_setup`、`contradiction`、`arc_break`、`insufficient_evidence`。
- 最小修复包：补铺垫、改压力、改选择、改代价、改关系状态或明确人物已变化。

## 必读参考

- 读取 `../character-intelligence-router/references/character-intelligence-ontology.md`，只选择能改变当前压力选择的 facet。
- 只有旧 prompt 或历史维度 id 需要兼容时读取 `../character-intelligence-router/references/character-intelligence-matrix.md`。
- 读取 `../character-intelligence-router/references/character-evidence-protocol.md`，区分设定事实、文本证据与假设。
- 需要标准压力测试格式时读取 `../character-intelligence-router/references/character-output-templates.md`。

## 压力家族

- **资源压力**：时间、钱、信息、体力、选择数量不足。
- **关系压力**：背叛、依赖、亲密暴露、亏欠、权力反转、被误解。
- **身份压力**：公开羞辱、角色冲突、秘密暴露、阶层或职业失位。
- **道德压力**：救一人或多数、忠诚或正义、真相或保护。
- **情绪压力**：触发旧伤、羞耻、嫉妒、内疚、失控或麻木。
- **弧线压力**：继续旧策略、尝试新策略、接受真相或拒绝改变。

## 工作流

1. 确认基准状态：人物当前相信什么、知道什么、想要什么、与对方是什么关系。
2. 定义压力：失去什么、倒计时是什么、谁在看、有什么诱惑、哪项价值被迫牺牲。
3. 选择最小充分 facet，预测第一反应、表面策略、隐藏目标和极限行为；若压力暴露的是认知、动机、情绪、身份、声音或身体中的单一承重缺口，交回 router 追加对应 specialist。
4. 检查选择是否使用了人物不知道的信息、越过未铺垫的能力或突然改变道德边界。
5. 比较至少一个替代选择，说明人物为何不会选它。
6. 评估后果是否真正改变人物、关系、信息、危险、资源或弧线。
7. 给出最小修复动作，不为了解释人物而重写整个剧情。

## 弧线验证

- 正向弧：新选择必须比旧策略更痛、更难，但更接近真实需求。
- 负向弧：每次堕落都必须带来短期收益并缩小回头空间。
- 平坦弧：人物坚持真相必须付出代价，并对他人或世界产生可见影响。
- 突然转变：若没有抵抗、失败、镜像或阈值选择，标记 `needs_setup`。

## 写作 handoff

- 小说成稿交给 `chinese-novel-chapter-writer` 或相应修订 skill。
- 剧本成稿交给 `screenplay-scene-writer`；压力测试只提供动作/潜台词/选择建议，不直接替代完整场景。
- Auctra finding 应进入 review handoff，不自动 accept 或覆盖正文。

## 边界

- 不为了保留预定情节而强迫人物做不可信选择；应暴露冲突并提出代价更合理的路径。
- 不把人物设定当静态法律；已发生且有证据的成长可以改变预测。
- 不诊断现实人物或预测现实暴力风险。

## 验证

- 每个结论都连接压力、人物机制、选择、代价和后果。
- 每个 `contradiction` 或 `arc_break` 都有最小修复动作。
- 至少说明一个人物不会选择的替代方案及原因。
