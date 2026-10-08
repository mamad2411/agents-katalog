---
name: hyperframes-scene-animator
description: 接管 talking-head-hyperframes 的 READY_FOR_EXECUTION 交接，由主 Agent 完成字幕分镜与具体导演，先交付全镜头最终静态页审核，批准后再用快速子 Agent 协助实现互不冲突的镜头与动效，最后完成 HyperFrames proof、四遍审查与 preview-v1。适用于口播镜头、语义动效、转场、声音 cue 和整改；TEMPLATE_ONLY 或路径/hash/合同不完整时精确拒绝，不用于创建固定模板。
---

# HyperFrames Scene Animator

在固定舞台交接后，先完成全镜头最终静态页的人工审核，再制作动效并闭环至 `preview-v1`。固定模板仍归 `talking-head-hyperframes` 所有。

## 开工门禁

每次执行先读取：

1. 项目的 manifest 与 template handoff；
2. 已锁定的导演脚本、制作规格、素材计划、对齐字幕和 motion contract；
3. 本地 [AESTHETICS.md](AESTHETICS.md)；
4. 本地 [runtime adaptation contract](references/runtime-adaptation.md)；
5. 当前启用的 `hyperframes`、`hyperframes-core`、`hyperframes-animation` 与 `hyperframes-cli` skills。只有写 GSAP 时才加载对应 adapter/GSAP reference，只有实现真实 scene boundary 时才加载 transition overview、catalog 和所选转场类别。

进入 proof 与审片阶段时再读 [proof and review contract](references/proof-and-review.md)，不要在编排阶段提前加载。

首次执行任何项目 package script 前，先用本 Skill 自带的 `scripts/verify_project_bundle.mjs <project-dir>` 验证 factory-owned 脚本、完整 package script 集合和只含 `ignore-scripts=true` 的 `.npmrc`；任何额外 pre/post hook、项目 Node options 或字节差异都必须停止，不能执行项目代码。通过后只使用生成项目公开的 package scripts 运行校验、proof 和 failure gates；不要复制活动 HyperFrames skills 的运行时文档，也不要依赖不可复现的隐藏手工步骤。

只有 manifest 明确为 `READY_FOR_EXECUTION`，且 handoff 中每个必填输入的实际路径、项目相对路径、SHA-256、媒体/字幕校验和 motion-contract source hash 都与实物一致，才可写内容 composition。

遇到 `TEMPLATE_ONLY`、缺失文件、无效媒体/字幕、未确认导演决定、合同缺字段/未覆盖整片或 hash 不一致时：

- 立即拒绝执行；
- 按项目实际状态逐项列出缺失或无效项，包含字段/期望路径、实际路径、期望 hash、实际 hash 或无法取得的原因；
- 指明应回到 factory 还是上游锁定资料；
- 不创建或修改任何内容 composition、场景、动效、转场或声音 cue。

不得用临时导演、占位场景或“先做几个看看”绕过门禁。

## 五条防回退红线

1. **一镜头只讲一个命题。** 屏幕只留口播当下需要记住的关键字；主词必须在字号、对比、位置或空间上显著压过辅助信息。不要把解释性隐喻、来源备注、英文装饰词和多组数据同时堆在画面上。
2. **章节牌是事件，不是常驻挂件。** 章节只在独立场景中出现一次，让观众读懂后结束。不得让“招牌热菜”、`NO.01`、章节标签或装饰卡在后续镜头中持续占位。
3. **一个场景只有一层主空间。** 禁止“外面一层页面，里面又塞一层完整背景框”的 PPT 套娃，也禁止没有口播含义的系统框、权限夹、执行工位和未解释标签。概念改变就切新场景；所有可见元素都必须服务当下命题。
4. **先审静态定稿，再做任何动效。** 依据字幕交付每个镜头信息完全呈现时的最终静态页和整片联系表。未获得用户对整套静态镜头的明确批准，不得写动效、转场或整片预览。
5. **音频微剪以听感和音素完整性为准。** 不得只依赖 silencedetect、波形或字级时间戳判断插入/删除点；停顿只放在完整语义短语边界，不得切在一个字或辅音内。每次从未修改的已批准母带按 EDL 重建，先输出 6–10 秒试听并获得人工批准，再按分段时间偏移同步下游字幕、cue、时长和 hash。本 Skill 不直接改锁定人声；修改后必须回到上游重新锁定输入。

