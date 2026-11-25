---
name: ppt-master
description: 专业PPT设计制作技能。⚠️【强制】必须先完成需求分析（Step 1），不允许直接开始制作。无论用户提供什么材料，都必须通过提问收集完整需求后才能继续。触发条件：用户需要制作PPT、设计幻灯片、汇报演讲、课件制作、PPT模板设计、PPT美化、PPT排版、幻灯片设计、slides、.pptx文件生成等任何与PPT相关的任务。融合了专业设计原理（CRAP原则、配色心理学、版式设计）、PptxGenJS代码生成能力和SVG高级图形绘制，包含22个PptxGenJS预建模板、52种SVG图表模板和Q1-Q9设计决策框架。
---

# PPT Master - 专业PPT设计制作技能

## 🚀 首次使用准备

### 安装依赖

> ⚠️ **重要**：首次使用前必须安装依赖，之后可跳过此步骤

**PPTX 依赖**（必须）：

```bash
cd "技能目录\assets"

# 检查有没有 node_modules，没有再安装
if not exist node_modules npm install
```

### 目录结构说明

```
ppt-master/
├── assets/                    ← PPTX 相关（需要 npm install）
│   ├── package.json          ← 依赖配置
│   ├── node_modules/         ← 依赖安装后生成（不要手动修改）
│   ├── slide-*.js           ← PPTX 模板
│   ├── chart-*.js           ← 图表模板
│   ├── compile*.js           ← 编译脚本（compile / compile-v2-base / compile-enhanced）
│   └── output/               ← 输出目录
├── components/               ← 组件
├── references/               ← 参考文档（28+ 个，含 slide-techniques.md）
├── templates/               ← SVG 图形模板（52个）
├── scripts/                 ← 项目完工工具链
│   ├── lint.js              ← 编译前静态检查（NBSP/颜色/async 等）
│   ├── punct-fix.js         ← 标点规范化（NBSP/智能引号 → ASCII）
│   ├── audit_pptx.py        ← PPTX 元数据审计
│   ├── extract_pptx.py      ← 文本抽取
│   └── extract_images.py    ← 图片抽取
└── SKILL.md                  ← 你正在读
```

---

## ⚠️ 执行警示（必读）

> **10%核心原则**：PPT设计的80%价值来自20%的核心知识。不要为了查"图片处理12法"而忽略了核心原则的应用。

### 每次必查的20%

