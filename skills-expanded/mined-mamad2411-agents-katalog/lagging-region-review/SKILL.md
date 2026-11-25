---
name: lagging-region-review
description: Audit and evaluate performance commitment materials for underperforming warzones/regions. Use when the user needs to (1) audit a业绩承诺材料 for a lagging warzone, (2) evaluate whether a warzone's performance commitment is measurable and actionable, (3) check material completeness against required sections, or (4) assess data quality and logical consistency. Triggered by mentions of 落后战区, 业绩承诺会, 战区述职, 区域业绩审核, or warzone-level performance commitment reviews.
---

# 落后战区业绩承诺会 — 材料审核 SKILL

> **Scene**: `lagging-region-review`
> **Short Name**: 落后战区业绩承诺会
> **Trigger**: 审核战区级别业绩落后人员的业绩承诺材料
> **Methodology Reference**: 借鉴华为"一报一会"经营分析会方法论

## Workflow

Execute this workflow sequentially when auditing a warzone performance commitment material.

---

### Step 1: Material Intake

1. Accept the KMS link to the warzone commitment material
2. Identify whether this is a **first-time commitment** or a **follow-up** (previous commitment not met)
3. If follow-up: check whether the material starts with **"上月决议执行复盘"** (华为经营分析会铁律：先复盘上月，再谈本月)
4. Parse the document for: performance targets, gap analysis, root causes, action plans, required sections, supporting data

---

### Step 2: 目标承诺 Check (20 points)

**Core Question**: Has the warzone made clear, measurable, and evidence-based performance commitments?

**Huawei Principle**: 华为经营分析会要求——承诺目标必须有"三层目标"（保底/目标/挑战），且必须基于"差距分析"。

#### 2.1 Required Commitment Elements

| # | Element | Full Marks | Deduction | Bad Example | Good Example |
|---|---------|-----------|-----------|-------------|--------------|
| 1 | **当月业绩承诺目标** | 4 | -4 if missing or qualitative | "努力提升业绩" | "6月承诺：签约500万（保底400/目标500/挑战600），回款400万" |
| 2 | **累计业绩承诺目标** | 3 | -3 if missing | Only monthly target, no cumulative | "H1累计签约2800万（vs年度目标6000万，缺口3200万），确保达成年度目标的47%" |
| 3 | **同比数据及目标** | 2 | -2 if missing or no baseline | "同比增长" without stating last year's number | "同比2024年6月（签约380万），承诺增长31.6%至500万，基数说明：去年6月受客户预算延迟影响基数偏低" |
| 4 | **业绩缺口分析** | 4 | -4 if only lists data without attribution | "缺口120万" without explanation | "缺口120万 = 大客户A延迟签约(60万，根因：客户内部审批流程延长) + 新项目B招标失败(40万，根因：报价高于竞品15%) + 人员流失导致覆盖不足(20万，根因：2名销售离职，新人未到位)" |
| 5 | **可量化、可衡量、有依据** | 4 | -4 if vague or no evidence | "争取突破历史最好水平" | "基于现有商机池450万（A客户200万+B客户150万+C客户100万），按历史转化率30%测算，承诺500万有数据支撑" |
| 6 | **经营质量指标** | 3 | -3 if only revenue | 只承诺收入，没有利润/现金流/回款 | "收入500万 + 毛利率≥25% + 回款率≥80% + 现金流为正" |

#### 2.2 经营质量要求（Huawei "大质量观"）

华为经营分析会不仅看收入，更看**经营质量**。目标承诺必须包含：

| 指标类型 | 最低要求 | 说明 |
|----------|---------|------|
| **收入/签约** | 必须有 | 最基本的业绩指标 |
| **利润/毛利率** | 建议有 | 避免"增收不增利" |
| **回款/现金流** | 必须有 | 华为最看重的指标之一 |
| **客户满意度** | 建议有 | NPS或等效指标 |

**🔴 Fatal Line**: Zero performance commitment (this dimension = 0 points) → **R5 退回重写**

---

### Step 3: 行动具体化 Check (30 points)

**Core Question**: Does every action item meet SMART criteria with clear ownership and deadlines? **More importantly: does each action correspond to a TRUE ROOT CAUSE?**

**Huawei Principle**: 华为要求行动必须对应"真因"——做了这个动作，问题就不再发生；做了这个动作，目标就一定能实现；是我能做的、尽我能力能做的。

