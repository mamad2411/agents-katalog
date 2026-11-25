---
name: wiki-diagram
description: Add Mermaid diagrams to wiki pages to aid understanding. This skill should be used during ingest/review when a concept involves a process, architecture, sequence, hierarchy, or comparison that is easier to grasp visually, or when the user explicitly asks to "画图"/"配图"/"diagram"/"visualize" a concept.
---

# Wiki Diagram — Mermaid 可视化

用 Mermaid 给概念页配图。Obsidian 原生渲染 ```mermaid 代码块，无需安装插件。

## 何时配图 When to Diagram

只在"文字描述比图更难懂"时配图，不要每页都加。适合配图的情况：

- 多步骤流程/算法 → flowchart
- 协议交互/攻击步骤，含时序（适合 COMP4337） → sequenceDiagram
- 系统架构/模型结构，含组件关系 → flowchart
- 概念分类/知识地图 → mindmap
- 状态转换/生命周期 → stateDiagram-v2
- 概念间关系网（跨课程连接） → graph

不适合配图：单一定义、纯数学公式推导、线性叙述无分支无关系的内容。

## 图表类型映射 Diagram Type Mapping

| 内容类型 | Mermaid 类型 |
|---|---|
| 算法步骤/数据处理流程 | `flowchart TD` |
| 协议/攻击交互序列 | `sequenceDiagram` |
| 模型架构/系统组件 | `flowchart LR` |
| 概念分类/知识地图 | `mindmap` |
| 状态机/生命周期 | `stateDiagram-v2` |
| 概念间关系网 | `graph TD` |

## 放置位置 Placement

在概念页的 `直觉 Intuition` 或 `详细解释 Detailed` 章节之后，新增 `## 图解 Diagram` 小节。局部插入，不重写全页。

```markdown
## 图解 Diagram

\`\`\`mermaid
flowchart TD
    A[输入 Input] --> B[处理 Process]
    B --> C[输出 Output]
\`\`\`
```

## 质量规则 Quality Rules

1. **≤10 个节点**：超过就简化或只画核心路径
2. **双语标签**：节点文字用"中文 English"或保持和页面其他部分一致的语言风格
3. **一页最多 1-2 个图**：避免视觉噪音
4. **语法要对**：节点 ID、箭头、括号/引号配对正确，避免渲染失败
5. 若图表来自课件原图：先在来源页文字描述要点，再判断是否用 Mermaid 重绘成更清晰的逻辑图（不需要 1:1 还原）

## 触发方式 Triggers

- **自动**：ingest/review 创建或更新概念页时，按上述标准判断是否需要配图（见 wiki-ingest 步骤）
- **手动**：用户说"画图"/"画个图"/"配图"/"diagram this"/"visualize X"，或用 `/diagram {concept}` 命令，针对指定概念页生成/补充图表
