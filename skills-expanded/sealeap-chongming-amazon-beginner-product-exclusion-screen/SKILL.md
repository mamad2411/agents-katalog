---
name: sealeap-chongming-amazon-beginner-product-exclusion-screen
description: "Screen product candidates against ten risk classes that commonly hurt first-time sellers (low price band, fragility, electronics, apparel sizing, batteries, patents, seasonality, food and supplements, oversized goods, gated categories), turning each into evidence checks against current fees, policies and certification requirements. Outputs an exclude / conditional / proceed verdict per candidate rather than a blanket ban. Use for 新手不该卖什么、候选产品风险排除、带电产品能不能做、季节品要不要做、这个品会不会被专利下架、类目是否需要认证. Do not use as the only screen, since margin, demand and supplier checks still apply, and experienced sellers may deliberately accept a barrier as a moat."
---

# Amazon 新手选品排除清单核查

## 目标

Screen product candidates against ten risk classes that commonly hurt first-time sellers (low price band, fragility, electronics, apparel sizing, batteries, patents, seasonality, food and supplements, oversized goods, gated categories), turning each into evidence checks against current fees, policies and certification requirements. Outputs an exclude / conditional / proceed verdict per candidate rather than a blanket ban.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的价格下限、服装退货率、大件运费倍数等均为经验数字，不作为规则；按当前站点费率与本账户数据校准。
- 来源称食品必须在目标国生产、补剂利润极高等说法未经核实；食品与补剂的准入、原产地与标签要求以当前平台与监管规定为准。
- 来源的儿童产品证书多次被拒是个案，说明证书格式、检测机构资质与类目要求可能不透明；申请前先查阅当前类目要求并与检测机构确认平台接受的模板。
- “门槛可以变成护城河”成立的前提是已有经验、资金与合规能力；本清单默认面向首个产品，不用于替代成熟卖家的类目策略。

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

1. 先按当前费率给候选算一次到手毛利：售价 − 佣金 − FBA 配送费 − 采购 − 头程 − 预计广告；低价带产品若在现有费率下毛利无法覆盖广告与退货，标为排除；价格下限以本账户测算校准，不用固定数字。
2. 退货与物流风险三项核查：易碎品（运输挤压与末端派送场景下的破损率、需要的防护包装成本）、电子/带电产品（退货率、使用复杂度、锂电池运输申报与危险品认定）、服装类（尺码退货、产地尺码与目标市场尺码差异、SKU 数量带来的库存分散）。每项记录证据来源与是否可用包装、说明或尺码表缓解。
3. 合规门槛核查：食品与补剂（原产地、标签、FDA 或站点等效监管要求、类目准入）、受限/受管制类目（儿童用品等所需证书、平台接受的检测机构与证书格式）；先建测试 Listing 或查看类目申请要求确认是否受限，再决定是否下单。
4. 专利与 IP 核查：对“卖家少、卖得好、评论不多”的候选先做专利与外观检索（公开专利检索平台）和商标检索；查到疑似权利时标为排除或需专业意见，不能凭“暂时没人投诉”放行。
5. 季节性核查：用关键词搜索量或类目销量的年度曲线判断淡旺季；季节品要预估淡季仓储费、资金占用与断季清仓风险，首个产品默认排除，除非能按旺季倒排备货。
6. 体积重量核查：与常规小件相比估算头程与配送费倍数（按当前 FBA 尺寸分级与货代报价），大件通常须走海运并核对交期；超出资金与周期承受范围的标为排除。
7. 汇总每个候选的十项核查结果，给出 EXCLUDE / CONDITIONAL（列出需补的证书、包装、检索）/ PROCEED，并记录每项依据；有条件项要写明解决成本与时间。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取专利与商标公开检索、类目准入要求页面以及候选品价格带与评论数的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 候选产品十项风险核查表
- 到手毛利粗算（按当前费率）
- 专利/商标/类目准入检索记录
- 季节性与体积重量评估
- EXCLUDE / CONDITIONAL / PROCEED 结论与补条件清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
