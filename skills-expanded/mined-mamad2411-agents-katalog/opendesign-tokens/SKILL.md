---
name: opendesign-tokens
description: OpenDesign 设计 Token 指南。当需要使用 @opensig/opendesign-token 包中的 CSS 变量时使用此 skill。包含六套主题（openEuler/Ascend/Kunpeng/Mindspore/openGauss/openUBMC）的完整 token 体系，支持颜色、间距、圆角、字体、阴影、响应式排版、栅格系统等所有设计令牌。使用场景：(1) 查找颜色值对应的语义 token，(2) 获取间距/圆角/字体的 token 名称，(3) 了解六套主题的差异，(4) 代码中使用 CSS 变量替代硬编码值，(5) 使用响应式 token 实现多断点适配
---

# OpenDesign 设计 Token 指南

`@opensig/opendesign-token` 是 OpenDesign 组件库的设计令牌包，所有 token 使用 `--o-` 前缀。

组件库有六套独立主题（openEuler / Ascend / Kunpeng / Mindspore / openGauss / openUBMC），**每个社区项目在初始化时选定一套，不在六套主题之间运行时切换**。选定主题后，只需在浅色/深色模式之间切换。

---

## 各社区主题的使用方式

### openEuler 主题（`e`）

```typescript
// main.ts 引入（必须在组件样式之前）
import '@opensig/opendesign-token/themes/e.token.css'
```

运行时切换 light/dark（设置在 `<html>` 或 `<body>` 上）：
```javascript
document.documentElement.setAttribute('data-o-theme', 'e.light') // 浅色
document.documentElement.setAttribute('data-o-theme', 'e.dark')  // 深色
```

品牌色：**Klein Blue（品牌蓝）**，控件悬浮时使用品牌色浅色调。

---

### Ascend 主题（`a`）

```typescript
// main.ts 引入
import '@opensig/opendesign-token/themes/a.token.css'
```

运行时切换 light/dark：
```javascript
document.documentElement.setAttribute('data-o-theme', 'a.light') // 浅色
document.documentElement.setAttribute('data-o-theme', 'a.dark')  // 深色
```

品牌色：**Ascend 品牌色**，控件悬浮时使用中性灰调。

---

### Kunpeng 主题（`k`）

```typescript
// main.ts 引入
import '@opensig/opendesign-token/themes/k.token.css'
```

运行时切换 light/dark：
```javascript
document.documentElement.setAttribute('data-o-theme', 'k.light') // 浅色
document.documentElement.setAttribute('data-o-theme', 'k.dark')  // 深色
```

品牌色：**Kunpeng 品牌色**，控件悬浮时使用中性灰调。

---

### Mindspore 主题（`m`）

```typescript
// main.ts 引入
import '@opensig/opendesign-token/themes/m.token.css'
```

运行时切换 light/dark：
```javascript
document.documentElement.setAttribute('data-o-theme', 'm.light') // 浅色
document.documentElement.setAttribute('data-o-theme', 'm.dark')  // 深色
```

品牌色：**Vivid Blue（鲜蓝）**，控件悬浮时使用品牌蓝浅色调。

---

### openGauss 主题（`g`）

```typescript
// main.ts 引入
import '@opensig/opendesign-token/themes/g.token.css'
```

运行时切换 light/dark：
```javascript
document.documentElement.setAttribute('data-o-theme', 'g.light') // 浅色
document.documentElement.setAttribute('data-o-theme', 'g.dark')  // 深色
```

品牌色：**Purple（紫色）**，控件悬浮时使用品牌紫浅色调。

---

### openUBMC 主题（`u`）

```typescript
// main.ts 引入
import '@opensig/opendesign-token/themes/u.token.css'
```

运行时切换 light/dark：
```javascript
document.documentElement.setAttribute('data-o-theme', 'u.light') // 浅色
document.documentElement.setAttribute('data-o-theme', 'u.dark')  // 深色
```

品牌色：**Azure Blue（天蓝）**，控件悬浮时使用品牌蓝浅色调。

---

## Token 体系架构

六套主题的 **token 名称完全相同**，只有颜色值（品牌色、圆角等）不同。

```
基础 Token（调色板）        →  语义 Token（颜色意义）         →  组件级 Token
--o-kleinblue-6            →  --o-color-primary1             →  --btn-color
--o-green-6                →  --o-color-success1             →  --input-border-color
--o-mixedgray-*            →  --o-color-info1                →  ...
```

**使用原则：**
- **推荐使用语义 token**（`--o-color-*`、`--o-gap-*` 等），它们会随 light/dark 自动适配
- **不要直接使用调色板 token**（`--o-kleinblue-*`、`--o-green-*` 等），这些是内部实现

---

## Pixso MCP 设计稿 → Token 映射指南

> 通过 Pixso MCP 读取设计稿节点属性时，用本节将 Pixso 的视觉值映射到对应 CSS Token，替换硬编码值。

### 匹配流程

```
Pixso 节点属性值（颜色 / 字号 / 间距 / 圆角 / 阴影 / 宽度）
  ↓
① 识别属性类型 → 查「属性类型速查表」定位到对应章节
  ↓
② 判断使用响应式 token（--o-r-*）还是静态 token（--o-*）
  ↓
③ 颜色类：确认是通用功能色（直接反查）还是主题特有色（查 reference）
  ↓
④ 输出 CSS 变量：var(--o-xxx)
```

### 属性类型速查

| Pixso 属性 | 判断规则 | 推荐 Token | 查阅章节 |
|-----------|---------|-----------|---------|
| Fill color（填充色）| 背景色、卡片/区块填充 | `--o-color-fill*` | 第 1 节 |
| Fill color（填充色）| 功能色（绿/橙/红/品牌色） | `--o-color-success/warning/danger/primary*` | 第 1 节 |
| Fill color（填充色）| 品牌主色、Primary — **主题特有** | 查对应主题 reference | 主题 reference |
| Stroke / Border color | 控件边框 | `--o-color-control*` | 第 1 节 |
| Text color（文字色）| 主次辅助文字（透明度写法） | `--o-color-info1` ~ `info4` | 第 1 节 |
| Font size（字号）| 页面标题、正文、提示文字 | **`--o-r-font_size-*`（优先）** | 第 2 节 |
| Font size（字号）| 组件内部固定字号 | `--o-font_size-*` | 第 6 节 |
| Line height（行高）| 页面级文字 | **`--o-r-line_height-*`（优先）** | 第 2 节 |
| Padding / Gap（间距）| 页面区块、模块间距 | **`--o-r-gap-*`（优先）** | 第 2 节 |
| Padding / Gap（间距）| 组件内部固定间距 | `--o-gap-*` | 第 4 节 |
| Frame width（列宽）| 多栏布局、侧边栏 + 主内容 | `--o-r-grid-N`（查第 3 节像素对照表确定 N） | 第 3 节 |
| Auto-layout gap | 模块水平间距（栅格水槽） | `--o-r-grid-column-gutter` | 第 3 节 |
| Corner radius（圆角）| 卡片、容器圆角 | `--o-radius-*` | 第 5 节 |
| Corner radius（圆角）| 按钮、输入框等控件圆角 | `--o-radius_control-*` | 第 5 节 |
| Drop shadow（阴影）| 卡片、弹窗 | `--o-shadow-*` | 第 7 节 |
| Opacity 降低（约 0.4）| 禁用状态 | 组件 `disabled` prop，非 token | — |

