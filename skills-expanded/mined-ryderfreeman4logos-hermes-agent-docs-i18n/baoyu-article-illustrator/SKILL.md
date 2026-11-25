---
name: baoyu-article-illustrator
description: "Article illustrations: type × style × palette consistency."
version: 1.57.0
author: 宝玉 (JimLiu)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [article-illustration, creative, image-generation]
    category: creative
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-article-illustrator
---

# 文章插画生成工具

基于 [baoyu-article-illustrator](https://github.com/JimLiu/baoyu-skills) 为 Hermes Agent 的工具生态体系定制开发。

该工具可分析文章内容，定位需要插图的位置，并按照**类型 × 风格 × 色彩方案**的一致性要求生成图像。

## 适用场景

当用户请求为文章添加插图、为内容生成图片，或使用“为文章配图”、“生成文章插画”或“添加图片”等表述时，即可触发此技能。用户需提供文章内容（文件路径或粘贴的文本），并可可选地指定类型、风格、色彩方案或图像密度。

## 三个设计维度

| 维度 | 控制参数 | 示例 |
|------|----------|------|
| **类型** | 信息结构类型 | 信息图、场景图、流程图、对比图、框架图、时间轴图 |
| **风格** | 渲染风格 | 极简风、温暖风、简约风、蓝图风、水彩风、优雅风 |
| **色彩方案** | 颜色主题（可选） | 棒棒糖色系、温暖色系、霓虹色系——可覆盖风格默认颜色 |

用户可自由组合参数，例如：`type=infographic, style=vector-illustration, palette=macaron`。

也可直接使用预设方案：`edu-visual` 一键设置类型、风格与色彩方案。更多详情请参阅 [style-presets.md](references/style-presets.md)。

## 支持的类型

| 类型 | 最佳适用场景 |
|------|--------------|
| `infographic` | 数据展示、指标分析、技术内容 |
| `scene` | 叙事类内容、情感表达 |
| `flowchart` | 流程展示、工作流程说明 |
| `comparison` | 并列对比、选项展示 |
| `framework` | 模型展示、架构设计 |
| `timeline` | 历史事件、发展历程 |

## 风格选项

关于核心风格、完整风格库以及类型与风格的兼容性信息，请参阅 [references/styles.md](references/styles.md)。

## 输出结构

```
{output-dir}/
├── source-{slug}.{ext}    # Only for pasted content
├── outline.md
├── prompts/
│   └── NN-{type}-{slug}.md
└── NN-{type}-{slug}.png
```

**默认输出目录**：

| 输入内容 | 输出目录 | Markdown 插入路径 |
|---------|----------|------------------|
| 文章文件路径 | `{article-dir}/imgs/` | `imgs/NN-{type}-{slug}.png` |
| 粘贴的内容 | `illustrations/{topic-slug}/`（当前工作目录） | `illustrations/{topic-slug}/NN-{type}-{slug}.png` |

如果用户要求不同的布局（例如将图片置于文章旁，或使用 `illustrations/` 子目录），则应予以满足。

**Slug 规则**：由 2-4 个单词组成，采用连字符分隔的小写格式。**冲突处理**：若存在同名文件，则在名称后追加 `-YYYYMMDD-HHMMSS`。

## 核心原则

- **呈现概念而非隐喻** —— 若文章使用了隐喻（例如“电锯切西瓜”），应绘制其背后的概念，而非字面意义上的图像。
- **标签使用文章中的真实数据** —— 应使用文章中的实际数字、术语和引文，而非通用占位符。
- **提示词文件是可复现性记录** —— 在生成任何图像之前，每幅插图都必须在 `prompts/` 目录下保存对应的提示词文件。
- **清除敏感信息** —— 在将任何内容写入磁盘之前，需先扫描源文件，移除其中的 API 密钥、令牌或凭证。

## 工作流程

```
- [ ] Step 1: Detect reference images (if provided)
- [ ] Step 2: Analyze content
- [ ] Step 3: Confirm settings (clarify tool, one question at a time)
- [ ] Step 4: Generate outline
- [ ] Step 5: Generate prompts
- [ ] Step 6: Generate images (image_generate)
- [ ] Step 7: Finalize
```

### 第1步：检测参考图片

如果用户提供了参考图片（直接粘贴的路径、附件或URL）：

1. 对每张参考图片，使用该路径/URL以及相关问题调用`vision_analyze`函数，问题需涵盖风格、色彩方案、构图和主题等方面。随后通过`write_file`函数将返回的描述内容保存到`{output-dir}/references/NN-ref-{slug}.md`文件中。
2. **切勿**尝试使用`write_file`或`read_file`函数来复制二进制文件——这些函数仅支持处理文本数据。如果需要为记录目的保留本地副本，可使用`terminal`命令（如`cp "$src" "{output-dir}/references/NN-ref-{slug}.{ext}"`）。该分析技能本身无需读取二进制文件，仅需依据视觉描述即可完成工作。
3. 由于`image_generate`函数不支持直接接收图片输入，因此在第5步生成提示词时，将使用上述视觉描述内容。

完整流程请参见：[references/workflow.md](references/workflow.md#step-1-detect-reference-images)。

### 第2步：进行分析

| 分析维度 | 输出内容 |
|----------|----------|
| 内容类型 | 技术类 / 教程类 / 方法论类 / 叙事类 |
| 目的 | 信息传递 / 可视化展示 / 想象拓展 |
| 核心论点 | 2-5个主要观点 |
| 插图应用位置 | 需要插图来增强价值的内容部分 |

首先读取源文件内容（可通过文件路径使用`read_file`函数读取，或直接粘贴文本），然后通过`write_file`函数将分析结果保存到`{output-dir}/analysis.md`文件中。

完整流程请参见：[references/workflow.md](references/workflow.md#step-2-analyze)。

### 第3步：确认设置参数

使用`clarify`工具来收集信息。由于该工具每次仅能处理一个问题，因此应优先询问最关键的问题。对于那些用户请求中已明确给出的答案，可直接跳过。

| 顺序 | 问题 | 选项 |
|------|------|------|
| Q1 | **预设模板或类型** | [推荐预设]、[其他预设]，或手动选择：信息图、场景图、流程图、对比图、框架图、时间轴图、混合类型 |
| Q2 | **内容密度** | 低密度（1-2个元素）、均衡密度（3-5个元素）、按章节划分（推荐）、高密度（6个以上元素） |
| Q3 | **风格** *（若Q1已选择预设模板，则可跳过此题）* | [推荐风格]、极简扁平风、科幻风、手绘风、编辑风、场景风、海报风 |
| Q4 | **色彩方案** *（可选）* | 默认风格配色、马卡龙色系、暖色调、霓虹色调 |
| Q5 | **语言** *（仅当文章语言不明确时使用）* | 文章原文语言 / 用户指定语言 |

请避免连续提出2-3个以上的`clarify`问题。如果用户已在请求中明确说明了相关参数，可直接跳过相应步骤。

完整流程请参见：[references/workflow.md](references/workflow.md#step-3-confirm-settings)。

### 第4步：生成大纲 → 生成`outline.md`文件

使用`write_file`函数保存`{output-dir}/outline.md`文件，文件中需包含前端元数据（类型、密度、风格、色彩方案、图片数量），同时为每幅插图对应添加一个条目：

```yaml
## Illustration 1
**Position**: [section/paragraph]
**Purpose**: [why]
**Visual Content**: [what to show]
**Filename**: 01-infographic-concept-name.png
```

完整模板：[references/workflow.md](references/workflow.md#step-4-generate-outline)。

### 第5步：生成提示词

**强制要求**：在生成任何图像之前，每幅插图都必须先有对应的提示词文件——该提示词文件即用于确保结果可复现的记录。

针对每幅插图需执行以下操作：

1. 按照[references/prompt-construction.md](references/prompt-construction.md)中的说明创建提示词文件。
2. 使用`write_file`函数并添加YAML格式的前置信息，将文件保存至`{output-dir}/prompts/NN-{type}-{slug}.md`路径下。
3. 提示词必须使用带有结构化板块（区域/标签/颜色/风格/宽高比）的类型专用模板。
4. 标签中必须包含文章相关的具体数据：实际数值、术语、指标及引文内容。
5. 需根据提示词前置信息中的说明处理引用内容（直接引用/样式引用/调色板引用）——对于直接引用，需在提示词中嵌入对该引用的文字描述（因为`image_generate`函数不支持直接传入参考图像）。

### 第6步：生成图像

针对每个提示词文件需执行以下操作：

1. 调用`image_generate(prompt=..., aspect_ratio=...)`函数。该函数会返回一个包含图像URL的JSON格式结果；它不会将图像写入磁盘，也不接受输出路径参数。
2. 将提示词中的宽高比映射到`image_generate`函数所支持的枚举值：`16:9`对应`landscape`（横向），`9:16`对应`portrait`（纵向），`1:1`对应`square`（正方形）；对于非标准宽高比，则自动匹配最接近的预设值。
3. 通过`terminal`工具下载返回的图像URL，保存至`{output-dir}/NN-{type}-{slug}.png`路径下（例如可使用命令`curl -sSL -o "{output-dir}/NN-{type}-{slug}.png" "{url}"`）。
4. 若生成失败，系统会自动重试一次。

注意：底层的图像生成后端由用户自行配置（默认为FAL FLUX 2 Klein 9B），且无法通过`image_generate`函数进行选择。请勿在提示词中写入模型名称期望其能指定特定后端。

### 第7步：完成整理

在对应段落之后插入`![描述文本]({relative-path}/NN-{type}-{slug}.png)`格式的图片链接。图片的替代文本应为用文章语言书写的简短描述。

报告：

```
Article Illustration Complete!
Article: [path] | Type: [type] | Density: [level] | Style: [style] | Palette: [palette or default]
Images: X/N generated
```

## 修改操作

| 操作 | 步骤 |
|------|-------|
| 编辑 | 更新提示词 → 重新生成 → 更新参考信息 |
| 添加 | 定位 → 输入提示词 → 生成 → 更新大纲 → 插入内容 |
| 删除 | 删除文件 → 移除参考信息 → 更新大纲 |

## 参考资料

| 文件路径 | 内容说明 |
|----------|----------|
| [references/workflow.md](references/workflow.md) | 详细操作流程 |
| [references/usage.md](references/usage.md) | 调用示例 |
| [references/styles.md](references/styles.md) | 样式库与调色板集 |
| [references/style-presets.md](references/style-presets.md) | 预设快捷键（类型+风格+调色板） |
| [references/prompt-construction.md](references/prompt-construction.md) | 提示词模板 |

## 常见误区

1. **数据完整性至关重要** —— 绝不可对原始统计数据进行总结、改写或修改。“73%增长”应保持为“73%增长”不变。
2. **清除敏感信息** —— 在将内容放入任何输出文件之前，务必先扫描其中是否存在API密钥、令牌或凭证等敏感数据。
3. **避免字面化理解隐喻** —— 应通过可视化方式呈现其背后的概念。
4. **提示词文件是必需的** —— 未保存提示词文件则无法生成图像。该文件可用于后续重新生成内容或切换后端模型。
5. **`image_generate`的分辨率选项** —— 该工具支持`landscape`（横屏）、`portrait`（竖屏）和`square`（正方形）三种格式。自定义比例会自动映射为最接近的选项。
6. **`image_generate`返回的是URL链接，而非本地文件** —— 在将本地图像路径插入文章之前，务必先通过终端命令（如`curl`）下载该图像。
7. **无法由智能体选择后端模型** —— `image_generate`会使用用户配置的模型（默认为FAL FLUX 2 Klein 9B）。切勿在提示词中写入“使用<模型名>来生成内容”这类语句，期望其自动切换模型。
