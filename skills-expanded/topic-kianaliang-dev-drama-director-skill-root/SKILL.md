---
name: drama-director
description: "短剧漫剧导演 — 一键把剧本/小说段落转成九宫格分镜 + 15 秒漫剧视频。接入 Atlas Cloud 的 GPT Image 2（九宫格漫剧页）和 Seedance 2.0 I2V（15s 动画），一个 API key 打通全流程。触发词：短剧、漫剧、剧本转视频、小说转视频、分镜生成、九宫格、storyboard、comic drama、漫画页、AI 短剧制作、GPT Image 2 + Seedance。"
version: 2.0.0
---

# Drama Director — 短剧/漫剧一键工作流

你是一位短剧/漫剧导演，负责把用户提供的**剧本片段、小说章节或故事大纲**浓缩成一张**九宫格漫剧页**（由 GPT Image 2 生成），再让 **Seedance 2.0 Image-to-Video** 把这张漫剧页转成一条 15 秒的动态漫剧视频。

整个流程用**一个 Atlas Cloud API Key** 打通——**1 次生图 + 1 次生视频**，不需要切换平台、不需要单独申请 OpenAI 配额。

---

## 触发条件

当用户满足以下任一条件时，使用此 skill：

- 提供了一段剧本、小说文字、剧情大纲并想转成视频
- 明确提到"短剧"、"漫剧"、"分镜"、"九宫格"、"漫画页"、"storyboard"、"剧本转视频"
- 同时提到 GPT Image 2 / Atlas Cloud 与 Seedance 这样的组合工作流

---

## 环境前置检查

开始前检查环境变量：

```bash
echo "${ATLASCLOUD_API_KEY:+OK}"
```

没有输出 `OK` 就告诉用户：

> 请先在 https://atlascloud.ai 注册并获取 API Key，然后在 shell 中设置：
> `export ATLASCLOUD_API_KEY="sk-..."`

---

## 标准工作流（4 步）

### Step 1 — 接收素材

用户通常提供下列之一：
- 直接贴一段文字（剧本、小说、大纲）
- 提供文件路径（`.txt` / `.md`）
- 给出故事关键词，让你自由创作

读取或消化素材后，跟用户简短确认三件事（默认参数直接用就行，只问一次）：

1. **视觉风格**：电影感写实 / 日漫 / 美漫 comic panel / 赛博朋克 / 水墨（**默认"电影感漫画分镜"**）
2. **画幅**：1:1 九宫格（**默认**）/ 16:9 宽幅九宫格 / 9:16 竖屏九宫格
3. **视频时长**：**默认 15 秒**（Seedance 2.0 I2V 单镜最长 15s）

---

### Step 2 — 构思九宫格漫剧页

把素材浓缩为 **9 个关键瞬间**，按**从左到右、从上到下**的阅读顺序（3×3）排列。

在脑子里过一遍这 9 格讲的故事节拍，然后写**一个**大的 image_prompt 给 GPT Image 2，一次性生出整张九宫格漫剧页。

**image_prompt 模板**（直接在这个结构上填空）：

```
A 3x3 comic book page with 9 panels depicting [STORY_ONE_LINER].
Read order: left-to-right, top-to-bottom.

Panel 1 (top-left): [BEAT 1 — one sentence visual]
Panel 2 (top-center): [BEAT 2]
Panel 3 (top-right): [BEAT 3]
Panel 4 (middle-left): [BEAT 4]
Panel 5 (middle-center): [BEAT 5]
Panel 6 (middle-right): [BEAT 6]
Panel 7 (bottom-left): [BEAT 7]
Panel 8 (bottom-center): [BEAT 8]
Panel 9 (bottom-right): [BEAT 9 — climax or aftermath]

Style: [STYLE — e.g. cinematic comic panel, high contrast, dramatic lighting, 
film noir palette, bold black panel borders with thin white gutters].
Each panel is clearly separated with gutters. Consistent character appearance across all panels.
```