### 颜色识别优先级

```
Pixso 颜色值
  ↓
1. 是否为功能色（绿/橙/红）或文字透明度色（rgba 黑/白）？
   → 直接用文末「通用色值反查表」
  ↓ 否
2. 是否为品牌主色 / Primary / Fill / 圆角？
   → 主题特有，查对应主题 reference 末尾「反查速查表」
  ↓
3. 替换为 var(--o-xxx)
```

### 画板尺寸 → 断点对照

响应式 token 的实际值取决于画板所在断点，读取 Pixso 画板宽度时按此对应：

| Pixso 画板宽度 | 对应断点 | 响应式 token 实际值参考列 |
|--------------|---------|----------------------|
| ≤840px | Phone | 第 2 节表格 Phone 列 |
| 841–1200px | Pad | 第 2 节表格 Pad 列 |
| 1201–1680px | Laptop | 第 2 节表格 Laptop 列 |
| >1680px | Desktop | 第 2 节表格 Desktop 列（= 静态 token 值） |

> 从 Pixso 读到字号 `22px` 且画板宽度为 1440px（Laptop 断点）→ 查第 2 节 Laptop 列 → 对应 `--o-r-font_size-h3`（Laptop: 18px）或 `--o-r-font_size-display3`（Laptop: 32px）中选最接近的。

---

## 1. 语义颜色 Token（推荐使用）

### 主色系（Primary）

| Token | 用途 | light 示例值 | dark 示例值 |
|-------|------|-------------|------------|
| `--o-color-primary1` | 常规主色 | `rgb(0, 47, 167)` | `rgb(72, 116, 220)` |
| `--o-color-primary2` | 悬浮主色 | `rgb(81, 119, 202)` | `rgb(40, 68, 149)` |
| `--o-color-primary3` | 激活主色 | `rgb(0, 39, 147)` | `rgb(0, 39, 147)` |
| `--o-color-primary4` | 禁用主色 | `rgb(132, 161, 220)` | `rgb(27, 48, 113)` |
| `--o-color-primary1-light` | 主色浅色（背景） | `rgb(190, 206, 237)` | — |
| `--o-color-primary2-light` | 主色浅色（悬浮背景） | `rgb(132, 161, 220)` | — |
| `--o-color-primary3-light` | 主色浅色（激活背景） | `rgb(81, 119, 202)` | — |
| `--o-color-primary4-light` | 主色浅色（禁用背景） | `rgb(227, 234, 246)` | — |

> 注：以上颜色值为 openEuler 主题的 light 模式示例，其他主题的品牌色会有所不同。

### 成功色（Success）

| Token | 用途 |
|-------|------|
| `--o-color-success1` | 常规成功色（`rgb(11, 177, 81)` light） |
| `--o-color-success2` | 悬浮成功色 |
| `--o-color-success3` | 激活成功色 |
| `--o-color-success4` | 禁用成功色 |
| `--o-color-success1-light` | 成功色浅色（背景） |
| `--o-color-success2-light` | 成功色悬浮浅色 |
| `--o-color-success3-light` | 成功色激活浅色 |
| `--o-color-success4-light` | 成功色禁用浅色 |

### 告警色（Warning）

| Token | 用途 |
|-------|------|
| `--o-color-warning1` | 常规告警色（`rgb(250, 115, 5)` light） |
| `--o-color-warning2` | 悬浮告警色 |
| `--o-color-warning3` | 激活告警色 |
| `--o-color-warning4` | 禁用告警色 |
| `--o-color-warning1-light` | 告警色浅色（背景） |
| `--o-color-warning2-light` ~ `--o-color-warning4-light` | 其他状态浅色 |

### 危险色（Danger）

| Token | 用途 |
|-------|------|
| `--o-color-danger1` | 常规危险色（`rgb(230, 0, 18)` light） |
| `--o-color-danger2` | 悬浮危险色 |
| `--o-color-danger3` | 激活危险色 |
| `--o-color-danger4` | 禁用危险色 |
| `--o-color-danger1-light` | 危险色浅色（背景） |
| `--o-color-danger2-light` ~ `--o-color-danger4-light` | 其他状态浅色 |

### 信息色 / 文字颜色（Info）

| Token | 用途 | 说明 |
|-------|------|------|
| `--o-color-info1` | 一级文字 | 标题、强调文本（不透明） |
| `--o-color-info2` | 二级文字 | 正文（80% 不透明度） |
| `--o-color-info3` | 三级文字 | 辅助信息（60% 不透明度） |
| `--o-color-info4` | 四级文字 | 禁用/占位文本（40% 不透明度） |
| `--o-color-info1-inverse` | 反色一级文字 | 深色背景上的白色文字 |
| `--o-color-info2-inverse` | 反色二级文字 | 深色背景上的次要白色文字 |
| `--o-color-info3-inverse` | 反色三级文字 | — |
| `--o-color-info4-inverse` | 反色四级文字 | — |

### 填充色 / 背景色（Fill）

| Token | 用途 | 说明 |
|-------|------|------|
| `--o-color-fill1` | 一级填充 | 页面背景 |
| `--o-color-fill2` | 二级填充 | 区块/卡片背景（**最常用**） |
| `--o-color-fill3` | 三级填充 | 嵌套卡片背景 |

**背景色选择规则：**
```css
/* 页面背景 */
background-color: var(--o-color-fill1);

/* 卡片/区块背景（最常用） */
background-color: var(--o-color-fill2);

/* 嵌套卡片背景 */
background-color: var(--o-color-fill3);

/* 纯白色（极少使用，特殊场景） */
background-color: var(--o-color-white);
```

