---
name: framevideo-ai-production
description: FrameVideo 的中文 AI 生产子流程。用于从原始剧本、剧情梗概、已有分镜 Clip、视频 Shot、参考图资产或单视频创意出发，完成剧本转分镜、分镜聚合为视频任务、提示词润色，并在需要真实生成时交接给蝉镜 Chanjing AIGC adapter 生成图片/视频资产后回填 FrameVideo composition。适用于用户要求端到端 AI 视频生产、视频工作流编排、分镜脚本生成、视频任务规划、Clip 聚合为 Shot、蝉镜 AIGC 生图/生视频任务规划、或从创意走通到 FrameVideo 预览/渲染的场景。
---

# FrameVideo AI 生产工作流

## 何时使用 (When To Use)

使用此 skill 当用户要求：

- **剧本转分镜** — 从原始剧本、故事梗概生成 Clip 级分镜
- **视频任务规划** — 将 Clip 聚合为 Shot 级视频生成任务
- **提示词润色** — 将简短创意润色为可直接投喂模型的最终提示词
- **蝉镜 AIGC 生成** — 使用蝉镜平台生图/生视频
- **端到端 AI 视频生产** — 从创意到最终 FrameVideo composition 的完整流程

## 不要使用 (Do NOT Use)

避免使用此 skill 当：

- **仅编辑 FrameVideo HTML** — 使用 `framevideo` skill
- **仅下载蝉镜音乐/音效** — 使用 `framevideo-media` skill
- **仅配音/字幕** — 使用 `framevideo-voiceover-ssml` + `framevideo-media`
- **数字人视频** — 使用 `chanjing-digital-human` skill
- **已有完整素材的手动剪辑** — 使用 `framevideo` skill

---

## 快速开始 (Quick Start)

### 场景 1: 从剧本生成分镜

```
用户: 帮我把这个剧本转成 AI 视频分镜：
【剧本内容】
场景一：清晨，阳光洒进房间...
```

系统行为：
1. 读取 `references/storyboard-script-generation.md`
2. 生成 Clip 级分镜脚本
3. 输出结构化 Clip 列表

### 场景 2: 规划视频生成任务

```
用户: 我有 10 个 Clip，帮我规划成视频生成任务

【Clip 列表】
```

系统行为：
1. 读取 `references/video-task-planning.md`
2. 聚合 Clip 为 Shot (每个 Shot ≤15 秒)
3. 输出 Shot 级任务规划

### 场景 3: 端到端生产

```
用户: 从这个剧本直接生成视频，用蝉镜 AIGC

【剧本内容】
```

系统行为：
1. 读取 `workflow-and-handoff-formats.md`
2. 剧本 → Clip → Shot → 蝉镜 AIGC Plan
3. 交接给 `chanjing-digital-human` 执行生成
4. 回填到 FrameVideo composition

---

## 核心单位

- `Script`: 原始剧本、剧情梗概、对白、场景描述或未结构化故事。
- `Clip`: 细颗粒度分镜单位，通常一条 Clip 只有一个主要动作、视觉重点或情绪节拍。
- `Shot`: 视频模型一次生成任务，由一个或多个连续 Clip 聚合而成，通常不超过 15 秒。
- `Final Prompt`: 可直接投喂视频模型的最终提示词，包含主体、场景、动作、台词、镜头语言、光影、环境动态和参考资产声明。
- `Chanjing AIGC Plan`: 面向蝉镜 AI Creation 的结构化任务计划，包含 `creation_type`、模型选择依据、payload 字段来源、幂等 fingerprint 输入、资产输出目录和 FrameVideo 回填位置。

## 渐进式披露规则

根据用户请求只读取必要 reference：

- 需要从原始剧本、短剧、网剧、影视片段生成分镜脚本时，读取 `references/storyboard-script-generation.md`。
- 需要把已有 Clip 合并、拆分、分组或规划为视频生成 Shot 时，读取 `references/video-task-planning.md`。
- 需要把单视频故事、参考图标签或简短剧情润色为最终模型提示词时，读取 `references/single-video-prompt-polisher.md`。
- 需要使用蝉镜 AIGC 真实生成图片/视频、把 Shot 转换为 AI Creation 任务、或将生成资产回填到 FrameVideo composition 时，读取 `references/chanjing-aigc-handoff.md`，并按需读取 `../chanjing-digital-human/references/ai-creation.md`。
- 需要判断工作流、转换格式、串联多阶段产物或处理端到端生产时，读取 `references/workflow-and-handoff-formats.md`。
- 用户已有前阶段输出并要求局部修改时，识别修改所在层级，只读取对应层级的 reference，不加载其他文件。

只有在用户要求“完整流程”“从剧本到最终提示词”“全部阶段都要”时，才按顺序读取多个 reference。否则保持最小读取。

## 入口判断

1. 用户提供 `Script`，并要求分镜、镜头脚本、AI 生图分镜、AI 视频分镜、故事板：
   - 读取 `storyboard-script-generation.md`。
   - 输出 Clip 级分镜。
