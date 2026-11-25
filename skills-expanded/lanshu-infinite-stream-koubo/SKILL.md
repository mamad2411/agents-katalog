---
name: lanshu-infinite-stream-koubo
description: >-
  高级无限流 / Advanced Infinite Stream — 数字人口播（talking-head）生产技能：底板只生成一次，切成带标签的镜头单元，
  按脚本像写代码一样装配（换镜头、推近、画中画、隐藏、重排、MG 动效），只把主播可见的片段送去口型模型（中文口型一等公民），
  QC 后多画幅导出，用轮换账本和月度换新把“无限复用”变成低成本长期复用。
  Use when the user wants digital-human / AI-presenter koubo videos (30 s – 10 min, Chinese or bilingual) built from reusable
  generated or filmed plates; when they ask for plate prompts (30 s / 60 s, natural on-camera openings), shot slicing and tagging,
  script-driven or programmatic assembly, lip-sync routing, multi-aspect export, or the cost model of “generate once, remix forever”.
  Not for full-body acting, multi-person scenes, product handling or strong emotion — route those to full generation or live shooting.
---

# 岚叔无限流 · Lanshu Infinite Stream Koubo

**一句话：** 主播的“表演”只买一次，之后每条视频只花“嘴”和“剪”的钱；剪辑由脚本驱动、像代码一样可改、每一步都有标签和 QC 兜底。

本技能建立在本项目已有成果之上，不推翻它们：
- 可行性结论：GO/NO-GO 边界、成本模型、Phase 0 评分卡已归纳在本技能第 1、9 节。
- `prompts/plates-source.md`：K01–K03 定稿提示词、回位姿势切点 0.5/7.5/14.5/21.5/29.0。`prompts/library.json` 逐字复刻它们（`istream prompts verify` 校验）。
- Glass Protocol 动效包（`recipes/demo60/mg/`）：MG 叠加的设计语言和素材。演示里直接复用了其中 16 组 PNG 卡。

```
① 生成底板 ──► ② 切片打标 ──► ③ 写稿标记 ──► ④ 脚本驱动规划 ──► ⑤ 像改代码一样改
   prompts/       slice + review      script.md        plan + qc            edit ops + qc
                                                              │
⑨ 导出 + 记账 ◄── ⑧ QC ◄── ⑦ 合成（空间操作 + MG + 字幕 + 配音）◄── ⑥ 口型（只送可见段）
   ledger           qc         render --stage composite                lipsync plan / run
```

**铁律（全技能通用）**
1. **配音锁时间：** 时间轴的录制时间由配音决定。编辑只改“每个槽位放什么、怎么放”，永远不挪语音。
2. **先时间、再口型、后空间：** 裁剪 / 倒放 / 变速在口型之前，推近 / 裁画幅 / 画中画 / 隐藏在口型之后。口型模型要拿到最高分辨率、单张脸的主播画面。
3. **标签是契约：** 规划器、QC、口型路由、成本只读标签，不靠猜。标签有来源（`spec` 预期 / `measured` 测得 / `reviewed` 复核），`spec` 标签在底板生成后必须复核。
4. **可见才对口型：** 主播被 B-roll 或卡片盖住的时段不送口型模型；小脸（画中画）走快模型，大脸 / 重音走 pro 模型。
5. **开场主播要“到场”：** 第一镜必须是主播全画面；有开场专用镜头时，配音自动延后，让她先抬眼、转身或前倾“到场”，再开口。

---

## 0. 速查：每个阶段一条命令

在本目录运行。核心模块只用 Python 标准库，渲染需要 ffmpeg ≥ 7，切片需要 numpy（OpenCV 可选）。

| 阶段 | 命令 | 产物 |
|---|---|---|
| 用户照片→数字人 | `python3 -m istream identity set --photo me.jpg [--id SLUG] [--name …] [--outfit …] [--describe …]` | 锁定身份 + `prompts/GENERATE_PACK.md`（元视频提示词一站包） |
| 查看/恢复身份 | `python3 -m istream identity show` · `identity restore` | 当前身份块；恢复定稿形象（`prompts verify` 再过） |
| 生成提示词 | `python3 -m istream prompts build` | `prompts/PROMPT_LIBRARY.md`、`prompts/prompts-only.txt` |
| 去AI味叠加 | `python3 -m istream prompts overlay --plate K01 --lang both --negative` | 复制时叠加真人感补丁（不改定稿） |
| 月度换新 | `python3 -m istream prompts refresh --n 4 --framing mcu --seed 202611` | 新底板 R01… 的提示词 + 预期标签 |
| 预期标签目录 | `python3 -m istream catalog build-spec --out catalog/spec` | `plates.json` + `shots.json`（provenance=spec） |
| 切片打标 | `python3 -m istream slice plate.mp4 --id P01 --out drafts/P01.json --sheet drafts/P01.jpg` | 测得的切点 / 人脸 / 缺陷 + 复核用联系表 |
| 合并复核 | `python3 -m istream catalog merge-review --draft drafts/*.json --review review.json --out catalog/x` | 正式目录（provenance=reviewed） |
| 规划 | `python3 -m istream plan script.md --cat catalog/x/plates.json [--align align.json] [--aspect 9:16] [--seed 7] --out timeline.json` | 时间轴 JSON + 可读表 |
| 改片 | `python3 -m istream edit timeline.json --cat … --ops-file my.ops --out timeline2.json` | 新时间轴 + diff |
| QC | `python3 -m istream qc timeline.json --cat …` | PASS/FAIL + RISK/WARN 清单 |
| 口型任务 | `python3 -m istream lipsync plan timeline.json --cat … [--policy p.json] --out jobs.json` | 分段口型任务 + 中文口型风险 |
| 渲染 | `python3 -m istream render timeline.json --cat … --jobs jobs.json --workdir build --out final.mp4 [--engine passthrough] [--scale 0.5]` | A 口型输入 → B 口型 → C 合成 |
| 成本 | `python3 -m istream cost timeline.json --cat … --jobs jobs.json --lifetime 300` | 本条视频 / 每成片分钟成本 |
| 记账 | `python3 -m istream ledger record timeline.json --ledger ledger.json` | 镜头曝光次数 → 疲劳惩罚 / 退役候选 |
| 全流程复现 | `bash tools/run_demo.sh` | 本包所有产物 + 测试 |

