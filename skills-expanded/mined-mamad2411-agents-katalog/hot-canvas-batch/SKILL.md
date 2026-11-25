---
name: hot-canvas-batch
description: 当需要把网络热点/流量高的内容批量做成 flipbook-skill 画册（canvas）时使用——联网搜当日热点、为每个选题生成根图+10+张下钻图的竖版画册，服务自启自关、近3个月同主题自动去重。触发词：热点画册、批量生成画册、网络热点做画册、build hot canvases、canvas 批量下钻、热搜做成画册。
---

# 热点画册批量生成 (hot-canvas-batch)

## 概述
两阶段，职责分明：
1. **选题（你来做，需联网+人工判断）**：联网搜当日热点，挑 1-3 个流量高的选题，
   为每个选题写一份 `themes.json`——含根图主题 + ≥10 个下钻 label。
2. **建册（脚本全自动）**：`build_canvases.mjs` 自己挑空闲端口启动 flipbook server
   （强制 `ENABLE_CODEBUDDY=1`，用 codebuddy 出图，**不依赖 OpenAI**）→ 逐个建竖版
   画册 → 每册根图 + 10 个 label 下钻 → 写带日期的历史记录 → **无论成功/报错/Ctrl-C
   都 kill 掉 server**。(脚本耗时较长，30min~1h)

## 何时使用
- "收集网络热点做成画册" / "批量生成画册" / "热搜做成 canvas"。
- 用户要一次产出多个画册、每册要够多图（≥10 张下钻）。

## 唯一铁律
**选题阶段必须过滤政治敏感话题**——不碰政治人物、政治制度、政府机构、选举、
地缘冲突等。只选娱乐、科技、体育、游戏、生活、文化等安全热点。这条优先级最高。

## 阶段一 —— 选题，写 themes.json

1. **先看已发布的主题（去重前置）**：选题前先列出近 N 天已经做过的画册主题，
   避免重复选题、白费搜索功夫。运行：

   ```bash
   node ./scripts/list_recent_topics.mjs           # 人读列表，近 90 天，最新在前
   # node ./scripts/list_recent_topics.mjs --json  # 机读 JSON
   # RECENT_DAYS=30 node ./scripts/list_recent_topics.mjs  # 收窄时间窗
   ```

   这个脚本**直接读** `topics-history/*/run.json`、不起服务、不联网。把输出里的
   topic + aliases 当作"黑名单"：**搜热点 / 挑选题时就主动避开这些已发布主题**
   （含近义说法）。这样在选题阶段就完成去重，而不是等到阶段二建册时才被 SKIP。
2. 用 WebSearch 搜当日热点（如票房榜、电竞赛事、AI 动态、热门影视/综艺等），
   抓取**具体事实**（数字、事件、名称），这些会成为下钻 label。挑选题时对照第 1 步
   的已发布列表，命中（或近义）的直接换别的热点。
3. 按 `scripts/themes.example.json` 的结构写一份 themes 文件。字段：

```json
[
  {
    "topic": "根图主题（一句话，作画册根图标题）",
    "aliases": ["去重关键词1", "去重关键词2"],
    "style": "按主题挑的风格（见下方风格列表，如 popart/goldluxe/kawaii…）",
    "branches": 5,
    "drills": ["下钻子图1", "下钻子图2", "...", "下钻子图10"]
  }
]
```

- `topic`：根节点主题，会触发一张全景信息图。
- `aliases`：去重用的近义关键词（脚本归一化后做包含匹配）。写全一点，避免下次
  换个说法又重复生成。
- `style`：**为每个 theme 挑一个最契合的视觉风格**（从下方「风格列表（12 种）」
  里按"适用主题"列匹配）。这是避免产出趋同的关键——不要清一色 `cinematic`。同一批
  多个 theme 尽量挑**不同**风格，特色越鲜明越好。`themes.json` 里的 `style` 字段
  优先级高于命令行 `STYLE=`（见下方优先级）。
- `drills`：每条是一个**下钻子图的主题 label**。脚本走 `/api/canvas/:id/click/upload`
  的 `label` 覆盖路径——**子图内容由 label 决定，不靠点击坐标语义**（坐标只用来在
  画面上铺开热点锚点，避免引导线重叠）。所以 label 要写成具体、自洽的主题句。
- 至少写 10 条 drills（`DRILL_PER` 默认取前 10 条）。

## 阶段二 —— 跑脚本（单条命令，服务自启自关）

```bash
node ./scripts/build_canvases.mjs --themes /path/to/themes.json
```

脚本会：挑空闲端口 → spawn server → 等就绪 → 去重 → 建册 → 写历史 → kill server。
**不需要你手动起服务，也不需要你记得关。**

