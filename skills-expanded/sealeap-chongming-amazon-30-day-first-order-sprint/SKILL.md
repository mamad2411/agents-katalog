---
name: sealeap-chongming-amazon-30-day-first-order-sprint
description: "Run a time-boxed first-order sprint that sequences business registration, relaxed-criteria product screening, a small stock-item test order, seller account creation, listing build, inbound shipment and an auto campaign into dated milestones with go/no-go checks at each stage. Designed to validate the end-to-end process and the seller's confidence, explicitly separated from long-term product selection. Use for 新手怎么快速出第一单、30 天走通流程、小批量试单、测款流程、迟迟不启动怎么办、第一个产品别选太久. Do not use to pick a long-term flagship product or to scale spend before the sprint's margin and sell-through data are read."
---

# Amazon 首单 30 天试跑计划

## 目标

Run a time-boxed first-order sprint that sequences business registration, relaxed-criteria product screening, a small stock-item test order, seller account creation, listing build, inbound shipment and an auto campaign into dated milestones with go/no-go checks at each stage. Designed to validate the end-to-end process and the seller's confidence, explicitly separated from long-term product selection.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的月销售额、评论数、重量、毛利率、订货件数与各阶段天数都是经验值；本 Skill 只保留顺序与检查项，数值按当前费率与本账户情况校准。
- 试跑期“定价低于竞品”和“自动广告日预算固定”是简化策略，可能造成亏损或价格锚定；试跑目标是走通流程，仍需设亏损上限与停止条件。
- 开户所需主体类型、资料与审核时长随平台政策变化；以当前注册页面要求为准，不按来源描述的步骤硬套。
- 试跑数据样本小，不能用于推断长期需求或广告效果；长期产品决策另走完整选品流程。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace 与案例 ASIN 的明确时间范围
- 销量、评论、价格、促销、变体和上架时间线
- 关键词自然/广告可见度、品牌与站外流量代理证据
- 可复核来源、数据口径、缺失项和替代解释

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 第 1 阶段（开户准备）：办理注册卖家所需的企业主体、可付外币的信用卡与收款账户；按当前开店要求核对法人、地址与营业执照信息一致，避免审核往返吃掉时间窗。
2. 第 2 阶段（限时选品，约 3 天）：用产品库工具按放宽的条件筛选——有稳定月销、评论数少、体积小重量轻、当前费率下有正毛利；做 5 个候选的对比表，并确认同类目至少还有若干产品达到同样销量，说明需求不是单品偶然；门槛按本账户资金与风险承受校准。
3. 第 3 阶段（供应商与试单）：只要现货、不谈定制，按小批量询价并说明试单成功后会加量，件数以试跑售罄周期倒推；用官方收益计算器按当前费率算毛利率，低于本账户设定的最低线就换品。
4. 第 4 阶段（开户与上架）：提交卖家账号审核的同时准备 Listing：参考竞品文案结构、用关键词工具提取核心词、请供应商提供原图再做精修；无品牌时按当前流程申请 GTIN 豁免以通用品牌上架。
5. 第 5 阶段（发货）：创建货件计划、填写箱数与每箱件数、把箱标交供应商贴箱；因为选的是小件轻货，可走空派缩短到仓时间；记录预计到仓日期作为上架日。
6. 第 6 阶段（上架出单）：到仓后开自动广告，日预算按本账户可承受额度设定；定价可略低于同类竞品作为试跑期策略；每周下载搜索词报告，否定无关词与只花钱不出单的词。
7. 复盘：把试跑全过程的费用、毛利、售罄天数、转化率与卡点记录成一页；无论盈亏，都以此决定下一轮是否按更严格标准做长期选品，而不是直接放大本品备货。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取候选产品的估算月销、评论数与体积重量等第三方代理数据用于限时筛选。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 30 天节点计划表（阶段、动作、截止、通过条件）
- 5 个候选对比表与最终试单品选择理由
- 试单毛利测算（按当前费率与供应商报价）
- 上架与发货核对清单
- 试跑复盘一页纸（费用、毛利、售罄、卡点）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
