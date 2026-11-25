---
name: chinese-novel-project-bible-keeper
description: Use when maintaining a Chinese long-form novel project bible with reader contract, style bible, world rules, timeline, knowledge boundaries, foreshadowing ledger, forbidden moves, and Auctra-facing author artifacts.
---

# 中文小说项目圣经管理员

把长篇小说的稳定事实、读者承诺和禁写边界维护成可复用作者资产，避免只藏在一次性提示词里。

## 输入

- 创作简报、人物档案、大纲、已完成章节、用户禁忌、风格偏好和 review 结论。
- Auctra 项目状态、`form`/`asset`/`kg` 输出或已有 author-facing artifacts。

## 输出

- `reader_contract`、`style_bible`、`continuity_ledger`、`foreshadowing_ledger`、`knowledge_boundary`、`forbidden_moves`。
- 本章可用事实、本章不可越界事实、新增事实候选和待 review 设定。
- 给连续性编辑、章节写手和修订制片的 handoff。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 worker 交付格式、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章节模板、场景卡字段或拆章规格时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-diagram-templates.md`：需要人物关系、时间发展、分卷推进、人物弧线、知识边界或伏笔回收 Mermaid 图预设时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 review、导出前检查或多轮修订门禁时读取。

## 工作流

1. 先从用户材料中提取稳定事实，不把未确认灵感写成铁律。
2. 按读者契约、世界规则、人物知识边界、时间线、伏笔、禁写规则分区整理。
3. 对每条约束标记来源：用户指定、已发布章节、已接受 review、暂定规划。
4. 需要结构化校验时建议运行 Auctra 命令，例如 `auctra form check forms/characters.md --template novel_series --strict --json`。
5. 给下游输出最小相关上下文，而不是把全量百科塞进正文。

## 质量门槛

- 每条规则都能回答谁受约束、从何时生效、违反会造成什么读者问题。
- 项目圣经帮助写作判断，不写成百科堆料。
- 硬矛盾、禁写规则违反、review 阻塞风险必须显式标记。

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