### flag / env
| 名称 | 默认 | 说明 |
|------|------|------|
| `--themes <path>` | 必填 | themes JSON 文件路径 |
| `--app-dir <path>` | 自动推断 | flipbook app 根目录；脚本不在 app 内时需指定 |
| `--keep-server` | 关 | 调试用，结束后保留 server 不 kill |
| `PORT` | 自动挑空闲端口 | 指定则用固定端口 |
| `ORIENTATION` | `portrait` | 画册方向，竖版/横版 |
| `STYLE` | 空 | 全局/轮询风格（如 `popart` 或 `popart,kawaii,pixel`）。**推荐改用 `themes.json` 里每个 theme 的 `style` 字段按主题挑**，优先级高于 `STYLE`；显式 `PROMPTS_DIR` 又高于二者 |
| `PROMPTS_DIR` | — | 直接指定 prompt 模板目录，覆盖 `STYLE` 的默认选择 |
| `RECENT_DAYS` | `90` | 去重时间窗（近 N 天同主题跳过） |
| `DRILL_PER` | `10` | 每册下钻子节点数 |
| `ENABLE_OCR` | `0`（关） | 建册默认关掉 Apple Vision OCR 文字层；设 `1` 重新开启 |
| `ENABLE_AUDIO` | `0`（关） | 建册默认关掉 macOS `say` 旁白音频；设 `1` 重新开启 |
| `DRY_RUN=1` | — | 起服务→打印去重计划→关服务，不建册（用于验证 themes/去重）|

> 注：批量建册默认关闭 OCR 与音频——下游 canvas-to-social 导出不消费文字层/旁白，
> 且二者各自给每张图增加一次额外处理开销。需要时用 `ENABLE_OCR=1` / `ENABLE_AUDIO=1` 开回。

建议先 `DRY_RUN=1` 跑一遍确认选题不会被去重命中，再正式建。

## 视觉风格（STYLE 开关）

默认用项目原始风格（米色 isometric 信息图，即"百科知识"风）——当**既没指定
`themes.json` 的 `style`、也没传 `STYLE=` / `PROMPTS_DIR=`** 时生效，对应
`app/prompts/` 目录。通过 `STYLE=` 切换风格包，支持**按主题指定**或**全局轮询**。

### 风格列表（12 种 + 默认）

> **默认风格**（不传任何 STYLE/style/PROMPTS_DIR）：米色 isometric 信息图，
> 偏中性百科知识感，适合工具/教程/通用科普。下面 12 种是可显式切换的风格包。

> **重要：模型必须按主题为每个 theme 自动挑选最契合的风格**（见阶段一第 4 步），
> 不要清一色用 `cinematic`。同一批多个 theme 尽量挑不同风格，让产出有辨识度、不趋同。

| STYLE 值 | 风格名 | 视觉特征 | 适用主题 |
|-----------|--------|----------|----------|
| `cinematic` | 深海电影感 | 深蓝渐变、生物发光、体积光、暗色电影感 | 科技/揭秘/深度/悬疑 |
| `vaporwave` | 蒸汽波 | 紫粉青渐变、霓虹网格地平线、罗马石膏像、80s 故障感 | 潮流/音乐/复古未来/二次元 |
| `claymorphism` | 黏土3D | 软萌 3D 黏土质感、圆润体块、柔和投影、马卡龙撞色 | 生活/教程/产品/萌系 |
| `risograph` | 套印孔版 | 2-3 色叠印错位、颗粒噪点、荧光粉蓝、复古印刷 | 文艺/活动/海报/手作 |
| `holographic` | 全息镭射 | 镭射彩虹渐变、液态金属反光、Y2K、未来高级感 | 美妆/数码/潮品/科技 |
| `papercut` | 剪纸分层 | 多层纸艺立体景深、清晰阴影、鲜明撞色 | 故事/节日/文化/传统 |
| `popart` | 波普漫画 | 漫画网点、粗黑描边、爆炸框 BAM/WOW、原色高饱和 | 娱乐/八卦/趣味/猎奇 |
| `kawaii` | 治愈卡通 | 圆润扁平卡通、糖果色、大眼贴纸、可爱吉祥物 | 育儿/萌宠/情感/轻科普 |
| `goldluxe` | 鎏金奢华 | 黑金配色、烫金质感、大理石纹、聚光灯、高级杂志感 | 财经/奢侈品/高端/汽车 |
| `airbrush70s` | 复古喷绘 | 70s 喷枪渐变、暖色日落条纹、颗粒、复古海报 | 旅行/音乐/怀旧/慢生活 |
| `glassmorphism` | 毛玻璃 | 半透磨砂玻璃卡片、彩色光晕背景、模糊层叠、现代 UI 感 | 科技/金融/数据/产品 |
| `pixel` | 复古像素 | 8-bit 像素网格、限色板、扫描线、街机游戏感 | 游戏/怀旧/80-90s/电竞 |

