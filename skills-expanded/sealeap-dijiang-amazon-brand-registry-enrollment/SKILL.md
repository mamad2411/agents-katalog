---
name: sealeap-dijiang-amazon-brand-registry-enrollment
description: "Verify trademark eligibility, complete Amazon Brand Registry enrollment end to end (including the accelerator path when no live trademark exists yet), then inventory the resulting brand tools so the team knows which levers exist for protection, content, and post-enrollment analytics. Use for 怎么做品牌备案、没有商标能不能先备案、备案后能用哪些工具、备案账号权限怎么设置. Do not use to claim brand protection benefits before enrollment is actually approved."
---

# Amazon 品牌备案申请与权益盘点

## 目标

Verify trademark eligibility, complete Amazon Brand Registry enrollment end to end (including the accelerator path when no live trademark exists yet), then inventory the resulting brand tools so the team knows which levers exist for protection, content, and post-enrollment analytics.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 商标申请到生效的周期、备案审批时长、以及相关代理服务费用均随地区与代理机构变化，来源中的具体天数与金额仅供参考，需以官方与代理机构当前信息为准。
- 平台后台某些“关键词排名可提升某百分比”一类的官方建议，来源认为部分有效、部分未必适用，应视为待验证假设，用自身账户测试结果判断是否采纳。
- “按搜索词查看当前转化最好的商品”一类报表容易被误读——高转化可能来自站外自带流量等因素，而非该商品页面本身优化得好，不能直接照抄其页面结构。
- 备案资格核验主要基于商标数据库等公开信息，属于初筛性质，正式的商标法律状态与是否存在冲突仍需以官方受理结果和必要时的专业代理意见为准。

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

1. 核实是否已有覆盖目标经营主体、且状态为“已注册生效”（非申请中）的商标，可通过官方商标数据库按商标文字自助查询注册号与状态，查不到注册号时不要凭印象直接去申请备案。
2. 若尚无生效商标，评估是自行委托代理机构申请，还是走平台提供的“预先核验+推荐律所”加速通道；两条路径都需要先拿到商标受理/注册号才能真正提交备案申请，加速通道能提前锁定备案资格，但不能跳过商标本身的审查周期。
3. 备案申请中使用的登录账号，应确认是店铺后台里的最高权限管理员账号（可在用户权限设置里核对），避免用普通子账号登录导致备案身份与店铺账号后续关联出问题。
4. 申请表单中的品牌名称必须与商标注册文本完全一致，若两者不一致（如商标注册的是完整公司名而非店铺常用品牌名），应先解决命名一致性问题（必要时重新申请更贴合经营品牌名的商标）而不是强行提交不一致的申请。
5. 备案通过后，逐项核对并启用可用权益：防伪追溯类工具、专属侵权举报与问题升级通道、加强型图文内容、品牌旗舰店、品牌广告、跨渠道广告效果归因、以及品牌分析报表，按经营优先级排期启用而非一次性全开。
6. 备案后定期通过品牌后台的评论监控、关键词排名参考、新品优化提示等功能做例行盘点，把工具给出的建议标记为“待验证假设”，用自身账户数据决定是否采纳，而不是照单全收。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：用于核验品牌名称对应商标的注册号与当前法律状态（如是否在主注册簿、是否生效），通过商标类公开数据源核对，属于备案资格的初筛依据，不构成正式法律意见。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 商标资格核验记录
- 备案申请材料与账号权限确认单
- 备案后权益启用优先级清单
- 品牌后台例行盘点模板
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
