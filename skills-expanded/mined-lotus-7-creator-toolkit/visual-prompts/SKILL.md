---
name: visual-prompts
description: AI生图提示词生成技能。为分镜脚本中的每个画面生成适用于Midjourney/Stable Diffusion等AI生图工具的提示词。包含风格、构图、光影、细节描述。触发场景：用户说"生成画面提示词"、"AI生图提示词"、"为脚本配图"等。
---

# Visual Prompts (画面提示词生成)

## Overview

为分镜脚本的每个镜头生成AI生图提示词，包含完整的画面描述、风格、构图、光影信息。

## 输入处理

### 必需输入
- **分镜脚本**: 包含镜号、景别、画面描述的分镜表
- **风格偏好**: funny / touching / suspense / educational / real
- **内容类型**: short-video / medium-video / story / knowledge / vlog

### 提示词要素

每个提示词需包含：
1. **主体描述**: 谁在做什么
2. **环境/背景**: 在哪里
3. **构图方式**: 如何构图
4. **光影效果**: 什么光线
5. **风格修饰**: 什么风格
6. **质量标签**: 高质量标签

## 输出格式

```
=== AI生图提示词 ===

【基本信息】
镜头数：[数量]
风格：[风格]
推荐模型：[MJ/SD推荐]

【提示词表】

| 镜号 | 景别 | 正向提示词 | 负向提示词 | 参数建议 |
|------|------|------------|------------|----------|
| 1 | MS | [prompt] | [negative] | [ar 16:9] |
| 2 | CU | [prompt] | [negative] | [ar 16:9] |
...

【风格一致性建议】
- 统一风格词：[保持风格一致的关键词]
- 色调建议：[色调方案]
- 人物一致：[如何保持人物一致]

【模型推荐】
- Midjourney: [推荐参数]
- Stable Diffusion: [推荐模型/参数]
- DALL-E: [补充说明]
```

## 提示词结构

### 正向提示词结构

```
[主体描述], [动作/表情], [环境/背景], [构图方式], [光影效果], [风格修饰], [质量标签]
```

**示例分解**
```
主体: a young office worker
动作: looking exhausted, climbing stairs
环境: modern office building staircase
构图: medium shot, eye level
光影: dim fluorescent lighting, shadows
风格: cinematic, realistic
质量: highly detailed, 8k, professional photography

完整提示词:
A young office worker looking exhausted while climbing stairs in a modern office building, medium shot, eye level, dim fluorescent lighting creating shadows, cinematic, realistic, highly detailed, 8k, professional photography
```

### 负向提示词（通用）

```
blurry, low quality, distorted, deformed, ugly, bad anatomy, extra limbs, extra fingers, missing fingers, text, watermark, signature, cartoon, illustration (unless specified)
```

## 按风格生成提示词

### funny (搞笑)

**风格词**: `exaggerated expression, comedy style, vibrant colors, cartoonish realism`

**光影**: `bright lighting, high contrast, colorful`

**构图**: `dynamic angle, close-up on expression`

**示例**
```
正向: exhausted office worker with exaggerated sweaty face climbing stairs, dramatic suffering expression, comedy style, bright office lighting, medium shot, highly detailed, funny caricature style
负向: serious, dark mood, horror
```

### touching (感人)

**风格词**: `warm atmosphere, soft focus, emotional, cinematic lighting, golden hour`

**光影**: `soft warm light, gentle shadows, natural lighting`

**构图**: `intimate framing, eye-level, shallow depth of field`

**示例**
```
正向: father and child silhouette watching sunset together, warm golden light, soft focus background, emotional moment, cinematic, shallow depth of field, highly detailed, 8k
负向: harsh lighting, cold colors, staged
```

### suspense (悬念)

**风格词**: `dark atmosphere, dramatic shadows, film noir style, mysterious`

**光影**: `low key lighting, harsh shadows, rim lighting`

**构图**: `dutch angle, extreme angles, deep perspective`

**示例**
```
正向: mysterious figure standing in dark hallway, dramatic backlighting, harsh shadows, film noir style, dutch angle, mysterious atmosphere, cinematic, highly detailed
负向: bright lighting, cheerful colors, flat lighting
```

### educational (干货)

**风格词**: `clean background, professional, bright lighting, modern minimal`

**光影**: `soft even lighting, white background, studio lighting`

**构图**: `centered composition, clean layout, product photography style`

**示例**
```
正向: person explaining concept with hands, clean white background, soft studio lighting, centered composition, professional headshot style, modern, crisp, highly detailed
负向: cluttered background, dramatic shadows, dark
```

### real (真实)

**风格词**: `documentary style, natural lighting, candid moment, authentic`

**光影**: `natural light, available light, mixed lighting`

**构图**: `handheld camera feel, natural framing, spontaneous composition`

**示例**
```
正向: candid moment of person working at desk, natural window light, messy desk in background, documentary photography style, authentic, spontaneous, shallow depth of field, highly detailed
负向: staged, studio lighting, overly perfect
```

## 按景别生成提示词

### ECU (特大特写)
```
关键词: extreme close-up, macro shot, detail focused

示例: extreme close-up of eye reflecting determination, macro photography, sharp focus on iris, dramatic lighting
```

