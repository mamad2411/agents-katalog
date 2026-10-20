---
name: chinese-novel-outline-architect
description: Use when planning Chinese novel structure, chapter outlines, serial arcs, reversals, foreshadowing seeds, chapter hooks, and payoff plans.
---

# 中文小说大纲架构师

创建能直接驱动章节写作的大纲，而不是只写故事简介或流水账。

## 输入

- 创作简报、人物档案、世界观、目标章节数、题材类型和更新节奏。
- 已完成章节、已埋伏笔、必须保留或避免的情节、读者反馈。

## 输出

- 分卷或阶段结构。
- 逐章表格：章号、标题、入场状态、核心事件、冲突、反转、结尾钩子、出场人物、伏笔/回收、连续性备注。
- 需要拆成场景卡的章节列表和风险标记。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 worker 交付格式、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章节模板、场景卡字段或拆章规格时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-diagram-templates.md`：需要人物关系、时间发展、分卷推进、人物弧线、知识边界或伏笔回收 Mermaid 图预设时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 review、导出前检查或多轮修订门禁时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-serial-operations.md`：需要把逐章大纲连接到更新节奏、章尾 cliffhanger 排程和下一章承诺时读取。
- 类型专项参考：悬疑/推理读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-suspense-mystery.md`，言情读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-romance.md`，玄幻/奇幻读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-xuanhuan-fantasy.md`，都市/职场读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-urban-career.md`，科幻读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-sci-fi.md`，历史/权谋/宫斗读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-historical-power.md`，武侠/仙侠读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-wuxia-xianxia.md`，灵异/恐怖读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-horror-supernatural.md`，冒险/夺宝/无限流/生存读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-adventure-survival.md`。
- `../chinese-novel-orchestrator/references/chinese-novel-premise-scene-idea-bank.md`：需要批量生成逐章场景思路、前 10 章钩子或类型组合变体时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-search-keyword-presets.md`：需要用搜索预设辅助同类作品结构拆解或参考边界时读取。

## 工作流

1. 读取 brief 与人物档案；缺失时先列最小补齐项。
2. 选择结构：悬疑升级、情感拉扯、修炼成长、生存链条、多幕结构或群像线。
3. 按主类型读取对应 genre reference，确定章节回报、雷区和验收点。
4. 先拆分分卷/阶段弧线，再逐章生成可执行表格。
5. 检查每章是否改变故事状态，删除纯过渡章和纯解释章。
6. 需要细化单章时交给 `chinese-novel-scene-card-writer`；需要连载排期时交给 `chinese-novel-serial-operations-editor`。

## 质量门槛

- 每章至少有一个冲突、转折、不可逆发现或情绪回报。
- 章节钩子要轮换危险、揭示、选择、背叛、倒计时、情绪反转。
- 伏笔必须有预计回收位置，不能只埋不收。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。
- Auctra `zh-CN/chinese-novel` 项目中，大纲 artifact 默认面向 `大纲/` display path；章节表应引用 `章节/ch_001.md` 这类 display_path，不手写 `.auctra/manuscript/**`。
- 写章前建议 `auctra gate check --before chapter_write --json`；已有项目先用 `auctra project next --json` 确认 pending review、materials 和 latest display path。
- 输出 handoff 时标明 phase=`outline`、artifact=`chapter_outline`、gate=`chapter_write`、需要拆成场景卡的章节和 display_path。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
