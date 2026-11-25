---
name: sealeap-chongming-amazon-new-listing-build-checklist
description: "Create a new-product listing as a pre-order gate: build a test listing to surface category restrictions and editability issues before committing inventory, then fill category, product identifier, title, brand, variations, offer, images, bullets, description and backend search terms following top-competitor structure and current listing policies. Every field is checked against the marketplace's current rules rather than legacy workarounds. Use for 新品 Listing 怎么建、上架前预检、类目选哪个、标题关键词怎么排、五点怎么写、后台搜索词怎么填、订货前先建链接. Do not use to submit or edit a live listing without the seller confirming brand, GTIN source and field values."
---

# Amazon 新品 Listing 创建与预检

## 目标

Create a new-product listing as a pre-order gate: build a test listing to surface category restrictions and editability issues before committing inventory, then fill category, product identifier, title, brand, variations, offer, images, bullets, description and backend search terms following top-competitor structure and current listing policies. Every field is checked against the marketplace's current rules rather than legacy workarounds.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源推荐从转售渠道或电商平台购买低价 UPC，这与当前 GTIN 政策冲突，本 Skill 不采用；编码来源以 GS1 或 GTIN 豁免为准。
- 来源建议把“价格”字段填得远高于实际售价以便日后涨价不丢购物车，这可能违反参考价规定且属未验证假设，不采用；涨价影响以实际购物车观测为准。
- 来源认为供应商图片“没人投诉就能用”，存在版权与品牌投诉风险，不采用；图片需自有版权或书面授权。
- 来源的开 case 申请品牌白名单、描述里用 HTML 标签等操作对应旧版后台；“五点比描述重要”“品牌名放标题末尾”是经验判断，以当前字段规范与本账户转化数据校准。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、产品事实和当前 Listing
- 同购买意图可比竞品、价格、评论、图片和销量
- Search Term、Placement、CTR、CVR、订单、退货和利润
- VOC、Q&A、退货原因与任何页面或广告变更日志

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 在联系供应商下单之前先创建 Listing：若创建后出现类目审批、证书要求，或数日内 Listing 变为不可编辑/被限制，先决定是否解决再下单；下单前再回读一次 Listing 的可编辑状态。
2. 选择“添加未在售的新商品”而非匹配已有 ASIN；类目按同类头部竞品详情页展示的类目路径选择（取 3 个头部竞品对照），不自行猜类目。
3. 产品编码按当前 GTIN 政策处理：使用 GS1 来源的 UPC/EAN，或符合条件时申请 GTIN 豁免；每个变体子体各需一枚编码；品牌字段若被拒，按当前品牌名称批准流程提交带品牌标识的产品/包装证据。
4. 标题：先列本品主关键词并按搜索量代理数据从高到低排列，写成目标市场读者能读通的一句；品牌名位置按类目头部竞品的通行写法与当前标题规范决定，作为可测试变量而非固定规则。
5. 报价与设置：选 FBA、全新；售价与参考价字段按当前参考价政策填写真实可支撑的数值；最大订单数量、礼品选项按产品属性决定并记录理由。
6. 图片与五点：首图白底，后续按头部竞品的图片类型组合（模特、场景、图文说明）准备且版权自有或有授权；五点先写功能事实再写使用体验，把关键词自然嵌入，避免只罗列尺寸；描述按当前站点允许的格式书写（多数站点不再渲染 HTML 标签）。
7. 后台搜索词：只放标题与五点未覆盖的词，不重复、不加标点、不超过当前字节上限；提交后回读各字段是否生效，并记录首版字段值以便后续 A/B。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取同类头部竞品的类目路径、标题结构、图片类型与关键词搜索量代理数据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 订货前 Listing 可编辑性与限制排查记录
- 类目路径与产品编码来源记录（GS1/豁免）
- 标题关键词序列与五点/描述草案
- 图片清单（类型组合与版权来源）
- 后台搜索词与提交后回读核对表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
