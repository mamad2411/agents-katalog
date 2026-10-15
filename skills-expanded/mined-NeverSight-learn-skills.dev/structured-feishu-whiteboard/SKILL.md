---
name: structured-feishu-whiteboard
description: >
  Use when the user wants to turn materials, reports, plans, webpages, Feishu docs,
  meeting notes, or free text into a structured, editable Feishu/Lark whiteboard,
  including requests for whiteboard beautification, consulting-style diagrams,
  infographics, roadmaps, matrices, workflows, or visual summaries.
---

# Structured Feishu Whiteboard

把任意材料转成结构清晰、咨询汇报风格的飞书画板。这个 skill 的重点不是装饰文本，而是先完成信息筛选、观点组织、版式选择，再通过确定性渲染器生成可编辑画板。V4.3 是稳定版，包含信息清单、候选路由、能力注册、内容覆盖、自适应密度布局、行级协调、语义组件、流程图质量门禁和运行记录。

## 快速判断

使用本 skill 时，按这个顺序工作：

1. **获取内容**：用户可能粘贴文本、给飞书文档、给网页、给本地文件，或要求你自行检索。读取动作可使用对应工具或其他 skill；本 skill 从“已获得的内容”开始负责结构化表达。
2. **判断体量**：读取 [`references/content-budget.md`](references/content-budget.md)，判断材料是短内容、中等内容、长文/报告还是复杂材料。
3. **理解材料**：读取 [`references/report-workflow.md`](references/report-workflow.md)，提炼主题、结论、证据、对象、冲突、时间线和行动项。
4. **长文处理**：中等内容、长文或复杂材料必须读取 [`references/long-form-workflow.md`](references/long-form-workflow.md)；长文还要读取 [`references/large-canvas-workflow.md`](references/large-canvas-workflow.md)，先做信息保全清单和 onepage 区域草稿；不要直接把全文塞进 SVG。
5. **选择版式**：读取 [`references/layout-library.md`](references/layout-library.md)，从生产版式和 V3.2/V3.3 受控表达场景中选择一个主结构；不要自由发明复杂版式。复杂材料如果包含指标、进展、证据、风险和行动等多种关系，再读取 [`references/expression-grammar.md`](references/expression-grammar.md)，判断是否使用 `expression-canvas`。
6. **选择风格**：读取 [`references/style-library.md`](references/style-library.md)，从生产可选风格中选择一个；如果用户指定风格偏好，优先匹配。V3.5 起，Apple Report、Linear System、Stripe Data、Vercel Precision 属于工作型增强风格；Neo Grid Bold 和 Riptide Cobalt 属于用户主动选择的创意张力风格，不能作为默认自动风格。新增或改动后的样例必须经过飞书侧预览复核。
7. **稳定渲染**：默认必须读取 [`references/deterministic-rendering.md`](references/deterministic-rendering.md)，先生成 JSON brief，再根据 `engine` 和 `renderTarget` 使用 `scripts/render-whiteboard.mjs`、`scripts/render-whiteboard-dsl.mjs` 或实验性的 `scripts/render-whiteboard-v4.mjs`；不要自由手写整张 SVG 或 DSL。
8. **生成画板产物**：只有用户明确要求“实验性手写 SVG”或当前仓库缺少渲染器脚本时，才允许读取 [`references/feishu-svg-rules.md`](references/feishu-svg-rules.md) 手写；否则手写 SVG/DSL 视为不合格输出。
9. **检查和修复**：读取 [`references/quality-checklist.md`](references/quality-checklist.md)；发现出框、堆叠、拥挤或乱码时，按 [`references/overflow-repair.md`](references/overflow-repair.md) 修复。
10. **写入飞书**：默认新建飞书文档，插入白板，写入生成结果，返回文档链接和预览图。

## V4.3 稳定链路

用户要求生成复杂画板、流程图、跨 Agent 稳定输出，或需要验证长文完整性时，必须使用 V4.3 控制链路：

1. 将材料写成符合 `schemas/content-inventory.schema.json` 的信息清单，为事实分配 ID、类型和重要程度。
2. 运行 `scripts/route-whiteboard.mjs`，保留前三个候选版式、分数、理由、置信度和回退方案。
3. 生成带 `pipelineVersion: "4.3"` 与 `planning` 的 brief，记录选中和省略的信息 ID。
4. 运行 `scripts/run-whiteboard.mjs`，统一完成覆盖验证、能力解析、渲染和质量检查。
5. 保留 `run-manifest.json`；没有运行记录或关键事实覆盖不足时，不得声称 V4.3 生成成功。

