---
name: shotfun-creator
description: 面向 AI 内容生产场景的 skill 集合，覆盖图片、视频、声音、数字人等内容生产能力。
---

# shotfun-creator

shotfun-creator 面向所有 AI 内容生产场景，是覆盖图片、视频、声音、数字人等能力的 skill 集合。它负责理解用户目标、自主选择合适的可用技能，并完成内容生产。用户只需要输入内容目标，它会帮助拆解任务、规划流程、完成工作任务，并可把已实现的工作流程沉淀为用户自己的 skill。

## 核心运行规则

1. 路由顺序：优先使用能完整覆盖用户目标的 workflow skill；其次使用 `task-skills/`；最后才下钻到 `scripts/cli/*.js` 或 `scripts/services/*.js` 原子能力。
2. 前置约定：调用 ShotFun 前读取 `references/calling-conventions.md` 和 `references/output-conventions.md`；缺少 `SHOTFUN_API_KEY` 时只做 dry-run 或引导配置，不提交真实任务。
3. 价格查询：当用户询问价格、费用、收费、积分、credits、成本或哪个模型更便宜时，先读取 `references/pricing.md`，按其中的价格表向用户展示相关条目；不要凭记忆报价。`references/model-catalog.md` 只作为模型选择目录，用户展示口径以 `references/pricing.md` 为准。
4. 脚本归属：新增 skill 的专用脚本、模板、示例输入、参考素材配置和辅助工具必须放进对应 skill 目录；主项目 `scripts/` 只放跨 skill 复用的稳定底层能力。
5. 安全边界：不要把 API Key、token、签名 URL、本机绝对路径、历史生成素材 URL、客户素材、私有项目名、角色资产或一次性生产参数硬编码到 skill 文件或主项目脚本中。
6. 汇报约定：最终回复优先给用户可直接使用的产物链接/本地路径、`outputDir`、`manifest` 和关键模型参数；不要粘贴原始 API 响应、内部 `task` 对象或大段 JSON。

新建 workflow/task skill 时，可在该 skill 目录下使用 `scripts/`、`templates/`、`examples/`、`references/` 等子目录承载专用内容。需要公开示例时，只使用无敏感信息的占位 URL 和最小示例数据。

## 前置检查

调用 ShotFun 之前：

