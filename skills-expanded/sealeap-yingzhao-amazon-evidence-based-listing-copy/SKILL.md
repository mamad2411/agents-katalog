---
name: sealeap-yingzhao-amazon-evidence-based-listing-copy
description: "Draft a title, bullets and image brief for a new listing by first building product knowledge from off-Amazon sources (brand sites, buying guides, expert reviews), extracting what buyers care about, validating each candidate selling point against competitor review mentions, and only then mining competitor listings for structure and vocabulary. Every claim maps to a product fact or buyer evidence and copy stays scannable and natively phrased. Use for 新品 Listing 怎么写、五点写什么、消费者关心什么卖点、场景怎么写不像堆砌、标题参考谁、图片风格统一、要不要埋词. Do not use to copy competitor or third-party text verbatim, and do not use for A+ module design or backend attribute filling."
---

# Amazon 精品 Listing 卖点证据写作

## 目标

Draft a title, bullets and image brief for a new listing by first building product knowledge from off-Amazon sources (brand sites, buying guides, expert reviews), extracting what buyers care about, validating each candidate selling point against competitor review mentions, and only then mining competitor listings for structure and vocabulary. Every claim maps to a product fact or buyer evidence and copy stays scannable and natively phrased.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “先站外后站内”是为了避免被竞品卖家的宣称误导，适合对产品尚不熟悉的场景；已有产品认知时可调整顺序，但“每个卖点有买家证据”的要求不变。
- 评论关键词提及次数只是代理指标，受评论总量、同义词与评论者用语影响；用于排序卖点优先级，不作为需求量或转化预测。
- 母语页面语法正确、可作参考，但复制第三方文案涉及版权与重复内容风险；只借鉴句式、术语和结构，文案按自己产品重新写。
- “优惠券比最低档多开一个百分点视觉折扣更大”“五点越简洁转化越高”是来源经验；以自家点击率与转化率数据校准后再定，不作为规则。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、产品事实和当前 Listing
- 同购买意图可比竞品、价格、评论、图片和销量
- Search Term、Placement、CTR、CVR、订单、退货和利润
- VOC、Q&A、退货原因与任何页面或广告变更日志

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 先建产品认知笔记，暂不看 Amazon 竞品 Listing：用搜索引擎打开品牌官网、其他零售平台、专业评测与榜单、百科类页面，记录术语、材料与结构、各部件带来的好处、典型使用场景与保养注意，并标注来源；对自己不熟悉的产品，这一步做完再进入下一步。
2. 提炼消费者关心点：重点阅读“如何选购这类产品”类内容与专家评测，列出买家选择时关注的属性候选清单（如舒适、耐用、透气、防滑、轻便等，按品类替换），标记每个关注点的来源。
3. 用竞品评论验证关心点：在头部竞品的评论中按关键词搜索每个候选关注点，记录提及条数与评论总量，把关注点分为高频、低频、无人提及三档；写入五点的优先级按此排序，无人提及的即使卖家常写也不作为主卖点。
4. 再读竞品 Listing，目的是提取而非评判：记录喜欢的标题结构、简洁的五点写法、自创的专业词汇与说明“为什么适用”的场景写法；对每个卖家宣称的点，回到第 3 步判断是否为买家关心，并核实自己产品确实具备该特性后才采用。
5. 写标题与五点：每条五点只承载一个关心点，用“特性→原因→场景”说明产品为什么适合，场景选同一类相近活动而非罗列反差很大的场合；句子短、可扫读，用母语级表达，借鉴站外页面的句式与术语但不复制原文，交付前做语法与本地化校对。
6. 图片与变体一致性检查：主图展示的款式必须与标题和目标搜索意图一致（如有无某个结构件），整组图片底色与风格统一，变体之间同一规范；把值得参考的竞品图片类型整理成拍摄清单，不直接使用他人图片。
7. 关键词处理与终检：核对标题、五点、描述是否已自然覆盖核心搜索词，未覆盖的放入后台搜索词字段，不为埋词牺牲可读性；逐条确认每个卖点可回指产品事实或评论证据，涉及安全、认证、成分类的表述必须有资质证据，否则删除。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取头部竞品 Listing 文案、评论文本与关键词反查结果，作为关心点验证与词覆盖核对的证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 产品认知笔记（术语、结构与好处、场景、来源）
- 消费者关心点清单与评论验证结果（提及数、样本、档位）
- 竞品 Listing 提取表（可用结构、词汇、场景写法、需核实的宣称）
- 标题与五点草案（每条对应的关心点与证据）
- 图片拍摄清单与一致性检查记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
