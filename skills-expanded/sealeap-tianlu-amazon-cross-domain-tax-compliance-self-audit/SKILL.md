---
name: sealeap-tianlu-amazon-cross-domain-tax-compliance-self-audit
description: "Audit a cross-border seller's tax-compliance exposure across platform data-reporting reconciliation, taxpayer classification, cost-voucher completeness, multi-store/entity reporting consistency, and offshore-entity exposure, producing a risk checklist for professional review. Does not calculate tax owed or issue a compliance conclusion. Use for 平台数据报送后自查、多店铺主体一致性排查、成本票缺口整理、境外主体合规暴露评估. Do not use to file taxes directly or to replace a qualified tax advisor's determination."
---

# Amazon 多维度税务合规自查

## 目标

Audit a cross-border seller's tax-compliance exposure across platform data-reporting reconciliation, taxpayer classification, cost-voucher completeness, multi-store/entity reporting consistency, and offshore-entity exposure, producing a risk checklist for professional review. Does not calculate tax owed or issue a compliance conclusion.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 文中出现的具体偏差比例、纳税人门槛金额、开票税点与主体数量等数字均为该报道时点信息，随政策与地区执行口径变化，操作前必须以官方最新规定核实，不作为固定规律套用。
- 多主体申报一致性、跨境投资备案与信息交换暴露属于税务与跨境合规的专业判断领域，本自查仅用于排查风险点，任何整改或申报决策需由具备资质的税务师/律师确认，不构成税务结论。
- 无票凭证的替代方案是否被认可因主管税务机关执行尺度而异，不能假定某种替代方式必然有效。

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

1. 核对本账户/店铺近期向平台申报或被平台报送的销售数据，与实际经营记录（银行流水、结算报表）之间的口径与差异幅度，任何显著偏离都先查明原因而非直接调整申报数字。
2. 核实当前适用的纳税人身份认定标准（是否达到一般纳税人门槛等）以官方最新口径为准，不沿用历史或经验性门槛数字。
3. 盘点成本凭证链条的完整性（发票、报关单、物流单、平台扣费明细、采购沟通记录等），对无法取得正式发票的采购环节，梳理当前可行的补充凭证方式并与税务顾问确认是否被认可。
4. 逐一核对名下全部店铺/主体的申报口径是否一致，标记任何“部分主体正常申报、部分主体长期低报或零申报”的结构性不一致，作为优先处理的风险项。
5. 如涉及境外主体（境外直接投资架构或香港等地公司），核实是否需完成境外投资备案、关联交易是否具备独立商业目的与公允定价支持，以及该境外主体在信息交换机制下的申报义务现状，评估长期零申报但有实际经营的风险敞口。
6. 将以上各项标记为已核实/待核实/不适用，形成可随政策更新复查的自查台账，不确定项升级给专业税务或法律顾问处理，不自行下合规结论。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 多店铺/主体申报口径核对表
- 成本凭证缺口清单
- 跨境主体合规风险清单
- 待税务顾问确认事项清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
