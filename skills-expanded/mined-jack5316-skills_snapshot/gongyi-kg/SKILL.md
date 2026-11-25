
---
name: gongyi-kg
description: 工艺文件知识图谱生成器。扫描工艺文件目录，读取 PDF 作业指导书和学习记录，用 AI 生成结构化 Obsidian 知识图谱（产品体系、工艺流程、领域分类、项目地图、学习路径）。Use when you want to build or update the process engineering knowledge graph.
---

# 工艺知识图谱 (/gongyi-kg)

为工艺设备部文档体系构建 AI 知识图谱，整合进 Obsidian vault。

## Quick Start

```bash
python3 _scripts/gongyi_knowledge_graph.py --save
```

## Features

1. **全景 Mermaid 图** - 产品族 → 工艺环节 → 关键文档三层关系可视化
2. **产品体系矩阵** - 柴发方舱/配电方舱/IT液冷/集装箱/钣金件 × 文档映射
3. **知识领域分类** - 安全/焊接/电气/管道/结构/测试/集成生产
4. **项目地图** - 新加坡K2/马来西亚/宁夏美团/阿里 项目矩阵
5. **管培生8周学习路径** - 按文档依赖关系排列的学习顺序
6. **核心概念索引** - 20-30 个关键工艺概念的 [[wikilink]] 节点

## Options

- `--save`: 保存到 vault（`Sources/工艺知识图谱 - YYYY-MM-DD.md`）
- `--no-pdf`: 跳过 PDF 读取（更快，仅用文件名推断关系）
- `--path PATH`: 指定工艺文件目录（默认 ~/Downloads/工艺文件）

## Examples

```bash
# 生成完整知识图谱（含 PDF 深度分析）并保存
python3 _scripts/gongyi_knowledge_graph.py --save

# 快速模式（仅扫描文件名）
python3 _scripts/gongyi_knowledge_graph.py --save --no-pdf

# 指定不同目录
python3 _scripts/gongyi_knowledge_graph.py --path ~/Documents/工艺文件 --save
```

## Output

- **保存文件**: `Sources/工艺知识图谱 - YYYY-MM-DD.md`
- **内容**: Mermaid 可视化图 + 产品体系 + 领域分类 + 项目地图 + 学习路径 + 概念索引

## 依赖文件

- `~/Downloads/工艺文件/工艺文件学习记录汇总.md` - 知识种子
- `~/Downloads/工艺文件/工艺科实习学习手册.md` - 学习框架
- 5 个核心 PDF（自动读取，需安装 poppler 或 pypdf）
