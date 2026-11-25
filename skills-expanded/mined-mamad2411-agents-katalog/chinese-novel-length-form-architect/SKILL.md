---
name: chinese-novel-length-form-architect
description: Use when choosing, planning, or converting Chinese fiction length forms across micro fiction, short stories, novelettes, novellas, long-form serial novels, and series with appropriate structure, density, ending strategy, and delivery constraints.
---

# 中文小说篇幅形态架构师

根据目标读者、题材承诺、素材规模和交付场景，决定中文小说应该写成微型、短篇、中篇、长篇、系列文还是连载，并给出可执行结构。

## 输入

- 故事前提、题材、目标读者、目标字数或阅读时长、发布/投稿/项目场景。
- 已有素材：人物、世界观、主题、冲突、结局、章节草稿或 Auctra 项目状态。
- 用户目标：新写、压缩、扩写、改成长篇、改成短篇、系列化或投稿/发布版本。

## 输出

- 推荐篇幅形态：微型、短篇、中篇、长篇、系列文或连载，并说明取舍。
- 结构方案：开场、转折、高潮、结尾、章节/场景数量、每段功能和字数区间。
- 压缩/扩写策略：保留内容、合并内容、删除内容、可延展内容和不可牺牲承诺。
- 交接包：应交给 brief、outline、scene-card、chapter-writer 或 revision 的下一步。

## 参考资料

只在任务需要对应细节时读取参考资料：
- `../chinese-novel-orchestrator/references/chinese-novel-length-form-matrix.md`：需要短篇、中篇、长篇、系列文结构选择、字数密度或结尾策略时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-theme-breakdown.md`：需要把主题拆成情节证明、人物承载和读者情绪回报时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章节/场景卡落地时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 handoff、risk_flags 和 continuity_delta 字段时读取。

## 工作流

1. 判断用户是在选篇幅、压缩、扩写、系列化还是为特定平台准备版本。
2. 评估素材体量：核心冲突数量、主要人物数量、世界规则复杂度、主题层数、伏笔债务和结局复杂度。
3. 选择最小可承载形态：短篇优先单核心冲突，中篇允许多阶段反转，长篇需要可持续升级和阶段兑现。
4. 输出结构骨架，不直接写完整正文；需要正文时交给 `chinese-novel-chapter-writer` 或具体写作技能。
5. 标注压缩/扩写风险：主题被稀释、结局过急、设定过重、人物弧线不足或长篇只是在注水。

## 质量门槛

- 推荐篇幅必须服务读者体验和素材规模，不能只按用户给出的字数机械拆分。
- 短篇必须有清晰单次情绪或认知转折；中篇必须有阶段推进；长篇必须有持续读者承诺。
- 扩写不能只增加解释、背景和空对白；压缩不能删掉动机、代价和结局因果。
- 输出必须说明下一步由哪个技能继续执行。

## Auctra 轻集成

- 普通篇幅规划可直接输出 Markdown。
- 若用户在 Auctra 项目内需要保存规划材料，建议把篇幅矩阵和结构方案作为 material 保存，再进入 outline 或 review。
- 不手写 `.auctra/**`、review 决策、SQLite rows 或 run evidence。

## 边界

- 不承诺平台投稿结果、商业签约、影视售卖或真实读者反馈。
- 不把长篇网文规则强套到短篇文学、投稿短篇或剧本改编。
- 不伪造用户未提供的出版、阅读量、版权或市场数据。
- 不写完整思维链、原始提示词、供应商载荷或隐藏系统提示。
- 已选定长篇/系列后的逐卷主题、升级路径和逐章结构交给 `chinese-novel-volume-arc-planner` 与 `chinese-novel-outline-architect`；本技能只决定篇幅形态与结构骨架。
- 跨媒介改编（短剧/电影/漫画/音频等）交给 `chinese-novel-adaptation-architect`，不在本技能范围内。

## 验证

- 检查篇幅形态是否与素材复杂度匹配。
- 检查结构是否含开场承诺、推进节点、高潮和结尾策略。
- 检查压缩/扩写建议是否列出保留、删除、合并和延展项。
- 检查下一步 handoff 是否明确到具体 skill。
