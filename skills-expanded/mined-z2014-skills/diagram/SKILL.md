---
name: diagram
description: "Feishu-whiteboard-style diagrams for distilling AI output into one picture per question: layered architecture, flowchart, sequence, comparison matrix. Agent writes structured JSON, a bundled renderer produces a self-contained HTML/SVG preview. Use when presenting a design, architecture, process, option comparison or plan to a human, or when asked to draw a diagram. 画图规范：需要把方案、架构、流程、方案对比或计划用图呈现给人看，或用户要求画图时使用。"
---

# 画图

目标：把 AI 产出里人真正关心的信息提炼出来，用一张最直观的图呈现。**你只负责想清楚内容，输出结构化数据；样式和排版交给渲染脚本**，保证谁来画都长得一样（飞书画板风格）。

## 工作步骤

1. **先写一句话结论**：这张图想让人得出什么判断。写不出来就说明还没想清楚，先别画。
2. **选图**：按下表，一张图只回答一个问题。一个问题需要两种图时，画两张。
3. **写数据**：按 `types/<类型>.md` 里的格式写一个 JSON 文件，例如 `diagram.json`。
4. **渲染**：`python3 <本 skill 目录>/scripts/render.py diagram.json -o diagram.html`，打开 HTML 检查。
5. **自检**（见文末清单），不通过就改数据重新渲染。
6. **交付**：一句话结论 + HTML 文件路径；需要贴进 Markdown 时，加 `--mermaid` 参数输出 Mermaid 代码。

如果环境里有 `draw_*` 这类 MCP 画图工具，优先直接调用工具（参数就是同一份 JSON）。没有 Python 时，直接输出 Mermaid，第一行加上下方兜底里的飞书主题。

## 选图

| 要回答的问题 | 图类型 | 定义 |
| --- | --- | --- |
| 系统由什么组成、谁依赖谁 | 分层架构图 `layered-architecture` | `types/layered-architecture.md` |
| 一件事怎么一步步走、在哪里分叉 | 流程图 `flowchart` | `types/flowchart.md` |
| 多个参与方按什么顺序交互 | 时序图 `sequence` | `types/sequence.md` |
| 几个方案选哪个 | 方案对比矩阵 `comparison-matrix` | `types/comparison-matrix.md` |

不要画"影响范围图"（这次改动碰到哪些文件/模块）。它是事实，应该由工具从 `git diff` 和代码依赖计算出来，不能由 Agent 凭印象画；设计阶段只在架构图里标注"计划新增/修改"。

## 兜底

以上四种都不合适时（例如状态图、ER 图），少用 `general`：把 Mermaid 原文写进 `mermaid` 字段。渲染脚本会套上飞书主题和卡片。这种图没有稳定的节点 id，评论只能挂在整张图上。某种图反复出现时，提议做成正式类型。

```json
{
  "type": "general",
  "title": "需求的状态有哪些",
  "summary": "需求只有在拍板点会挂起",
  "mermaid": "stateDiagram-v2\n  [*] --> 进行中\n  进行中 --> 待放行\n  待放行 --> 进行中: 放行\n  待放行 --> [*]: 完成"
}
```

没有渲染脚本时，在 Mermaid 第一行加上：

```text
%%{init: {"theme":"base","themeVariables":{"primaryColor":"#EEF3FF","primaryBorderColor":"#7A9CF5","primaryTextColor":"#1F2329","lineColor":"#646A73","secondaryColor":"#FFF5C2","tertiaryColor":"#F8F9FA","fontFamily":"PingFang SC, Noto Sans CJK SC, sans-serif","fontSize":"13px"}}}%%
```

## 画图原则

- **一张图一个问题**。架构图里不画先后顺序；流程图里不画模块组成；不在一张图里混用"调用"和"读写数据"两种关系。
- **节点数 ≤ 12**（硬上限 15）。超了就拆：架构图按 C4 思路分层下钻（先系统全景，再展开某个模块），流程图把子流程单独画。
- **命名和代码一致**：模块名用代码里真实的目录/服务名，或者"中文名 + 代码名"。
- **id 稳定（硬规则）**：修订时，没变的和被修改的元素沿用上一版的 id；只有新元素才分配新 id。禁止给已有元素改 id。
- **颜色有固定含义，不能挪作他用**：绿 = 新增，橙 = 修改，灰/白 = 不变，红 = 风险或异常分支。用 `status` 字段表达，不要自己指定颜色。
- **文字短**：节点内 ≤ 12 个字，细节放到图外的说明里。
- **先结论后图**：每张图都带 `title`（回答什么问题）和 `summary`（一句话结论）。

## 处理图上的评论

评论锚定在「哪张图、哪个版本、哪个元素 id」上，并带有元素名称和用户原文。每条都按直接指令处理，不要让用户再复述一遍。

评论改的是设计，不只是图。先改设计文档或计划，再重画图，两份一起交付，保证一致。

每条评论只给一个结论：`已改`、`不改`（附原因）、或 `需要确认`（要用户拍板）。

只动被评论的元素和直接相关的连线。其余元素和全部已有 id 保持不变。

交付新版本时按评论逐条列出：锚定 id、结论、一句话说明。

## 自检清单

- [ ] JSON 能被 `render.py` 正常渲染，没有报错或警告
- [ ] 一张图只回答 `title` 里那一个问题
- [ ] 节点数没超限
- [ ] 可评论元素都有图内唯一的 id；旧元素的 id 没有被改掉
- [ ] `status` 只用在真的新增、修改、有风险的地方
- [ ] 流程图有且只有一个起点，每条路径都能走到终点
- [ ] 人只看这张图和一句话结论，就能做出判断
