---
name: sealeap-fenghuang-amazon-fba-inbound-shipment
description: "Walk through creating an FBA inbound shipment on the US marketplace—ship-from address, destination marketplace, case-pack template within current inbound limits, prep requirements, FNSKU labeling, carton count, ship date, SPD versus LTL, carrier and FBA box labels—and verify each item before cartons leave for the carrier. Use for 怎么发货到 FBA 仓、第一次入仓、货件计划怎么建、FNSKU 标签、箱规限制、SPD 还是 LTL、箱标怎么贴. Do not use for hazmat classification or customs and import compliance decisions."
---

# Amazon FBA 入仓货件创建与标签核对

## 目标

Walk through creating an FBA inbound shipment on the US marketplace—ship-from address, destination marketplace, case-pack template within current inbound limits, prep requirements, FNSKU labeling, carton count, ship date, SPD versus LTL, carrier and FBA box labels—and verify each item before cartons leave for the carrier.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的箱规上限、贴标费用与运费金额是当时数值，一律以当前 Seller Central 显示为准。
- 「平台合作承运商一定更便宜」是经验判断，需按本次箱数、重量与地区实际比价。
- 本 Skill 不覆盖清关、关税与危险品判定；跨境直发前先确认进口人身份与产品资质。

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

1. 从库存管理进入「发送/补充库存」，先核对发货地址：从工厂直发就填工厂地址；地址错误会导致分仓与运费偏差。
2. 确认目的 marketplace（默认 US），建立箱规模板：填写每箱件数、箱体尺寸与重量，并对照当前 FBA 入仓限制（单边长度、单箱重量、每箱件数上限），以当前官方要求为准，超限要拆箱或换包装。
3. 判断预处理：多数商品选无需额外预处理，但婴童、成人用品、易碎、液体、纺织类可能需要装袋或加固；按品类核对后再保存模板。
4. FNSKU 贴标：优先让工厂在包装上直接印刷或贴标，Amazon 代贴按件收费；确认每件单品条码清晰可扫、不与其他条码冲突。
5. 填写箱数与总件数、选择发货日期，再选 SPD（小包裹，快递上门取件或自送）或 LTL（整托盘，安排卡车提货）；比较平台合作承运商报价与自行安排的报价。
6. 打印两类箱标——承运商面单与 FBA 箱号标签，逐箱核对重量尺寸、发货与收货地址；标签贴平整、不被胶带覆盖。
7. 发出后在货件列表跟踪状态（已送达 ≠ 已入库）；入库延迟超过承运商承诺时间时，准备签收凭证以便发起货件调查。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 货件创建检查表
- 箱规模板记录
- 预处理与贴标方案
- 运输方式比价表
- 箱标与跟踪记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
