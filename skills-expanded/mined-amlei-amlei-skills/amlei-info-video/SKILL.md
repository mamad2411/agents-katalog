---
name: amlei-info-video
description: 把有可靠来源的信息、新闻、热点、事件、产品、政策、研究或绯闻，制作成 9:16 中文资讯视频。使用线上 Qwen TTS 和 filetrans ASR、无文稿盲字幕、yt-dlp 素材、FFmpeg 硬切合成。当用户要收集资讯选题、制作新闻解读、热点事件、产品发布、政策研究或人物事件视频，或要求这套 qwen-audio TTS/ASR 流水线时使用；不用于虚构剧情、普通剪辑或无来源爆料。
---

# 资讯视频

制作规则：一个主题一个视频；事实必须有可靠来源；不虚构、不传播未证实内容；信息可以来自任何领域，但必须可核验。

## 核心流水线

```text
收集选题 → 用户选定 → 核实来源 → 资讯拆解 → 写旁白稿 → 线上 TTS →
线上盲 ASR → 自动字幕 cue → 素材池 → 9:16 视频分段 → 字幕/水印 overlay → 合成 → QC
```

默认模型：

```text
TTS: qwen-audio-3.1-tts-flash
ASR: qwen-audio-3.1-asr-flash-filetrans
```

所有模型请求必须通过 `scripts/info_video.py` 完成；不要把 API key 写入提示词、日志或交付文件。

## 目录约定

`init` 会创建并落盘以下结构：

```text
<slug>/
  00_project.md
  01_topics/topic_shortlist.md
  01_topics/selected_topic.md
  02_narration/narration.md
  02_narration/title_description.md
  03_materials/material_list.md
  03_materials/visual_pool.json
  04_tts/
  05_asr/
  06_subtitles/
  07_final/
  08_qc/
.amlei-skill/info-video/  本 Skill 的项目级授权/设置
```

人类可读的事实、清单、旁白、运行记录、QC 报告都写 `.md`。JSON 只作为下一步流水线的机器状态。

## 1. 选题与用户确认

先广泛搜索新闻、官方公告、X、YouTube、微博、小红书、播客、论文、报告、产品页面等公开来源，写入 `01_topics/topic_shortlist.md`。

每条推荐必须有：

- 最重要的一件事；
- 为什么现在值得看；
- 冲突、反转、影响或实用价值；
- 至少一个可靠来源和链接；
- 素材线索；
- 风险；
- 推荐理由。

只有可核验的信息才可推荐。未证实爆料、断章取义、虚构剧情不得进入正片。给出推荐后停下，让用户选择。

## 2. 选定后落盘

把用户选中的主题写入 `01_topics/selected_topic.md`。

先读 [references/editorial_intake.md](references/editorial_intake.md)，完成：

- 抓核心；
- 补背景；
- 站在观众角度；
- 选择叙事结构。

再落盘：

- 核心事件时间线；
- 每条事实和来源；
- 素材线索；
- 开头 3 秒钩子；
- 中段关键信息或金句；
- 结尾问题；
- 明确不采用的无来源内容。

## 3. 旁白稿

写旁白前先读 [references/editorial_intake.md](references/editorial_intake.md)。  
不要只把资料压缩成流水账；要先把信息转成观众能理解的资讯，再写成口播文本。

写入 `02_narration/narration.md`。格式：

```markdown
## S01
第一句完整旁白。

## S02
第二句完整旁白。
```

要求：

- 开头直接给最重要的事实或反差；
- 不用“近日”“据悉”“今天我们来说说”；
- 短句为主，术语必须解释或类比；
- 背景穿插，不单独堆科普；
- 把抽象信息翻译成观众能感知的影响；
- 结尾可以直接收束，或抛问题引导评论；
- 旁白稿只服务 TTS；后续字幕不得用它修正、对齐或覆盖 ASR 文本。

## 4. 初始化与模型调用