> ⚠️ **不存在的 token 命名——严禁使用**：
>
> | 错误写法 | 正确替换 | 说明 |
> |---------|---------|------|
> | `var(--o-color-bg1)` | `var(--o-color-fill2)` | **bg1 不存在**，在 token CSS 中无定义，解析为 transparent |
> | `var(--o-color-bg2)` | `var(--o-color-fill2)` | **bg2 不存在**，同上 |
> | `var(--o-color-bg3)` | `var(--o-color-fill3)` | **bg3 不存在**，同上 |
>
> `bg*` 命名是其他设计系统（Bootstrap、Element Plus 等）的惯例，opendesign **不��用此命名**。背景色统一用 `fill*`。

### 控件色（Control）

| Token | 用途 |
|-------|------|
| `--o-color-control1` | 常规边框色（25% 透明度） |
| `--o-color-control2` | 悬浮边框色（60% 透明度） |
| `--o-color-control3` | 激活边框色（80% 透明度） |
| `--o-color-control4` | 禁用边框色（10% 透明度） |
| `--o-color-control1-light` | 常规控件背景 |
| `--o-color-control2-light` | 悬浮控件背景 |
| `--o-color-control3-light` | 激活控件背景 |
| `--o-color-control4-light` | 禁用控件背景 |
| `--o-color-control-light` | 很浅控件色（常用于表格背景） |

### 链接色（Link）

| Token | 用途 |
|-------|------|
| `--o-color-link1` | 常规链接色 |
| `--o-color-link2` | 悬浮链接色 |
| `--o-color-link3` | 激活链接色 |
| `--o-color-link4` | 禁用链接色 |

### 遮罩色（Mask）

| Token | 用途 |
|-------|------|
| `--o-color-mask1` | 全局遮罩（40% 透明） |
| `--o-color-mask2` | 局部遮罩（20% 透明） |

### 基础色（Base）

| Token | 用途 |
|-------|------|
| `--o-color-white` | 纯白色 `rgb(255, 255, 255)`（极少直接使用） |
| `--o-color-black` | 纯黑色 `rgb(0, 0, 0)`（极少直接使用） |

---

## 2. 响应式 Token（Responsive）— 页面级首选

> **优先使用响应式 Token**。对于字号、行高、间距，响应式变量（`--o-r-*`）会根据视口自动缩放，是纠正硬编码值的首选。静态 Token（`--o-font_size-*`、`--o-gap-*`）仅在需要固定不变的场景下使用。

响应式变量前缀为 `--o-r-`，引入主题 CSS 后自动生效，无需额外导入。共 4 个断点：

| 断点 | 视口范围 | 典型设备 |
|------|---------|---------|
| Phone | ≤840px | 手机、平板竖屏 |
| Pad | 841–1200px | 平板横屏 |
| Laptop | 1201–1680px | 笔记本 |
| Desktop | >1680px | 桌面大屏 |

### 响应式字号 + 行高

| 语义 | Token 名称 | Phone | Pad | Laptop | Desktop |
|------|-----------|-------|-----|--------|---------|
| 一级数据展示 | `--o-r-font_size-display1` / `line_height` | 22/30 | 40/56 | 48/64 | 56/80 |
| 二级数据展示 | `--o-r-font_size-display2` / `line_height` | 20/28 | 32/44 | 40/56 | 48/64 |
| 三级数据展示 | `--o-r-font_size-display3` / `line_height` | 18/26 | 24/32 | 32/44 | 40/56 |
| 一级标题 | `--o-r-font_size-h1` / `line_height` | 18/26 | 20/28 | 20/28 | 32/44 |
| 二级标题 | `--o-r-font_size-h2` / `line_height` | 16/24 | 18/26 | 20/28 | 24/32 |
| 三级标题 | `--o-r-font_size-h3` / `line_height` | 16/24 | 16/24 | 18/26 | 22/30 |
| 四级标题 | `--o-r-font_size-h4` / `line_height` | 16/24 | 16/24 | 18/26 | 20/28 |
| 大号正文 | `--o-r-font_size-text2` / `line_height` | 14/22 | 14/22 | 16/24 | 18/26 |
| 常规正文 | `--o-r-font_size-text1` / `line_height` | 14/22 | 14/22 | 14/22 | 16/24 |
| 提示文本1 | `--o-r-font_size-tip1` / `line_height` | 12/18 | 12/18 | 14/22 | 14/22 |
| 提示文本2 | `--o-r-font_size-tip2` / `line_height` | 10/16 | 12/18 | 12/18 | 12/18 |

> 单位均为 px。Token 名称中 `font_size` 和 `line_height` 共享后缀（如 `--o-r-font_size-h1` 配 `--o-r-line_height-h1`）。

### 响应式间距

| Token 名称 | Phone | Pad | Laptop | Desktop |
|-----------|-------|-----|--------|---------|
| `--o-r-gap-10` | 32px | 40px | 56px | 72px |
| `--o-r-gap-9` | 24px | 32px | 48px | 64px |
| `--o-r-gap-8` | 16px | 24px | 40px | 48px |
| `--o-r-gap-7` | 12px | 16px | 24px | 40px |
| `--o-r-gap-6` | 12px | 16px | 24px | 32px |
| `--o-r-gap-5` | 12px | 12px | 16px | 24px |
| `--o-r-gap-4` | 8px | 8px | 12px | 16px |
| `--o-r-gap-3` | 8px | 8px | 8px | 12px |
| `--o-r-gap-2` | 8px | 8px | 8px | 8px |
| `--o-r-gap-1` | 4px | 4px | 4px | 4px |

> **对照关系**：`--o-r-gap-N` 的 Desktop 值 = `--o-gap-N` 的静态值。响应式变量在小屏上自动压缩间距。

### 响应式 vs 静态 Token 选择

| 场景 | 推荐 | 原因 |
|------|------|------|
| 页面标题、正文、区块间距 | `--o-r-*`（响应式） | 随视口自动适配，无需写 media query |
| 组件内部固定尺寸（如图标旁 4px 间距） | `--o-gap-*`（静态） | 尺寸不应随视口变化 |
| 设计稿硬编码的字号/间距纠正 | `--o-r-*`（响应式） | **首选**，确保多端一致 |

---

## 3. 栅格系统 Token（Grid）— 页面级模块布局

> **栅格系统用于页面级布局**，是控制页面各模块在水平方向（X 轴）上宽度与间距的核心配置形式。多栏布局、侧边栏 + 主内容区、模块间的水平分割均应优先使用栅格变量，而非手动写死宽度或 padding。

