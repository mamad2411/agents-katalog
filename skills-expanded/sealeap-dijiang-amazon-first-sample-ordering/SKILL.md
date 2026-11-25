---
name: sealeap-dijiang-amazon-first-sample-ordering
description: "Order and evaluate a first product sample against a why-what-how-many readiness check, pay through a dispute-capable payment method, then inspect packaging, aesthetics, and function with documented photo evidence usable for negotiation and future production QC. Use for 第一次订样品要注意什么、订样品前要准备什么、样品验收清单、样品货款怎么付更安全. Do not use to skip landed-cost validation just because a sample photo looks acceptable."
---

# Amazon 首样订购三步验证法

## 目标

Order and evaluate a first product sample against a why-what-how-many readiness check, pay through a dispute-capable payment method, then inspect packaging, aesthetics, and function with documented photo evidence usable for negotiation and future production QC.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “样品费用在下正式订单后可退还”属于需要与具体供应商事先书面确认的条款，不是所有供应商的默认政策，下单前务必单独确认，不能默认适用。
- 至少订购两家样品会增加前期成本，是否严格执行需按自身预算与该品类的供应商分散度权衡，非绝对规则。
- 样品验收合格不等于量产合格，验收记录应作为后续批量生产验货的对照基准之一，而非跳过批量验货的理由。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、类目、价格带、上架时间与运营模式
- 候选品与同购买意图可比样本的销量、评论、价格和上架时间
- 关键词需求、历史趋势、广告依赖、同款密度和品牌集中度
- 采购、头程、平台费、退货、仓储、交期和合规/IP 基础信息

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 订样前先自答“为什么订这个样”：是否已有需求侧证据（销量/搜索量等代理数据）支持这个品类，以及是否已做过覆盖包装、头程运费、关税等要素的到岸成本测算，证明留有目标利润空间；两者缺一都不建议先花钱订样。
2. 明确“订什么样”：现货样品还是定制样品，按“上市速度要求”与“产品复杂度”两个因素判断——越简单且越急于验证市场的，越适合直接要求供应商基于现有产品定制打样；越需要实物触摸确认设计细节的，越适合先拿现货样品再决定是否定制。
3. 明确“订多少”：至少从两家不同供应商各订一份样品，用于横向比较质量并保留备选供应商，即使会增加样品成本，也优于只押注一家导致没有对比基准或备选方案。
4. 付款环节使用具备买家拒付/争议保障机制的支付方式（例如关联信用卡的第三方支付工具），并在下单前把规格要求、定制说明落成书面记录，作为万一发生纠纷时的凭证。
5. 收到样品后按“包装-外观-功能”三个维度依次验收：先检查包装是否足够牢固（不要急着拆完就丢弃包装，它本身也是验收对象之一），再检查颜色/做工/表面处理等外观一致性，最后逐项验证实际使用功能是否达标。
6. 验收过程全程拍照并记录问题点，这些证据既用于后续量产前的品控对照基准，也可作为与供应商谈判价格或要求整改的依据。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 订样前置条件自查（需求/成本双证据）
- 现货/定制样品决策依据
- 样品验收拍照记录
- 供应商横向对比结论
- 量产前品控对照基准
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