---

## 1. 先判断能不能用（GO / NO-GO）

沿用可行性报告的结论，不重复论证：

- ✅ **GO：** 口播、讲解、课程、产品介绍。正面 ±20°，近景 / 中景，手势温和。
- ⚠️ **部分：** 强情绪、动作必须对上台词意思。用标签选片（情绪 / 手势 / 关键词对齐）+ B-roll 缓解，做不到逐字精确。
- ❌ **NO-GO：** 全身走动、与物体互动、多人、带货演示、大笑大哭。改用全量生成或实拍。
- **“无限”的真实含义：** 低成本长期复用 + 每月补 4–6 条新底板。轮换账本（第 9 节）告诉你哪些镜头该退役了。
- **先算账再自建：** 本人出镜、每月成片少于约 60 分钟，先试一周现成数字分身服务（约 $1–1.5/分钟）当基准。原创虚拟形象、多品牌、要统一高级审美、或月产量大，才值得用本技能自建。
- **Phase 0（1–2 天，< $100）必须先过：** 3 条底板 × 2 个口型引擎 × 3 段中文音频（含绕口令）。按可行性报告 §7.1 的评分卡打分：平均 ≥ 4，单项无 ≤ 2，且 5 人盲测中至少 3 人没指出“嘴不对”。

---

## 2. 阶段一 · 生成底板（Generate）

### 2.0 用户照片 → 数字人元视频（先做这一步）

**正确顺序：先生成无遮挡、可无限复用的口播元视频（底板），再切片、再写稿装配。** 不要先剪片再回头找底板。

```bash
# 1) 上传自己的照片，锁定数字人身份（会改 blocks.identity + 首帧图 Subject，并写出 GENERATE_PACK）
python3 -m istream identity set --photo /path/to/me.jpg --id liz --name Liz \
  --outfit "solid navy blazer over a plain white crew-neck top" \
  --describe "optional short appearance lock — only what you type; no auto face analysis"

# 2) 打开一站式生成包，复制 K01 / K02 / O01 中英提示词去视频模型
#    prompts/GENERATE_PACK.md
#    （完整库仍见 prompts/PROMPT_LIBRARY.md）

# 3) 按包内清单生成：挂上同一张参考图、≥1080p、25fps、静音模型音频、无遮挡
# 4) 入库切片 → 再 plan / edit / lipsync
python3 -m istream slice K01.mp4 --id K01 --out drafts/K01.json
```

| 要点 | 说明 |
|---|---|
| **无遮挡** | 脸/嘴全程可见：手不挡脸、无道具挡嘴、纯净背景。Avoid / Negative 里已写死，生成时仍要盯。 |
| **GENERATE_PACK.md** | 操作清单 + 负面词 + 首帧图 + **K01/K02/O01** 完整中英 Master Prompt，复制即用。 |
| **外貌锁定** | `--describe` / `--outfit` / `--name` 才会写进提示词；**不会**自动读图认脸。 |
| **frozen verify** | 换身份后 `prompts verify` 会对不上定稿，属预期；`identity restore` 可恢复包内默认形象。 |
| **手改 JSON** | 仍可只改 `blocks.identity` 再 `prompts build`；有照片时优先走 `identity set`。 |

详见 `docs/USER_PHOTO.md`。

### 2.1 锁定段（同一套库内一字不改）
身份、服装、灯光、背景、机位、回位姿势。提示词由积木拼成：

```
锁定行(时长/画幅/景别) + 身份 + 场景与光线 + 表演 + 时间线 + 避免
```

`prompts/library.json` 是唯一来源。**有照片时用 `identity set`（推荐）**；也可手改 `blocks.identity` 一处再 `prompts build`，全库提示词同步换人。默认形象下 K01–K03 与定稿逐字一致（`prompts verify`）。

### 2.2 底板组合（按发布频率选）

| 档位 | 底板 | 总时长 | 一次性生成成本* | 适合 |
|---|---|---|---|---|
| 起步 | K01 | 30 s | $10–21 | Phase 0、每周 ≤ 2 条 |
| 标准（推荐） | K01 + K02 + O01 | 90 s | $29–63 | 每周 2–4 条，60–90 s 口播 |
| 进阶 | 标准 + K03 + L01 + L02 + K01H | 270 s | $86–189 | 日更、3–10 分钟长视频、横竖双版 |