24 列响应式栅格，共 6 个断点。引入主题 CSS 后自动生效。

| 断点 | 视口范围 | 列数 | 留白(单侧) | 水槽 |
|------|---------|------|-----------|------|
| 超大屏 | >1920px | 24 | 64px | 32px |
| 桌面 | 1441–1920px | 24 | 64px | 32px |
| 小桌面 | 1201–1440px | 24 | 40px | 24px |
| 平板横屏 | 841–1200px | 12 | 32px | 16px |
| 平板竖屏 | 601–840px | 8 | 32px | 16px |
| 手机 | ≤600px | 4 | 24px | 12px |

**关键变量**：`--o-r-grid-1` ~ `--o-r-grid-24`（N 列宽度），`--o-r-grid-column-gutter`（水槽宽度）。

**栅格容器**：直接使用 `.o-r-grid-container` 类即可（`display:flex; max-width:1920px; margin:0 auto; padding:var(--o-r-grid-padding)`）。

```css
.sidebar { width: var(--o-r-grid-6); margin-right: var(--o-r-grid-column-gutter); }
.content { width: var(--o-r-grid-18); }
```

### Pixso 画板 → grid-N 像素对照表

> 从 Pixso 读到 frame 宽度后，在对应画板宽度的行中找最接近的值，即可确定应使用 `--o-r-grid-N`。

**列宽公式**：`col = (画板宽 - 2×留白 - (最大列数-1)×水槽) / 最大列数`
**grid-N 宽度**：`grid-N = N × col + (N-1) × 水槽`

| 画板宽度 | 断点 | col | 水槽 | grid-4 | grid-6 | grid-8 | grid-12 | grid-16 | grid-18 |
|---------|------|-----|------|--------|--------|--------|---------|---------|---------|
| 1920px | 超大屏 | 44px | 32px | 272px | 424px | 576px | 880px | 1184px | 1336px |
| 1680px | 桌面 | 34px | 32px | 232px | 364px | 496px | 760px | 1024px | 1156px |
| 1440px | 小桌面 | ~33.7px | 24px | ~207px | ~322px | ~437px | ~668px | ~899px | ~1014px |
| 1200px | 平板横屏 | 80px | 16px | 368px | 560px | 752px | 1136px | *(超出12列)* | *(超出12列)* |
| 840px | 平板竖屏 | 83px | 16px | 380px | 578px | 776px | *(超出8列)* | — | — |
| 375px | 手机 | ~72.75px | 12px | 327px | *(超出4列)* | — | — | — | — |

> **说明**：平板横屏最多 12 列，超出部分等于全宽（grid-12 值）；平板竖屏最多 8 列；手机最多 4 列。

### 水槽分隔原则（核心规则）

X 轴方向上相邻的大块元素（Card、楼层区块、内容模块等）之间的间距**固定为 1 个水槽**（`--o-r-grid-column-gutter`），不使用 gap token。

**列数分配约束**：N 个并排块的列数之和 = 当前断点的总列数。

```
grid-N₁ + gutter + grid-N₂ + gutter + ... + grid-Nₙ = 内容区全宽
即：N₁ + N₂ + ... + Nₙ = 总列数（24 / 12 / 8 / 4，取决于断点）
```

**等宽 N 块**：每块列数 = 总列数 ÷ N

| 并排块数 | 超大屏/桌面/小桌面（24列） | 平板横屏（12列） | 平板竖屏（8列） | 手机（4列） |
|---------|--------------------------|----------------|----------------|-----------|
| 2 块等宽 | grid-12 + grid-12 | grid-6 + grid-6 | grid-4 + grid-4 | grid-2 + grid-2 |
| 3 块等宽 | grid-8 × 3 | grid-4 × 3 | — (不整除) | — |
| 4 块等宽 | grid-6 × 4 | grid-3 × 4 | grid-2 × 4 | — |
| 6 块等宽 | grid-4 × 6 | grid-2 × 6 | — | — |

**不等宽（按比例分配）**：各块列数 = round(比例权重 × 总列数)，确保总和 = 总列数。

| 比例 | 24列断点 | 12列断点 | 典型场景 |
|------|---------|---------|---------|
| 1 : 1 : 2 | 6 + 6 + 12 | 3 + 3 + 6 | 两窄一宽 |
| 1 : 2 : 1 | 6 + 12 + 6 | 3 + 6 + 3 | 中间主推 |
| 1 : 3 : 1 | 5 + 14 + 5 | 2 + 8 + 2 | 突出中间 |
| 2 : 3 | 10 + 14 | 5 + 7 | 偏宽主内容 |

> **取整原则**：比例分配出现小数时，最后一块用剩余列数补齐，保证总和严格等于断点总列数。

**验证示例（1920px，24列，col=44px，gutter=32px）**：
- 3×grid-8：576 + 32 + 576 + 32 + 576 = **1792px** = 内容区宽 ✓
- grid-6 + grid-12 + grid-6：424 + 32 + 880 + 32 + 424 = **1792px** ✓

### 常见多栏布局速查

| 布局比例 | 列数分配 | 左栏 token | 右栏 token | 典型场景 |
|---------|---------|-----------|-----------|---------|
| 1 : 3 | 6 + 18 | `--o-r-grid-6` | `--o-r-grid-18` | 窄侧边导航 + 主内容 |
| 1 : 2 | 8 + 16 | `--o-r-grid-8` | `--o-r-grid-16` | 标准侧边栏 + 主内容 |
| 1 : 1 | 12 + 12 | `--o-r-grid-12` | `--o-r-grid-12` | 两栏等宽 |
| 1 : 5 | 4 + 20 | `--o-r-grid-4` | `--o-r-grid-20` | 超窄图标导航 + 宽内容 |
| 2 : 1 | 16 + 8 | `--o-r-grid-16` | `--o-r-grid-8` | 主内容 + 辅助信息栏 |

> **水槽处理**：两栏之间只需设一侧的 `margin: var(--o-r-grid-column-gutter)`，不要两侧都加（否则水槽加倍）。

### 从 Pixso frame 宽度判断 grid-N 的步骤

```
① 读取 Pixso 画板宽度 → 确定断点行
② 读取 frame.width
③ 在对照表中找最接近的列值 → 得到 N
   （误差在 ±5px 以内可认为是同一列，因设计工具精度或子像素造成）
④ 若 frame 占满内容区（全宽减两侧留白）→ 使用 .o-r-grid-container 包裹即可，无需 grid-N
⑤ 代入：width: var(--o-r-grid-N)
```