| 原则 | 文件 | 为什么重要 |
|------|------|------------|
| **CRAP四原则** | [design-principles.md](references/design-principles.md) | 对比/重复/对齐/接近贯穿始终 |
| **叙事弧模板** | [narrative-arc.md](references/narrative-arc.md) | 内容结构化方法论 |
| **配色7:2:1法则** | [references/color-system.md](references/color-system.md) | 控制颜色不超过3种+黑白灰 |
| **场景信息密度** | [references/scenarios/*.md](references/scenarios) | 决定一页放几个要点 |
| **实战代码模式** | [slide-techniques.md](references/slide-techniques.md) | slideConfig/假渐变/数据驱动,真实项目沉淀 |

---

## 🚨 强制执行警告

> 🚨 **违规警告**：如果在没有完成 Step 1 需求分析的情况下直接开始生成内容，所产生的内容不被认为是正确的技能执行。正确的流程永远是：**提问 → 确认 → 执行**。
>
> ⚠️ **【强制规则 - 绝对禁止跳过】**
> - 即使用户给了完整文档，也要提问确认
> - 即使用户说"直接做"，也要先完成需求收集
> - 需求分析是**第一步也是唯一的第一步**，在完成之前禁止：
>   - ❌ 阅读用户材料
>   - ❌ 分析内容
>   - ❌ 生成任何内容
> - 违反此规则将导致生成内容不符合用户需求

---

## 核心决策流程

```
⚠️ 【强制入口】必须从这里开始，不允许跳过
    ↓
[Step 1: 需求分析] → ★★★ 必须先完成 Step 1 ★★★
    ↓
[Step 2: 场景判定] → ★ 必须等 Step 1 完成 ★
    ↓
★ [叙事弧规划] → ★ 用叙事弧组织整体结构 ★
    ↓
[Step 3前: 设计决策] → ★ Q1-Q9 + CRAP框架自问 ★
    ↓
[Step 3: 设计执行] → 按must-read + scenario读取references
    ↓
★ [SVG决策] → ★ 复杂图形用SVG模板 ★
    ↓
[Step 4前: 设计验证] → ★ 单页+全局检查清单 ★
    ↓
[Step 4: 代码生成] → PptxGenJS实现
```

---

## Step 1: 需求分析（强制执行）

> ⚠️ **【强制规则 - 绝对禁止跳过】**
> 在完成需求分析之前，你 **绝对不能** 做以下任何事情：
> - ❌ 阅读用户的材料文件
> - ❌ 分析材料内容
> - ❌ 规划PPT结构
> - ❌ 生成任何代码
>
> **必须使用 AskUserQuestion 工具提问**

### 必要信息检查

| 必要信息 | 说明 |
|----------|------|
| 主题 | 汇报什么/演讲什么 |
| **受众** | **谁来听（影响风格和内容深度）** |
| **页数** | **预计多少页（影响信息密度）** |
| **风格** | **正式/轻松/技术深度（影响用词和视觉）** |
| **场景** | 什么场合 |

> ⚠️！！！ **即使提供了材料，也要向用户确认以上信息**。材料 ≠ 完整需求。

### 提问清单

| # | 问题 | 选项示例 |
|---|------|---------|
| 1 | 听众是谁？ | 内部同事/领导/客户/投资人/学术/其他 |
| 2 | 什么场景？ | 工作汇报/商业提案/产品发布/培训/个人展示 |
| 3 | 几分钟/几页？ | 5-10页/10-20页/20-30页/40页+ |
| 4 | 有材料吗？ | 完整文档/部分素材/大纲/无材料 |
| 5 | 什么风格？ | 正式商务/科技简约/轻松活泼/高端大气 |

**进阶分析**：观众分层和KANO需求分析见 [references/thinking.md](references/thinking.md)

### 需求确认模板

```
## 需求摘要（待确认）

| 项目 | 您提供 |
|------|--------|
| 主题 | [提炼的主题] |
| 受众 | [用户选择 - 决定风格和内容深度] |
| 场景 | [用户选择 - 决定信息密度] |
| 时长/页数 | [用户选择 - 决定篇幅] |
| 风格 | [用户选择 - 决定视觉和用词] |

请确认以上信息是否准确？

```



---

## Step 2: 场景判定（核心决策点）

根据受众+场景组合判定PPT等级和设计策略。

### 听众 → 内容深度

| 听众 | 技术深度 | 术语处理 |
|------|----------|----------|
| 学生/学术 | 低 | 通俗解释 |
| 技术人员 | 高 | 可用专业术语 |
| 管理层 | 中 | 侧重价值/成本 |
| 客户/投资人 | 低~中 | 侧重商业价值 |
| 普通大众 | 极低 | 避免术语 |

### PPT三等判定

| 等级 | 特征 | 适用场景 |
|------|------|---------|
| **一等** | 极简、故事、打动人 | 产品发布/路演/TED |
| **二等** | 结构清晰、信息分层 | 学术汇报/培训/工作汇报 |
| **三等** | 功能完整、操作熟练 | 日常汇报/入门演示 |

### 场景 → 等级映射

| 场景 | 等级 | 信息密度 | 核心原则 |
|------|------|----------|----------|
| 产品发布/路演 | 一等 | 极低（一页一信息） | 乔布斯极简法 |
| 学术汇报/培训 | 二等 | 中~高 | 专业严谨、逻辑清晰 |
| 工作汇报/述职 | 二等 | 中 | 结论先行、数据支撑 |
| 商业提案/BP | 一等~二等 | 低~中 | 结论先行、说服力 |
| 内部分享 | 二等~三等 | 中~高 | 技术清晰、适度详细 |

### 三维体系快速自检

| 维度 | 问题 | 检查点 |
|------|------|--------|
| **难忘感** | 观众离开后能记住什么？ | 金句/画面/数据 |
| **设计感** | PPT是否专业好看？ | 配色/字体/排版 |
| **仪式感** | 演讲是否有感染力？ | 开场/结尾 |

完整说明见 [references/three-dimensions.md](references/three-dimensions.md)

### ★ 叙事弧应用（内容结构化）

**使用时机**：在Step 2场景判定后，用叙事弧来规划整体内容结构。

**为什么在这里用**：
- 叙事弧是**宏观规划工具**，解决"讲什么、怎么讲"的问题
- Q1-Q9是**微观设计工具**，解决"每页怎么设计"的问题
- 顺序：叙事弧 → Q1-Q9 → 配色/字体

**五段式结构**：
```
钩子(Hook)       → 1 页   : 抛一个反差 / 问题 / 硬数据让人停下来
定调(Context)    → 1-2 页 : 说明背景 / 你是谁 / 为什么讲这个
主体(Core)       → 3-5 页 : 核心内容,用版式穿插
转折(Shift)      → 1 页   : 打破预期 / 提出新观点
收束(Takeaway)   → 1-2 页 : 金句 / 悬念问题 / 行动建议
```

**页数规划参考**：
| 时长 | 总页数 | 分配 |
|------|--------|------|
| 5分钟 | 8-10页 | Hook(1) + Context(1) + Core(5) + Shift(1) + Takeaway(1) |
| 15分钟 | 15-20页 | Hook(1) + Context(2) + Core(10) + Shift(2) + Takeaway(2) |
| 30分钟 | 25-30页 | Hook(1) + Context(2) + Core(18) + Shift(3) + Takeaway(3) |

详细模板见 [references/narrative-arc.md](references/narrative-arc.md)

---

## ★ Step 3前: 设计决策（强制节点）

> ⚠️ **必须执行**：在选择配色/字体/版式之前，先用 Q1-Q9 + CRAP框架自问。

### Q1-Q9 设计决策清单

> 每页必须完成 Q1-Q9，**Q4 记忆点不能答"无"**。

**快速清单**：
| # | 问题 | 关键检查 |
|---|------|---------|
| Q1 | 观众是谁？关注什么？ | 核心观众+关注点 |
| Q2 | 演示后观众会做什么？ | 具体行动 |
| Q3 | 需求层级？ | 基本型/期望型/兴奋型 |
| Q4 | 记忆点？（不能"无"） | 金句/画面/数据 |
| Q5 | PPT等级？目标？ | 一等打动人/二等说明白/三等做出来 |
| Q6 | 3秒能说清核心吗？ | 一句话核心信息 |
| Q7 | 有念稿内容吗？ | 念稿→删除 |
| Q8 | 删减检查？ | 每句回答保留/删除 |
| Q9 | 字体选择？ | 参考typography-guide.md |

完整模板：
```
页面 {N}：
- Q1观众：{核心观众}
- Q2行动：{演示后观众会}
- Q3需求：{层级}
- Q4记忆点：{金句/画面/数据}
- Q5等级：{一等/二等/三等}
- Q6核心：{一句话}
- Q7念稿：{有/无}→{处理}
- Q8删减：{保留/删除}
- Q9字体：{字体名}
- 版式：{选择}
- 配色：{确定值}
```

**CRAP自问**：
| 原则 | 自问 | 检查 |
|------|------|------|
| 对比 | 标题vs正文≥2倍？颜色有区分？ | 是/否 |
| 重复 | 整体风格一致？ | 是/否 |
| 对齐 | 元素有参考线？ | 是/否 |
| 接近 | 相关内容靠近？间距一致？ | 是/否 |

### 版式判定树

**内容页（6种）：** 标题+正文 | 左右分栏 | 上下分割 | 三栏并列 | 卡片式 | 时间轴
**封面（3种）：** 居中式(学术/正式) | 左右分栏(企业/产品) | 全图型(创意/活动)
**目录（2种）：** 垂直列表(3-5章) | 双栏网格(4-6章)

---

## Step 3: 设计执行

按场景读取必要文件，选择设计要素。

### 必读文件（每次）

| 文件 | 内容 |
|------|------|
| [design-principles.md](references/design-principles.md) | CRAP四原则 |
| [color-system.md](references/color-system.md) | 配色7:2:1 |

### 场景文件（必须读）

| 场景 | 文件 |
|------|------|
| 学术汇报 | [scenarios/academic.md](references/scenarios/academic.md) |
| 产品发布/路演 | [scenarios/commercial.md](references/scenarios/commercial.md) |
| 培训课件 | [scenarios/training.md](references/scenarios/training.md) |
| 工作汇报 | [scenarios/workplace.md](references/scenarios/workplace.md) |

### 按需读取

| 场景 | 文件 |
|------|------|
| 字体决策 | [typography-guide.md](references/typography-guide.md) |
| 数据图表 | [charts.md](references/charts.md) |
| 创意灵感 | [master-inspiration.md](references/master-inspiration.md) |
| **复杂图形/SVG** | **[svg-graphics-guide.md](references/svg-graphics-guide.md)** |

---

## 🚫 【强制禁止规则】

> ⚠️ 禁止不读场景文件就直接跳过

| 场景 | 必须读 |
|------|--------|
| 学术汇报 | academic.md |
| 商业/产品发布 | commercial.md |
| 培训/教育 | training.md |
| 工作汇报 | workplace.md |
| 涉及数据表格 | charts.md |
| 涉及配色 | color-system.md |
| 涉及字体 | typography-guide.md |
| **涉及复杂图形** | **svg-graphics-guide.md** |

### 3.5 设计要素选择

**配色**：见 [color-system.md](references/color-system.md) 行业配色18套
**字体**：见 [typography-guide.md](references/typography-guide.md)

### 动画设计（可选）

> ⚠️ PptxGenJS不支持动画，需在PowerPoint中手动添加

**三大作用**：指南针（引导逻辑）| 魔术师（制造悬念）| 放大镜（强调重点）

**规划**：每页最多1个动画，时长≤3秒，风格统一

---

## ★ Step 4前: 设计验证（强制节点）

### 单页检查

```
□ 核心信息突出？  □ 对比足够？（标题vs正文≥2倍）
□ 风格统一？      □ 元素对齐？
□ 适当留白？      □ 记忆点视觉化？
□ 3秒测试通过？
```

### 全局检查

```
□ 配色统一？  □ 字体统一？  □ 标题位置一致？
□ 页码位置一致？  □ 信息密度符合场景？
```

详细清单见 [references/quality-checklist.md](references/quality-checklist.md)

---

## ★ Step 4 前置: 质量门禁（Hard Constraints）

> ⚠️ **必读**：在开始写任何 slide-XX.js 代码之前,先把下面 15 条硬约束读 3 遍。
> 这 15 条是 A 真实项目多次踩坑后沉淀的"红线",**违反任何一条都可能导致编译失败、文件损坏或交付质量不达标**。

### Hard Constraints 15 条

| # | 约束 | 验证方式 |
|---|---|---|
| 1 | 使用 `LAYOUT_16x9`（10" x 5.625"） | compile.js 第一行 `pres.layout = "LAYOUT_16x9"` |
| 2 | Canvas 边界：`x + w ≤ 10.0`,`y + h ≤ 5.625` | `node scripts/lint.js` 或人工 review |
| 3 | 安全区域：所有元素在 [0.5, 0.4]→[9.5, 5.225] | 4.x 节 GRID 系统 |
| 4 | 一页一文件：`slide-XX.js`（任务页允许 `slide-task{N}-*.js`） | `ls assets/` 检查 |
| 5 | `createSlide(pres, theme)` 必须**同步**函数 | `node scripts/lint.js` 的 `async-createSlide` 规则 |
| 6 | Theme 5 键：`primary / secondary / accent / light / bg` | compile.js theme 定义 |
| 7 | 颜色 6 位 HEX **无 `#`** | `node scripts/lint.js` 的 `color-hash` 规则 |
| 8 | 不在 hex 中编码 opacity（用 `opacity` 属性） | `node scripts/lint.js` 的 `hex-opacity` 规则 |
| 9 | 中文用 `Microsoft YaHei`,英文用 `Arial` | [slide-techniques.md §2](references/slide-techniques.md) |
| 10 | 字号对比 ≥ 2 倍（标题 ≥ 24pt,正文 12-16pt） | 4.x 节 FONT 常量 |
| 11 | 配色不超过 3 种 + 黑白灰（7:2:1 法则） | [color-system.md](references/color-system.md) |
| 12 | 复用 option 对象 → 用工厂函数 | [common-errors.md](references/common-errors.md) |
| 13 | **文件名要描述性**:`{主题}-{日期}.pptx`,禁止 `presentation.pptx` | compile.js writeFile 路径 |
| 14 | 编译前必须运行 `node scripts/lint.js` 通过（0 error） | `node scripts/lint.js` |
| 15 | 交付前必须通过 🚫 QA 强制门禁 | markitdown + grep（见文末） |

**违反 Hard Constraints 的后果**：

| 违反规则 | 后果 | 紧急程度 |
|---|---|---|
| #1, #4, #5 | 编译失败或文件损坏 | 🔴 高 |
| #2, #3, #6-#10 | 视觉缺陷（元素超出、字号过小、颜色失真） | 🟡 中 |
| #11-#13 | 质量不达标但可运行 | 🟡 中 |
| #14-#15 | 流程缺陷,潜在 bug 流入交付 | 🔴 高 |

### 📝 文字/图形 质量要求（强制）

> 不论生成 SVG 图形还是 PPT 代码,必须满足以下两条质量规范。

**文字质量规范**:
```
✓ 字符完整：无缺损、无乱码
✓ 形态正确：无变形、无扭曲
✓ 尤其针对中文：
  - 笔画清晰,间距均匀
  - 无粘连、无截断
  - 无生僻字替代或问号
```

**图形质量规范**:
```
✓ 线条完整：无断裂、无缺失
✓ 轮廓清晰：无模糊、无锯齿
✓ 边缘平滑：无毛边、无虚影
✓ 结构完整：无截断、无遮挡
```

**生成后自检清单**：
```
□ 所有文字是否清晰可辨？
□ 中文字符是否有乱码/问号/缺失？
□ 图形线条是否完整连续？
□ 线条边缘是否平滑无锯齿？
□ 是否有模糊或虚影区域？
□ 图形轮廓是否清晰锐利？
```

### 🔧 中文文案标点（避免踩坑）

**CJK 标点**（`,。、（）` 等）在 `Microsoft YaHei` 下完美渲染,代码中**直接写即可**：

```javascript
slide.addText("你的 AI 编程伙伴,让写代码更轻松", { ... });
```

**不需要** 替换为 ASCII 逗号/句号。lint 已**移除**对 CJK 标点的检查。

**唯一需要警惕的是 NBSP**(不间断空格,`\u00a0`),通常从 Word、飞书、网页复制时混入。

**一键修复**:
```bash
node scripts/punct-fix.js
```

工具会扫描 `work/` 下所有 `.js` 文件,将 NBSP、智能引号替换为 ASCII 等价。**直接修改文件,无备份,建议先 Git commit**。改完再跑 `node scripts/lint.js` 验收。

### 🛠 工具链（scripts/）一览

| 工具 | 何时跑 | 做什么 |
|------|-------|--------|
| `node scripts/lint.js` | **编译前** | 静态检查:NBSP / `#` 颜色 / 8 位 hex / async createSlide / theme 缺键 |
| `node scripts/punct-fix.js` | lint 报 `invisible-spaces` 时 | 全角标点 → ASCII |
| `python scripts/audit_pptx.py <file.pptx>` | 完工后 | 审计元数据/主题/字体/超链接/敏感度标签,输出 JSON |
| `python scripts/extract_pptx.py <file.pptx>` | 完工后 | 抽文本（含/不含 speaker notes、按页码/范围） |
| `python scripts/extract_images.py <file.pptx>` | 完工后 | 抽图片（支持 group shape 递归） |

---

## Step 4: 代码生成

### 4.0 可视化技术选择（重要）

**核心原则**：简单用 PptxGenJS，复杂用 SVG

```
页面需要图形/图表？
│
├── 不需要 → PptxGenJS 纯文本布局
│
├── 需要简单图形 → PptxGenJS
│   • 基础形状（矩形/圆形/箭头）
│   • 简单图表（柱状/折线/饼图）
│   • 标准文本布局
│
└── 需要复杂图形 → SVG 生成图片插入
    • 甘特图、桑基图、热力图
    • 金字塔、鱼骨图、思维导图
    • 仪表盘、漏斗图、雷达图
    • SWOT、波特五力、2×2矩阵
    • 渐变背景、阴影卡片、特效
```

**SVG 生成方案（简化版）**：

不同于 ai-pptx 的整页 SVG 工作流，ppt-master 采用**局部 SVG 图形**方案：
- 用 PptxGenJS 创建页面框架（标题、页脚等）
- 用 SVG 生成复杂图形区域
- 导出 PNG 插入 PptxGenJS 页面

**使用流程**：

```bash
# Step 1: 阅读 SVG 生成实战指南（必读）
read_file references/svg-generation-guide.md

# Step 2: 选择模板参考
read_file templates/svg-charts/charts_index.json  # 查看可用模板
read_file templates/svg-charts/swot_analysis.svg  # 参考具体结构

# Step 3: 生成 SVG → 导出 PNG → 插入 PPT
```

**代码示例**：

```javascript
const sharp = require('sharp');

// 1. PptxGenJS 创建框架
let slide = pres.addSlide();
slide.addText("SWOT分析", { x: 0.5, y: 0.5, fontSize: 32 });

// 2. 生成 SVG 字符串
const svgString = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">
  <!-- SWOT 四象限 -->
  <rect x="20" y="20" width="370" height="270" rx="8" fill="#E8F5E9"/>
  <rect x="20" y="20" width="370" height="40" rx="8" fill="#4CAF50"/>
  <text x="40" y="48" font-size="20" font-weight="bold" fill="#FFFFFF">优势 S</text>
  <!-- ... 其他内容 -->
</svg>`;

// 3. 导出 PNG
await sharp(Buffer.from(svgString))
  .png()
  .toFile('swot.png');

// 4. 插入 PPT
slide.addImage({
  path: 'swot.png',
  x: 0.5, y: 1.5, w: 9, h: 5.5
});
```

**52种 SVG 模板分类**：

| 类别 | 数量 | 模板示例 | 适用场景 |
|------|------|----------|----------|
| 对比分析 | 8 | bar_chart, waterfall_chart, butterfly_chart | 数据对比、排名 |
| 趋势分析 | 4 | line_chart, area_chart | 时间趋势 |
| 构成分析 | 3 | pie_chart, donut_chart | 占比展示 |
| 指标仪表 | 3 | kpi_cards, gauge_chart | KPI看板 |
| 高级分析 | 8 | radar_chart, heatmap_chart, funnel_chart | 多维分析 |
| 流程项目 | 5 | gantt_chart, timeline, sankey_chart | 项目管理 |
| 战略框架 | 2 | swot_analysis, porter_five_forces | 战略分析 |
| 信息图 | 20 | pyramid_chart, mind_map, fishbone_diagram | 信息可视化 |

### 4.1 项目结构

```bash
slides/
├── slide-01-cover.js
├── slide-02-toc.js
├── ...（每页一个文件）
├── compile.js
└── output/
```

### 4.2 Theme 定义（必须 - 5键结构）

```javascript
const theme = {
  primary: "1A237E",   // 深色，用于标题/深背景
  secondary: "3949AB", // 次深色，用于正文
  accent: "F57C00",     // 强调色
  light: "E8EAF6",      // 浅色
  bg: "FFFFFF"          // 背景
};
```

### 4.3 Slide 模块格式

```javascript
const pptxgen = require("pptxgenjs");

const FONT = "Microsoft YaHei";   // 中文
const FONT_EN = "Arial";          // 英文/数字

// ✅ 必加:slideConfig 元数据,供 compile.js 注册和 lint 校验
const slideConfig = {
  type: 'cover',       // cover | toc | section | content | summary | end
  index: 1,            // 页码
  title: '产品介绍'    // 用于 TOC 自动生成
};

function createSlide(pres, theme, options = {}) {
  const slide = pres.addSlide();
  // ... 幻灯片内容
}

// ✅ 必加:导出 slideConfig
module.exports = { createSlide, slideConfig };
```

**为什么 slideConfig 必加**：
- 配合 [slide-techniques.md §1](references/slide-techniques.md) 自动生成 TOC
- compile.js 可以按 type 分组/排序
- lint 可以按 type 检查必备字段
- 防止出现"compile.js 不知道是封面还是内容页"的混乱状态

**实战代码模式**（数据驱动 + FONT 分离 + slideConfig）见 [slide-techniques.md](references/slide-techniques.md)。

### 4.4 CRAP 原则代码检查清单（强制执行）

**每次生成代码前，必须完成以下检查**：

#### C - 对比 (Contrast)

```javascript
// ✓ 字号对比 ≥ 2倍
const FONT = {
  coverTitle: 54,    // 封面标题
  pageTitle: 32,     // 页面标题 (正文16pt的2倍)
  subtitle: 20,      // 副标题
  body: 16,          // 正文
  caption: 12        // 注释
};

// ✓ 颜色对比（主色vs背景）
// 确保对比度 ≥ 4.5:1
```

#### R - 重复 (Repetition)

```javascript
// ✓ 统一使用 theme 变量，禁止硬编码颜色
slide.addText("标题", { color: theme.primary });     // ✓ 正确
slide.addText("标题", { color: "1A237E" });          // ✗ 错误

// ✓ 统一边距和标题位置
const MARGIN = { left: 0.5, right: 0.5, top: 0.4, bottom: 0.4 };
const HEADER_Y = 0.4;    // 所有页面标题y坐标相同
```

#### A - 对齐 (Alignment)

```javascript
// ✓ 使用网格对齐，禁止随意坐标
const GRID = {
  x: [0.5, 1.25, 2.0, 2.75, 3.5, 4.25, 5.0, 5.75, 6.5, 7.25, 8.0, 8.75],
  y: [0.4, 1.3, 2.2, 3.1, 4.0, 4.9]
};

// ✓ 元素左边缘对齐到网格
slide.addText("文本1", { x: GRID.x[0], y: GRID.y[1] });
slide.addText("文本2", { x: GRID.x[0], y: GRID.y[2] }); // 左对齐
```

#### P - 接近 (Proximity)

```javascript
// ✓ 相关内容间距小（0.2-0.3"）
const SPACING = { tight: 0.2, normal: 0.4, loose: 0.8 };

// ✓ 列表项紧凑排列
items.forEach((item, idx) => {
  slide.addText(item, { y: 1.5 + idx * 0.4 });
});
```

#### 安全区域检查（强制）

```javascript
// ✓ 所有元素必须在安全区域内 [0.5, 0.4] 到 [9.5, 5.225]
// x 必须 ≥ 0.5 且 x + w ≤ 9.5
// y 必须 ≥ 0.4 且 y + h ≤ 5.225
```

### 4.5 Compile 脚本（完整示例）

```javascript
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

// ✅ 必加:metadata 字段（Hard Constraints #1, #13）
pres.author = "PPT Master";
pres.title = "演示文稿";
pres.subject = "Generated with PptxGenJS";

const theme = {
  primary: "1A237E", secondary: "3949AB", accent: "F57C00", light: "E8EAF6", bg: "FFFFFF"
};

// 自动创建 output 目录
const outputDir = path.join(__dirname, "output");
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

const slides = ["slide-01-cover.js", "slide-02-toc.js", /* ... */];
slides.forEach(file => {
  try {
    const mod = require(path.join(__dirname, file));
    mod.createSlide(pres, theme);
    console.log(`✓ ${file}`);   // 每页 OK 提示
  } catch (err) {
    console.error(`✗ ${file}: ${err.message}`); // 单页失败不中断
  }
});