\* 按 $0.08–0.14/秒 × 每条抽 4–5 次估算（2026-10 公开价，落地前请核实）。

**底板说明（完整提示词见 `prompts/PROMPT_LIBRARY.md`）：**
- **K01 / K02 / K03：** 定稿 30 s。K01 近景主力，K02 中景手势，K03 近景变体。
- **K04 / K05（v1.3，叠加层定义，待验证）：** K04 中景手势密集（递出 / 对比 / 节拍点 / 耸肩），K05 近景表情密集（思考 / 皱眉 / 轻笑 / 倾听）。用 `prompts overlay --plate K04 --gesture` 取提示词，见 §2.6。
- **K01H：** K01 的 16:9 孪生版，主播在左三分之一，右半边留给图形。用于横屏“主播 + 内容区”分屏，也能裁成 9:16。
- **L01 / L02：** 60 s 长底板，各 8 段且段段不同。L02 含“掌心向画面右 / 左托举”两段，MG 可以“放在她手上”。不支持 60 s 的模型用“接力 A / B”两段各 30 s 生成，接力点在 28–31 s 的回位静止段。
- **O01 开场入镜：** 一条 30 s 里有 4 种自然开场：抬眼入镜、回身入镜、前倾入镜、静场开口。前三个镜头从“准备动作”中间切入，第一帧主播就已经在场。它们标了 `position: first_only` 和 `speech_offset`，规划器会自动把配音延后 1–1.6 s。

### 2.3 生成设置与入库验收
- 同一模型和版本。1080p 起，能更高就更高：要做 112–125% 推近或 16:9→9:16 裁切，就必须有像素余量，QC 的 `upscale` 检查会报出来。
- 统一帧率（优先 25fps）。挂同一张身份参考图，用 IMG-A / IMG-B / IMG-A169 作首帧，支持尾帧就同图首尾。模型自带音频一律静音。
- 每条抽 4–5 次，挑最好的一条入库。

**入库验收清单：**
1. 和参考图是同一个人。
2. 回位静止出现在 0 / 7 / 14 / 21 / 28 s 附近（±0.5 s）。
3. 手不过胸、不碰脸。
4. 闭嘴段确实闭嘴。
5. 光线、色温稳定。
6. 无文字、无多余人物、无镜头漂移。

### 2.4 命名与目录（沿用可行性报告 §7.4–7.5，加上本技能的产物）

```
{身份}_{服装}_{景别}_{画幅}_{动作}_{能量}_{时长}_v{版本}.mov   例：liz01_o1_mcu_916_koubo-main_mid_30s_v01.mov
镜头单元 ID：{底板代号}_s{序号}                                  例：K01_s3、P01_s2
dh-library/
├── 00_identity/      参考图、首帧图、声音样本、授权文件
├── 01_plates_raw/    生成 / 拍摄原片（只读）
├── 02_plates_master/ 母版（稳定、调色、超分）
├── 06_metadata/      plates.json · shots.json · review.json · ledger.json   ← istream 目录
├── 07_projects/2026-11-03_topic/
│   ├── script.md  align.json  vo.wav
│   ├── timeline.json  jobs.json  qc.txt  cost.txt
│   └── build/ (lipsync/in · lipsync/out · segments 缓存)  export/
└── 08_qc/            评分卡、问题记录
```

### 2.5 真人感与高级感（去 AI 味）

一句话目标：像布光讲究的**真人访谈**；生气来自微行为，不来自大动作；底板无遮挡 / 回位纪律不变。细则与可复制补丁见 `docs/HUMAN_PREMIUM.md`。

**P0（不做就会有 AI 味）：** 真皮肤（毛孔 / 绒毛 / 非油亮）· 静止时仍呼吸眨眼（不是定格）· 会思考的眼睛（不规律眨眼、同侧眼神光）· 动作由语言驱动（绝非节拍器点头）· 主补光约 3:1、墙面有减光空间 · 等效 85mm / ~f/2.8、焦点在眼睛 · 首帧与参考照决定一半（拒美颜自拍）。

**怎么用（不改定稿库）：**
```bash
python3 -m istream prompts overlay --plate K01 --lang both --negative
# 字数紧：加 --compact；要气质句：加 --style
```
数据源：`prompts/overlays/human_premium.json`。`prompts verify` 仍对 K01–K03 定稿逐字通过。口型后可 `render --grain 2–4` 统一细颗粒。

**入库：** `HUMAN_PREMIUM.md` §5 的 10 项是/否，≥9 通过；身份不一致或底板纪律（手挡脸等）一票否决。参考照规则见同文档 §4；禁止清单见 §6。

**验证：** Phase 0 A/B（基础版 vs overlay）按文档 §8；未跑通前叠加层标「待验证」，不要当已证明默认。

### 2.6 手势与表情词表

一句话目标：底板里的人在**交流**，不只是“活着”。手势是访谈主持人的对话手势，不是短视频舞蹈或舞台表演。硬规则不变：嘴不被挡、手不碰脸、切点回位、±20°。词表、例时间线和补丁原文见 `docs/GESTURE_EXPRESSION.md`（全部 待验证）。

