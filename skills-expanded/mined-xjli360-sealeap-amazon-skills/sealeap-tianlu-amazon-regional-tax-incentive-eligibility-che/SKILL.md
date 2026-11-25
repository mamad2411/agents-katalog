---
name: sealeap-tianlu-amazon-regional-tax-incentive-eligibility-check
description: "Verify a China-based cross-border seller's current eligibility for regional tax-incentive pilot programs (deemed-basis taxation, invoice-free exemption, or export-tax-refund routes) against live official sources, and track the registration process to completion. Does not compute or assert any specific tax liability or legal conclusion. Use for 综试区税收优惠资格判断、核定征收/无票免税申请前核查、离境即退税流程确认、多地政策对比. Do not use to calculate a final tax rate or liability, or to replace a qualified tax advisor's opinion."
---

# Amazon 跨境税收优惠试点资格核验

## 目标

Verify a China-based cross-border seller's current eligibility for regional tax-incentive pilot programs (deemed-basis taxation, invoice-free exemption, or export-tax-refund routes) against live official sources, and track the registration process to completion. Does not compute or assert any specific tax liability or legal conclusion.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源中列举的具体准入条件、名额上限、税率/征收率与计税公式为该时间点报道内容，实际执行以当地政府与税务机关当前公开文件为准，且可能因地区、时间而异。
- 文中的多步骤线下/线上登记流程可能随平台或政务系统更新调整，操作前应在官方入口重新核对每一步的当前名称与顺序。
- 是否符合“小微企业”等优惠条件涉及企业整体经营数据判断，不属于可自行下定论的事项，需由具备资质的税务顾问确认。

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

1. 识别本账户注册主体所在地及经营结构，能实际触达哪些地方性综试区/专项政策，不假设某项政策全国通用。
2. 直接从当地政府或税务机关官网、平台官方公告获取政策原文，记录版本、生效日期与名额是否仍开放的核查时间点，不采用二手转述。
3. 把账户实际情况（主体注册地、是否走保税仓/海外仓、开票方式、使用的平台）逐条对照官方公布的准入条件，标记已核实/待核实/不符合。
4. 涉及多方登记的流程（如物流代理协议、税务机关出口退免税登记、平台账户备案）按官方当前流程顺序推进，每一步都以签发机关自身的记录或确认为准，而不是仅凭申请人自留的提交记录。
5. 任何优惠税率或免税结论用于财务测算前，先由具备资质的税务顾问确认适用的计算口径及企业自身条件（如小微企业认定、发票取得情况）是否改变结果，不自行计算或对外发布具体税负数字。
6. 设定复查节奏（如每次申报周期前），因试点名额、税率与有效期存在时限，需重新核实而非依赖首次登记时的信息快照。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 试点资格核验记录
- 官方政策原文与生效日期存档
- 待确认/待补材料清单
- 注册流程完成度跟踪表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
