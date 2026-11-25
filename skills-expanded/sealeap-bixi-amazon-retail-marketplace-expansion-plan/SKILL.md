---
name: sealeap-bixi-amazon-retail-marketplace-expansion-plan
description: "Screen whether a new retail-marketplace opportunity, such as a vertical e-commerce platform, a home-improvement or electronics retail chain, or an invitation-only general-merchandise retailer, is worth pursuing by matching an already-proven Amazon SKU against the channel's stated category gaps and a seller-fit checklist, then sequence a low-risk entry before committing to deeper channel-specific investment. Use for 要不要开亚马逊之外的新零售渠道、新Marketplace值不值得申请、哪些SKU适合先复制过去试水、入驻前要准备哪些资料、渠道扩容信号怎么判断. Do not use to submit an actual marketplace application, sign a channel agreement, or pay onboarding fees without verifying current rules and costs on the target platform's own seller portal."
---

# Amazon 新零售渠道拓展机会评估

## 目标

Screen whether a new retail-marketplace opportunity, such as a vertical e-commerce platform, a home-improvement or electronics retail chain, or an invitation-only general-merchandise retailer, is worth pursuing by matching an already-proven Amazon SKU against the channel's stated category gaps and a seller-fit checklist, then sequence a low-risk entry before committing to deeper channel-specific investment.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源中列出的具体营收规模、GMV增速、活跃客户数、门店数量等均为渠道在特定报告期公开的数字，会随时间推移变化，执行前需以渠道最新官方或投资者披露为准，不能直接引用旧数字做投入决策依据。
- 满足若干条以上即值得申请或尝试的门槛条数是来源给出的经验参考而非渠道官方标准，应按自身产品实际情况和渠道当期审核松紧度重新校准，仅作优先级排序参考，不作为唯一准入依据。
- 渠道费用结构（佣金、货损费、手续费、后台系统使用费等）与合规要求（保险、责任险、产品认证）会因品类和渠道而异，来源提及的具体费率和条款仅为参考，正式申请前必须以渠道官方费率页面或合同文本核实。
- 报道中提到的具体品牌进驻案例、单品销量增幅等为渠道方或第三方公开宣传的个案，不代表普遍可复制的增长率，不能作为自身销量预期或投入回报测算的依据。

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

1. 先核实目标渠道的当前信号：查证该渠道近期公开披露的营收或GMV增长趋势、第三方卖家名额是否在扩容、以及是开放自主申请还是邀请审核制，渠道规则和门槛会随时间调整，须以官方最新页面和披露日期为准，不沿用旧印象判断。
2. 用渠道通用的卖家自测维度打分：核对是否已在其他渠道（含亚马逊）有真实销量证明、是否有品牌和稳定供应链而非临时铺货、美国仓库存与退换货能力是否已跑通、产品资料与合规单据是否齐全、以及是否愿意投入新品上架和渠道运营资源；多数维度不达标时先补齐能力再申请，避免裸申请消耗审核名额。
3. 核对候选产品与渠道当前品类缺口是否匹配：对照该渠道公开强调的品类扩张方向，用能否第一眼看懂卖点、场景是否明确、是否有独特理由、价格是否容易尝试、能否延伸成系列等标准，排除与渠道现有供给高度同质、缺乏差异化理由的SKU。
4. 优先选一到三个包装可控、售后简单、已经过亚马逊验证的成熟SKU做首批试水，不要求全系列产品同步迁移；起步阶段先用自行履约或已有的跨境仓配能力，上线后再评估是否加入渠道自有仓配、备货或推荐位等更深度合作项目。
5. 若渠道设有邀请制或多阶段审核，提前列出从了解到上线每一关（品类匹配确认、企业与供应链资质沟通、商品清单审核与后台账号创建、品牌备案与首批测试上传、上线后与渠道对接人协同）所需的材料与预计耗时，并明确这通常是需要投入时间甚至费用的服务而非免费招商，判断产品匹配度合格后再进入付费或深度合作阶段。
6. 为首批测试设定止损与推进条件：约定测试期内的最低转化、销量或退货率基准，达标则追加SKU或深化渠道合作，不达标则暂停追加投入并复盘是品类选择、渠道匹配度还是执行环节出了问题。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：核实目标零售渠道当前的增长数据与入驻门槛等公开页面信息，并视需要核对同类产品在该渠道的评论与上架情况。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 渠道信号与准入门槛核实记录
- 卖家自测维度打分表
- 候选SKU与渠道品类匹配度对照表
- 分阶段准入关卡与所需材料清单
- 首批测试止损或推进条件设定表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
