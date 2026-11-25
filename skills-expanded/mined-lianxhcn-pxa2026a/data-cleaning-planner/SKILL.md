---
name: data-cleaning-planner
description: Use this skill when planning or reviewing data cleaning for empirical research. Given a variable list and data dictionary, it drafts a cleaning plan; checks whether a merge/join is sound (1:1 vs m:1, key name/case/type/leading-zero consistency, expected match rate); explains the differences among missing-value handling, outliers, winsorizing, trimming, log transform and standardization; recommends exploratory plots given variable types; explores each table's observation unit, grain, primary key and shape (long/wide) into a review checklist; and plans text-variable extraction without hand-writing regex. Emphasizes judgment and human review; never fabricates data, codebooks, or results.
---

# data-cleaning-planner（数据清洗计划师）

在动手 `merge`、`reg` 之前，帮你把数据清洗**先想清楚、再落地**。它不替你改数据，而是根据你的变量清单和数据字典，产出可执行的清洗计划、合并逻辑核查、变换选择建议和探索性图形清单——判断权始终在你手里。对应第 2 讲「数据处理、探索性分析与样本构造」的多处 AI 协作。

## 何时用

- 拿到一份（或几份）数据，不确定该按什么顺序清洗；
- 要合并两张表，拿不准用 `1:1` 还是 `m:1`、键会不会对不上、该期望多大匹配率；
- 分不清缺失、离群、缩尾、截尾、对数、标准化各自解决什么、代价是什么；
- 不知道某个变量该画什么图来检查（分布、离群、组间、样本选择）；
- 面对来路不明的多张表，想先让 agent 探索结构、生成一张待审清单再动手；
- 遇到公司名、地址等文本变量，想描述清楚任务、交给技能，而不是自己写正则。

## 使用方式（提示词）

**生成清洗计划 / 数据字典**：

> 这是我的变量清单（表头 + 前几行）：[粘贴]。请生成：(1) 数据字典草稿（每个变量的含义、单位、口径、取值范围、异常提示）；(2) 一份分步清洗计划。凡是拿不准的口径，标出来让我确认，不要编造。

**检查 merge / join 逻辑**：

> 表 A：[粒度、主键、行数]；表 B：[粒度、主键、行数]。我打算用 [键] 做 [1:1 / m:1] 合并。请检查：合并类型对不对、两边键在名称/大小写/空格/存储类型/前导零上是否一致、预期匹配率多少、出现 master-only / using-only 各说明什么。先检查与提问，不要写最终代码。

**解释各种变换的差别**：

> 针对我的变量 [名称、含义、偏度/极值/缺失比例]，分别解释缺失、离群、缩尾、截尾、对数转换、标准化各解决什么问题、代价是什么、会如何改变回归系数含义，并建议对这个变量先做哪一步、为什么。把判断依据摆出来让我选。

**按变量类型建议探索性图形**：

> 我有这些变量 [名称、类型、含义]，研究问题是 [一句话]。请给一份 EDA 图形清单：每项写「画哪种图、对哪些变量、能查什么问题」，优先安排最可能暴露离群、缺失、分组结构、样本选择的图，并给可运行代码骨架，图例统一放图形下方。

**探索数据形态、生成待审清单**：

> 这里有若干数据表：[列出]。请逐表报告观察单位与粒度、主键候选（含唯一性检查）、数据形态（long/wide）、潜在问题（重复、异常缺失、同名键类型/大小写不一、粒度不齐），汇成一张待审清单。只报告与提问，不要修改数据。

**规划文本变量处理**（不陷入正则代码）：

> 我有一列 [文本变量示例]，想提取 [目标]。请先规划处理步骤，再给可运行代码；对拿不准的匹配规则，先列出让我确认，不要硬编造。

## 输出约定

- 清洗计划分步、每步注明「做什么、为什么、动手后查什么」；
- 合并核查必须给出**预期匹配率**和键不一致的排查点，而不是直接给合并代码；
- 变换建议要列**取舍依据**（保留样本 vs 损失样本、系数含义变化），不替用户拍板；
- 一切以用户提供的数据与字典为准，**不编造变量口径、不虚构数据**；拿不准的地方显式标出。

## 最小使用示例

> 用 data-cleaning-planner 帮我看一下：我要把一张「公司-年度」财务表和一张「行业代码-行业名」对照表合并，键是行业代码。该用哪种合并？合并后我该查什么？

## 人工检查清单

- AI 给的匹配率、样本量、口径判断，回到真实数据上用 `isid`、`duplicates`、`tab _merge` 复核；
- 离群值先查明来源（录入错误 vs 真实极端），能改的改、不要一律缩尾；
- 变量口径、清洗理由要落进变量字典与样本筛选日志（配 `06-repro-logger`）；
- **AI 辅助、不替代判断**：处理方案是否合适，取决于你的数据和研究问题，最终由你把关。

## 来源与许可

- 原创：本课程为「连享会 2026 暑期班·初级班」编写，Agent 无关的开放 Skill，MIT（随仓库 `LICENSE-CODE`）。
- 最后验证日期：<!-- TODO: T7 彩排 Claude Code 与 Codex 双端实测后填写 -->
