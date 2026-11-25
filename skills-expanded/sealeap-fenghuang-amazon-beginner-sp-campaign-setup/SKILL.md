---
name: sealeap-fenghuang-amazon-beginner-sp-campaign-setup
description: "Set up a beginner Sponsored Products structure on the US marketplace in five gated steps—auto campaigns bid by targeting group, search-phrase research, manual keyword campaigns, product (ASIN) targeting, and negative keywords—plus a launch-week budget stance with inventory guardrails. Use for 新手怎么开广告、自动广告怎么设、四个匹配组分开出价、手动广告怎么建、ASIN 定向、否词怎么加、首发周广告怎么投. Do not use to mutate live campaigns without approval or to set bids without account CPC data."
---

# Amazon 新手 SP 广告五步搭建

## 目标

Set up a beginner Sponsored Products structure on the US marketplace in five gated steps—auto campaigns bid by targeting group, search-phrase research, manual keyword campaigns, product (ASIN) targeting, and negative keywords—plus a launch-week budget stance with inventory guardrails.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 「新品期平台按短周期滚动评估排名」是来源对算法的解释，只作待验证假设；不据此追加超出承受范围的预算。
- 来源提到的各定向组建议竞价与广告效果数字均为个案，一律以当前账户 CPC、转化率与盈亏平衡 ACOS 校准。
- 来源中的广告软件推荐不采纳；本 Skill 仅描述工具类别。
- 首发周牺牲利润换销量必须设停止线（预算上限、ACOS 上限、库存下限），触线即回退。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、店铺、ASIN/SKU、广告类型和目标
- 同口径的 Campaign、Targeting、Search Term、Placement 与 Advertised Product 报告
- 售价、优惠、COGS、Amazon 费用、退款与目标贡献利润
- 库存、Buy Box、Listing、评论和同期市场事件

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 先确认对象：marketplace（默认 US）、广告 ASIN、Listing 是否可售且有库存、当前盈亏平衡 ACOS；缺任何一项标 NEEDS_EVIDENCE。
2. 建自动广告时不要只填统一默认竞价：按四个定向组（紧密匹配、宽泛匹配、替代品、互补品）分别出价或拆成独立活动，紧密匹配给最高竞价，其余按账户数据校准；来源的建议竞价不作参考值。
3. 做搜索短语研究：从自动广告搜索词报告、关键词工具类别与竞品反查里列出「买家真的会这样搜」的短语，按相关性分档；无关短语直接进否词候选。
4. 建手动关键词活动承接已验证短语，长期利润通常来自手动活动；Sponsored Brands 需要多个 SKU 且偏品牌曝光，Sponsored Display 另议，新手先跑通 SP。
5. 建 ASIN 商品定向活动，让广告出现在可比竞品详情页；选对象时对比价格、评论数与评分，只定向本品有明显优势的竞品。
6. 按固定周期从搜索词报告加否定关键词：有点击无转化且与产品无关的词否掉；观察窗以当前账户样本量决定，不用固定阈值。
7. 首发周可把目标从利润切换为「集中出单」，但必须同步确认库存可支撑：断货会打断早期数据积累；提前与供应商约定补货交期。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充关键词搜索需求与可比竞品 ASIN 的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 广告活动结构表
- 定向组竞价方案
- 搜索短语与否词分档表
- 竞品 ASIN 定向清单
- 首发周预算与停止线
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
