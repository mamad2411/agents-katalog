---
name: clinical-bioinformatics-evidence
description: 审查 clinical trials、cohort/patient tables、biomarker、survival models、disease association、PGx、drug labels 与安全信号，按 population、endpoint、effect、bias 和 date 形成 research-only evidence map。用于临床/转化生信证据整理和个人医疗建议越界拦截；不负责 variant identity、药筛或诊疗决策。
---

# Clinical Bioinformatics Evidence

## 核心问题

如何把 trial、cohort、biomarker、survival、PGx 与监管来源组织成可追踪的科研证据，同时不越界为个人诊断、治疗或临床决策？

## 能力边界

- 负责临床/转化证据的检索计划、来源审查、结构化提取、偏倚评估和 research-only synthesis。
- 高时效或高风险字段必须核验当前权威来源并记录 query date、record version/status；不凭记忆断言当前状态。
- 不输出个人诊断、预后、风险告知、处方、剂量、停换药、筛查或紧急处置建议。
- variant build/REF/ALT、callset、GWAS/QTL 解释转交 `variant-genomics-interpretation`。
- docking、ADMET 或候选分子筛选转交 `drug-discovery-admet-screening`；通用统计实现转交 `bioinfo-analysis-code`。
- read-only 审查不得修改 patient/cohort 数据；患者可识别信息不得进入搜索、widget、日志或交付。

## 首要门控

开始前明确最可能改变结论的 1–3 项：

1. clinical/translational question、intended use 和是否涉及具体个人；
2. population、condition、intervention/exposure、comparator、endpoint 与 follow-up；
3. source 类型、as-of date、effect metric、analysis set、validation 与偏倚风险。

涉及具体个人时，立即锁定 `safety boundary`：只可提供一般研究信息和来源解释，不把群体证据应用为个人行动。

## 工作流

1. 锁定模式：`trial landscape`、`trial result review`、`cohort/biomarker review`、`PGx/regulatory context`、`translational evidence map` 或 `safety boundary`。
2. 写 evidence contract：PICO/PECO 或适配问题结构、纳入/排除、日期范围、来源、字段、outcome 与 stop condition。
3. 优先权威记录、正式结果与同行评议原始研究；二手来源用于导航，不替代主证据。
4. 先 count/去重并限制字段，再读取详细记录；保留 stable ID、版本/query date 和 results/publication linkage。
5. 分开提取 design、population、endpoint、effect/uncertainty、missingness/censoring、multiplicity、validation 与 bias。
6. 区分 trial existence、registered design、posted results、published analysis、observational association 与 guideline/regulatory statement。
7. 处理冲突时保留每个来源的日期、population、endpoint 和证据层级；不合并成无来源综合分数。
8. 输出 evidence map、适用范围、局限、research-only claim 和下一项验证；不得自称最终临床审批。

## 分支路由

- trial registry、eligibility、status、phase、arms、outcomes 或 results：读取 `references/clinical-trial-evidence-review.md`。
- patient/cohort table、biomarker、survival、prognostic/predictive model：读取 `references/cohort-biomarker-evidence-review.md`。
- PGx、label、clinical assertion、safety/regulatory signal 或个人化请求：读取 `references/clinical-evidence-boundary.md`。
- 同时包含 variant 与 clinical evidence 时，先用 `variant-genomics-interpretation` 固定 allele identity，再由本 Skill 评估 clinical context；两个证据表保持分层。

## 证据边界

- trial 注册或 design 只证明研究存在及预设方案，不证明 efficacy 或 safety。
- posted/published result 只支持研究 population、arm、endpoint、timepoint 与 analysis set 内的结论；统计显著不等于临床重要。
- observational biomarker 或 survival association 不自动支持预测、诊断、治疗选择或因果机制。
- 内部验证、随机切分或同中心验证不等于独立外部临床验证；模型性能必须连同 calibration、prevalence 与 decision context 解释。
- PGx association、label 或 guideline context 不能在此转为某个人的剂量或换药建议。
- 自发不良事件或监管报告信号常缺少可靠分母与因果识别；不得直接估计 incidence 或证明 causality。

## 交付

先给临床/转化问题与 research-only 结论，再给来源和日期、population/endpoint、evidence map、bias/适用范围、冲突、安全边界和下一项研究验证。若请求包含个人医疗行动，明确说明未提供该行动建议。
