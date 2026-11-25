---
name: questionnaire-analysis
description: >-
  全流程问卷/量表数据分析方法学助手（中英文通用 / bilingual）。当用户需要分析问卷、量表或调查数据的任何环节时使用：量表与问卷设计、Likert 计分、数据清洗与缺失值/异常值处理、反向计分、描述性统计与正态性、共同方法偏差(Harman/CLF)、信度(Cronbach's α / CR 组合信度)、效度(内容/结构效度、EFA 探索性因子分析、CFA 验证性因子分析、收敛/区分效度 AVE)、差异检验(t检验、ANOVA、卡方、非参数)、相关与回归(含多重共线性 VIF)、结构方程模型 SEM、中介与调节效应(Bootstrap / PROCESS)、效应量、APA 表格与结果写作。工具中立，实操以 SPSS / AMOS 为主并在关键处给出 R(psych/lavaan/PROCESS) 做法。触发词包括"问卷分析""量表""信度效度""Cronbach""因子分析""EFA/CFA""SPSS""AMOS""结构方程""SEM""中介效应""调节效应""回归分析""方差分析""Likert""问卷数据"等。
license: MIT
---

# 问卷数据分析全流程助手（Questionnaire / Survey Data Analysis）

覆盖问卷与量表数据分析从**设计**到**成文**全链路的方法学助手。**中英文通用**：术语全程中英对照，结果句提供中英两版（投英文期刊可直接用）。工具中立——核心方法适用于 SPSS、AMOS、Mplus、R、Python、JASP、jamovi；实操示例以 **SPSS / AMOS 为主**，关键处附 **R（psych / lavaan / PROCESS）** 做法。

## 这个 skill 能做什么 / What it does

| 阶段 Stage | 你可以让我做的事 |
| --- | --- |
| 1. 问卷设计 Design | 量表选型、Likert 计分、变量类型判定、构念操作化、抽样与样本量估算 |
| 2. 数据清洗 Cleaning | 缺失值诊断与处理、异常值、反向题计分、维度合成 |
| 3. 描述统计 Descriptives | 集中/离散趋势、正态性(偏度峰度)、共同方法偏差检验 |
| 4. 信度与效度 Reliability & Validity | Cronbach's α、组合信度 CR、内容/结构效度、EFA、CFA、AVE 收敛/区分效度 |
| 5. 差异检验 Difference | t 检验、单因素/多因素 ANOVA、卡方、非参数检验、效应量 |
| 6. 相关与回归 Correlation & Regression | 相关分析、多元/层次/逻辑回归、多重共线性、假设检验 |
| 7. SEM 与中介调节 SEM & Mediation | 验证性因子分析、结构方程模型、中介/调节/有调节的中介(Bootstrap, PROCESS) |
| 8. 报告写作 Reporting | APA 7 表格、结果句模板(中英)、p 值与效应量规范报告 |

## 使用方式（重要：先读对应 reference）

每个阶段都有详细方法学子文档。**进入某阶段时先 Read 对应文件再动手**——里面有具体的判定阈值、SPSS/AMOS 操作路径、R 代码与中英 APA 结果句，不要凭记忆作答。

- `references/01-questionnaire-design.md` — 量表/问卷设计、Likert、变量类型、样本量
- `references/02-data-cleaning.md` — 缺失值、异常值、反向计分、数据准备
- `references/03-descriptive-statistics.md` — 描述统计、正态性、共同方法偏差
- `references/04-reliability-validity.md` — α / CR / AVE、EFA、CFA、内容/结构/收敛/区分效度
- `references/05-difference-tests.md` — t 检验、ANOVA、卡方、非参数、效应量
- `references/06-correlation-regression.md` — 相关、多元/层次/逻辑回归、共线性
- `references/07-sem-mediation.md` — SEM、CFA、中介/调节、Bootstrap、PROCESS、拟合指数
- `references/08-reporting-apa.md` — APA 表格、结果写作、p/效应量、常见审稿点

流程图与可视化：

- `diagrams/analysis-flow.md` — 总分析流程、方法决策树、EFA/CFA 判定、中介调节流程（Mermaid，GitHub 直接渲染）
- `diagrams/index.html` — 离线渲染页，双击查看全部流程图并截图（论文/科普用）

当用户要"分析流程图""该用什么检验""可视化分析步骤"时，先 Read `diagrams/analysis-flow.md`。

模板与工具：

- `templates/` — APA 结果句（中英对照）、分析流程自检表
- `tools/stats-cheatsheet/index.html` — 离线「统计阈值与拟合指数速查表」，双击即用（α/KMO/AVE/CR/SEM 拟合标准/效应量）

## 核心工作原则（贯穿所有阶段）

1. **方法服从测量层次与设计**。先确认变量是定类/定序/定距，再选检验；别对定序数据硬套需要正态的参数法而不检查前提。
2. **先信效度，后假设检验**。量表未通过信效度，后续回归/SEM 结论不可信。
3. **报告效应量，不止 p 值**。APA 7 与多数期刊要求 p 值 + 效应量（Cohen's d、η²、r、R²、f²）+ 置信区间。
4. **检查前提假设**。t/ANOVA 看正态与方差齐性、回归看共线性/残差、SEM 看样本量与拟合——前提不满足要说明或改用稳健/非参方法。
5. **中介调节用 Bootstrap**。中介效应优先报 Bootstrap 偏差校正置信区间（不含 0 才显著），而非过时的 Sobel/逐步法单独使用。
6. **共同方法偏差要处理**。自评横断面问卷需做并报告 CMB 检验（Harman 单因素 / 控制未测潜因子法）。
7. **如实报告**。前提违反、样本不足、拟合欠佳要写明，不藏不饰。

## 典型触发场景与首步动作

- "帮我分析这份问卷数据" → 先问研究假设/变量/题项 → 按"清洗→描述→信效度→假设检验"链路推进
- "算一下信度效度 / Cronbach / 因子分析" → 读 `04`，区分 EFA(探索)还是 CFA(验证)
- "做中介/调节效应" → 读 `07`，用 Bootstrap/PROCESS，先确认前因-中介-结果与测量信效度
- "跑结构方程 / AMOS 拟合不好" → 读 `07` 拟合指数与修正部分
- "回归该怎么报 / 表格怎么做" → 读 `06`+`08`，给 APA 表与中英结果句
- "审稿人说有共同方法偏差" → 读 `03` CMB 部分

## 语言 / Language

默认用简体中文交流与解释；**结果句、表格、术语同时给英文版**，便于中英文论文与中英文期刊投稿。用户要求纯英文时可全程英文产出。
