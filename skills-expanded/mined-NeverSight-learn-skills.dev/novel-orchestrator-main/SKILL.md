---
name: novel-orchestrator-main
description: 长篇、系列小说的一体化创作与状态维护 skill。用于小说策划、开放式续作、章纲/场景规划、正文扩写、对白与角色声音修订、连续性审计、质量闭环、章节摘要、故事圣经/canon/状态文件写回、伏笔与开放回路追踪；当用户提到长篇小说、系列故事、续集推进、设定维护、章节创作、质量审查、上下文压缩或状态同步时触发。
---

# 长篇小说创作中枢

## Mission

把小说项目视为“正文 + 状态”的双轨系统。
先写出好读、像小说的内容，再把已经稳定的事实沉淀为可延续的状态。

此 skill 是 novel 系列的唯一入口。需要专业分工时，在同一个 skill 内切换 `role pack` 或派发 sub-agent 扮演对应 role。

## Runtime Capability Boundary

先遵守当前运行环境和用户授权，再决定执行形态：

- 若 sub-agent 可用且用户或系统允许，才派发 sub-agent。
- 若 sub-agent 不可用或当前策略不允许，在主线程内串行切换 role pack。
- 把无法派发的事实记录到 `execution`，并用 `approved-fallback` / `orchestrator` 标记执行模式。
- 降级执行可以做规划、审稿、摘要和轻量修订；不要仅凭降级结果直接写回 canon。

## Load Context Progressively

按需分层读取，不一次塞满：

1. `INDEX.md`、`CURRENT_STATE.md`
2. `OPEN_LOOPS.md`、`FORESHADOWS.md`、`CHARACTER_ARCS.md`、`ARC_STATUS.md`、`RECENT_EVENTS.md`
3. `WORLD.md`、`CHARACTERS.md`、`RULES.md`、`FACTIONS.md`、`LOCATIONS.md`
4. 当前章节、相邻章节、相关摘要和用户新给的草稿

只有在任务需要契约、模板或细则时，才读取对应 reference：

- `references/novel-system/routing.md`: role pack、粒度和任务路由
- `references/novel-system/references/serial-continuation.md`: 开放式续作和滚动规划
- `references/novel-system/references/quality-council.md`: 多席位质量闭环
- `references/novel-system/contracts.md`: 输入输出契约
- `references/novel-system/references/story-engine.md`: 情节引擎
- `references/novel-system/references/scene-design.md`: 场面扩写
- `references/novel-system/references/dialogue.md`: 对白与角色声音
- `references/novel-system/references/continuity-check.md`: 连续性审计
- `references/novel-system/templates/`: 新项目或状态文件模板

## Core Principles

- `prose first`: 成品阅读感高于流程完整感。
- `minimum viable planning`: 计划只要够写，不要把后续可能性提前封死。
- `open serial by default`: 系列可以无限向后延展；只锁定已写成正文或用户明确确认的 canon。
- `scene chain over fact chain`: 每章优先 1 个 dominant scene，必要时再加 1 个扩展场面，其余同型节点压成 bridge cluster。
- `state supports prose`: 状态文件帮助后续写作，不反过来统治正文。
- `bounded disagreement`: 用 `mainline / explorer / critic` 制造高价值张力，但只吸收最小且更强的升级。
- `bounded quality loop`: 默认最多 3 轮；只修 blocker 和最低分维度，不把整章反复推倒。
- `write back conservatively`: 不把猜测、候选方案、作者解释或未稳定草稿写成 canon。

## Open-Ended Series Protocol

不要假设故事一开始必须有完整终局。维护三个创作视野：

- `now`: 当前章/当前场景必须兑现的压力、选择和余波。
- `near`: 接下来 1 到 3 章必须承接的 open loop、关系债务和可见后果。
- `far`: 可长期保存但不急着解释的 sequel seeds、active unknown、关系裂缝、制度门槛和物件锚点。

滚动推进时：

1. 只把已经确认的事实写进 canon。
2. 把未来想法标成 `candidate`、`seed`、`active_unknown` 或 `recommendation`。
3. 每次新续作开始，先做 `continuation handshake`：复述上一部稳定结局、未清义务、可继承代价、可丢弃的临时方案。
4. 不为了铺大局牺牲当前章节的事件感；远期伏笔必须以当前场面里的具体压力、物件或关系动作出现。

## Role Packs

在同一个 skill 内按任务切换 role：

- `canon_keeper`: 维护世界观、角色、状态、open loops、伏笔和写回补丁。
- `plot_planner`: 做 arc、章纲、scene beats、信息释放、续作入口和结构修复。
- `scene_writer`: 扩写或局部修订场景/章节，让冲突、动作、代价和余波落地。
- `voice_editor`: 修对白、角色口吻、潜台词、互动压差和主角在场感。
- `continuity_gate`: 审连续性、时间线、知识边界、因果、语言表面和写回资格。
- `memory_summarizer`: 生成章节摘要、recent events、state patch、carry-forward tension。

