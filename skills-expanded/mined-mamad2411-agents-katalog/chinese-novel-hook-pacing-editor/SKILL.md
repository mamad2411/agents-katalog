---
name: chinese-novel-hook-pacing-editor
description: Use when improving Chinese novel pacing, tension peaks, openings, cliffhangers, reversals, serial retention, emotional payoff, and reading drive.
---

# 中文小说钩子与节奏编辑

设计章节级留存，但不靠廉价反转、硬凑悬念或牺牲人物逻辑。

## 输入

- 章节草稿、大纲、上章结尾、下章目标、目标读者和题材类型。
- 用户反馈的拖沓位置、想强化的高潮、必须保留的慢节奏段落。

## 输出

- 节奏诊断：张力波峰、拖慢段落、解释块、跳读风险。
- 开头、中段、结尾钩子的改写建议。
- 可选钩子变体，说明风险和后续回收方式。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一节奏诊断、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章首压力、章中转折、章尾钩子和场景家族入口时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要按留存、结构、钩子偿还和 deferred 风险判定时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-transition.md`：修订过渡章、日常缓冲、旅途、训练、调查间隙和余波节奏时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-climax-payoff.md`：修订小高潮、卷末高潮、伏笔回收和情绪结算节奏时读取。

## 工作流

1. 标记张力波峰、拖慢段落、反转、解释块和读者可能跳读的位置。
2. 强化前 20%：用压力、异常、发现、对峙或艰难选择开场。
3. 确保每章至少有一个有意义转折和一个可感知回报。
4. 把平直结尾替换为与人物、危险、揭示或选择绑定的钩子。
5. 问题集中在开篇三章时交给留存编辑。

## 质量门槛

- 钩子必须来自故事内部压力，不能凭空制造事故。
- 反转要回看合理，不能只追求意外。
- 钩子必须能被后文偿还，不能透支读者信任。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
