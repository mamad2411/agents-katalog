---
name: chinese-novel-volume-arc-planner
description: Use when planning Chinese long-form novel volume arcs, serial escalation, milestones, payoff schedules, and cross-volume hooks.
---

# 中文小说分卷弧线规划师

当小说超过单卷或十几章，需要控制升级、回报和伏笔债务时使用。

## 输入

- 创作简报、类型契约、全书核心问题、目标总章数、更新节奏。
- 已有大纲、章节列表、伏笔台账、读者反馈或中段疲软问题。

## 输出

- 分卷目标：每卷主题、反派/阻力、主线问题、情绪回报。
- 升级阶梯：信息、危险、关系、能力、资源和代价如何逐层升级。
- 章节里程碑：开篇钩子、中点反转、低谷、高潮、余波和下一卷引线。
- 伏笔回收表：seed、误导、升级、payoff、最迟回收章节。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 worker 交付格式、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章节模板、场景卡字段或拆章规格时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-diagram-templates.md`：需要人物关系、时间发展、分卷推进、人物弧线、知识边界或伏笔回收 Mermaid 图预设时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 review、导出前检查或多轮修订门禁时读取。

## 工作流

1. 先锁定全书核心问题，再拆成每卷阶段问题。
2. 每卷定义入场状态、升级机制、不可逆转折和离场状态。
3. 每 3-5 章设置一个小回报，每卷设置一次结构性回报。
4. 让人物成长、世界揭示和外部冲突同步升级。
5. 标记需要连续性编辑追踪的伏笔、债务和世界规则。

## 质量门槛

- 章节规划不能只写“调查、修炼、相处”，必须写冲突、转折和后果。
- 每卷高潮必须回应本卷承诺，同时打开下一卷更大的问题。
- 伏笔回收不能全堆到结尾，长篇需要阶段性兑现。

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
