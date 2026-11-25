---
name: baoyu-comic
description: "Knowledge comics (知识漫画): educational, biography, tutorial."
version: 1.56.1
author: 宝玉 (JimLiu)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [comic, knowledge-comic, creative, image-generation]
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-comic
---

# 知识漫画创作工具

该功能基于 [baoyu-comic](https://github.com/JimLiu/baoyu-skills) 开发，专为 Hermes Agent 的工具生态设计。

支持通过灵活的美术风格与色调组合，创作原创知识漫画。

## 适用场景

当用户要求创建知识/教育类漫画、传记漫画或教程漫画，或提及“知识漫画”、“教育漫画”或“Logicomix风格”等术语时，可触发此技能。用户需提供内容（文本、文件路径、URL或主题），并可选择性指定美术风格、色调、布局、宽高比或语言。

## 参考图片处理

Hermes 的 `image_generate` 工具仅支持**文本提示词**——它接收文本提示词和宽高比，然后返回图像URL，**不支持**接收参考图片。当用户提供参考图片时，需先从中**提取文字描述的特征**，并将其嵌入到每一页的提示词中：

**输入处理**：若用户提供文件路径（或在对话中粘贴图片），则将其复制到 `refs/NN-ref-{slug}.{ext}` 文件中，与漫画输出结果一同保存以追溯来源。
- 提供了文件路径的图片 → 复制至对应路径文件；未提供路径的粘贴图片 → 通过 `clarify` 功能询问用户路径，或口头描述风格特征作为文本替代方案；
- 无参考图片 → 跳过此步骤。

**根据参考图片的不同，有以下三种使用模式**：

| 使用模式 | 效果 |
|---------|------|
| `style` | 提取风格特征（线条处理方式、纹理、氛围等），并添加到每一页的提示词中 |
| `palette` | 提取十六进制颜色值，并添加到每一页的提示词中 |
| `scene` | 提取场景构图或主题相关描述，并添加到对应的页面中 |

当存在参考图片时，需将相关信息**记录在每一页提示词的前置信息中**：

```yaml
references:
  - ref_id: 01
    filename: 01-ref-scene.png
    usage: style
    traits: "muted earth tones, soft-edged ink wash, low-contrast backgrounds"
```

角色设定的一致性由 `characters/characters.md` 文件中的**文本描述**（在步骤3中编写）决定，这些描述会被嵌入到每个页面的提示语中（步骤5）。步骤7.1中生成的可选PNG角色表仅用于人工审核，不会作为输入传递给 `image_generate` 工具。

## 选项设置

### 视觉风格参数

| 选项 | 可选值 | 描述 |
|------|--------|-------------|
| 艺术风格 | 简线风格（默认）、漫画风格、写实风格、水墨风格、粉笔风格、极简风格 | 绘画风格/渲染技术 |
| 氛围基调 | 中性（默认）、温暖、戏剧化、浪漫、充满活力、复古、动作感 | 整体情绪/氛围 |
| 分镜布局 | 标准布局（默认）、电影式布局、密集布局、插图式布局、混合布局、网络漫画布局、四格布局 | 分镜排列方式 |
| 页面比例 | 3:4（默认，竖屏）、4:3（横屏）、16:9（宽屏） | 页面长宽比 |
| 输出语言 | 自动检测（默认）、中文、英文、日文等 | 输出语言 |
| 参考图片 | 文件路径 | 用于提取风格特征/配色方案的参考图像（不会传递给图像生成模型）。详情参见上文的[参考图像](#reference-images)部分。 |

### 部分工作流选项

| 选项 | 描述 |
|------|-------------|
| 仅生成分镜 | 仅生成分镜，跳过提示语和图像生成环节 |
| 仅生成提示语 | 生成分镜+提示语，跳过图像生成环节 |
| 仅生成图像 | 根据现有的提示语目录直接生成图像 |
| 重新生成指定页面 | 仅重新生成特定页面（例如输入 `3` 或 `2,5,8`） |

更多详情请参阅：[references/partial-workflows.md](references/partial-workflows.md)

### 艺术风格、氛围基调与预设目录

- **艺术风格**（6种）：`ligne-claire`、`manga`、`realistic`、`ink-brush`、`chalk`、`minimalist`。完整定义见 `references/art-styles/<style>.md` 文件。
- **氛围基调**（7种）：`neutral`、`warm`、`dramatic`、`romantic`、`energetic`、`vintage`、`action`。完整定义见 `references/tones/<tone>.md` 文件。
- **预设方案**（5种）：除基础的艺术风格+氛围基调组合外，还包含特殊规则：

  | 预设名称 | 对应组合 | 特点说明 |
  |--------|-----------|----------|
  | `ohmsha` | 漫画风格 + 中性氛围 | 使用视觉隐喻，不出现对话框，注重道具展示 |
  | `wuxia` | 水墨风格 + 动作感 | 包含气场效果、战斗场景及浓郁的氛围感 |
  | `shoujo` | 漫画风格 + 浪漫氛围 | 突出装饰性元素、眼部细节以及浪漫情节 |
  | `concept-story` | 漫画风格 + 温暖氛围 | 具有视觉符号系统，包含角色成长线，对话与动作比例均衡 |
  | `four-panel` | 极简风格 + 中性氛围 + 四格布局 | 采用起承转合的结构，黑白画面搭配局部彩色，角色为火柴人造型 |

  完整规则见 `references/presets/<preset>.md` 文件——选择预设时会自动加载该文件。
- **兼容性矩阵**以及**内容特征→预设方案**对应表均收录在 [references/auto-selection.md](references/auto-selection.md) 中。在步骤2中推荐组合之前，请先仔细阅读该文档。

## 文件结构

输出目录：`comic/{topic-slug}/`
- Slug：由主题名称提取的2-4个单词组成的下划线连接格式字符串（例如 `alan-turing-bio`）
- 若存在同名文件冲突，需在名称后添加时间戳（例如 `turing-story-20260118-143052`）

**目录内容**：
| 文件名 | 描述 |
|--------|-------------|
| `source-{slug}.md` | 保存的原始内容（下划线连接的Slug与输出目录格式一致） |
| `analysis.md` | 内容分析报告 |
| `storyboard.md` | 包含分镜详细信息的剧情板 |
| `characters/characters.md` | 角色设定说明 |
| `characters/characters.png` | 角色参考表（由 `image_generate` 生成并下载） |
| `prompts/NN-{cover\|page}-[slug].md` | 用于图像生成的提示语文件 |
| `NN-{cover\|page}-[slug].png` | 生成的图像文件（由 `image_generate` 生成并下载） |
| `refs/NN-ref-{slug}.{ext}` | 用户提供的参考图像文件（可选，用于追溯内容来源） |

## 语言处理机制

**语言检测优先级**：
1. 用户明确指定的语言
2. 用户在对话中使用的语言
3. 原始内容的语言

**规则**：所有交互均使用用户输入的语言：
- 分镜大纲与场景描述
- 图像生成提示语
- 用户选择的选项及确认信息
- 进度更新、问题提示、错误信息、总结内容

技术术语仍保持英文形式。

## 工作流程

### 进度检查清单

```
Comic Progress:
- [ ] Step 1: Setup & Analyze
  - [ ] 1.1 Analyze content
  - [ ] 1.2 Check existing directory
- [ ] Step 2: Confirmation - Style & options ⚠️ REQUIRED
- [ ] Step 3: Generate storyboard + characters
- [ ] Step 4: Review outline (conditional)
- [ ] Step 5: Generate prompts
- [ ] Step 6: Review prompts (conditional)
- [ ] Step 7: Generate images
  - [ ] 7.1 Generate character sheet (if needed) → characters/characters.png
  - [ ] 7.2 Generate pages (with character descriptions embedded in prompt)
- [ ] Step 8: Completion report
```

### 流程

```
Input → Analyze → [Check Existing?] → [Confirm: Style + Reviews] → Storyboard → [Review?] → Prompts → [Review?] → Images → Complete
```

### 步骤概要

| 步骤 | 操作 | 关键输出 |
|------|------|----------|
| 1.1 | 分析内容 | `analysis.md`、`source-{slug}.md` |
| 1.2 | 检查现有目录 | 处理冲突 |
| 2 | 确认风格、主题、目标受众及审核要求 | 用户偏好设置 |
| 3 | 生成故事板与角色设定 | `storyboard.md`、`characters/` 目录 |
| 4 | （如用户要求）审核大纲 | 用户确认通过 |
| 5 | 生成提示词 | `prompts/*.md` 文件 |
| 6 | （如用户要求）审核提示词 | 用户确认通过 |
| 7.1 | （如需要）生成角色表 | `characters/characters.png` 文件 |
| 7.2 | 生成页面图像 | `*.png` 文件 |
| 8 | 完成报告 | 工作总结 |

### 用户提问方式

请使用 `clarify` 工具来确认选项。由于该工具一次仅能处理一个问题，因此应先询问最重要的问题，再依次进行后续提问。完整的步骤2问题集详见 [references/workflow.md](references/workflow.md)。

**超时处理（非常重要）**：`clarify` 可能会返回提示“用户在规定时间内未给出回复。请凭您的判断选择默认值并继续操作。”——这**并不等同于**用户同意全部使用默认设置。

- 应将此视为**仅针对该单个问题**的默认处理方式。需继续按顺序询问步骤2中的其余问题；每个问题都是独立的同意节点。
- 在下一条消息中**明确向用户展示所采用的默认值**，以便他们有机会进行更正。例如：“风格已默认为 ohmsha 预设（因 clarify 超时）。如需更改，请告知。”——若未告知用户，默认设置与从未询问过并无区别。
- 一旦出现超时情况，**切勿直接将步骤2简化为“全部使用默认值”这一操作**。如果用户确实不在场，那么他对所有五个问题都会保持沉默——但当他们回来后可以更正那些明确显示的默认值，而无法更正那些未被提及的默认值。

### 第7步：图像生成

所有图像渲染均需使用Hermes内置的 `image_generate` 工具。该工具的架构仅支持 `prompt`（提示词）和 `aspect_ratio`（宽高比，可选 `landscape`、`portrait`、`square`）参数；它**返回的是URL链接**，而非本地文件。因此，每张生成的页面图像或角色表都必须下载到输出目录中。

**提示词文件要求（强制）**：在调用 `image_generate` 之前，必须将每张图像的完整最终提示词写入 `prompts/` 目录下的独立文件中（文件命名规则为 `NN-{type}-[slug].md`）。该提示词文件是确保结果可复现的关键记录。

**宽高比映射规则**：故事板中的 `aspect_ratio` 字段与 `image_generate` 所支持的格式对应关系如下：

| 故事板宽高比 | `image_generate` 格式 |
|--------------|------------------------|
| `3:4`、`9:16`、`2:3` | `portrait`（竖屏） |
| `4:3`、`16:9`、`3:2` | `landscape`（横屏） |
| `1:1` | `square`（正方形） |

**下载步骤**：每次调用 `image_generate` 后需执行以下操作：
1. 从工具返回的结果中获取URL链接。
2. 使用**绝对路径**下载图像数据，例如：<br>`curl -fsSL "<url>" -o /abs/path/to/comic/<slug>/NN-page-<slug>.png`。
3. 在继续处理下一张页面之前，必须确认该路径下确实存在且文件非空。

**切勿依赖Shell当前工作目录的持久性来设置 `-o` 参数的路径**。终端工具的当前工作目录在不同批次之间可能会发生变化（如会话超时、`TERMINAL_LIFETIME_SECONDS` 设置导致路径失效，或 `cd` 操作失败使当前目录出错）。使用 `curl -o relative/path.png` 的方式存在隐蔽风险：如果当前工作目录发生变动，文件将会被写入错误位置，而工具不会报错。**务必为 `-o` 参数提供完整的绝对路径**，或者为终端工具设置 `workdir=<绝对路径>` 参数。2026年4月曾发生过一起事故：某部共10页的漫画中第06至09页被错误地保存在仓库根目录下，而非 `comic/<slug>/` 目录，原因是第3批处理继承了第2批的旧当前工作目录，导致 `curl -o 06-page-skills.png` 将文件写入错误目录。此后该智能体多次声称这些文件存在于本应保存的位置，但实际上并不存在。

**7.1 角色表生成**：当漫画为多页且包含重复出现的角色时，需生成角色表并保存为 `characters/characters.png`，其宽高比为横屏格式。对于简单的预设模板（如四格极简风格）或单页漫画，则无需生成角色表。在调用 `image_generate` 之前，必须先确保 `characters/characters.md` 文件已存在。生成的PNG文件是供人工审核使用的参考资料（便于用户直观查看角色设计），也可作为后续重新生成内容或手动修改提示词的参考——它**不会直接影响**第7.2步的流程。页面的提示词其实已在第5步根据 `characters/characters.md` 中的**文本描述**预先编写完成；`image_generate` 工具不支持以图像作为视觉输入。

**7.2 页面生成**：在调用 `image_generate` 之前，每张页面的提示词必须已存在于 `prompts/NN-{cover|page}-[slug].md` 文件中。由于 `image_generate` 仅支持处理提示词，因此角色一致性是通过**在第5步的每个页面提示词中直接嵌入来自 `characters/characters.md` 的角色描述**来实现的。无论第7.1步是否生成了PNG角色表，这一嵌入操作都会统一执行；PNG文件仅起到审核和重新生成时的辅助作用。

**备份规则**：在重新生成内容之前，需将现有的 `prompts/…md` 和 `…png` 文件重命名为带有 `-backup-YYYYMMDD-HHMMSS` 后缀的版本。

完整的逐步工作流程（包括内容分析、故事板制作、审核环节以及不同生成方案）详见 [references/workflow.md](references/workflow.md)。

## 参考资料

**核心模板**：
- [analysis-framework.md](references/analysis-framework.md) - 深度内容分析框架
- [character-template.md](references/character-template.md) - 角色定义格式规范
- [storyboard-template.md](references/storyboard-template.md) - 故事板结构模板
- [ohmsha-guide.md](references/ohmsha-guide.md) - Ohmsha漫画风格指南

**风格定义**：
- `references/art-styles/` - 绘画风格（线条清晰风、漫画风、写实风、水墨风、粉笔风、极简风）
- `references/tones/` - 风格基调（中性、温暖、戏剧化、浪漫、活力、复古、动作风）
- `references/presets/` - 含有特殊规则的预设模板（ohmsha风格、武侠风格、少女风格、概念故事风、四格风格）
- `references/layouts/` - 页面布局类型（标准布局、电影感布局、密集布局、封面页布局、混合布局、网络漫画布局、四格布局）

**工作流程相关文档**：
- [workflow.md](references/workflow.md) - 完整的工作流程说明
- [auto-selection.md](references/auto-selection.md) - 内容特征自动分析机制
- [partial-workflows.md](references/partial-workflows.md) - 部分流程选项

## 页面修改指南

| 操作类型 | 操作步骤 |
|----------|----------|
| **编辑** | **首先更新提示词文件** → 重新生成图像 → 下载新的PNG文件 |
| **添加新页面** | 在指定位置创建提示词文件 → 生成页面并嵌入角色描述 → 重新编号后续页面 → 更新故事板 |
| **删除页面** | 移除对应文件 → 重新编号后续页面 → 更新故事板 |

**重要提示**：在修改页面内容时，务必**先更新提示词文件**（即 `prompts/NN-{cover|page}-[slug].md` 文件），然后再进行重新生成。这样才能确保所有更改都有记录可查，且结果可复现。

## 常见问题与注意事项

- **图像生成速度**：每张页面的生成时间约为10至30秒；如生成失败，系统会自动尝试重试一次。
- **必须下载本地文件**：务必将 `image_generate` 返回的URL链接下载为本地的PNG文件——后续的处理工具以及用户的审核工作都需要在输出目录中看到实际文件，而非临时的URL链接。
- **使用绝对路径进行下载**：调用 `curl -o` 命令时必须使用绝对路径，切勿依赖终端当前工作目录在不同批次间的持久性。否则可能会出现隐蔽问题：文件会被写入错误目录，而后续在预期路径下执行 `ls` 命令时却找不到任何文件。详情请参阅第7步的“下载步骤”。
- 对于公众人物形象，应使用经过处理的替代图像。
- **必须完成步骤2的确认**——不可跳过此步骤。
- **步骤4和步骤6为可选操作**：仅当用户在步骤2中明确要求时才需执行。
- **步骤7.1的角色表生成**：建议在多页漫画中使用，简单预设模板则可选。该PNG文件仅用于审核和重新生成参考，而页面的提示词（已在第5步根据文本描述编写）并不依赖该PNG文件。`image_generate` 工具不支持以图像作为视觉输入。
- **清除敏感信息**：在将任何输出文件保存之前，务必扫描源内容，确保其中没有API密钥、令牌或其他敏感凭证。
