---
name: huashu-book-pdf
description: |
  橙皮书全流程：调研→规划→多Agent并行写作→三审三校→构建PDF/DOCX/EPUB。带你用写一本书的方法快速搞懂一个陌生领域，并沉淀成可分发的书籍级成果。
  适用场景：制作橙皮书、电子书、PDF手册、参考指南、完整入门书；或用结构化方法快速入门一个陌生领域。
  触发词：橙皮书、PDF手册、电子书、参考指南、完整手册、书籍级PDF、做一本XX、搞懂陌生领域、快速入门XX、更新EPUB。
  不适用：单页文档/PPT/海报（→ 用对应其他 skill）；纯网页内容（→ 用 website-* 工具链）。
---

# 橙皮书全流程：从主题到成书

从一个陌生主题到一本完整的电子书，五个阶段：调研 → 规划 → 写作 → 审校 → 构建。
**核心不是「出书」，是用写一本书的方法快速搞懂一个陌生领域。**

> 写一本书只是这条流水线最费功夫的一个出口；「快速搞懂一个陌生领域」这个能力本身，谁都用得上。

## 适用边界

**适合用这个 skill**：
- 想系统搞懂一个陌生行业、工具、赛道、领域
- 想做一份能交付给别人（同事/客户/读者）的系统化资料
- 想沉淀团队/项目的知识库为可分发的书籍级成果
- 有几万字的长内容生产需求，但不想一个人硬扛

**不适合用这个 skill**：
- 几页的快速参考（→ 直接 markdown 即可）
- 单页海报 / PPT（→ 用对应 skill）
- 实时更新的内部 wiki（→ 走 docs 系统）

## 拿到这个 skill 你能做什么

1. **30 分钟内搭起一本书的项目骨架** — 一条命令生成完整目录、CSS、构建脚本、模板
2. **多个 Agent 并行写章节** — 不再一个人熬几万字，按章节拆给 sub-agent 写
3. **四遍审校流水线** — 内容/风格/细节/事实核查，解决「写得对」「写得好」两个问题
4. **一次生成三种产物** — PDF（免费分发）/ DOCX（出版社交稿）/ EPUB（电子阅读器）
5. **版本化管理** — `vYYMMDD` 日期版本，每次更新自动 +1 build 号

## 前置依赖

| 依赖 | 用途 | 安装 |
|------|------|------|
| Node.js >= 16 | 运行构建脚本 | https://nodejs.org/ |
| Playwright + Chromium | HTML → PDF 渲染 | `npm install playwright && npx playwright install chromium` |
| pandoc >= 3.0 | HTML → DOCX | `brew install pandoc` |
| Python 3 + ebooklib | HTML → EPUB | `pip install ebooklib` |
| Python 3 + lxml | DOCX 后处理 | `pip install lxml` |
| docx (npm) | DOCX 样式模板 | `npm install docx` |

## 参考资料导航

| 需要时读取 | 路径 | 内容 |
|-----------|------|------|
| 写 HTML 片段时 | [references/design-system.md](references/design-system.md) | CSS 变量、HTML 组件速查、视觉红线 |
| 改封面规范时 | [references/cover-system.md](references/cover-system.md) | 企鹅三段式封面 + Prompt 模板 + 禁忌 |
| 写事实核查时 | [references/fact-check-sop.md](references/fact-check-sop.md) | 怀疑者三问 + 易错场景清单 |
| 审校风格时 | [references/style-guide.md](references/style-guide.md) | 降 AI 味检查清单 + 加个性化语感 |
| 新建项目时 | [scripts/init-project.sh](scripts/init-project.sh) | 一键生成项目骨架 |
| 写作模板 | [templates/](templates/) | 可直接复制的 styles.css / build.js / 片段 |

## 项目结构

```
[书名]/
├── README.md              # 项目简介（状态、定位、章节结构）
├── PROJECT.md             # 详细项目规划（大纲+进度+数据速查）
├── version.json           # {"version":"260403","build":0,"lastUpdate":"2026-04-03","title":"..."}
├── CHANGELOG.md
├── fragments/             # HTML 章节片段（纯 HTML，不含 <html><head>）
│   ├── 00-cover.html / 01-toc.html
│   ├── part{N}-{名称}.html 或 ch{NN}-{名称}.html
│   └── 99-backpage.html
├── output/                # 构建产物（HTML/PDF/DOCX/EPUB）
├── 封面/                  # 封面设计稿（PNG/JPG）
├── research/              # 调研资料
├── build.js               # HTML 合并脚本（编辑 FRAGMENT_ORDER）
├── build-pdf.js           # Playwright → PDF
├── build-epub.py          # HTML → EPUB（含表格自动截图）
├── build-docx.js          # HTML → DOCX（出版社交稿）
├── styles.css             # 共享 CSS
├── fix-docx-pagebreaks.py # DOCX 后处理（分页符、表格美化）
└── versions/              # 历史版本存档
```

