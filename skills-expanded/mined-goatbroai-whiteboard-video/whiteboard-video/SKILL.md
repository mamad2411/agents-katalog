---
name: whiteboard-video
description: "手绘风格技术讲解视频模板。当用户要求生成技术讲解视频、将文章/代码转化为视频、制作知识讲解动画时使用。自带腾讯云 TTS 脚本与 Remotion 项目；如需本地 TTS 请额外配合 vibevoice-tts 技能（可选）。"
---

# 手绘风格技术讲解视频模板

## 用途

将技术文章或代码转化为带语音讲解的手绘风格动画视频，适合社交媒体发布。

## 核心原则

1. **语音说信息，画面演概念，文字只出现关键词/公式**
2. **每场景少元素、有重点**
3. **稿子层层递进**：全局递进，场景内也递进
4. **单一数据源驱动**：`scene-config.json` 是演讲稿、语音、动画、字幕的唯一事实源，视频代码零硬编码
5. **照抄 canonical 实现**：每次新视频以 `LightclawaceVideo.tsx` 为蓝本复制改造，不重新发明组件

## 视频规格

- 竖屏 9:16，1080x1920，30fps
- 总时长约 3 分钟（~180 秒）
- 7-8 个场景，每场景 22-26 秒
- 每场景 140-170 字（腾讯云 TTS 专业梓欣 602005 + 1.1 倍速，实测约 6.5 字/秒）
- 总字数约 1000-1200 字

## 路径约定

执行前必须先确定以下变量：

| 变量 | 含义 | 值 |
|------|------|-----|
| `{CWD}` | 当前工作目录 | `pwd` 的结果 |
| `{SKILL_DIR}` | 本技能目录 | `~/.codebuddy/skills/skills/whiteboard-video` |
| `{OUTPUT_DIR}` | 本次视频的输出目录 | `{CWD}/output/{topic}-{timestamp}` |
| `{REMOTION_DIR}` | Remotion 项目目录 | `{SKILL_DIR}/remotion-project` |
| `{ENV_FILE}` | 腾讯云密钥文件 | `{SKILL_DIR}/.env`（**不是 {CWD}/.env**） |
| `{topic}` | 视频英文 slug | 小写+连字符，如 `claude-tools`、`lightclawace` |
| `{timestamp}` | 生成时间戳 | `YYYYMMDD-HHmm` |

## Installation（首次使用 / 迁移新服务器）

**系统依赖：** `python3` + `node` (>= 18) + `npm` + `ffmpeg`（提供 ffprobe）

一键初始化：
```bash
cd {SKILL_DIR}
bash scripts/setup.sh
```

setup.sh 会：
1. 检查系统依赖（缺了会报错并提示 brew/apt 命令）
2. `pip install -r requirements.txt`（腾讯云 SDK + python-dotenv）
3. `cd remotion-project && npm install`（首次约 2-5 分钟）
4. 生成 `.env.example` 模板供用户填密钥

**必备文件检查：** `{REMOTION_DIR}/public/bgm.mp3` 必须存在（背景音乐，随 skill 分发）。丢失则从备份复制或重新获取。

**密钥配置：**
```bash
cp {SKILL_DIR}/.env.example {SKILL_DIR}/.env
# 编辑 .env 填入 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY
```

**可选外部依赖：** 如需本地 TTS（vibevoice），安装 `~/.codebuddy/skills/skills/vibevoice-tts` 并跑其 setup.sh；未安装时将 `meta.ttsProvider` 保持为 `"tencent"`。

## 参考文档（按需加载）

主流程涉及的详细规范存放在 `references/`：

| 文档 | 何时阅读 |
|------|---------|
| `references/script-writing.md` | Step 1 写演讲稿时 |
| `references/scene-config-schema.md` | Step 2 设计 scene-config.json 时 |
| `references/cover-prompt.md` | Step 2.5 生成封面提示词时 |
| `references/layout-engine.md` | Step 6 实现或复制布局引擎时 |
| `references/components.md` | Step 6 需要查看组件实现细节时 |
| `references/canonical-video-reference.md` | Step 6 **必读**，照抄的起点 |
| `references/publish-copywriting.md` | Step 8 生成发布文案和标签时 |

