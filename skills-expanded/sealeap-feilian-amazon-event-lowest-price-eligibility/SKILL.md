---
name: sealeap-feilian-amazon-event-lowest-price-eligibility
description: "Reconstruct each candidate ASIN's recent real-transaction price trail (coupons, discounts, lightning deals) against the current event's lowest-price eligibility window before submitting a deal, then screen out ASINs that already used up their price room through routine promotions. Treats the lookback-window length and the required additional discount as marketplace-specific parameters to reconfirm on the current official rules page rather than fixed constants. Use for 大促最低价资格自查、价格历史梳理、ASIN提报筛选、站外价格与站内提报价冲突核查、子账号价格权限检查. Do not use to submit a deal price without first reconstructing the lookback-window price history in the account's own pricing tool."
---

# Amazon 大促最低价资格筛查规划

## 目标

Reconstruct each candidate ASIN's recent real-transaction price trail (coupons, discounts, lightning deals) against the current event's lowest-price eligibility window before submitting a deal, then screen out ASINs that already used up their price room through routine promotions. Treats the lookback-window length and the required additional discount as marketplace-specific parameters to reconfirm on the current official rules page rather than fixed constants.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的具体回溯天数、额外折扣幅度与各站点早鸟减免额度是特定批次的活动参数，会随大促届次调整，一律以当前官方活动规则页面为准，不作为固定公式套用。
- 站外推广价格是否计入最低价参考是来源提出的待验证担忧，官方判定口径未公开确认，只能按当前规则页面的明确说明处理，不确定时按更保守的假设规划价格。
- 子账号价格权限的具体开通路径可能随后台界面调整，操作前以当前登录后台的实际菜单位置为准。
- 最低价规划不得通过先抬价再制造大幅折扣、虚构订单或异常交易伪造价格历史的方式满足资格条件，只使用真实成交价格达标。

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

1. 在后台价格相关工具中导出候选ASIN最近一段时间的真实成交价轨迹，包括优惠券、限时折扣、秒杀价等各类促销留下的价格点，与日常自然标价分开标记。
2. 打开目标站点当前的大促最低价资格规则页面，记录本次要求的回溯窗口长度与在此基础上需额外让利的幅度（不同站点规则可能不同），以当前页面文字为准，不沿用以往批次的印象。
3. 逐个候选ASIN比对：过去的常规促销（冲单优惠券、清库存折扣、节日短促）是否已把价格降到低于或接近本次门槛，若是则判定为已提前透支价格空间，不强行报名。
4. 核对是否存在站外渠道展示价与站内价不一致的情况，评估站外价格是否可能被计入官方参考价轨迹，避免站内外价格体系冲突导致资格误判。
5. 对通过筛查、确认有资格空间的ASIN，在报名前于价格工具中做一次模拟核验，并确认操作账号（主账号或已获得相应价格权限的子账号）拥有查看与提交权限。
6. 把站内提报价与站外促销节奏放在同一张时间表里统一规划，避免不同团队各自调价导致某个时间点价格意外跌破或未达到资格门槛。
7. 报名前最后复核一次盈亏平衡：确认该最低价水平下的单件净贡献仍为正或在可接受范围内，而不是为拿到大促曝光资格牺牲全部利润空间。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：视需要核对第三方比价或价格历史工具中的公开价格轨迹，交叉验证后台参考价判断是否与站外可见价格一致。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 候选ASIN真实成交价历史轨迹表
- 当前大促最低价资格规则记录
- ASIN资格筛查结果（通过/透支/待定）
- 站内外价格协同时间表
- 报名前盈亏平衡复核记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