**表情 E01–E10（近景、中景通用）：** 浅笑承接 · 认同点头 · 思考一瞥 · 扬眉点题 · 轻皱眉 · 轻笑后收 · 倾听脸 · 笃定收句 · 共情柔和 · 会心一笑。表情小、短、略不对称，峰值约 0.5–1.5 s 后回到中性脸。

**手势 G01–G11（只用于中景）：** 摊手讲解 · 单手递出 · 两手对比 · 计数（高风险，默认用节拍点 + 字幕 ①②③ 代替）· 节拍点 · 合手收束 · 轻耸肩 · 比划大小 · 手按胸口 · 侧向引导 · 指尖相触。
- **语法：** 回位 → 手势 → 回位，约 2 s；腰到胸口略低处；单手为主、两手不镜像；每段最多两个。
- **禁止：** 指镜头、OK / 比耶 / 点赞、挥手、抱臂、道具。
- **近景（K01 / K03 / K05 / O01）：** 手不入画，只用表情。

**怎么用（不改定稿库）：**
```bash
python3 -m istream prompts overlay --plate K02 --lang both --negative --gesture   # 真人感 + 手势表情
python3 -m istream prompts overlay --plate K04 --lang zh --negative --gesture     # 新：中景手势密集（K05 = 近景表情密集）
python3 -m istream catalog build-spec --overlay gesture_expression --out catalog/gesture
```
数据源是 `prompts/overlays/gesture_expression.json`；K04 / K05 只在叠加层里，`prompts verify` 照常通过。

**脚本：**
- 新意图：`[认同] [对比] [提醒]/[转折] [思考] [共情]`。
- 点名：`[手势: 对比]`、`[表情: 浅笑+扬眉]`，规划器会优先选带这个标签的镜头，选不到会给出警告。
- 不用这些标记的老脚本，结果逐字节不变。

**入库：** HUMAN_PREMIUM 10 项 + GE1–GE8；GE2（手过胸 / 近脸）和 GE7（手势梗）一票否决。全部通过才打新的表情 / 手势标签。


---

## 3. 阶段二 · 切片打标（Slice + Tag）

```bash
python3 -m istream slice plate.mp4 --id P01 --out drafts/P01.json --sheet drafts/P01_sheet.jpg
```

**机器测得（`measured`）：**
- **硬切：** 左右两半同时剧变。
- **叠化：** 两半同时持续升高，且两半的边缘密度对调（机位换了）。
- **烧录图形：** 只有一半的边缘密度离开本机位基线。如果那块区域大部分是皮肤，就判为手势（例如托举），不是缺陷。
- **回位 / 低运动静止段**、说话停顿（静音检测）。
- **人脸框和脸高：** 肤色启发式，可换 YuNet 等人脸检测。
- **其他：** 手是否靠近脸、语音占比、能量。

**需要复核的语义标签：** 情绪、手势名、角色（roles）、可否倒放。把联系表（每镜 3 帧）和测量值交给 VLM（提示词在 `PROMPT_LIBRARY.md` §6，枚举值由词表生成），或人工写进 `review.json`，再 `catalog merge-review`。抽查 20%。

### 3.1 标签 schema（完整枚举见 `schema/TAGS.md`，JSON Schema 见 `schema/shot.schema.json`）

| 字段 | 例 | 谁在用 |
|---|---|---|
| `src.in/out`、`home_in/out`、`edit.cut_points` | 回位静止点 | 规划器选入点；无缝拼接 |
| `camera.framing / aspect / subject_pos / face_box / face_h_px` | mcu · 16:9 · left · 脸框 · 184px | 裁画幅、推近锚点、口型路由、`upscale` 检查 |
| `performance.energy / emotion / mouth / hands / gaze / head_motion` | 3 · warm · talking · chest | 角色匹配、闭嘴段、排除手近脸 |
| `performance.gestures[{g, t, zone}]` | palm_present @2.35s · right_half | 手势峰值对准关键词；MG 放在掌心 |
| `edit.roles` | open / hook / explain / emphasis / list / data / question / summary / cta … | 脚本角色 → 镜头 |
| `edit.layouts / transitions_in / position` | full · split · pip ／ first_only | 版式、转场、开场专用 |
| `edit.scale_max / reversible / keep_out / speech_offset` | 1.25 · good · [[1.5,4.5]] · 1.6 | 推近上限、倒放变体、不在手势中间切、开场延迟 |
| `mg.safe_zones` | right_half · upper_band · lower_third | MG 放哪里不挡人 |
| `lipsync.ready / jaw / second_face` | true · mid · true（玻璃倒影） | 口型可否、锁定主脸 |
| `quality.qc / defects[{type,in,out,zone}]` | baked_overlay · right_half | 只有能被裁掉的缺陷才允许用 |
| `usage` / `ledger.json` | 曝光次数、最后使用 | 疲劳惩罚、退役 |

