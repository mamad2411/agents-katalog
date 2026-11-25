---
name: sealeap-bixie-amazon-seasonal-demand-cycle-timing
description: "Distinguish genuine seasonal products from short-lived trends using multi-year search-volume cycles, BSR swings, and competitor price patterns, then map the confirmed cycle into staging, growth, peak, and clearance phases. Provides stop and clearance triggers tied to declining-demand evidence rather than a fixed calendar date. Use for 判断是不是季节性产品、季节性产品备货节奏、旺季衰退信号识别、清仓时机判断. Do not use for routine evergreen-product selection, or to conclude seasonality from a single month of data."
---

# Amazon 季节性产品热度与备货节奏

## 目标

Distinguish genuine seasonal products from short-lived trends using multi-year search-volume cycles, BSR swings, and competitor price patterns, then map the confirmed cycle into staging, growth, peak, and clearance phases. Provides stop and clearance triggers tied to declining-demand evidence rather than a fixed calendar date.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 判断季节性需要多个周期重复验证的证据，仅凭一年数据或单一竞品表现得出结论，容易把偶发热点误判为稳定季节性规律。
- 搜索量、BSR 与销量的对应关系是经验假设，不同类目的转化路径不同，量级换算需用自身实际转化数据校准，不能直接套用统一比例。
- 连续下滑即衰退的判断标准会因类目波动性不同而需要调整灵敏度，窄幅正常波动不应被误判为衰退信号。

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

1. 拉取核心关键词较长周期（建议一年以上）的搜索量曲线，判断是否存在固定月份反复出现的波动，而不是只看近期数据。
2. 交叉核对三到五个头部竞品同期的 BSR、价格与新链接进入节奏，确认排名与价格波动的时间点是否与搜索量曲线吻合。
3. 只有搜索量、BSR、价格三个信号在多个周期里都重复出现类似节奏，才判定为真季节性产品，单一信号或只观察到一个周期不足以下结论。
4. 一旦确认季节性，以搜索量连续多周环比抬升作为进入预热期的信号，启动上架与基础优化，备货量以此前周期的实际峰值销量为参考起点而非固定倍数。
5. 峰值期后紧盯搜索量与竞品价格是否连续走弱，一旦出现连续走弱信号，立即停止补货并启动广告收缩，不等销量数据本身下滑再反应。
6. 清仓定价以覆盖仓储与处理成本为底线，只要高于该底线即可考虑放行，不与旺季价格锚点比较。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：拉取核心词多年历史搜索量曲线与竞品 BSR、价格走势作为季节性判断的代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 季节性判断证据表
- 热度周期阶段划分
- 分阶段备货与广告节奏计划
- 衰退与清仓触发条件清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