// ✅ 文件名要描述性:{主题}-{日期}.pptx（Hard Constraints #13）
const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, "");
pres.writeFile({ fileName: path.join(outputDir, `q1-product-review-${dateStr}.pptx`) })
  .then(() => console.log("✓ 生成成功"))
  .catch(err => console.error("✗ 失败:", err));
```

**支持的运行模式**（以 `assets/compile.js` 为例）：

```bash
node assets/compile.js                 # 全量编译
node assets/compile.js --list         # 列出所有页面
node assets/compile.js --preview 3     # 预览第 3 页
node assets/compile.js --watch         # 监听模式,文件变动自动重建
node assets/compile.js --name=产品发布    # 自定义文件名前缀（compile-enhanced.js 支持）
node assets/compile.js --theme=./my-theme.js  # 自定义主题（compile-enhanced.js 支持）
```

详细完整版参考：`assets/compile-enhanced.js`(支持 per-slide config)、`assets/compile-v2-base.js`(v2 基础版)。

### ⚠️ 动画声明

**PptxGenJS 不支持动画**。动画需在 PowerPoint 中手动添加。

---

## 预建模板库（22个）

位于 `assets/` 目录，可直接使用或按需修改：

| 类型 | 文件名 | 说明 |
|------|--------|------|
| 封面 | slide-01-cover.js | 居中标准封面 |
| 封面 | slide-01a-cover-split.js | 左右分栏 |
| 封面 | slide-01b-cover-fullimage.js | 全图型 |
| 目录 | slide-02-toc.js | 垂直列表 |
| 目录 | slide-02a-toc-grid.js | 双栏网格 |
| 章节 | slide-03-section.js | 标准章节页 |
| 章节 | slide-03-section-enhanced.js | 增强章节页 |
| 内容 | slide-04-content.js | 标准内容页 |
| 内容 | slide-04a-content-card.js | 卡片式 |
| 内容 | slide-04b-content-image-text.js | 图文左右 |
| 内容 | slide-04c-content-chart.js | 图表页 |
| 内容 | slide-04d-content-timeline.js | 时间轴 |
| 内容 | slide-04e-content-compare.js | 对比式 |
| 内容 | slide-04f-content-table.js | 表格页 |
| 总结 | slide-05-summary.js | 标准总结页 |
| 总结 | slide-05-summary-enhanced.js | 增强总结页 |
| 结束 | slide-06-end.js | 标准结束页 |
| 结束 | slide-06-end-enhanced.js | 增强结束页 |
| 图表 | chart-bar.js | 柱状图 |
| 图表 | chart-line.js | 折线图 |
| 图表 | chart-pie.js | 饼图 |

**每个模板特性**：
- 独立预览脚本（`node slide-04a-preview.js` 直接生成单页）
- Q4 记忆点设计
- PptxGenJS 兼容性标注

---

## 实战案例（真实项目代码）

> ⚠️ **22 个预建模板是"骨架"** —— 演示版式和结构,但**没有真实内容**。
> 想看"真实项目里代码长什么样",见 [references/cases/real-project-example/](references/cases/real-project-example/)：
>
> - 10 个 slide JS（封面/目录/痛点/能力1-3/场景/对比/总结）
> - 1 个 compile.js（已改通用,可直接 `node compile.js` 跑）
> - 1 个 README.md（说明怎么用、能学到什么）
>
> **能学到的实战模式**（见 [slide-techniques.md](references/slide-techniques.md)）：
> - §4 假渐变背景（slide-01-cover）
> - §5 数据驱动卡片（slide-03/05/06/07）
> - §6 大编号装饰（slide-04）
> - §7 对比表（slide-09）
> - §8 记忆点数据（每页都有）
>
> 💡 **3 类案例互补**：
> - 理论案例([huawei/apple/ted 拆解](references/cases/))→ 学"什么是好设计"
> - 反面案例([failed-bp/10-failure-patterns](references/cases/))→ 学"什么是不能做的"
> - **实战案例**(本节)→ 学"好设计怎么变成可运行代码"

---

## SVG 高级图形生成指南

### 核心区别：ai-pptx vs ppt-master

| 维度 | ai-pptx | ppt-master（我们的简化方案） |
|------|---------|----------------------------|
| 生成目标 | 整页 SVG 幻灯片 | **局部 SVG 图形** |
| 工作流程 | 多角色协作（Strategist→Executor） | **单步骤直接生成** |
| 后处理 | finalize_svg.py + svg_to_pptx.py | **sharp 直接导出 PNG** |
| 复杂度 | 高 | **简化** |

**ppt-master SVG 方案核心**：
```
PptxGenJS 创建页面框架（标题/页脚）
          ↓
