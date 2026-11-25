---
name: sealeap-tianlu-amazon-eu-compliance-system-audit
description: "Audit the account's actual EU-marketplace footprint against the current official text for each relevant regulatory category (customs/low-value-parcel duty, VAT/OSS-IOSS registration, packaging EPR, product-safety disclosure, and platform data-reporting rules), confirming scope, effective date, and which of the account's own entities, products, and stock locations are affected before treating any rule as settled. Also runs an internal consistency check across order, payment, goods-movement, and invoice records plus entity-name matching across VAT, business, and packaging registrations. Use for 欧洲市场合规体系核对、VAT/EPR/关务法规适用性核对、多单证主体一致性审计、进入欧洲新站点前合规排查. Do not use to assert a specific tariff threshold, VAT rate, or regulation effective date as current fact without checking the official source; do not use as a substitute for a qualified customs, tax, or legal advisor's sign-off."
---

# Amazon 欧洲合规体系核对

## 目标

Audit the account's actual EU-marketplace footprint against the current official text for each relevant regulatory category (customs/low-value-parcel duty, VAT/OSS-IOSS registration, packaging EPR, product-safety disclosure, and platform data-reporting rules), confirming scope, effective date, and which of the account's own entities, products, and stock locations are affected before treating any rule as settled. Also runs an internal consistency check across order, payment, goods-movement, and invoice records plus entity-name matching across VAT, business, and packaging registrations.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 各类关税起征点、VAT 税率、EPR 注册要求与生效日期在来源中被总结为具体数字与日期，均可能随政策版本调整，执行前必须以官方最新文本为准，不作为可依赖的当前事实。
- 多单证一致性核对是一种内部审计方法论，不等于官方合规认定标准；即使内部单证一致，仍需以监管机构实际判定为准。
- 不同产品类别（如含电池、含包装、涉及个人数据的联网设备）适用的具体法规组合不同，不能用统一清单不加区分地套用所有产品。
- 本流程只产出适用性与一致性核对记录，不构成海关、税务或法律结论，最终合规判断需由具备资质的顾问基于完整单证作出。

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

1. 列出账户当前实际在售、有库存或计划进入的欧洲站点与仓储所在国，作为后续法规适用范围核对的对象清单，而不是笼统按欧洲整体判断。
2. 对关务与低值包裹关税、VAT/OSS-IOSS、包装 EPR（含电子电器与电池法适用情形）、产品安全披露、平台端涉税数据报送这几类法规逐项核对官方最新文本，记录各自的生效日期版本与是否覆盖对象清单中的国家与产品类别。
3. 核对账户在各国 VAT 登记、EORI、包装/EPR 注册号等身份类单证上的主体名称、地址与营业执照、销售主体信息是否完全一致，标出任何不一致项作为优先整改对象。
4. 核对进口方与实际销售主体是否一致，梳理授权书、代理协议、发票开具主体是否指向同一实体，形成单证链条的一致性核对表。
5. 抽样核对近期订单的资金流、物流、订单信息与发票记录是否可以相互匹配，标出任何流向不一致或缺失单证的订单，作为一致性审计的证据。
6. 针对核对中发现的适用缺口（如未注册的 EPR 类别、未启用的 OSS/IOSS），列出需要注册或调整的事项及对应的官方申请入口，但不自行判断是否已经合规达标。
7. 将适用性核对结果、单证一致性缺口与抽样审计发现整体提交给具备资质的海关、税务或合规顾问复核，由其确认最终合规状态与整改优先级。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 欧洲经营站点与产品适用范围清单
- 分法规类别的官方核对记录（范围/生效日期/是否适用）
- 多单证主体一致性缺口表
- 抽样一致性审计记录
- 待专业顾问复核的整改优先级清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