### 3.2 打标规则（直接影响成片）
- 手靠近脸 → `hands: near_face`，永远不进自动装配。
- 画面里有第二张脸（倒影、海报）→ `lipsync.second_face: true`，口型任务带 `face_lock` 框。
- 缺陷尽量标上 `zone`。例如“右半区烧录乱码”在 9:16 裁人物时仍可用，演示里 P02_s4/s5 因此在竖版里复活。
- 手势进行中的区间写进 `keep_out`，规划器不在手势中间切。
- 开场镜头写 `position: first_only` + `speech_offset`（开口前的在场秒数）。

---

## 4. 阶段三 · 脚本驱动装配（Plan）

### 4.1 稿件标记（`script.md`）

```markdown
---
title: …
aspect: 16:9          # 或 9:16 / 1:1
profile: short        # short ≤ 2 min / long 3–10 min / 省略则按时长自动
vo: vo.m4a            # 配音；没有就按 rate 估算时间
mg_library: mg_library.json
---
# 第一讲 · AI Native                      ← 章节（长视频自动加章节卡 + MG 擦除转场）
[开场][钩子][MG: an_hook] 全员都开了AI账号，效率怎么还原地踏步？
[故事][B-roll: 车间俯拍] 直到有人给每台机器配上小电机……   ← 主播隐藏，配音继续
[强调][重音: 打字机] AI也一样，塞进旧流程，它只是台更快的打字机。   ← 在“打字机”上推近
[列点] ①…②…③…                          ← 自动识别列点
[停顿 0.6]                                ← 句后静场
```

**标签表：**
- **角色：** `[开场] [钩子] [解释] [故事] [列点] [数据] [提问] [强调]/[金句] [总结] [过渡] [结尾] [关注]`，v1.3 新增 `[认同] [对比] [提醒]/[转折]/[注意] [思考] [共情]`（只在显式标记时生效）。不写会按句式推断：首句 = hook，问号 = question，数字 = data，“因为” = explain，“才叫 / 记住 / 一句话” = emphasis，末句含“关注” = cta。
- **版式提示：** `[主播] [推近] [画中画] [隐藏] [切]`。
- **内容：** `[B-roll: …] [MG: id] [重音: 词] [停顿 秒]`。
- **手势 / 表情（v1.3）：** `[手势: 对比]`、`[表情: 浅笑+扬眉]`。可以写中文名、E01–E10 / G01–G11 或 vocab 键，见 §2.6。

### 4.2 时间
- **有配音时：** 给 `align.json`（逐句 start/end，可带关键词 `keys`）。TTS 或 ASR 的时间戳导出就是这个格式（见 `recipes/demo60/align.json`）。
- **没有配音时：** 按 `rate` 字/秒估算（默认 5.0），适合先出方案和动态分镜。

### 4.3 决策规则（规划器就是这么做的，人工剪也照这个做）

**1. 句子 → 版式：**

| 情况 | 版式 |
|---|---|
| 首句 | `full`（主播必须到场） |
| 有 `[B-roll]` | `hidden` |
| 列点 / 数据 | `split`（主播 + 内容区） |
| 强调 / 提问 | `punch`（推近，落在 `[重音]` 那个字上） |
| 其他 | `full` |

**2. 覆盖率平衡：** 被内容盖住的比例（hidden + pip）达不到档位下限时，把最长的叙述 / 解释 / 故事句改成“内容主导 + 主播画中画”。short 档 15–35%，long 档 25–40%。

**3. 切槽：**
- 在下一句开口前 2 帧切（J-cut 感）。
- 强调句在关键词起点切进推近。
- 同版式的短句合并，但带关键词的强调 / 钩子 / 数据句单独成槽，给手势对齐留空间。
- 超长槽拆成跳切（short 槽长 1.6–4.2 s，long 3–7.5 s）。

**4. 选镜顺序：** 最受约束的槽先选（候选最少的先挑，带关键词的优先），而不是从左到右。招牌镜头（例如掌心托举）因此留给最需要它的那句。

**5. 硬过滤：**
- 说话槽只要 `talking` 且口型可用的镜头。
- 手近脸、qc < 3 排除。
- 画幅不合且裁不出来的排除。
- MG 要的半区必须在 `safe_zones` 里。
- 开场专用镜头只能做第一镜。

**6. 打分：**

| 项 | 分 |
|---|---|
| 角色匹配 | +3 |
| 情绪匹配 | +1.5 |
| 意图偏好标签（只对 v1.3 新 role）/ 点名的 `[手势]` `[表情]` | +0.8 / +2.0 |
| 能量差每级 | −0.8 |
| 与相邻镜头机位 / 景别不同 | +0.5 |
| 与相邻同一镜头 | −5 |
| 本片已用每次 | −1 |
| 账本疲劳 | −0.5·ln(1+n)，近 2 天用过再 −1.5 |
| 推近超上限 | −3 |
| 需要放大超过 1.6× | −0.6~−2 |
| 种子噪声 | ±0.3 |

**7. 选入点（窗口）：**
- 落在回位点 +0.8；开场从底板起点入 +1。
- 跨手势 `keep_out` −2。
- 手势峰值离关键词每 0.1 s 少 0.2 分（满分 +2）。
- 窗口碰到缺陷时，只有裁画幅能裁掉才可用。
- 同一时刻 12 s 内不许再出现；更远的重复 −3，并且必须做成不同变体。