## 版本号规则

**格式：`vYYMMDD`**（如 `v260403` = 2026 年 4 月 3 日）

- `version.json` 中存纯数字：`"version": "260403"`
- 构建产物文件名自动带 v 前缀：`MyBook-v260403.pdf`
- 每次有实质性更新时更新日期，同一天多次更新不变
- 不再使用语义版本号（1.0.0），日期版本更直观
- `build` 字段是同一天内的构建次数（每次 `update.sh` +1）

## 阶段 1：调研

> 目标：把领域拆成 6-10 个互不重叠的板块，搭出知识树骨架

1. **与用户确定主题和目标读者** — 一句话讲清「这本书帮谁解决什么问题」
2. **拆分调研维度** — 列出 6-10 个互不重叠的板块（避免 A/B 章节内容重叠）
3. **启动多个 background agent 并行调研** — 每份保存到 `research/YYYY-MM-{关键词}.md`
4. **调研完成后汇总，进入规划**

**反模式**：
- ❌ 一上来就甩一堆链接和名词把读者淹死
- ❌ 调研维度之间内容重叠（导致后面章节重复）
- ❌ 调研不区分"事实"和"观点"（后面审校会出问题）

## 阶段 2：规划

> 目标：把调研收敛成一份有逻辑的大纲。**列得出说明入门了，列不出说明还在门外。**

编辑 `PROJECT.md`，必须包含：
- **章节大纲表**：Part + 节号 + 标题 + 核心内容 + 信息来源
- **调研资料索引**：路径 + 摘要 + 状态
- **Agent 并行分工方案**：哪个 agent 写哪几章
- **进度追踪表**：每章 ⬜ / ⏳ / ✅
- **关键数据速查**：所有需要复用的事实/数据集中放这里

修改 `build.js` 中的 `FRAGMENT_ORDER`（或 `build-epub.py` 中的 `CHAPTERS`）。**与用户确认大纲后进入写作。**

## 阶段 3：多 Agent 并行写作

> 目标：让几万字不必一个人硬扛，每个 agent 负责若干章节

### 风格学习（每个写作 agent 必须先做）

```
## 第一步：学习目标写作风格（必须先做！）
读取你的写作风格规则文件 + 2-3 篇代表作样本，统一全书语感：
1. [你的写作风格规则文件路径]
2. [references/style-guide.md](references/style-guide.md)
3. [选 2-3 篇代表文章的路径]
```

橙皮书 vs 普通文章的区别：橙皮书是**教程手册**，结构化（步骤/表格/代码块）是必要的，但文字部分要有个性化语感，不能写成工具书。

### 片段结构铁律

每个正文片段必须遵循：

```html
<div class="content">
<h2 class="section-title page-break" id="partN"><span class="num">§0N</span> 标题</h2>
<p class="section-en">English Title</p>
<p class="section-intro">概述</p>
<!-- 正文 -->
</div>
```

三条铁律：
- **`<div class="content">` 包裹** — 控制左右 55px 边距
- **`id="partN"` 属性** — 目录锚点跳转
- **`page-break` class** — 每章新页

完整设计系统 + 组件速查见 [references/design-system.md](references/design-system.md)。

### 序言与前言（按发布渠道分版本）

| 渠道 | 包含内容 | 片段文件 |
|------|---------|---------|
| PDF（免费下载） | 不含前言 | 无 |
| DOCX（出版社） | 序言 + 前言 | `part00-preface.html` + `part00-introduction.html` |

**序言**（个人视角，~500 字）：
1. 「你好，我是 {作者名}。」开头
2. 为什么写这本书（个人动机、核心洞察）
3. 这个领域的现状和趋势
4. 核心问题与作者的回答
5. 「{作者名}」+ 日期 落款

**前言**（书的介绍，~300 字）：
1. 书的内容结构（前半/后半）
2. 适合谁读
3. 和系列其他书的关系
4. 「{作者名}」+ 日期 落款

### 封面页规则

- **作者**：`{作者名}`（注意是笔名，不是真实姓名）
- **不写页数预估**：封面不出现「~XX 页」等页数信息（实际页数会随内容更新变化，预估永远不准确）
- **封底二维码**：复制 `templates/fragments/gzh-qrcode.jpg` 到项目 `fragments/`，img 加 `style="width:360px;"`
- **完整封底模板**：见 [templates/fragments/99-backpage.html](templates/fragments/99-backpage.html)，按占位符替换为自己的社媒链接

## 阶段 4：三审三校

> ⚠️ 初稿写完后**不要直接构建**，必须经过审校。流程和公众号文章同等标准。

### 第一遍：内容/事实审校

