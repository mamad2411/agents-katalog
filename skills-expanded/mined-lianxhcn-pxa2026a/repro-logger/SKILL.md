---
name: repro-logger
description: Use this skill to turn a data-analysis run into reproducible records. Given the scripts you ran, the data you used and the outputs you got, it drafts a reproduction log (input data → processing script → output), a variable-construction note, a sample-selection log (row counts at each filter), a results explanation and an open-questions checklist; it also abstracts one analysis run into a reusable project template. Records only what the user provides; marks steps that could not run for missing data or license; never fabricates numbers, file names or results. The human checks the draft for errors and omissions.
---

# repro-logger（复现日志员）

把一次分析或复现，落成**别人照着能重跑**的记录。它不替你做研究判断，而是根据你实际跑过的脚本、用过的数据和得到的产出，起草复现日志、变量构造说明、样本筛选日志、结果说明和待检查问题清单，并能把一次流程抽象成可复用的项目模板——初稿由它写，错漏由你查。对应第 2 讲「留痕与可复现」和第 6 讲「整理复现日志、把流程整理成模板」的 AI 协作。

## 何时用

- 跑完一段清洗或复现，想把「从哪份数据、经过哪些步骤、得到哪个结果」记成一份日志；
- 样本一路筛下来行数在变，想留一张「每一步筛了什么、还剩多少」的样本筛选日志；
- 要给关键变量写一份构造说明（怎么来的、口径是什么），补进变量字典；
- 想把这次分析流程抽象成模板，下次拿到新任务照着套；
- 复现里有些步骤因为缺数据或缺许可跑不了，要如实标注、不留假账。

## 使用方式（提示词）

**生成「从数据到结果」复现日志**：

> 以下是我跑过的脚本、用到的数据和得到的产出：[粘贴]。请整理成一份复现日志，按步骤记录「输入数据 → 处理脚本 → 产出（中间数据 / 图 / 表）」，并标出哪些步骤因为缺数据或缺许可没跑成。只依据我提供的信息，不要补全我没给的内容。

**生成样本筛选日志**：

> 这是我的样本筛选步骤和每步后的样本量：[粘贴，如「剔除缺失 126→124」]。请整理成一张样本筛选日志：每一行写「筛选条件、剔除多少、剩余多少、为什么这样筛」，末尾提示样本量变化里有没有需要我再核对的异常。

**生成变量构造说明 / 结果说明**：

> 这些是我构造的变量和它们的定义：[粘贴]。请写成一份变量构造说明，每个变量写「原始来源、构造公式或规则、单位、口径注意点」；口径拿不准的地方标出来让我确认，不要编造定义。

**整理成可复用的项目模板**：

> 请把我们这次分析的完整流程，抽象成一份可复用的项目模板：包括标准的文件夹结构、每一步做什么、每步建议调用哪个 skill、每步要人工核对的要点。目标是我下次拿到新任务，照着这份模板就能走一遍。

## 输出约定

- 日志按**步骤**组织，每步「输入 → 处理 → 产出」三段齐全，缺一不补；
- 跑不了的步骤**如实标注**原因（缺数据 / 缺许可 / 未运行），绝不假装跑过；
- 样本筛选日志给出每步**剔除数与剩余数**，能对上最终分析样本；
- 只依据用户提供的脚本、数据与产出，**不编造行数、文件名、变量口径或结果**；拿不准的显式标出。

## 最小使用示例

> 用 repro-logger 帮我把这段整理成复现日志：我先 `use firm_finance_2021.dta`（84 行），`append` 2022 年那份得到 126 行，再剔除 rd 缺失的 2 行剩 124 行，最后 `reg rd_ratio size` 出了一张回归表。

## 人工检查清单

- 日志里每一步的输入输出，回到你实际跑的脚本逐条对一遍，数字（行数、匹配率）要对得上；
- 跑不了的步骤有没有被如实标注——**一份诚实的日志，比一份漂亮但注水的更有价值**；
- 变量口径、清洗理由与筛选依据要与真实数据一致，别让 AI 替你「圆」一个说法；
- **AI 辅助、不替代判断**：记录是否可信、能否复现，最终由你把关。

## 来源与许可

- 原创：本课程为「连享会 2026 暑期班·初级班」编写，Agent 无关的开放 Skill，MIT（随仓库 `LICENSE-CODE`）。
- 最后验证日期：<!-- TODO: T7 彩排 Claude Code 与 Codex 双端实测后填写 -->
