---
name: talking-head-hyperframes
description: 为 HyperFrames 口播或旁白项目创建、修复并验证固定舞台，锁定数字人 PIP 的区域、裁切、人物安全区和不透明背景，归档输入，生成 manifest 与 template handoff，并在就绪后按“字幕驱动的全镜头静态审核→动效”门禁路由到 hyperframes-scene-animator。适用于“新建 HyperFrames 口播模板”“准备或修复数字人/PIP”“导入音频字幕和制作资料”“检查模板能否开工”等请求；不负责镜头导演、内容场景、整片渲染或审片整改。
---

# Talking Head HyperFrames · Template Factory

只产出经过舞台证明的固定模板和可审计交接。内容执行属于 `hyperframes-scene-animator`。

## 先路由意图

- 只建或修复固定舞台、归档输入、检查就绪状态：由本 Skill 执行。
- 用户要求制作镜头，而工程尚无合格模板：先完成本 Skill 的职责，再按交接状态停止或路由。
- 工程已经 `READY_FOR_EXECUTION`，且用户只要求镜头实现、语义动效、转场、声音、proof 或整改：直接路由到 `hyperframes-scene-animator`，不要复制其流程。
- 用户明确调用本 Skill 做内容场景时，仍按上述边界路由，不能越权代做。

生成或验证工程前，必须读取当前启用的 `hyperframes` 与 `hyperframes-cli` skills。不要复制它们的运行时规则；所有 scaffold、校验和舞台 proof 都通过生成项目公开的 package scripts 复现。若这些脚本或实现资源尚未提供，明确报告缺少的能力并停止，不要临时发明替代工程。

## 唯一职责

本 Skill 负责：

- 创建或修复固定模板与稳定根 composition；
- 归档用户已经提供的锁定输入，保留源路径、项目相对路径、大小与 SHA-256；
- 校验媒体可解码性和时长、字幕 schema/时间、motion contract 覆盖与 source hash；
- 写 manifest 和 template handoff；
- 运行只证明固定舞台的结构检查与 stage proof；
- 根据就绪状态停止或路由下游。

本 Skill 不导演镜头，不写内容场景，不选择语义动效或转场，不做 SFX/BGM 设计，不渲染整片，不审片，也不整改内容实现。不得为了演示而加入标题页、三卡片、流程图、TopBar、通用 `enterStyle` 或全局 crossfade。

## 就绪状态

允许缺少正式输入时创建固定模板，但必须把状态写成 `TEMPLATE_ONLY`。manifest 与 handoff 应逐项列出每个缺失或无效输入，并给出期望路径、实际路径以及可获得的 hash/校验结果；不得伪造占位输入或假装就绪。

只有以下各项全部有效且相互一致时才写 `READY_FOR_EXECUTION`：

- 可解码且有精确时长的锁定完整人声音频；
- 非空、时间有效、与音频时长一致的对齐字幕；
- 用户已确认的导演脚本与制作规格；
- 素材计划；
- 覆盖整片、字段完整的 motion contract；
- 上述锁定输入的源路径、项目相对路径和 SHA-256，以及 contract source hash 比对结果。

口播视频、录屏、截图和字体按实际提供情况归档并记录；缺少可选媒体不冒充必填失败。输入矛盾、导演未确认或 source hash 不一致时保持 `TEMPLATE_ONLY` 并停止升级状态。

## 脚手入口

生成前读 [references/project-layout.md](references/project-layout.md) 确认固定层与下游所有权，再读 [references/input-handoff.md](references/input-handoff.md) 执行输入、hash 和就绪门。

只要挂载数字人或 PIP 占位，还必须完整读取 [references/pip-contract.md](references/pip-contract.md)。PIP 不是一个可随手摆放的视频：模板必须锁定外圈、媒体区、层级、裁切、人物安全区、不透明背景和审查证据。当前 Bozhou Digital Twin 的默认裁切是 `object-fit: cover; object-position: 66.7% 50%`；更换人物时允许用脚手参数覆盖，但覆盖值必须进入 manifest 并通过静态页与成片放大审查。

```bash
node scripts/scaffold_talking_head_hyperframes_project.mjs --project-dir /absolute/path/to/project [input flags]
node scripts/validate_inputs.mjs /absolute/path/to/project
node scripts/validate_fixed_stage.mjs /absolute/path/to/project
```

生成后必须在项目内运行 `npm run check:inputs` 和 `npm run check:fixed-stage`；需要完整 HyperFrames 静态/运行门时运行 `npm run check:template`。任何调用 HyperFrames 的 package script 必须保持精确版本 `0.7.65`。

固定舞台的背景像素证明运行 `npm run check:stage-parity`。它在隔离副本里把节目时长扩展到 10 秒，只显示真实固定背景，在 0s、4s、9s 截图，先校验三张用户确认的窄中心光斑网格 golden 的 SHA-256，再按 yuv420p 计算 SSIM；任一时刻低于 `0.995` 即失败。这个命令对 `TEMPLATE_ONLY` 和 `READY_FOR_EXECUTION` 都可运行，不实现内容镜头。

挂载数字人时，`npm run check:fixed-stage` 还必须拒绝以下状态：媒体层不在 `190×190px` 固定区、人物裁切未写入 manifest、PIP 背景没有不透明底色、媒体层与圆框层级反转、视频未静音、或回退到未校准的 CSS 默认。技术检查通过仍不能替代视觉批准：动效前的全镜头静态联系表必须包含 PIP；正式发布前必须从实际编码文件抽取至少一个 PIP 区域，裁成 `300×300px` 并放大 3 倍，确认圆内无舞台网格穿透且人物满足安全区。

`--force` 是原子修复：已有项目与其中所有路径必须不是软链接；完整模板在同级临时目录中生成和校验后才替换原目录。无参数修复会从既有 manifest 的项目内锁定文件恢复输入、时长、PIP 和来源记录，不能把 READY 项目降级。任何后期碰撞或失败都必须保持原项目逐字节不变。

## 舞台证明与交接

舞台 proof 只证明固定层、空的透明内容 composition、字幕/PIP 安全关系与稳定根挂载；不得借 proof 实现或渲染内容镜头。

- 用户只要模板：交付项目路径、manifest、handoff、stage proof 和完整缺失清单后停止。
- 用户还要求继续制作且状态为 `READY_FOR_EXECUTION`：把同一项目交给 `hyperframes-scene-animator`，由它实施下面的制作门禁。
- 状态为 `TEMPLATE_ONLY`：不得调用下游执行；明确列出阻塞项和修复方式。

## 下游制作门禁

路由下游时，明确交接并不得稀释以下约束：

1. 主 Agent 保持唯一导演与集成所有权：它负责字幕分段、镜头规划、画面层级、文字与素材取舍、每个镜头具体怎么写、动效语义与最终审查。
2. 方案锁定后，互不冲突的单镜头实现尽量委派给快速子 Agent；子 Agent 只按逐镜确定稿编码，不得重做导演、改文案、改镜头数量或改全局转场语言。
3. 依据对齐字幕为全片划分镜头，先生成每个镜头“信息完全呈现时”的最终静态页，组成可连续审阅的联系表。
4. 只有用户明确批准整套静态镜头后，下游才能写入进场、语义动效、转场、声音 cue 或整片预览。修改期间仍停留在静态阶段，不得用技术 proof 代替人的创意审核。

完成条件是固定舞台已证明，输入记录可审计，状态判断可复现，且没有任何内容场景、整片渲染或审片产物。
