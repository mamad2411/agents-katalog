---
name: sealeap-luduan-amazon-brand-content-site-setup
description: "Plan a brand content or affiliate site that supports off-Amazon traffic by choosing the site type, vetting new or aged domains with backlink, archive-history and index-status checks, selecting managed hosting on measured latency, uptime, SSL and quota terms, verifying storefront page mappings, and starting with content plus compliant link building. Provides a checklist and hypotheses, not a ranking guarantee. Use for 品牌独立站怎么起步、内容站还是电商站、域名怎么选、老域名值不值得买、建站程序主机怎么选、服务器地区与速度、电商插件页面配置核对、博客做 SEO 引流. Do not use for paid search campaign setup or for link schemes that build satellite blogs solely to pass links."
---

# Amazon 品牌内容站搭建与域名主机选型

## 目标

Plan a brand content or affiliate site that supports off-Amazon traffic by choosing the site type, vetting new or aged domains with backlink, archive-history and index-status checks, selecting managed hosting on measured latency, uptime, SSL and quota terms, verifying storefront page mappings, and starting with content plus compliant link building. Provides a checklist and hypotheses, not a ranking guarantee.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源把“域名含关键词即有排名权重”“精确匹配域名会排第一”当作规律，这属于过时或未验证的 SEO 假设；以实测排名与流量为准。
- 来源介绍在免费博客平台批量建站互链（web 2.0 外链）以及买老域名承接旧权重的做法；前者属于搜索引擎可能处罚的链接操纵，本 Skill 不采用；后者效果不确定且有污染风险，三项核查只用于排除风险，不把旧外链当作可靠资产。
- 来源给出的主机月费、延迟毫秒阈值、在线率数字与联盟站收益上限均为特定时点的经验值，本 Skill 不保留；一律以当前报价与实测为准。
- 内容站见效周期长，来源称有经验者半年可见效果属个案；投入前评估团队持续写作能力，并为站点设置阶段性停止条件。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、产品事实与目标购买任务
- 关键词、商品投放、展示和视频的聚合表现
- 受众包定义、资格、站点限制和隐私边界
- 价格、评论、页面、库存与转化基线

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 先定站点类型与目标：电商站（资金与物流压力最大）、在线工具/服务、企业官网、内容/联盟站（起步门槛最低）；为 Amazon 引流的品牌站通常从内容型起步，写明目标关键词主题与承接动作（点击到 Listing 或订阅）。
2. 新域名：优先含核心需求词的可读域名，用免费关键词工具找竞争低的主题词，不追求品牌短域名；域名含词是否带来排名加成记为待验证假设，不作为购买理由。
3. 老域名（拍卖/交易市场）三项核查：外链档案（引用域数量、两类权威指标是否均衡，偏向一侧提示垃圾外链）；历史快照（过去做什么行业、是否与本主题相关、是否有大量跳转记录，跳转多提示权重已被转走）；搜索引擎收录状态（用 site: 检索确认是否被除名）。任一项不通过不高价购买。
4. 主机选型：电商出身团队优先托管型（预装、备份、SSL、一键安装），不选需自行配置系统的裸服务器；免费或共享主机因速度、在线率与地区差不推荐。购买后做速度测试：服务器所在地延迟与全球主要市场延迟以实测为准，来源经验阈值仅作参考；服务器地区与目标市场一致。
5. 核对套餐条款：在线率承诺、SSL 是否包含、带宽/存储/月流量三者分别指什么并留意把月流量与带宽混写的营销话术；折扣价通常绑定多年预付，按实际年成本比较。
6. 电商插件配置核对（以当前控制台为准）：购物车页、结账页、我的账户页、条款页是否已创建并在设置中正确指向；导航菜单是否包含这些页面；表格类内容用插件生成并按读者需要决定是否允许排序。
7. 起步推广：先写面向目标关键词的指南型文章（长文、可读、有结构），观察搜索流量与停留；外链只通过真实合作与被引用获得；前期不开搜索广告作为主要引流手段，记为待验证的资源分配假设。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取候选域名的历史快照、外链概况与收录状态等公开代理数据，以及目标主题词的搜索需求参考。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 站点类型与目标定义（主题词、承接动作）
- 域名核查表（新域名候选/老域名外链-历史-收录三项）
- 主机选型对比表（延迟实测、在线率、SSL、配额条款、年成本）
- 电商页面配置核对清单
- 内容与外链起步计划及停止条件
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