2. 用户提供编号分镜、Clip 列表、镜头脚本或故事板，并要求规划视频生成、聚合、合并、拆分：
   - 读取 `video-task-planning.md`。
   - 输出 Shot 级视频任务规划。
3. 用户提供单视频创意、短剧情、参考图资产标签，要求提示词润色或直接生成视频提示词：
   - 读取 `single-video-prompt-polisher.md`。
   - 输出最终提示词。
4. 用户要求使用蝉镜 AIGC 生图、生视频、生成 B-roll、生成镜头素材，或要求从 Shot 继续到真实生成：
   - 读取 `chanjing-aigc-handoff.md`。
   - 若输入仍是 Script，先读取 `storyboard-script-generation.md` 生成 Clip。
   - 若输入仍是 Clip，读取 `video-task-planning.md` 聚合 Shot。
   - 按 Shot 输出 Chanjing AIGC Plan，后续交给 Chanjing AI Creation 提交/轮询/下载。
5. 用户要求端到端生产：
   - 先读取 `workflow-and-handoff-formats.md`，确认格式衔接。
   - 再读取 `storyboard-script-generation.md` 生成 Clip。
   - 再读取 `video-task-planning.md` 聚合 Shot。
   - 若只需要提示词，读取 `single-video-prompt-polisher.md` 生成 Final Prompt。
   - 若需要真实生成或 FrameVideo 项目落地，读取 `chanjing-aigc-handoff.md` 生成 Chanjing AIGC Plan，再交给 FrameVideo 编排、预览、校验。
6. 用户已有前阶段输出，要求局部修改、重写某个 Shot 或 Clip、调整节奏、重新分配台词：
   - 识别修改涉及的层级（Clip / Shot / Final Prompt）。
   - 只加载对应层级的 reference，不重新跑整条管线。
   - 保留未涉及修改的部分原样输出，只改动用户指定的范围。
   - 若修改跨越多个层级（如重写某个 Clip 并更新对应 Shot），按从上到下顺序依次处理。

## 标准管线

端到端请求按以下顺序执行：

```text
Script
-> Clip 级分镜
-> Shot 级视频任务
-> Final Prompt 或 Chanjing AIGC Plan
-> 本地生成资产
-> FrameVideo composition
```

每一阶段都必须保留：

- 原始角色名、人物关系和事件顺序。
- 原始台词；除非用户明确要求改写，否则不得润色台词内容。
- 参考图、角色图、道具图等资产标签的原始格式。
- 关键连续性信息：人物身份、服装、道具、站位、光线方向、空间状态和动作方向。

## 输出选择

根据用户要的深度决定输出到哪一层：

- 只要分镜：停在 Clip。
- 要视频任务规划：停在 Shot。
- 要模型可用提示词：输出 Final Prompt。
- 要蝉镜 AIGC 真实生成：输出 Chanjing AIGC Plan，并交接给 Chanjing AI Creation。
- 要完整方案：依次输出工作流定位、Clip 分镜、Shot 规划、Final Prompt 或 Chanjing AIGC Plan、自检。

## 交接原则

- 从 Clip 到 Shot 时，优先看核心生成状态是否稳定，而不是机械按景别或正反打切分。
- 从 Shot 到 Final Prompt 时，合并动作链和情绪链，但不要把不同段落目标强行塞进同一条提示词。
- 从 Shot 到 Chanjing AIGC Plan 时，不得硬编码模型参数。先让 Chanjing AI Creation 获取当前账号可用模型，再根据所选模型的 `params_config.fields` 构造 payload。
- 若单个 Shot 内出现复杂群体调度、强动作冲突、大量台词、复杂手部动作、空间转场或强特效，必须评估是否拆分。
- 如果用户的输入缺少关键信息，优先基于文本合理推断；只有缺口会改变剧情、人物关系或生成格式时才询问。

## FrameVideo 交接

当用户目标是“生成一个视频”而不是“只要分镜/提示词”时，本 skill 不在 Final Prompt 停止。继续执行：

1. 生成 Chanjing AIGC Plan。
2. 使用 `../chanjing-digital-human/references/ai-creation.md` 的幂等规则提交和同步蝉镜 AI Creation 任务。
3. 只使用下载到本地的 `assets/ai-creation/images/` 或 `assets/ai-creation/videos/` 资产。
4. 回到 `framevideo` skill 编写 composition、字幕、转场、音乐和最终校验。

## 全局自检

最终交付前按层级简短检查。分镜层的详细自检见 `storyboard-script-generation.md` 末尾。

**Clip 层**
1. 每场戏是否有开场落点和收束落点。
2. 关键对话是否满足基础 2 镜制，高能对话是否满足强化 3 镜制。
3. 动态动作是否拆出起势、执行、结果，没有一镜带过。

**Shot 层**
4. Clip 是否过碎（应合并），或 Shot 是否过长过复杂（应拆分）。
5. 视觉连续性是否稳定：人物、道具、光线方向、轴线、空间状态在同一 Shot 内无原因跳变。

**Final Prompt 层**
6. 是否完整保留原剧情、原台词和资产标签，没有新增无依据情节。
7. 最终提示词是否明确禁止字幕，输出层级是否符合用户要求。