#### 3.1 Root Cause Quality (华为根因三标准)

Before evaluating actions, first evaluate whether the material has found **true root causes**:

| Standard | Test Question | Deduction if Failed |
|----------|--------------|---------------------|
| **标准1：做了就不再有** | 做了这个动作，问题还会发生吗？ | -5 if action addresses symptom not root cause |
| **标准2：做了就必达** | 做了这个动作，目标就一定能实现吗？ | -5 if action insufficient to achieve target |
| **标准3：是我能做的** | 这个动作是我能控制的、尽我能力能做的吗？ | -5 if action depends on external factors only |

**Example of Bad Root Cause + Action:**
- "根因：市场竞争激烈" → "行动：加大市场投入" (❌ 不是真因，是市场常态)
- **真因应该是**："根因：我们对TOP3竞品的价格策略缺乏动态监控机制" → "行动：建立周报机制，每周跟踪竞品价格，由销售运营中心负责，每周五输出报告" (✅ 符合三标准)

#### 3.2 SMART Criteria (each action item)

| Criterion | Full Marks | Deduction | Bad Example | Good Example |
|-----------|-----------|-----------|-------------|--------------|
| **S**pecific — 明确责任人 | 6 | -6 if no owner | "团队加强客户拜访" | "责任人：张三（战区总监），负责TOP10客户逐一拜访" |
| **T**ime-bound — 明确时间节点 | 6 | -6 if vague deadline | "月底前完成" | "6月15日前完成A客户签约，6月20日前完成B客户投标" |
| **S**pecific — 行动描述具体 | 3 | -3 if vague | "加强管理" / "提升能力" | "每周新增50条有效商机线索，通过线上+线下双渠道" |
| **M**easurable — 可衡量的产出 | 3 | -3 if no metrics | "提高客户满意度" | "客户拜访覆盖率从60%提升至90%，NPS从30提升至40" |
| **R**elevant — 与业绩目标关联 | 3 | -3 if off-target | 行动与业绩承诺无直接关系 | "开拓2个新获客渠道 → 预计新增商机300万 → 支撑500万承诺" |
| **A**chievable — 切实可行 | 3 | -3 if unrealistic | "下个月业绩翻5倍" | "基于当前商机转化率15%，需新增2000万商机池 → 需增加2名销售" |
| **根因对应** | 3 | -3 if not linked to root cause | 行动与材料中的根因无关 | 根因"客户分层不到位"→行动"Q1完成全量客户分层，由客户成功部负责" |
| **记分牌跟踪** | 3 | -3 if no tracking mechanism | 没有说明怎么跟踪进展 | "每周五战区例会review进度，由运营部输出记分牌dashboard" |

#### 3.3 Action-to-Target Mapping Matrix

Required: Each performance commitment must have ≥1 corresponding action item.

```
┌─────────────────┬────────────────────────────┬────────────┬──────────┬─────────────┐
│ 业绩承诺        │ 对应行动项                  │ 责任人     │ 时间节点 │ 记分牌指标  │
├─────────────────┼────────────────────────────┼────────────┼──────────┼─────────────┤
│ 签约500万       │ ①A客户签约200万 ②B客户... │ 张三/李四  │ 6月15日  │ 每周review  │
│ 回款400万       │ ①催收C客户欠款150万 ...    │ 王五       │ 6月20日  │ 每周review  │
└─────────────────┴────────────────────────────┴────────────┴──────────┴─────────────┘
```

**Audit Rules:**
- Each commitment target must have ≥1 corresponding action: -5 points/target if missing
- Action item without clear owner: -4 points/item
- Action item with vague deadline ("月底前" instead of specific date): -4 points/item
- Action not linked to root cause: -3 points/item
- Action without tracking mechanism (记分牌): -3 points/item

**🔴 Fatal Line**: Action concretization < 10 points (zero owners or zero deadlines) → **R5 退回重写**

---

### Step 4: 材料规范度 Check (35 points)

**Core Question**: Does the material follow Huawei's "一报一会" structure? Are all required sections present and insightful?

**Huawei "一报一会" Structure**: 差距→根因→改善→下一场怎么打

#### 4.1 Required Sections (华为经营分析会标准结构)

