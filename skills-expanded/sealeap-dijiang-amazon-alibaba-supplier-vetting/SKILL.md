---
name: sealeap-dijiang-amazon-alibaba-supplier-vetting
description: "Screen B2B sourcing-platform suppliers using a four-dimension check (registered identity, business type, track record, certifications) plus category-focus analysis, then batch-qualify the shortlist through a single grouped RFQ instead of one-by-one outreach. Use for 供应商背调、如何筛选靠谱工厂、辨别贸易商与工厂、批量发询价单. Do not use to guarantee supplier legitimacy without direct contact and sample verification."
---

# Amazon 货源供应商四步核验

## 目标

Screen B2B sourcing-platform suppliers using a four-dimension check (registered identity, business type, track record, certifications) plus category-focus analysis, then batch-qualify the shortlist through a single grouped RFQ instead of one-by-one outreach.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 供应商分级标签、认证角标等信息由平台或第三方审核机构提供，本质是平台侧的信用代理指标，不等于对产品质量或工厂真实产能的保证，仍需自行验证。
- 企业注册名称的地域/层级构成规则属于来源经验总结，不同地区、不同时期的工商登记规则可能有例外，不能作为唯一真伪判断依据。
- “经营年限”“品类集中度”等门槛均为经验性参考，需按自身风险承受能力与品类特性设定标准，不存在放之四海皆准的固定数值。
- 批量群发询价能提升效率，但也可能降低单个供应商的重视程度，报价质量下降时应考虑针对高优先级供应商单独跟进。

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

1. 用目标品类关键词在 B2B 平台按“供应商”维度而非“商品”维度检索，先看平台内置的供应商分级信号（如认证供应商、实地核验、交易保障类标签），把候选圈定在评级较高的一批，而不是先比价。
2. 核对供应商主体信息：注册名称与经营地是否与其展示的产地/规模说法一致、注册的经营类型是否为“生产+贸易”双资质（能否直接出口）、经营年限是否达到你能接受的最短门槛（自定，不套用他人经验值）、是否有第三方体系认证；证据来源应为平台公开的企业资质页面。
3. 分析该供应商的主营品类是否集中于你要采购的品类：产品线越聚焦通常代表工艺更专精；产品线极度分散时，需要在沟通阶段额外确认其是否真具备该品类的量产与品控能力。
4. 用同一份标准化询价模板（规格、目标价区间、起订量、认证要求、打样周期）同时发给一批入围供应商，避免逐家改写话术导致信息不一致，便于横向比较回复质量与响应速度。
5. 记录首轮回复的沟通质量（专业度、报价逻辑是否合理、是否主动澄清规格疑点）作为二次筛选依据；对未回复者统一跟进一次提醒，而非无限等待。
6. 对通过前两轮的供应商，再进入打样与实地/视频验厂等更高成本的验证步骤，最终决策以打样结果与验厂证据为准，不单凭线上资料下单。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：如需核对候选供应商的平台公开经营资质、认证标签等信息，可用阿里巴巴/1688 类数据连接器辅助核验公开页面证据，不替代直接沟通与验厂。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 供应商候选清单（含四维评分）
- 标准化询价（RFQ）模板
- 首轮沟通质量记录表
- 入围/淘汰依据说明
- 待打样供应商短名单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
