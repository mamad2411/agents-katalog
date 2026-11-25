---
name: character-intelligence-router
description: Use when routing character analysis, original character design, personality and thinking-style modeling, relationship or ensemble design, character arc work, dialogue consistency checks, or dramatic stress tests for novels and screenplays to the smallest suitable character-intelligence workflow.
---

# 角色智能路由器

把人物任务分给最小合适的工作 skill。路由器只判断目标、输入缺口、owner 和 handoff，不直接替代人物分析、人物设计或场景写作。

## 输入

- 用户目标：分析已有角色、创建原创人物、修复扁平人物、比较人物声音、设计群像、规划弧线或验证场景反应。
- 可用材料：brief、人物卡、章节、场景、对白、关系表、故事圣经、Auctra 项目状态。
- 目标媒介：小说、剧本、短剧、广播剧、游戏叙事或仅做方法研究。

## 输出

- 唯一主工作 skill、可选的一个 facet specialist、推荐理由和输入缺口。
- 交付物、验证方式、下一步 owner。
- Auctra 项目中的 phase、artifact、gate 和真实命令建议。

## 路由表

| 用户任务 | 主 skill | 交付物 |
| --- | --- | --- |
| 从文本、对白、场景或资料分析人物性格、思维、动机、关系和盲区 | `character-evidence-profiler` | 证据式人物画像 |
| 从主题、角色功能、冲突或已有薄弱人设创建/重构人物 | `character-psychology-designer` | 人物设计包 |
| 验证人物在诱惑、背叛、失去、权力变化、道德困境或弧线转折中的反应 | `character-dramatic-stress-tester` | 压力测试与最小修复包 |
| 深挖注意、推理、不确定性、风险、证据阈值与具体决定 | `character-cognition-decision-modeler` | 认知模型与决策指纹 |
| 深挖目标、需要、奖励、价值排序、承诺与动机冲突 | `character-motivation-value-architect` | 动机价值层级与冲突图 |
| 深挖事件评估、触发、表达、调节、共调节与恢复 | `character-emotion-regulation-modeler` | 情绪调节回路 |
| 深挖自我故事、角色身份、面具、记忆与身份威胁 | `character-identity-narrative-modeler` | 身份叙事图 |
| 深挖言语行为、含意、潜台词、沉默、称谓与语码转换 | `character-voice-pragmatics-designer` | 声音语用与潜台词规则 |
| 深挖感官、身体、空间、物件、日常、技能与疲劳行为 | `character-embodiment-habit-designer` | 身体习惯表演图 |
| 为特定时代、地域、制度、职业或群体建立带来源的社会背景 | `character-social-knowledge-researcher` | sourced social context pack |
| 建模信任、亲密、互惠、依赖、边界、债务、背叛与修复 | `character-relationship-dynamics-modeler` | 关系动力图 |
| 建模资源、信息、权威、地位、声誉、制裁、赞助与继承 | `character-power-status-analyst` | 权力地位图 |
| 建模文化脚本、社会化、阶层、语言、流动、污名与身份切换 | `character-culture-class-context-modeler` | 文化阶层情境图 |
| 建模团队、家族、派系、组织、联盟、规范、网络与集体行动 | `character-group-organization-modeler` | 群体组织图 |
| 设计价值、道德、意识形态、正当性、宣传与阵营内部异议 | `character-moral-ideology-conflict-designer` | 道德意识形态冲突图 |
| 只需要普通中文小说人物卡、声音规则和关系网 | `chinese-novel-character-architect` | 轻量人物档案 |
| 已有人物模型，需要写成完整剧本场景 | `screenplay-scene-writer` | 可制作场景 |
| 已有人物模型，需要写小说章节 | `chinese-novel-chapter-writer` | 章节候选稿 |

## 参考资料

