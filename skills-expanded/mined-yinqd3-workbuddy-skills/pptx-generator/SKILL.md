---
name: pptx-generator
description: "生成、编辑、读取 PowerPoint 演示文稿。支持用 PptxGenJS 从零创建（封面、目录、内容页、章节分隔页、总结页），通过 XML 工作流编辑已有 PPTX，或使用 markitdown 提取文本。触发器：PPT, PPTX, PowerPoint, 演示文稿, 幻灯片, 幻灯片组。"
license: MIT
agent_created: true
metadata:
  version: "1.2"
  category: productivity
  source: "MiniMax-AI/skills 仓库（经授权安装），实战反馈修正 v1.2"
  sources:
    - https://gitbrent.github.io/PptxGenJS/
    - https://github.com/microsoft/markitdown
---

# PPTX Generator & Editor

## Overview

本 Skill 处理所有 PowerPoint 任务：读取/分析已有演示文稿、通过 XML 操作编辑基于模板的演示文稿，以及使用 PptxGenJS 从零创建演示文稿。内置完整的设计系统（调色板、字体、风格配方）和每种幻灯片类型的详细指南。

## Quick Reference

| 任务 | 方式 |
|------|------|
| 读取/分析内容 | `python -m markitdown presentation.pptx` |
| 编辑或基于模板创建 | 见 [Editing Presentations](references/editing.md) |
| 从零创建 | 见下方 [从零创建工作流](#creating-from-scratch-workflow) |

| 项目 | 值 |
|------|------|
| **画布尺寸** | 10" x 5.625" (LAYOUT_16x9) |
| **颜色格式** | 6 位十六进制，不带 #（例如 `"FF0000"`） |
| **英文字体** | 微软雅黑（中文PPT建议全篇统一） |
| **中文字体** | 微软雅黑 |
| **页码徽章位置** | x: 9.3", y: 5.1" |
| **基础主题键** | `primary`, `secondary`, `accent`, `light`, `bg` |
| **可选扩展键** | `gold`, `coral`, `violet`（根据需要添加） |
| **形状** | RECTANGLE, OVAL, LINE, ROUNDED_RECTANGLE |
| **图表** | BAR, LINE, PIE, DOUGHNUT, SCATTER, BUBBLE, RADAR |

## 参考文件

| 文件 | 内容 |
|------|------|
| [slide-types.md](references/slide-types.md) | 5 种幻灯片页面类型（封面、目录、章节分隔、内容、总结）+ 附加布局模式 |
| [design-system.md](references/design-system.md) | 调色板、字体参考、风格配方（Sharp/Soft/Rounded/Pill）、排版与间距 |
| [editing.md](references/editing.md) | 基于模板的编辑工作流、XML 操作、格式化规则、常见陷阱 |
| [pitfalls.md](references/pitfalls.md) | QA 流程、常见错误、关键 PptxGenJS 陷阱 |
| [pptxgenjs.md](references/pptxgenjs.md) | 完整的 PptxGenJS API 参考 |

---

## 读取内容

```bash
# 文本提取
python -m markitdown presentation.pptx
```

---

## 从零创建 — 工作流

**当没有模板或参考演示文稿时使用。**

### 第 1 步：调研需求

搜索以理解用户需求 — 主题、受众、目的、语气、内容深度。

### 第 2 步：选择调色板与字体

使用 [调色板参考](references/design-system.md#color-palette-reference) 选择与主题和受众匹配的调色板。使用 [字体参考](references/design-system.md#font-reference) 选择字体配对。

### 第 3 步：选择设计风格

使用 [风格配方](references/design-system.md#style-recipes) 选择与演示文稿基调相匹配的视觉风格（Sharp, Soft, Rounded 或 Pill）。

### 第 4 步：规划幻灯片大纲

将**每一张幻灯片**精确分类为 [5 种页面类型](references/slide-types.md) 之一。规划每张幻灯片的内容和布局。确保视觉多样性 — 不要在不同幻灯片上重复相同布局。

### 第 5 步：生成幻灯片 JS 文件

在 `slides/` 目录下为每张幻灯片创建一个 JS 文件。每个文件必须导出一个同步的 `createSlide(pres, theme)` 函数。遵循 [幻灯片输出格式](#slide-output-format) 和 [slide-types.md](references/slide-types.md) 中的类型特定指南。如果有 subagent，最多同时生成 5 张幻灯片。

**告诉每个 subagent：**
1. 文件命名：`slides/slide-01.js`, `slides/slide-02.js` 等
2. 图片存放：`slides/imgs/`
3. 最终 PPTX 存放：`slides/output/`
4. 尺寸：10" x 5.625" (LAYOUT_16x9)
5. **字体：全部统一使用 微软雅黑**（包括英文、数字、中文混排场景）
6. 颜色：6 位十六进制，不带 #（例如 `"FF0000"`）
7. 必须使用 theme 对象契约（见 [Theme 对象契约](#theme-object-contract-mandatory)）
8. 必须遵循 [PptxGenJS API 参考](references/pptxgenjs.md)
9. 中文文本字符串使用单引号包裹，避免双引号嵌套问题
10. **严格遵循布局间距规则**（见下方 [布局防重叠规则](#布局防重叠规则)），每个 slide 生成后必须做 Y 轴重叠检查

**大规模 PPTX（30+ 张幻灯片）并行生成策略：**
- 启动 8-9 个 subagent 并行生成，每个负责 ~5 张幻灯片
- 均分场景覆盖：封面/分隔页分配给专门的 agent，内容页按顺序均分
- 每个 subagent 必须遵循相同的 theme 契约和 slide 模板
- 最后 compile.js 合并所有 slide 模块

---

## 布局防重叠规则（强制）

**内容页垂直布局每层元素的底部必须严格小于下一层元素的顶部。** 常见重叠场景和标准解法如下：

### 顶部区域（y: 0 ~ 1.8）三层结构

```
┌─ 行 1: 章节标签 ─┬── y_min=0.30, h_max=0.25, 底部≤0.55
├─ 行 2: 页面标题 ─┬── y_min=0.75, h_max=0.50, fontSize_max=26
├─ 行 3: 副标题 ───┬── y_min=1.40, h_max=0.30, fontSize_max=14
└─── 之后的内容 ───┬── y≥1.85
```

| 元素 | 最小 y | 最大 h | 最大字号 | 说明 |
|------|--------|--------|---------|------|
| 章节标签 | 0.30" | 0.25" | 13pt | 紧凑显示 |
| 页面标题 | 0.75" | 0.50" | **26pt** | 长标题会换行，用小字号保证一行显示 |
| 副标题 | 1.40" | 0.30" | 14pt | 灰色/辅助色 |

### 相邻元素垂直间距规则

| 场景 | 最小间距 | 说明 |
|------|---------|------|
| 标题底部 → 副标题顶部 | ≥ 0.15" | 防止文字串行重叠 |
| 副标题底部 → 卡片/形状顶部 | ≥ 0.15" | 副标题与内容块之间 |
| 卡片底部 → 反馈循环文本 | ≥ 0.15" | 流程图中箭头文本 |
| 内容底部 → 总结面板顶部 | ≥ 0.10" | 底部总结框 |
| 总结面板底部 → 页码徽章 | ≥ 0.05" | 最后一行的间距 |

### 容器内元素不越界规则

**卡片/组内的子元素必须完全在容器边界内。** 这是编写自定义函数时最容易出错的地方。

```
例如: 靶心图（2×2网格）
┌─────────────────────┐
│  卡片框 (cx±1.05, cy±0.8)     │
│  ├── 靶心环 (cx±0.32)       │  ← ✅ 在卡片内
│  └── 弹孔 (cx+dx, cy+dy)    │  ← ⚠️ dx,dy 必须在 ±0.77 内
│      标注 (cy+0.4~0.8)      │  ← ✅ 在卡片内
└─────────────────────┘
```

**容器内元素边界检查清单：**
- [ ] 所有子元素的 x ≥ 容器.x 且 x+w ≤ 容器.x+容器.w
- [ ] 所有子元素的 y ≥ 容器.y 且 y+h ≤ 容器.y+容器.h
- [ ] 相对坐标（如 cx+dx, cy+dy）的偏移量不超出容器的半宽/半高
- [ ] 卡片内的标注/描述文本完整可见，不被卡片边界裁剪

### 水平边界规则

**幻灯片画布为 10" × 5.625"，所有元素必须在画布范围内：**

| 规则 | 条件 | 后果 |
|------|------|------|
| **左边界** | 任何元素的 `x ≥ 0` | x 为负则内容被裁剪 |
| **右边界** | **任何元素的 `x + w ≤ 10`** | 超右则内容被裁剪 |
| **上边界** | `y ≥ 0` | 同上 |
| **下边界** | `y + h ≤ 5.625` | 超下则内容被裁剪 |
| **安全边距** | 建议 `x ≥ 0.4`, `x + w ≤ 9.6` | 打印/投影仪可能裁边 |

**常见越界场景：**
- 时间线/卡片布局：最后一个节点的卡片右边缘超过 10"
  ```javascript
  // ❌ 越界：cx + cardW/2 > 10"
  // ✅ 修正：缩减 totalW 或增大 startX
  const totalW = 7.5;  // 不够宽？用 7.5
  const startX = 1.0;  // 不靠左？用 1.0
  // 验证：startX + totalW + cardW/2 ≤ 10
  ```
- 文本框内容太长：建议使用 `fit: "shrink"` 自动缩小文本
  ```javascript
  slide.addText("长标题文字", { x: 0.5, y: 2, w: 9, h: 0.6, fontSize: 24, fit: "shrink" });
  ```

### 重叠快速自查清单

生成每张 slide 后，逐项检查：
- [ ] 章节标签底部(y+h) < 标题顶部(y) ？（至少 0.10" 间隙）
- [ ] 标题底部(y+h) < 副标题顶部(y) ？（至少 0.15" 间隙）
- [ ] 副标题底部(y+h) < 卡片/形状的 yStart ？
- [ ] 所有 "STEP" 标签的底部低于上一层元素的底部？
- [ ] 页码徽章不在任何内容框的范围内？
- [ ] 标题文本的 fontSize ≤ 26pt（内容页）？
- [ ] 所有元素的 x ≥ 0 且 x+w ≤ 10？
- [ ] 对称布局（如多卡片时间线）的最左和最右卡片不超出边界？
- [ ] 底部面板的底部(y+h) ≤ 5.3，给页码徽章留空间？
- [ ] 自定义函数中的子元素（弹孔/图标）不超出父容器边界？

### 关于 fontSize 的硬性上限

| 元素 | 上限 | 原因 |
|------|------|------|
| 内容页标题 | 26pt | 长中文标题（15-20字）在 9" 宽空间内一行显示 |
| 章节分隔页标题 | 32pt | 标题较短，可以稍大 |
| 封面主标题 | 48-54pt | 封面空间大 |
| 副标题/描述 | 14pt | 辅助文本，不需要大字号 |
| 卡片内标题 | 16-18pt | 卡片空间有限 |
| 卡片内正文 | 10-12pt | 紧凑信息展示 |
| 表格/代码内容 | 9-11pt | 密集数据场景 |

## 上下文感知布局规则（v1.2 新增）

以下规则无法通过纯坐标检查发现，需要结合文本内容和容器边界做语义判断：

### Rule A: 标签行文换行检测 + 页码基线对齐

**问题：** 标签文本（如 `PART 01`、`STEP N` 等）因容器宽度不足导致自动折行，或页码徽章与相邻底部面板的文字基线不齐。

**标准解法：**
```
❌ 错误：w=0.55 的标签框放 "PART 01"（7字符 @ 10pt）→ 可能折行为 "PAR" / "T 01"
✅ 正确：w≥0.65 或 fontSize≤9pt，确保标签文字单行完整显示
```

| 场景 | 最小宽度 | 最大字号 | 说明 |
|------|---------|---------|------|
| "PART 01" 类 | 0.65" | 9pt | 7字符标签，窄框易折行 |
| "STEP 1" 类 | 0.55" | 10pt | 6字符以内 |
| 3字符标签 | 0.40" | 11pt | 如 "01"、"A" 等 |

**页码徽章基线对齐检查：**
- 页码徽章的垂直中心线应与相邻底部面板的文字基线对齐
- 底部面板 `y + h/2` ≈ 页码徽章 `y + h/2`（差值 ≤ 0.05"）
- 徽章不应与面板重叠：面板右边缘 x+w ≤ 徽章 x（或徽章 x 在面板右侧）

### Rule B: 时间线上方元素重叠检测

**问题：** 时间线布局中，年份/标签文字（位于时间线上方）与标题区或副标题区域重叠。

**标准解法：**
```
时间线 Y 轴布局模板：
┌─ 标题 ─────────────┬── y=0.60~0.70, 底部≤1.05
├─ 副标题 ───────────┬── y=1.00~1.10, 底部≤1.30
├─ 年份标签 ─────────┬── y≥1.20 (副标题底部), h=0.30
├─ 时间线 ───────────┬── y≥1.65, 圆圈中心在时间线上
├─ 卡片/节点 ────────┬── y=时间线底部+0.3~0.4
└─ 底部面板 ─────────┬── y≥4.0
```

**检查清单：**
- [ ] 年份标签顶部 y ≥ 副标题底部 y（至少 0.05" 间隙）
- [ ] 时间线节点卡片的内容（描述文字）不超出卡片边界
- [ ] 最下方节点/卡片的底部 ≤ 底部面板的顶部 - 0.15"

### Rule C: 卡片头部边界检测 + 行内文字重叠

**问题：**
1. 引用文本/副标题与大标题位于同一行（同一 y 坐标），视觉上相互重叠
2. 卡片头部标题文字（中文 + 英文混排）溢出卡片头部的彩色背景区域

**标准解法：**
```
// ❌ 错误：引用文本与大标题同一行
slide.addText("大标题", { x: 0.65, y: 0.52, w: 6, h: 0.35, fontSize: 22 });
slide.addText("· 引用文本", { x: 3.4, y: 0.52, w: 5, h: 0.35, fontSize: 14 }); // ← 重叠！

// ✅ 正确：引用文本放在单独一行
slide.addText("大标题", { x: 0.65, y: 0.52, w: 6, h: 0.35, fontSize: 22 });
slide.addText("· 引用文本", { x: 0.65, y: 0.95, w: 6, h: 0.3, fontSize: 14 }); // ← 新行
```

**卡片头部溢出检测：**
- 卡片头部标题文本框的右边缘（x + w）不得超出卡片头部的彩色背景区域
- 中文 + 英文混排时，英文部分会使文本总宽度超出预期 → 使用 `fit: "shrink"` 或减小字号
- 头部文本字号建议：中英文混排 ≤ 11pt，纯中文 ≤ 12pt

### Rule D: 底部边缘碰撞检测 + 垂直间距均匀分布

**问题：** 容器（卡片、面板）内的最后一行文字几乎接触到容器底部边界；中间区域的元素间距过于拥挤。

**标准解法：**
```
容器内文字垂直分布：
┌─────────────────────┐
│  标题 (y+0.08~0.15)  │  ← 顶部留空
│  主文字 (y+0.35~0.45) │  ← 间距 0.20~0.30"
│  描述 (y+0.70~0.80)   │  ← 间距 0.25~0.35"
│  ░░░ 底部安全边距 ░░░ │  ← 至少 0.10" 留白
└─────────────────────┘
```

**卡片内垂直间距规则：**

| 区域 | 距卡片顶部 | 间距 | 说明 |
|------|-----------|------|------|
| 头部标签 | 0.08~0.15" | — | 卡片内部标题 |
| 主文字 | 0.35~0.45" | 0.20~0.30" | 大号强调文字 |
| 描述文字 | 0.70~0.80" | 0.25~0.35" | 更靠近底部 |
| 底部安全边距 | — | ≥ 0.10" | 文字底部到卡片底部 |

**中间区域拥挤检测：**
- 当一页有多个并行元素（如 3 张卡片）时，确保元素间的垂直间距 ≥ 0.15"
- 元素内部文字不超出底部边界（最后一行文字底部 ≤ 元素底部 - 0.10"）
- 卡片内最后一行文字的 fontSize 适配：长文本使用 11pt，确保在有限宽度内不换行

### Rule E: 列表/概念图方框文字适配

**问题：** 列表项（bullet items）或概念图方框内的多行文字总高度超出文本框高度，导致文字被裁剪。

**标准解法：**
```
// 计算所需高度
const lineCount = items.length;
const lineHeight = fontSize * lineSpacingMultiple / 72;  // pt → inches
const requiredH = lineCount * lineHeight + 0.10;  // + 底部边距

// 检查：textBox.h ≥ requiredH
if (textBox.h < requiredH) {
  // 修复选项：
  // 1. 增加卡片高度
  // 2. 减小 fontSize
  // 3. 减小 lineSpacingMultiple
}
```

**列表项高度速查表：**

| 条目数 | 字号 | 行间距倍率 | 所需高度 | 建议框高 |
|-------|------|-----------|---------|---------|
| 5 项 | 12pt | 1.6 | 1.33" | ≥ 1.45" |
| 5 项 | 11pt | 1.5 | 1.15" | ≥ 1.30" |
| 4 项 | 12pt | 1.6 | 1.07" | ≥ 1.20" |
| 3 项 | 12pt | 1.6 | 0.80" | ≥ 0.95" |
| 3 项 | 11pt | 1.5 | 0.69" | ≥ 0.85" |

**验证方法：**
- 使用 PptxGenJS 的 `fit: "shrink"` 作为保险（但不要依赖它作为唯一手段）
- 生成后通过 python-pptx 解析每张 slide 的文本框高度和内容行数做验证
- 如果页面布局复杂（顶部卡片 + 中部概念图 + 底部面板），确保所有元素之间有合理的垂直间隙

---

### 第 6 步：编译为最终 PPTX

创建 `slides/compile.js` 来合并所有幻灯片模块：

```javascript
// slides/compile.js
const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

const theme = {
  primary: "003D24",    // 最深色，用于深色背景/标题
  secondary: "6B4FCF",  // 次要强调色（紫色）
  accent: "006A3F",     // 主强调色（墨绿）
  light: "A8D5BA",      // 浅色强调
  bg: "FFFFFF",         // 背景色（学术PPT建议白色）
  // 可选扩展键（根据需要添加）：
  gold: "C49A2A",       // 金色 - 页号角标/特殊强调
  coral: "C2411F"       // 珊瑚红 - 警告/错误标识
};

for (let i = 1; i <= 43; i++) {
  const num = String(i).padStart(2, '0');
  const slideModule = require(`./slide-${num}.js`);
  slideModule.createSlide(pres, theme);
}

pres.writeFile({ fileName: './output/presentation.pptx' });
```

运行：`cd slides && NODE_OPTIONS= node compile.js`
（注意：如果遇到 `--use-system-ca is not allowed in NODE_OPTIONS` 错误，需要清空该环境变量）

### 第 7 步：QA（必需）

参见 [QA 流程](references/pitfalls.md#qa-process)。

### 输出结构

```
slides/
├── slide-01.js          # 幻灯片模块
├── slide-02.js
├── ...
├── imgs/                # 幻灯片中使用的图片
└── output/              # 最终产物
    └── presentation.pptx
```

---

## 幻灯片输出格式

每张幻灯片是一个**完整的、可运行的 JS 文件**：

```javascript
// slide-01.js
const pptxgen = require("pptxgenjs");

const slideConfig = {
  type: 'cover',
  index: 1,
  title: '演示文稿标题'
};

// 必须是同步的（不能是 async）
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addText(slideConfig.title, {
    x: 0.5, y: 2, w: 9, h: 1.2,
    fontSize: 48, fontFace: "微软雅黑",
    color: theme.primary, bold: true, align: "center"
  });

  return slide;
}

// 独立预览 — 使用幻灯片特定的文件名
if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  const theme = {
    primary: "22223b",
    secondary: "4a4e69",
    accent: "9a8c98",
    light: "c9ada7",
    bg: "f2e9e4"
  };
  createSlide(pres, theme);
  pres.writeFile({ fileName: "slide-01-preview.pptx" });
}

module.exports = { createSlide, slideConfig };
```

---

## Theme 对象契约（强制）

编译脚本传递一个 theme 对象。以下 **5 个键是必须的**，可以根据需要**增加额外的键**（如 `gold`, `coral`, `violet` 等）：

| 键 | 用途 | 示例 |
|-----|---------|-------|
| `theme.primary` | 最深色，用于深色背景/标题 | `"003D24"` |
| `theme.secondary` | 次要强调色 | `"6B4FCF"` |
| `theme.accent` | 主强调色（装饰条/标识/高亮） | `"006A3F"` |
| `theme.light` | 浅色强调（辅助文字/浅填色） | `"A8D5BA"` |
| `theme.bg` | 背景色（学术PPT建议白色） | `"FFFFFF"` |

**必须包含以上 5 键，但可以扩展**。例如可以添加 `gold`, `coral`, `violet` 等键用于特殊场景。

---

## ⚠️ PptxGenJS v3.x 关键陷阱（必读）

以下的踩坑经验来自于实战，严重程度较高，请在生成幻灯片时严格遵守：

### 1. 使用 `pres.shapes.*` 而非 `pres.ShapeType.*`
PptxGenJS v3.x 不支持 `pres.ShapeType.RECTANGLE`，必须使用 `pres.shapes.RECTANGLE`：
```javascript
// 正确
slide.addShape(pres.shapes.RECTANGLE, { ... });
slide.addShape(pres.shapes.OVAL, { ... });
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { ... });

// 错误（v3.x 中不存在）
slide.addShape(pres.ShapeType.RECTANGLE, { ... });
```

### 2. `slide.background` 使用 `{ color: ... }` 而非 `{ fill: ... }`
```javascript
// 正确
slide.background = { color: "FFFFFF" };
slide.background = { color: theme.primary };

// 错误（会被静默忽略，幻灯片背景透明）
slide.background = { fill: "FFFFFF" };
slide.background = { fill: { color: "FFFFFF" } };
```

### 3. 项目符号用 `bullet: true`，不要用 `bullet: { code: "•" }`
```javascript
// 正确
{ text: "第一项", options: { bullet: true, breakLine: true } }

// 错误（不支持 code 属性）
{ text: "第一项", options: { bullet: { code: "•" } } }
```

### 4. 中文文本使用单引号包裹
如果中文文本中包含双引号（如"关键"、"注意"等），用双引号包裹会产生 SyntaxError：
```javascript
// 正确
slide.addText('模型判断"我对哪些样本最不确定"', { ... });

// 错误（字符串内的双引号未转义）
slide.addText("模型判断"我对哪些样本最不确定"", { ... });
```

### 5. 运行 `node compile.js` 时清空 NODE_OPTIONS
```bash
cd slides && NODE_OPTIONS= node compile.js
```

---

## 页码徽章（必需）

**除封面页外**的所有幻灯片**必须**在右下角包含页码徽章。

- **位置**：x: 9.3", y: 5.1"
- 只显示当前页码（如 `3` 或 `03`），不要显示 "3/12"
- 使用调色板颜色，保持微妙

### 圆形徽章（默认）

```javascript
slide.addShape(pres.shapes.OVAL, {
  x: 9.3, y: 5.1, w: 0.4, h: 0.4,
  fill: { color: theme.accent }
});
slide.addText("3", {
  x: 9.3, y: 5.1, w: 0.4, h: 0.4,
  fontSize: 12, fontFace: "微软雅黑",
  color: "FFFFFF", bold: true,
  align: "center", valign: "middle"
});
```

### 胶囊形徽章

```javascript
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 9.1, y: 5.15, w: 0.6, h: 0.35,
  fill: { color: theme.accent },
  rectRadius: 0.15
});
slide.addText("03", {
  x: 9.1, y: 5.15, w: 0.6, h: 0.35,
  fontSize: 11, fontFace: "微软雅黑",
  color: "FFFFFF", bold: true,
  align: "center", valign: "middle"
});
```

---

## 依赖项

- `pip install "markitdown[pptx]"` — 文本提取
- `npm install -g pptxgenjs` — 从零创建
- `npm install -g react-icons react react-dom sharp` — 图标（可选）