## 设计规范速查

### 色彩
- 背景 `#F5F5F0`（米白方格纸），方格线 `#E0DDD5`，间距 100px
- 粉 bg `#FDE8E8` border `#E8A0A0`
- 蓝 bg `#E0EEFF` border `#8BB8E8`
- 黄 bg `#FFF5E0` border `#E8C878`
- 深 bg `#2D3748` border `#1A202C`
- 文字：标题 `#2D3748`，正文 `#4A5568`，强调 `#C05050`
- 箭头 `#6B7280`

### 字体
- 全部使用 **站酷快乐体** (`@fontsource/zcool-kuaile`)
- T1 标题 64px / T2 正文 40px / T3 注释 26px

### 手绘风格
- Box/Arrow **内联 SVG 实现**（不要用 roughjs，会在 Remotion 中闪烁）
- 箭头：粗胖实心方块箭头（矩形身体 + 三角头）

### 音频参数
- **旁白音量**：腾讯云 TTS `volume={5.0}`（原始输出偏小），vibevoice-tts `volume={1.0}`
- **BGM**：音量 `0.03`（3%），开头 1 秒淡入，结尾 1 秒淡出，文件 `{REMOTION_DIR}/public/bgm.mp3`，必须 `loop`

### 动画
- 元素入场：`Fade`（淡入+上移）或 `Pop`（spring 弹入）
- 动画 delay 绑定到触发句子的开始时间：`delay = (trigger / subCount) * sceneDur`
- 场景间 PAD = 0.3s
- **不能有黑屏**：每个 Sequence 内必须重绘 Grid 背景（见 canonical-video-reference.md）

## 工作流程

### Step 1: 写演讲稿 ⭐ 最重要的一步

**必读** `references/script-writing.md`。

三步提炼：核心主张（1 句）→ 关键论点（3-5 个）→ 7-8 个场景。

五种骨架选一种：揭秘型 / 问题-方案型 / 概念拆解型 / 对比型 / 清单型。

写完逐条过自检清单（见 script-writing.md 第 7 节）。

### Step 2: 设计分镜，生成 scene-config.json

**必读** `references/scene-config-schema.md`。

操作：
1. 演讲稿按句拆分 → 填入每个场景的 `subtitles[]`
2. 为每句话设计视觉元素 → 填入 `elements[]`，`trigger` 指向对应句子索引
3. 为每个元素标 `row` 编号（同 row 并排，不同 row 上下）
4. 校验所有 `trigger` 值在 `[0, subtitles.length)` 范围内
5. **`meta.topic` 字段必填**，后续资产目录隔离要用
6. **`scenes[].audio` 路径必须带 topic 子目录**：`audio/{topic}/scene1.wav`

核心原则：**画面演概念，不搬字幕**。AI 只决定语义布局，不算坐标。

### Step 2.5: 输出等用户确认 -- 必须停下来

**创建输出目录（用 scaffold 脚本）：**
```bash
cd {CWD}
bash {SKILL_DIR}/scripts/new_video.sh {topic}
# 会创建 output/{topic}-{timestamp}/ 并生成空 scene-config.json 模板
```
> 该脚本校验 topic 格式（必须小写字母+数字+连字符），创建 `audio/{topic}/` 和 `assets/{topic}/` 子目录。

随后用 AI 将完整 scene-config.json 写入 `{OUTPUT_DIR}/scene-config.json`（覆盖模板）。

**在对话中展示给用户：**

