---
name: douyin-viral-analysis
description: 把一个抖音账号的爆款作品全流程拆解成数据 —— 采集作品与互动数据、按内容类型分类、量化画风（墨/留白/灰/彩色占比、色相、调色板）、量化文案（结构、句式、文字位置、高频词）、算指标相关性，产出通用「数据速览」页与 PDF，再由 AI 基于 JSON 撰写结论。当用户要「分析某个抖音账号的爆款 / 拆解某账号的内容规律 / 做抖音账号诊断 / 看某账号的画风文案数据 / 竞品内容分析」时使用。同时支持图文号和视频号（视频号自动跳过画面 OCR 与画风量化）。
agent_created: true
---

# 抖音爆款分析（引擎 + AI 写报告）

> 本文件是**给 AI agent 读的入口**（WorkBuddy / Claude Skills 约定格式）。
> 面向人类的介绍、快速开始、合规声明见 [`README.md`](README.md)。
> 两份文档有内容重叠 —— **改流程或改依赖时两边都要改**。

## 这个技能是什么

**一条把抖音账号拆成数据的流水线**。它负责把数字弄对、把口径说清；**结论由 AI 写**。

为什么这么分工：旧版是一份 910 行的报告生成脚本，里面写死了「安全科普转发率最高」「育儿教育性价比最高」这类结论。
换个账号跑，它照样输出这些话 —— **结论是错的，而且从输出里看不出来**。
所以现在拆开：脚本产出干净数据 + 一张中立的速览页，判断交给 AI。

**先读** [`references/口径与坑.md`](references/口径与坑.md)。所有数字错，几乎都不是算错，而是拿两套口径的数去比。

---

## 一、准备

```bash
# 依赖（三选一，按你的机器情况）
cd <技能目录> && npm i puppeteer-core sharp        # 装在技能目录里
# 或：export DY_NODE_MODULES=/path/to/node_modules  # 指向已有的 node_modules
# 或：在 $DY_WORK 里 npm i puppeteer-core sharp

pip install rapidocr-onnxruntime                   # 图文号才需要（模型随 wheel 打包，国内离线可用）
```

环境变量（**都可以不设，有默认值**）：

| 变量 | 默认 | 说明 |
|---|---|---|
| `DY_WORK` | `./_douyin_run` | 工作目录，所有输入输出都落这里 |
| `DY_NODE_MODULES` | — | 存放 `puppeteer-core` / `sharp` 的目录 |
| `DY_CHROME` | 自动探测 | Chrome 可执行文件 |
| `DY_PROFILE` | `$DY_WORK/_browser_profile` | 登录态目录 |
| `DY_PYTHON` | 自动探测 | 跑 OCR 的解释器 |

**先跑自检**，缺什么一次性列清楚，别跑到第 8 步才炸：

```bash
node scripts/preflight.js
```

⚠️ **`DY_PROFILE` 里是你的登录凭据，不要分享给别人。** 同事各自跑一次 `login.js`。

---

## 二、完整流程

```
[0]  preflight.js         环境自检
 ↓
[1]  login.js             扫码登录（只需一次，登录态持久化）
 ↓
[2]  search_user.js       拿到 sec_uid（可给抖音号，也可直接给主页链接）
 ↓
[3]  collect_posts.js     拦截接口采集全部作品 → raw_posts.json
 ↓
[4]  classify.js          关键词粗分内容类型 → categories.json
 ↓        ↑
 ↓        └── AI 读 unlabeled / 并列命中列表，用 --set 写回（可反复）
 ↓
[5]  build_data.js        合成数据集 → data.json（meta / kpi / rows / catStats）
 ↓
[6]  download_media.js    下载素材 → media/（图文下全部图，视频只下封面）
 ↓
[7]  make_sheets.js       每帖拼一张速览长图 → contact_sheets/      可选
 ↓
[8]  ocr_all.py           画面 OCR → ocr_raw.json（图文号）           可选
 ↓
[9]  style_features.js    画风量化 → style_features.json（含切换点自动检测）
 ↓
[10] palette.js           配色拆解 → palette.json
 ↓
[11] copy_features.js     文案量化 + 相关性 → copy_features.json
 ↓
[12] gen_summary.js       数据速览页 → 数据速览.html
 ↓
[13] print_pdf.js         → 数据速览.pdf
 ↓
[14] AI 读 JSON 写结论
```