| # | Required Section | Full Marks | Deduction | Content Requirements | Huawei Principle |
|---|-----------------|-----------|-----------|---------------------|-----------------|
| 1 | **上月决议执行复盘** | 7 | -7 if missing (conditional) | 上月任务令完成情况：承诺→实际→差距→原因→纠正 | 铁律：先复盘上月，再谈本月 |
| 2 | **经营仪表盘** | 7 | -7 if missing | 关键经营指标全貌：收入/利润/回款/客户/人效 | 一页纸看清经营全貌 |
| 3 | **差距分析** | 7 | -7 if missing | 目标vs实际vs基准，按维度拆解 | 差距导向，不绕弯子 |
| 4 | **根因分析** | 7 | -7 if missing | 用5Why或鱼骨图，找到真因 | 归因于内，主观原因≥40% |
| 5 | **改善行动（任务令）** | 7 | -7 if missing | 差距→根因→行动→责任人→时间→记分牌 | 一一对应，闭环管理 |

#### 4.2 Section Quality Standards

**上月决议执行复盘** (7 points, conditional):
- **Trigger**: If previous commitment was made
- **Must include**: ①上月承诺 ②实际结果 ③差距分析 ④未达成原因（根因） ⑤纠正措施
- **Huawei Rule**: 如果上月承诺未达成，必须首先复盘——这是华为经营分析会的铁律
- **记分牌要求**: 每个上月任务令必须有完成状态（✅完成/⚠️进行中/❌未完成）
- Bad: "上月承诺签约500万，实际完成480万，基本达成" (没有根因分析)
- Good: "上月承诺签约500万，实际完成480万，缺口20万。根因：A客户内部审批延迟（真因：未提前与客户CFO对齐审批流程）。纠正：本月提前2周与客户CFO确认审批节点，责任人张三，6月5日前完成" (符合三标准)

**经营仪表盘** (7 points):
- Must be **one-page overview** of key business metrics
- Must include at least 4 of:
  - 收入/签约金额
  - 利润/毛利率
  - 回款/现金流
  - 客户数/客户满意度
  - 人效（人均产出）
  - 商机池金额
- Must show: target vs actual vs gap for each metric
- Must be visual (tables/charts preferred)
- Bad: 10 pages of scattered data with no summary
- Good: One-page dashboard with 6 KPIs, each showing target/actual/gap/YoY trend

**差距分析** (7 points):
- Must decompose total gap by dimension (customer/region/product/time)
- Must quantify each sub-gap
- Must identify the biggest gap (Pareto: 20% causes → 80% gap)
- Bad: "总缺口120万" (没有拆解)
- Good: "总缺口120万 = 大客户A(60万, 50%) + 新项目B(40万, 33%) + 人员流失(20万, 17%)。最大缺口来源：大客户A延迟签约，占50%"

**根因分析** (7 points):
- Must use at least one structured analysis tool: 5Why / Fishbone / Funnel
- Must distinguish between **symptom** and **root cause**
- **Huawei Root Cause Test**: 连续问三个"为什么"，直到找到真因
- Must have ≥40% internal/self-attribution (归因于内)
- Bad: "根因：市场竞争激烈" (不是真因，是外部环境)
- Good: "为什么签约延迟？→客户内部审批延长。为什么延长？→我们没有提前与客户CFO对齐审批流程。为什么没有对齐？→缺乏客户关键决策人mapping机制。真因：缺乏系统化的客户决策链管理机制" (符合三标准)

**改善行动（任务令）** (7 points):
- Must be structured as **任务令** (Task Order): 差距→根因→行动→责任人→时间→验收标准→记分牌
- Each action must correspond to a root cause (一一对应)
- Must include tracking mechanism (记分牌)
- Bad: "加强客户管理" (没有对应根因，没有责任人，没有时间)
- Good: "任务令1：建立客户决策链mapping机制。对应根因：缺乏系统化的客户决策链管理。行动：①梳理TOP20客户决策链 ②建立CFO/采购负责人沟通机制 ③每周review进展。责任人：张三。时间：6月30日完成。验收标准：TOP20客户100%完成决策链mapping。记分牌：每周五战区例会review" (完整任务令)

#### 4.3 Differentiation Check

- 建议 across sections must NOT be雷同 or repetitive
- Each section should have unique, non-overlapping focus

---

### Step 5: 数据质量 Check (15 points)

**Core Question**: Is the data accurate, logically consistent, and free of obvious errors?

**Huawei Principle**: 经营数据必须经得起追问——"这个数据从哪里来的？口径是什么？"

#### 5.1 Data Accuracy Checks