```bash
SKILL=/Users/amlei/Data/codespaces/projects/amlei-skills/skills/amlei-info-video

python3 "$SKILL/scripts/info_video.py" init \
  --slug "<slug>" --out "<输出根目录>" --title "<项目标题>"

python3 "$SKILL/scripts/info_video.py" narration \
  --project "<项目目录>"
```

TTS 按大段切分，不逐句生成；默认每段上限 420 字：

```bash
python3 "$SKILL/scripts/info_video.py" tts \
  --project "<项目目录>" \
  --model qwen-audio-3.1-tts-flash \
  --voice Cherry \
  --chunk-chars 420
```

ASR 使用线上 filetrans 盲转写；优先直接传入 TTS 返回的音频 URL：

```bash
python3 "$SKILL/scripts/info_video.py" asr \
  --project "<项目目录>" \
  --model qwen-audio-3.1-asr-flash-filetrans \
  --language zh
```

ASR 只负责文本和时间轴。不要把旁白稿传给 ASR 提示词，也不要用旁白稿修正 ASR 输出。

## 5. 盲字幕

```bash
python3 "$SKILL/scripts/info_video.py" cues \
  --project "<项目目录>" \
  --model qwen-audio-3.1-asr-flash-filetrans
```

生成：

- `06_subtitles/blind_cues.json`
- `06_subtitles/subtitles.md`

规则：

- 字幕文本和时间轴来自 ASR；
- 每条 cue 说完整一句或完整语义段；
- 中文约 16 字/行，最多 3 行；
- 不截断英文单词；
- 不用黑色字幕底；
- cue 不重叠、不倒退。

## 6. 素材池与画面

先下载素材到 `03_materials/`，并在 `material_list.md` 记录来源、链接、时间区间、主体和风险。可用 `yt-dlp`：

```bash
yt-dlp -f "bv*[height<=1080]+ba/b[height<=1080]" \
  --merge-output-format mp4 \
  -o "03_materials/<source>.mp4" "<URL>"
```

编辑 `03_materials/visual_pool.json`，给每个 source 提供：

```json
{
  "id": "SOURCE_01",
  "file": "/absolute/path/source.mp4",
  "duration": 215.64,
  "crop": [1138, 640, 400, 100],
  "scenes": [
    {"start": 40.0, "end": 48.0, "tags": ["产品界面", "发布现场"], "clean": true}
  ]
}
```

规则：

- 视频片段为主，图片、截图、图表只点缀；
- 有多个主体时，优先找相关主体同框或同场景；
- 不重复同一画面区间；
- 裁掉原视频字幕、台标和滚动条；
- 不用儿童正脸；
- 9:16 内主体不拉伸：原比例前景 + 同素材毛玻璃背景；
- 背景透明度按 30% 透明处理；
- 镜头直接硬切，不加黑场或淡入淡出。

生成场景计划：

```bash
python3 "$SKILL/scripts/info_video.py" plan \
  --project "<项目目录>" \
  --pool "<项目目录>/03_materials/visual_pool.json" \
  --cover "<项目目录>/cover.png"
```

## 7. 合成

```bash
python3 "$SKILL/scripts/info_video.py" build \
  --project "<项目目录>" \
  --pool "<项目目录>/03_materials/visual_pool.json" \
  --watermark-text "<用户确认的水印文本>"
```

水印文本必须先问用户。没有用户明确提供的水印文本时，不加水印。

音频加速与混流：

```bash
python3 "$SKILL/scripts/info_video.py" package \
  --project "<项目目录>" \
  --audio "<final_voice.m4a>" \
  --speed 1.06
```

## 8. QC

```bash
python3 "$SKILL/scripts/info_video.py" qc \
  --project "<项目目录>" \
  --final "<项目目录>/07_final/成片_1080x1920.mp4"
```

必须检查：

- STT 回听旁白；
- 抽帧检查字幕、水印、素材；
- 无重复素材区间；
- 无黑场；
- 无原视频字幕/台标遮挡主体；
- 无儿童正脸；
- 无拉伸；
- 1080x1920 正式版和 720p 预览都存在；
- 封面大字清晰。