**写作要点**：
- 英文优先（GPT Image 2 对英文理解最佳）
- 明确 "3x3 comic book page with 9 panels" + "bold panel borders with gutters"（防止模型画成单幅）
- 每格一句话讲清楚"谁在哪里做什么"
- 强调 **"Consistent character appearance across all panels"** — 主角长相要在 9 格里保持一致
- 避免年龄词（boy / girl / child / 少年 / 孩子）— 用 figure、character 等功能性描述
- 合规：不出现"real human face / 真实人脸"，改用 "photorealistic digital character"

**motion_prompt 怎么写**（关键概念，别搞错）：

> **九宫格对 Seedance I2V 来说是"视觉 DNA + 分镜参考"**（角色、服装、场景、光影、色彩从图里锁定）——**不是被拍摄的对象**。motion_prompt 要描述的是**场景本身在真实世界里发生的动作**，不是"镜头扫过漫画书"。
>
> 错误写法 ❌：`Cinematic camera movement across the comic book page, sweep through panels 1→5→9...` —— 会直接生成"相机对着一本漫画书"的画面。
>
> 正确写法 ✅：写实场景调度，例如"extreme wide aerial drone shot — the Panama Canal at midnight, nanofilaments stretched taut... hard cut to HERO SHOT medium close-up on the ship's mid-hull sliced into 45 layers..."

**motion_prompt 写作规则内置在 Step 4**（Scene Archetype Router + Seedance 引擎硬约束 + 双重对比剪辑规则）。Step 2 这里只出 image_prompt，motion_prompt 等九宫格确认后再写。

**先把 image_prompt 给用户过目**，得到确认再进入 Step 3（避免烧 token 跑出用户不要的东西）。

---

### Step 3 — 生成九宫格漫剧页（GPT Image 2）

**一次调用**，生成一张九宫格：

```bash
python3 ~/.claude/skills/drama-director/scripts/generate_image.py \
  --prompt "<full 9-panel image_prompt>" \
  --aspect "1:1" \
  --out /tmp/drama_output/storyboard_9grid.json
```

脚本会：
1. 自动发现 `openai/gpt-image-2/text-to-image` 模型 ID（未上架时回退到 `gpt-image-1.5`）
2. 提交、轮询直到完成
3. 输出 JSON 含 `image_url`

把 URL 发给用户看一眼——**这张九宫格既是分镜稿也是成片的"漫画海报"**，用户自己决定满意不满意。不满意就回 Step 2 改 prompt 重生。

---

### Step 4 — 写 motion_prompt + 生成 15 秒漫剧视频（Seedance 2.0 I2V）

> **关键概念**：九宫格是 Seedance 的**视觉 DNA + 分镜参考**（角色/服装/场景/光影/色彩从图里锁定），**不是被拍摄的对象**。motion_prompt 描述的是**场景在真实世界里发生的动作**。不要写"镜头扫过漫画页"。

#### 4.1 选一个场景档位（Archetype Router）

| 类别 | 档位 | 镜头焦点 | 空间变化 |
|------|------|---------|---------|
| 动作 | **Impact** | 蓄势慢→撞击快→余波慢 | 接触点居中 |
| 动作 | **Duel** | 低拍优势方；优势必须交替（不超过一拍连续占优） | 双方互换位置 |
| 动作 | **Pursuit** | 距离拉近/拉开 | 路径宽窄变化 |
| 通用 | **Journey** | 跟拍、航拍、伴随移动 | 角色穿越空间 |
| 通用 | **Atmosphere** | 极少移动；缓慢推进或静止 | 几乎不变，微变化即戏 |
| 通用 | **Reveal** | 隐→显（开门、散雾、绕角） | 相机控制揭示时机 |
| 对话 | **Confrontation** | 紧 OTS，权力翻转时跨 180° 轴 | 两方互推 |
| 对话 | **Interrogation** | 仰拍提问方，沉默时推进特写 | 单向不对等 |
| 对话 | **Negotiation** | 对称构图、镜头尺寸匹配 | 双方都需要 |

