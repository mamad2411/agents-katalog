---
name: chinese-novel-content-spinoff-architect
description: Use when turning Chinese novel chapters, synopses, or project bibles into social/marketing content packs (Xiaohongshu, WeChat, short-video) with选题, angle, spoiler boundaries, and handoff to platform builders, not the final post itself.
---

# 中文小说社媒衍生架构师

把小说章节、梗概、项目圣经、人物设定转成可执行的社媒宣发包。它负责选题诊断、平台角度映射、剧透边界分级和平台内容包，不直接替代小红书笔记、公众号长文或短视频脚本写手。定位是把作品变成社媒引流素材，扩大读者入口，与全媒介改编、作品分析互补。

## 输入

- 原小说文本、章节表、梗概、项目圣经、人物关系、目标平台（小红书 / 公众号 / 短视频）和目标读者。
- 原作已完成的分析拆解（主题、卖点、名场面、结构、人物弧线、伏笔台账）。
- 连载状态与已发布章节范围：决定剧透边界。
- 平台限制：平台调性、禁区、是否允许硬广导流、目标读者画像。

## 输出

- 选题诊断：原作核心卖点 → 每个平台最匹配的角度，每条选题绑定原作证据。
- 剧透边界分级：每个选题标注 `spoiler_level`（hint / arc_setup / payoff_safe / locked），保护连载悬念。
- 平台内容包：小红书标题组 + 图卡规划、公众号选题 + 分节大纲、短视频钩子 + 脚本骨架。
- Handoff：交给 `xhs-note-writer`、`wechat-article-writer` 或 `short-video-scriptwriter`，附带必须读取的 reference 和引文范围。

## 参考资料

只在任务需要对应细节时读取参考资料：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要 worker 统一交付格式、handoff 字段、continuity_delta 和 risk_flags 时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-analysis-decomposition.md`：需要先获得原作主题、卖点、名场面、人物弧线作为社媒选题源头时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-content-spinoff.md`：需要选题诊断表、剧透边界矩阵、小红书/公众号/短视频平台内容包模板和 handoff 字段时读取。
- `../xhs-orchestrator/references/xhs-lifecycle-handoff.md`：小说衍生内容需要进入小红书选题、brief、正文、标题优化、review 或 Auctra handoff 时读取。
- `../xhs-note-writer/references/xhs-content-playbook.md`：需要小红书标题公式、正文结构、图卡节奏等平台调性细节时读取。
- `../wechat-article-writer/references/platform-nonfiction-playbook.md`：需要公众号结构、分节大纲、行动引导等平台模板时读取。

## 工作流

1. 判断任务是选题诊断、平台角度映射、剧透边界分级还是平台内容包交接。
2. 提炼原作可外宣的核心卖点：高概念反转、人物关系拉扯、世界观奇观、主题命题、名场面，每条绑定章节证据。
3. 按连载状态和平台调性给每个选题打 `spoiler_level`：连载中严守未兑现伏笔，卷末可点当卷结局，完结后仍为新读者保留保护带。
4. 把卖点映射到三个平台的角度，套用对应平台 playbook 的标题公式和结构模板。
5. 对小红书方向标注 `lifecycle_stage`：通常从 topic 或 brief 开始，只有内容包足够完整时才 handoff 到 draft。
6. 输出每个平台的内容包，标注名场面引文范围和 spoiler 等级，handoff 到具体平台写手，不声称已写出最终成品。

## 质量门槛

- 每个选题必须绑定原作核心卖点，不接受靠通用"打工人/读书人设"硬套的泛泛角度。
- 剧透边界必须按连载状态 × 平台分级，绝不提前覆盖未兑现伏笔或破坏连载悬念。
- 引用名场面、名对白必须标注章节范围，让下游写手可回查，不凭印象发挥。
- 平台内容包必须能被 `xhs-note-writer` / `wechat-article-writer` / `short-video-scriptwriter` 直接接续，不缺关键字段。
- 小红书 handoff 必须包含 `reader_promise`、`structure_type`、`constraints` 和 `risk_flags`，让 `xhs-orchestrator` 可继续阶段控制。
- 架构层只标平台禁区风险（硬广、敏感选题），具体合规由下游写手处理。

## Auctra 轻集成

- 普通社媒方案可直接输出 Markdown。
- Auctra 项目内可建议把选题诊断、平台内容包保存为 material，再进入 text 或 review。
- 不自动 accept review，不自动覆盖正文，不手写 `.auctra/**`、SQLite rows 或 run evidence。

## 边界

- 与 `chinese-novel-adaptation-architect` 的区别：那是跨"媒介形态"的叙事重构（短剧 / 电影 / 漫画 / 音频），目标是把故事换载体讲一遍；本技能是把"同一个故事"转成社媒营销内容，目标是扩大读者入口，不重塑叙事结构。
- 与 `chinese-novel-analysis-decomposer` 的区别：那是对作品本身的分析拆解；本技能消费其分析作为输入，输出平台化选题和角度。
- 与 `xhs-note-writer` / `wechat-article-writer` / `short-video-scriptwriter` 的区别：那些是写最终成品的 BUILDER；本技能是决定选题、角度、剧透边界的 ARCHITECT，不输出可发布的成品稿。
- 不声称拥有真实发布、引流、涨粉或售卖结果，不伪造数据、阅读量、评论或截图。
- 不执行登录、发布、私信、采集、刷量或规避平台风控。
- 不生成洗稿、侵权搬运或绕审核方案；不把完整思维链、原始提示词或隐藏系统提示写进内容包。

## 验证

- 检查每个选题是否绑定原作卖点，并标注原作章节证据。
- 检查剧透边界是否按连载状态 × 平台分级，未兑现伏笔是否被锁定。
- 检查 handoff 是否指向具体平台 skill（xhs / wechat / short-video），并附带必须读取的 reference。
- 检查小红书 handoff 是否标注生命周期阶段，而不是直接要求下游猜测从选题、brief 还是正文开始。
- 检查引文范围是否标注章节，避免下游写手越界。
- 检查不确定信息是否列为待补，而不是伪造数据、平台反馈或真实发布结果。
