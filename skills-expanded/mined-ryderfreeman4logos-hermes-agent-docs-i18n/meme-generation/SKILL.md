---
name: meme-generation
description: Create meme PNGs from templates with Pillow text overlay.
version: 2.0.0
author: adanaleycio
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, memes, humor, images]
    related_skills: [ascii-art]
    category: creative
---

# 模因生成

根据给定主题生成真实的模因图片。系统会自动选择模板、撰写文字说明，并输出带有文字叠加层的真实 .png 文件。

## 适用场景

- 用户要求你创建或生成模因
- 用户希望针对特定主题、情境或烦恼制作模因
- 用户说出“把XX做成模因”之类的指令

## 可用模板

该脚本支持通过名称或编号调用 **约100种流行的imgflip模板**，此外还提供10种经过精心筛选的模板，其文字位置已优化设置。

### 精选模板（自定义文字位置）

| ID | 名称 | 字段位置 | 最佳适用场景 |
|----|------|----------|--------------|
| `this-is-fine` | 一切正常 | 顶部、底部 | 混乱状态、否认态度 |
| `drake` | Drake Hotline Bling | 拒绝、同意 | 表达拒绝或偏好 |
| `distracted-boyfriend` | 分心的男友 | 分心物、当前对象、人物 | 面对诱惑时优先级改变 |
| `two-buttons` | 两个按钮 | 左侧、右侧、人物 | 面临两难选择 |
| `expanding-brain` | 扩展的大脑 | 4个层级 | 逐步加剧的讽刺情境 |
| `change-my-mind` | 改变我的想法 | 文字陈述 | 表达激烈观点 |
| `woman-yelling-at-cat` | 女人对着猫大喊 | 女人、猫 | 争吵场景 |
| `one-does-not-simply` | 事情并非如此简单 | 顶部、底部 | 看起来困难实则简单的任务 |
| `grus-plan` | 格鲁的计划 | 第1-3步、最终领悟 | 计划最终适得其反 |
| `batman-slapping-robin` | 蝙蝠侠打罗宾 | 罗宾、蝙蝠侠 | 驳斥糟糕主意 |

### 动态模板（来自imgflip API）

任何未列入精选列表的模板，均可通过其名称或 imgflip ID 来调用。这些模板都具备智能的默认文本定位功能：双字段模板会将文本置于上下两侧，而三字段及以上的模板则会让文本均匀分布。可通过以下方式进行搜索：
```bash
python "$SKILL_DIR/scripts/generate_meme.py" --search "disaster"
```

## 操作步骤

### 模式1：经典模板（默认）

1. 阅读用户提供的主题，识别其中的核心情感或情境（如混乱、两难、偏好、反讽等）。
2. 选择最匹配的模板。可通过“适用场景”一栏进行筛选，或使用 `--search` 参数进行搜索。
3. 为每个字段编写简短的标题说明（每字段字数建议在8-12字之间，越简短越好）。
4. 找到对应技能的脚本目录：
   ```
   SKILL_DIR=$(dirname "$(find ~/.hermes/skills -path '*/meme-generation/SKILL.md' 2>/dev/null | head -1)")
   ```
5. 运行生成器：
   ```bash
   python "$SKILL_DIR/scripts/generate_meme.py" <template_id> /tmp/meme.png "caption 1" "caption 2" ...
   ```
6. 使用 `MEDIA:/tmp/meme.png` 返回图片。

### 模式2：自定义AI图片（当支持 `image_generate` 功能时）

当传统模板不适用，或用户希望获得原创内容时，可使用此模式。

1. 先编写文字说明。
2. 使用 `image_generate` 创建与表情包概念相匹配的场景。在图片提示词中不要包含任何文字——文字将由脚本添加，只需描述视觉场景即可。
3. 从 `image_generate` 的结果URL中获取生成的图片路径，如有需要可将其下载到本地。
4. 运行脚本并加上 `--image` 参数来叠加文字，同时选择叠加模式：
   - **叠加**（文字直接显示在图片上，白色背景并带有黑色轮廓）：
     ```bash
     python "$SKILL_DIR/scripts/generate_meme.py" --image /path/to/scene.png /tmp/meme.png "top text" "bottom text"
     ```
- **条状栏**（上下为黑色条带，配以白色文字——视觉更简洁，且始终清晰可读）：
     ```bash
     python "$SKILL_DIR/scripts/generate_meme.py" --image /path/to/scene.png --bars /tmp/meme.png "top text" "bottom text"
     ```
当图像内容过于复杂或细节繁多，导致文字难以清晰显示时，请使用 `--bars` 参数。
5. **通过视觉功能进行验证**（若支持 `vision_analyze` 功能）：检查结果是否正常。
   ```
   vision_analyze(image_url="/tmp/meme.png", question="Is the text legible and well-positioned? Does the meme work visually?")
   ```
如果视觉模型检测到问题（如文字难以辨认、位置不当等），请尝试其他模式（在叠加显示与条形图显示之间切换），或重新生成该场景。
6. 使用 `MEDIA:/tmp/meme.png` 返回图像。

## 示例

**“凌晨2点进行生产环境调试”：**
```bash
python generate_meme.py this-is-fine /tmp/meme.png "SERVERS ARE ON FIRE" "This is fine"
```

**“在入睡与再看一集之间做选择”：**
```bash
python generate_meme.py drake /tmp/meme.png "Getting 8 hours of sleep" "One more episode at 3 AM"
```

**“周一早上的各个阶段”：**
```bash
python generate_meme.py expanding-brain /tmp/meme.png "Setting an alarm" "Setting 5 alarms" "Sleeping through all alarms" "Working from bed"
```

## 模板列表

如需查看所有可用模板：
```bash
python generate_meme.py --list
```

## 常见问题

- 文字说明请保持简短。包含过长文字的模因看起来会很糟糕。
- 文本参数的数量需与模板中的字段数量相匹配。
- 应根据笑话的结构来选择模板，而不仅仅是依据主题。
- 禁止生成充满仇恨、辱骂性或针对个人的内容。
- 脚本会在首次下载后将模板图片缓存到 `scripts/.cache/` 目录中。

## 验证标准

只有满足以下条件，输出结果才视为正确：
- 输出路径下已生成 .png 格式的文件；
- 模板上的文字清晰可辨（白色背景搭配黑色轮廓）；
- 笑话效果良好——文字说明符合模板预定的结构；
- 文件可通过 MEDIA: path 方式进行传输。