SVG 生成复杂图形（图表/信息图）
          ↓
sharp 导出 PNG
          ↓
PptxGenJS 插入图片
```

### 52种 SVG 模板参考

位于 `templates/svg-charts/` 目录，**不要直接复制，只作为结构参考**。

| 需求 | 推荐模板 | 路径 |
|------|----------|------|
| 项目进度 | 甘特图 | `svg-charts/gantt_chart.svg` |
| SWOT分析 | 四象限图 | `svg-charts/swot_analysis.svg` |
| 能力评估 | 雷达图 | `svg-charts/radar_chart.svg` |
| 转化漏斗 | 漏斗图 | `svg-charts/funnel_chart.svg` |
| KPI看板 | 仪表盘 | `svg-charts/kpi_cards.svg` |
| 战略层级 | 金字塔 | `svg-charts/pyramid_chart.svg` |
| 因果分析 | 鱼骨图 | `svg-charts/fishbone_diagram.svg` |
| 知识框架 | 思维导图 | `svg-charts/mind_map.svg` |

### 使用步骤

**Step 1**: 阅读 SVG 生成实战指南（必读）
```bash
read_file references/svg-generation-guide.md
```

**Step 2**: 参考模板结构（不要复制颜色）
```bash
read_file templates/svg-charts/charts_index.json  # 查看有哪些模板
read_file templates/svg-charts/swot_analysis.svg  # 参考具体结构
```

**Step 3**: 生成 SVG 代码
- 理解模板布局逻辑
- 使用项目配色方案
- 填充实际数据

**Step 4**: 导出 PNG 并插入
```javascript
const sharp = require('sharp');