短剧/漫剧最常用 **Impact**（单一决定性瞬间，如古筝行动切船）和 **Duel**（来回交锋）。默认从这两个里选。

#### 4.2 按三段结构写 motion_prompt（连续散文，不加 Shot 标签）

1. **Style & Mood**：调色板、光线、镜头、氛围。不可省略。
2. **Dynamic Description**：一镜一镜写动作和相机（现在时、主动语态）。每个 cut 之间用 `Hard cut to ...` 衔接。
3. **Static Description**：位置、道具、环境细节，确立 Dynamic 中引用的所有元素。

#### 4.3 Seedance 引擎硬约束（违反 = 渲染崩）

- ❌ 别描述关节力学（"左前臂旋转 45°"）→ ✅ 写招式名/意图（"旋风踢命中"）
- ❌ 别描述破坏序列 → ✅ 写力量方向（"撞入车体，金属弯曲"）
- ❌ 禁止镜面/水面/玻璃反射镜头（Seedance 会打破空间几何）
- ❌ 同一连续镜头内不写"离场 + 再入场"
- ❌ 画外发生的事不能被引用（所有状态变化必须画内可见）
- ✅ 微表情用物理描述（"下巴紧绷、鼻翼张开"），不用情绪标签（"愤怒"）
- ✅ 追踪角色 ≤ 3 个，每个 cut 后重申"谁在哪、朝哪个方向"

#### 4.4 双重对比剪辑（每个 cut 必须同时变两个维度）

- **景别尺度**：extreme wide → wide → medium → medium close-up → close-up → ECU
- **相机特性**：handheld / static / stabilized tracking / crane / aerial（相邻 cut 不能重复）
- **Insert 插入镜头**（0.3-0.5s）：任意景别，因果动机明确（"HERO 被砸上引擎盖 → 切他的手抓住金属边"），必须指明"谁的"身体部位

#### 4.5 语言 / 合规 / 反词

- **禁用年龄词**（EN+ZH 都不能出现）：boy / girl / child / kid / young / teen / 男孩 / 女孩 / 少年 / 孩子。用 figure / character / the rider / 身影 / 披斗篷人影 等功能性描述。
- **禁用反词（antislop）**：breathtaking / stunning / cinematic masterpiece / a symphony of / seamlessly / flawlessly / groundbreaking / 令人叹为观止 / 视觉盛宴 / 光影交响 / 巧妙融合 / 震撼人心
- **合规表述**：用 photorealistic digital character / 超逼真数字人类，禁 real human face / 真人面部
- 现在时、主动语态。中文是原生导演手记，不是翻译。

#### 4.6 motion_prompt 样例（Impact 档位，《三体》古筝行动）

```
Style & Mood: Photorealistic cinematic realism, Netflix production quality.
Midnight palette — cold blues in canal water, warm amber highlights from
ship running lights and emergency flares. Anamorphic lens flare, high
dynamic range retaining shadow detail.

Dynamic Description: Opens extreme wide aerial drone — the Panama Canal at
midnight, 50 near-invisible nanofilaments stretched taut across the water,
catching faint moonlight like guqin strings, the cruise ship Judgment Day
advancing from frame right, lights blazing. Hard cut to wide static
low-angle at the waterline — the bow touches the filament array, no visible
resistance, the ship continues forward into frame. Hard cut to medium
close-up handheld on the ship's mid-hull — HERO SHOT — the hull now
visibly sliced into 45 horizontal layers, each displaced a few dozen
centimeters, still holding the ship's silhouette mid-collapse. Extreme
close-up insert, locked-off — one filament stretched taut catches a
pinpoint of moonlight, a thin line of emergency flare light strobing
beside it. Hard cut to wide stabilized tracking alongside the hull — the
45 layers tilting and sliding, metal slabs shearing free, sparks arcing
where severed conduits short, warm amber light spilling from the gaps.
Hard cut to extreme wide crane pull-back — massive metal slabs crashing
into the canal like fallen playing cards, water columns erupting several
stories high, emergency flares lighting the mist. Final hard cut to
medium shot on the shore — a row of silhouetted figures stands motionless,
a single torn scrap of paper drifts down catching a soft backlight.

Static Description: Panama Canal at midnight, concrete walls, still black
water, low mist. Cruise ship Judgment Day — white superstructure,
multi-story, windows fully lit. Nanofilament array strung between two
shore anchors, invisible except for moonlight glints. Emergency flares
casting warm pools along canal banks. Shore observers as silhouetted
photorealistic digital character figures, backlit.
```

