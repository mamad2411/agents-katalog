---
name: darin-broll-skill
description: Darin 的外部工具 editorial paper-collage B-roll 提示词工作流。把约 5 秒口播、观点句、小红书/抖音选题或抽象概念压成一个清晰视觉隐喻，再依次输出视觉方向、首帧与尾帧英文提示词、视频生成英文提示词。用户提到“拼贴 B-roll”“纸拼贴视频”“半调拼贴动画”“给这句口播配画面”“首尾帧提示词”或要求把文稿做成编辑拼贴动画时使用。强制执行两次确认：视觉方向确认后才给静帧提示词，静帧提示词确认后才给视频提示词。默认只写提示词，不调用图像或视频生成工具。
---

# Darin Broll

把一句口播压成一个 sharp visual idea，再把它设计成从空色场逐件组装的高级编辑纸拼贴动画。默认交付外部生成工具可直接使用的提示词，不在本 Skill 内生成媒体。

## 工作协议

严格按以下顺序工作，不合并闸门：

1. Gate 1：只给视觉方向，停下等待确认。
2. Gate 2：方向确认后，只给首帧和尾帧英文提示词，停下等待确认。
3. Gate 3：静帧提示词确认后，给视频生成英文提示词。

遵守以下规则：

- 用中文沟通；所有生成提示词用英文。
- 默认不调用内置或外部图像、视频生成工具，不要求用户提供本地文件路径。
- 用户说“确认”“同意”“OK”“可以”“继续”时，只确认当前 Gate。
- 用户修改方向或提示词时，修改当前 Gate 并再次等待确认，不提前进入下一 Gate。
- Gate 2 的确认足以进入 Gate 3，不要额外等待“图片好了”。用户说“图片好了”也视为 Gate 2 已确认。
- 即使用户一开始直接索要完整提示词，也先完成 Gate 1；只有用户明确要求跳过审批时才一次性输出。
- 不模仿具体品牌或活跃艺术家的可识别签名。把“Vox 风格”等请求转译为可描述的编辑拼贴机制：半调网点、平坦色场、卡纸、奶油白 keyline 和逐件组装。

## 视觉语法

每条画面只表达一个清晰命题，并满足：

- 使用 2–4 个大型、可分离的纸片组；不要堆满零碎小物件。
- 把主体控制在画面中部约 70% 范围，保留充足纯色负空间。
- 使用强烈、平坦、均匀的纸张色场，不用渐变、暗角或写实环境。
- 以黑白 halftone photographic cut-outs 为骨架，只用少量彩色卡纸建立信息层级。
- 所有纸片具有清晰裁切边、细奶油白 keyline、低透明度柔和纸影和细微非涂布纸纹。
- 默认 9:16、约 5 秒、锁定镜头、无声、从空场逐件组装。
- 禁止字幕、口播全文、可读文字、数字、logo、水印、真实平台 UI、假通知和无关装饰。

### 色彩语义

按内容选择背景，不要固定使用单一颜色：

| 背景 | 适用语义 | 建议色值 |
|---|---|---|
| 焦橙 / 红 | 时间消耗、劳动、失败、紧迫 | `#D95D39` / `#C9433F` |
| 芥末黄 | 工具、警示、经验、踩坑 | `#D3A72C` |
| 深青 / 墨绿 | 判断、认知、协作、恢复掌控 | `#174F52` / `#274C3B` |
| 深紫 | 规范、沉淀、长期记忆 | `#493A68` |

点色优先使用暖奶油白 `#F1E6CF`、芥末黄、焦橙和少量浅青。同一批内容保持纸张、半调和 keyline 一致，但可随叙事更换背景色。

## Gate 1：视觉方向

先提取：

- 核心意思：观众最终要看懂什么。
- 情绪：例如疲惫、紧迫、反讽、笃定、释然或重新振作。
- 动作动词：例如跌倒、爬起、堆叠、阻断、连接、穿过、打开或归档。
- 视觉关系：什么主体通过什么动作表达核心意思。

优先使用可见动作，不要只摆放象征物。人物、设备和界面都必须服务于同一个动作关系。

创作者和数码题材可使用：人物、电脑、手机、相机、耳机、键盘、抽象视频缩略图、播放窗口、发布按钮轮廓、失败导出卡片、草稿纸堆和规则门槛。平台主页必须画成抽象频道网格或无字缩略图墙，不出现真实 logo、平台名称、可读标题、粉丝数字或完整 UI 截图。