1. **全局结构概览**：场景 1 → 场景 2 → ... → 场景 N，递进逻辑说明
2. **每场景摘要**：语音稿全文 + 画面元素列表（type + trigger 对应哪句）
3. **生成封面图（优先使用内置文生图工具）**：
   - ✅ **首选方案**：调用当前 Agent 环境中的 `image_gen` 工具（如 WorkBuddy/Claude Code 内置的 image_gen），按 `references/cover-prompt.md` 构造提示词，**size 设为 `1024x1536`（9:16 竖版，与视频比例一致）**，直接输出到 `{OUTPUT_DIR}/cover.png`
   - ⚠️ **降级方案**：如果当前环境没有文生图工具，输出提示词让用户复制到 nano banana / Midjourney，生成后放到 `{OUTPUT_DIR}/cover.png`
   - 封面用于视频开场 0.5 秒。在 `scene-config.json` 中设 `meta.cover = "cover.png"`，无封面则设为 `null`
4. **素材清单**：所有 SVG 文件名和描述

询问用户：演讲稿是否清晰？视觉元素是否合适？封面提示词是否满意？

**用户确认后才进入 Step 3。**

### Step 3: 生成 TTS 音频，回填时长

TTS 方案由 `meta.ttsProvider` 决定：
- `"tencent"` → **本 skill 自带的**腾讯云 TTS（需要 `{SKILL_DIR}/.env` 中有 `TENCENT_SECRET_ID`/`TENCENT_SECRET_KEY`）
- `"vibevoice"` → 本地 vibevoice-tts（**可选外部依赖**，需要额外安装 `~/.codebuddy/skills/skills/vibevoice-tts` 及其 venv。未安装则降级为 tencent 或提示用户选择）

**先创建 topic 隔离的音频目录：**
```bash
mkdir -p {OUTPUT_DIR}/audio/{topic}
```

**腾讯云 TTS：**
```bash
python3 {SKILL_DIR}/scripts/tts_tencent.py \
  --text "讲解文字" \
  --output {OUTPUT_DIR}/audio/{topic}/scene1.wav
```
音色：专业梓欣 602005，1.1 倍速。长文本用 `{SKILL_DIR}/scripts/tts_batch.py`。

**vibevoice-tts（可选外部 skill）：**
```bash
# 前置：确认 ~/.codebuddy/skills/skills/vibevoice-tts/.venv 存在；
# 不存在时告知用户运行 `bash ~/.codebuddy/skills/skills/vibevoice-tts/scripts/setup.sh` 初始化，
# 或将 scene-config.json 的 meta.ttsProvider 改为 "tencent"。
VIBEVOICE_DIR=~/.codebuddy/skills/skills/vibevoice-tts
uv run --python ${VIBEVOICE_DIR}/.venv/bin/python ${VIBEVOICE_DIR}/scripts/tts_generate.py \
  --text "讲解文字" \
  --output {OUTPUT_DIR}/audio/{topic}/scene1.wav \
  --speaker_names zh-Xinran_woman
```

**回填 duration：**
```bash
duration=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 {OUTPUT_DIR}/audio/{topic}/scene1.wav)
```
用 Edit 写回 scene-config.json 对应场景的 `"duration": null` 行。

**必须所有场景都回填 duration 才进入下一步。**

### Step 3.5: 校验时长，必要时回调修稿

- 单场景 duration 应在 **18-30 秒**
- 总时长（scenes duration 之和 + pad + 封面）应在 **2:30 - 3:30**

不通过：打印问题摘要给用户，确认修改 → 只重跑改过场景的 TTS → 再校验。

### Step 4: 计算 timeline.json ⚡ 可与 Step 5 并行

Claude Code 直接计算，用 Write 写出 `{OUTPUT_DIR}/timeline.json`，不需要跑脚本。

**计算逻辑：**
```python
fps = 30
padFrames = round(0.3 * fps)  # 9
coverFrames = round(meta.coverDuration * fps) if meta.cover else 0

globalOffset = coverFrames
for scene in scenes:
    scene.startFrame = globalOffset
    scene.durationFrames = round(scene.duration * fps)
    # 校验 trigger 在 [0, len(subtitles)) 范围，越界立即报错回到 Step 2
    for elem in scene.elements:
        assert 0 <= elem.trigger < len(scene.subtitles)
    globalOffset = scene.startFrame + scene.durationFrames + padFrames

totalFrames = globalOffset - padFrames  # 最后场景无尾部 pad
```

