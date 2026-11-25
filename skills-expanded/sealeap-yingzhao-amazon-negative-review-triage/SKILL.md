---
name: sealeap-yingzhao-amazon-negative-review-triage
description: "Triage negative reviews on a listing by visibility and severity, resolve underlying order problems through Amazon's official brand review-contact tool and buyer-seller messaging within policy, report only reviews that breach community guidelines, and route recurring complaint themes into product and listing fixes. It never solicits review removal, buys reviews or hides ratings by re-listing ASINs. Use for 差评怎么处理、带图差评在首页、评分掉了怎么办、品牌备案联系差评买家、什么样的差评可以举报、子 ASIN 评分拆分、差评复盘. Do not use to request or trade for review removal, to buy reviews, or to recreate ASINs in order to reset ratings."
---

# Amazon 差评分级处理与合规申诉

## 目标

Triage negative reviews on a listing by visibility and severity, resolve underlying order problems through Amazon's official brand review-contact tool and buyer-seller messaging within policy, report only reviews that breach community guidelines, and route recurring complaint themes into product and listing fixes. It never solicits review removal, buys reviews or hides ratings by re-listing ASINs.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “评分达到某个小数位就会显示更高星级”是来源对前台展示的观察；星级取整与评分加权规则由平台当期决定，按当前前台核对，不作为固定阈值。
- 来源提到的付费删差评、付费带图好评、“首页无差评”服务以及每批货换新子 ASIN 再删除低分旧 ASIN 的做法，均属评论操纵或重复 Listing 违规，不采用。
- 来源在买家满意后请求其删除差评，这违反平台沟通政策，不采用；联系买家只能解决订单问题，评论是否修改由买家自行决定。
- 举报只对违反社区准则的评论有效，结果由平台判定；本 Skill 不承诺删除率，处理进度以后台 case 记录为准。

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

1. 建立差评台账：记录当前评分、星级显示、各星级数量，逐条登记 1–3 星评论的日期、主题、是否带图或视频、是否出现在详情页首屏、对应子 ASIN/SKU；评分对点击与转化的影响以自家同期数据观察，不套用固定分数线。
2. 按可见度与严重度排序：带图/视频差评与首屏可见的差评优先，其次是内容负面强度高的；同时按根因归类（质量缺陷、描述与预期不符、尺寸/兼容问题、物流与包装、服务），形成处理顺序。
3. 逐条做合规判定：对照当前评论社区准则检查是否含辱骂、敏感内容、与产品无关、竞争者或利益相关方发表等可举报情形；符合的通过评论旁的举报入口或开 case 提交，附截图与说明；真实但负面的评论不举报，进入售后与改进流程。
4. 对品牌备案账户，用品牌后台的买家评论工具联系差评买家，选择客户支持路径而非默认退款，沟通只限于了解问题与提供解决方案（补发、换货、退款）；找不到对应评论时，用评论者显示名、评论时间与 SKU 在订单管理中匹配订单后通过买卖家消息处理售后；所有消息遵守当前沟通政策，不请求修改或删除评论，不以补偿换评论。
5. 拆分子 ASIN 评分：在变体家族中记录每个子体的独立评分与差评集中度，识别拖低整体评分的子体；根因属产品的进入改款或停售评估，属描述的立即修正 Listing 与图片，而不是删除或重建 ASIN 抹掉历史。
6. 每周回读台账：更新评分与星级显示、举报结果、售后处理率与买家回复率，把重复出现的差评主题写进产品改进与 Listing 修改清单，并记录哪些动作带来了评分变化。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 差评台账（评分、星级显示、逐条主题、可见度、子 ASIN 归属）
- 处理优先级与根因分类表
- 举报清单与 case 记录（依据条款、证据、结果）
- 售后联系记录（渠道、问题、解决方案、政策合规检查）
- 产品与 Listing 改进清单及评分回读
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
