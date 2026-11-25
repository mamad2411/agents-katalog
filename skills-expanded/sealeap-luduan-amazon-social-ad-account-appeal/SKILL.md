---
name: sealeap-luduan-amazon-social-ad-account-appeal
description: "Handle a suspended social-media advertising account used for off-Amazon traffic by first separating billing errors from policy enforcement, auditing creatives for misleading or overstated claims, filing the platform's official review request with a factual description of the business, supply source and products, and hardening creatives before relaunch. Does not create replacement accounts or circumvent platform review. Use for 社媒广告账号被封、社媒广告账户被停用怎么申诉、广告审核不通过、账户显示错误是不是被封、站外投放素材合规自查. Do not use to open new accounts after a ban, buy or borrow accounts, or disguise the business entity."
---

# Amazon 站外社媒广告账号受限申诉

## 目标

Handle a suspended social-media advertising account used for off-Amazon traffic by first separating billing errors from policy enforcement, auditing creatives for misleading or overstated claims, filing the platform's official review request with a factual description of the business, supply source and products, and hardening creatives before relaunch. Does not create replacement accounts or circumvent platform review.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源猜测审核人员的地区与政治因素影响解封概率，本 Skill 不采纳任何关于审核者身份的推测；申诉成败只按政策条目与素材事实分析。
- 来源提到用境外公司主体注册广告账号以降低被封概率，属于规避审核的做法，不采用；主体信息必须真实。
- 来源强调被封后不要注册新账号，这与平台规则一致；但来源给出的申诉回复时长是个案，实际时长以平台当前处理为准。
- 站外广告账号问题不影响 Amazon 站内广告，但站外流量中断会影响依赖它的新品计划；评估影响时按站外归因口径单独统计。

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

1. 先核对账户状态来源：在广告平台的账户与账单页面（以当前控制台为准）核对余额、支付方式状态与账户状态提示文字；余额为零或支付失败导致的“账户错误”不是处罚，先充值或更新支付方式再判断。
2. 确认处罚类型与依据：记录状态栏提示的政策条目（误导性信息、侵权、受限品类等）、触发时间与最近一次改动（新建广告、改素材、改支付方式、频繁申诉），作为自查线索。
3. 自查素材：逐条检查标题、描述与图片是否存在夸大或极限用语、产品名称与实际售卖物不一致（如把配件写成主机）、受限品类关键词、与落地页不符的承诺；发现问题先修正或下线，不带着问题素材申诉。
4. 按官方流程提交复核：在账户状态提示处的复核入口（以当前控制台为准）填写申诉，核对字段：账户 ID、涉及的政策条目、经营主体与身份、供货来源、售卖产品类别、已删除或修正的内容、联系方式；正文只陈述事实，不做无关辩解，不重复提交。
5. 记录时间线：申诉提交时间、平台回复时间、结果；恢复后先不做大改动，逐步恢复投放并观察是否再次触发；再次被限时对照最近改动定位诱因。
6. 建立投放前合规检查表（品类、用语、产品描述一致性、落地页一致性）与申诉模板，把每次处罚原因回填到检查表。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 账户状态判定记录（余额/支付/政策处罚）
- 素材合规自查表与修正记录
- 复核申诉正文与字段核对清单
- 申诉时间线与再次触发分析
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