// 生成 SVG 字符串
const svgString = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">
  <!-- 你的 SVG 代码 -->
</svg>`;

// 导出 PNG
await sharp(Buffer.from(svgString))
  .png()
  .toFile('graphic.png');

// 插入 PPT
slide.addImage({ path: 'graphic.png', x: 0.5, y: 1.5, w: 9, h: 4.5 });
```

### 完整分类

详见 `templates/svg-charts/charts_index.json`：
- 8种对比图表、4种趋势图表、3种构成图表
- 3种指标仪表、8种高级分析、5种流程项目
- 2种战略框架、20种信息图

### 文档索引

| 文档 | 用途 |
|------|------|
| [svg-generation-guide.md](references/svg-generation-guide.md) | **SVG 生成实战指南**（代码示例、技术规范） |
| [svg-graphics-guide.md](references/svg-graphics-guide.md) | 52种模板详细说明（分类、场景、决策树） |

### 快速预览命令

```bash
# 单页预览（进入 assets 目录）
cd assets
node slide-04a-content-card.js        # 生成单页 preview.pptx
node slide-04d-content-timeline.js
node chart-bar.js

# 全量编译
node compile-enhanced.js               # 生成 output/presentation.pptx
```

### 模板索引速查

| 场景需求 | 推荐模板 | 命令 |
|----------|----------|------|
| 需要一页数据对比 | slide-04f-content-table.js | `node slide-04f-content-table.js` |
| 需要时间轴/流程 | slide-04d-content-timeline.js | `node slide-04d-content-timeline.js` |
| 需要三栏对比 | slide-04a-content-card.js | `node slide-04a-content-card.js` |
| 需要图文混排 | slide-04b-content-image-text.js | `node slide-04b-content-image-text.js` |
| 需要柱状图 | chart-bar.js | `node chart-bar.js` |
- PptxGenJS 兼容性标注
- 可配置参数说明