**示例**：Pixso 画板 1440px，frame 宽度 322px → 查表 "1440px 行，grid-6 ≈ 322px" → 使用 `width: var(--o-r-grid-6)`。

### 表单组件栅格规则

> OForm 及输入类组件（OInput、OSelect、OTextarea 等）在多列表单布局中，每个表单项的宽度应对齐到栅格列，行间距遵循设计规范值。

**多列表单：每行项数与列宽分配**

| 断点 | 总列数 | 每行项数 | 每项宽度 Token | 标签位置 |
|------|-------|---------|-------------|---------|
| Desktop >1680px | 24 | **4** 项/行 | `--o-r-grid-6` | 左置水平 |
| Laptop 1201–1680px | 24 | **4** 项/行 | `--o-r-grid-6` | 左置水平 |
| Pad 841–1200px | 12 | **3** 项/行 | `--o-r-grid-4` | 左置水平 |
| Phone ≤840px | 4 | **1** 项/行 | 全宽 | 上置堆叠 |

> **验证**（桌面端，4 项×grid-6）：4×grid-6 + 3×gutter = 4×424 + 3×32 = 1696 + 96 = **1792px** = 24列内容区 ✓
> **验证**（平板横屏，3 项×grid-4）：3×grid-4 + 2×gutter = 3×368 + 2×16 = 1104 + 32 = **1136px** = 12列内容区（1200px画板）✓

**行间距（form item 垂直方向）**

| 断点 | 每行 form item 间距 |
|------|-------------------|
| >840px（水平标签） | `32px` |
| ≤840px（堆叠标签） | `12px` |

**标签宽度与内部间距**

| 区域 | >840px（PC 水平模式） | ≤840px（手机堆叠模式） |
|------|---------------------|----------------------|
| 标签区域宽度 | 固定 **96px** | 全宽（100%） |
| 标签到输入框间距 | `4px`（标签文字到冒号间距） | `8px`（标签文字到输入框） |
| Hint/帮助文字位置 | 输入框右侧，右侧留 **24px** | 输入框下方，间距 `12px` |

**分组约束**

- 多列表单中，单个表单分组（section）建议包含 **2–7 个表单项**
- 跨全行的宽项（文本域、文件上传等）单独占满一行（width = 容器全宽）
- 并排项的列数之和须等于当前断点总列数（同「水槽分隔原则」）

**示例：桌面端 4 列表单布局（>1200px）**

```css
/* 每个 form item 宽度 = grid-6 */
.form-item {
  width: var(--o-r-grid-6);
}

/* 多列 form 行容器：flex + gutter 间距 */
.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 32px var(--o-r-grid-column-gutter);
  /* ↑ row-gap=32px(PC)，column-gap=水槽 */
}
```

```css
/* 平板横屏（841-1200px）：3 列，每项 grid-4 */
@media (max-width: 1200px) {
  .form-item { width: var(--o-r-grid-4); }
  .form-row  { gap: 12px var(--o-r-grid-column-gutter); }
}

/* 手机（≤840px）：1 列，全宽 */
@media (max-width: 840px) {
  .form-item { width: 100%; }
  .form-row  { gap: 12px 0; }
}
```

---

## 4. 间距 Token（Gap）— 静态值

> **页面级间距推荐使用响应式 token `--o-r-gap-*`**（见第 2 节），以下静态 token 适用于不随视口变化的固定间距场景。

间距 token 适用于 `gap`、`padding`、`margin` 等属性。

| Token | 值 | 用途 |
|-------|----|------|
| `--o-gap-1` | `4px` | 最小间距（紧凑元素内部） |
| `--o-gap-2` | `8px` | 小间距（组件内部元素） |
| `--o-gap-3` | `12px` | 中小间距（相关元素之间） |
| `--o-gap-4` | `16px` | **常规间距（默认，最常用）** |
| `--o-gap-5` | `24px` | 中等间距（区块之间） |
| `--o-gap-6` | `32px` | 大间距（页面级布局） |
| `--o-gap-7` | `40px` | 较大间距 |
| `--o-gap-8` | `48px` | 很大间距 |
| `--o-gap-9` | `64px` | 超大间距 |
| `--o-gap-10` | `72px` | 最大间距 |

---

## 5. 圆角 Token（Radius）

> **⚠️ 圆角值因主题而异**：以下 `值` 列是通用参考值，实际值取决于主题。例如 openEuler 主题所有圆角均为 **4px**（接近直角风格），而 Mindspore 主题则更圆润。使用时请查阅对应主题 reference 文件中的圆角表格。
> 也不存在 `--o-r-radius-1` 等带 `r-` 前缀的圆角变量，圆角 token 没有响应式变体。

### 内容圆角（用于卡片、容器等）

| Token | 通用参考值 | 用途 |
|-------|----------|------|
| `--o-radius-xs` | `4px` | 超小圆角 |
| `--o-radius-s` | `8px` | 小圆角 |
| `--o-radius-m` | `12px` | 中等圆角 |
| `--o-radius-l` | `16px` | 大圆角 |
| `--o-radius-xl` | `24px` | 超大圆角（一般用于卡片） |

### 控件圆角（用于按钮、输入框等组件）

| Token | 通用参考值 | 用途 |
|-------|----------|------|
| `--o-radius_control-xs` | `4px` | 超小控件圆角 |
| `--o-radius_control-s` | `8px` | 小控件圆角 |
| `--o-radius_control-m` | `12px` | 中等控件圆角 |
| `--o-radius_control-l` | `16px` | 大控件圆角 |

---

## 6. 字体 Token（Font）— 静态值

> **页面级文字推荐使用响应式 token `--o-r-font_size-*` / `--o-r-line_height-*`**（见第 2 节），以下静态 token 适用于不随视口变化的固定字号场景。

### 字体大小（Font Size）

| Token | 值 | 用途 |
|-------|----|------|
| `--o-font_size-display1` | `56px` | 一级数据展示 |
| `--o-font_size-display2` | `48px` | 二级数据展示 |
| `--o-font_size-display3` | `40px` | 三级数据展示 |
| `--o-font_size-h1` | `32px` | 一级标题 |
| `--o-font_size-h2` | `24px` | 二级标题 |
| `--o-font_size-h3` | `22px` | 三级标题 |
| `--o-font_size-h4` | `20px` | 四级标题 |
| `--o-font_size-text2` | `18px` | 大号正文 |
| `--o-font_size-text1` | `16px` | **常规正文（最常用）** |
| `--o-font_size-tip1` | `14px` | 提示文本（小字） |
| `--o-font_size-tip2` | `12px` | 辅助提示文本（最小） |

