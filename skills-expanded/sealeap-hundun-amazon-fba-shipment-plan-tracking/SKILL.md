---
name: sealeap-hundun-amazon-fba-shipment-plan-tracking
description: "Walk through creating an FBA inbound shipment end to end — barcode strategy, packing-type qualification (mixed-SKU carton versus single-SKU manufacturer-packed carton), box-level quantity allocation, prep/labeling ownership, carrier selection — then track the shipment through to warehouse receipt, flagging the small tolerance for post-submission quantity edits and the possibility of automatic warehouse splitting. Operational checklist only; current fee schedules and thresholds must be confirmed in-account. Use for FBA发货计划怎么创建、混装和原厂包装怎么选、贴标该自己做还是让亚马逊做、发货后怎么跟踪到仓状态、货件被分仓了怎么办. Do not use for FBM self-fulfillment shipping, and do not finalize box quantities assuming unlimited post-submission edit room."
---

# Amazon FBA发货计划创建与跟踪

## 目标

Walk through creating an FBA inbound shipment end to end — barcode strategy, packing-type qualification (mixed-SKU carton versus single-SKU manufacturer-packed carton), box-level quantity allocation, prep/labeling ownership, carrier selection — then track the shipment through to warehouse receipt, flagging the small tolerance for post-submission quantity edits and the possibility of automatic warehouse splitting. Operational checklist only; current fee schedules and thresholds must be confirmed in-account.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 贴标/预处理代做费用、每箱数量上限、提交后可调整的数量幅度等均为来源经验观察，具体数值需以当前账户/类目页面显示的最新条款为准。
- 分仓是平台可能出现的正常调度行为而非操作失误，遇到时应逐个子货件核对目的地仓库和到货数量，不要按总量笼统核对。
- 条码策略涉及串码/唯一性合规问题，选择前需确认当前平台政策与自身产品是否符合共用条码的资格条件。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、库存阶段、补货与到仓时间
- 断货或备货前后的销量、流量、广告、自然位置和转化基线
- COGS、头程、仓储、平台费、退货和清仓成本
- 可比产品的成熟度、销量区间和需求趋势

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 确认前置条件：listing 已上传、当前为在售状态、有购物车按钮、有可售库存，再考虑转换/创建 FBA 发货；条码策略上，优先使用平台分配的唯一条码，除非有明确理由需要与目录共用制造商条码。
2. 选择发货范围与地址：已经确定马上要发货就直接选择“转换并发送库存”一步到位；只是想先转换发货方式、暂不创建货件则用“直接转换”；发货地址如非默认注册地址，需在对应入口手动指定并补全地址要素。
3. 判断包装类型：单个外箱内有多个不同 SKU 或不同状态用“混装商品”；单个外箱内 SKU、状态、每箱数量完全一致的用“原厂包装商品”，并确认满足该类目当前对每箱数量上限等要求后再选择，不确定就按混装处理更保险。
4. 混装场景下按箱建立/复用装箱模板，逐箱填写各 SKU 的实际装箱数量，并如实填写每箱的重量与外尺寸，不能用估算值敷衍。
5. 选择预处理与贴标由卖家自己完成还是由平台代为完成：代做通常会产生额外的单件费用，是否使用应结合当前费率与自身产品利润空间判断，而不是默认选择省事的一方。
6. 提交前完整核对每个 SKU 的数量、箱数、尺寸重量，因为提交后可修改的数量幅度非常有限，不能寄望于先交上去再慢慢改。
7. 确认配送方式与承运人、发货日期与预计送达窗口后完成提交，打印外箱标签与单品标签贴妥；发货后录入跟踪号并标记已发货，之后通过货件处理进度定期核对已发/已收数量与状态，留意平台可能把一次发货拆分到多个仓库的情况，分别跟踪每个子货件。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- FBA发货计划参数记录（条码策略/包装类型/地址）
- 装箱模板与逐箱SKU数量表
- 箱唛与单品标签文件
- 货件跟踪状态表（已发/已收/目的仓）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