### 命令序列

```bash
export DY_WORK=/path/to/work DY_NODE_MODULES=/path/to/node_modules

node scripts/preflight.js
node scripts/login.js                      # 扫码，登录态存 DY_PROFILE
node scripts/search_user.js Lumm_6         # 或 --url "https://www.douyin.com/user/MS4w..."
node scripts/collect_posts.js <sec_uid>    # 全量采集（默认连续 12 次无新条目才停）
node scripts/classify.js --min-digg 1000   # 粗分；输出里会列出没命中的，交 AI 判
node scripts/build_data.js --min-digg 1000
node scripts/download_media.js             # 543 张图约 50MB
node scripts/make_sheets.js                # 可选
python scripts/ocr_all.py                  # 图文号；543 张约 15 分钟
node scripts/style_features.js
node scripts/palette.js
node scripts/copy_features.js
node scripts/gen_summary.js
node scripts/print_pdf.js
```

**视频号**：`download_media.js` 之后直接跳到 `copy_features.js`。
`ocr_all.py` / `style_features.js` / `palette.js` 会自动跳过视频帖（靠 `manifest.json` 的 `mediaType`），
不会报错，也不会输出一堆看起来像数据的 0。

---

## 三、分类这一步的用法（重要）

`templates/taxonomy.json` 是**起点不是标准答案**。实测在一个真实账号上，关键词粗分与人工标注的一致率是 **40/44**。

剩下 4 条是**标签边界争议** —— 比如「有些夫妻，或许前世就已经定好了」，算「夫妻婚恋」还是「奇闻灵异」？关键词规则本质上判不了。

**正确用法**：

```bash
node scripts/classify.js --min-digg 1000 --list-unlabeled
# 看输出的 unlabeled 列表 + 并列命中列表，AI 读完标题定类型，然后写回：
node scripts/classify.js --set "7648494718120460648=家庭亲情"
node scripts/classify.js --set "7653674334740889851=奇闻灵异"
```

不要指望调词表能调到 100%，那只会过拟合到某一个账号。

词表规则：**正文（第一个 `#` 之前）命中记 3 分，话题标签命中记 1 分**。
为什么不能一视同仁：实测 `#老师和学生` 这种次要标签会把一条「时隔多年，物是人非」的亲情帖拉成育儿教育。

想换一套分类体系？改 `taxonomy.json`，或在工作目录放一份同名文件覆盖它（同名文件优先）。

---

## 四、产出

| 文件 | 内容 |
|---|---|
| `raw_posts.json` | 采集到的原始接口数据（兜底） |
| `categories.json` | 每条作品的类型判定 + 来源（rule / manual / ai） |
| `data.json` | 账号 meta、KPI、全部作品明细、各类型统计（含均值与中位数） |
| `media/` + `manifest.json` | 图片素材（图文全部，视频仅封面） |
| `contact_sheets/` | 每帖一张速览长图 |
| `ocr_raw.json` | 每张图的逐行 OCR 结果（含坐标） |
| `style_features.json` | 每帖画风指标 + **自动检测的画风切换点** |
| `palette.json` | 每帖彩色主色与线条色 |
| `copy_features.json` | 每帖文案结构指标 + 互动数据 |
| `数据速览.html` / `.pdf` | 中立的数据速览页（**不含结论**） |

---

## 五、AI 写结论时怎么用

速览页只有数据。结论基于这些文件写：