## 主 Agent 与快速子 Agent

- 主 Agent 是唯一导演、编辑与集成者：它负责字幕→beat→镜头的划分，锁定可见文字、素材、布局层级、每个镜头具体怎么写、时序、转场接力与验收标准，并审查全部合并结果。
- 完成主 Agent 的逐镜锁定简报后，把互不冲突的镜头页/镜头模块优先分配给快速子 Agent。调用 `spawn_agent` 时默认使用 `agent_type: worker`、`fork_turns: none`、`model: gpt-5.4-mini`、`reasoning_effort: medium`，并在自包含 prompt 中写清下面的任务合同；该模型不可用时，选当前最快且能稳定完成 HTML/SVG/GSAP 的 worker 模型。
- 每个子 Agent 必须获得自包含的逐镜任务：字幕时段、单一命题、最终静态图、允许的文字/素材、尺寸与设计 token、入/出状态、精确文件所有权和验收帧。子 Agent 只实现，不重新规划、不增删屏幕文案、不改镜头数量、不改全局视觉/动效语言。
- 子 Agent 只修改分配给它的独立文件；`content.html`、全局 timeline、shared styles/tokens、runtime adaptation、转场接力、音频/字幕及最终集成只由主 Agent 修改。场景不独立或强共享文件时，不强行并行。
- 审查可由其他 Agent 发现问题，但修改仍回到原镜头文件所有者或主 Agent；不得创建第二套竞争实现。所有 Agent 都必须适配共享工作区已有改动，不回退他人的工作。

## 执行路径