**8. 变体与跳切：**
- 再次使用同一时刻时，必须换缩放（1.0 / 1.10 / scale_max）或倒放。
- 同底板相邻两镜，缩放差必须 ≥ 8%，否则读起来像“跳帧”。

**9. 供给放宽：** 素材里没有能让出某个半区的新镜头时，该槽自动改成画中画，并提示“补一条那一侧空着的底板”。

**10. 转场：**
- 主播 ↔ 主播：`cut` / `zoomcut`。**两个说话的脸之间永远不叠化**（双脸会让口型失效）。
- 主播 ↔ B-roll / 卡片：4–8 帧淡化。
- 长视频章节：MG 擦除。

**11. MG：** 脚本 `[MG: id]` 或按角色自动出模板（列点 / 计数 / 提问 / 关键词 / 关注）。区域按画幅取。尾巴在下一句前收掉，防止跨到不让位的镜头上。

**12. 开场到场：** 目录里有 `first_only` 镜头时，配音整体延后（最大 `speech_offset` − 首句起点），第一镜必选开场专用镜头。

**13. 种子：** 同脚本、同目录、同种子，结果完全一致；换种子得到另一版合法剪辑（演示：seed 7 → 11 有 5/21 个镜头不同，QC 仍通过）。可用于 A/B 测试或多账号分发。

### 4.4 档位参数

| 档 | 槽长 | 覆盖率 | 同镜不重复窗口 | 推近 | 交替缩放 | 章节卡 |
|---|---|---|---|---|---|---|
| short | 1.6–4.2 s | 15–35% | 45 s | 1.15 | 1.10 | — |
| long | 3–7.5 s | 25–40% | 100 s | 1.12 | 1.08 | 1.6 s |

---

## 5. 阶段四 · 像改代码一样改（Edit API）

配音锁定录制时间，所以所有操作都是“槽位内”的：换内容、换显示方式，不挪语音。

| 操作 | 语法 | 作用 | 守卫 |
|---|---|---|---|
| swap | `swap c05 K02_s1 [offset]` | 换镜头（默认从第一个放得下的回位点入） | 镜头必须够长；锁定的不能改 |
| punch / scale | `punch c07 1.15` | 推近 / 缩放（锚在脸上） | ≤ `scale_max` |
| crop | `crop c03 9:16 [cx]` | 裁画幅（默认跟脸） | — |
| pip | `pip c04 br 0.3` | 主播缩成画中画（scale down） | 需要有镜头 |
| hide / show | `hide c13 card`、`hide c07 broll:关键词`、`show c13 K01_s2` | 隐藏主播交给卡片 / B-roll；或恢复 | — |
| order | `order c02,c07,c20` | 这些槽位的镜头轮换（重排） | 长度要放得下 |
| split | `split c04 12.3` | 在 12.3 s 加一个跳切，后半自动换缩放 | 两边各 ≥ 0.8 s |
| reverse / speed | `reverse c06`、`speed c06 0.95` | 倒放变体 / 轻微变速 | 标签禁止倒放就拒绝；变速 0.85–1.15 |
| transition | `transition c06 zoomcut` | 指定转场 | — |
| mg / broll | `mg 26.1 28.7 keyword_pop lower_third 文案`、`broll 18 24 关键词` | 加动效 / 用 B-roll 盖住一段 | — |
| lock | `lock c01` | 之后的操作不能再改它 | — |

**Python 链式写法：** `tl.clip("c05").swap("K02_s1").punch(1.15)`

**推荐闭环：** 写 `.ops` 文件 → `istream edit`（打印 diff）→ `istream qc` → 修 → 再 QC → 渲染。渲染有内容哈希缓存，只重建改过的片段。

演示：6 个改动让 QC 抓到 4 个 FAIL（MG 被挡、同一画面 3.4 s 内重复、同变体重复 ×2），4 行修复后 PASS（`recipes/demo60/edit/`）。

---

## 6. 阶段五 · 口型（Lip-sync，一等公民）

### 6.1 为什么在“拼好的底板”上做，而且只做可见段
- 规划完成后，`lipsync plan` 把连续的“主播可见段”合成任务，B-roll / 卡片段直接跳过。
- 每个任务的输入，是只做了时间操作（裁剪 / 倒放 / 变速）的原分辨率主播画面，加上对应的配音切片。
- 引擎返回后，再做推近、裁画幅、画中画和 MG。因此口型模型永远拿到最大的那张脸，而且画面里没有字幕、没有 MG、没有第二个主播。

### 6.2 路由（`recipes/policies/*.json`，可改）

| 档 | 条件 | 默认引擎 |
|---|---|---|
| hero | 开场 / 钩子 / 强调 / 关注，或推近，或输出脸高 ≥ 300px | `sync-2-pro` |
| standard | 其余可见说话段 | `latentsync`（自部署） |
| small | 画中画，或输出脸高 < 160px | `musetalk`（快，256px 脸部区域，小脸看不出差别） |

合并相邻任务时，按秒数取主导档位（0.7 s 的推近不会把 10 s 任务整段升成 pro）。

### 6.3 引擎选项（2026-10 公开信息，价格以官网为准）