- **`data.json`** → `rows`（逐条明细，含 `aweme_id`）、`catStats`（各类型统计）、`kpi`、`meta`
- **`style_features.json`** → `posts`（逐帖画风）、`regimeSplit`（画风切换点）
- **`copy_features.json`** → `posts`（逐帖文案指标，`hasOCR` 标记是否有画面文案）
- **`palette.json`** → 彩色主色与线条色
- **`ocr_raw.json`** → 需要逐句引用原文时用

写结论时必须遵守的几条：

1. **报数字必须带口径**：「均值」还是「中位数」、「整图」还是「局部」、「全期」还是「某期」。
2. **条数 ≤ 3 的类型只当线索**，不当规律。
3. **跨画风分界做对比必须分期算**。`regimeSplit` 非 null 时，凡涉及画风的对比都要分期。
4. **相关系数用原始词频**（`copy_features.js` 已经是），不是密度。
5. **n < 30 时 |r| < 0.3 视为噪声**；报 r 前先看去掉最高赞那条还成不成立。
6. **不写「应该怎么做」式的空话**，只写数据支持的判断，并标明样本量。

---

## 六、已知的坑（详见 references/）

最容易踩的几条：

- **图文帖的 `video.play_addr` 是背景音乐 mp3，不是画面**。图片在 `a.images[]`。
- **Windows 上 `os.listdir` 会吞掉目录名尾空格** → 必须用 `os.scandir`（本技能已封装成 `lib/paths.py` 的 `list_dirs()`）。
  这个坑实测漏掉 8/44 个目录、442/543 张图，**而且不报错**。
- **点赞数会变，不能当关联键**。一律用 `aweme_id`。
- **抖音号的扁平文本有歧义**（`Lumm_660.6万` 读成 `Lumm_6`+`60.6万` 还是 `Lumm_66`+`0.6万` 都通）。
  必须读最深层的、只含抖音号的那个 DOM 元素。
- **画风切换点不要写死日期**，本技能自动检测（实测自动找到的日期与人工判断完全一致）。
- **报告里最容易出的错是混口径**：实测有份报告「留白/墨/灰」取了全期均值、「彩色」取了切换后的 0%，
  四个数两套口径；而它要描述的是切换后的黑白期，真实墨量是 **8.19%** 而不是 5.4%（差 52%）。

完整清单见 [`references/口径与坑.md`](references/口径与坑.md)；
接口与选择器（抖音改版时看这个）见 [`references/抖音接口与选择器.md`](references/抖音接口与选择器.md)。

---

## 七、这套流程能产出什么（实测）

在一个 190 条作品、44 条爆款（点赞 ≥ 1000）、543 张插画的真实账号上跑通，得到：

- **画风**：全期 墨 5.38% / 留白 81.82% / 灰 9.13% / 彩 3.67%（均值）；
  自动检测到 2026-08-24 从彩色期切到纯黑白期（效应量 d=2.76），
  切换后 **墨 8.19% / 留白 82.26% / 灰 9.55% / 彩 0.00%**
- **文案**：画面汉字数中位 209.5、分镜数中位 11、每图 18.7 字、行数中位 28
- **文字纵向位置**（**必须分期看**）：全期中位 0.281 是个**双峰分布的中位数，两个峰都不描述** ——
  P1 彩色期文字在**底部**（中位 0.790，20/24 在底部），P2 黑白期文字在**顶部**（中位 0.057，**20/20 全在顶部**）。
  这是「全期中位数」最典型的失效场景。
- **相关性**（n=44，**对收藏率**）：
  画面行数 **r = +0.440**、对话次数 r = +0.349、「我/咱」次数 **r = −0.365**、分镜图数 vs 转发率 r = −0.310

**回归验证**：这套脚本的 `copy_features.json` 与原始人工分析结果逐字段比对 —— **528 个值，0 处不一致**；
`style_features.json` 的四项占比均值/中位数也逐位相同。改代码后用这个当回归基线。

这些数字都可用 `node scripts/style_features.js` 和 `node scripts/copy_features.js` 复现。
