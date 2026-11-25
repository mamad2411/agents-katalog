---
name: research-writing
description: 科研论文写作 prompt 库：中英互译（LaTeX 与 Word 两版）、缩写与扩写、英文和中文润色、去 AI 味、终稿逻辑检查、审稿人视角评审与两轮严苛审稿、论文架构图、实验绘图推荐、图表标题、实验分析段落，以及写作模型与第三方写作 Skills 推荐。用户要翻译、润色、压缩或扩写论文段落，写 figure 或 table caption，把实验数据写成分析段落，挑实验图表类型，生成方法框架图，或想在投稿前模拟审稿时使用，即使用户没有提到 prompt 或本技能名。
metadata:
  updated: "2026-11-11"
  sources: Leey21/awesome-ai-research-writing@df0af72, Leey21/awesome-ai-research-writing#40
  authors: Leey21, MySunX, Pioneer-wxh
  curated_by: Alice39s/agent-stash
---

# 科研写作 Prompt

`references/` 下每个文件是一段完整的科研写作 prompt，多数按 Role、Task、Constraints、Output Format、Input 组织。文件开头的 frontmatter 记录用途（`use_when`）、需要的输入（`input`）、原作者（`authors`）和出处链接（`source`）。

## 用法

1. 在下面的索引里按任务找到 reference。同一任务分 LaTeX 版和 Word 版时，按稿件的去向选：放进 `.tex` 的用 LaTeX 版（转义 `%`、`_`、`&`），粘贴进 Word 的用 Word 版（纯文本，不带 Markdown 标记）。
2. 读这个 reference 的全文。
3. 用户要处理结果时，把 prompt 当作本轮指令执行：`[在此处粘贴…]` 这类占位换成用户给的内容，按 prompt 的约束和输出格式（Part 1、Part 2……）直接给出结果。用户要 prompt 本身时，原样给出代码块里的文本。
4. 占位需要的输入缺失时（投稿目标、实验数据、方法描述），先向用户要，不要自己编。
5. 用户项目里已有的写作规范、会议模板和页数要求，优先于 prompt 里的通用约束。

## 索引

### 翻译

| Reference                                              | 用途                                                                 | 输入            | 作者   |
| ------------------------------------------------------ | -------------------------------------------------------------------- | --------------- | ------ |
| [中转英（LaTeX）](references/translate-zh-en-latex.md) | 把中文草稿翻译并润色成英文论文段落，结果放进 .tex                    | 中文草稿        | Leey21 |
| [英转中（LaTeX）](references/translate-en-zh-latex.md) | 把英文 LaTeX 片段直译成中文用于阅读核对，去掉引用、标签与公式语法    | 英文 LaTeX 片段 | Leey21 |
| [中转英（Word）](references/translate-zh-en-word.md)   | 把中文草稿翻译并润色成英文论文段落，结果粘贴进 Word，不做 LaTeX 转义 | 中文草稿        | Leey21 |

### 润色与改写

| Reference                                             | 用途                                                       | 输入                     | 作者   |
| ----------------------------------------------------- | ---------------------------------------------------------- | ------------------------ | ------ |
| [中文草稿重写（Word）](references/rewrite-zh-word.md) | 把口语化或零散要点的中文草稿重写成中文论文段落             | 中文草稿、零散想法或要点 | Leey21 |
| [缩写（LaTeX）](references/condense-en-latex.md)      | 英文段落缩短 5 到 15 个词，保留全部信息与实验参数          | 英文 LaTeX 片段          | Leey21 |
| [扩写（LaTeX）](references/expand-en-latex.md)        | 英文段落加长 5 到 15 个词，写出原文隐含的前提、因果与结论  | 英文 LaTeX 片段          | Leey21 |
| [英文润色（LaTeX）](references/polish-en-latex.md)    | 修正英文论文段落的语法、句式与语体，保留 LaTeX 命令        | 英文 LaTeX 片段          | Leey21 |
| [中文润色（Word）](references/polish-zh-word.md)      | 只修中文论文段落的语病、口语与逻辑断层，通顺的句子原样保留 | 中文论文段落             | Leey21 |
| [去 AI 味（LaTeX 英文）](references/deai-en-latex.md) | 替换英文段落里的 AI 高频词与机械连接词，附 AI 高频词表     | 英文 LaTeX 片段          | Leey21 |
| [去 AI 味（Word 中文）](references/deai-zh-word.md)   | 去掉中文段落里的渲染性词汇、翻译腔与机械罗列               | 中文学术文本             | Leey21 |

