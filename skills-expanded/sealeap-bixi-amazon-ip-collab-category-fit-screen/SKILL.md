---
name: sealeap-bixi-amazon-ip-collab-category-fit-screen
description: "Screen whether a product category fits an IP-collaboration or emotional-premium strategy, and if so which licensing tier and limited-release mechanics to use, based on evidence about the target buyer's purchase motivation and the product's shareability rather than assumed IP heat. Use for 判断产品适不适合做IP联名、该选头部IP还是腰部或区域性IP、限量编号发售怎么设计、情绪溢价空间怎么评估. Do not use to sign or execute any IP licensing agreement without legal and rights-holder verification."
---

# Amazon IP联名品类机会评估

## 目标

Screen whether a product category fits an IP-collaboration or emotional-premium strategy, and if so which licensing tier and limited-release mechanics to use, based on evidence about the target buyer's purchase motivation and the product's shareability rather than assumed IP heat.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 海外消费者对中国IP接受度已提升是来源账号的解读性判断，需用自身目标市场的独立数据（搜索热度、社媒声量、同类产品复购率）验证，不能直接当作已验证事实套用。
- 来源中的具体二手溢价倍数、限量数量、单IP营收占比等数字均为个案观察，不能作为自身选品的定价预期或授权成本假设，须以自身测试和实际报价为准。
- 限量抢购、饥饿营销等玩法若涉及虚假库存展示、刷单造势等操纵手段不采用；营销文案与稀缺性宣称需符合平台规则与当地广告合规要求。
- IP授权谈判、独家品类授权等条款具有法律约束力，需由法务或专业代理审核后再签约，不能仅凭案例报道自行判断可行性或标准条款。

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

1. 先判断目标客群的购买动机：用评论、社媒讨论或问卷等证据核实是偏情绪、身份认同或收藏型，还是偏性价比或实用型，后者不宜强行叠加IP，需用自身客群数据验证而非套用来源判断。
2. 盘点候选IP的授权层级与成本：区分头部大IP（授权费高、通常有销售分成、审核严格）与腰部、区域性或小众IP（成本更低、谈判空间更大），按自身预算和目标品类利润率筛选可承受层级，具体费率以实际报价和合同为准。
3. 核对品类是否具备可炫耀的社交属性：产品能否被随身携带、展示、拍照或更换外观；缺乏这类社交货币属性的品类即使贴标也难复制同等溢价，需用自身客评与晒单、退货数据验证而非直接套用来源结论。
4. 若产品本身具备故事性或视觉记忆点，可设计限量编号、平台首发等发售机制；执行前核实目标站点对限量、绝版等营销文案的合规要求，避免夸大库存稀缺性。
5. 先以小批量或单一SKU测试情绪溢价能否转化：对比加贴IP前后的转化率、客单价与退货率，而不是直接大规模投入生产与备货。
6. 设定终止条件：若测试结果显示溢价未能覆盖授权与开发成本，或退货、差评指向货不对板，应停止扩大投入并复盘IP与品类的匹配假设，而不是加大营销投入硬撑。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充目标市场对候选IP与品类的搜索热度、社媒声量与同类联名产品评论证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- IP联名品类适配度评估表
- 候选IP授权层级与成本对比清单
- 限量发售机制设计与合规核对记录
- 小规模测试转化数据复盘报告
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