合法的引擎、版式、目标和风格组合以 `config/capabilities.json` 为准。禁止把不支持的风格静默替换为专业蓝白。

## 默认输出

- 一个新建飞书文档链接。
- 文档内包含一块可编辑飞书画板。
- 一张渲染预览图，方便用户不用打开文档也能快速检查。
- 简短说明：使用了什么版式、什么风格、哪些信息被压缩或合并。
- V4.3 额外返回运行清单，说明内容覆盖、路由候选、实际引擎、产物哈希和检查结果。

不要把用户的原始指令、来源路径、工具过程、风格名解释或“根据某材料整理”等元信息写到画板上。画板上只放最终内容。

## 前置检查

开始写入飞书前，运行：

```bash
bash scripts/preflight.sh
```

如果缺少 `lark-cli`、Node 或白板转换工具，先告诉用户需要补齐依赖；不要假装已经能写入飞书。

## 选择规则

- 用户给的是方案、报告、研究、网页长文：优先用 **结论先行**、**问题拆解** 或 **对比矩阵**。
- 用户给的是计划、路线、阶段安排：概念上可参考 **路线图/阶段规划**，但当前交付仍必须映射到确定性渲染器；优先使用 `large-canvas` 的 roadmap 区域承载。
- 用户给的是普通机制、业务链路、系统过程：可使用 `process-chain` 或 `large-canvas` 的模块区/roadmap 区域承载。
- 用户明确需要“流程图”、审批流、跨角色协作、系统交互、人机协同、节点到节点依赖：优先评估 V4.1 `flow-canvas`。线性步骤使用 `flowMode: "linear-flow"`；多角色责任流转使用 `flowMode: "swimlane-flow"`。流程图必须设置 `engine: "v4"` 和 `renderTarget: "svg"`。
- 用户给的是版本迭代、事件推进、里程碑复盘：优先使用 `milestone-timeline`，并设置 `renderTarget: "dsl"`。
- 用户给的是筛选、转化、收敛、优先级漏斗：优先使用 `funnel`，并设置 `renderTarget: "dsl"`。
- 用户给的是层级、优先级、能力基座、战略承接：优先使用 `pyramid`，并设置 `renderTarget: "dsl"`。
- 用户给的是多个核心指标、状态复盘、覆盖率、风险数或效率变化：优先使用 `metric-dashboard`，并设置 `renderTarget: "dsl"`。
- 用户给的是经营复盘、增长项目、指标趋势、状态和行动组合：优先考虑 `expression-canvas` + `stripe-data`，但仍要保持单页结构清晰。
- 用户给的是机制、Agent 协作、工程系统图但不需要真实节点连接：优先考虑 `expression-canvas` + `linear-system`。
- 用户给的是产品介绍、能力总览、策略一页稿：优先考虑 `expression-canvas` + `apple-report`。
- 用户给的是规则、验收、技术方案、发布检查：优先考虑 `expression-canvas` + `vercel-precision`。
- 用户明确要求更大胆、更有设计感、发布感或概念包装：可以考虑 `neo-grid-bold` 或 `riptide-cobalt`，但必须短句化、固定网格、人工复核；不要默认自动使用。两者必须走专属创意渲染器，不能只套用通用 `expression-canvas` 卡片模板换颜色。
- 用户给的是目标完成度、阶段进展、OKR 复盘或风险收敛：优先使用 `progress-wall`，并设置 `renderTarget: "dsl"`。
- 用户给的是 Top-N、贡献度、问题分布、异常来源或资源占比：优先使用 `ranked-bars`，并设置 `renderTarget: "dsl"`。
- 用户给的是数字变化、成本变化、人力优化、收入差异或效率提升归因：优先使用 `variance-bridge`，并设置 `renderTarget: "dsl"`。
- 用户给的是复杂项目汇报、经营复盘、决策诊断或混合长文，且同时包含指标、进展、证据、风险和行动中的至少三类：优先评估 V3.3 `expression-canvas`。根据材料主导关系选择 `dashboard-onepage`、`narrative-map` 或 `modular-canvas`，并设置 `renderTarget: "svg"` 或省略 `renderTarget`。
- V3.4 起，`expression-canvas` 可以使用更强的数据化表达组件：状态/健康度用 `status-board`，时间变化用 `trend-sparkline`，方案选择用 `decision-matrix`，起终点差异归因用 `variance-bridge-v2`。这些组件必须由 JSON brief 触发并经渲染器生成，不允许手写自由 SVG。
- V4.3 起，复杂 `expression-canvas` 和 `flow-canvas` 默认使用 `engine: "v4"` 与 `renderTarget: "svg"`。流程图必须先构建节点和边，再由脚本完成分层、边界连接和质量检查；禁止 Agent 自由手写连线坐标。
- V4.2 起，复杂架构、知识治理、风险治理和行动清单类材料如果使用 `expression-canvas`，必须避免把长说明压成小窄框。真正长内容可以升级为全宽模块，但不能只因条目达到 4 个就强制全宽。
- V4.3 起，场景选择不得只凭关键词直接落到一个模板。先生成信息清单和候选路由；低置信度时保留备选和稳定回退。V4 expression-canvas 根据条目长度、说明密度和方向关系在 1/3、1/2、2/3、全宽之间选择；四到六个短并列项优先使用紧凑网格，禁止连续稀疏全宽积木墙。同一行的模块必须选择高度协调的内部变体；风险、证据和行动必须使用各自的语义组件，不能退化成同一种竖线列表。
- 信息太多时，先做信息保全清单，再在一张 onepage 大画布内扩展区域承载；不要把原文完整搬上画板，也不要丢掉关键结论、约束、风险、指标、证据和行动。
- 长文默认生成一个统一 onepage 大画布；总览、模块、路线、指标、证据、风险和行动属于同一张连续版面。
- 如果某个区域超过容量预算，不要靠缩小字号硬塞；改写短句、合并重复项，或扩大同页区域。
- 结论先行、问题拆解和长文 onepage 必须使用确定性渲染器，确保其他 Agent 输出的留白、字号、颜色和卡片结构稳定一致。
- 当前生产可交付版式包括 `conclusion-first`、`problem-breakdown`、`large-canvas`、`roadmap`、`process-chain`、`comparison-matrix`、`expression-canvas` 和 `flow-canvas`。V3.2 受控表达版式包括 `milestone-timeline`、`funnel`、`pyramid`、`metric-dashboard`、`progress-wall`、`ranked-bars` 和 `variance-bridge`。如果内容不满足对应版式条件，不要自由手写新布局；回退到 `conclusion-first` 或 `large-canvas`。
- 单张画板只表达一个主任务；如果同时出现主线、动作、指标和读图说明，优先拆成总览图和指标图。
- 并列模块不要使用箭头；只有时间推进、流程依赖或价值链才使用箭头。
- 指标和 `xx%` 等草稿占位按 `content-budget.md` 执行：必须有业务语义，同类指标只出现一次，卡片内指标和底部指标区二选一。

