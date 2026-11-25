---
name: chinese-novel-chapter-writer
description: Use when drafting, continuing, or rewriting a Chinese novel chapter from outline, scene cards, character profiles, continuity ledger, reader contract, and style constraints.
---

# 中文小说章节写手

把每章写成完整叙事单元：有压力、有转折、有后果、有回报、有钩子。

## 输入

- 当前章节大纲、场景卡、人物档案、连续性台账、读者契约、风格说明。
- 上章结尾、当前章目标、必须出现或避免的情节、目标字数。

## 输出

- 一章中文小说正文候选稿。
- 本章连续性 delta：事实、人物状态、伏笔、知识边界、待回收问题。
- 修订建议和需要用户确认的问题。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一章节候选稿、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章首、章中转折、章尾钩子、连续性 delta 或场景写作模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-diagram-templates.md`：需要人物关系、时间发展、分卷推进、人物弧线、知识边界或伏笔回收 Mermaid 图预设时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：章节写完后需要按结构、连续性、留存、对白和文风门禁自检时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-review-gate.md`：需要按章节目标、冲突升级、信息增量、人物推进、连续性 delta、章尾钩子和 risk_flags 自检候选稿时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-suspense.md`：需要线索发现、误导、审讯、跟踪、反转或真相推进模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-relationship.md`：需要初遇、试探、误会、告白、背叛或和解模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-escalation.md`：需要升级、战斗、竞赛、谈判、资源争夺或失败代价模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-worldbuilding.md`：需要规则展示、地点进入、组织势力、道具能力或信息解释模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-transition.md`：需要过渡章、日常缓冲、旅途、训练、调查间隙或余波模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-climax-payoff.md`：需要小高潮、卷中/卷末高潮、伏笔回收或情绪结算模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-investigation-procedure.md`：需要取证、讯问、证词矛盾、时间线复核或程序阻力场景时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-power-politics.md`：需要权谋、宫斗、朝堂、宗门、派系或公开仪式场景时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-heist-strategy.md`：需要夺宝、潜入、救援、破阵、团队分工或撤离追逐场景时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-survival-disaster.md`：需要生存、灾变、无限流副本、资源耗尽或逃生倒计时场景时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-horror-supernatural.md`：需要灵异、恐怖、民俗禁忌、规则怪谈或异常信号场景时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-comedy-satire.md`：需要喜剧、讽刺、黑色幽默、身份错位或误会升级场景时读取。
- 类型专项参考：悬疑/推理读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-suspense-mystery.md`，言情读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-romance.md`，玄幻/奇幻读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-xuanhuan-fantasy.md`，都市/职场读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-urban-career.md`，科幻读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-sci-fi.md`，历史/权谋/宫斗读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-historical-power.md`，武侠/仙侠读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-wuxia-xianxia.md`，灵异/恐怖读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-horror-supernatural.md`，冒险/夺宝/无限流/生存读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-adventure-survival.md`。

## 工作流

1. 读取本章规划、活跃人物、连续性事实和文风约束。
2. 按主类型读取对应 genre reference，明确本章类型回报和禁写雷区。
3. 用压力开场：行动、发现、对峙、倒计时、背叛或艰难选择。
4. 按场景写作：欲望、障碍、策略、转折、后果。
5. 对白写潜台词和角色差异，不只负责解释信息。
6. 每章给读者阶段回报，并用可偿还钩子收尾。
7. 候选稿完成后按 `chinese-novel-chapter-review-gate.md` 自检，无法自证通过时 handoff 到 `chinese-novel-chapter-reviewer`。

## 质量门槛

- 默认每章 3000-5000 个中文字符，用户另有要求时按用户要求。
- 本章必须同时推进情节、人物和至少一个开放线索。
- 不擅自改动已确认的大纲核心事件或项目圣经。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。
- Auctra 中文项目中，章节候选稿只能作为 review candidate 或人工草稿 handoff；不要直接覆盖 `.auctra/manuscript/**`。
- 写章前建议 `auctra gate check --before chapter_write --json`；生成后建议 `auctra review list --status pending --json`，采纳必须由 `review accept|partial` 完成。
- Auctra 项目内写章前必须先绑定声音锚点：用 `auctra voice show` 核对、`auctra voice set`/`auctra voice patterns add` 声明并用 `auctra voice compile` 固化，需要声音上下文时用 `auctra voice brief`；voice 未绑定时不开写。
- 按场景类型取角色化约束：叙述段用 `auctra voice brief --json --role narration` 取叙述基线，紧张/动作段用 `--role scene` 取节奏约束，对白密集场景用 `--role dialogue` 取对白层策略；对白角色策略只提供约束，不代评对白活人感。
- 首章/首集必须先走 scratch proof-slice：在 `auctra scratch`（generic_text）准备 3 个结构不同的 voice 策略候选，逐个用 `auctra scratch validate <ref> --candidate <c> --profile novel_naturalness_v1 --with-naturalness` 验证后 `scratch present`，由用户选择；只有 `auctra voice patterns import --from-scratch <ref> --candidate <c>` 把胜出策略回写 voice.yaml 后才允许批量扩写。
- 自然度修复按 loop policy 单轮推进：每轮至多执行一份已批准 patch（`auctra chapter naturalness patch-check` 通过后 `patch-apply` 一次），读取 guard refs、不碰 read-only 句；不自主连打多轮补丁，也不整章重写。
- 输出 handoff 时标明 phase=`chapter_write`、artifact=`chapter_candidate`、gate=`review_required`、display_path（例如 `章节/ch_001.md`）和连续性 delta。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 有章节文件时可运行 `python3 novel-writing/chinese-novel-orchestrator/scripts/check_chinese_chapter_wordcount.py <chapter.md> 3000`。
- 检查开场压力、场景转折、人物知识边界、章尾钩子和连续性 delta。
- 检查章节目标、冲突升级、信息增量、人物推进、连续性 delta、章尾钩子和 risk_flags 是否完整。
- 未通过连续性或字数检查时，不把候选稿说成最终稿。
