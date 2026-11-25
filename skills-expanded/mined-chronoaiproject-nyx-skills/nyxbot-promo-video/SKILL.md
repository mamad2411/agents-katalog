---
name: nyxbot-promo-video
description: "为 ChronoAI / NyxBot 的中小企业客户（餐馆、招牌店等）做 45–65 秒、抓人的中文宣传视频：读客户人物志和方案页，产出逐帧可控的 HTML 动画影片、按配音时段压低的原创配乐、配音稿与字幕（SRT），并渲染 MP4；配音由用户在第三方平台生成。当用户要给某个客户做 NyxBot 宣传片、按人物志和方案做视频、出配音稿或按中文配音调整画面节奏时使用。"
version: "0.1"
compatibility: "Python 3.10+ (numpy, scipy, pillow), ffmpeg; Chromium + Playwright for screenshots and video rendering"
metadata:
  category: mixed
  output-type: file
  runtime: [python]
  runtime-dependency: [numpy, scipy, pillow, playwright]
  tool-list: [Bash, Read, Write, Edit]
  tag: [video, nyxbot, promo, voiceover, chinese]
---

# NyxBot 客户宣传片

做一条给**某一位老板本人**看的短片：开头先让他点头（"这就是我"），再让他憋屈（他真实的痛），再让他扬眉吐气（NyxBot 现在就能做的事），最后用一句口号和零风险的试用条件收尾。

参考成片：`assets/examples/forest-media-v5/`。这是 Forest Media（招牌店，白老板）的 62 秒版本，市场总监已认可。新片子都从它复制出来改。

## 先读这些
| 文件 | 什么时候读 |
|---|---|
| `references/method.md` | **一定要先读。** 故事结构、怎么从人物志挑痛点、配音写法、哪些话不能说 |
| `references/design.md` | 写画面之前读：NyxID 设计语言、色板、字号、版式 |
| `references/engine.md` | 改 `film.html` 之前读：`seek(t)` 动画引擎、场景写法、时间对齐 |
| `references/audio.md` | 写 `timeline.json` 之前读：配乐段落、重音、音效、配音压低 |
| `references/lessons.md` | 交付之前读：踩过的坑和验收清单 |
| `assets/examples/forest-media-v5/README.md` | 参考案例：人物志怎么变成镜头和台词 |

## 流程

1. **检查环境。** 运行 `python3 scripts/check_env.py`，看哪些步骤能在当前沙盒里跑。
   - 没有 Chromium / Playwright 时，照样产出 `film.html`、配乐、配音稿，最后附上本机一键渲染命令。
   - 不要假装渲染过。
2. **读材料。** 读人物志和方案页，按 `method.md` 填"素材表"：
   - 他的作品或骄傲是什么；
   - 他的真实痛点（用他自己的原话）；
   - 现在**已经开通**的服务、**下一步**才开通的服务；
   - 价格条款；
   - 不能说的话。
3. **写配音稿和时间表。** 先写台词，再排时间：
   - 每句一个时段；
   - 中文约每秒 4 个字；
   - 句与句之间至少空 0.3 秒；
   - 重音（高潮、闪白）放在某个关键词说出的瞬间。
   - 写进 `timeline.json`（格式见 `audio.md`），然后运行 `python3 scripts/make_vo_script.py timeline.json out/ 客户名-v1`，它会检查语速。
4. **做画面。**
   - 复制 `assets/examples/forest-media-v5/` 到新目录。
   - 把 `film.html` 里的字体路径 `../../fonts/` 改成新位置，或者把 `assets/fonts` 一起复制过去。
   - 按 `engine.md` 改场景、文字和时间点。
   - **画面时间必须和 `timeline.json` 的配音时段对齐。**
5. **截图自查。**
   - 运行 `python3 scripts/shot.py film.html shots 2 6 10 …`，每个场景至少截 1–2 张。
   - 再用 `python3 scripts/sheet.py shots/sheet.jpg shots/*.png` 拼成一张，亲眼看。
   - 查重叠、溢出、换行、空白、字太小；修完再截。
6. **做配乐。**
   - 运行 `python3 scripts/make_bed.py timeline.json bed_raw.wav`，再运行 `python3 scripts/master.py bed_raw.wav bed.wav -18`。
   - 输出 −18 LUFS 的音轨，每句配音的位置已经把音乐压低 7 dB。
7. **渲染。**
   - 运行 `python3 scripts/render_all.py film.html <秒数> bed.wav out/客户名-v1-待配音.mp4`。
   - 它会顺带生成 `_sheet.jpg`，每秒一格。整张看一遍再交付。
8. **交付四样东西：**
   - 待配音 MP4；
   - 配音稿 `.md`：每句的开始时间、最长时长、台词、语气提示；
   - 字幕 `.srt`：剪映之类可以按字幕生成配音；
   - 配乐音效 `.wav`：单独一轨。
   - 回复里直接贴出逐句配音稿（编号、开始、最长、台词），方便复制。
   - 告诉用户：配音生成后把 01–NN 的音频发回来，可以按实际长度微调画面并混音出成片。
9. **收到配音后做混音。**
   - 用每段音频的实际长度更新 `timeline.json` 里的 `vo` 时段，同步改画面时间。
   - 重新生成配乐。
   - 用 ffmpeg 把配音按开始时间叠上去，母带做到 −14 LUFS、真峰值 ≤ −1.5 dBTP。

## 硬规则
- **只讲已经开通的服务**，例如听电话、做官网；还没开通的只能作为"下一步 · 即将开通"出现一次，例如信息回复。
- **不替老板报价。** NyxBot 收集尺寸、地点、需求；价格、做法、日期等他一句话。
- 对老板**不说 "AI"、"API"、"自动报价"**。不承诺还没开通的渠道，例如 WhatsApp。
- 画面里的来电、客人、对话、价格都是示例，**右下角一直挂"演示 · …为示例"**。电话号码要编，域名标"示意"。
- 客户的真实照片只用他自己的作品照。对外公开前提醒用户先征得客户同意。
- 人物志里的私人信息不进画面：年龄、证件、家人。
- 用户指定的开头、口号、出场顺序，**一字不改地照做**。需要断句时只加标点，并在回复里说明。
