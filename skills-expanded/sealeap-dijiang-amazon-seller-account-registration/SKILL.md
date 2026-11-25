---
name: sealeap-dijiang-amazon-seller-account-registration
description: "Prepare Amazon seller account registration inputs (legal identity naming, professional email, cross-border-capable payment card, and business documentation) and cross-check them against common first-time rejection and suspension causes before submitting, aligning every choice with Amazon's current account and relationship-disclosure policies. Use for 注册亚马逊卖家账号要准备什么、注册资料填写要注意什么、为什么开店被拒、多账号关联怎么避免. Do not use to open a second seller account without disclosing the relationship exactly as Amazon's current related-accounts policy requires."
---

# Amazon 卖家账号注册材料清单

## 目标

Prepare Amazon seller account registration inputs (legal identity naming, professional email, cross-border-capable payment card, and business documentation) and cross-check them against common first-time rejection and suspension causes before submitting, aligning every choice with Amazon's current account and relationship-disclosure policies.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 不同经营方案（个人 vs 专业）的具体月费/费率、以及注册被拒后是否会退还已收费用，均以官方当前公示信息为准，来源中的具体金额与退费说法未经证实，不作为可依赖的事实。
- “信用卡必须是某个特定卡组织”的具体说法为来源经验总结，实际受理范围应以官方当前收款说明为准，只需确认满足“可跨境扣款”这一核心要求即可，不必拘泥于单一卡组织。
- 多账号关联的判定规则与允许条件由平台政策决定且可能调整，任何“如何避免被判定关联”的操作都应以官方当前关联账号政策为准，本条目仅从材料一致性与如实申报角度降低无意关联的风险，不提供规避审核的方法。
- 注册资料的地域/身份合规要求可能因经营主体所在地不同而有差异，涉及具体司法辖区要求时应以官方当前政策或专业顾问意见为准。

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

1. 先完成产品与经营计划的基本判断（打算卖什么、大致什么时候能上架）再着手注册店铺，避免店铺开通后长期空置却持续产生月费/维护成本。
2. 姓名类字段按本人真实法定身份填写（有护照等官方证件对应的英文名用英文名，没有的用中文姓名的规范拼音），不要临时编造一个没有任何证件对应的英文名，以免后续身份核实材料对不上。
3. 注册邮箱使用与经营主体匹配、长期可控、能及时查收的邮箱（优先企业域名邮箱而非个人免费邮箱），因为该邮箱后续会承担账户安全验证与找回的唯一联系入口。
4. 确认支付卡类型：需使用能跨境扣款、受理外币交易的信用卡，不能用不支持境外扣款的借记卡/储蓄卡类产品，否则后续月费、广告费等扣款失败可能直接影响账户状态；具体受理卡组织与规则以官方当前要求为准。
5. 以公司主体注册时，逐项核对经营地址、联系电话、统一社会信用代码等资料与官方证件完全一致，避免因资料不一致触发人工审核延迟或被要求补件。
6. 涉及是否已运营其他账号、是否与其他店铺/主体存在关联关系等问题时如实申报，并遵循平台当前的关联账号披露政策；不同店铺之间应避免共用同一邮箱、电话、收款卡等标识信息，除非按官方要求完成了合规的关联披露。
7. 提交后如遇补充材料或审核延迟，按要求逐项补齐，材料真实准确是最终通过的前提，账号通过审核只是长期经营的第一步，后续仍需持续学习平台规则。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 身份与联系方式材料清单
- 邮箱与支付卡合规核对结果
- 公司资料一致性核对表
- 关联关系如实申报记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