### 行高（Line Height）

| Token | 值 | 配套字号 |
|-------|----|---------|
| `--o-line_height-display1` | `80px` | display1 |
| `--o-line_height-display2` | `64px` | display2 |
| `--o-line_height-display3` | `56px` | display3 |
| `--o-line_height-h1` | `44px` | h1 |
| `--o-line_height-h2` | `32px` | h2 |
| `--o-line_height-h3` | `30px` | h3 |
| `--o-line_height-h4` | `28px` | h4 |
| `--o-line_height-text2` | `26px` | text2 |
| `--o-line_height-text1` | `24px` | text1 |
| `--o-line_height-tip1` | `22px` | tip1 |
| `--o-line_height-tip2` | `18px` | tip2 |

**字体和行高应配套使用：**
```css
/* 响应式（推荐，自动适配多端） */
.title {
  font-size: var(--o-r-font_size-h3);
  line-height: var(--o-r-line_height-h3);
}

/* 静态（仅在需要固定值时使用） */
.fixed-label {
  font-size: var(--o-font_size-tip1);
  line-height: var(--o-line_height-tip1);
}
```

---

## 7. 阴影 Token（Shadow）

| Token | 值 | 用途 |
|-------|----|------|
| `--o-shadow-1` | `0 3px 8px rgba(..., 0.08)` | 卡片、小弹窗、楼层阴影 |
| `--o-shadow-2` | `0 2px 24px rgba(..., 0.15)` | 卡片悬浮阴影 |
| `--o-shadow-3` | `0 8px 40px rgba(..., 0.1)` | 大弹窗、抽屉阴影 |

---

## 8. 动画 Token（Animation）

### 持续时间（Duration）

| Token | 值 | 用途 |
|-------|----|------|
| `--o-duration-s` | `200ms` | 退出屏幕的动画 |
| `--o-duration-m1` | `250ms` | standard-in 曲线进入动画 |
| `--o-duration-m2` | `300ms` | standard 曲线开始/结束动画 |
| `--o-duration-m3` | `400ms` | emphasized-in 曲线进入动画 |
| `--o-duration-l` | `500ms` | emphasized 曲线开始/结束动画 |
| `--o-duration-xl` | `1000ms` | 轮播切换动画 |

### 缓动曲线（Easing）

| Token | 值 | 用途 |
|-------|----|------|
| `--o-easing-linear` | `cubic-bezier(0, 0, 1, 1)` | 线性 |
| `--o-easing-standard` | `cubic-bezier(0.2, 0, 0, 1)` | 标准（组件动画，**推荐**） |
| `--o-easing-standard-in` | `cubic-bezier(0, 0, 0, 1)` | 标准进入 |
| `--o-easing-standard-out` | `cubic-bezier(0.3, 0, 1, 1)` | 标准退出 |
| `--o-easing-emphasized` | `cubic-bezier(0.2, 0, 0, 1)` | 强调（大卡片/场景切换） |
| `--o-easing-emphasized-in` | `cubic-bezier(0.3, 0, 0.8, 0.15)` | 强调进入 |
| `--o-easing-emphasized-out` | `cubic-bezier(0.05, 0.7, 0.1, 1)` | 强调退出 |

```css
/* 推荐的动画写法 */
transition: all var(--o-duration-m1) var(--o-easing-standard);
```

---

## 9. 组件尺寸 Token（Control Size）

| Token | 值 | 用途 |
|-------|----|------|
| `--o-control_size-2xs` | `14px` | 超超小控件 |
| `--o-control_size-xs` | `16px` | 超小控件 |
| `--o-control_size-s` | `24px` | 小控件 |
| `--o-control_size-m` | `32px` | 中等控件 |
| `--o-control_size-l` | `40px` | 大控件 |
| `--o-control_size-xl` | `48px` | 超大控件 |
| `--o-control_size-2xl` | `56px` | 超超大控件 |

---

## 10. 图标尺寸 Token（Icon Size）

### 独立图标

| Token | 值 |
|-------|----|
| `--o-icon_size-xs` | `16px` |
| `--o-icon_size-s` | `20px` |
| `--o-icon_size-m` | `24px` |
| `--o-icon_size-l` | `32px` |
| `--o-icon_size-xl` | `40px` |
| `--o-icon_size-2xl` | `48px` |
| `--o-icon_size-3xl` | `56px` |
| `--o-icon_size-4xl` | `64px` |

### 控件内图标（组件使用）

| Token | 值 |
|-------|----|
| `--o-icon_size_control-xs` | `16px` |
| `--o-icon_size_control-s` | `20px` |
| `--o-icon_size_control-m` | `24px` |
| `--o-icon_size_control-l` | `32px` |
| `--o-icon_size_control-xl` | `40px` |

---

## 11. 调色板 Token（参考，不推荐直接使用）

调色板 token 是原始颜色值，为语义 token 提供基础，**不应在业务代码中直接使用**。

每个色系均有 10 个色阶（1=最浅，10=最深），light/dark 模式下颜色相反。

| 色系 | Token 前缀 | 主色代表 | 用途 |
|------|-----------|---------|------|
| 品牌蓝 | `--o-kleinblue-*` | `#002FA7` | 主色/链接色 |
| 绿色 | `--o-green-*` | `#0BB151` | 成功色 |
| 橘红色 | `--o-orange-*` | `#FA7305` | 告警色 |
| 红色 | `--o-red-*` | `#E60012` | 危险色 |
| 黄色 | `--o-yellow-*` | `#F0BC06` | 辅助色 |
| 琥珀色 | `--o-amber-*` | `#E78900` | 辅助色 |
| 黄绿色 | `--o-lime-*` | `#A7C900` | 辅助色 |
| 浅绿色 | `--o-light-green-*` | `#70B31B` | 辅助色 |
| 蓝绿色 | `--o-teal-*` | `#00B385` | 辅助色 |
| 青色 | `--o-cyan-*` | `#00A7B3` | 辅助色 |
| 浅蓝色 | `--o-light-blue-*` | `#009CE5` | 辅助色 |
| 蓝色 | `--o-blue-*` | `#1075E8` | 辅助色 |
| 紫罗兰 | `--o-violet-*` | `#5E12CB` | 辅助色 |
| 紫色 | `--o-purple-*` | `#8702B3` | 辅助色 |
| 粉红色 | `--o-pink-*` | `#E00070` | 辅助色 |
| 白色 | `--o-white` | `#FFFFFF` | 基础 |
| 黑色 | `--o-black` | `#000000` | 基础 |

