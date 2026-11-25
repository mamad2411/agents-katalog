---
name: sealeap-dijiang-amazon-china-to-fba-freight-routing
description: "Choose between shipping supplier-direct to Amazon fulfillment centers versus routing through a local prep/3PL warehouse first, based on inbound volume limits, product complexity, and seller experience, then execute the labeling and freight-forwarder checklist needed for either path. Use for 从工厂直发FBA还是先到海外仓、头程物流怎么选、FBA入仓标签要求、货代和报关怎么配合. Do not use to skip a China-based inspection step purely to save cost on a first-time or high-defect-risk product."
---

# Amazon 头程物流路径选择

## 目标

Choose between shipping supplier-direct to Amazon fulfillment centers versus routing through a local prep/3PL warehouse first, based on inbound volume limits, product complexity, and seller experience, then execute the labeling and freight-forwarder checklist needed for either path.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 入仓分拨服务的具体附加费率、免费重量门槛等以平台当前费率表为准，来源中的具体数字仅为示例，不能直接套用到当前账户。
- “供应商知道你在做零售电商后可能会绕过你直接上架竞争”是来源提出的风险假设，需结合具体供应商的历史合作情况判断，不是所有供应商都会如此，但在选择直发合作深度时应纳入考量。
- 特殊类目（易碎/服饰/珠宝等）会被强制指定发往特定仓的规则以平台当前政策为准，选择物流路径前应在实际创建入仓计划时核实，而不是凭品类经验预判。
- 货代与中转仓的资质、口碑差异很大，选择前应做独立尽调（资质、过往案例、是否可现场抽查），不能仅凭价格低或宣传选择。

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

1. 先核实自身账号当前的入仓量与仓容限制，以及目标商品是否属于常被指定发往特定仓（如易碎/服饰/珠宝等类目）的特殊类目，这两点决定了“能否走整柜/大批量直发”这条路是否现实。
2. 在创建入仓计划时对比两种分仓设置：按平台默认的分布式入仓（多仓分散、时效更好但打包发货成本更高），与集中发到一个仓再由平台代为二次分拨（省去自己拆分打包、但会产生按重量/尺寸计算的额外服务费）；按自身批量大小与利润空间选择，货值高、单件不大的更适合走后者。
3. 若选择工厂直发：与供应商逐项确认产品标签、外箱标签、栈板标签三类标签是否齐全且信息正确，要求供应商在发货前提供每个栈板、每箱及抽样产品的实拍照片核对，并确认包装材料满足目的地的植物检疫等基础合规要求。
4. 若选择先入本地中转仓：预留质检窗口，让中转仓在货物入库时先做外观与数量抽检，出问题在造成大批量入仓前就能拦截，这一步是新手或对该供应商还不熟悉时降低批量事故风险的关键动作。
5. 无论走哪条路径都要提前联系货代确认清关文件与费用预估，货代的角色是衔接工厂发货与目的地入仓/中转仓收货的中间环节，出现单据或清关问题时由其协调处理，不要等到货物已在途才第一次接触货代。
6. 综合判断标准：新手、批量小、或对供应商标签合规能力没把握时优先选先入中转仓路径；有经验、供应商配合度高、且能在合理时间内把货售出的，直发路径通常更省成本和时效，两条路径都应在出发前完成上面的标签与单据核对清单。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 入仓路径选择依据（直发 vs 先入中转仓）
- 标签与包装合规核对清单
- 货代与清关对接记录
- 入库质检拦截结果（如走中转仓）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
