---
name: sealeap-dijiang-amazon-1688-sourcing-translation-bridge
description: "Bridge the language gap on a Chinese-domestic B2B sourcing platform by translating search terms into Chinese before searching, since homepage auto-translate can be unreliable, and escalate manufacturer contact through in-site chat, messaging apps, and a dedicated desktop IM client, reaching out to multiple manufacturers in parallel rather than one at a time. Use for 内销批发平台看不懂中文怎么搜、联系不上工厂怎么办、内销平台和外贸平台比价. Do not use to skip verifying specs, certifications, or sample quality just because a manufacturer responded quickly."
---

# Amazon 1688跨语言寻源联系路径

## 目标

Bridge the language gap on a Chinese-domestic B2B sourcing platform by translating search terms into Chinese before searching, since homepage auto-translate can be unreliable, and escalate manufacturer contact through in-site chat, messaging apps, and a dedicated desktop IM client, reaching out to multiple manufacturers in parallel rather than one at a time.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 平台自带翻译与检索行为可能随版本更新变化，实际体验以当次操作为准，不代表长期稳定如此。
- 未在其他外贸平台出现是较弱的独家性信号，可能只是尚未开通对外店铺，需向供应商直接求证，不能作为唯一判断依据。
- 涉及账号注册、即时通讯工具安装等操作，只从官方渠道下载客户端，避免安装来源不明的软件。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、类目、价格带、上架时间与运营模式
- 候选品与同购买意图可比样本的销量、评论、价格和上架时间
- 关键词需求、历史趋势、广告依赖、同款密度和品牌集中度
- 采购、头程、平台费、退货、仓储、交期和合规/IP 基础信息

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 面向内销买家的中文B2B平台，其自带的整页翻译在首页等入口位置可能失效，先直接进入商品或搜索结果页测试翻译是否正常，而不是在首页反复尝试后就判定工具不可用。
2. 该类平台的自身搜索通常按中文分词匹配，直接输入英文关键词往往召回结果很少；把目标关键词先翻译成中文简体再粘贴进搜索框，通常能显著扩大召回的供应商与商品数量。
3. 找到候选商品后优先查看是否留有电话或即时通讯联系方式，能加即时通讯工具的先加，说明对方习惯跨境沟通或已有外贸经验积累。
4. 站内自带的即时聊天入口通常需要额外注册一个桌面端即时通讯账号才能使用，如果愿意投入这一次性设置成本，这条通道能获得比留言表单更快的直接对话。
5. 对同一款商品同时联系多家供应商，而不是找到第一家愿意回复的就停止；一家供应商如果在其他外贸平台完全没有同款曝光，可以作为其可能是相对独家供应渠道的参考信号之一，但需要直接询问对方确认，不能仅凭搜不到就断定。
6. 涉及打样与批量下单的沟通，优先使用平台提供的担保交易或在线支付通道，在供应商资质与样品质量未经验证前避免场外直接转账。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 中文检索词对照表
- 候选供应商多渠道联系记录（站内消息/即时通讯/桌面IM）
- 多家比价与独家性核实结论
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
