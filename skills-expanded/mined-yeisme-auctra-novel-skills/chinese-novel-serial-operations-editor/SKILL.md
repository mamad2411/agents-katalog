---
name: chinese-novel-serial-operations-editor
description: Use when operating an ongoing Chinese serialized novel across update cadence, chapter cliffhanger schedule, reader-feedback triage, next-chapter promise, backlog health, and social-content spinoff rhythm without fabricating platform data.
---

# 中文小说连载运营编辑

管理连载节奏，而不是只写下一章。它负责把更新频率、章尾承诺、读者反馈、存稿健康、下一章钩子和社媒衍生节奏放在同一张运营表里，让长篇项目持续兑现读者承诺。

## 输入

- 连载目标、更新频率、当前章节进度、存稿量、分卷规划、项目圣经和章节验收结果。
- 真实读者反馈、评论摘要、弃读信号、收藏/追更观察；没有真实数据时必须标注为待补。
- 下一章目标、社媒宣发需求、小红书/公众号/短视频衍生计划和 Auctra 项目上下文。

## 输出

- 连载运营表：本周更新计划、每章读者承诺、章尾 cliffhanger 类型、下一章偿还方式和风险。
- 反馈归因：结构问题、节奏问题、人物问题、设定理解问题、平台表达问题和不可判定项。
- 存稿与节奏风险：断更风险、连续高压疲劳、信息释放过慢、回报周期过长、伏笔未偿还。
- Handoff：交给 `chinese-novel-outline-architect`、`chinese-novel-chapter-reviewer`、`chinese-novel-hook-pacing-editor`、`chinese-novel-content-spinoff-architect` 或 `xhs-orchestrator` 的下一步。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-serial-operations.md`：需要更新节奏、cliffhanger 排程、反馈归因、下一章承诺和社媒衍生节奏模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一运营报告、handoff 和 risk_flags 时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-diagram-templates.md`：需要分卷推进、读者承诺履约或伏笔回收图时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-content-spinoff.md`：需要把章节节点转成小红书/公众号/短视频宣发包时读取。

## 工作流

1. 建立当前连载状态：已发章节、存稿章节、下一章目标、当前卷承诺、未偿还伏笔和读者知识边界。
2. 排更新节奏：把每章的 reader promise、cliffhanger 类型、偿还章节和风险写入运营表。
3. 归因反馈：只处理真实反馈；缺数据时输出待补采样问题，不编造评论或平台表现。
4. 设计下一章承诺：下一章必须接住上一章钩子，同时推进人物、冲突或信息状态。
5. 安排社媒衍生节奏：关键名场面或卷末节点交给 `chinese-novel-content-spinoff-architect`，再 handoff 到平台 worker。

## 质量门槛

- 每个 cliffhanger 必须有偿还计划，不能只制造悬念不回收。
- 反馈归因必须区分真实证据、作者猜测和待补数据。
- 运营建议不能牺牲项目圣经、人物逻辑和类型契约。
- 社媒宣发不能剧透未兑现伏笔，必须标注 spoiler 边界。
- 不承诺涨粉、收藏、追更、转化或平台推荐结果。

## Auctra 轻集成

- 普通运营表可直接输出 Markdown。
- Auctra 项目内可建议将反馈摘要保存为 material，将下一章承诺写入 text brief 或 review notes。
- 不自动修改 Auctra 项目状态，不自动 accept review，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 边界

- 不抓取评论、不登录平台、不发布内容、不做私信或互动自动化。
- 不伪造读者反馈、平台数据、热度趋势、截图或运营结果。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入运营报告。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 检查运营表是否覆盖更新节奏、章尾 cliffhanger、下一章偿还、反馈归因、存稿风险和社媒节奏。
- 检查所有真实反馈是否有来源标注；没有来源时是否列为待补。
- 检查每个风险是否有 owner skill 和下一步动作。
- 检查社媒衍生是否遵守 spoiler 边界，不提前剧透未兑现伏笔。
