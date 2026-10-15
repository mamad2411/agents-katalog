---
name: component-analyzer
description: React/Vue 组件代码分析器 - 分析已生成组件，输出依赖图、重复代码报告和拆分建议。Use when analyzing React or Vue component code to identify optimization opportunities, detect duplicate patterns, build dependency graphs, and generate refactoring suggestions. Supports both JSON (machine-readable) and Markdown (human-readable) output formats.
---

# Component Analyzer - 组件代码分析器

用于分析 React/Vue 组件代码，自动解析组件结构、构建依赖关系图、检测重复模式，并生成智能的拆分建议。

## 快速开始

### 基本使用

```bash
# 分析 React 组件目录（JSON 格式输出）
py -3 .claude/skills/component-analyzer/scripts/analyze_components.py \
  --input ./react-components \
  --output ./analysis-report.json

# Markdown 格式报告
py -3 .claude/skills/component-analyzer/scripts/analyze_components.py \
  --input ./react-components \
  --format markdown
```

### 与 psd-component-splitter 配合使用

```bash
# 第一步：PSD 拆分为组件
py -3 .claude/skills/psd-component-splitter/scripts/split_components.py \
  --json layer-tree.json --images sliced-images/ \
  --out ./split-components/ --framework react

# 第二步：分析生成的组件
py -3 .claude/skills/component-analyzer/scripts/analyze_components.py \
  --input ./split-components/ --output ./component-analysis.json
```

## 命令行参数

| 参数 | 简写 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--input` | `-i` | ✅ | - | 组件目录路径 |
| `--output` | `-o` | ❌ | stdout | 输出文件路径 |
| `--format` | `-f` | ❌ | `json` | 输出格式：`json` 或 `markdown` |
| `--framework` | - | ❌ | `react` | 框架：`react` 或 `vue` |
| `--threshold` | `-t` | ❌ | `0.7` | 相似度阈值（0.0-1.0） |
| `--verbose` | `-v` | ❌ | - | 显示详细进度 |

## 核心功能

### 1. 组件结构分析
- 解析 Import/Export 语句
- 提取 Props 签名
- 分析 JSX 元素结构
- 检测 CSS Module 使用

### 2. 依赖图构建
- 扫描目录收集组件
- 解析组件间依赖关系
- 检测循环依赖
- 识别入口组件

### 3. 重复模式检测
- Props 签名相似性（40%）
- JSX 结构相似性（40%）
- CSS Module 使用（20%）
- 层次聚类算法分组

### 4. 智能拆分建议
- **提取子组件** - 识别可复用的重复 JSX
- **合并组件** - 发现可合并的相似组件
- **Props 重构** - 统一组件接口
- **样式分离** - 提取共享样式
- **架构优化** - 检测深层嵌套

## 输出示例

### JSON 格式
```json
{
  "summary": {
    "total_components": 12,
    "patterns_detected": 4,
    "suggestions_count": 8
  },
  "dependency_graph": {
    "nodes": [...],
    "edges": [...]
  },
  "patterns": [...],
  "suggestions": [...]
}
```

### Markdown 格式
包含概览统计、详细建议列表、依赖图可视化。

## 模块说明

### scripts/

- **`analyze_components.py`** - CLI 入口，整合所有功能
- **`react_ast_parser.py`** - React 组件 AST 解析（正则实现）
- **`dependency_graph.py`** - 依赖图构建与循环依赖检测
- **`pattern_detector.py`** - 相似度计算与模式检测
- **`split_suggester.py`** - 拆分建议生成与格式化输出

## 实现细节

详见 [references/IMPLEMENTATION.md](references/IMPLEMENTATION.md) 了解：
- 相似度计算算法
- 正则表达式解析模式
- 数据结构定义
- 扩展开发指南

## 局限性

1. **解析能力**：使用正则表达式，不支持完整 AST
2. **框架支持**：主要支持 React，Vue 支持有限
3. **相似度计算**：基于特征匹配，语义分析能力有限
4. **性能**：大型项目（>100 组件）分析可能较慢

## 前置依赖

- Python 3.6+
- 输入：已生成的 React/Vue 组件目录
