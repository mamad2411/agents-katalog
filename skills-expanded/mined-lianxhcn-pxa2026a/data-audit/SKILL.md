---
name: data-audit
description: Use this skill to audit and cross-validate a data-cleaning result before trusting it, especially work produced by an AI/agent. Given the cleaning code plus before/after data, it checks the empirical red lines: is every change in sample size accounted for (a sample-selection log); is the merge match rate normal (no silent losses); were outliers blanket-winsorized instead of investigated; are variable definitions/units consistent and summary statistics in line with published papers on similar samples; and above all, were any samples dropped or thresholds picked to favor a desired result. It never modifies data; it only flags suspicious points for the researcher to review.
---

# data-audit（数据审计员）

数据清洗做完之后，在你信任它、拿去跑回归之前，用它做一次体检。它专门审查一份清洗结果有没有踩「数据处理红线」——尤其针对 agent 干的活：agent 很能干，但它优化的是「完成任务」，未必是「对研究负责」。这个 skill 拿着一张红线清单逐条核对，把可疑处列出来交你复核。它不改数据，只审、只报。对应第 2 讲末尾的「不可破除的红线」。

## 何时用

- agent（或你自己）清洗完一份数据，想在用它之前查一遍有没有出问题；
- 复现别人的数据处理，想核对样本量、匹配率、变量口径对不对得上；
- 担心清洗过程为了迎合下游结果而做了手脚（删样本、挑阈值）；
- 想给一份清洗流程配上「样本筛选日志 + 变量字典 + 一致性检查」的成品。

## 使用方式（提示词）

把清洗的 do / 代码，以及清洗前后的数据摘要（`describe`、`summarize`、样本量）交给 agent：

> 这是一份数据清洗的代码和清洗前后的数据摘要：[粘贴]。请当我的审计员，逐条核对下面这些红线，把每一条的核对结果和可疑处列出来，只报告、不要改数据:
>
> 1. **样本流失有没有账**：从原始到最终，每一步样本量怎么变的？有没有哪一步无故大增大减？
> 2. **合并匹配率**：每次 merge 的匹配率是多少？有没有大量 master-only / using-only 没被发现？
> 3. **离群处理**：离群值是先查明来源再处理，还是被无差别缩尾/删除？有没有把本可修正的录入错误也一并缩尾？
> 4. **变量口径与单位**：构造变量的定义、单位是否前后一致？关键变量的均值/标准差，和做同类样本的已发表文献相比是否离谱？
> 5. **有没有为结果做手脚**：有没有在没有正当理由的情况下删掉某些样本、或专挑能凑出显著的阈值？
>
> 对每条给出：通过 / 存疑 / 不通过，以及依据。存疑处告诉我该去核对什么。

## 红线检查清单（skill 内建）

- 原始数据是否只读、清洗是否全部写成代码（可复现）；
- 样本筛选日志是否完整、每步增减是否有理由；
- 每次合并是否记录并检查了匹配率，异常是否被发现；
- 离群是否「先查明来源、再决定」，而非无差别处理；
- 变量口径、单位是否一致，基本统计量是否与文献可比；
- 是否存在为迎合结果而做的可疑筛选或阈值选择。

## 输出约定

- 逐条给「通过 / 存疑 / 不通过」+ 依据，不含糊；
- 存疑与不通过项，指出**该去核对什么、可能的后果**，而不是直接替用户下结论或改数据；
- 发现「样本无故大变」「匹配率异常未报警」「离群被无差别缩尾」「为结果筛样本」中任何一项，一律标为需人工复核的高风险项。

## 最小使用示例

> 用 data-audit 审一下这份清洗：原始 126 行，最终 118 行，中间只写了「drop if 缺失」。请核对样本流失有没有交代清楚、这 8 行是怎么没的。

## 人工检查清单

- 审计结论只是「提示」，最终由你回到原始数据核实；
- 高风险项（尤其「为结果筛样本」）必须人工逐条查证；
- 审计发现的问题，回填到样本筛选日志与变量字典（配 `06-repro-logger`）。

## 来源与许可

- 原创：本课程为「连享会 2026 暑期班·初级班」编写，Agent 无关的开放 Skill，MIT（随仓库 `LICENSE-CODE`）。
- 最后验证日期：<!-- TODO: T7 彩排 Claude Code 与 Codex 双端实测后填写 -->
