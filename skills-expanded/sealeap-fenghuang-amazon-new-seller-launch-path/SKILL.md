---
name: sealeap-fenghuang-amazon-new-seller-launch-path
description: "Sequence a first Amazon FBA launch on the US marketplace into gated stages—seller plan choice, keyword-gap product discovery, supplier sourcing, listing creation, and launch-week sales focus—each with the evidence required before moving on. Defaults to US but flags the marketplace-specific fee and policy checks needed elsewhere. Use for 新手怎么开始做亚马逊、开户选哪个计划、从零到上架流程、第一款产品怎么落地、启动顺序检查. Do not use to replace category-specific compliance review or to promise ranking outcomes."
---

# Amazon 新卖家开户到首发启动路径

## 目标

Sequence a first Amazon FBA launch on the US marketplace into gated stages—seller plan choice, keyword-gap product discovery, supplier sourcing, listing creation, and launch-week sales focus—each with the evidence required before moving on. Defaults to US but flags the marketplace-specific fee and policy checks needed elsewhere.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源以「Amazon 是搜索引擎、头部位置拿走绝大多数销量」为出发点，可作经验假设，但位置与销量的分布要用当前类目数据观察，不当作固定规律。
- 「搜索量高且无对应产品」可能是需求真空，也可能是该品无法合规销售或搜索词本身有歧义；必须交叉验证。
- 「首发拿到大量订单就会被推上排名」是来源对平台机制的解释，只能作待验证假设；不采用任何刷单或操纵评论的手段。
- 各站点账户计划费用、佣金与品类政策随时间变化，一律以当前官方页面为准。

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

1. 确认 marketplace（默认 US）与经营主体资料；比较按件收费计划与月费计划时，用预计月销量乘以按件费与月费对照，一律以当前站点费用表为准，不套用来源年份的价格。
2. 用关键词工具类别做需求缺口扫描：找搜索量稳定、但搜索结果里缺少精准匹配产品的短语；把「有需求无供给」写成假设，再用前台搜索结果与近似品销量估算验证，而不是只看工具给出的机会评分。
3. 按品类决定供应链路径：消耗品、入口类等合规敏感品优先考虑本土制造商数据库，通用品可走海外 B2B 采购平台；记录样品费、起订量、交期与是否能协助直发入仓。
4. 在货到之前先建好 Listing 骨架（标题、主图、副图、五点、描述），并确认品类是否需要审核或资质；Listing 存在是后续品牌备案、广告与入仓货件的前提。
5. 把首发周设为「集中出单」阶段：提前准备广告、站外触达与充足库存，让早期销售与转化数据尽量集中；具体节奏以当前账户数据校准。
6. 为每个阶段设停止条件：需求验证不通过则回到缺口扫描；样品不合格或交期超出资金承受范围则换供应商；上架审核未通过不得先发货入仓。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取候选短语的搜索需求与前台搜索结果供给情况的代理观测。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 启动阶段清单与门槛
- 计划选择对比表
- 需求缺口候选表
- 供应链路径记录
- 首发周准备检查表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