---

## 最佳实践

### OpenDesign 组件样式原则

使用 `@opensig/opendesign` 组件库中的组件时，**组件应作为一个整体使用，不应修改组件内部样式**（除非有明确的特殊需求并经过确认）。组件的视觉表现由 Token 体系统一控制：
- 通过切换主题（`data-o-theme`）改变组件的品牌色和圆角风格
- 通过组件暴露的 props 控制尺寸、颜色变体等
- **不要**通过 CSS 覆盖组件内部的 class 样式（如 `.o-btn__text`）
- **不要**通过 `::v-deep` / `:deep()` 穿透修改组件内部结构

Token 变量主要用于**自定义业务区域**的样式（如页面布局、自定义卡片、业务容器等），而非覆盖组件内部。

### ✅ 推荐做法

> ⚠️ **边框规则**：**只在设计稿 DSL 中有 `strokes` 属性时才加边框，绝对不要默认给卡片/容器加边框。** 设计稿没有描边就不写 `border`。

```css
.card {
  background-color: var(--o-color-fill2);        /* 卡片背景 */
  /* ⚠️ border 只有在 DSL strokes 非空时才加 */
  /* border: 1px solid var(--o-color-control1); */
  border-radius: var(--o-radius-m);              /* 圆角 */
  padding: var(--o-r-gap-4);                     /* 内边距（响应式） */
  box-shadow: var(--o-shadow-1);                 /* 阴影（有 DSL effects 时才加） */
}

.title {
  font-size: var(--o-r-font_size-h3);            /* 响应式字号 */
  line-height: var(--o-r-line_height-h3);        /* 响应式行高 */
  color: var(--o-color-info1);                   /* 标题文字 */
}

.body-text {
  font-size: var(--o-r-font_size-text1);         /* 响应式字号 */
  line-height: var(--o-r-line_height-text1);     /* 响应式行高 */
  color: var(--o-color-info2);                   /* 正文 */
}

.section-gap {
  padding: var(--o-r-gap-6) var(--o-r-gap-4);   /* 响应式间距 */
}

.caption {
  font-size: var(--o-r-font_size-tip1);
  color: var(--o-color-info3);                   /* 辅助信息 */
}

.button:hover {
  transition: all var(--o-duration-m1) var(--o-easing-standard);
  box-shadow: var(--o-shadow-2);
}

.link {
  color: var(--o-color-link1);
}
.link:hover {
  color: var(--o-color-link2);
}
```

### ❌ 不推荐做法

```css
/* 不要使用调色板 token */
.card {
  background-color: rgb(var(--o-white));        /* ❌ 应使用 var(--o-color-fill2) */
  border: 1px solid rgb(var(--o-grey-5));       /* ❌ 应使用 var(--o-color-control1) */
}

/* 不要硬编码字号/间距——应使用响应式 token */
.title {
  font-size: 22px;                              /* ❌ 应使用 var(--o-r-font_size-h3) */
  line-height: 30px;                            /* ❌ 应使用 var(--o-r-line_height-h3) */
}
.card {
  padding: 16px;                                /* ❌ 应使用 var(--o-r-gap-4) */
  border-radius: 12px;                          /* ❌ 应使用 var(--o-radius-m) */
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);  /* ❌ 应使用 var(--o-shadow-1) */
}
.section {
  gap: 32px;                                    /* ❌ 应使用 var(--o-r-gap-6) */
}

/* 不要用静态 token 代替响应式 token（除非确实需要固定值） */
.page-title {
  font-size: var(--o-font_size-h1);             /* ⚠️ 应使用 var(--o-r-font_size-h1)，自动适配多端 */
}
```

---

## 使用场景速查

### 背景色

| 场景 | Token |
|------|-------|
| 页面背景 | `--o-color-fill1` |
| 卡片/区块背景 | `--o-color-fill2`（**最常用**） |
| 嵌套卡片 | `--o-color-fill3` |
| 纯白（特殊） | `--o-color-white` |

### 文字颜色

| 场景 | Token |
|------|-------|
| 标题/强调 | `--o-color-info1` |
| 正文 | `--o-color-info2` |
| 辅助信息 | `--o-color-info3` |
| 禁用/占位 | `--o-color-info4` |
| 深色背景白字 | `--o-color-info1-inverse` |

### 边框颜色

| 场景 | Token |
|------|-------|
| 默认边框 | `--o-color-control1` |
| 悬浮边框 | `--o-color-control2` |
| 激活/聚焦边框 | `--o-color-primary1` 或 `--o-color-control3` |
| 禁用边框 | `--o-color-control4` |

### 间距

> 页面级间距优先使用响应式 token `--o-r-gap-*`，组件内部固定间距可用静态 `--o-gap-*`。

| 场景 | Token（响应式优先） | Desktop 值 |
|------|-------------------|-----------|
| 图标与文字间距 | `--o-r-gap-1` / `--o-gap-1` | 4px |
| 组件内部元素 | `--o-r-gap-2` / `--o-gap-2` | 8px |
| 相关元素间 | `--o-r-gap-3` | 12px |
| 默认内边距 | `--o-r-gap-4` | 16px |
| 区块间距 | `--o-r-gap-5` | 24px |
| 页面布局 | `--o-r-gap-6` | 32px |

### 字号

> 字号和行高优先使用响应式 token `--o-r-font_size-*` / `--o-r-line_height-*`。

| 场景 | Token（响应式优先） | Desktop 值 |
|------|-------------------|-----------|
| 页面大标题 | `--o-r-font_size-h1` + `--o-r-line_height-h1` | 32/44px |
| 区块标题 | `--o-r-font_size-h3` + `--o-r-line_height-h3` | 22/30px |
| 正文 | `--o-r-font_size-text1` + `--o-r-line_height-text1` | 16/24px |
| 辅助/提示 | `--o-r-font_size-tip1` + `--o-r-line_height-tip1` | 14/22px |

---

## 色值反查（设计稿写死色值 → Token）

设计稿中可能存在写死色值（如 `#002FA7`、`rgba(0,0,0,0.25)`）的情况，需要反向匹配为对应 CSS 变量。

### 操作流程

```
1. 确认截取色值时的模式（light / dark）
2. 确认项目使用的主题（e / a / k / m / g / u）
3. 在下方通用表或对应主题 reference 中查找色值
4. 将写死的值替换为 var(--o-xxx)
5. 字号/行高/间距优先替换为响应式 token var(--o-r-xxx)
```

