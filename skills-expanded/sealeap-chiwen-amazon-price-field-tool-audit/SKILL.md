---
name: sealeap-chiwen-amazon-price-field-tool-audit
description: "Audit Amazon pricing fields and diagnose missing List Price or Typical Price displays using current marketplace rules, genuine price history, Featured Offer and same-product evidence. Use for 划线价消失、参考价不显示、2026参考价规则、自动定价边界、企业购折扣、订购省折扣 or 促销资格核查. Do not fabricate reference prices, orders, or guaranteed display thresholds."
---

# Amazon 定价字段与促销工具核对

## 目标

Audit whether the price-related fields on a listing offer are populated correctly — the advertised-price floor, the everyday selling price, automated-pricing bounds, a time-boxed promotional price, and a reference/list price — and configure the pricing-automation, discount, business-price, and subscription-discount tools that read from them. Flags the specific downside of leaving any one field wrong or unset ahead of a promotional event.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 各价格字段填错的具体后果（如是否隐藏价格、是否限流）由当前平台机制决定且可能调整，实际表现以当前后台真实情况为准，不代入来源描述作为必然结果。
- 订购省折扣幅度、企业购最低降价比例等区间是来源给出的经验建议，需按当前商品的实际利润空间重新测算，不作为固定标准。
- 大促定价新规（报名费、销售额抽成、价格核算窗口等）随活动周期变化，执行前必须在当前官方页面和后台复核，不沿用历史规则。
- 涉及参考价/划线价的设置需符合当前平台对真实定价历史的要求，不采用先抬价再打折或制造虚假参考价的做法。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、币种、店铺、SKU/子 ASIN 与当前定价字段
- Featured Offer、日常价/促销价/List Price、自动定价边界及有效日期
- 当前参考价规则、真实成交/促销历史、同款站外报价与商品身份凭据
- 单位成本、平台/履约费、退货损失及可承受贡献利润；缺失时不建议折扣幅度

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 参考价专项

划线价不展示、突然消失或子体显示不同，先读 [参考价诊断](references/reference-price-diagnostics.md)。用户只问显示异常时交付对应核查结果，不强制开展选品和广告研究。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 逐字段核对当前 Listing 的价格设置：广告最低价类字段是否与日常售价矛盾（矛盾可能导致前台隐藏价格、广告受限），日常售价是否频繁大幅波动（影响排名与折扣核算基准）。
2. 若开启自动定价，检查允许的最低/最高价边界是否已设置，避免系统无边界跟价导致亏本或恶性竞争；大促前评估是否需要临时关闭，防止系统动作影响基准价计算。
3. 核对促销价类字段是否设置了结束日期，避免长期挂折扣价造成持续亏本，并评估促销天数占比是否会拉低后续大促可用的基准价。
4. 核对参考/建议零售价类字段是否有真实依据支撑，虚高的参考价存在被判定误导性定价、无法展示划线价的风险，无依据时应清理或按真实价格重设。
5. 按业务需要配置企业购价格（通常需比日常价低一定幅度，可设阶梯折扣）与订阅省复购折扣，折扣幅度需按当前品类利润空间测算，不套用固定区间，且需先确认账户资质是否满足开启条件。
6. 大促报名前完整走一遍以上字段与工具核对，并核实当前大促的资格、费用与定价新规是否有更新，以当前官方公告为准再确认参与。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 价格字段核对清单（含填错风险标注）
- 自动定价边界设置记录
- 促销价与参考价合规检查结果
- 企业购/订阅省工具配置记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
