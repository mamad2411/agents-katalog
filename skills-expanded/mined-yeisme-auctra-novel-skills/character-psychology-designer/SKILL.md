---
name: character-psychology-designer
description: Use when creating or rebuilding fictional characters for novels, screenplays, short drama, audio drama, or game narrative from theme, role function, conflict, premise, archetype, or thin character notes, and when the result must connect beliefs, wants, fears, emotion, relationships, voice, pressure behavior, and transformation.
---

# 人物心理设计师

把人物从“冷酷、聪明、有创伤”这类标签，转成能在场景中持续做出具体选择的心理与行为系统。

## 输入

- 主题、题材、角色功能、故事前提、外部目标、关键关系、必须发生的情节和用户禁忌。
- 可选：已有薄弱人物卡、参考气质、目标媒介、人物弧线方向和制作限制。

## 输出

- 人物核心引擎：表层欲望、深层需求、主导恐惧、核心信念、保护策略。
- 最小充分的承重 facet、公开面具、私下自我、语言与行为规则。
- 关系筹码、压力反应、道德边界、诱惑路径、弧线节点和验证场景。

## 必读参考

- 读取 `../character-intelligence-router/references/character-intelligence-ontology.md`。
- 需要区分作者决定与待验证假设时读取 `../character-intelligence-router/references/character-evidence-protocol.md`。
- 需要标准人物设计包时读取 `../character-intelligence-router/references/character-output-templates.md`。

## 工作流

1. 先定义角色在故事中的功能与不可替代价值，避免只从性格词开始。
2. 建立人物核心引擎：`want -> need -> fear -> belief -> protection strategy`。
3. 从开放本体选择能形成“机制—行为—关系—代价—验证”闭环的最小充分 facet；只有某个内在或社会机制需要独立深挖时，交回 router 追加一个 specialist。
4. 把每个承重维度翻译成：平时行为、压力行为、语言表现、关系影响和失败代价。
5. 设计至少一组内部矛盾：欲望与价值、面具与私我、优点与阴影、爱与恐惧。
6. 设计关键关系的双向结构：双方想要什么、能给什么、欠什么、怕什么、谁能伤害谁。
7. 选择正向、负向或平坦弧线；用选择与代价证明变化，不用解释性独白代替转变。
8. 生成 2-4 个验证场景：诱惑、失去、羞辱、权力变化、亲密暴露或道德边界。

## 设计原则

- 创伤不是人物深度的必需品；人物也可由责任、欲望、文化、阶层、信仰、职业或爱驱动。
- 缺陷必须同时带来短期收益，否则人物不会坚持它。
- 反派和阻力人物必须有可理解的目标与有效压力来源，不必被洗白。
- 人物声音要来自认知、关系与语用策略，不只是口头禅；需要言语行为、潜台词或语码转换规则时 handoff 给 `character-voice-pragmatics-designer`。
- 认知决策、动机价值、情绪调节、身份叙事或身体习惯成为承重难题时，使用对应 specialist 的独立产物后再整合。
- 角色设定只有在场景中改变选择、关系、信息或代价时才算有效。

## 媒介适配

- 小说：可保留受控内心活动，但必须与行为和叙事视角一致。
- 剧本/短剧：把心理机制翻译成动作、停顿、道具、空间、潜台词和 blocking。
- 音频：强化节奏、停顿、称谓、语气和声音记忆点。
- 游戏叙事：明确触发条件、状态变化、选择边界和重复交互的一致性。

## Auctra handoff

- 标明 `phase=character`、`artifact=character_design_pack`、建议 display path 和待 review 假设。
- 持久化必须通过 Auctra CLI 或 application service；不得把设计草案直接写成 accepted canon。

## 边界

- 不复制现成人物或用几个外部角色拼接成“原创人物”。
- 不把本体覆盖率或维度数量作为完成标准。
- 不替代章节、场景或对白成稿 skill。
- 不把临床疾病标签当作人物复杂度快捷方式。

## 验证

- 人物至少能回答：他想要什么、怕什么、相信什么、如何保护自己、压力下会做什么。
- 每个承重维度至少绑定一个可观察行为或语言规则。
- 至少一个验证场景会迫使人物在两项重要价值之间做选择。