---

## References 文件索引（按使用时机重组）

### must-read（每次必读）

| 文件 | 核心内容 |
|------|----------|
| [design-principles.md](references/design-principles.md) | CRAP四原则、字号对比、对齐方式 |
| [color-system.md](references/color-system.md) | 配色7:2:1法则、行业配色18套 |
| [three-dimensions.md](references/three-dimensions.md) | 三维体系：难忘感·设计感·仪式感 |
| **[slide-techniques.md](references/slide-techniques.md)** | **实战代码模式**：slideConfig/假渐变/数据驱动（从 A 真实项目沉淀） |

### scenario-specific（按场景必须读）

| 文件 | 适用场景 |
|------|----------|
| [scenarios/academic.md](references/scenarios/academic.md) | 学术汇报、论文答辩 |
| [scenarios/commercial.md](references/scenarios/commercial.md) | 产品发布、路演 |
| [scenarios/training.md](references/scenarios/training.md) | 培训课件、教学 |
| [scenarios/workplace.md](references/scenarios/workplace.md) | 工作汇报、述职 |

### on-demand（按需查阅）

| 文件 | 主要内容 |
|------|----------|
| [philosophy.md](references/philosophy.md) | 字体性格论、10%理论、简约大道 |
| [techniques.md](references/techniques.md) | 36计、图片处理12法、动画三大作用 |
| [case-studies.md](references/case-studies.md) | 案例分析（带场景标注） |
| [thinking.md](references/thinking.md) | 五种思维、KANO模型、观众分级 |
| [pptxgenjs.md](references/pptxgenjs.md) | PptxGenJS API详解 |
| [charts.md](references/charts.md) | 图表制作指南 |
| [svg-generation-guide.md](references/svg-generation-guide.md) | **SVG 生成与插入实战（代码示例）** |
| [svg-graphics-guide.md](references/svg-graphics-guide.md) | 52种 SVG 模板详细说明 |
| [layout-system.md](references/layout-system.md) | 版式系统详解 |
| [slide-types.md](references/slide-types.md) | 幻灯片类型指南 |
| [common-errors.md](references/common-errors.md) | 常见错误与修复 |
| [editing.md](references/editing.md) | PPT编辑技巧 |
| [quality-checklist.md](references/quality-checklist.md) | 完整质量检查清单 |
| [speech-preparation.md](references/speech-preparation.md) | 演讲准备完整指南 |
| [narrative-arc.md](references/narrative-arc.md) | 叙事弧模板（内容结构化） |
| [accessibility.md](references/accessibility.md) | 无障碍设计检查清单 |
| [extended-themes.md](references/extended-themes.md) | 扩展配色方案参考 |

