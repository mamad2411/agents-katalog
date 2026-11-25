---
name: sealeap-baxia-amazon-ai-agent-deployment-boundary
description: "Gate adoption of self-hosted open-source AI agent tooling for back-office Amazon operations behind a public-exposure security check and a task-complexity boundary that currently excludes advertising and product-selection decisions. Use for 自建AI智能体自动化前的安全自查、判断哪些环节适合当前交给智能体、智能体使用边界评审. Do not use to hand advertising bid changes, campaign creation, or product-selection decisions to an unsupervised agent."
---

# Amazon AI智能体接入边界

## 目标

Gate adoption of self-hosted open-source AI agent tooling for back-office Amazon operations behind a public-exposure security check and a task-complexity boundary that currently excludes advertising and product-selection decisions.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 开源智能体工具当前适合的任务边界是行业阶段性观察，会随工具成熟度和自身验证结果推移，需要定期重新评估而非一次性定论。
- 公网暴露实例数量等安全态势数据会持续变化，以官方安全预警发布渠道的最新信息为准，不使用过去的统计数字。
- 凡涉及自动登录、批量操作店铺后台的智能体配置，需先对照账号关联与安全合规要求评估风险，不确定时保持人工操作。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、产品事实、品牌语气和当前政策约束
- 已授权的 Listing、关键词、评论/VOC、图片和竞品证据
- 每项数据的来源、时间、站点、样本和限制
- 人工审核人、发布边界和不可生成的声明或视觉特征

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 部署前确认服务器与实例的访问控制、默认账号密码是否已修改，避免以默认或不当配置暴露在公网。
2. 按任务盘点候选自动化场景，优先挑选高频、规则清晰、出错影响小的后台环节，例如物流轨迹查询回写、多表数据同步。
3. 对涉及外部账号或密钥的自动化任务，评估凭证存储与权限范围是否最小化，出错时的影响半径是否可控。
4. 对广告竞价、活动创建、选品决策等核心且难以回退的业务，暂不交给智能体独立执行，仅允许其做信息收集类的辅助拆解。
5. 小范围试运行后统计执行准确率、异常处理情况与人工介入频率，达不到预期时收窄自动化范围而不是扩大。
6. 定期复核官方或行业发布的相关安全预警，出现新的暴露或漏洞提示时立即检查自身实例是否受影响。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 部署前安全自查清单
- 自动化场景分级清单
- 试运行准确率记录
- 使用边界复核记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
