---
name: sealeap-tianlu-amazon-tax-reporting-income-selfcheck
description: "Check whether the account's current seller entity type and marketplaces fall inside an active platform tax-information-reporting requirement by reading the official regulation text directly, then assemble a self-check package of revenue records and deductible-cost evidence (supplier invoices, logistics invoices, platform commission and ad-spend statements) for a qualified tax advisor to review. Produces an evidence checklist, not a tax filing conclusion or exemption determination. Use for 平台涉税信息报送适用性核对、收入与抵扣凭证归集、税务顾问对接材料准备. Do not use to determine actual tax liability, exemption eligibility, or filing amounts — those require a qualified tax advisor working from the account's real financial records."
---

# Amazon 税务报送与所得税自查

## 目标

Check whether the account's current seller entity type and marketplaces fall inside an active platform tax-information-reporting requirement by reading the official regulation text directly, then assemble a self-check package of revenue records and deductible-cost evidence (supplier invoices, logistics invoices, platform commission and ad-spend statements) for a qualified tax advisor to review. Produces an evidence checklist, not a tax filing conclusion or exemption determination.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 报送规则的具体条款、首次报送时间与覆盖范围来自单一来源总结，未逐条核实官方公告原文，实际适用以官方最新文本与主管税务机关口径为准。
- 各类小规模纳税、核定征收、园区返税等优惠政策的具体门槛、比例会因地区、主体类型与政策版本不同而有差异，来源提到的具体数字不作为可依赖的当前标准。
- 特定费用的税前扣除比例限制、抵扣凭证的具体要求应以官方最新规定与税务顾问意见为准，不据来源总结直接计算应纳税额。
- 本流程仅产出证据归集清单，不构成税务或法律结论，实际申报决策需由具备资质的税务顾问基于完整财务记录作出。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace 与案例 ASIN 的明确时间范围
- 销量、评论、价格、促销、变体和上架时间线
- 关键词自然/广告可见度、品牌与站外流量代理证据
- 可复核来源、数据口径、缺失项和替代解释

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 核对当前适用的平台涉税信息报送规定原文与官方公告，确认报送的信息范围（如身份、交易额、收入、佣金等）、首次报送节点与本账户经营主体类型是否落入报送范围。
2. 核对本账户在报送范围内的各平台店铺，梳理店铺注册主体名称、经营类型与实际报关/收汇主体是否一致，标出需要提前核实或调整的不一致项。
3. 按报送涉及的时间窗口，导出对应期间的出口收入记录，核对与报关金额、收汇金额是否可以相互印证，标出差异项待核实原因。
4. 归集可能用于抵扣的成本凭证（采购发票、物流发票、平台佣金与广告费凭证、其他经营性费用发票），按凭证类型分类整理，标出缺失或无法开票的部分。
5. 核对当前适用的费用税前扣除口径（如特定费用是否存在扣除比例限制）是否有官方最新规定，若有先记录来源出处，不直接按经验比例计算应纳税额。
6. 将收入记录、凭证清单与适用口径核对结果整体提交给具备资质的税务顾问，由其判断具体申报方式与是否存在可适用的优惠政策，不自行下税务结论。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 报送规则适用性核对记录（主体类型/店铺/生效节点）
- 收入与报关收汇一致性核对表
- 抵扣凭证归集清单（含缺失项标注）
- 待税务顾问复核的材料包
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