### 稳定性规则

- 物件超过 4 组时，先合并同类物件。
- 避免缠绕、穿插、复杂遮挡和多层透视；这些关系容易让视频模型重排尾帧。
- 需要严格落位时使用平铺、并列、堆叠、滑入和卡位关系。
- 抽象数量概念必须明确限定组数，例如：`The image contains ONLY these three groups and absolutely nothing else.`
- 人物动作需要清楚的起止状态，例如“跌倒在底部”到“重新站回中央”，不能只写“人物恢复信心”。

### Gate 1 输出格式

只输出：

```text
核心意思：...
情绪：...
一句话视觉命题：...
关键物件：...（不超过 4 组）
建议底色与点色：...
预期组装顺序：...

确认这个视觉方向吗？确认后我会发送首帧和尾帧的英文提示词。
```

输出后停下。不要在同一条回复中附带静帧或视频提示词。

## Gate 2：首帧与尾帧提示词

方向确认后，写两段完整、自包含、可直接粘贴的英文提示词。必须把颜色、物件、位置、关系和组数全部实例化，不能保留 `[color]`、`[group 1]` 等占位符。

### First Frame Prompt

首帧必须是与尾帧相同背景色和纸张质感的纯空场。按以下结构写成一段完整 prompt：

```text
Use case: ads-marketing
Asset type: empty first frame for a vertical 9:16 image-to-video B-roll clip
Primary request: Create a perfectly empty [具体颜色与色值] paper field that will serve as the opening frame of an editorial paper-collage stop-motion animation.
Scene/backdrop: A flat, uniform [具体颜色与色值] uncoated paper surface with subtle fine paper fiber.
Composition/framing: Locked vertical 9:16 poster frame filled edge to edge by the same solid paper color. No foreground elements.
Lighting/material: Even soft studio light, tactile matte 2D paper, no vignette and no gradient.
Avoid: No objects, no people, no devices, no cut-outs, no icons, no typography, no readable letters, no numerals, no logos, no watermark, no UI, no border, no frame, no pattern, no folds, no stains, no shadows, no gradient.
```

### Last Frame Prompt

尾帧必须是已经完成的最终构图，而不是动作过程截图。按以下结构写成一段完整 prompt：

```text
Use case: ads-marketing
Asset type: final still frame for a vertical 9:16 image-to-video B-roll clip
Primary request: Create a finished editorial paper-collage image expressing [已经确认的一句话视觉命题].
Scene/backdrop: A perfectly flat [具体颜色与色值] paper field with subtle uncoated paper fiber.
Style/medium: Premium editorial stop-motion paper collage; black-and-white halftone photographic cut-outs mixed with selective [具体点色] cardstock accents.
Composition/framing: Locked vertical 9:16 poster frame; [明确主体位置、朝向和尺度]; keep all subjects within the middle 70 percent; preserve generous clean color-field negative space; use exactly [2–4] large separable paper groups.
Elements and relationships: [逐组写清物件、动作、位置、前后关系和视觉作用].
Materials/textures: Visible printed halftone dots, crisp machine-cut edges, thin warm-cream paper keylines, soft low-opacity physical paper shadows.
Critical constraints: [写明画面必须一眼成立的核心关系，并限定只能出现哪些组].
Avoid: No typography, no readable letters, no Chinese characters, no English words, no numerals, no logos, no watermark, no real UI screenshot, no subtitles, no fake notifications, no glossy 3D, no photoreal environment, no gradient, no clutter, no extra objects.
```

写提示词时执行以下硬性规则：

- 便签、卡片、书页、屏幕或频道页面只能带抽象波浪涂鸦线，必须加入：`carrying only abstract wavy squiggle doodle lines -- absolutely no letters or words`。
- 屏幕界面使用抽象网格、缩略图块、播放三角形和无字控制条，不复刻真实产品 UI。
- 人物使用黑白半调照片剪贴；数码设备和强调物可用彩色卡纸，但点色不要超过 3 种。
- 用户指定的动作、人物数量和设备必须准确保留，不能为了“丰富画面”添加奖杯、时钟、箭头、爱心、货币符号或无关手掌。
- 批量任务先统一材质和点色逻辑，再为每条选择符合语义的不同背景。

### Gate 2 输出格式

只输出：

