---
name: screenshot-to-design-system
description: >-
  Extracts color tokens and component styles from UI screenshots by reading each
  control region individually (not full-page layout). Generates a complete design
  system demo with tokens.css and components.html. Ignores backgrounds and icons.
  Use when the user uploads a UI screenshot, asks for design tokens, color palette
  extraction, or component library generation from a reference image.
disable-model-invocation: true
metadata:
  author: WCF900905
  version: "1.1.0"
  open-standard: https://agentskills.io
  agents: cursor, claude-code, codex
---

# Screenshot to Design System

Compatible with [Agent Skills](https://agentskills.io) tools: **Cursor** (`~/.cursor/skills/`), **Claude Code** (`~/.claude/skills/`), **OpenAI Codex** (`~/.agents/skills/`). Install: `curl -fsSL .../scripts/install.sh | bash`

从参考图中**逐个读取控件区域**（非整页），提取配色 token 与控件样式，生成控件库 Demo。**不还原页面布局**，只关心控件与配色；**忽略背景与 icon**。

## 核心原则：读控件，不读页面

| 读 | 不读 |
|----|------|
| 截图中每个独立控件的样式 | 整页布局、页面背景、装饰层 |
| 控件自身的填充色、边框、圆角、阴影、字号 | 状态栏、导航栏所在「页面」结构 |
| 控件之间的样式规律（归纳 token） | 控件在页面中的位置关系 |

输入可以是 App 截图、控件展示板、设计稿局部——**一律按控件区域处理**，不按整屏页面处理。

## 范围

| 提取 | 忽略 |
|------|------|
| 各控件区域的配色、尺寸、圆角、阴影 | 页面背景图、渐变底、插画 |
| 控件形状与变体 | icon 图形、logo、头像内容 |
| 文字层级（来自控件内文案） | 地图、3D、复杂装饰 |

整页高保真复刻 → 转用 `image2_UI_skill`。

## 输出

`demo/<slug>/`：

```
tokens.json / tokens.css
components-list.md
style-guide.html / components.html
analysis.md / ui-review-report.md
reference.png / screenshots/
```

## 工作流

```
- [ ] Step 1: 控件区域检测（非整页）
- [ ] Step 2: 逐控件取色与 token 归纳
- [ ] Step 3: 控件识别与补全
- [ ] Step 4: 生成 Demo HTML
- [ ] Step 5: 浏览器截图
- [ ] Step 6: 子 Agent 走查（仅 1 次）
- [ ] Step 7: 修复严重与中等问题
- [ ] Step 8: 交付用户
```

**修复完成前不得告知用户任务结束。**

### Step 1: 控件区域检测

1. 读图，判断输入类型（控件展示板 / App 截图 / 拍屏 / 无 UI）。规则见 [references/input-detection.md](references/input-detection.md)。
2. **划定控件区域**：枚举图中每个可独立识别的 UI 控件（按钮、输入框、卡片、列表行、Tab、Chip 等），记录类别与大致位置。
3. **排除非控件区域**：页面背景、留白、状态栏、装饰插画、icon 图形——不纳入分析。
4. 推断平台与设计语境（iOS / Android），画布尺寸仅作参考，**不作为页面复刻目标**。
5. 将检测结果写入 `analysis.md` 的「控件区域清单」。

### Step 2: 逐控件取色与 token 归纳

**禁止从页面背景或大面积留白采样。**

1. 对每个控件区域单独取色：填充色、文字色、边框色、阴影色。
2. 从各控件测量：圆角、padding、高度、字号、字重。
3. 将多个控件的共性归纳为 semantic token（主色、文字层级、圆角刻度等）。
4. 写入 `tokens.json`（见 [references/token-schema.md](references/token-schema.md)），生成 `tokens.css`。

### Step 3: 控件识别与补全

**Phase A — 逐控件提取（优先）**：对照 Step 1 区域清单，为每个截图控件记录 CSS 属性，标注 `source: screenshot`。

**Phase B — 库补全（必须）**：对照 [references/component-checklist.md](references/component-checklist.md) 补全缺失类别，从已有控件样式推断，标注 `source: inferred`。

Icon Button / Avatar / 带 icon 的 ListItem → 只提取容器样式，icon 区用灰色占位块。

### Step 4: Demo HTML

基于 [templates/style-guide.html](templates/style-guide.html) 与 [templates/components.html](templates/components.html)。**Demo 以控件陈列方式展示**，不复刻参考图的页面排版。样式走 `tokens.css` 变量，禁止硬编码 hex。

### Step 5: 浏览器截图

打开 `style-guide.html` 与 `components.html`，验证渲染正常，保存截图到 `screenshots/`。

### Step 6: 子 Agent 走查（仅 1 次）

启动只读子 Agent（见 [references/ui-review.md](references/ui-review.md)），输出 `ui-review-report.md`。

子 Agent 返回三级问题：
- **严重（blocking）**：截图控件明显不对，必须修复
- **中等（important）**：截图控件有可见偏差，必须修复
- **可接受（acceptable）**：推断项或近似，仅记录

**不启动第 2 轮走查。**

### Step 7: 修复严重与中等问题

1. 读取 `ui-review-report.md`
2. **必须修复**全部 blocking 项
3. **必须修复**全部 important 项
4. `acceptable` 项记入 `analysis.md`，无需改代码
5. 更新 `tokens.css`、`components.html`、`style-guide.html`、`components-list.md`
6. 修复后重新浏览器截图，更新 `ui-review-report.md` 的「修复记录」

仍有未修复的 blocking/important 时，**继续修复，不得交付**。

### Step 8: 交付用户

**全部 blocking + important 修复完成后**，才可回复用户。

交付回复含：路径、核心配色摘要、控件数量、修复了几项严重/中等、剩余可接受差异。

## 约定

- 字体：系统栈近似，商业字体不擅自下载
- CSS 类名：`.ds-button--primary`、`.ds-input` 等；颜色间距走 `var(--token)`
- 精确取色：`python scripts/sample_colors.py --image ... --points "x,y"`（采样点必须在控件像素内）

## 参考

- [references/input-detection.md](references/input-detection.md)
- [references/token-schema.md](references/token-schema.md)
- [references/component-checklist.md](references/component-checklist.md)
- [references/ui-review.md](references/ui-review.md)
- [templates/](templates/)
