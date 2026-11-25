---
name: psd-component-splitter
description: 将 PSD 设计稿按第一级分组拆分为独立的 React 或 Vue 组件。适用于从 PSD 设计稿生成组件化前端代码，支持自动生成 JSX/CSS Modules 或 Vue SFC 文件。
---

# PSD 组件拆分器

将 PSD 图层结构按第一级分组拆分为多个独立组件文件，支持 React (JSX + CSS Modules) 和 Vue (SFC)。

## 快速开始

### React

```bash
py -3 .claude/skills/psd-component-splitter/scripts/split_components.py \
  --json layer-tree.json \
  --images sliced-images/ \
  --out output/ \
  --framework react
```

> 输出目录：`output/react-split/`

### Vue

```bash
py -3 .claude/skills/psd-component-splitter/scripts/split_components.py \
  --json layer-tree.json \
  --images sliced-images/ \
  --out output/ \
  --framework vue
```

> 输出目录：`output/vue-split/`

## 前置依赖

```bash
# 1. 导出图层切片
py -3 .claude/skills/psd-slicer/scripts/export_slices.py \
  design.psd -o sliced-images/

# 2. 生成图层结构 JSON
py -3 .claude/skills/psd-layer-reader/scripts/psd_layers.py \
  design.psd -o layer-tree.json
```

## 参数说明

| 参数 | 必需 | 说明 |
|------|------|------|
| `--json` | ✅ | JSON 图层树文件路径 |
| `--images` | ✅ | 切片图片目录路径 |
| `--out` | ✅ | 输出目录路径 |
| `--framework` | ✅ | `react` 或 `vue` |
| `--component-name` | ❌ | 主组件名称（默认：`PsdApp`） |

## 输出结构

脚本会根据框架类型自动在输出目录下创建对应的子目录：
- React: `<out>/react-split/`
- Vue: `<out>/vue-split/`

### React

```
output/react-split/
├── App.jsx                     # 主入口组件
├── App.module.css              # 全局样式
├── components/                 # 组件目录
│   ├── group-header/
│   │   ├── index.jsx
│   │   └── index.module.css
│   └── ...
└── images/                     # 图片资源
    └── ...
```

### Vue

```
output/vue-split/
├── App.vue                     # 主入口组件
├── components/                 # 组件目录
│   ├── group-header/
│   │   └── index.vue
│   └── ...
└── images/                     # 图片资源
    └── ...
```

## 工作原理

1. **解析 JSON**：读取图层树结构
2. **识别分组**：遍历第一级图层，识别 `kind: "group"` 节点
3. **生成组件**：将分组名转换为 PascalCase（如 `user-card` → `UserCard`）
4. **创建入口**：生成 App.jsx/App.vue 整合所有子组件
5. **复制资源**：将图片复制到 `images/` 目录

## 组件特性

**React**
- CSS Modules 样式隔离
- 支持 `className`、`style`、`onClick` props
- BEM 类名规范

**Vue**
- 单文件组件（SFC）
- Scoped CSS
- 支持 props 传递

## 使用建议

### ✅ 适用场景

- PSD 第一级分组代表不同功能模块
- 需要组件化开发，各模块独立维护
- 团队协作开发

### ❌ 不适用场景

- PSD 无明确分组结构
- 需要像素级精确的单页预览（使用 psd-json-preview）
- 需要响应式 flexbox 布局（使用 psd-semantic-layout）

## 故障排查

### 未找到有效的第一级分组

**原因**：PSD 结构中没有 `kind: "group"` 的第一级节点

**解决**：
- 检查 JSON 结构确认存在分组图层
- 在 PSD 中创建分组后重新导出

### 组件生成失败

**原因**：生成器模块未找到或脚本路径错误

**解决**：
- 确认脚本目录结构完整
- 检查 `react_generator.py` 或 `vue_generator.py` 是否存在

### 图片未复制

**原因**：图片名称与图层名不匹配

**解决**：
- 切片时使用 `--mapping-json` 参数
- 检查 JSON 中的 `name` 字段与图片文件名是否一致

## 相关技能

- **psd-layer-reader** - 读取 PSD 图层结构为 JSON
- **psd-slicer** - 导出 PSD 图层为 PNG 图片
- **psd-json-preview** - 生成 HTML 预览
- **psd-semantic-layout** - 生成语义化 flexbox 布局

## 详细文档

完整工作流、实战示例和常见问题，参见 [references/WORKFLOW.md](references/WORKFLOW.md)。
