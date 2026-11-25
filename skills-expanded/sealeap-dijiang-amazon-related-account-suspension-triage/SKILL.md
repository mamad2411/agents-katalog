---
name: sealeap-dijiang-amazon-related-account-suspension-triage
description: "When a store is suspended for being linked to another account, identify which shared identifier the platform flagged, such as name, phone, payment method, device, or network, determine whether the root-cause account is known or resolvable, and assemble a structured, evidence-based appeal rather than resubmitting generic explanations. Use for 账号被关联暂停怎么办、收到关联通知先查什么、申诉材料怎么准备. Do not use this to design ways of running multiple accounts undetected — only for resolving and preventing genuine, compliant linkage incidents."
---

# Amazon 关联暂停排查与申诉

## 目标

When a store is suspended for being linked to another account, identify which shared identifier the platform flagged, such as name, phone, payment method, device, or network, determine whether the root-cause account is known or resolvable, and assemble a structured, evidence-based appeal rather than resubmitting generic explanations.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 具体的处理时长、资金冻结周期与所需材料以官方当次答复为准，来源中的经验时间仅供参考，不构成承诺。
- 判断哪些信息会导致关联是创作者基于自身经历的推测，并非官方公开文档确认的完整清单，实际判定逻辑以平台官方说明为准。
- 本方法仅用于解决与预防真实合规的关联暂停问题，不用于设计规避平台关联检测的操作方式，多账号经营需按平台当前政策走合规申请与身份隔离，而非技术手段掩盖关联。
- 涉及付费的第三方账号申诉代办机构属于一类可选服务，选择前应独立核实其资质与口碑，不代表任何特定机构的背书，且不应在申诉过程中向第三方提供完整账号密码等敏感凭证而不设风控。

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

1. 收到通知后先逐字核对通知内容，确认具体触发原因的表述，通常会提示与另一账号存在关联并给出该关联账号的部分信息片段，把原文完整留档作为后续申诉的对照依据。
2. 判断关联可能来自哪一类共享身份信息：注册人信息、联系电话、收款或支付方式，或登录时的网络与设备环境，逐项对照自己名下是否确实存在另一个账号使用了相同或相近信息。
3. 确认该关联账号是否为自己知情且合规持有的账号：如果是遗忘或早年注册后未使用的账号，先查明其当前状态；如果确实是他人或历史遗留造成的误关联，收集能证明两者无实际关联的证据。
4. 判断问题的根源在哪个账号：通常是先有一个账号被处罚，才连带另一账号被关联暂停，优先解决根源账号的问题，根源解决后关联账号的申诉才有明确依据。
5. 撰写申诉时按问题根源说明、已采取的纠正措施、后续预防措施三段式组织内容，并逐条对应通知里提到的具体触发信息，避免使用笼统套话。
6. 通过官方申诉入口提交并记录提交时间，等待官方回复期间不要频繁重复提交相同内容，如需补充材料按官方要求逐次追加而不是整篇重写。
7. 问题解决后检查名下所有账号的注册信息、支付方式与登录环境是否存在不必要的交叉重叠，如需保留多个合规账号，按当前平台的多账号相关规定做好身份信息隔离，减少未来被误关联的概率。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 暂停通知原文与关联信息比对记录
- 根源账号与关联账号问题定位结论
- 结构化申诉材料（问题根源/纠正措施/预防措施）
- 账号身份信息隔离自检清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
