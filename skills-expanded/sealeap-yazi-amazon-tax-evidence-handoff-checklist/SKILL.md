---
name: sealeap-yazi-amazon-tax-evidence-handoff-checklist
description: "Assemble an evidence package for cross-border e-commerce tax questions by mapping the operating entity, transaction chain, and available documentation (sales exports, cost invoices, customs records), flagging gaps before handoff. Produces no tax conclusions, rates, or filing positions on its own -- the output is a review-ready package for a qualified tax professional. Use for 跨境电商税务问题怎么核查、税务约谈前怎么准备资料、多主体收入归属怎么说明、成本票缺失怎么整理证据、出口备案资料清单怎么列. Do not use to determine tax rates, filing amounts, exemption eligibility or any tax conclusion -- always hand off to a qualified tax professional before filing or responding to authorities."
---

# Amazon 跨境税务单证复核转介

## 目标

Assemble an evidence package for cross-border e-commerce tax questions by mapping the operating entity, transaction chain, and available documentation (sales exports, cost invoices, customs records), flagging gaps before handoff. Produces no tax conclusions, rates, or filing positions on its own -- the output is a review-ready package for a qualified tax professional.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源涉及的具体税率、免税销售额门槛、罚款比例、结算周期天数等数字会随司法辖区和政策生效时间变化，本 Skill 不复述任何数字，一律以税务师核实当前规则为准。
- 来源中按平台展示的成交总额而非到账金额申报、买单报关无法享受免税等属于特定政策环境下的经验判断，需由税务师结合企业当前主体架构与最新政策重新确认，不作为通用结论直接套用。
- 涉及关联主体定价、跨境资金归集、备案缺失补救等场景，风险认定与补救路径必须由税务或外汇合规专业人员出具意见，本 Skill 只负责证据整理，不判断是否合规。
- 来源中任何绕开正规报关、伪造交易真实性证明或掩饰关联交易的操作建议一律不采纳，识别到此类描述时只记录为来源提及但不采用。

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

1. 列出涉及的全部经营主体（境内公司、个体户、境外主体等）及其登记与备案状态，逐个核对是否存续、由谁控制、必要的对外投资或跨境电商相关备案是否已完成，缺失信息一律标记为待核实。
2. 梳理交易链条：货物流（供应商到仓储/海外仓到买家）、资金流（平台回款路径，是否经关联主体或个人账户）、单据流（报关单、发票、物流单）三条链路逐一画出，标出目前证据缺失的环节。
3. 汇总收入与成本的原始单证：平台后台可导出的销售与费用明细、报关记录、进项发票、供应商与物流合同，按统一时间窗口对齐，原始数据来源不明的先标注待核实。
4. 核对每类单证与所在司法辖区现行规则的对应关系（是否需要特定备案、发票类型、申报口径）时，只记录规则要求核对的项目，不代入具体税率、免税门槛或金额结论，交由税务师依据当前政策判断。
5. 识别并列出高风险信号供专业人员优先处理：长期零申报但有真实交易记录、大额个人账户流水无凭证、关联主体间定价缺乏独立商业依据、报关与平台销售数据差异较大且无解释文件。
6. 把主体清单、交易链条图、单证缺口清单与风险信号整理成转介材料，注明本材料不构成税务结论，连同缺口清单提交给有资质的税务师或会计师事务所，取得正式意见后再申报或答复税务机关。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 经营主体清单（含备案与存续状态标记）
- 交易链条图（货物流/资金流/单据流）
- 单证与证据缺口清单
- 高风险信号清单
- 转介税务师的证据包与待确认事项
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
