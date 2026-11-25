---
name: psd-json-preview
description: 从 PSD 导出的 JSON 图层树和切片图片生成 HTML/CSS 预览。默认保留 PSD 的分组嵌套结构，用 --flatten 参数可切换为平铺模式。
---

# PSD JSON → HTML 预览

从 PSD 导出的 JSON 图层树和切片图片生成静态 HTML/CSS 预览。

**⭐ 新特性**：
- **2026-02-11**：支持在生成 HTML 预览的同时生成 React 组件（JSX + CSS Modules）

## 快速开始

### 生成 HTML 预览 + React 组件

```bash
py -3 scripts/generate_preview.py \
  --json /path/to/layer-tree.json \
  --images /path/to/images \
  --out /path/to/preview \
  --generate-react \
  --component-name MyComponent \
  --preserve-names
```

这会同时生成：
- HTML 预览页面（`preview/index.html`）
- React 组件（`preview/react-component/index.jsx` + `index.module.less`）

### 默认模式：仅生成 HTML 预览（保留分组结构）

```bash
py -3 scripts/generate_preview.py \
  --json /path/to/layer-tree.json \
  --images /path/to/images \
  --out /path/to/preview
```

生成的 HTML 会保留 PSD 的分组嵌套，例如：

```html
<div class="canvas">
  <div class="group_rs_card">
    <div class="layer_rs_layer_3"></div>
    <div class="layer_rs_layer_2"></div>
    <!-- ... -->
  </div>
</div>
```

### 平铺模式：所有图层平铺到 canvas（旧行为）

```bash
py -3 scripts/generate_preview.py \
  --json /path/to/layer-tree.json \
  --images /path/to/images \
  --out /path/to/preview \
  --flatten
```

添加 `--flatten` 参数后，所有图层会直接放在 canvas 下，不保留分组关系。

## 输出结构

### 仅生成预览

```
preview/
├── index.html    （HTML 预览页面）
├── styles.css    （CSS 样式文件）
└── images/       （复制的图片资源）
    └── <copied slices>
```

### 生成预览 + React 组件

```
preview/
├── index.html           （HTML 预览页面）
├── styles.css           （CSS 样式文件）
├── react-component/     （React 组件）
│   ├── index.jsx           （React 组件代码）
│   ├── index.module.less  （CSS Modules 样式）
│   └── images/            （组件图片资源）
│       └── <copied slices>
└── images/              （预览图片资源）
    └── <copied slices>
```

## 期望的 JSON 结构

JSON 应为数组（或对象），节点结构如下：

```json
{
  "name": "layer-name",
  "kind": "group|pixel|type",
  "visible": true,
  "bbox": [x1, y1, x2, y2],
  "children": []
}
```

脚本使用 `bbox` 进行定位，并按名称匹配图片文件：

- `layer-name` → `layer-name.png`（也支持 .jpg/.jpeg/.webp）

## 核心行为

### 默认模式（保留分组）

- ✅ 自动识别 `kind: "group"` 的图层组
- ✅ 生成嵌套的 `<div>` 结构
- ✅ 自动计算相对坐标（子图层相对父容器定位）
- ✅ 分组容器自动添加 `position: absolute` 规则
- ✅ 便于后续手动调整和维护

### 平铺模式（--flatten）

- 所有图层直接放在 canvas 下
- 使用绝对坐标（相对 canvas）
- 适合快速预览和设计验证
- 不便于后续代码维护

## 命令行参数

```bash
python scripts/generate_preview.py --help
```

关键参数：

- `--json`：JSON 图层树文件路径（必需）
- `--images`：图片目录路径（必需）
- `--out`：输出目录路径（必需）
- `--flatten`：使用平铺模式（不保留分组结构）
- `--dict`：项目级图层名翻译字典 JSON 文件路径（可选，用于翻译拼音/缩写等项目特有术语）
- `--copy-all`：复制所有图片（不仅是匹配到的）
- `--include-text`：把文字图层渲染成 `<div>` 标签（默认关闭）。当开启此参数时，脚本会直接读取 JSON 中的文本内容和样式进行 HTML 还原，而不是寻找对应的切片图片。这对于需要保留页面文案可编辑性、SEO 友好或减少图片体积的场景非常重要。
- `--generate-react`：同时生成 React 组件（JSX + CSS Modules）
- `--generate-vue`：同时生成 Vue 组件（单文件组件 SFC）
- `--component-name`：React 组件名称（默认为 PsdComponent）
- `--preserve-names`：React 组件中保留PSD原始图层名作为类名（便于设计对应）

## 使用建议

### 何时使用默认模式（保留分组）

- ✅ 需要生成易维护的代码
- ✅ 后续会手动调整样式
- ✅ PSD 设计有明确的分组结构
- ✅ 作为前端开发的起点

### 何时使用平铺模式（--flatten）

- ✅ 仅用于设计稿验证
- ✅ 快速预览效果
- ✅ PSD 分组结构混乱或无意义
- ✅ 作为设计交付文档

## 技术细节：分组结构的自动处理

默认模式下，脚本会自动：

1. **识别分组**：检测 `kind: "group"` 的节点
2. **生成嵌套 HTML**：为每个分组创建容器 `<div>`
3. **计算相对坐标**：子图层坐标 = 原始坐标 - 父容器偏移
4. **生成 CSS 规则**：

   ```css
   /* 分组容器 */
   .group_rs_card {
     position: absolute;
     left: 119px;
     top: 145px;
     width: 620px;
     height: 849px;
   }

   /* 子元素定位规则 */
   .group_rs_card > div {
     position: absolute;
     display: block;
   }

   /* 子图层（相对坐标） */
   .layer_rs_layer_3 {
     left: 194px; /* 313 - 119 */
     top: 0px; /* 145 - 145 */
     width: 343px;
     height: 284px;
   }
   ```

## 说明

- 如果图层找不到匹配图片，则会跳过（除非开启 `--include-text`）。
- 若 JSON 根节点为数组，使用第一个含 bbox 的节点作为画布。
- 默认只复制**匹配到的**图片到 `output/images`。

## 参考

- 命名与映射说明见 `references/json-format.md`。
- 平铺模式的手动分组指南见 `references/MANUAL_GROUPING.md`（仅用于 --flatten 模式）。

```

```