重点检查：
- 时间线、产品发布日期是否准确
- 工具对比是否客观（不贬低竞品）
- 命令/快捷键是否真实可用
- 数据/引用是否有来源
- 人物归因是否正确

### 第二遍：风格审校（降 AI 味）

每个审校 agent 必须先读 [references/style-guide.md](references/style-guide.md)。重点：
- 去 AI 腔（排比、首先其次最后、套话）
- 加个性化语感（思考过程、个人判断、经验感）
- 破折号（——）每片段最多 1 处
- 使用「」引号，不过度使用
- 加粗约 10 处标记重点

### 第三遍：细节打磨

- 句子长度 15-25 字为主
- 段落手机屏 3-5 行
- 小标题不密集（每 300-500 字一个）
- 检查序言/前言与正文的一致性

### 第四遍：事实核查（Fact Check）— 怀疑者角色

> 三审三校解决的是「写得好不好」，事实核查解决的是「写得对不对」。这是两个完全不同的问题。

**为什么需要独立的事实核查**：写作 agent 凭模型知识库写竞品/外部信息，审校 agent 也用同一个知识库校验，错误会在同一个信息茧房里反复传播。事实核查员必须**用 WebSearch 获取一手信息**，不能依赖模型记忆。

**核查员的核心行为——对每条事实声明问三个问题**：
1. 「这是真的吗？」— 信息本身是否准确
2. 「来源在哪？」— 能否找到一手来源验证
3. 「前提成立吗？」— 修正事实后，基于此事实的论点/对比/判断是否仍然成立

第三个问题最容易被忽略。比如「A 和 B 的定价策略很不一样」，即使把 A 的价格改对了，整句的判断（「很不一样」）可能就不成立了。**事实核查不只是修数字，是质疑论点。**

完整 SOP + 易错场景清单见 [references/fact-check-sop.md](references/fact-check-sop.md)。

### 第五遍：全书一致性审查

多 Agent 并行写作容易出现跨章节的重复和冲突。事实核查完成后，**启动一个单独的 agent 通读全部 fragment**，检查以下三类问题：

**跨章节重复表达**：
- 相同的对比表格在多个章节重复出现（应只完整出现 1-2 次，其余章节简要引用）
- 相同的概念被反复从头解释（第一次出现详细讲，后续应「如 §0N 所述」简引）
- 相同的比喻/类比/故事被多次使用
- 相同的功能介绍在不同章节各展开一遍

**观点/信息冲突**：
- 不同章节对同一事物的推荐/评价矛盾
- 数据/定价/版本号等硬事实在不同位置不一致
- 对竞品的描述前后矛盾

**术语不一致**：
- 同一概念在不同章节用了不同名称
- 技术术语的大小写/格式不统一
- 命令写法不一致

**执行方式**：启动单个 agent，按顺序读取全部 fragment（不含封面/目录/尾页），输出结构化审查报告（问题位置+类型+建议），然后根据报告修复。

## 阶段 5：构建

> ⚠️ 必须在三审三校完成后才能构建。**不要跳过审校直接构建。**

### PDF 构建
```bash
node build.js       # 合并片段 → HTML
node build-pdf.js   # Playwright → PDF
```

### DOCX 构建（出版社交稿用）
```bash
node build-docx.js        # fragments→HTML→pandoc→docx→后处理
# fix-docx-pagebreaks.py 由 build-docx.js 自动调用
```

**出版社版内容清理**（build-docx.js 自动执行）：
- ✅ 包含序言+前言
- ❌ 移除 backpage 整页
- ❌ 移除 cover-disclaimer
- ❌ 移除飞书/外链更新链接

**DOCX 样式规范**（对齐出版社要求）：

| 样式 | 字号 | 字体 | 颜色 | 行距 | 备注 |
|------|------|------|------|------|------|
| Normal（正文） | 10pt | 微软雅黑 | #1a1a1a | 1.5 倍 (360) | 段后 120 |
| Heading 1（章标题） | 18pt bold | 微软雅黑 | #C4531A | 276 | 橙色底线 |
| Heading 2（节标题） | 14pt bold | 微软雅黑 | #1a1a1a | 276 | |
| Heading 3（小节） | 12pt bold | 微软雅黑 | #444444 | 276 | |
| Source Code | 9pt | Menlo | #333333 | 276 | 灰底 F5F5F5 |
| Block Text（引用） | 10pt | - | #555555 | - | 橙色左线，无斜体 |

**页面设置**：上/左/右 = 1 英寸，下 = 0.83 英寸

### EPUB 构建
```bash
python3 build-epub.py
# 输出：output/{书名}-v{版本号}.epub
```

部分阅读器的渲染引擎不支持 `<table>`、CSS flex/grid、SVG。构建脚本会自动截图替换。

构建完成后检查：
- [ ] EPUB 中所有表格/流程图都是 PNG 截图
- [ ] 在 Apple Books 中预览确认排版正常

