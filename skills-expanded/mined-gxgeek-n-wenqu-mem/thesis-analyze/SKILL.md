---
name: thesis-analyze
description: >-
  ZJU MEM学位论文数据分析入口。涵盖数据生成机制审计、数据处理（采集→清洗→统计→建模）和专业图表生成
  （Mermaid/PlantUML/Python matplotlib），输出可直接嵌入论文的代码和图表。
  【改道声明】画图/图表/可视化/出成品图/改图/重渲图类请求，一律路由到 thesis-figures
  （本项目画图统一入口）；本skill只管数据处理、统计分析与探索性草图，不产出论文成品图。
  含 t检验、ANOVA、回归、聚类、卡方、相关性、信度效度、描述性统计等具体统计方法（读 CSV→出结果）。
  触发词：数据生成机制、数据如何产生、数据分析、数据处理、数据清洗、统计分析、建模、data analysis、
  t检验、方差分析、ANOVA、回归分析、相关分析、聚类分析、卡方检验、显著性检验、
  描述性统计、信度效度、Cronbach、KMO、Cohen's d、假设检验。
allowed-tools: Read, Write, Bash
---

# ZJU MEM 学位论文数据分析

两步工作流。先处理数据，再生成图表。输出均为可执行的代码和可直接嵌入论文的图表。

## Step 1: 数据处理

- 在选择统计方法前完成数据生成机制审计，先解释业务事件如何变成分析变量、
  样本如何进入数据以及干预如何实际发生。涉及前后对比、因果措辞、企业日志
  或口径变化时，必须读取 `references/data-generating-process-audit.md`。
- 数据采集：调研问卷、企业日志、AI系统日志、质量指标等真实来源。
- 数据清洗：缺失值处理（均值/中位数/删除）、异常值检测（IQR/Z-score）、归一化（MinMax/StandardScaler）。
- 统计方法：描述统计（均值/标准差/分布）、假设检验（t检验/卡方/ANOVA）、回归分析（线性/逻辑回归）、AI模型评价指标（准确率/召回率/F1）。
- 方法选择：内部对比后推荐最适合的一种（DMAIC/PDCA/六西格玛等）。
- 输出可执行Python代码模板（numpy/pandas/statsmodels）。
- 现成骨架（data-free，读你自己的 CSV，`--demo` 看用法）：`scripts/inferential.py`（Welch t+Cohen's d / ANOVA+Tukey，**仅抽样 Likert**）、`scripts/regression.py`（OLS+VIF+标准化 β，派生值可喂 fig_coef_ci.R）、`scripts/reliability.py`（Cronbach α+KMO）。详见 `scripts/README.md`。
- 详细指南见 `references/analysis-guide.md`。

## Step 2: 专业图表生成

> **改道声明**：论文成品图（新建/修改/重渲）一律走 `thesis-figures`（本项目画图统一入口，R/ggplot2 + TikZ + 可编辑改造三路线，含 FIGURES.md 登记与验收闭环）。本节仅用于数据探索性草图。

- 支持Mermaid（架构图/流程图/时序图/甘特图）、PlantUML、Python matplotlib/seaborn。
- 严格遵循ZJU图表自明性：图题下置、表题上置、三线表、分章编号。
- 学术配色方案：避免过于鲜艳，优先灰度友好配色。
- 输出图编号+图题+可执行代码+自明性检查清单。
- 详细规范见 `references/visualization.md`。

## 输出内容

每步输出：
1. 分步操作指南
2. 可直接执行的Python/Mermaid代码
3. 图表自明性检查清单
4. 下一步技能推荐

若项目提供 `scripts/thesis_quality.py`，在统计结果或正文关键数字变化后调用
`thesis-quality-gate` 执行 `evidence refresh` 和 `evidence validate`。只登记真实
输入、脚本和输出；不得把自动分类直接标成已确认或已核验。

生成机制审计出现关键 `unsupported` 时，不得用新增模型或显著性结果掩盖数据链
缺口；先补证据，无法补齐则降低主张上限。