## 交付标准

生成前必须能回答：

- 这张画板的主结论是什么？
- 用户看完后应该记住哪 3 到 5 件事？
- 版式为什么适合这份材料？
- 哪些信息被删减、合并或降级？
- 当前内容是否超过单画板容量？
- 如果是长文，为什么选择单屏总览或 onepage 大画布？
- 如果是长文，哪些重要信息进入了同页后续区域？
- 这张画板是否只承担一个主表达任务？
- 指标是真实数字，还是带业务语义的草稿占位？
- 指标是否重复出现，且是否使用统一网格对齐？
- 如果使用 V3.3，为什么选择当前 `expressionMode`，以及每个 `expressionBlock` 承担什么信息关系？
- 如果使用 V3.4 组件，为什么当前材料需要状态、趋势、决策或变化桥，而不是普通卡片？
- 如果使用 V4.2 高密度表达，哪些模块被全宽呈现，为什么没有继续塞进半宽小框？
- 如果使用 V4.3，关键事实覆盖率是否为 100%，高优先级事实是否全部被选中或明确省略？路由候选和选择理由是什么？
- 如果使用 V4.3，短内容是否被无意义拉伸？同排模块是否高度协调？风险、证据和行动是否使用了不同的信息表达语法？
- 如果使用流程图，连线是否位于节点下层、连接节点边界、避免穿越无关节点，并保留必要的边标签？

生成后必须确认：

- 渲染产物没有明显文字溢出、重叠或裁切。
- 产物是由 `scripts/render-whiteboard.mjs`、`scripts/render-whiteboard-dsl.mjs` 或明确试点的 `scripts/render-whiteboard-v4.mjs` 生成的，除非用户明确接受实验性手写 SVG。
- 所有正文是 `<text>` / `<tspan>`，不是路径或图片。
- 结构元素使用 rect、circle、ellipse、line、polyline 等可编辑形状。
- 画板没有无意义装饰、元信息页眉、来源说明或过程说明。
- 没有乱码、异常符号、长 URL 或未清理的原文残片进入画板。
- V4.3 产物通过 `scripts/check-v43-visual-quality.mjs`，并生成状态为 `passed` 的 `run-manifest.json`。
