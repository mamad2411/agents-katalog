---
name: sealeap-chiwen-amazon-ad-report-template-export
description: "Generate a consolidated advertising performance report spanning all sponsored-ad types in one export, using either an official report template or a custom column set filtered by campaign, marketplace, and date range. Supports recurring reuse by editing and rerunning a saved template rather than rebuilding the filter each time. Use for 广告报表怎么导、新品广告数据怎么监控、对比不同广告位表现、关联出单要看哪个报表、周度月度复盘要拉哪些字段. Do not use to compare reports across different date ranges, currencies, or ad types without first checking their attribution window and statistical caveats are consistent."
---

# Amazon 广告报表模板化导出分析

## 目标

Generate a consolidated advertising performance report spanning all sponsored-ad types in one export, using either an official report template or a custom column set filtered by campaign, marketplace, and date range. Supports recurring reuse by editing and rerunning a saved template rather than rebuilding the filter each time.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 报表入口的具体菜单路径、预设模板种类与可筛选字段会随后台改版调整，实际操作以当前界面为准，不代入固定路径。
- 合并 SP/SB/SD 到同一报表虽方便对比，但不同广告类型的计费与归因口径可能不同，跨类型比较结论需按当前官方说明核实统计口径是否一致。
- 关联出单、广告位点击率对比等衍生分析依赖报表字段是否完整覆盖所需维度，字段缺失时应先补齐定制列，不用不完整数据下结论。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、店铺、ASIN/SKU、广告类型和目标
- 同口径的 Campaign、Targeting、Search Term、Placement 与 Advertised Product 报告
- 售价、优惠、COGS、Amazon 费用、退款与目标贡献利润
- 库存、Buy Box、Listing、评论和同期市场事件

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 进入广告活动管理下的报告入口，判断用官方预设模板（覆盖活动、受众、商品、搜索词展示份额、定向等常见场景）还是自定义新建模板。
2. 命名报告并设置筛选条件：账户、广告活动范围、国家/地区、广告产品类型，可一键全选以合并 SP/SB/SD 到同一份报表，用广告产品列区分类型。
3. 定制列：按当前分析目的勾选维度（日期、广告活动、广告位、商品、受众等）与指标（展示量、点击量、点击率、花费、购买量、销售额等），删除当前用不到的冗余列。
4. 提交生成，在报告列表中等待状态完成后下载；同一模板可在后续复用时直接编辑筛选条件重新生成，无需从头搭建。
5. 针对新品监控，用「活动+新品ASIN」筛选专项报表跟踪曝光、点击、转化；针对广告位优化，对比首页首位与商品页面等不同广告位的点击率与转化率差异。
6. 需要跨维度透视（如按日期、广告类型、广告位聚合看周月趋势）时，把导出的明细数据用表格工具二次汇总，不依赖报表原始视图直接下结论。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 合并广告报表模板（可复用）
- 新品监控专项报表
- 广告位表现对比表
- 跨维度周月复盘透视表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