> 注意：同一 token 在 light 和 dark 模式下对应不同色值，确保对应正确的模式。

---

### 通用色值反查（六套主题相同）

以下 token 的色值在六套主题中**完全相同**，可直接反查。

#### 功能色（Light 模式）

| Hex | RGB | Token | 语义 |
|-----|-----|-------|------|
| `#0BB151` | `rgb(11, 177, 81)` | `--o-color-success1` | 成功色 |
| `#54D07F` | `rgb(84, 208, 127)` | `--o-color-success2` | 成功悬浮 |
| `#07984A` | `rgb(7, 152, 72)` | `--o-color-success3` | 成功激活 |
| `#80E09E` | `rgb(128, 224, 158)` | `--o-color-success4` | 成功禁用 |
| `#B1EFC3` | `rgb(177, 239, 195)` | `--o-color-success1-light` | 成功浅色背景 |
| `#FA7305` | `rgb(250, 115, 5)` | `--o-color-warning1` | 告警色 |
| `#FCB05F` | `rgb(252, 176, 95)` | `--o-color-warning2` | 告警悬浮 |
| `#CF5803` | `rgb(207, 88, 3)` | `--o-color-warning3` | 告警激活 |
| `#FDCA8C` | `rgb(253, 202, 140)` | `--o-color-warning4` | 告警禁用 |
| `#FEE2BA` | `rgb(254, 226, 186)` | `--o-color-warning1-light` | 告警浅色背景 |
| `#E60012` | `rgb(230, 0, 18)` | `--o-color-danger1` | 危险色 |
| `#F0575A` | `rgb(240, 87, 90)` | `--o-color-danger2` | 危险悬浮 |
| `#C00016` | `rgb(192, 0, 22)` | `--o-color-danger3` | 危险激活 |
| `#F58886` | `rgb(245, 136, 134)` | `--o-color-danger4` | 危险禁用 |
| `#FAB9B6` | `rgb(250, 185, 182)` | `--o-color-danger1-light` | 危险浅色背景 |

#### 文字色（透明度写法，Light 模式）

| 设计稿常见写法 | Token | 语义 |
|--------------|-------|------|
| `rgba(0,0,0,1)` 或 `#000000` | `--o-color-info1` | 一级文字/标题 |
| `rgba(0,0,0,0.8)` 或 `#000000 80%` | `--o-color-info2` | 二级文字/正文 |
| `rgba(0,0,0,0.6)` 或 `#000000 60%` | `--o-color-info3` | 三级文字/辅助 |
| `rgba(0,0,0,0.4)` 或 `#000000 40%` | `--o-color-info4` | 四级文字/禁用 |
| `rgba(255,255,255,1)` | `--o-color-info1-inverse` | 深色背景白字 |
| `rgba(255,255,255,0.8)` | `--o-color-info2-inverse` | 深色背景次要白字 |

#### 遮罩和边框（Light 模式）

| 设计稿常见写法 | Token | 语义 |
|--------------|-------|------|
| `rgba(0,0,0,0.4)` | `--o-color-mask1` | 全局遮罩 |
| `rgba(255,255,255,0.2)` | `--o-color-mask2` | 局部遮罩 |
| `rgba(0,0,0,0.25)` | `--o-color-control1` | 默认边框 |
| `rgba(0,0,0,0.1)` | `--o-color-control4` | 禁用边框 |

#### 间距（六套主题完全相同）

> 硬编码间距应优先替换为响应式 token `--o-r-gap-*`。

| 硬编码值 | 响应式 Token（推荐） | 静态 Token |
|---------|-------------------|-----------|
| `4px` | `--o-r-gap-1` | `--o-gap-1` |
| `8px` | `--o-r-gap-2` | `--o-gap-2` |
| `12px` | `--o-r-gap-3` | `--o-gap-3` |
| `16px` | `--o-r-gap-4` | `--o-gap-4` |
| `24px` | `--o-r-gap-5` | `--o-gap-5` |
| `32px` | `--o-r-gap-6` | `--o-gap-6` |
| `40px` | `--o-r-gap-7` | `--o-gap-7` |
| `48px` | `--o-r-gap-8` | `--o-gap-8` |
| `64px` | `--o-r-gap-9` | `--o-gap-9` |
| `72px` | `--o-r-gap-10` | `--o-gap-10` |

> 注意：上表硬编码值对应的是 Desktop 断点（>1680px）的响应式值。小屏下响应式 token 会自动缩小。

#### 字号 / 行高（六套主题完全相同）

> 硬编码字号应优先替换为响应式 token `--o-r-font_size-*` + `--o-r-line_height-*`。

| 硬编码 font-size | 响应式 Token（推荐） | 静态 Token |
|-----------------|-------------------|-----------|
| `56px` | `--o-r-font_size-display1` | `--o-font_size-display1` |
| `48px` | `--o-r-font_size-display2` | `--o-font_size-display2` |
| `40px` | `--o-r-font_size-display3` | `--o-font_size-display3` |
| `32px` | `--o-r-font_size-h1` | `--o-font_size-h1` |
| `24px` | `--o-r-font_size-h2` | `--o-font_size-h2` |
| `22px` | `--o-r-font_size-h3` | `--o-font_size-h3` |
| `20px` | `--o-r-font_size-h4` | `--o-font_size-h4` |
| `18px` | `--o-r-font_size-text2` | `--o-font_size-text2` |
| `16px` | `--o-r-font_size-text1` | `--o-font_size-text1` |
| `14px` | `--o-r-font_size-tip1` | `--o-font_size-tip1` |
| `12px` | `--o-r-font_size-tip2` | `--o-font_size-tip2` |

---

### 主题特有色值反查

品牌色、Primary 色、Fill 色、圆角等因主题而异，请查阅对应 reference 文件：

- **openEuler (e)**：[references/tokens-openeuler.md](references/tokens-openeuler.md) → 末尾「反查速查表」
- **Ascend (a)**：[references/tokens-ascend.md](references/tokens-ascend.md) → 末尾「反查速查表」
- **Kunpeng (k)**：[references/tokens-kunpeng.md](references/tokens-kunpeng.md) → 末尾「反查速查表」
- **Mindspore (m)**：[references/tokens-mindspore.md](references/tokens-mindspore.md) → 末尾「反查速查表」
- **openGauss (g)**：[references/tokens-opengauss.md](references/tokens-opengauss.md) → 末尾「反查速查表」
- **openUBMC (u)**：[references/tokens-openubmc.md](references/tokens-openubmc.md) → 末尾「反查速查表」
