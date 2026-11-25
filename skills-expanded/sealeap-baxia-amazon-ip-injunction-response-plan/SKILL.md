---
name: sealeap-baxia-amazon-ip-injunction-response-plan
description: "Guide a seller through preparing for and responding to a U.S. intellectual-property injunction against an Amazon account, from routine infringement risk screening and evidence retention to engaging counsel and pursuing procedural relief once funds are frozen. Use for 知产诉讼禁令预警、账户资金被冻结应急、上市前侵权风险自查、储备海外律师资源. Do not use to draft legal filings or make litigation strategy decisions without a licensed attorney in the jurisdiction."
---

# Amazon 知产禁令风险应对预案

## 目标

Guide a seller through preparing for and responding to a U.S. intellectual-property injunction against an Amazon account, from routine infringement risk screening and evidence retention to engaging counsel and pursuing procedural relief once funds are frozen.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 个案中通过重审动议等程序性救济翻盘的结果与具体律师策略强相关，不能作为可复制的胜诉方法，只作为'禁令不必然等于终局'的待验证参考。
- 资金冻结比例、禁令期限与担保金要求因个案与法院裁量而异，不写入固定数值，以当次案件的法院文书为准。
- 跨境知产诉讼涉及境外司法程序，任何策略性判断都必须由当地执业律师确认，本流程仅覆盖卖家自身可控的预防与配合环节。

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

1. 梳理近期上架新品的外观、包装与功能描述，对照可能存在的专利、商标、版权风险做常态化自查，标记待验证的高风险项。
2. 建立可随时调取的交易与沟通证据包（供应商往来、设计来源说明、真实成交记录），按站点与经营主体分类留存。
3. 提前筛选并储备至少一支熟悉平台知产诉讼程序的当地律师团队，明确联系方式与响应时效，不等禁令发生后再现找。
4. 若收到禁令或资金冻结通知，第一时间联系律师并核实冻结范围、可用现金流与业务连续性影响，不与运营方单独私下处理。
5. 配合律师压缩争议焦点、复核对方证据链缺口，评估是否存在申请重新审理或其他程序性救济的空间，作为常规抗辩之外的补充路径。
6. 禁令解除或案件了结后复盘风险来源，更新合规自查清单与证据留存流程，把本次暴露的缺口补齐。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 侵权风险自查清单
- 证据留存台账
- 律师资源储备表
- 禁令应急响应流程
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