### 使用方式

**方式一（推荐）：按主题指定风格**——`themes.json` 中每个 theme 带一个 `style` 字段，
模型选题时就按"适用主题"挑好，**这是避免趋同的关键**：
```json
[
  {
    "topic": "顶流明星塌房始末",
    "style": "popart",
    "aliases": ["塌房", "明星八卦"],
    "drills": ["事件时间线", "粉丝反应", "..."]
  },
  {
    "topic": "新能源汽车销量榜",
    "style": "goldluxe",
    "aliases": ["新能源", "销量榜"],
    "drills": ["销量第一", "续航对比", "..."]
  }
]
```
不带 `style` 字段时，回退到命令行 `STYLE=` 或项目默认。

**方式二：全局统一风格**（整批用同一种）
```bash
STYLE=glassmorphism node ./scripts/build_canvases.mjs --themes /path/to/themes.json
```

**方式三：多风格轮询**（逗号分隔，多个 canvas 时依次轮用）
```bash
STYLE=popart,kawaii,pixel node ./scripts/build_canvases.mjs --themes /path/to/themes.json
```

**方式四：完全自定义**——复制任意 `prompts-<style>/` 目录，改写后直接用 `PROMPTS_DIR` 指向：
```bash
PROMPTS_DIR=/path/to/my-custom-prompts node ./scripts/build_canvases.mjs --themes ...
```

### 风格包结构

每个风格对应 `prompts-<style>/` 目录（位于 `skills/hot-canvas-batch/` 下），包含：
- `system.md` — 全局视觉约束
- `image-prompt.md` — 风格后缀（引擎用 `>` 引用 + 反引号格式提取）
- `planner.md` — 文案风格（标题字数/正文语气）
- `click-label.md`、`decide-search.md` — 通常复用，无需修改

### 优先级

显式 `PROMPTS_DIR=xxx` > `themes.json` 中 `style` 字段 > `STYLE=` 环境变量 > 项目默认（米色 isometric）

## 去重机制（两道防线）
两个阶段都基于同一份历史数据 `<app>/topics-history/*/run.json`，归一化口径一致
（`topic`+`aliases` 去空格/标点/大小写后做包含匹配）：

1. **选题阶段（前置，推荐）**：跑 `list_recent_topics.mjs` 列出近 `RECENT_DAYS` 天
   已发布主题，**搜热点时就主动避开**——从源头省掉重复选题与无谓搜索。
2. **建册阶段（兜底）**：`build_canvases.mjs` 起服务后会再扫一遍历史，对本次 themes
   逐条做包含匹配，命中则 SKIP（控制台打印 `SKIP "..." (recent duplicate of "...")`）。

两层用同一逻辑，前置那层让你尽早换题，兜底那层保证万一漏了也不会重复生成。
**所以每次换新热点即可，老主题不会被重复生成。**

## 产物
- 画册数据：`<app>/server/data/canvases/<canvasId>/`（manifest / tree.json / nodes / images）。
- 历史记录：`<app>/topics-history/<YYYY-MM-DD_HHMMSS>/run.json`，含
  `{canvasId, topic, aliases, orientation, nodeCount}`。**不存 url**——端口是临时的、
  服务会被关掉，url 没有意义；要看画册时另起服务再访问 `/?c=<canvasId>`。

## 每册图片数与结构
- 根图 1 张（全景信息长卷）+ 10 个一级下钻 = 11 张，每册稳定 ≥10 张。
- 想要更多层级/更多图：建完后对某些一级子节点再 click 下钻一层（depth 2），
  或调大 `DRILL_PER`。

## 常见坑
- **codebuddy planner 偶发 JSON 解析失败** → 个别下钻节点缺图（tree 有节点但 images/
  下无对应 .png）。补救：`POST /api/canvas/:id/nodes/:hash/regenerate`，或对根图再补
  一个 label 下钻。脚本的 settle 阶段会等重试落盘。
- **每个父节点并发上限 4**（server 端 `MAX_PARALLEL_CLICKS_PER_NODE`）。脚本按 ~800ms
  间隔投递、整体串行等待，不会触顶；手动批量 click 时注意别一次性超过 4 个。
- **根图较慢**：planner（联网搜索+规划，≤90s）+ 图片生成（≤180s），根图就绪通常
  1-4 分钟，属正常，不要误判卡死。
- **--app-dir**：脚本默认从自身路径上溯 4 级定位 app 根。若把脚本拷到别处运行，
  必须用 `--app-dir` 指向 flipbook app 根目录（含 `server/src/index.js` 的那层）。