### CU (特写)
```
关键词: close-up shot, portrait, face focused

示例: close-up of woman's face showing surprise, expressive eyes, soft background blur, professional portrait lighting
```

### MCU (近景)
```
关键词: medium close-up, chest up, conversational

示例: medium close-up of man talking to camera, casual expression, natural lighting, office background
```

### MS (中景)
```
关键词: medium shot, waist up, body language

示例: medium shot of person gesturing while explaining, upper body visible, casual stance, natural lighting
```

### FS (全景)
```
关键词: full body shot, entire figure, wide framing

示例: full body shot of person standing confidently, casual clothing, office environment, natural lighting
```

### LS (远景)
```
关键词: wide shot, establishing shot, environment focused

示例: wide establishing shot of modern office building exterior, city context, golden hour lighting, cinematic
```

## Midjourney 参数建议

### 基础参数

| 参数 | 说明 | 常用值 |
|------|------|--------|
| `--ar` | 宽高比 | `16:9` (横屏) / `9:16` (竖屏) |
| `--v` | 版本 | `6` (最新) |
| `--stylize` | 风格化 | `100-500` (数值越高越艺术) |
| `--quality` | 质量 | `1` 或 `2` |
| `--chaos` | 随机性 | `0-100` |

### 按风格设置

| 风格 | `--stylize` | `--chaos` | 补充参数 |
|------|-------------|-----------|----------|
| funny | 300-500 | 20-50 | `--jitter` |
| touching | 100-250 | 0-20 | 无 |
| suspense | 200-400 | 10-30 | `--weird` |
| educational | 50-150 | 0-10 | 无 |
| real | 100-200 | 10-30 | 无 |

### 宽高比建议

| 用途 | 参数 |
|------|------|
| 横屏视频 | `--ar 16:9` |
| 竖屏短视频 | `--ar 9:16` |
| 方形 | `--ar 1:1` |

## Stable Diffusion 参数建议

### 推荐模型

| 风格 | 推荐模型 |
|------|----------|
| 真实摄影 | Realistic Vision, Photorealistic |
| 搞笑夸张 | DreamShaper, Counterfeit |
| 电影感 | Rev Animated, Mo-Di Diffusion |
| 插画风格 | Anything, AbyssOrangeMix |

### 采样参数

```
Sampling method: DPM++ 2M Karras
Steps: 20-30
CFG Scale: 7-12
Size: 512x768 (竖屏) / 768x512 (横屏) 或更高
```

### 负向提示词模板

```
(worst quality, low quality:1.4), (zombie, sketch, interlocked fingers, comic), bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, ugly, disgusting, poorly drawn hands, missing limb, floating limbs, disconnected limbs, malformed hands, blurry, out of focus, long neck, long body, mutated hands and fingers, out of frame, extra limbs, extra digits, people in background
```

## 人物一致性技巧

### 方法1: 固定种子
```
Midjourney: 在 prompt 后加 --seed 1234 (相同种子+相似prompt可保持一致)
Stable Diffusion: 使用固定 seed 值
```

### 方法2: 人物描述词保持一致
```
为同一人物始终使用相同描述:
"a young Asian woman with short black hair, wearing glasses, casual office attire"
```

### 方法3: 使用参考图（高级）
```
Midjourney: 使用 --cref [url] 参数
Stable Diffusion: 使用 img2img 或 ControlNet
```

## Examples

**Example 1: 搞笑短视频镜头**

| 镜号 | 画面描述 | 正向提示词 | 负向提示词 | 参数 |
|------|----------|------------|------------|------|
| 1 | 主角疲惫爬楼梯 | exhausted office worker climbing stairs, exaggerated sweaty face, suffering expression, comedy style, bright office lighting, medium shot, highly detailed, funny | serious, dark mood | --ar 16:9 --v 6 --stylize 400 |
| 2 | 特写崩溃表情 | extreme close-up of man's desperate sweaty face, exaggerated suffering expression, dramatic comedy, bright lighting, macro photography | serious, normal expression | --ar 16:9 --v 6 --stylize 500 |

**Example 2: 感人剧情镜头**

| 镜号 | 画面描述 | 正向提示词 | 负向提示词 | 参数 |
|------|----------|------------|------------|------|
| 1 | 父子看日落 | father and child silhouette watching sunset together, holding hands, warm golden light, soft focus background, emotional moment, cinematic, shallow depth of field | harsh lighting, cold colors | --ar 16:9 --v 6 --stylize 200 |
| 2 | 侧脸温情 | profile shot of father's gentle smile looking at child, warm sunset lighting, soft shadows, emotional, cinematic, highly detailed | sad, serious expression | --ar 16:9 --v 6 --stylize 150 |

## 质量标准

- **描述完整**: 主体+动作+环境+构图+光影+风格
- **风格一致**: 同一视频使用统一风格词
- **参数合理**: 宽高比、版本、stylize 适配用途
- **可用性**: 可直接复制到 MJ/SD 使用
- **中文对照**: 提供中文说明，方便用户理解

## Resources

### references/
无额外参考文件，所有提示词框架已包含在本文件中。
