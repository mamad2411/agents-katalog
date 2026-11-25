---
name: modern-ppt
description: 生成现代分享/投屏风格的单文件网页 PPT(横向翻页·专业极简风·干净排版·3 套可切配色)。当用户要做线下分享、演讲、发布会的网页 deck,或提到「modern ppt」「做个分享 PPT」「投屏 deck」「网页 PPT」「把这段做成 slides」时使用。内置 12 个版式 + 交互动效(count-up / Chart.js 图表) + 3 套配色(默认安全橙,可切明亮蓝/柔和粉)+ 一套排版硬规范(单一 body 字号 token、标题靠分隔线、正文不上色、底部安全区等),产出一致、可直接投屏放映。
---

# Modern PPT · 现代投屏网页 deck

生成一份**单文件 HTML** 的横向翻页 deck:专业极简风、干净克制的排版,内置 12 版式 + 交互 + **3 套配色**(默认安全橙,放映按 `1/2/3` 切明亮蓝 / 柔和粉)。键盘 ← →、滚轮、触屏翻页,ESC 出索引,`B` 切静态模式。**默认就是"能直接投屏放映 / 发给别人 fork 改"的成品**。

> **来源与许可(必读)**:本 skill 衍生自 [规藏 guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)(© op7418,**AGPL-3.0**)——复用了它的 Swiss 模板底盘、WebGL/ASCII 背景、翻页/索引/动效引擎。在其上做了:安全橙主题(现扩为 3 套可切配色)、一整套投屏排版规范(下文)、12 版式 + 交互动效、已验证版式裁剪、已修模板 bug。**因此本 skill 整体仍是 AGPL-3.0**:再分发须保留 `LICENSE` + 本段署名 + 注明改动;放公司内部仓前先过开源合规(AGPL 常被禁)。生成出来的**最终 deck 不必写署名**。**模板示例页只用通用/公开内容,别烤进项目私货**(否则再分享前要现场清洗——本 skill 踩过)。

## 工作流(动手前先走)

1. **澄清**(用户只给主题/模糊想法时):受众与场景?时长(15min≈10页 / 30min≈18-22页)?**默认配色**(❶ 黑+橙 / ❷ 明亮蓝 / ❸ 柔和三文鱼粉——3 套都内置,放映时按 `1/2/3` 随时切,这里只是先定个默认;不确定就用默认黑橙)?有无素材/数据?有无硬约束(必须含 X / 不能出现 Y)?**数字一律来自用户素材,缺就标「待补」,绝不编造。**
2. **先定大纲再动手**:**从源文档 / URL 做 deck,先找出那一句 thesis 当锚点**(如「上下文会填满就变笨」),全篇结论先行、围着它转。每页一个观点(标题即观点);用"叙事弧"(钩子→定调→主体→转折→收束);分幕的长 deck 每 4-5 页插一张 divider(深墨底 + 幽灵编号,见排版规范 §9)。和用户对齐大纲再写。**先砍后写**:第一版总会过载,删页 / reframe 比堆料更出彩(comprehensive ≠ persuasive)。
3. **拷模板**:`cp assets/template.html 项目/index.html`。它是**完整成品**——18 页展示全部 12 版式 + 3 套配色 + 交互(count-up / Chart.js / 缩略图墙 / 章节 divider),已含全部 CSS/JS。改 `<title>`,**留下要用的版式页、删掉不用的**,把内容替换成用户的。
4. **先样页后放量**:先做封面 + 2-3 张代表页 → 截图 review(见下"验证") → 用户拍板 → 再批量产剩余页。**每轮都截图。**
5. **自检(必跑,不许跳)**:`node scripts/deck-lint.mjs <deck.html>`——机器检 斜体/裸字号/单格高光/无源数字/reduce-motion 陷阱/元叙述,**FAIL 修完才交付,WARN 逐条确认**;再逐条过下方硬规则 + `references/排版规范.md` 里机器检不了的(对齐/留白/呼吸感)。

## 排版硬规则(产出一致的关键 · 详见 references/排版规范.md)

1. **正文走单一 `--fs-body` token**(投屏 ≈21px;视频剪辑改 32px)。所有描述/段落/卡片说明/表格单元格都 `var(--fs-body)`,**禁止各写各的裸 font-size**。
2. **每页字号 ≤ 几档**:页标题 / 卡片标题 / 正文 / mono 角标 + 大数字特例。**字号编码层级**。
3. **栏目标题靠"分隔线 + 留白 + 角色对比"立住,不靠加大字号**。用 `.col-head`(安静灰字 + `border-bottom:2px solid ink`)。加大加粗反而和正文打架、更难读。
4. **正文不上色**:accent / 品牌色只给**标题关键词、图表数据、1px 分隔线**;正文强调 = **黑色加粗**,不用斜体。
5. **内容紧跟标题连排,不锚底**:禁止 `margin-top:auto` 把内容推到卡片底,造成"标题在天上、内容在地下"。
6. **底部安全区 ≥6vh**(`.canvas-card` 底 padding):满高内容块不要贴右下角导航提示/分页点。
7. **编号列表(01/02/03)用单一 grid 共享列轨 + `font-feature-settings:'tnum'`**,否则比例字体下数字宽度不同、各行标题左缘参差。
8. **强弱用 5 格方块刻度**(领跑=5 满格),可横向扫读;别只写文字。
9. **卡片"小标在上"而非右上角标**(长标题会和角标重叠);**一组卡别随手单格高光**(高光要么有数据/焦点语义,要么别加)。
10. **accent 不满屏铺**(安全橙满屏刺眼):封面/幕封用**深墨底 + 关键词上色**;split 收束页半屏橙可接受。