```text
First Frame Prompt
[完整英文提示词]

Last Frame Prompt
[完整英文提示词]

确认这两张静帧提示词吗？确认后我会发送视频生成提示词。
```

输出后停下。静帧提示词的确认就是进入 Gate 3 的条件，不再询问图片是否已经生成。

## Gate 3：视频生成提示词

默认假设外部工具支持首尾帧输入：Image 1 是纯色首帧，Image 2 是确认过的完成尾帧。输出一段完整英文提示词，必须把组装顺序、颜色和物件全部实例化。

使用以下结构：

```text
Create a 5-second vertical 9:16 paper-collage stop-motion assembly animation, using Image 1 as the exact empty first frame and Image 2 as the exact completed last frame. Use one continuous locked-off shot.

Open by holding the empty flat [具体颜色与色值] paper field briefly. Assemble the scene piece by piece with crisp physical stop-motion timing: [第一组从何处以何种方式进入]; then [第二组动作]; then [第三组动作]; finally [第四组动作或人物完成动作]. Every element must land in the exact position shown in Image 2. Hold the supplied final composition clearly at the end.

Preserve the exact 9:16 framing, flat [具体颜色与色值] background, [具体点色] cardstock accents, uncoated paper grain, black-and-white halftone dots, warm-cream keylines, crisp cut edges and soft paper shadows. Restrained tactile 2D paper craft only.

No scene cuts, no camera movement, no pan, no tilt, no zoom, no parallax, no morphing, no liquid motion, no object redesign, no new objects, no text, no letters, no numbers, no logos, no watermark, no real UI, no subtitles, no sound.
```

动作采用“基础结构 → 主体 → 辅助物件 → 关键动作或结果”的顺序。不要让所有物件同时淡入；每组必须有可辨认的 `slide in`、`drop in`、`snap into place`、`pop open`、`fall` 或 `rise` 动作。

如果用户明确说明工具只支持一张图，改用尾帧单图模式：要求视频从相同纯色空场开始，并在结尾精确匹配所提供图片。除此之外保持相同动作与禁止项。

Gate 3 输出后结束，不追加新的确认问题。

## 批量任务

- Gate 1 按编号输出所有视觉方向，允许用户只确认部分编号。
- 只有已确认条目进入 Gate 2；未确认条目继续修改。
- Gate 2 同样支持部分确认，只有已确认静帧提示词进入 Gate 3。
- 优先形成叙事弧，例如：手工消耗 → 失败积累 → 经验沉淀 → 恢复掌控。
- 同批保持半调颗粒、纸张、keyline 和阴影一致，背景颜色随情绪推进变化。

## 输出前检查

每个 Gate 输出前静默检查：

- 是否只表达一个视觉命题。
- 是否不超过 4 个大型可分离组。
- 是否有明确动作和最终状态。
- 是否保留足够纯色负空间。
- 是否完全禁止可读文字、数字、logo、水印和真实 UI。
- 首尾帧是否使用相同背景颜色、色值、纹理、比例和光线。
- 视频动作是否逐组发生并精确结束在尾帧，而不是整体淡入或慢 zoom。
- 当前回复是否只包含当前 Gate 允许的内容和规定的确认句。

## 常见修正

- 隐喻不清：删除装饰物，改成一个主体、一个阻力和一个结果。
- 构图漂移：减少组数，取消缠绕穿插，改用并列、平铺或卡位。
- 组装感弱：为每组指定不同进入方向和 `snap into place` 时点。
- 出现假字：回到尾帧提示词，强化无字涂鸦线和禁止文字；不要指望视频提示词修复。
- 首尾帧底色跳变：以实际尾帧空白区域采样色值，再用该色值重做纯色首帧。
- 尾帧被改造：强化 `Image 2 as the exact completed last frame` 和 `no object redesign`，必要时进一步简化空间关系。
- 质感变成写实或 3D：强化 `Restrained tactile 2D paper craft only`、平坦色场和机器裁切纸边。

## 来源与许可

本 Skill 基于 [gbro-collage-broll](https://github.com/pyang5166/gbro-collage-broll) 和其 Ray Broll 工作流改编，保留其编辑纸拼贴视觉体系，并将本地媒体生成流程改为外部工具提示词与两次人工确认流程。上游项目采用 MIT License，原始版权归 `Copyright (c) 2026 狗哥笔记` 所有。

发布、复制或再分发本 Skill 时必须同时保留同目录下的 `LICENSE` 文件及其中的版权与许可声明。
