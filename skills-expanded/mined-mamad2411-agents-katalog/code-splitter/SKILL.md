---
name: code-splitter
description: 智能分析 React 组件代码，识别可拆分的子组件并生成独立组件文件。使用场景：(1) psd-json-preview 生成的大组件需要优化结构，(2) 将单个复杂组件拆分为多个可复用小组件，(3) 自动生成带 Props 接口的标准化组件。
---

# Code Splitter - 组件代码拆分器

## 快速开始

```bash
# 1. 分析组件（建议模式 - 只生成报告）
py -3 .claude/skills/code-splitter/scripts/split_component.py \
  --input ./my-component/ \
  --dry-run

# 2. 查看报告后，生成实际组件
py -3 .claude/skills/code-splitter/scripts/component_generator.py \
  --input ./my-component/ \
  --output ./split/
```

## 系统要求

- Python 3.6+
- 组件目录包含 `index.jsx` 和 `index.module.css`

## 两种工作模式

### 模式 1：Suggestion Mode（建议模式）

使用 `split_component.py` 分析并生成报告，不创建文件：

```bash
py -3 scripts/split_component.py --input ./my-component/ --dry-run
py -3 scripts/split_component.py --input ./my-component/ --dry-run --output report.md
py -3 scripts/split_component.py --input ./my-component/ --dry-run --min-score 0.5
```

### 模式 2：Generate Mode（生成模式）

使用 `component_generator.py` 生成实际组件：

```bash
py -3 scripts/component_generator.py --input ./my-component/ --output ./split/
py -3 scripts/component_generator.py --input ./my-component/ --output ./split/ --min-score 0.5
py -3 scripts/component_generator.py --input ./my-component/ --output ./split/ --dry-run
```

## 分析维度

基于四个维度识别可拆分组件：

1. **语义类名**：识别 `btn-*`、`card-*`、`header-*` 等模式
2. **DOM 结构**：检测包裹多个子元素的容器
3. **重复模式**：发现相似结构（如多个按钮）
4. **位置分析**：从 CSS 推断 Header/Footer 区域

## 置信度解读

- **HIGH (≥0.8)**：强建议拆分，风险低
- **MEDIUM (0.5-0.8)**：可以拆分，可能需要微调
- **LOW (<0.5)**：谨慎考虑，可能保持现状更好

## 输出结构

```
split-output/
├── app/
│   ├── index.jsx          # 主入口组件
│   └── index.module.css   # 主样式
├── card/                  # 拆分出的子组件
│   ├── index.jsx
│   └── index.module.css
└── generation-report.json # 生成报告
```

## 与其他技能配合

- **psd-json-preview**：处理生成的大组件
- **psd-component-splitter**：进一步优化拆分结果
- **frontend-code-review**：审查生成的组件代码

## 参考文档

- **详细使用指南**：[references/USER_GUIDE.md](references/USER_GUIDE.md)
- **技术实现细节**：[references/IMPLEMENTATION.md](references/IMPLEMENTATION.md)
- **故障排查**：[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)

## 已知限制

1. 只支持 React 函数组件（v2 支持 Vue）
2. 使用正则解析 JSX（覆盖 80% 常见场景）
3. 不处理 CSS-in-JS（只支持 CSS Modules）
4. v1 不做 CSS 坐标转换（原样复制样式值）
5. 不处理 hooks 依赖（state 留在原组件）
