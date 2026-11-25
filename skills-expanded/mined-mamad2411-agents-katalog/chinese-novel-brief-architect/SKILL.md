---
name: chinese-novel-brief-architect
description: Use when turning Chinese novel ideas into an executable brief with genre, protagonist, core conflict, reader promise, world rules, titles, and writing constraints.
---

# 中文小说创作简报架构师

在写大纲、人物档案或章节前，把零散灵感压成可执行创作决策。它服务中文小说，尤其是中文网文长篇，不把一句灵感扩散成无法落地的设定堆。

## 输入

- 用户的故事灵感、题材偏好、角色想法、目标篇幅、更新节奏和禁忌。
- 参考作品、平台读者、世界观碎片、叙事视角、语气样例和必须保留的桥段。
- 如果材料不足，先列最小补问：主角欲望、核心阻力、失败代价、读者为什么追。

## 输出

- 一句话故事前提、读者承诺、题材定位和 3-7 个中文标题候选。
- 主角种子、关系种子、反派/阻力种子、故事引擎和升级路径。
- 写作约束：视角、基调、禁写项、目标章节数、每章目标字数、待确认问题。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 worker 交付格式、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章节模板、场景卡字段或拆章规格时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 review、导出前检查或多轮修订门禁时读取。

## 工作流

1. 识别用户真正想写的题材、情绪和读者承诺，过滤互相冲突的设定。
2. 把冲突写成“谁想要什么、谁阻止、失败代价是什么”。
3. 定义类型契约、主角驱动力、世界规则、更新节奏和不能踩的雷。
4. 生成标题和开篇承诺，并说明每个标题对应的读者预期。
5. 输出给大纲、人物和项目圣经可直接复用的简报，不写成泛泛脑暴。

## 质量门槛

- 简报必须能直接驱动 `chinese-novel-outline-architect` 和 `chinese-novel-character-architect`。
- 不能只用“成长、救赎、热血、高级感”这类空词描述主题。
- 每个暂定事实都要标注待确认，不把灵感写成正典。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。
- Auctra 中文项目启动时，brief artifact 应写成可落入 `大纲/` 或 `素材/` 的作者文件；机器状态仍通过 CLI 写入 `.auctra/`。
- 若项目缺 locale/layout，先建议 `auctra project init ... --locale zh-CN --layout chinese-novel` 或交给 `auctra-i18n-workspace-router`；若进入写章前，建议 `auctra gate check --before chapter_write --json`。
- 输出 handoff 时标明 phase=`brief`、artifact=`novel_brief`、gate=`chapter_write`、display_path 建议和待补素材。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