## 12 个版式(模板已内置示例页,cp 后改文案即可)

三层分类,每层 divider 分幕(见排版规范 §9):
- **① 基础骨架**:Cover 封面 · Agenda 目录 · Page divider 章节页 · Closing 收束
- **② 数据·对比·图表**:Stat grid(大数字 count-up 从 0 滚)· Chart(Chart.js 柱状+折线,逐柱升起/自动绘线 + hover tooltip + 折线标 QoQ%)· Comparison 对比矩阵(标准×选项 + 5 格刻度,主推列高亮)
- **③ 叙事·流程·内容**:Two-column 图文分栏(右栏可换 图/mock/图表/代码终端)· Three-column 三栏卡(3-grid)· Strategy house 战略房子图(SVG OGSM:橙屋顶使命 + 主题列×编号目标卡 + 价值观地基)· Process/Timeline 流程时间线 · Quote 金句
- 外加 **缩略图墙**:live 克隆全部版式,一屏预览,自动跟随配色。

## 已验证版式组件(只用这些,别发明)

- 卡片:`.sub-card`(.accent/.ink)、`.sub-grid-3-2`(六格)、`.triad`(3-grid 三栏卡)
- 数据:`.cnt`(count-up 数字)、`.stat-card`、`canvas[data-chart="bar|line"]`(Chart.js)、5 格方块刻度、`.cmp`(对比矩阵)
- 结构:`.stack-row/.stack-block`、`.duo-compare`(双轨对照 + `.vrule`)、`.timeline-v/.timeline-h`、`.house-svg`(战略房子图)
- 文字:`.h-xl-zh`(页标题)、`.lead`/`.body`(正文)、`.t-cat/.t-meta`(mono 角标)、`.mk`(accent 关键词)
- 版面:`.split-half`(收束)、`slide.dark` + 幽灵大编号(章节 divider)、`.code-card`(终端)、`.chart-card`、`.dot-mat`(点阵)
- 18 页示例就是这些组件的活样例,**直接 copy 改文案**最快。

## 交互 / 动效(模板已接好,`</body>` 前的 IIFE 自动跑)

- **数字 count-up**:`<span class="cnt" data-to="85" data-dec="0">85</span>` → 翻到该页从 0 滚到 85(tnum 防抖)。
- **图表**:`<canvas data-chart="bar">` / `data-chart="line"`,进页自动初始化,逐柱升起 / 自动绘线 + hover tooltip;折线每点标 QoQ%。改数据在 IIFE 的 `chartConfig`。
- **Agenda 不做逐项点亮**(2026-07-08 用户拍板):目录页静态全亮,所有条目常态可读——放映时不需要一项一项过,别再给 agenda 加 step 交互或 `data-agenda-steps`。
- **三栏逐张点亮(默认开)**:凡是 `.triad` 三栏页**默认**就带 → `←→`/滚轮每次高亮一张 `.triad-card`、其余转灰,讲到哪栏哪栏才彩色,到最后一张再翻页。**高亮色走 `var(--accent)`,自动跟随橙/蓝/粉配色**。适合"三件事逐个讲"的节奏。**不想要就给 `.triad` 加 `data-no-steps`**(如 `<div class="triad" data-no-steps>`,恢复满色静态)。缩略图墙里的三栏不受影响,保持满色。
- **缩略图墙**:`.thumb-wall[data-thumb-wall]` → 进页克隆全部版式做缩略图,自动跟随配色。

## 配色(3 套 · 放映时按 `1`/`2`/`3` 或 URL `?scheme=`)

- **1 = 黑+橙**(默认,深色页保留)· **2 = 明亮蓝**(纯白底)· **3 = 柔和三文鱼粉**(暖白底)。
- 蓝/粉两套自动给 `<body>` 加 `.lite` → 深色页(封面/数据/章节/金句)翻浅底。换/加配色:改 IIFE 的 `SCHEMES` 对象(覆盖 `--paper/--ink/--accent` 等 CSS 变量)。**单套配色只用一个 accent。**
- **设默认配色**(用户在澄清步选了蓝/粉时):在 IIFE 末尾加一行 `applyScheme('blue')`(或 `'salmon'`),这份 deck 打开就是那套;`1/2/3` 仍可现场切。

## 已知坑(别重踩)

- **截图验证陷阱**:Chrome 后台标签会冻结动画时钟,截图会拍到"动画第一帧=空白"——**不是 bug**,前台放映正常。验证动效**先按 `B` 切静态模式**(`window.__setLowPowerMode(true,{persist:false})`)再逐页截图。
- **只用上面列的组件**:模板未带 CSS 的花式版式(matrix/four-cards/loop 等)直接用会崩。
- **改单文件用脚本/正则时**:锚唯一串,改完数 section 数自检(定位串撞车会误删页)。
- **配色翻浅底(`.lite`)覆盖内联白字**:motion 动效会把内联 `color:#fff` 归一化成 `color: rgb(255, 255, 255)`,`body.lite .slide.dark` 的选择器要**同时匹配 `#fff` 和 `rgb(255, 255, 255)` 两种写法**,否则白字在浅底上隐身。

## 预览

```bash
open 项目/index.html   # macOS,无需服务器;断网时 motion 自动降级为无动画可读
```

<!-- lain-ppt(公开仓库名 modern-ppt) · 衍生自 guizang-ppt-skill(© op7418, AGPL-3.0) · 本段随分发须保留 -->
