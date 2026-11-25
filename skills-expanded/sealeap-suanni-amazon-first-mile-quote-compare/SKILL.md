---
name: sealeap-suanni-amazon-first-mile-quote-compare
description: "Normalise freight-forwarder quotes for FBA inbound shipments into a per-unit first-mile cost by applying each channel's own chargeable-weight rule, surcharges, duty treatment and last-mile delivery type, then rank channels on cost, transit time and reliability. Use for 头程物流成本怎么算、货代报价怎么比、体积重除数、包税不包税、卡派快递派、海运空运选哪个、一箱运费多少. Do not use to prepare customs declarations or to decide declared values; those follow destination-country customs rules and a licensed broker."
---

# Amazon FBA 头程物流报价比价

## 目标

Normalise freight-forwarder quotes for FBA inbound shipments into a per-unit first-mile cost by applying each channel's own chargeable-weight rule, surcharges, duty treatment and last-mile delivery type, then rank channels on cost, transit time and reliability.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源中的体积重除数、单价、附加费与税率均为某一时期某一货代的报价，仅用于说明算法；实际比价以当前报价表和货代书面确认为准。
- 来源提到目的国申报价值可按采购价的一定比例低报以降低税费，这是海关合规风险，不采用；申报价值按目的国海关规则如实申报，税率以货代或报关行确认为准。
- 海运比空运单位成本低、卡车派送比快递派送便宜是一般倾向，但要结合备货周期、资金占用与断货风险判断，不能只看单价。
- 不同货代的计费重、税费、附加费口径不一致，比价前先统一口径；报价缺项时标 NEEDS_EVIDENCE，不得用平均值补。

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

1. 先固定比较基准：外箱实测尺寸与毛重、每箱装数、目的仓库代码（由平台分配，不可自选）、时效要求；所有货代与渠道都按同一箱规、同一目的仓比较。
2. 逐家货代逐渠道读取报价表并记录：单价适用的重量段、体积重除数（同一货代可能给多档除数对应不同单价）、是否包税、尾端是卡车派送还是快递派送、按品类的附加费条款、最低起收量（如按方计费的起收方数）。
3. 对每个渠道按其自己的除数算体积重，与实重取大得到计费重；同一渠道有多档除数时每档各算一遍，取该渠道内的最低总价，不能拿甲渠道的除数套乙渠道的单价。
4. 每箱总费用 = 计费重 × 单价 + 附加费 + 税费：不包税渠道按目的国规则如实申报、税率以货代书面确认为准估算；包税渠道税费为零但单价通常更高；不确定的附加费与税率先向货代确认再算，不猜。
5. 把每箱总费用除以每箱装数并折算到售价币种，得到每单位头程成本，与 FBA 配送费、佣金一起放进单品利润表。
6. 在成本排序之外加入稳定性与时效维度（历史准点率、旺季爆仓、丢件赔付、尾端派送方式对入仓速度的影响），对最便宜渠道做“便宜多少、慢多少、风险多大”的对照后再定。
7. 把本次比价表存档并定期重跑：长期固定用同一家货代或同一渠道往往并非最便宜，按季度或旺季前复核一次。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 渠道比价表（每箱与每单位头程成本）
- 计费重与除数计算记录
- 附加费与税费假设清单（含货代确认状态）
- 渠道推荐与成本、时效、风险对照
- 复核周期与触发条件
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