1. **锁定 handoff。** 先从本 Skill 运行 trusted bundle verifier，再运行 `npm run check:inputs`、`npm run check:fixed-stage` 与 `npm run check:motion-contract`，记录输入与 hash、允许修改的内容范围、不可改的导演决定、beat 状态 A→B、验收点、readable hold 和接力关系。首次接管运行 `npm run proof:lock -- <stable-executor-id>`；锁一旦存在只能由同一主 Agent id 继续。接受来源 `pipeline=remotion` 或 `hyperframes`，但不得改写来源 JSON。
2. **主 Agent 先完成分镜规划。** 在写 composition 前生成 `runtime-adaptation.json`，逐项追踪 source contract hash、root `DESIGN.md` hash、beat→scene state/hold、acceptance→snapshot、handoff→anchor/transition。依据对齐字幕和语义边界划分镜头，为每个镜头写锁定简报：时段、单一命题、屏幕关键字、素材、最终静态布局、前/后状态、动效语义和验收帧。复杂 choreography 同时生成或验证 `STORYBOARD.md`、`SCENE_SCHEMA.json`、`VECTOR_TEMPLATES.json`、`MOTION_PRIMITIVES.json`、`MOTION_MAP.json`。
3. **先校验映射。** 运行 `npm run check:runtime-map`。映射不完整、hold 引入动作、scene 入口重播、空转场或来源/设计 hash 漂移时停止，不先写 HTML。
4. **生成全镜头最终静态页。** 主 Agent 可按已锁定简报将独立镜头静态页分配给快速子 Agent。此阶段只做最终布局、SVG/图像/文字层级和素材适配，不写 GSAP、进场、转场、SFX 或整片预览。对每个镜头输出一张 1920×1080 最终静态图，并在 `review/static-vN/` 生成按时序排列的联系表和镜头清单，使用户不看动效也能判断信息层级和全片节奏。
5. **通过静态审核门。** 主 Agent 先做整片连续性与五条红线自查，再把全部静态页交给用户。只有获得用户对当前整套版本的明确批准，才记录 `STATIC_SCENES_APPROVED`。用户要求修改时仍留在本阶段；不允许只批准几个镜头就偷跑动效，也不允许由校验脚本、子 Agent 或主 Agent 代替用户授权。
6. **批准后才实现动效。** 主 Agent 锁定进场、状态变化、readable hold、转场接力和时序，再把互不冲突的镜头模块优先分配给快速子 Agent。所有动效都必须从已批准静态页出发并回到它所规定的可读状态，不得因为动效方便而改布局、增文案或发明新元素。每个真实 HyperFrames scene 都有逐场编写的显式入口；非最终 scene 在语义转场开始前保持可读，不得预先 fade；`readable-hold` 完全静止。
7. **限定工作面。** 只在 `compositions/content.html`、`compositions/scenes/`、上述 derived contracts、项目内容素材、`review/static-vN/`、acceptance/transition proof、executor review 与内部 preview 中工作。不得修改 `index.html` 固定 mounts、`styles.css`、`DESIGN.md`、固定背景、字幕、PIP 或最终人声资产。
8. **构建可 seek timeline。** 每个 composition 同步构建且只注册一个 `paused` GSAP master timeline，registry key 等于 composition id。禁止 `Math.random`、`Date.now`、async/Promise/timer 构建、手动 media playback/currentTime、无限 repeat、属性时间重叠和直接动画 timed video；PIP/人物只动画非 timed wrapper。
9. **遵守项目动效约束。** 本项目比 generic GSAP 建议更严格：不动画 `visibility` 或 `autoAlpha`，只用 `opacity`、`clipPath` 与 transform，并让 HyperFrames 管理 clip 生命周期。禁止通用 crossfade、共享 `enterStyle`、重复 `opacity+y` 进场和无语义循环。
10. **生成 proof。** composition 完成后运行 `npm run check:runtime-adaptation`，然后按 [proof and review contract](references/proof-and-review.md) 运行 `npm run proof:generate`（`proof:all` 是同义入口），产生带当前项目指纹与日志摘要的 input/fixed-stage/motion/runtime/stage/doctor/lint/validate/inspect/check/snapshot/animation-map/render receipts，以及全部 source acceptance snapshots、cue 前后帧、章节/密度状态、最宽字幕、转场中点、readable hold、1920×1080 联系表、完整内部预览、媒体尾部分析和执行报告。
11. **完成四遍审查。** 依次完成 Montage、Static、Motion、Delivery 四遍审查，并执行 Anti-PPT / AI 味硬拒绝门。Motion 必须实看完整 `internal-preview-vN.mp4`，静帧不得代替；Montage 只看联系表且不读字幕。proof 项状态只用 `PASS / FAIL / NOT_APPLICABLE`，lead finding 只用 `BLOCKER / MAJOR / MINOR`。
12. **绑定审批并晋级。** 所有整改回到原镜头文件所有者或主 Agent，只重跑受影响 proof 并记录版本和 recheck。先运行 `npm run proof:bind-review`，把执行报告、lead、四遍审查、recheck 及其实际文件字节绑定到当前项目指纹、执行锁和内部预览 SHA-256；再由明确的审批人运行 `npm run proof:approve -- <reviewer> <proof-version>`，生成不可静默漂移的审批收据并推进到 `REVIEW_APPROVED`。最后运行 `npm run proof:finalize`：先做 promotion preflight，再用可恢复的事务晋级为 `renders/preview-v1.mp4`，并以完整 proof validator 收口。预览、项目素材、审片文件或审批决定在审批后有任何变化都必须重新审片。

正式发布渲染不属于本 Skill；到 `preview-v1` 与审查闭环后停止，等待单独确认。

## 完成条件

只有主 Agent 保持唯一导演与集成所有权，整套静态镜头已获得用户明确批准，主 Agent/子 Agent 的文件所有权无冲突，锁定输入与 hash 仍一致，语义运动与 scene 入口/转场契约成立，proof 齐全，四遍审查通过且没有 open BLOCKER/MAJOR 或阻断首感的 MINOR，`preview-v1` 经受控晋级、可播放且最终 bundle validator 通过，才算完成。
