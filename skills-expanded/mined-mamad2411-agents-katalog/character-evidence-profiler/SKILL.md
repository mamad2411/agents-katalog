---
name: character-evidence-profiler
description: Use when analyzing an existing fictional character, draft, scene, dialogue sample, character dossier, or public-domain character through evidence-backed personality, cognition, motivation, emotion, relationship, voice, contradiction, and arc profiling with explicit confidence and non-clinical boundaries.
---

# 人物证据画像师

从材料中提取“人物实际做了什么、说了什么、如何选择”，再形成可验证的人物画像。先证据，后解释；不知道的维度保留未知。

## 输入

- 章节、场景、对白、人物卡、梗概、关系记录或公开领域作品材料。
- 可选：分析问题、比较对象、目标媒介、作者已确认事实和禁止推断项。

## 输出

- 材料覆盖与证据质量说明。
- 承重维度画像、思维拓扑、决策指纹、情绪与关系模式、人物声音。
- 矛盾证据、未知项、验证场景和下游修复建议。

## 必读参考

- 读取 `../character-intelligence-router/references/character-evidence-protocol.md`。
- 读取 `../character-intelligence-router/references/character-intelligence-ontology.md`，只选能解释当前人物选择的最小充分 facet。
- 只有旧 prompt 或历史维度 id 需要兼容时读取 `../character-intelligence-router/references/character-intelligence-matrix.md`。
- 需要标准交付格式时读取 `../character-intelligence-router/references/character-output-templates.md`。

## 工作流

1. 定义分析单位：单场、单章、全稿、角色对比或某一关系阶段。
2. 提取可观察证据：动作、选择、用词、回避、信息使用、关系变化、压力反应和前后状态。
3. 给每条证据标注 source ref；不要先套 MBTI、原型或心理标签。
4. 选择承重 facet，逐项区分 `observed_evidence`、`creative_inference`、`author_decision`、`open_hypothesis`；若某一机制需要独立深挖，交回 router 追加一个 specialist。
5. 标注 `high`、`medium`、`low` 置信度，并说明缺少什么材料才能提高置信度。
6. 对相反证据分类：状态变化、关系差异、伪装、成长、叙事视角偏差或连续性错误。
7. 生成画像，并把每个重要结论落到可写的动作、对白、选择、潜台词或代价。

## 分析重点

- **思维方式**：如何注意、归因、推理、处理不确定性和时间。
- **驱动机制**：想要什么、真正需要什么、怕什么、用什么策略保护自己。
- **关系机制**：信任阈值、边界、权力、亲密、亏欠和背叛风险。
- **表达机制**：句长、词汇、回避方式、情绪泄露点、身体习惯和禁用表达。
- **矛盾机制**：公开面具与私下自我、价值观与欲望、优点与阴影的冲突。

## Auctra handoff

- 输出可作为人物 material 或 review 输入，但不得直接成为 accepted canon。
- 保存前可建议运行 `auctra gate check --before chapter_write --json`。
- 如果需要新增人物持久化命令，报告产品缺口，不手写 `.auctra/**`。

## 边界

- 不仅凭几句话诊断现实人物的精神疾病、人格障碍、危险性或谎言。
- 不把“没有证据”写成“角色没有该特质”。
- 不用单一人格测试替代文本证据。
- 不大量引用受版权保护作品；优先使用用户提供材料、短证据片段和概括。

## 验证

- 每个关键结论都有 source ref、facet 或兼容维度 alias、事实状态和置信度。
- 至少列出一个替代解释或未知项。
- 建议能够转化为场景、对白或人物选择，而不是抽象心理形容词。