## 阶段 6：封面制作

> 完整规范见 [references/cover-system.md](references/cover-system.md)

### 经典三段式布局（Penguin 企鹅出版社风格）

```
┌─────────────────────────┐
│    焦橙色 #C4531A        │  30% — 书名（白色大字）+ 「橙皮书」
├─────────────────────────┤
│    米白底 #F5F0E8         │  45% — 手绘墨水插画 + 副标题（灰色小字）
├─────────────────────────┤
│    焦橙色 #C4531A        │  25% — 「{作者名} 著」（白色居中）
└─────────────────────────┘
```

### 关键约束

1. **工具**：必须用 AI 一步生成（nano-banana-pro / Midjourney / GPT-Image），不用 HTML 拼接
2. **每次生成 3 版候选**让作者选
3. **分辨率**：2K（2048px）
4. **封面不加署名/水印**（底部「{作者名} 著」除外）
5. **比例**：竖版 3:4（绝对不要正方形）

### 禁忌清单

- ❌ 橙底+黑字
- ❌ 赛博霓虹/深蓝底
- ❌ 3D 书籍效果/阴影/透视
- ❌ 正方形比例（必须竖版 3:4）
- ❌ HTML 拼接（必须 AI 一步生成）

## 快速启动清单

### 新书
1. [ ] `bash scripts/init-project.sh ./我的新书 "我的新书标题"` 创建项目骨架
2. [ ] 调研 → `PROJECT.md` 大纲确认
3. [ ] 多 Agent 并行写作（先读 [references/style-guide.md](references/style-guide.md)！）
4. [ ] 三审三校（3 个 agent 并行审校）
5. [ ] 事实核查（1 个怀疑者 agent，WebSearch 验证所有事实声明，尤其是竞品信息）
6. [ ] 全书一致性审查（1 个 agent 通读全文，查重复/冲突/术语）
7. [ ] 根据核查+审查报告修复问题
8. [ ] 构建 EPUB + PDF
9. [ ] 制作封面（企鹅三段式，3 版候选）

### 更新已有书
1. [ ] 修改 `fragments/*.html`
2. [ ] 更新 `version.json`（日期格式 YYMMDD）
3. [ ] 三审三校（至少风格审校）
4. [ ] `./update.sh` 重建 EPUB + PDF

## 占位符速查

新建项目时，按需替换以下占位符为自己的真实信息：

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{作者名}` | 笔名/对外署名 | 花叔 |
| `{公众号名}` | 公众号名称（中文） | 花叔 |
| `{公众号二维码描述}` | 二维码 alt 文本 | 微信搜一搜「花叔」公众号 |
| `{官网}` | 官网 URL | https://www.huasheng.ai/ |
| `{GitHub用户名}` | GitHub 用户名 | alchaincyf |
| `{X用户名}` | X/Twitter 用户名 | AlchainHust |
| `{B站用户名}` | B 站用户 | 花叔v |
| `{YouTube频道}` | YouTube 频道 | @Alchain |
| `{小红书用户ID}` | 小红书 profile ID | (URL 末段) |
| `{代表作名}` | 最知名的产品名 | 小猫补光灯 |
| `{代表作成就}` | 代表作的成就描述 | AppStore 付费榜 Top 1 |
| `{开源项目列表}` | 开源项目，顿号分隔 | 女娲.skill、huashu-design |
| `{GitHub粉丝数}` | 粉丝数量描述 | 6.2k followers |
| `{知识星球名}` | 知识星球名称 | AI编程：从入门到精通 |
| `{书数量}` | 已出版技术书数量 | 9 |
| `{系列其他书名}` | 系列其他书名 | Claude Code 从入门到精通 |

## 红线

- ❌ **不编造数据**：涉及事实、数字、日期、定价时回查一手源；查不到如实说
- ❌ **不贬低竞品**：工具对比必须客观，给出真实差异而非拉踩
- ❌ **跳过审校直接构建**：四遍审校不能省
- ❌ **跨章节重复内容**：相同的对比表只完整出现 1-2 次
- ❌ **要花钱/签字/担责的结论当建议**：给的是线索，让用户找专业的人核
- ❌ **3D 书籍效果/深蓝底/赛博霓虹封面**：背离企鹅三段式
- ❌ **HTML 拼接封面**：必须 AI 一步生成

## 与其他 skill 的区别

| 场景 | 用这个 skill | 用别的 |
|------|-------------|--------|
| 1-3 页快速参考 | ❌ | 直接 markdown |
| 1 本完整的书 | ✅ | - |
| PPT 演示 | ❌ | `ai-image-to-pptx` |
| 单页海报 | ❌ | 对应图片生成 skill |
| 实时更新的 wiki | ❌ | 飞书/Notion 文档 |
