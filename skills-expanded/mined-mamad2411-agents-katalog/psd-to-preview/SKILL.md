---
name: psd-to-preview
description: 从 PSD 设计文件到预览页面 + React 组件 + Vue 组件的完整转换工作流。
---

# psd-to-preview: PSD 转预览和 React 组件

## AI 执行指令（置顶）

**当用户请求使用此技能时，必须按以下步骤实际执行命令。**

**AI 执行规则**：

1. **默认**：`psd-slicer` 现已默认支持导出所有的图层（包含中文字符和非常规字符），并且会自动在 PSD 目录下寻找 `layer-tree.json` 等映射文件。
2. **规范化**：如果设计稿的层级命名很乱，想要标准化图层名字，可以在调用 `psd-slicer` 时直接加上 `--auto-rename` 参数将资源转为 `layer-xxx` 格式。如果想要强制图层名字只能是标准的英文+横杠，可以使用 `--strict-naming` 过滤掉不规范命名的层。
3. **输出文案**：如果用户要求“输出真实文本”或“文案转代码”，必须在步骤 2 使用 `--skip-type`，并在步骤 3 使用 `--include-text`

### 技能依赖（必备条件）

此技能作为工作流入口，高度依赖以下三个核心技能。在执行前请确保它们在指定路径存在：

- `psd-layer-reader`: 负责解析 PSD 结构生成 JSON 树。
- `psd-slicer`: 负责导出图层切片图片。
- `psd-json-preview`: 负责将 JSON 和图片合成为终端代码（HTML/React/Vue）。

### 依赖预检查（AI 执行前必须执行）

AI 在执行工作流前，**必须**先检查依赖是否已安装：

```powershell
# 检查 psd-tools
py -3 -c "import psd_tools" 2>&1
# 如果返回 ImportError，表示未安装

# 检查 scikit-image
py -3 -c "import skimage" 2>&1
```

**如果缺少依赖，AI 必须询问用户**：

> "检测到缺少以下依赖，是否安装？
>
> - `psd-tools`（必需）
> - `scikit-image`（必需）
>
> 输入 '是' 确认安装，或 '否' 跳过（部分图层可能无法导出）"

**用户确认后，AI 执行安装**：

```powershell
# 安装必需依赖
py -3 -m pip install psd-tools

# 安装可选依赖（如果用户同意）
py -3 -m pip install scikit-image
```

**版本检查（可选）**：

```powershell
# 检查已安装的版本
py -3 -c "import psd_tools; print('psd-tools:', psd_tools.__version__)"
py -3 -c "import skimage; print('scikit-image:', skimage.__version__)"
```

**注意事项**:

- 如果用户选择不安装 `psd-tools`，无法继续执行工作流
- 如果用户选择不安装 `scikit-image`，可以执行但部分带图层效果的元素会被跳过
- 安装完成后，建议重新检查依赖是否安装成功

---

### 执行命令

```powershell
# 步骤 1：图层解析
py -3 .claude/skills/psd-layer-reader/scripts/psd_layers.py \
  <PSD文件路径> --output <输出目录>/layer-tree.json

# 步骤 2：图层切片
py -3 .claude/skills/psd-slicer/scripts/export_slices.py \
  --psd <PSD文件路径> --output <输出目录>/sliced-images
# 注：psd-slicer 现默认允许各种图层导出并在工作目录自动查找映射 JSON。若用户需转命名规范化图形文件，可添加 --auto-rename。

# 步骤 3：代码生成
py -3 .claude/skills/psd-json-preview/scripts/generate_preview.py \
  --json <输出目录>/layer-tree.json --images <输出目录>/sliced-images \
  --out <输出目录> --generate-react --generate-vue \
  --component-name PsdComponent --preserve-names

---

### 高级方案：输出真实文本（保留文案可编辑性）

如果用户提到“要输出文案”、“文字转代码”或“文字不要切图”，请使用以下组合命令：

```powershell
# 步骤 2：图层切片（跳过文本图层，避免生成文字图片）
py -3 .claude/skills/psd-slicer/scripts/export_slices.py \
  --psd <PSD文件路径> --output <输出目录>/sliced-images --skip-type

# 步骤 3：代码生成（开启文本渲染，将文字转为 HTML/CSS）
py -3 .claude/skills/psd-json-preview/scripts/generate_preview.py \
  --json <输出目录>/layer-tree.json --images <输出目录>/sliced-images \
  --out <输出目录> --generate-react --generate-vue --include-text
```
```

**关键提醒**：

- ✅ 使用 `py -3`（Windows）或 `python3`（Linux/Mac）

---

### 执行检查清单

- [ ] `<输出目录>/layer-tree.json` 有数据
- [ ] `<输出目录>/sliced-images/` 有 PNG 文件
- [ ] `<输出目录>/preview/` 有 HTML 文件
- [ ] `<输出目录>/react-component/` 有 JSX 和 CSS 文件
- [ ] `<输出目录>/vue-component/` 有 Vue 文件

---

## 工作原理

PSD → psd-layer-reader → layer-tree.json → psd-slicer → sliced-images/ → psd-json-preview → preview/ + react-component/ + vue-component/

---

## 快速参考

### 核心参数

| 参数       | 说明         | 示例                    |
| ---------- | ------------ | ----------------------- |
| `<PSD路径>` | PSD 文件路径 | `assets/design.psd`     |
| `--output` | 输出目录     | `output/design-preview` |

### 常见问题

**Q: 某些图层没有被导出？**  
A: 大部分通常是因为图层不可见、不包含内容或者完全透明。如果使用了 `--strict-naming` 参数，则不合规命名（中文等）也会被跳过。

**Q: 导出的图层名字是乱的/中文的？**  
A: psd-slicer 会默认使用 PSD 中的原始名称进行导出。你可以在生成切片时加入 `--auto-rename` 将它们转化为通用的标准命名，或者确保 `psd-layer-reader` 已执行并在它的工作目录下自然匹配映射结构。

---

## 输出目录结构

```
output/
├── layer-tree.json       # 图层数据
├── sliced-images/        # PNG切片
├── preview/              # HTML 预览
│   ├── index.html
│   ├── styles.css
│   └── images/
├── react-component/      # React组件
│   ├── index.jsx
│   ├── index.module.css
│   └── images/
└── vue-component/        # Vue组件
    ├── index.vue
    └── images/
```

---

## 故障排查

| 错误          | 原因       | 解决方案         |
| ------------- | ---------- | ---------------- |
| PSD 未找到    | 路径错误   | 检查文件路径     |
| 权限错误      | 无写入权限 | 检查目录权限     |
| 预览加载失败  | 路径错误   | 确保目录结构完整 |
| JSON 解析错误 | 文件损坏   | 重新运行工作流   |

---

## 依赖说明

### 必需依赖

- `psd-tools`: PSD 文件解析核心库

### 可选依赖

- `scikit-image`: 用于导出包含图层效果的元素（如阴影、发光、渐变等）

### 手动安装命令

如果预检查阶段的自动安装失败，可手动执行：

```bash
# 安装依赖
py -3 -m pip install psd-tools
py -3 -m pip install scikit-image
```

**注意**：虽然 SKILL.md 中包含安装命令，但 AI 执行时**不会自动运行**。请参考"依赖预检查"小节，让 AI 在执行工作流前检查并安装依赖。

---

**版本**: 1.6 | **更新**: 2026年3月12日
