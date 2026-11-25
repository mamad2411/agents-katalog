---
name: sealeap-zouwu-amazon-brand-registry-enroll
description: "Prepare and submit an Amazon Brand Registry enrollment once a trademark filing receipt arrives: verify brand name, logo image, serial or registration number, trademark status, product images showing the permanently affixed brand, then complete the verification-code loop through the trademark correspondent and the Brand Registry case log. Follows the current registry form. Use for 品牌备案流程、商标备案资料准备、序列号在哪找、待定和已注册选哪个、备案图片要求、备案验证码怎么回复. Do not use to fabricate brand-affixed product photos or to enroll trademarks the account does not own."
---

# Amazon 品牌备案资料预检与验证闭环

## 目标

Prepare and submit an Amazon Brand Registry enrollment once a trademark filing receipt arrives: verify brand name, logo image, serial or registration number, trademark status, product images showing the permanently affixed brand, then complete the verification-code loop through the trademark correspondent and the Brand Registry case log. Follows the current registry form.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 审核耗时（来源约数个工作日）与商标由待定转注册的周期随商标局和站点而异，不作固定预期。
- 来源提到用定制印字或印章临时制作带标图片；本 Skill 不采用任何与实际销售产品不符的补拍方式，备案图片必须来自真实产品与包装。
- 备案表单字段与验证方式随平台更新，以当前品牌注册页面为准。

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

1. 确认前提：商标申请已受理并拿到含序列号或注册号的回执；从回执中定位序列号、提交日期与申请人信息，核对与店铺主体一致。
2. 准备资料：品牌名称与商标文字完全一致；品牌徽标用白底清晰图；按商标所在国家选择商标局，商标状态按实际选待定或已注册，文字商标或设计商标按实际类型选择。
3. 商品图片必须是真实产品或包装上永久附着品牌标识的多角度实拍图（含包装），不用贴纸、后期合成或临时印制；代表性 ASIN 可留空。
4. 填写销售身份与站点后提交，记录 Case ID；进入等待期时不重复提交。
5. 收到验证码通知后，联系商标申请时登记的联系人邮箱（通常是律师或服务商）取得验证码，在品牌注册的支持或问题日志中按要求格式回复。
6. 回读结果：备案通过后确认品牌已出现在账户品牌列表，A+、品牌分析等功能已解锁；未通过时按拒绝原因补充资料。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 品牌备案资料核对表
- 带标产品图片清单
- 提交与验证码回复记录
- 备案结果与功能解锁回读
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
