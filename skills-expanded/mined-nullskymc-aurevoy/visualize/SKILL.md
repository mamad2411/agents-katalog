---
name: visualize
description: 将结构化数据转成直接渲染在 Aurevoy 对话中的交互式探索器、图表、比较视图或模拟器（present_ui canvas）。用于用户要查看、筛选、比较、钻取数据，或需要可调参数来理解动态关系时；不用于要求改现有应用页面、组件或网站的任务。
user-invocable: true
metadata:
  version: "1.2"
---

# Visualize

使用 `present_ui(kind="canvas")` 将交互式可视化直接放入对话流。Canvas 在 sandbox iframe 中运行，HTML、CSS、JavaScript 与数据均不离开该片段；不要改为 HTML 文件附件，也不要声称它是应用页面。

## 数据与范围

1. 先定位用户给出的 CSV、TSV、JSON、Excel 或工作区数据文件，读取少量样本与字段名，确认单位、时间范围、缺失值和唯一标识。
2. 数据不存在时，简洁请求文件或路径。仅当用户明确说“随便生成”“示例”或“看看效果”时，才创建并标注为合成演示数据。
3. 只保留支撑交互与详情的字段。大数据集先聚合、分箱或抽样，避免把原始大文件完整内联。
4. 选择最小合适的图形：数值关系用散点/折线，分类比较用条形图，构成变化用堆叠图，密集类别用可选择网格；地理数据必须使用真实的 GeoJSON/经纬度与投影。

## 创建 Canvas

1. 调用 `present_ui`，固定 `kind="canvas"`。根对象只能有 `kind`、`id`、`fallbackText`、`props`；`title`、`description`、`html`、`css`、`script`、`state` **都必须放在 `props` 内**。`props.html` 必须是 HTML fragment（不是完整文档），交互时再提供 `script`；给稳定的 `id`，后续更新时复用它。
2. 使用内联数据、CSS 和 JavaScript。不要使用 `fetch`、XHR、WebSocket、远程 CDN、外部图片、`parent`、`top`、`opener` 或其他宿主窗口 API。
3. 只添加用户要求的筛选、选择或参数控件；使用语义化的 `label`、`select`、`input`、`button` 和原生键盘交互。筛选变化必须立刻更新主图、列表/表格和选中详情。
4. 保持一个主视觉、紧凑的已选项详情和必要的图例。默认不做 KPI 卡；只有用户明确要求且指标随交互变化时，最多保留三个。不要堆砌装饰性状态块、搜索框或“重置”按钮。
5. 让图表本身可读：标注轴、单位、关键值和多系列图例；颜色之外同时使用形状、文字或线型。为 SVG/Canvas 提供标题、描述或等价可访问文本。
6. 设计为窄宽度也可用：避免固定视口高度、水平溢出、固定定位和内部滚动；控件在窄屏换行，表格过宽时提供响应式容器。
7. 所有用户输入与交互状态保留在 Canvas 内。`window.aurevoy.state` 只读地提供初始状态；不要尝试向宿主发送消息或读取宿主数据。

## Aurevoy 视觉语言

Canvas 是 Aurevoy 对话的一部分，不是独立网页或通用暗色 dashboard。外层卡片已经展示 `props.title` 与 `props.description`，因此 HTML fragment 内不要重复标题、日期横幅或第二层页面容器。

1. 颜色必须使用 Canvas 已注入的主题变量：`--av-bg`、`--av-surface`、`--av-text`、`--av-muted`、`--av-border`、`--av-accent`、`--av-accent-contrast`、`--av-accent-soft-bg`、`--av-accent-soft-fg`。不要硬编码整套浅色/深色调色板、Tailwind 色值、白色卡片或黑灰背景；深浅主题必须自然切换。
2. 根节点保持透明、无边框、无阴影、全宽。只在必要的选中详情或少量动态指标上使用一个低强调 surface；不要给每条列表项、分组或布局容器重复套卡片。
3. 延续项目的克制留白与 Mist Teal 强调：正文使用 `--av-text`，辅助信息用 `--av-muted`，只将 `--av-accent` 用于当前选中态、关键标记和一个主要操作。不要把多种鲜艳颜色当作装饰。
4. 片段内不使用 `<h1>`，也不重述用户请求。标题交给 `props.title`；图例、坐标、数值和当前选中项才留在片段中。
5. 控件必须使用原生 `<button>`、`<input>`、`<select>`、`<textarea>`，并保留浏览器焦点样式。不要用可点击的 `<div>`、伪 tab 或仅靠颜色表达选中状态；筛选 tab 要用 `button`，并提供 `aria-pressed` 或 `aria-selected`。
6. 列表或新闻流默认只展示摘要；点击或键盘选择一项后才显示该项详情。不要让全部条目在首屏同时展开。卡片点击区域应是明确的 `button`，而不是整个 `div`。

## 验证与交付

1. 调用前检查 HTML、CSS、JavaScript 中没有未定义的查询元素，且首屏在不操作时也有价值。
2. 确认主交互会更新至少一个可见视觉元素；筛选后无结果时明确显示空状态；所有默认展开项不得超过一个。
3. 检查 fragment 没有重复 `props.title`、硬编码深浅色背景、大于三个的 KPI/状态块，及可点击 `div`。
4. 提供简短的对话说明，说明用户可以筛选、选择或调整什么。`present_ui` 返回成功后才可以说内联交互器已经展示。

## 不要

- 没有真实数据时假装来自用户数据。
- 把大型原始数据、密钥或工作区无关内容嵌进 Canvas。
- 依赖不可用的会话宿主桥接、网络资源或文件预览来完成交互。
- 用 Canvas 替代用户要求交付的长篇、可保存 HTML 报告；那类需求加载 `research` skill，走 `bundle_report` + `attach_content`。