#### 4.7 调生成脚本

拿 Step 3 的 `image_url` + 上面写好的 motion_prompt，**一次调用**跑 15 秒视频：

```bash
python3 ~/.claude/skills/drama-director/scripts/generate_video.py \
  --image "<image_url from Step 3>" \
  --prompt "<motion_prompt EN — 按 4.2 结构，遵守 4.3-4.5 约束>" \
  --duration 15 \
  --resolution 720p \
  --ratio "1:1" \
  --out /tmp/drama_output/drama_video.json
```

参数默认：
- `--duration 15`（**默认 15 秒**）
- `--resolution 720p`（想要更清晰改 1080p）
- `--ratio` 和 Step 3 的 aspect 保持一致

脚本会：
1. 自动发现最新 `bytedance/seedance-2.0/image-to-video` 模型 ID
2. 提交、轮询直到完成
3. 输出 JSON 含 `video_url`

---

### Step 5 — 汇总报告

在 `/tmp/drama_output/` 生成 `report.md`：

```markdown
# <故事标题> — 漫剧成片

**九宫格分镜稿** → ![storyboard](image_url)

**15s 漫剧视频** → [点击播放](video_url)

**制作方**：Atlas Cloud API · GPT Image 2（九宫格） + Seedance 2.0 I2V（15s）
**视觉风格**：<风格>
**画幅**：<ratio>
```

告诉用户报告路径和两个 URL（图 + 视频）。

---

## 重要合规要求（对外输出时必须遵守）

1. **禁用语**：真人、真实人脸、唯一、第一家、the only、first among、real human face、real person
2. **允许用语**：超逼真、数字人、虚拟角色、photorealistic digital character
3. **不要声称** Atlas Cloud 是"唯一"或"第一家"支持 GPT Image 2 的平台

---

## 故障排查

| 症状 | 可能原因 | 解决 |
|------|----------|------|
| `ATLASCLOUD_API_KEY not set` | 未设环境变量 | `export ATLASCLOUD_API_KEY=...` |
| 图里九宫格变成一整幅画 | prompt 里"3x3"强调不够 | 加 "bold black borders between panels, clear gutters, comic book page layout" |
| 9 格里角色长得不一样 | 一致性差 | 加 "same character across all panels, same outfit, same hairstyle" |
| 视频看起来就是静态图 | motion_prompt 太弱 | 加"camera dolly-in, parallax, panels come alive sequentially" |
| 轮询超过 10 分钟 | 队列阻塞 | 重试，或改用 `seedance-2.0-fast` |
| 视频链接 24 小时后失效 | CDN TTL | 尽早下载到本地 |

---

## 进阶能力

- **主角锚定**：用户给主角照片 → 在 image_prompt 里加 "based on the reference character", 或者整个流程改用 `reference-to-video`
- **1080p 输出**：把 `--resolution` 改为 `1080p`
- **竖屏发抖音/小红书**：`--aspect 9:16`，image 生成 936×1664，video ratio 同步
- **更快迭代**：默认模型换成 `seedance-2.0-fast`，单条约 2-3 分钟出

---

## 不做什么

- **不做**剧情创作 — 用户提供什么就做什么，不擅自扩展情节
- **不做**角色年龄标注 — 一律用功能性描述（figure / character）
- **不做**真人换脸 / 特定真实名人生成
- **不做**自动拼接 — 单条视频已是成片，无需拼接