**timeline.json 格式（极简）：**
```json
{
  "totalFrames": 5226,
  "totalDuration": 174.2,
  "cover": { "startFrame": 0, "durationFrames": 15 },
  "scenes": [
    { "id": "scene1", "startFrame": 15, "durationFrames": 690, "duration": 23.0 }
  ]
}
```

> 字幕/元素的场景内时间由视频代码从 scene-config.json 实时计算（按句数均分），不存到 timeline.json。

**打印时间轴摘要供核对：**
```
封面  [0.0s - 0.5s]
场景1 [0.5s - 23.5s] "源码泄露" 3 句 / 3 元素
场景2 [23.8s - 48.2s] ...
总时长: 174.2s (2:54)
```

### Step 5: 生成 SVG 插图 ⚡ 可与 Step 4 并行

从 scene-config.json 找所有 `type: "svg"` 的元素，用 Write 工具创建文件到 `{OUTPUT_DIR}/assets/{name}.svg`。

**SVG 规范：**
- `viewBox="0 0 400 400"`，透明背景
- 使用设计规范色彩
- `stroke-width: 3-4px`，`stroke-linecap: round`，`stroke-linejoin: round`
- 有机线条（非完美几何），保持手绘感
- 所有元素内联，不引用外部图片/字体

参考已有素材：`{REMOTION_DIR}/public/assets/` 下有历史 SVG。

### Step 6: 同步资源到 Remotion 项目

**新架构（2026-04 重构）**：`LightclawaceVideo.tsx` 已是"数据驱动的 canonical 渲染器"——它动态读取 `scene-config.json` 的 `meta.topic`、subtitles、elements，**不需要为每个新视频复制/修改 tsx**。只需：

1. 覆盖 `src/scene-config.json` 和 `src/timeline.json`
2. 把资源复制到 `public/` 对应的 topic 子目录
3. 直接跑 Studio / 渲染

**6a. 复制资源到 remotion public（topic 隔离）：**
```bash
# 音频：隔离到 public/audio/{topic}/
mkdir -p {REMOTION_DIR}/public/audio/{topic}
cp {OUTPUT_DIR}/audio/{topic}/*.wav {REMOTION_DIR}/public/audio/{topic}/

# SVG：隔离到 public/assets/{topic}/
mkdir -p {REMOTION_DIR}/public/assets/{topic}
cp {OUTPUT_DIR}/assets/*.svg {REMOTION_DIR}/public/assets/{topic}/ 2>/dev/null || true

# 封面（如有）
cp {OUTPUT_DIR}/cover.png {REMOTION_DIR}/public/assets/cover_{topic}.png 2>/dev/null || true
```

> **为什么 topic 子目录：** 多个视频共用 `public/` 会互相覆盖。每个视频的 `scenes[].audio` 格式为 `audio/{topic}/scene1.wav`，SVG 的 `src` 为 `assets/{topic}/xxx.svg`，新旧视频互不干扰。

**6b. 覆盖 JSON 数据（单一事实源）：**
```bash
cp {OUTPUT_DIR}/scene-config.json {REMOTION_DIR}/src/scene-config.json
cp {OUTPUT_DIR}/timeline.json    {REMOTION_DIR}/src/timeline.json
```

> 这是同一时刻 Remotion 项目中唯一活跃的视频数据。下次渲染另一个视频时再覆盖即可。历史视频数据如需保留，在 `{OUTPUT_DIR}` 里自动归档。

**6c. 不需要改 tsx / index.tsx！**

index.tsx 已注册 id 为 `VideoMain` 的 Composition，`durationInFrames` 从 `timeline.totalFrames` 自动读取，`LightclawaceVideo` 组件从 `meta.topic` 动态拼接资源路径。

**仅当你需要改组件逻辑（新增元素类型、动画）时才编辑 `LightclawaceVideo.tsx`。**

### Step 6.5: 在线预览校验 -- 必须停下来