| # | Check Item | Full Marks | Deduction | Example Error | Huawei Principle |
|---|-----------|-----------|-----------|---------------|-----------------|
| 1 | **同比/环比计算正确** | 3 | -3 if wrong | "同比增长20%" but actual is (500-400)/400 = 25% | 口径一致，基数明确 |
| 2 | **百分比总和校验** | 2 | -2 if ≠100% | "A占比30% + B占比40% + C占比35% = 105%" | 逻辑自洽 |
| 3 | **关键指标计算正确** | 3 | -3 if wrong | "利润率 = 利润/收入" but calculates as "利润/成本" | 公式准确 |
| 4 | **正文与表格数据一致** | 3 | -3 if mismatch | Text says "签约500万" but table shows "480万" | 前后一致 |
| 5 | **数量级合理** | 2 | -2 if absurd | "客户数1200.5个" or "营收50万元" for a billion-dollar company | 常识校验 |
| 6 | **经营指标逻辑关系** | 2 | -2 if inconsistent | 收入增长20%但利润下降50%，没有解释 | 指标之间逻辑自洽 |

#### 5.2 Data Quality Rules

- Does NOT verify data source authenticity (trusted input)
- Focuses on: calculation errors, logical contradictions, formatting issues
- One error per category: deduct full marks for that category
- Multiple errors in same category: still deduct once (don't double-count)
- **Huawei Special**: 经营指标之间必须有逻辑关系（如收入增长但利润下降，必须有解释）

**🔴 Fatal Line**: Data quality < 5 points (major errors causing decision误导) → **R5 退回重写**

---

### Step 6: Generate Audit Report

**Report Structure:**

```
[AI] XX战区业绩承诺材料审核报告
战区：XXX  汇报人：XXX  考核周期：XXX

总分：XX/100  等级：[R1/R2/R3/R4/R5]

一、评分总览
| 维度 | 权重 | 得分 | 判定 |
|------|------|------|------|
| 目标承诺 | 20% | XX | ... |
| 行动具体化 | 30% | XX | ... |
| 材料规范度 | 35% | XX | ... |
| 数据质量 | 15% | XX | ... |

二、R级判定
R1(90-100) 达标上会 | R2(80-89) 微调上会 | R3(70-79) 修改重审
R4(60-69) 大幅修改重审 | R5(0-59) 退回重写

三、华为经营分析会规范检查
□ 上月决议执行复盘 (如适用)
□ 经营仪表盘 (一页纸全貌)
□ 差距分析 (按维度拆解)
□ 根因分析 (真因三标准)
□ 改善行动任务令 (一一对应)

四、详细审核（每维度：得分+打分理由+问题清单）
五、红线检查 / 一票否决检查
六、审核结论（总分+定性+最大硬伤+上会风险+追问预判）
七、修改清单（按R5→R4→R3→R2→R1优先级）
```

**R级判定标准:**
- **R1 (90-100)**: 材料达标，可直接上会
- **R2 (80-89)**: 基本达标，微调后上会
- **R3 (70-79)**: 明显不足，修改后需重新评审
- **R4 (60-69)**: 较多问题，大幅修改后重新评审
- **R5 (0-59)**: 严重不达标，退回重写

---

## Issue Classification & Improvement Suggestions

### 🔴 R5 级别（一票否决，必须退回重写）

| # | Problem Diagnosis | Improvement Suggestion |
|---|-------------------|------------------------|
| 1 | **零业绩承诺** — 材料没有明确的业绩承诺目标 | 在材料开头明确写出：当月承诺目标（保底/目标/挑战三层）、累计承诺、同比基准。目标必须定量、可衡量、有数据支撑。同时包含经营质量指标（利润/回款/现金流） |
| 2 | **行动方案完全无责任人** — 所有行动项都没有指定负责人 | 为每个行动项指定具体责任人（姓名+职位），避免"团队负责""相关部门" |
| 3 | **行动方案完全无时间节点** — 所有行动项都没有具体日期 | 为每个行动项设定具体完成日期（如"6月15日"），拒绝"月底前""尽快" |
| 4 | **数据存在重大错误** — 计算错误导致决策误导 | 重新核算所有数据，特别是：同比/环比公式、百分比加总、关键指标定义、正文与表格一致性 |
| 5 | **行动与根因不对应** — 所有行动都没有对应到材料中的根因 | 建立「根因-行动一一对应矩阵」，确保每个根因都有对应的改善行动 |

### 🟡 R4→R3 级别（严重问题，大幅修改）

| # | Problem Diagnosis | Improvement Suggestion |
|---|-------------------|------------------------|
| 6 | **缺少上月决议复盘** — 上月做了承诺但没达成，本月材料没有复盘 | 增加「上月决议执行复盘」章节：上月承诺→实际结果→差距→根因→纠正措施。这是华为经营分析会的铁律 |
| 7 | **缺少经营仪表盘** — 没有一页纸经营全貌 | 增加一页经营仪表盘，包含：收入/利润/回款/客户/人效等关键指标，每个指标显示目标/实际/差距/同比趋势 |
| 8 | **差距分析只有总数没有拆解** — "缺口120万"没有按维度拆解 | 按客户/区域/产品/时间维度拆解差距，找出最大缺口来源（Pareto分析） |
| 9 | **根因分析全是外部因素** — "市场不好""竞争激烈"，没有找到真因 | 用5Why连续追问三个"为什么"，直到找到真因。确保主观/内部原因≥40%。对照华为根因三标准检验 |
| 10 | **建议雷同、缺乏差异化** — 各章节建议内容重复 | 每章聚焦不同维度：差距分析→根因→财务建议→销售运营建议→项目运营建议→改善行动 |
| 11 | **行动不对应根因** — 行动与材料中的根因无关 | 建立「根因-行动一一对应矩阵」，确保每个行动都对应一个真因 |
| 12 | **缺少记分牌跟踪机制** — 行动没有说明怎么跟踪进展 | 为每个任务令增加记分牌机制：每周/每月review的频率、责任人、输出物 |

### 🟢 R3→R2 级别（一般问题，修改后提升）

| # | Problem Diagnosis | Improvement Suggestion |
|---|-------------------|------------------------|
| 13 | **同比基数未说明** — 写了同比增长但没有说明去年同期的具体数字 | 补充去年同期数据作为基数，并说明计算口径和影响因素 |
| 14 | **承诺目标缺乏数据支撑** — 目标数字没有基于商机/历史/市场分析 | 在目标后附数据支撑：商机池清单、历史达成率、市场容量分析 |
| 15 | **经营指标逻辑矛盾** — 收入增长但利润下降，没有解释 | 分析指标之间的逻辑关系，如有异常必须解释原因 |
| 16 | **缺少可衡量的产出标准** — 行动项没有验收标准 | 为每个行动项增加验收标准："完成标志是什么？怎么判断是否达成？" |
| 17 | **数量级不合理** — 小数点错误、单位错误等低级错误 | 通读全文检查：客户数应为整数、金额单位统一、百分比≤100% |

---

## Quality Writing Standards

### 1. Score Calibration
Each score must explain: "Not full marks because... not zero because... so we take..."

### 2. Use "Zero" for Complete Absence
- Not "lacks performance commitment" → "**Zero** performance commitment (no quantitative target)"
- Not "missing responsible person" → "**Zero** accountability (no named owner for any action)"
- Not "lacks root cause analysis" → "**Zero** root cause analysis (all external blame, no 5Why)"

### 3. R-level Characterization
Be direct about the R-level: "This material is R4-level: it has a framework but lacks substance in every section."

### 4. Conclusion 5 Elements
1. One-sentence total score and R-level
2. One-sentence material characterization
3. Biggest硬伤
4. 上会 risk assessment (high/medium/low)
5. 2-3 questions the committee will most likely ask

> **Example**: "Total 58分, R5 退回重写. Material has a performance commitment (签约500万) but zero corresponding action items with owners or deadlines. The biggest硬伤: 4个action items all say '团队负责' with dates like '月底前'. No root cause analysis — just 'market is competitive'. 上会 risk: very high. If this goes to meeting, the GM will ask: ①'Who exactly is responsible for each action?' ②'What's the true root cause of the 120万gap?' ③'Where's the task order with tracking mechanism?'"

---

## Reference

- **Frontend dimension cards**: `src/pages/reviewer/main.js` → `sceneDimensionData['lagging-region-review']`
- **Checklist (21 items)**: `src/pages/reviewer/main.js` → `getLocalSceneHints('lagging-region-review')`（本地审核要点，代理不可用时使用）
- **Unified PRD**: `docs/01-Product产品/会议材料智能审核助手-统一产品设计.md` §4.2
- **Huawei "一报一会" methodology**: 月度经营分析报告 + 经营分析会，差距→根因→改善→下一场怎么打