1. 确认用户目标：完整工作流、单个任务产物，还是原子能力调用。
2. 读取 `references/calling-conventions.md`（环境变量、输出目录、安全约束）和 `references/output-conventions.md`。
3. 确认本地 `<cwd>/.env.local` 或运行环境中存在 `SHOTFUN_API_KEY`；如果缺失，先引导用户到 [shotfun.cn/agent](https://shotfun.cn/agent) 注册/登录 ShotFun 账户并获取 API Key，再把 key 写入当前项目根目录的 `<cwd>/.env.local`。对于当前仓库使用场景，默认就是 `shotfun-creator/.env.local`。不要继续提交真实任务；可用 `--dry-run` 帮用户预览执行计划。
4. 对多步骤或含糊请求，优先使用 `--dry-run` 预演。
5. 对用户期望本轮直接拿到结果的单能力任务，使用 `--wait`。
6. 对工作流执行，只有在真实运行有成本门槛的工作流时才使用 `--confirm`，不要在 dry-run 规划阶段使用。
7. `--project-code` 传用户填写的 ShotFun 项目名称，未传时默认为 `default`；`--project-name` 只控制本地归档目录，未传时也使用 `default`。
8. 如果任务反馈余额不足、积分不足或账户余额不够，先停止继续提交并引导用户到 [ShotFun 充值页](https://shotfun.cn/dashboard/recharge) 充值后再继续。

凭证优先来自本地 `<cwd>/.env.local`，其次才是运行时环境变量。不要把 API Key、token、私有 URL 或生成资产硬编码到 skill 文件或已跟踪文件中。

## ShotFun API Key 引导

当任务需要调用 ShotFun OpenAPI，但环境中没有 `SHOTFUN_API_KEY` 时，停止真实执行并用简短步骤引导用户：

1. 打开 [shotfun.cn/agent](https://shotfun.cn/agent)。
2. 注册或登录 ShotFun 账户。
3. 在账户/API Key 页面创建或复制 API Key。
4. 将 API Key 写入当前工作目录的 `.env.local`，格式为 `SHOTFUN_API_KEY=<用户的 key>`。在本仓库场景下，默认路径是 `shotfun-creator/.env.local`。
5. 后续所有 ShotFun CLI/service 会通过 `scripts/core/env-loader.js` 自动从 `.env.local` 读取。

推荐提示语：

```text
当前本地缺少 SHOTFUN_API_KEY，所以我还不能提交真实生成任务。你可以到 https://shotfun.cn/agent 注册/登录 ShotFun 账户并获取 API Key。拿到后我会把它写入当前工作目录的 .env.local，后续 ShotFun 任务会自动从这个文件读取。配置好后回复“继续”，我会接着执行。
```

如果用户明确要求你代写本地配置，直接把 key 写入当前项目根目录的 `<cwd>/.env.local`；在 `shotfun-creator` 仓库里就是 `shotfun-creator/.env.local`。不要在回复中复述密钥。`.env.local` 已被 `.gitignore` 的 `.env.*` 规则忽略。

## 需求澄清规则

当用户输入不够明确，且会影响成本、模型选择、产物质量或是否能执行时，先引导用户确认需求，不要直接猜测并提交真实任务。

必须澄清的情况：

- 缺少核心输入：例如没有提示词、没有参考图、没有口播稿、没有视频/图片 URL、没有项目名称或必要凭证。
- 输出规格不明确且会影响结果：例如图片比例、分辨率、视频时长、语言、音色、是否需要字幕、是否需要严格保留人物身份。
- 任务类型存在歧义：例如用户只说“做个视频”，但没有说明是图生视频、口播视频、单镜头视频还是完整工作流。
- 成本或执行风险较高：例如高分辨率、长视频、多步骤工作流、批量生成、会发布到外部平台。
- 参考素材的用途不明确：例如用户给了人物照片和场景图，但没有说明要换背景、合成场景、做口播图还是做视频。

澄清方式：

- 优先问 1-3 个最关键问题，不要一次性抛出长表单。
- 给出推荐默认值，帮助用户快速确认，例如“我建议 16:9、默认模型、先 dry-run，再正式生成”。
- 如果需求可以安全默认，先说明默认假设，再执行 dry-run；真实执行前仍需确认高成本或外部发布动作。
- 如果用户已经明确说“直接生成/按你建议来”，可以使用合理默认值继续执行。

## 主 Skill 调度规则

按以下顺序选择执行路径：

1. 如果用户描述的是端到端目标或跨渠道产物，且仓库存在 `workflow-skills/README.md`，先读取匹配的 workflow skill。
2. 如果用户描述的是一个输入输出明确的产物，先查 `task-skills/README.md` 并读取匹配的 task skill。
3. 如果用户只需要图片、视频、音频、视频分析、ASR、字幕、资产管理或余额查询中的一个原子能力，读取 `references/*.md` 并调用对应 CLI/service。
4. 如果没有现成 workflow/task skill，先用原子服务跑通 MVP，并把缺口作为后续可新增 skill 记录。

工作流 skill 可以调用 task skill；task skill 可以调用 atomic service。不要让 atomic service 反向依赖 task/workflow skill。

## 用户意图路由

| 用户意图 | 优先读取 | 推荐命令 |
| --- | --- | --- |
| 默认口播内容生产、口播形象图、口播视频、封面和可复用口播工作流 | `workflow-skills/koubo.md` | 先用 `gpt-image2`（即 gpt-image-2）生成/确认口播形象图，再按工作流规划脚本、声音、视频和封面 |
| 公众号文章一体化写作、封面和发布到草稿箱 | `task-skills/wechat-write-publish-allinone.md` | 先生成标题/正文/封面，再按发布条件推送到草稿箱 |
| 公众号封面图 | `task-skills/wechat-cover-image.md` | `node scripts/cli/image-generate.js ...` |
| 小红书/RedNote 图片卡片或卡片系列 | `task-skills/xhs-images-gen.md` | `node scripts/cli/image-generate.js --model gpt-image2 ...` |
| 任意内容生成图片、促销图、培训说明图 | `task-skills/universal-content-to-image.md` | 先设计 visual brief，再 `node scripts/cli/image-generate.js --model gpt-image2 ...` |
| 参考视频分析、抽帧和风格拆解 | `task-skills/reference-video-analysis.md` | `node scripts/cli/video-analyze.js ...` + 按需 `ffprobe` / `ffmpeg` 抽帧 |
| 口播场景图生成 | `task-skills/talking-head-scene-image.md` | `node scripts/cli/image-generate.js ...` |
| 真人口播风格视频 / 根据图片和口播稿生成完整口播视频 | `task-skills/scripted-talking-video.md` | 短稿走 single-shot；长稿或需穿插内容镜头时先做分镜和模型确认 |
| 创建、检查或渲染 HyperFrames 项目 | `task-skills/hyperframes-project.md` | `node scripts/cli/run-workflow.js --workflow news-broadcast-video ...` 或 `npx --yes hyperframes@0.6.30 render ...` |
| 给指定 skill 生成 Web 工作台、查看生产过程和产物 | `task-skills/workbench-web-skill.md` | HTML5 + Tailwind CSS 4 + Vite 静态工作台 |
| 一句话同时生图和生视频 | `references/model-catalog.md#单镜头工作流` | `node scripts/cli/one-shot.js ...` |
| 生成或编辑图片 | `references/model-catalog.md#图片生成` | `node scripts/cli/image-generate.js ...` |
| 将图片转成视频 | `references/model-catalog.md#视频生成图生视频` | `node scripts/cli/video-generate.js ...` |
| 生成语音或多模态音频 | `references/model-catalog.md#音频--tts` | `node scripts/cli/audio-generate.js ...`；默认模型 `seed_audio` |
| 试听或使用目录音色 | `references/model-catalog.md#音频--tts` | 显式选择 `--kind preview` / `--kind single` 和目录音色 |
| 视频去字幕 | `references/model-catalog.md#视频处理` | `node scripts/cli/video-process.js --operation subtitle-remove ...`；超分暂不支持 |
| 视频内容理解 / 多模态分析 | `references/model-catalog.md#视频分析` | `node scripts/cli/video-analyze.js ...` |
| 音频或视频转录 / ASR | `references/model-catalog.md#语音识别--asr` | `node scripts/cli/asr-transcribe.js ...` |
| 生成字幕并烧录到视频 | `references/model-catalog.md#字幕生成` | `node scripts/cli/run-workflow.js --workflow video-subtitle ...` |
| 克隆参考声音 / 参考音频生成语音 | `references/model-catalog.md#音频--tts` | `node scripts/cli/audio-generate.js --model seed_audio --voice-url <url> --text "..." ...`；必须有声音授权 |
| 查询可用积分余额 | `references/calling-conventions.md#余额查询` | `node scripts/cli/account-balance.js` |
| 批量执行同一种原子能力 | `references/calling-conventions.md#批量执行` | `node scripts/cli/batch-run.js --capability <id> --items <json-file> ...` |
| 调用已有后端文本任务 | `references/calling-conventions.md#文本任务` | `scripts/services/chat-task-service.js` 的 `runChatTask()`；必须提供实际 taskCode |
| 保存或修改结构化分镜 / 分组产物 | `references/calling-conventions.md#结构化产物保存` | `node scripts/cli/save-artifact.js ...`；需符合项目 manifest 和产物契约 |
| 创建 ShotFun 素材组或素材 | `references/model-catalog.md#项目素材` | `node scripts/cli/project-assets.js ...` |
| 生成一个短镜头视频 | `references/model-catalog.md#单镜头工作流` | `node scripts/cli/one-shot.js ...` |
| 生成角色素材包 | 暂未实现 | 说明限制；手动组合图片/文本服务 |
| 生成多镜头场景 | 暂未实现 | 说明限制；重复使用 `single-shot`，或等待工作流支持 |

### News Broadcast 输入纪律

当用户只说“用 News Broadcast Video Workflow 做一个播报视频”或类似请求，但没有在本轮明确给出主题、素材、JSON 路径或“复用某个历史 run”的指令时：

1. 先问用户现在想播报什么，不要在 `shotfun-output/`、`manual-inputs/` 或历史 run 里自动挑一个 JSON。
2. 可以运行 `node scripts/cli/run-workflow.js --workflow news-broadcast-video --project-name "<name>"` 生成 `needs-broadcast-input` 请求包，但不要把历史产物当作正式输入。
3. 只有当用户明确说要复用某个历史文件/run 时，才可以传 `--input-file` 指向 `shotfun-output/` 下的 JSON，并且必须同时传 `--allow-historical-input`。

只有当注册表中存在专用服务尚未支持的任务时，才把 `scripts/cli/run-template.js` 作为低层逃生口使用。

## 模型决策协议

调用任何 ShotFun service / CLI 之前，AI 必须按本协议选定 `--model` / `--kind` / `--operation`，不要让用户自己挑模型，也不要在 task-skills 文档里硬编码。

### 1. 读 catalog

每次调用前必读 `references/model-catalog.md`。该文件由 `scripts/core/dump-model-catalog.js` 从 `scripts/core/task-registry.js` 自动生成，包含所有可用 model 的 `key / priceTier / 推荐分 / 适用场景 / 能力约束 / 亮点 / 取舍`。registry 更新后必须重新运行脚本同步。用户询问价格或成本时，另读 `references/pricing.md`，并以该文件作为展示口径。

不要凭记忆调用未在 catalog 中列出的 model key。

### 2. 选 model 的判断顺序

1. **用户已显式指定**：用户消息含具体 `--model X` 或写了 model key，直接采用，不再决策。
2. **任务级硬约束**：根据输入特征过滤候选模型：
   - 有参考图 / `anchorPhoto` / `Asset://...` → 必须 `supports.referenceImage = true`。
   - 要求素材模式 → 必须 `supports.assetMode = true`，按 catalog 中当前模型约束选择。
   - 用户指定分辨率 1080P / 4K → 选 `defaults.resolution` 匹配的或显式 1080p 的 model。
   - 用户指定时长 → 校验模型的时长范围、整数约束和参考媒体限制。
   - 真实视频生成必须显式传 `--aspect-ratio`；先从用户目标、已确认的输出规格或参考素材确认比例，不依赖 CLI 隐式默认。
3. **场景匹配**：剩余候选按 `selection.scenarios` 与用户描述做语义匹配，命中场景的优先。
4. **预算偏好**：
   - 用户暗示「便宜 / 草稿 / 试试」→ 选 `priceTier ∈ {low, standard}` 中推荐分最高的。
   - 用户暗示「最好 / 发布 / 投放」→ 进入下面的高成本确认流程。
   - 用户未表态 → 默认走低成本，`priceTier = standard` 推荐分最高者优先；同分按 credits 升序。
5. **同分裁决**：先看 `selection.tags` 中 `default` 标签；再看 `recommendationScore`；再看 `credits` 升序。

### 3. 静默推进 vs 复述确认

**默认静默推进**（不打断对话）：

- `priceTier ∈ {low, standard, free}`
- 单次调用、`--dry-run`、`--wait` 单产物
- 用户已显式指定 model 或说过「按你建议」/「直接生成」

静默推进时 AI 仍要在最终汇报里写明实际使用的 `model` 和一句话原因（如 `model: nano2 — 通用稳定 + 支持参考图`）。

**必须复述确认**（拦截一步，等用户回应）：

- `priceTier ∈ {high, premium}`
- 高分辨率或其他高成本规格，以当前 catalog 的成本和约束为准
- 工作流多镜头 / 批量生成 / 单次任务 ≥ 5 个产物
- 用户描述含「发布 / 上线 / 投放 / 给客户 / 给老板 / 上传到平台」
- 单次预估 credits ≥ 12

复述格式（保持简短）：

```
我打算用 <model-key>（<credits> credits，<一句话原因>），需要换吗？
可选：<其他 1-2 个候选 key + 价格差异>
```

用户回复任一以下视为确认：「是 / 行 / 可以 / 继续 / 用这个 / 按你建议」。回复具体 key 视为指定。回复「换 / 不要 / 太贵」要重新决策并复述。

### 4. 决策可追溯

- 工作流（写 manifest 的场景）：把最终选定的 `model` 和选中原因写进 `manifest.json` 的 `decision` / `notes` 字段（若 runtime 暂未支持该字段，可暂留在 step sidecar）。
- 单次 CLI 调用：在最后向用户的汇报里附 `model + 一句话原因`。

### 5. 例外

- 音频默认使用 `seed_audio`（CLI kind 为 `seed-audio`），包括普通音频生成和参考音频生成；不默认使用 MiniMax 或 CosyVoice。仅用户明确选择目录音色或旧服务时使用 `single` / `preview` / `clone` / `clone-direct`。视频处理、素材管理按用户意图选择对应 `--operation` / `--action` 即可。
- 单镜头工作流的图片和视频步骤由当前 registry 与任务约束共同选择；查看 dry-run 的 `modelSelection`，不沿用旧别名或旧价格。

## 当前可用的任务生成能力

已端到端实现：

- 通过 `image-generate.js` 生成或编辑单张图片。
- 通过 `video-generate.js` 执行图生视频。
- 通过 `audio-generate.js` 执行 TTS/音频生成。
- 通过 `video-process.js` 执行视频处理。
- 通过 `one-shot.js` 执行一句话生图 + 生视频。
- 通过 `run-workflow.js --workflow single-shot` 执行单镜头工作流。
- 通过 `project-assets.js` 创建素材组和素材。
- 通过 `video-analyze.js` 分析视频，支持本地代理和长视频分段。
- 通过 `asr-transcribe.js` 转录音频或视频。
- 通过 `run-workflow.js --workflow video-subtitle` 执行 ASR、生成 SRT 和字幕烧录。
- 通过 `audio-generate.js --model seed_audio --voice-url <url>` 执行参考音频生成；`clone-direct` 仅作为显式选择的旧服务保留。
- 通过 `account-balance.js` 查询 OpenAPI 可用积分；查询失败不等于余额不足。
- 通过 `batch-run.js` 批量调用 schema 中可批处理的服务，保留失败项和恢复信息。
- 通过 `chat-task-service.js` 调用已知后端文本任务，使用 UTF-8 base64 的 `userMessage` 协议。
- 通过 `save-artifact.js` 按契约保存分镜、分组计划等产物；通过 `model-json-result.js` 解析和审查模型 JSON。
- 通过 `supplement-video-service.js` 提交、等待和导出补镜；通过 `scripts/media/compatible-video-assembly.js` 合成兼容视频。

本地视频代理、字幕烧录及视频拼接需要 `ffmpeg` / `ffprobe`。会员区域默认 `CN`，国际账号在私有环境配置中设置 `SHOTFUN_REGION=EN`。桌面宿主注入登录态时仍须验证账号区域，不可用手动配置绕过。

## 批量任务执行经验

多图生成时不要串行执行 `image-generate.js --wait` 等完一张再提交下一张。推荐流程：

1. 先为每张图生成独立 prompt、参考图 URL 和 sidecar JSON。
2. 优先用 `batch-run.js` 并发执行，显式设置 `--concurrency 3` 或 `SHOTFUN_CONCURRENCY=3`；运行时默认/最大并发度为 50，高成本模型或网络不稳时降到 `2`。
3. 记录每个任务的 `taskNo`、输入 prompt、参考图 URL、模型、项目名和本地 sidecar 路径。
4. 统一轮询所有 `taskNo` 到终态，成功后再下载或整理远程 URL。
5. 单个任务超时但后端仍是 `RUNNING` 时，不要重新提交扣费；继续用 `taskNo` 查询或恢复。

适用场景：多页 PPT 图片重绘、小红书多图卡片、批量封面、任意内容多图展示图。单张图或需要人工逐张确认风格时，仍可串行生成。

### 批量图片归档默认规则

对小红书、多图封面、系列海报等批量图片任务，默认不要只返回分散在各个 run 目录里的原始图片。

- 生成完成后，应额外整理一个同批次的聚合目录。
- 聚合目录下统一使用 `card-01.png`、`card-02.png` 这类命名。
- 同时提供一个 `index.json`，记录每张图的 `taskNo`、原始 run 路径、批次路径、标题和顺序。
- 如果用户明确要求保留原始 run 结构，再只返回分散路径。

暂未作为工作流实现：

- `short-drama`：把故事、角色、分镜、图片、视频和处理串成一个可恢复流程。
- `character-pack`：多视角一致角色素材。
- `video-scene`：包含多个协同镜头的单场景。
- 工作流 `--fetch-remote` 仍未实现；单能力媒体任务使用 `--wait` 后默认下载产物并返回本地路径。
- 导出可分享的 manifest 脱敏版本，隐藏私有/签名 URL。
- `scripts/core/task-registry.js` 中的价格只作为模型决策快照；用户询价以 `references/pricing.md` 为准。

不要把未支持的工作流承诺为完整自动化能力。应提供最接近的已实现路径，并明确说明限制。

## 命令模板

使用 `{baseDir}` 表示包含本 `SKILL.md` 的目录。

### 单镜头视频

默认流程：用户一句话先生成图片，再基于该图片生成视频。用户说“一句话生图和生视频”“generate an image and video from this prompt”或“make this into a short shot”时使用。

最短入口：

```bash
node {baseDir}/scripts/cli/one-shot.js \
  --project-code <project-name> \
  --prompt "A cinematic sunrise over a quiet lake" \
  --confirm
```

请求含糊或用户要求先预览时，先规划：

```bash
node {baseDir}/scripts/cli/one-shot.js \
  --project-code <project-name> \
  --prompt "A cinematic sunrise over a quiet lake" \
  --dry-run
```

使用已有图片：

```bash
node {baseDir}/scripts/cli/run-workflow.js \
  --workflow single-shot \
  --project-code <project-name> \
  --prompt "Slow camera push-in, soft morning haze" \
  --image-url "https://example.com/scene.png" \
  --confirm
```

恢复工作流：

```bash
node {baseDir}/scripts/cli/run-workflow.js \
  --workflow single-shot \
  --project-code <project-name> \
  --prompt "A cinematic sunrise over a quiet lake" \
  --resume "<run-id>" \
  --confirm
```

### 图片

```bash
node {baseDir}/scripts/cli/image-generate.js \
  --project-code <project-name> \
  --prompt "A polished product poster, studio lighting" \
  --model nano2 \
  --wait \
  --agent-output
```

带参考图：

```bash
node {baseDir}/scripts/cli/image-generate.js \
  --project-code <project-name> \
  --prompt "Keep the character, change outfit to a black suit" \
  --image-url "https://example.com/character.png" \
  --model nano2 \
  --wait \
  --agent-output
```

### 图生视频

```bash
node {baseDir}/scripts/cli/video-generate.js \
  --project-code <project-name> \
  --prompt "Animate this character with a slow confident walk" \
  --image-url "https://example.com/character.png" \
  --model minimax-h3-768p-cheap \
  --aspect-ratio 16:9 \
  --asset-mode none \
  --wait \
  --agent-output
```

当请求需要素材模式参考行为时，使用支持 asset 模式的模型，例如 `sd2.0-720p`：

```bash
node {baseDir}/scripts/cli/video-generate.js \
  --project-code <project-name> \
  --prompt "Animate this character, preserve identity" \
  --image-url "https://example.com/character.png" \
  --model sd2.0-720p \
  --aspect-ratio 16:9 \
  --wait \
  --agent-output
```

### 语音 / 音频

普通音频生成和声音克隆（参考音频生成）默认都用 `seed_audio`。可传 `--prompt` 描述声音，也可用 `--text` 提供准确口播稿；参考声音通过 `--audio-url` 或 `--voice-url` 传入，不需要目录音色 ID。

价格为 **5 积分/秒（人民币 0.02 元/秒）**，例如 10 秒为 50 积分、0.20 元。先确认目标时长再估算费用；未传 `--duration-seconds` 时默认 5 秒，长稿先分段并确认模型支持的时长，不把整篇稿件塞进默认 5 秒任务。参考音频必须获得声音授权，Seed Audio 不承诺生成可复用的 `voiceId`。

```bash
node {baseDir}/scripts/cli/audio-generate.js \
  --project-code <project-name> \
  --model seed_audio \
  --duration-seconds 5 \
  --text "你好，这是语音生成测试。" \
  --wait \
  --agent-output
```

参考声音生成语音：

```bash
node {baseDir}/scripts/cli/audio-generate.js \
  --project-code <project-name> \
  --model seed_audio \
  --voice-url "https://example.com/voice.mp3" \
  --duration-seconds 5 \
  --text "你好，这是克隆音色后的语音生成测试。" \
  --wait \
  --agent-output
```

只有用户明确需要目录音色时才使用 `--kind single --voice-platform <platform>`；音色目录见 `references/voice_<platform>.json` 和 `references/voice-catalog-format.md`。旧克隆流程仍可显式选择 `--kind clone` 或 `--kind clone-direct`，不作为默认入口。

### 视频处理

```bash
node {baseDir}/scripts/cli/video-process.js \
  --project-code <project-name> \
  --operation subtitle-remove \
  --video-url "https://example.com/input.mp4" \
  --wait \
  --agent-output
```

当前 `--operation` 仅支持 `subtitle-remove`；不要调用已移除的 `upscale`。

### 项目素材

```bash
node {baseDir}/scripts/cli/project-assets.js \
  --project-code <project-name> \
  --action asset-group-create \
  --name "Hero refs" \
  --description "Reference images" \
  --wait
```

```bash
node {baseDir}/scripts/cli/project-assets.js \
  --project-code <project-name> \
  --action asset-create \
  --group-id 123 \
  --url "https://example.com/hero.png" \
  --name hero \
  --asset-type Image \
  --wait
```

## 输出规则

单能力 CLI 默认返回面向任务的 JSON。当调用方需要稳定的 `userArtifacts` JSON、而不是原始 `task` 对象时，对图片、视频、音频和视频处理 CLI 添加 `--agent-output`。工作流始终返回面向 Agent 的 JSON：

```json
{
  "ok": true,
  "runId": "20260514-031211-a1b2c3d4",
  "outputDir": "/abs/path/to/shotfun-output/...",
  "manifest": "/abs/path/to/manifest.json",
  "userArtifacts": [
    { "kind": "video", "name": "video", "url": "https://..." }
  ],
  "cost": { "estimated": 0, "currency": "CNY" }
}
```

返回图片、视频、音频结果时，默认把本地路径和线上 URL 都格式化成可点击链接；优先给本地路径，其次补充线上 URL。不要只用纯文本路径展示。

向用户汇报时：

- 优先给出来自 `userArtifacts` 或 `resultUrls` 的最终产物 URL 或本地路径，并用可点击链接格式输出。
- 对工作流运行，说明 `outputDir` 和 `manifest`。
- 对分组项目运行，在有帮助时说明 `projectName`、`projectSlug`，以及项目 `latest.json`/`index.jsonl` 的位置。
- 不要粘贴内部 `task` 对象、token、签名 URL 查询参数细节、原始 API 响应或大段 JSON。
- 如果 URL 看起来是签名或私有链接，告诉用户它可能会过期，并建议下载或妥善保存。

## 失败与恢复规则

- 缺少 API key、用户输入的项目名称、提示词、输入文件、URL 或必需选项：停止并报告缺失输入。
- API 任务失败：报告 `taskNo`、状态和人类可读错误；不要隐藏失败。
- 如果失败原因是任务余额不足或积分不足，明确提示用户去 [ShotFun 充值页](https://shotfun.cn/dashboard/recharge) 充值。
- 超时：如果存在 `taskNo`，将其报告为可恢复状态。
- 工作流部分失败：保留 `manifest.json` 和步骤 sidecar 文件，然后建议使用 `--resume <run-id>`。
- 只有当工作流输入 hash、注册表版本、工作流版本和步骤输入 hash 都匹配时，恢复才安全。工作流版本不匹配时必须重新运行。