```bash
cd {REMOTION_DIR}
npx remotion studio src/index.tsx
```

打开 `http://localhost:3000`，选择 **`VideoMain`** composition，检查：
- [ ] 字幕出现时机与语音内容对得上
- [ ] 元素在对应语句说出时出现
- [ ] 单行单元素是否居中，多行是否整体居中
- [ ] 无闪烁、无黑帧
- [ ] 字体正确（站酷快乐体）
- [ ] BGM 不盖过旁白

问题调整：
- 时间不对 → 改 scene-config.json 的 subtitles 或 elements.trigger → 回 Step 4 重新计算 timeline.json → 重跑 6b
- 画面不对 → 改 scene-config.json 的 elements → 重跑 6b
- 组件渲染不对 → 改 LightclawaceVideo.tsx（一次性修复，之后所有视频受益）

Studio 热更新，改完刷新即可。用户确认后按 Ctrl+C 关掉，进入 Step 7。

### Step 7: 全量渲染

```bash
cd {REMOTION_DIR}
npx remotion render src/index.tsx VideoMain \
  --output {OUTPUT_DIR}/video.mp4 \
  --concurrency=1
```

`--concurrency=1` 避免内存问题。3 分钟视频约渲染 10-15 分钟。

完成后打印：
```
✅ 视频渲染完成！
  文件：{OUTPUT_DIR}/video.mp4
  时长：{totalDuration}s
  尺寸：1080x1920
  场景数：{N}
  topic：{topic}
```

### Step 8: 生成短视频发布文案和标签 🚀 必做

**必读** `references/publish-copywriting.md`。

渲染完成后，基于 scene-config.json 自动生成**纯内容**发布文案，写入 `{OUTPUT_DIR}/publish.md`。**原则：拿来即用，不给选择题，无任何小标题/说明/装饰**。

**输出格式（严格遵守，纯内容按顺序排列，空行分隔）：**

```
[标题 14-20字]

[正文第1段 钩子 20-40字]

[正文第2段 核心内容 40-80字]

[正文第3段 CTA引导 20-30字]

#标签1 #标签2 #标签3 ... （10-12 个一行，空格分隔）
```

**示例（完整 publish.md 内容）：**

```
锐评2026十款AI视频软件，从夯到拉依次排名！

作为用了一年AI视频软件的老用户，掏心窝子说句实话👇

2026年AI视频格局洗牌：Sora 2和即梦并列"夯"；可灵和Veo 3并列"顶级"；海螺、Vidu、拍我AI、Runway属于"人上人"；通义万象和SD只能算"NPC"。

做漫剧选可灵，做特效选Veo3，做打戏选海螺，预算有限闭眼冲拍我AI。你最常用哪款？评论区告诉我！

#AI视频 #AI工具推荐 #Sora #可灵 #即梦 #Veo3 #Runway #AIGC #AI测评 #2026AI #国产AI #AI视频软件
```

**AI 执行流程：**

1. 读取 `{OUTPUT_DIR}/scene-config.json`，提取 `meta.title` 和所有 subtitles
2. 从讲解稿提炼核心关键词 3-5 个
3. 按上述格式直接写入 `{OUTPUT_DIR}/publish.md`
4. 在对话中同步展示内容给用户

**严禁出现：**
- `## 标题` `## 正文` `## 标签` 之类的小标题
- "以下是..." "候选方案" "发布建议" 之类的说明文字
- 多个候选、平台分版、检查清单
- emoji 堆砌（每段最多 1 个）

**内容要求：**
- 标题只给一个 14-20 字，带数字/情绪词/悬念至少 2 项
- 正文三段共 80-150 字（钩子→内容锚点→CTA）
- 标签 10-12 个，一行，带 `#` 空格分隔
- 紧扣视频实际内容，禁止虚假承诺

## 输出目录结构