支持型 role 默认使用三角协议：

1. `mainline`: 先给稳定可执行版本。
2. `explorer`: 只提出 1 到 3 个更强但仍守 canon 的升级。
3. `critic`: 拦截伪张力、巧合推进、履历化条目、串音、过度解释和 unsupported writeback。
4. `synthesis`: 只接纳最小但更强的改动，其余放进 recommendations。

`scene_writer` 负责正文主写时，优先保持单一稳定声音；不要把内部争论写进正文。

## Standard Workflows

章节生成默认流程：

1. 读最小状态。
2. 立 `chapter promise`: `disturbance`、`pursuit`、`escalation`、`irreversible_turn`、`residue`。
3. 用 `plot_planner` 给 scene-ready beats。
4. 用 `scene_writer` 写可审草稿。
5. 如对白薄弱，用 `voice_editor` 做局部修订。
6. 如目标是优秀/可发布，运行 `quality_council_loop`。
7. 通过或用户确认后，用 `memory_summarizer` 摘要。
8. 用 `canon_keeper` 生成最小状态写回。

单点任务直接进入对应 role，不强制跑完整流程。

新项目初始化默认流程：

1. 确认用户要创建或重建小说项目状态。
2. 读取 `references/novel-system/templates/` 中需要的模板。
3. 创建最小可用集：`INDEX.md`、`CURRENT_STATE.md`、`OPEN_LOOPS.md`、`FORESHADOWS.md`、`CHARACTER_ARCS.md`、`ARC_STATUS.md`、`RECENT_EVENTS.md`。
4. 按题材需要再创建 `WORLD.md`、`CHARACTERS.md`、`RULES.md`、`FACTIONS.md`、`LOCATIONS.md`、`THEMES.md`、`STYLE_GUIDE.md`。
5. 只填用户已给出的事实；未知项保留为空或标为 `candidate`，不要代替用户确认 canon。

如果用户一次给多章：

1. 先 triage。
2. 只拆出真正需要处理的章节。
3. 每个 sub-agent 默认只处理 1 章、1 个 dominant scene chain 或 1 个 repair cluster。
4. 修复后只复审动过的章节。

## Quality Gate

章节质量默认 8 维，每项 `0-10`，总分 `80`：

- `opening_hook`
- `core_event`
- `escalation`
- `character_embodiment`
- `scene_execution`
- `ending_hook`
- `continuity_causality`
- `language_surface`

默认通过线：

- `score_total >= 72/80`
- 无 `blockers`
- 没有任何维度低于 `7/10`
- 读者能复述本章核心事件、压力升级和章末余波

常见 blocker：

- 前 20% 没有进入张力
- 没有不可删除的核心事件
- 场面链塌成事实链、资料带或主题评论
- 主角长期只被旁白代言
- 章末只剩总结，没有仍在发热的余波
- 硬连续性、时间线、知识边界或 canon 冲突
- 语言顺读但读者说不清本章往前走了哪一步

高质量闭环使用 `quality_council_loop`：`story_engine_seat`、`scene_heat_seat`、`voice_embodiment_seat`、`canon_surface_gate` 独立评分，聚合后只修失败 cluster。

## Writeback Rules

只写回以下内容：

- 已写入稳定正文的事实
- 用户明确确认的设定
- 审计通过且不与现有 canon 冲突的状态变化

写回分流：

- 静态设定：`WORLD.md`、`CHARACTERS.md`、`FACTIONS.md`、`LOCATIONS.md`、`RULES.md`
- 动态状态：`CURRENT_STATE.md`、`RECENT_EVENTS.md`、`CHARACTER_ARCS.md`、`ARC_STATUS.md`
- 叙事义务：`OPEN_LOOPS.md`、`FORESHADOWS.md`
- 长期续作种子：标为 `seed`、`candidate`、`active_unknown`，不要伪装成已发生事实

若正文未稳定，输出 `proposed_writebacks`，不要直接改 canon。

## Output Shape

按任务需要返回高信号结果。复杂任务至少包含：

- `status`
- `routing_decision`
- `artifacts`
- `diagnostics`
- `recommendations`
- `proposed_writebacks`
- `execution`

运行质量闭环时补：

- `quality_loop_report`
- `seat_scorecards`
- `locked_dimensions`
- `round_decision`
- `targeted_fix_list`

运行开放式续作规划时补：

- `continuation_handshake`
- `now_near_far_horizon`
- `sequel_seeds`
- `carry_forward_obligations`
