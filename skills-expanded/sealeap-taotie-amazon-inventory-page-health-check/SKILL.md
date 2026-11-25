---
name: sealeap-taotie-amazon-inventory-page-health-check
description: "Run a health check on the Manage Inventory page: triage inactive and search-suppressed listings, read available, inbound, unfulfillable and reserved quantities with their reasons, audit estimated fees against own measurements, complete missing attributes flagged by the listing quality dashboard, and review merchant-fulfilled handling-time settings. Use for 商品搜不到、非在售原因、搜索结果中禁止显示、库存预留是什么、运营中心调拨、不可售库存怎么处理、预估费用不对、缺失属性提示、商品信息质量面板、自发货处理时间. Do not use to change prices in bulk or to file removal orders without confirming the current fee schedule."
---

# Amazon 库存页体检：可售状态与属性完整度

## 目标

Run a health check on the Manage Inventory page: triage inactive and search-suppressed listings, read available, inbound, unfulfillable and reserved quantities with their reasons, audit estimated fees against own measurements, complete missing attributes flagged by the listing quality dashboard, and review merchant-fulfilled handling-time settings.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 「属性补全会提升曝光与转化」是平台提示与来源经验的组合，提升幅度未知；用补全前后 30 天的浏览与转化对照验证。
- 库龄阈值、IPI 计算方式与费用重测流程随政策更新，来源数字仅作参考，以当前库存绩效页面为准。
- 面板内的浏览量与销售额统计可能滞后或为空，不用它替代业务报告。
- B2B 定价与品牌健康度功能的可用性因账户而异，缺失时记录 NEEDS_EVIDENCE，不猜测。

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

1. 打开管理库存页并切换到平台配送视图，先看「非在售/禁止显示」类入口：缺货、搜索结果中禁止显示（质量原因）、存在风险三类各自的 ASIN 与原因；无提示但前台仍搜不到时再联系支持，入口名称以当前控制台为准。
2. 读库存四个数量：可售、入库中、不可售、预留；预留展开看买家订单、运营中心间调拨、运营中心处理三种原因，调拨中的库存前台会显示延迟到货，旺季调拨周期可能很长，补货计划要提前。
3. 不可售库存及时创建移除或弃置，长期滞留会拖累 IPI；超过当前库龄阈值的库存（可售或不可售）同样影响周转分数，按库龄报告处理。
4. 核对预估配送费：把后台按 Listing 尺寸重量算出的费用与自测尺寸重量对照，差异明显时提交重新测量申请，多收部分可退；此类错误并不少见，列入每月例行。
5. 打开商品信息质量面板（或改进商品信息入口）逐条补全缺失属性：材质、能效、功率、规格等；补全后可进入左侧筛选、五点上方概览、搜索结果规格对比表与单位价格展示，属性填写按类目当前模板。
6. 有品牌健康度/竞争价格提示时，把它理解为站外零售价参考而非站内对手价，定价时只作参考；管理定价页可批量改价但需先写变更表。
7. 自配送商品检查处理时间设置与实际绩效：处理时间过短会伤绩效并可能丢购物车，过长伤转化；按站点模板设默认值并对特定 SKU 单独设置。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 非在售与禁止显示排查表
- 库存四状态与预留原因记录
- 不可售与库龄处理清单
- 预估费用核对与重测申请记录
- 缺失属性补全清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
