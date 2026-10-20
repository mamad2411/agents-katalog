---
name: chinese-novel-genre-contract-strategist
description: Use when defining or revising Chinese web-novel genre contract, reader promise, trope strategy, anti-cliche boundary, update rhythm, and market-positioned story engine.
---

# 中文小说类型契约策划

当故事有题材但缺乏追读理由、开篇承诺或章节爽点时使用。它把作者想写的东西翻译成读者能感知的连续回报。

## 输入

- 创意、参考作品、目标平台、目标读者、篇幅、更新节奏和已有样章。
- 用户喜欢和讨厌的套路、频道限制、商业/文学取向、必须规避的雷点。

## 输出

- 一句话类型定位、主类型/副类型、读者点开理由和继续追的理由。
- 必备桥段、可变桥段、禁用套路、差异化钩子和替代写法。
- 前 3 章、前 10 章、每卷高潮和阶段回报策略。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 worker 交付格式、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章节模板、场景卡字段或拆章规格时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 review、导出前检查或多轮修订门禁时读取。
- 类型专项参考：悬疑/推理读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-suspense-mystery.md`，言情读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-romance.md`，玄幻/奇幻读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-xuanhuan-fantasy.md`，都市/职场读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-urban-career.md`，科幻读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-sci-fi.md`，历史/权谋/宫斗读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-historical-power.md`，武侠/仙侠读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-wuxia-xianxia.md`，灵异/恐怖读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-horror-supernatural.md`，冒险/夺宝/无限流/生存读取 `../chinese-novel-orchestrator/references/chinese-novel-genre-adventure-survival.md`。
- `../chinese-novel-orchestrator/references/chinese-novel-search-keyword-presets.md`：需要参考知名小说、搜索预设关键词、同类作品结构拆解或反抄袭边界时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-premise-scene-idea-bank.md`：需要扩展故事前提、类型组合、场景思路或前 10 章钩子时读取。

## 工作流

1. 识别主类型和副类型，例如悬疑、古言权谋、都市异能、无限流、现实成长。
2. 写出核心读者问题：能否翻盘、真相是什么、关系如何破局、世界规则是否可信。
3. 把爽点绑定人物选择、代价和后果，不停留在标签。
4. 设计可重复运行的故事引擎：欲望、阻力、升级、代价、回报。
5. 按主类型读取对应 genre reference，补齐雷区、章节验收点和 handoff。
6. 标注禁用套路和替代方案，例如不靠误会拖剧情、不靠无铺垫开挂。

## 质量门槛

- 类型契约必须能指导前 3 章怎么开、每卷怎么收、章节结尾怎么留。
- 差异化卖点要落到机制、情节或人物压力，不能只说“有新意”。
- 市场定位服务写作判断，不输出虚假平台数据或保证成绩。

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
