---
name: paper-context
description: Use this skill to build a quick, structured Chinese overview of an empirical (economics/social-science) paper — its research background, question, approach, main findings, and literature position. For fast top-journal reading, relevance screening, and mapping a paper's place in the literature. Keeps figure/table citations so a human can verify; never fabricates references.
---

# paper-context（论文整体解读与文献定位）

从**整体介绍**与**文献定位**两个角度，快速读懂一篇实证论文：它想回应什么问题、大致怎么做、发现了什么、站在哪些文献之间。产出结构化中文短笔记，并**保留图表编号引证**，供人工核对。本 skill 是第 1 讲「任务切割」读法的一环，对应配套阅读笔记的「整体介绍」与「迷你文献定位」。

## 何时用

- 拿到一篇顶刊论文，想先花几分钟看懂全貌、判断和自己的研究是否相关；
- 想弄清一篇论文的研究背景、研究问题、研究思路与主要结论；
- 想快速梳理一篇论文的文献坐标（它接续谁、反驳谁、补上什么空白），建立一小片文献地图。

## 使用方式（提示词）

把论文 PDF 连同下面的要求发给 agent（网页版 ChatGPT、Claude、Codex、OpenCode 均可）：

> 请**只从「整体介绍」这一个角度**帮我写一份简短的中文笔记，包含：研究背景、研究问题、研究思路（一两段讲清、不展开公式）、主要结论（给关键数量级）。控制在一页以内；**只依据论文本身，不要编造**；每条结论标注它对应论文里的哪张图或哪张表。

做文献定位时，追加一问：

> 再帮我梳理这篇论文的文献坐标：主要对话哪几支文献，各建立了什么、又不能回答什么；它声称补上的空白是什么。**只依据论文及其参考文献，不要编造不存在的文献**。

## 输出约定

- 结构固定：研究背景 → 研究问题 → 研究思路 → 主要结论 →（可选）文献坐标；
- 结论后保留图/表编号（如 Figure 2、Table 1），便于回原文核对；
- 参考文献按课程 myAPA 格式记录（`作者 (年份). 标题. 期刊, 卷(期), 页码.` + `[Link]`/`[PDF]`/`[Google]`）。

## 最小使用示例

> 用 paper-context 读一下这篇 QJE 论文（附 PDF），先给我一份「整体介绍」笔记，判断它和产业政策评估相不相关。

## 人工检查清单

- **AI 辅助、不替代研究判断**：这份笔记是初稿，不是定论；结论对不对、方法能不能迁移，由你判断。
- 结论逐条回原文核对（看图表编号）。
- **文献不许 AI 凭空生成**：找相关文献或「被引用」必须用检索工具（Google Scholar、Connected Papers 等）查实，AI 只用来归纳你查到的题录；URL 拿不准就留空，不编造。

## 来源与许可

- 原创：本课程为「连享会 2026 暑期班·初级班」编写，Agent 无关的开放 Skill，MIT（随仓库 `LICENSE-CODE`）。
- 最后验证日期：<!-- TODO: T7 彩排双端实测后填写 -->