| 引擎 | 类型 | 模式 | 约价 / 分钟 | 中文要点 |
|---|---|---|---|---|
| sync lipsync-2-pro / lipsync-2 | 商用 API | 只换嘴 | $4–5 / $3 | Phase 0 必测快语速、闭唇音、英文字母夹杂 |
| 可灵对口型 | 商用 | 只换嘴 | 见控制台 | 中文数据充足，国内首选候选；注意单次时长上限 |
| HeyGen 数字分身（Avatar III 类） | 服务 | 底板 + 换嘴的产品化 | $1–1.5 | 需真人授权素材；本人出镜、低产量时最划算 |
| LatentSync | 开源 Apache-2.0 | 只换嘴，扩散模型 | GPU 约 $0.05–0.5 | 画质优先、较慢；中文需实测 |
| MuseTalk | 开源 | 只换嘴，接近实时 | GPU 约 $0.05–0.3 | 256px 脸部区域，适合小脸 / 画中画 |
| OmniHuman / InfiniteTalk / Avatar IV | 商用 / 开源 | **整段重演**（头身嘴全重做） | — | 不是复用路线；只给需要新动作的 hero 镜头 |
| Wav2Lip / VideoReTalking / SadTalker | 开源 | 老一代 | — | 只作对比基线 |

`istream lipsync run --engine passthrough` 可以直接跑通（不改嘴，只用于预览）。其他引擎在本包里是**模板适配器**：只打印要发出的请求或命令，拒绝伪造结果。接上真实引擎后，把结果放到任务的 `output` 路径，再跑 `render --stage composite`。

### 6.4 中文口型：必须单独对待
- **语速：**
  - ≤ 5.5 字/s 理想；> 6.0 记 WARN；> 6.6 记 RISK，必须逐帧复核或让 TTS 放慢 5–10%。
  - 演示里 MCP 段真人原声是 7.3–7.4 字/s，被准确标出。
  - 每个口型任务按重叠时长加权计算语速。
- **闭唇音 b/p/m：** 必须真正闭合。按密度报警（内置常用字表；装了 `pypinyin` 就精确计算）。
- **唇齿音 f：** 看上齿是否压下唇。
- **夹杂英文和缩写**（AI、MCP、USB-C、GitHub）：字母口型和汉字不同，单列出来人工看。
- **数字：** TTS 读“十 / 一百 / 10”的方式要和字幕一致。
- **停顿：** ≥ 0.8 s 的静场落在说话镜头里会记 WARN。要么确认引擎在静音时闭嘴，要么切到闭嘴倾听镜头（K01_s4、L01_s8）。
- **脸的大小：**
  - 1080 竖屏里脸高 300–500px 最好。
  - < 160px 走小脸档。
  - 推近不超过 `scale_max`（脸太大、嘴部分辨率不够会糊）。
- **遮挡与第二张脸：** 手近脸的镜头不进自动装配；有倒影的镜头带 `face_lock`。

### 6.5 口型之后（可选的“嘴部校准”）
- 嘴糊：在同一任务上换 pro 引擎重跑，比后期修复更稳。
- 表情微调：LivePortrait（开源）。
- 面部修复（GFPGAN / CodeFormer）：只用低强度，修完一定和身份参考图比对，过度修复会换脸。
- 复核：按可行性报告的评分卡（口型准确、嘴部清晰、身份、头身自然、接缝）。有条件可以加 SyncNet 类指标（LSE-C / LSE-D），本包未内置。

---

## 7. 阶段六 · 合成与“高级感”规则

**版式语法：**
- `full`：主播全画面，主力。
- `punch`：推近 112–125%，用于重音和金句。
- `split`：主播在一侧，内容区在另一侧（横屏左右分；竖屏上下分）。
- `pip`：内容主导，主播缩成圆形窗口，放在内容的对侧。
- `hidden`：主播隐藏，演播室虚化成背景，B-roll 或卡片在上，配音继续。

**节奏：**
- 短视频平均镜头长 2.2–3.8 s，长视频 3.5–7 s。
- 同底板跳切的缩放差 ≥ 8%。
- 在开口前 2 帧切，推近落在关键词上。
- 说话脸之间不叠化。
- B-roll 进出 4–8 帧淡化。

**裁 / 缩 / 藏：**
- 推近锚在脸上，不超过 `scale_max`。
- 竖版从横版裁时跟着脸框走，QC 会报放大倍数。
- 带缺陷的镜头只在“裁掉缺陷那一半”时使用。
- 被 MG 或 B-roll 盖住的时段不花口型的钱。

**MG 挂点：**
- `mg_library.json` 把 `[MG: id]` 映射到素材、区域、`at_keyword`（在重音词上出现）和预览文字。
- 横屏演示直接复用 Glass Protocol 的 PNG 卡。其他画幅回退为扁平预览卡。
- 正式的动态 MG（描边、粒子、玻璃模糊）用本项目 Glass Protocol 动效包的合成流程制作，本渲染器负责摆位、时间和淡入淡出。

**字幕：**
- ASS 格式，思源黑体 / Noto Sans CJK 粗体。
- 按宽度断行（拉丁字母算半格），不以标点开头，不留 1–2 字的孤字。
- 竖屏字幕放在平台按钮区以上。

---

## 8. 阶段七 · QC 与导出

**自动 QC（`istream qc`）：**

