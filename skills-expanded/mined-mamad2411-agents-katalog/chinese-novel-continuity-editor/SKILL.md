---
name: chinese-novel-continuity-editor
description: Use when checking Chinese novel cross-chapter continuity, including timeline, character facts, world rules, knowledge boundaries, foreshadowing, clue payoff, and unresolved questions.
---

# 中文小说连续性编辑

保护长篇小说的记忆、因果和读者信任，尤其适合多章续写或修订前后检查。

## 输入

- 已写章节、大纲、人物档案、世界规则、伏笔记录、修改要求。
- 用户指出的疑似矛盾、角色知识边界、道具/伤病/时间线问题。

## 输出

- 带章节引用的连续性报告。
- 未解线索、开放问题和伏笔债务列表。
- 按读者影响排序的最小修复建议。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一连续性报告、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要判定硬矛盾、伏笔债务、知识边界和 export 阻塞风险时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要抽取或复核章节连续性 delta 时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-diagram-templates.md`：需要人物关系、时间发展、分卷推进、人物弧线、知识边界或伏笔回收 Mermaid 图预设时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-suspense.md`：检查线索、误导、真相推进和公平回收时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-worldbuilding.md`：检查世界规则、组织势力、道具能力和信息解释一致性时读取。

## 工作流

1. 从目标章节抽取事实、时间点、人物状态、知识边界、世界规则、线索和回收。
2. 对照大纲、人物档案和连续性台账。
3. 分类问题：硬矛盾、软不一致、缺失回收、重复揭示、时间线不清。
4. 优先修复影响读者理解和情感信任的问题。
5. 把新增稳定事实交给项目圣经维护。

## 质量门槛

- 不把风格差异误判为事实矛盾。
- 修复建议必须尽量小，不重写无关段落。
- 硬矛盾、禁写规则违反和 review 阻塞风险要标记 blocking。

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
