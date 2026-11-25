---
name: sealeap-baxia-amazon-video-verification-readiness
description: "Prepare an Amazon account holder for live video verification by rehearsing authentic operational knowledge and natural on-camera behavior, and by auditing that account details stay synchronized after any ownership or entity change. Use for 视频认证前的资料与仪态准备、法人或主体变更后的账户信息同步核查、认证被拒后的复盘. Do not use to script memorized answers or to coach any form of deception during the interview."
---

# Amazon 视频认证准备清单

## 目标

Prepare an Amazon account holder for live video verification by rehearsing authentic operational knowledge and natural on-camera behavior, and by auditing that account details stay synchronized after any ownership or entity change.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 审核员关注的具体行为信号（眼神、语速、停顿）是来源经验总结，不同批次审核标准可能调整，只作为待验证的参考清单，不是固定判分规则。
- 账户信息同步的具体必填项以当前官方认证要求为准，执行前需在后台复核最新清单，不依赖历史经验判断是否齐全。
- 本流程不涉及也不支持任何形式的资料造假或找人代答，这类做法一律不采用。

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

1. 认证前梳理真实经营痕迹（供应商沟通记录、转账与收款流水、实际操作截图），确认本人能随时调取并说明来源，而不是临时准备话术。
2. 用自我录像方式模拟问答，检查是否存在过度流畅、眼神游移、长时间低头看稿等容易被判定为背题的行为，反复修正到自然表达。
3. 核对光线、收音、拍摄范围与在场人员，确认全程只有受访本人入镜，环境中不出现提示性材料。
4. 若近期发生法人、主体或经营权变更，逐项核对密码、收款卡、绑定手机号等账户信息是否已同步更新，避免因信息不一致触发怀疑。
5. 认证中被追问细节时如实说明并允许合理停顿，不强行编造无法支撑的答案；遇到确实不了解的历史信息，直接说明由何人经办。
6. 认证结束后记录被追问的问题类型与结果，用于更新下一次的准备清单。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 真实经营痕迹核对清单
- 认证仪态自查记录
- 账户信息同步核对表
- 认证复盘与问题记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