### 检查与审稿

| Reference                                                       | 用途                                                                               | 输入                | 作者        |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------- | ----------- |
| [逻辑检查（LaTeX）](references/logic-check-en-latex.md)         | 终稿前检查前后矛盾、术语不一致与严重语病，只报必须改的问题                         | 英文 LaTeX 片段     | Leey21      |
| [审稿人视角整体审视](references/reviewer-assessment.md)         | 按投稿目标给整篇论文写审稿报告（Summary、Strengths、Weaknesses、Rating）与改稿建议 | 论文 PDF 与投稿目标 | Leey21      |
| [严苛审稿人（两轮批判评审）](references/reviewer-gatekeeper.md) | 用尖锐的语气分两轮审论文或研究计划：先列致命缺陷，再逐条追问并给出重建方向         | 完整论文或研究计划  | Pioneer-wxh |

### 图表

| Reference                                         | 用途                                                                         | 输入                   | 作者   |
| ------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------- | ------ |
| [论文架构图](references/architecture-figure.md)   | 让图像模型按方法描述生成扁平矢量风格的方法框架图，含中文与英文两版 prompt    | 摘要与方法部分描述     | Leey21 |
| [实验绘图推荐](references/plot-recommendation.md) | 按实验数据与要强调的结论推荐 1 到 2 种学术图表，并给出坐标轴、尺度与配色设计 | 实验数据表格与核心结论 | Leey21 |
| [图标题](references/figure-caption.md)            | 把中文描述写成英文 figure caption                                            | 图的中文描述           | Leey21 |
| [表标题](references/table-caption.md)             | 把中文描述写成英文 table caption                                             | 表的中文描述           | Leey21 |
| [实验分析](references/experiment-analysis.md)     | 把实验数据写成以 \paragraph{} 结论开头的 LaTeX 分析段落                      | 实验数据或结果文本     | Leey21 |

### 工具与模型

| Reference                                                 | 用途                                                                                                                    | 输入 | 作者           |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---- | -------------- |
| [写作模型选择](references/model-selection.md)             | 上游按 arena.ai Creative Writing 榜单给出的写作与润色模型推荐                                                           | 无   | Leey21         |
| [论文写作相关的 Agent Skills](references/agent-skills.md) | 上游整理的第三方写作 Skills（20-ml-paper-writing、humanizer、docx、doc-coauthoring、canvas-design）、安装方法与使用场景 | 无   | MySunX、Leey21 |

## 出处

- 除 `reviewer-gatekeeper.md` 外的 reference 整理自 [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) 的 README，固定在提交 [`df0af72`](https://github.com/Leey21/awesome-ai-research-writing/tree/df0af726a79109b8760c1b80d5dfc36ed44a6f1f)。作者 Leey21、MySunX，各文件的 `source_lines` 指向原文行号。
- `reviewer-gatekeeper.md` 整理自 [Leey21/awesome-ai-research-writing#40](https://github.com/Leey21/awesome-ai-research-writing/issues/40)，作者 [Pioneer-wxh](https://github.com/Pioneer-wxh)。
- 上游仓库没有声明许可证，prompt 文本的版权归原作者。
- 整理：[Alice39s/agent-stash](https://github.com/Alice39s/agent-stash) 把上游内容按任务拆成独立的 reference，补充用途、输入与出处字段，并编写本索引。
