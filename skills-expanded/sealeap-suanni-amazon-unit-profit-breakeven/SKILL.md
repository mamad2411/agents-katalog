---
name: sealeap-suanni-amazon-unit-profit-breakeven
description: "Build a per-unit profit model for an FBA product from selling price, sourcing cost, first-mile cost, fulfilment fee, referral fee and other fees, and derive gross margin, net payout and the break-even price under alternative logistics routes. Use for 一单能赚多少、利润怎么算、保本价、盈亏平衡价、毛利率、店铺回款、海运空运利润对比、最多能降到多少钱. Do not use to set final prices or promotions without current fee schedules and verified cost inputs."
---

# Amazon FBA 单品利润与保本价测算

## 目标

Build a per-unit profit model for an FBA product from selling price, sourcing cost, first-mile cost, fulfilment fee, referral fee and other fees, and derive gross margin, net payout and the break-even price under alternative logistics routes.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源使用的类目佣金比例、汇率、配送费与头程单价都是示例数值，正式测算以当前站点费率表、类目佣金表和实际报价为准。
- “首批小批量仓储费可忽略、不打广告就没有广告费”是简化假设，只适合首单可行性测算；正式经营模型必须计入广告、仓储、退货与促销折扣。
- 保本价只覆盖已列出的成本项，未列项（退货、广告、超龄库存、汇兑损失）会让真实盈亏点高于计算值；以当前账户的实际费用结构校准。
- 只在 marketplace、币种、时间窗一致时比较不同方案；不同来源的成本口径冲突时保留各自口径并说明，不取平均。

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

1. 定义测算售价：用目标市场同类产品的公开售价区间与自身定位确定，并注明是拟定价还是现价；采购价按含税含运的实际到手价，用当期汇率折算成售价币种并记录汇率取值日。
2. 逐项填入每单变动成本：FBA 配送费（按尺寸分段与当前费率表）、头程每单位成本（按计费重与所选渠道）、平台佣金（按当前类目费率与价格分段计算，不同类目与价格段比例不同）、以及包装、标签、退货等已知的单位成本。
3. 单独列出阶段性或可选成本：月度仓储费（按体积与季节，首批小批量时占比通常很低）、入库配置费、广告费、超龄库存费等；标明本次是否计入及理由，避免把“未计入”误当成“不存在”。
4. 计算四个结果：毛利 = 售价 − 各项每单成本；店铺回款 = 售价 − 平台扣除项（配送费、佣金等）；毛利率 = 毛利 ÷ 售价；并核对回款能否覆盖采购与头程等自付现金成本。
5. 计算保本价：把随售价按比例变动的费用（佣金等）与固定金额费用分开，保本价 = 固定金额成本之和 ÷ (1 − 比例费率之和)；用保本价回代验证毛利为零，作为降价、促销与竞价的底线。
6. 对不同物流方案（空运/海运、不同渠道）各做一版，比较毛利额与毛利率差异；差异大时把物流方案当作决策变量而非常量。
7. 输出前做敏感性检查：售价下调、汇率变化、退货率上升、广告投入增加时的毛利变动，并标出哪一项最先把利润打穿。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取同类竞品的公开售价区间，作为测算售价与保本价的对照。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 单品成本结构表（每单变动成本与阶段性成本）
- 毛利、毛利率与店铺回款计算
- 保本价与回代验证记录
- 物流方案利润对比
- 敏感性检查与缺口说明
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