| 级别 | 含义 | 检查项 |
|---|---|---|
| **FAIL** | 必须改 | 覆盖缺口、开场主播不在、同一时刻 12 s 内重复或同变体 45 s 内重复、开场专用镜头用在中间、说话段用了不能对口型的镜头、手近脸、缺陷露出、推近超上限、倒放了禁止倒放的镜头、MG 挡人、两张说话的脸叠化 |
| **RISK** | 不阻断，口型后必须人工复核 | 中文语速 > 6.6 字/s |
| **WARN** | 进人工清单 | 语速 > 6.0、同底板同缩放跳切、长停顿落在说话镜头、远距离变体复用、节奏超档、覆盖率越界、输出脸 < 120px、放大 > 1.6× |

**人工复核（5–10 分钟）：** 手机竖屏、1 倍速看一遍，重点看 b/p/m、牙齿、接缝、身份、重复感，以及 RISK 段逐帧。

**导出：**
- 同一份脚本可以出多个画幅：`--aspect 16:9` 和 `--aspect 9:16` 各规划一次，裁切、MG 区域和可用镜头都会自动变。
- 按平台规定标注“AI 生成 / 数字人”；授权文件放 `00_identity/`。
- 发布后记账：`istream ledger record`。

---

## 9. 经济账（详见 ARCHITECTURE.md §4）

```
单条成本 = Σ 可见说话秒数 × 引擎单价 × 返工系数  +  底板一次性成本 ÷ 预计服务的成片分钟  （TTS 各路线都要，另计）
```

**演示实测（同一份时间轴，只换路由策略文件）：**

| 方案 | 默认混合 | 全自部署 | 全 pro | 不分段全 pro |
|---|---|---|---|---|
| 56 秒合集（替身底板） | $2.0–3.3 | $0.11–0.72 | $3.6–5.2 | $4.1–6.1 |
| 约 4 分钟长视频（规格目录） | $9.3–15.4（$2.4–4.0/分钟） | $1.3–4.9（$0.34–1.26/分钟） | $15.9–23.7 | $17.0–25.1 |

**对照（每成片分钟）：**
- 通用视频模型整段生成：$10–25
- 音频驱动数字人 SaaS：$5–8
- 现成数字分身服务：$1–1.5

**结论：**
- 自建 + 自部署口型，才能把边际成本压到 $1/分钟以下。
- 只用商用 pro 时，和 SaaS 价差不大。省钱的真正来源是可见段路由、小脸走快模型、剪辑全自动。

**账本：**
- 每次发布后把用过的镜头记进 `ledger.json`。
- 规划器按 0.5·ln(1+n) 加疲劳惩罚，近 2 天用过的再罚 1.5。
- 曝光超过阈值的镜头进退役名单。
- 月度换新（`prompts refresh`）从菜单里组合没用过的动作，生成新底板。

---

## 10. 本技能的文件

| 路径 | 内容 |
|---|---|
| `SKILL.md` | 本文件：阶段、命令、规则 |
| `ARCHITECTURE.md` | 为什么这样设计、成本模型、故障模式、升级路线 |
| `DEMO.md` | 一份脚本 → 时间轴 → QC → 口型任务 → 渲染 → 改片的完整实录 |
| `README.md` | 快速开始 |
| `istream/` | 工具包：vocab · schema · catalog · script · planner · timeline · qc · lipsync · render · cost · prompts · slicer · CLI |
| `schema/` | `shot.schema.json` · `timeline.schema.json` · `TAGS.md`（由词表生成） |
| `prompts/` | `library.json`（唯一来源）· `GENERATE_PACK.md` · `identity_default.json` · `identity/` · `PROMPT_LIBRARY.md` · `prompts-only.txt` · `refresh_example.json` · `overlays/`（`human_premium.json` · `gesture_expression.json`，复制时叠加） |
| `catalog/spec/` | 7 条底板（K01–K03 · K01H · L01 · L02 · O01）、36 个镜头的预期标签 |
| `catalog/gesture/` | v1.3：spec + 手势表情叠加层（打过补丁的 K01–K03 标签 + K04 / K05），9 条底板、44 个镜头 |
| `catalog/standin/` | 2 条真实替身底板（本项目原片）的切片草稿、复核与正式目录 |
| `recipes/demo60/` | 56 秒合集：脚本、对齐、MG 库、时间轴、QC、口型任务、成本、16:9 / 9:16 预览、改片演示 |
| `recipes/longform/` | 约 4 分钟长视频配方：脚本、时间轴、QC、口型任务、成本、占位动态分镜 |
| `recipes/gesture/` | v1.3 手势与表情配方：新意图 / `[手势]` `[表情]` 标记 → 规划 + QC（不出片） |
| `recipes/policies/` | 口型路由策略：默认混合 / 全自部署 / 全 pro |
| `docs/` | `USER_PHOTO.md` · `HUMAN_PREMIUM.md` · `GESTURE_EXPRESSION.md` · `SKILL_2_6_OUTLINE.md`；渲染与切片的联系表 |
| `tools/` | `build_library.py`（提示词库构建）· `build_human_premium_doc.py` / `build_gesture_expression_doc.py`（从叠加层渲染文档）· `run_demo.sh`（一键复现） |
| `tests/` | 37 个契约测试 |
