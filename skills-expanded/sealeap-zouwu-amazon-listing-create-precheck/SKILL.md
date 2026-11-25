---
name: sealeap-zouwu-amazon-listing-create-precheck
description: "Walk through creating a brand-new Amazon listing in Seller Central field by field: confirm the category path, title structure, bullet coverage, attribute fields, variation theme, SKU naming, product IDs, pricing and fulfillment settings before submission, then read back the live listing to verify. Field names follow whatever the current console shows; no proprietary ranking claims. Use for 新建 Listing、上架第一个产品、添加商品字段怎么填、变体主题选择、外部产品 ID 和 UPC、Search Terms 填什么、上架后怎么检查. Do not use to create offers by attaching to another seller's detail page, or to submit a listing before the user confirms product facts and compliance fields."
---

# Amazon Listing 新建字段预检

## 目标

Walk through creating a brand-new Amazon listing in Seller Central field by field: confirm the category path, title structure, bullet coverage, attribute fields, variation theme, SKU naming, product IDs, pricing and fulfillment settings before submission, then read back the live listing to verify. Field names follow whatever the current console shows; no proprietary ranking claims.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 标题结构与五点信息类型是来源经验的组织方式，不是平台排名规则；标题长度、禁用词与必填字段以当前站点类目模板和政策为准。
- 前台可见图片张数、可上传上限、提交后生效时长等界面数值随站点与版本变化，一律以当前控制台为准，不作固定规律。
- 控制台的 AI 生成文案功能效果是来源的主观判断，只能当草稿工具；产品事实与合规声明必须人工核对。
- 不采用在他人商品页上直接添加报价来替代新建 Listing；跟卖需单独评估品牌保护与授权风险。

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

1. 先在当前控制台确认入口：通过「添加商品」搜索产品名后，区分「在已有商品上添加报价」与「创建新的商品信息」，本 Skill 只走新建路径；系统自动识别的商品类型要与目标类目核对，识别偏差时手动改选。
2. 用目标站点的标准商品页地址（只保留含 ASIN 的 dp 路径）核对可比竞品的真实类目节点，避免从活动或搜索入口进入时看到的类目偏差；记录选定的类目节点与产品类型关键字。
3. 标题按「品牌 + 核心品类词 + 关键属性/材质 + 卖点 + 使用或兼容场景 + 变体值」的结构起草，每一段回指已调研的关键词与产品事实；五点按优势、功能、外观、用途、场景、质保、包含物、售后等信息类型覆盖，不与标题重复。
4. 逐项核对属性字段：品牌（未备案时按当前控制台的无品牌选项处理）、型号、制造商、Search Terms（只放标题和五点放不下的词）、专有特征、装数、动力/电压/接口/兼容设备、商品尺寸；可选字段能填尽填，并记录每个字段的事实来源。
5. 变体与 SKU：先确定变体主题（如颜色/尺寸）再逐个新建子体，SKU 用统一命名规则；无品牌备案或 GTIN 豁免时每个子体需填写来源可核验的外部产品 ID（UPC/EAN）。
6. 图片、价格与配送：主图与副图按当前站点允许数量安排并把最重要的图放在前列，售价与划线价（不含税价目表）分开填写，首次可先选卖家自配送再转 FBA；包装尺寸、原产地、保修、电池与危险品字段按实际填写，不留必填空项。
7. 提交后等待生效，再从库存管理和前台商品页回读：类目、标题、变体关系、图片顺序、价格与配送方式是否与草案一致，差异记入待修项。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取同购买意图竞品 Listing 的标题结构、五点信息类型与属性字段的公开页面观测，以及 Search Terms 关键词候选的代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- Listing 字段填写核对表
- 标题与五点草案（含关键词回指）
- 变体、SKU 与产品 ID 清单
- 发布后回读差异清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
