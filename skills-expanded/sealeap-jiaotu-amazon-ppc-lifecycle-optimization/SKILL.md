---
name: sealeap-jiaotu-amazon-ppc-lifecycle-optimization
description: "Sequence Sponsored Products/Brands/Display structure and budget emphasis across a cold-start, growth, and mature phase using the account's own click and conversion thresholds rather than fixed benchmarks, then run a fixed weekly review that reallocates spend toward proven winners and pauses zero-conversion or low-CTR targets. Phase boundaries and target ACOS are treated as calibrated to the product's own margin, not universal numbers. Use for 新品广告冷启动结构搭建、广告阶段升级判断、每周否词与加价SOP、分时竞价设置、SD再营销预算占比. Do not use to copy fixed day-counts, ACOS targets, or budget percentages from another account without recalibrating to this product's margin and data volume."
---

# Amazon PPC生命周期分阶段优化

## 目标

Sequence Sponsored Products/Brands/Display structure and budget emphasis across a cold-start, growth, and mature phase using the account's own click and conversion thresholds rather than fixed benchmarks, then run a fixed weekly review that reallocates spend toward proven winners and pauses zero-conversion or low-CTR targets. Phase boundaries and target ACOS are treated as calibrated to the product's own margin, not universal numbers.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的各阶段具体天数、目标ACOS区间和预算占比表是其经验模板，实际阶段划分应按自身产品的流量获取速度和数据积累速度判断，不同客单价和类目差异很大。
- "再营销转化率是新客的数倍""ROAS可超过某具体值"等是来源给出的经验数字，需用自身账户的再营销实际数据验证后才能作为预算倾斜依据，不能直接引用。
- 分时竞价的具体高效/低效时段因类目、目标市场时区和购物习惯而异，应基于自身账户按小时的转化数据分析后设置，不套用固定时间段。
- 具体竞价策略组合的效果依赖当前平台的竞价算法机制，属于待验证的操作假设，应小范围测试后再扩大应用。

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

1. 冷启动阶段以自动广告和少量高确定性长尾词手动广告并行，目标是积累搜索词数据而非控制ACOS；设定进入下一阶段前必须达到的最低数据量门槛，门槛按自身类目单价与流量水平设定，不套用固定数值。
2. 达到数据量门槛后，用自动广告跑出的搜索词报告识别高转化词并转入手动精准，同时识别持续无转化或方向不对的词做否定；否定范围只覆盖明确不相关的词，避免把还没积累够数据的长尾词提前否掉。
3. 进入成长阶段后，按每个关键词/定位自身的转化效率重新分配预算：把预算从高花费低转化的方向移向已验证的高转化方向，加价与降价幅度按账户自身ACOS与目标ACOS的差距决定，而非固定百分比。
4. 建立固定周期的优化例程：核对累计点击量已达统计意义的目标是否零转化并降价或暂停、核对高曝光低点击的目标是否需要降价或暂停、对表现优于目标ACOS的方向适度加价；复核数据窗口应覆盖足够天数以避免单日波动误判。
5. 进入稳定阶段后，把预算逐步向已验证的核心词与再营销方向集中：核心词采用不主动加价的竞价策略卡位，再营销面向近期浏览或购买过但未复购的访客，用自身数据验证再营销的实际转化与投产是否确实优于新客获取。
6. 品牌词与自身ASIN定位的防御性广告贯穿各阶段，按竞品截流的实际发生情况决定是否需要加大品牌防御预算，而非预先假设一定需要。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 三阶段广告结构与预算分配草案
- 关键词/定位分类与否定词处理记录
- 每周优化SOP执行清单
- 再营销人群与投产验证记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