```
{OUTPUT_DIR}/
├── scene-config.json     # 单一数据源
├── timeline.json         # 派生时间轴
├── audio/
│   └── {topic}/          # topic 隔离，避免覆盖旧视频
│       ├── scene1.wav
│       └── ...
├── assets/               # SVG 插图
├── cover.png             # 封面（可选）
├── video.mp4             # 最终输出
└── publish.md            # 短视频发布文案+标签（Step 8 产物）
```

## Troubleshooting

### 开发相关
- **字幕与语音不同步**：检查 scene-config.json 的 duration 是否已回填、timeline.json 是否重新生成
- **动画时机不对**：检查 elements[].trigger 是否指向正确的 subtitle 索引
- **trigger 越界报错**：trigger 必须 `>= 0` 且 `< subtitles.length`
- **Box 闪烁**：确认没有用 roughjs canvas，改用 RoughBox（内联 SVG）
- **字体没加载**：`@fontsource/zcool-kuaile` 已安装且顶部 import
- **TTS 中文标点发音异常**：讲解文字中文标点必须转英文
- **渲染内存不足**：`--concurrency=1`
- **场景间跳帧/重叠**：Sequence 的 durationInFrames 不包含 pad
- **场景间黑帧/黑屏**：每个 Sequence 内必须重绘 Grid 背景（见 canonical-video-reference.md）
- **改稿后视频没变**：改 scene-config.json 后必须重跑 Step 3→4→6b，并重新复制资源到 public/
- **staticFile 找不到**：确认 Step 6a 已把资源按 topic 子目录复制到 `{REMOTION_DIR}/public/`

### 迁移/环境相关
- **腾讯云 TTS 报"密钥未找到"**：`.env` 必须在 `{SKILL_DIR}/.env`（不是 CWD），可 `cp .env.example .env` 后填入
- **`ffprobe: command not found`**：未安装 ffmpeg。macOS `brew install ffmpeg`；Ubuntu `apt-get install ffmpeg`
- **`npx: command not found` 或 Studio 报缺依赖**：未跑过 `npm install`，运行 `bash scripts/setup.sh` 或 `cd remotion-project && npm install`
- **Python `ModuleNotFoundError: tencentcloud`**：未装 Python 依赖，运行 `pip install -r requirements.txt`
- **bgm.mp3 不存在**：`.gitignore` 会跳过 public/ 大部分内容但白名单保留 bgm.mp3；如果克隆后仍缺失，从备份手动复制到 `{REMOTION_DIR}/public/bgm.mp3`
- **Remotion Studio 只显示 VideoMain 和 Prototype**：这是当前设计——一次只跑一个主视频（VideoMain）。想并列多个视频做对比预览，复制 index.tsx 的 Composition 并改 id

## 性能注意事项

- **TTS 是瓶颈**：腾讯云秒级，vibevoice 本地需 2-5x 实时因子
- **推荐工作流**：TTS 全部生成 → 回填 duration → 计算 timeline（可与 SVG 并行）→ 写场景代码
- **预览优先**：全量渲染前用 Studio 实时预览，改代码即时生效

## 踩坑经验

（由 AI 在实际调用中自动积累。只记录经过 **2 次及以上尝试** 才成功的情况。格式：`- 场景描述：经验要点`）

- LightclawaceVideo / 腾讯云 TTS 旁白偏小：`volume={5.0}` 才能盖过 BGM，文档曾写 3.0 不够
- Remotion Sequence 切换 / PAD 黑屏：每个 Sequence 内必须重绘 `<Grid />`，只靠外层 AbsoluteFill 的 Grid 在 Sequence 活跃期间会被遮挡
- RoughBox / 手绘矩形闪烁：roughjs 每帧重算路径在 Remotion 中会闪烁，改用内联 SVG `<rect>` + 伪高光条
- 字幕时间分配 / 按字数 vs 按句数：按字数比例分配对中英混合不稳定，改为按句数均匀分配（`(i/subCount) * sceneDur`）更可靠
- 多视频共用 public/ / 资源覆盖：audio/assets 必须按 topic 子目录隔离（`public/audio/{topic}/`），否则新视频会覆盖旧视频的资源