---

## 📚 完整文档索引

> ⚠️ **重要**：详细文档请查看 [references/README.md](references/README.md)

**快速分类**：
| 类别 | 位置 | 说明 |
|------|------|------|
| 案例库 | [references/cases/](references/cases/) | 理论(华为/苹果/TED)+ 反面(failed-bp) + **实战([real-project-example](references/cases/real-project-example/))** |
| 核心方法论 | [references/](references/) | design-principles, color-system, layout-system等 |
| 场景指南 | [references/scenarios/](references/scenarios/) | academic/commercial/training/workplace |

---

## QA 验证建议

```bash
# 1. 编译前 lint（Hard Constraints #14, 必跑）
node scripts/lint.js
# 2. 标点规范化（如 lint 报错）
node scripts/punct-fix.js

# 3. 全量编译
node assets/compile.js

# 4. 编译后审计（Hard Constraints #15, 必跑）
python scripts/audit_pptx.py output/presentation.pptx
python scripts/audit_pptx.py output/presentation.pptx --sections themes,hyperlinks

# 5. 提取文本（验证内容完整性）
python -m markitdown output/presentation.pptx
# 6. 检查 placeholder 残留
python -m markitdown output/presentation.pptx | grep -iE "xxxx|lorem|ipsum|placeholder"
# 7. 提取图片（资产复核）
python scripts/extract_images.py output/presentation.pptx --output-dir ./extracted

# 8. 章节结构（PowerPoint 大纲视图）
# 9. ⚠️ 动画需手动添加
```

---

## 更新日志

| 日期 | 变更 |
|------|------|
| 2026-06-01 | **A → B 反哺融合**：新增 `scripts/` 工具链（lint/punct-fix/audit/extract）、新增 [slide-techniques.md](references/slide-techniques.md) 实战技巧、新增 ★ Step 4 前置 质量门禁（Hard Constraints 15 条 + 文字/图形质量要求 + CJK 标点规范）、4.3 Slide 模块增加 slideConfig 强制规范 |
| 2026-04-29 | 新增叙事弧模板（narrative-arc.md） |
| 2026-04-29 | 新增无障碍设计清单（accessibility.md） |
| 2026-04-29 | 新增扩展配色方案（extended-themes.md） |
| 2026-04-18 | 修复关键缺陷：新增安全边距规范和网格系统（pptxgenjs.md），新增 CRAP 原则代码检查清单（SKILL.md 4.4 节） |
| 2026-04-18 | 新增 SVG 高级图形文档索引（svg-generation-guide.md、svg-graphics-guide.md） |