- `references/character-intelligence-ontology.md`：所有深度人物任务的 canonical domain/facet、扩展门槛与 specialist 索引。
- `references/character-intelligence-matrix.md`：只有旧 prompt、旧链接或历史维度 id 需要兼容时读取；这是 deprecated seed catalog。
- `references/character-evidence-protocol.md`：需要分析已有文本、处理冲突证据、标注置信度或现实人物边界时读取。
- `references/character-output-templates.md`：需要标准人物画像、设计包、压力测试或 Auctra handoff 模板时读取。
- `references/internal-facet-output-templates.md`：需要六个内在机制 specialist 的标准产物时读取。
- `references/cognition-decision-and-uncertainty.md`、`motivation-needs-and-values.md`、`emotion-appraisal-and-regulation.md`、`identity-memory-and-self-narrative.md`、`voice-pragmatics-and-subtext.md`、`embodiment-sensation-and-habit.md`：只读取被选内在 specialist 对应的一份。
- `references/social-knowledge-index.md`：需要判断社会问题属于关系、权力、文化阶层、群体组织还是道德意识形态时读取。
- `references/social-context-output-templates.md`：需要社会情境包与五类社会图谱标准格式时读取。
- `references/social-research-source-ledger.md`：需要使用社会科学来源、检查许可或补充地域资料时读取。
- `references/relationships-and-kinship.md`、`power-status-and-institutions.md`、`culture-class-and-socialization.md`、`groups-organizations-and-networks.md`、`morality-ideology-and-legitimacy.md`：只读取被选 specialist 对应的一份，不一次加载全部。
- `references/work-economy-and-material-life.md`、`law-bureaucracy-and-citizenship.md`、`religion-ritual-and-symbolic-order.md`、`media-technology-and-publics.md`、`migration-place-and-diaspora.md`：需要跨域社会事实包时只读取对应一份，由社会研究员拥有来源结论。
- `references/source-ledger.md`：需要了解本体系的公开来源、抽象启发和版权边界时读取。

## 工作流

1. 第一阶段判断主交付物是 `analyze`、`design`、`stress_test`、`social_research` 还是具体成稿；只选择一个主 skill。
2. 判断是否只需轻量人物卡；只有需要证据、完整认知机制、社会机制或跨场景验证时才升级到角色智能 worker。
3. 第二阶段判断是否存在一个通用 worker 无法充分回答、且会实质改变当前选择、关系、声音、代价或弧线的 facet；若否，不追加 specialist。
4. 内在机制优先按“怎样知道与决定 → 为什么追求与拒绝 → 怎样感受与调节 → 怎样维持自我故事 → 怎样通过语言行动 → 怎样通过身体与环境行动”选择最主要的一项。
5. 社会机制按“关系能否继续 → 权力能否奖惩 → 文化阶层是否限制资格 → 群体如何施压 → 何种价值赋予正当性”选择最主要的一项。
6. 内在和社会 facet 同时出现时，以最直接改变当前人物决策的机制为 owner；其他项只列为后续 handoff，不同时加载。
7. 列出最小输入缺口。普通任务只选择最小充分 facet，不要求覆盖开放本体或全部社会字段。
8. Auctra 项目中标明 `phase=character`、artifact、review/canonical owner；结构化状态只能由 Auctra CLI 或 application service 修改。

## 边界

- 不在路由器中直接完成最终人物分析或人物设计。
- 不选择模型、reasoning effort、Agent 或子 agent，不扩大权限。
- 不把文学人物分析当成现实人物临床诊断、精神疾病判定或测谎。
- 不把文化、阶层、性别、族群、职业、组织或意识形态当成固定人格。
- 不为现实政治操纵、群体极化、胁迫、仇恨或暴力动员提供优化方案。
- 不把 Pinax、RAG、向量库或 skill reference 当成 Auctra 人物正典。
- 不手写 `.auctra/**`、SQLite rows、review 决策或运行证据。

## 验证

- 路由必须只有一个主工作 skill。
- 若追加 facet specialist，最多一个，并说明为什么它比相邻 skill 更接近当前人物决策及其独立交付物。
- 路由必须说明交付物、缺失输入、事实/推断边界和下一步 owner。
- 深度人物任务必须指向证据分析、人物设计、压力测试或社会研究之一作为主 worker；内在或社会 specialist 只能作为有限追加，最终成稿必须交给具体小说或剧本 writer。
