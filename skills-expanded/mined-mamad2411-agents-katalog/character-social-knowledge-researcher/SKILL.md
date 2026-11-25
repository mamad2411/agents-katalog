---
name: character-social-knowledge-researcher
description: Use when researching the social context of a fictional character or story world, including era, region, family, occupation, class, institutions, customs, group norms, political order, or historical constraints, and when the result must be sourced, bounded, and translated into creative consequences rather than presented as generic worldbuilding trivia.
---

# 人物社会知识研究员

为人物或故事世界建立“有来源、有限定、能改变角色选择”的社会情境包。先界定时代、地域、制度与问题，再检索；不把现代常识、单一资料或群体刻板印象直接投射到角色身上。

## 输入

- 研究问题：角色在什么社会中，受到什么机会、义务、风险或禁忌影响。
- 时空范围：年代、地域、城市/乡村、战争/和平、制度阶段；未知项必须显式保留。
- 人物位置：家庭、职业、阶层、性别角色、族群/宗教身份、组织成员资格。
- 可用材料：用户资料、项目 bible、历史文献、开放教材、研究论文或可信网页。

## 输出

- `research_scope`：问题、时空边界、关键词和禁止泛化项。
- `source_table`：来源、类型、直接 URL/定位、可信度、许可或引用边界。
- `fact_layer`：可追溯事实、争议点、缺口和过时风险。
- `creative_interpretation`：事实如何改变角色的资源、语言、声誉、关系与选择。
- `scene_rules`：可写的冲突、日常细节、公开/私下差异和反证场景。
- `specialist_handoff`：最多推荐一个社会 specialist。

## 必读参考

- 读取 `../character-intelligence-router/references/social-knowledge-index.md` 选择研究领域。
- 读取 `../character-intelligence-router/references/social-research-source-ledger.md` 了解已有来源与版权边界。
- 需要标准格式时读取 `../character-intelligence-router/references/social-context-output-templates.md`。
- 工作/经济、法律/官僚、宗教/仪式、媒介/技术或迁移/地方问题，分别读取 `work-economy-and-material-life.md`、`law-bureaucracy-and-citizenship.md`、`religion-ritual-and-symbolic-order.md`、`media-technology-and-publics.md` 或 `migration-place-and-diaspora.md`。
- 只读取与问题直接相关的领域 reference，不一次加载全部社会知识。

## 工作流

1. 把宽泛主题改写成可验证问题，例如把“古代女性地位”改成具体时代、地域、阶层、婚姻制度和行动场景。
2. 先查项目资料和共享 references，再补充外部来源。新事实优先一手史料、官方材料、同行评审研究或开放教材。
3. 为每条结论标注 `established`、`contested`、`context_specific`、`creative_inference` 或 `unknown`。
4. 交叉检查时间、地域、制度与群体差异；单一来源只支持候选结论，不支持强断言。
5. 把事实转成角色可感知的成本：能不能进入、谁能惩罚、失去什么、如何说话、哪些事只能私下做。
6. 设计至少一个反例或越轨者，避免把社会规范写成所有人的统一人格。
7. 输出 context pack，并只 handoff 给最主要的社会 specialist 或人物/writer owner。

## 研究最低标准

- 事实与创作推断分栏。
- 重要结论至少有一个直接定位；高争议结论尽量有两类独立来源。
- 明确材料没有覆盖什么，尤其是普通人、边缘群体和地区差异。
- 只使用必要的短引文，优先原创概括。

## Auctra handoff

- context pack 可以成为人物、世界观或场景 material，但不得自动成为 accepted canon。
- 结构化项目状态只能由 Auctra CLI 或 application service 更新。
- 若研究发现原人物设定与史实冲突，提交 review 选项，不直接改写正典。

## 边界

- 不做现实个人诊断、群体本质判断、政治宣传或法律/医疗结论。
- 不把“常见”“被规范要求”写成“每个人必然如此”。
- 不伪造访问过的来源、页码、引文或统计数据。
- 不复制受版权保护的整章、整篇论文或第三方 skill 正文。

## 验证

- 每个关键事实都有来源状态与时空限定。
- 至少三个结论已经转成角色机会、代价、关系或场景，而非百科摘要。
- 至少一个反例、争议或未知项可阻止刻板化。
- handoff 只有一个主要 specialist 或下游 owner。
