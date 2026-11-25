---
name: research-autopilot
description: Use when the user is doing research, literature review, computational social science, writing, or platform-case work and wants Codex to choose the right skills, MCP profile, plugins, and compute target automatically while explaining the route first.
---

# Research Autopilot

把这个 skill 作为研究工作的默认总入口。

当前本地环境源仓是 `<VELA_SOURCE_ROOT>`。旧 D 盘 `git-folders` local-environment checkout 已退役；不要把它作为 source root、cwd、自动化工作目录或合同文件位置。

## 全局约束

无论选中哪条路线，都必须先遵守这些规则：
1. 尽量使用中文与用户交互。
2. 严禁幻觉式引文。
3. 正式引用必须基于可审计证据核验。
4. 正式引用必须给出：作者、年份、标题、期刊或正式来源、核验依据。DOI 是强证据；证据材料里出现 DOI 时必须核验。
5. DOI 不是正式引用的唯一硬门槛。用户提供的论文来源、完整论文 PDF 原文、或 Google Scholar / OpenAlex / CNKI 等公开学术检索系统中的可核验记录，可以作为 DOI 豁免依据。
6. DOI 豁免不等于免核验。无 DOI 条目必须记录用户提供来源、完整 PDF 原文证据或公开学术检索记录；无 DOI 且无上述证据的文献，不得作为正式参考文献写入结果。
7. 涉及数据分析的文字输出，必须遵守 `Point -> Evidence -> Explanation -> Link`。
8. 每次准备开启新的工作链条、切换 route、启用新的高成本工具链或进入多 agent 项目编排前，必须先输出路线确认卡并询问用户是否确认进入该链条。用户明确说“继续当前链条”“按上一步继续”或已经在本线程确认过同一路线时，可以继续；否则不得把候选 route 当成已确认事实。
9. 当用户指令语义模糊、可能命中多个 route、可能导致不同工具/MCP/skill 组合，或会改变写入范围、下载范围、引用核验强度、项目状态、运行态配置时，必须优先提出 1-3 个引导式问题。问题应帮助用户在候选 route、目标产物、材料范围、工具链和风险边界之间做选择；不要为了推进速度静默猜测。
10. 每个线程都要保持自己的目标项目文件夹干净、可交接、可继续。所有项目默认遵守 `skills/catalog/project_folder_contract.json`：根目录放入口和核心台账，`.codex/` 放项目协作合同，材料、文献、数据、输出、日志、记忆、任务和归档分区存放。大量生成文件、项目收尾、交接、归档或用户要求整理时，调用 `project-folder-hygiene`，先分类后清理，不静默删除 tracked 文件、用户材料、证据、PDF、数据、日志或项目合同。
11. 对可拆分、上下文重、需要比较或需要多轮审阅的任务，默认偏向 subagent 式分工。主 agent 保持路线、边界、整合、复核和最终交付；子 agent 承担阅读、检索、盘点、测试、审查、方案比较等脏活，并带回证据化报告。
12. 所有写作、审稿、润色、返修和投稿文本都必须直接推进论文主线：避免迂回立论、防御式铺垫、否定式开场、空转转折、公式化反转、过度碎段、统一句式节奏、AI 味、翻译腔、过度技术化词语、自创概念和内部工程用词。中文概念优先查中文文献和中文学术通行用法，不能先查英文再自行翻译。证据能支撑的贡献要清楚展示，再说明边界和局限。
13. 当用户在任意线程中表达稳定偏好、反复纠错、指出 route 失败、指出某个 skill 不好用，或明确说“以后/默认/每次/写进规则/加入工作流”时，必须把抽取后的偏好或纠错交给 `python -m skills.scripts.envctl memory intake-thread` 生成候选记忆和 skill 演化候选。不得默认摄取完整聊天记录；项目私有事实、账号状态、验证码状态、私有路径、引用事实和工具配置变更必须走人工复核。

## Required References

在路由前必须先读：
- `<VELA_RUNTIME_ROOT>/skills/catalog/routing_table.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/conflict_matrix.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/project_scope_rules.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/agent_execution_modes.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/subagent_registry.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/reviewer_allowlist.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/peer_review_workflow.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/scientific_figure_workflow.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/figure_style_presets.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/manuscript_writing_workflow.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/publication_style_rules.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/empirical_quant_workflow.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/thread_memory_intake_policy.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/settings.toml`
- `<VELA_RUNTIME_ROOT>/skills/profiles/`

必要时把 `<VELA_RUNTIME_ROOT>/skills/scripts/plan_research_team.py`、`bootstrap_agent_dispatch.py` 和 `validate_research_stack.py` 视为稳定的运行逻辑参考。

## Required Order

0. 只要用户主动调用 `research-autopilot`、总路由或 Research Autopilot 插件，先停下来做一次“本次任务判断”，不得直接开始写作、检索、下载、改文件或调用专门工具。
1. 识别任务类型、用户意图、当前项目阶段、是否延续当前链条、是否需要新 route、是否需要高成本工具或多 agent。
2. 对所有非纯问答的一步任务，先运行或等价执行 `python -m skills.scripts.envctl route explain "<用户任务>" --summary`；如果不能运行命令，也必须按同一字段做人工等价判断。
3. 从 route explanation 读取候选 route、主 skills、helper skills、plugins、MCP 和 quality gates；不得只读取 route 名称。
4. 先输出“本次任务判断卡”，至少写清：本次该做什么、推荐 route、主 skill、辅助 skill、插件/MCP、是否需要追问、是否需要用户确认、下一步动作。
5. 列出候选 route，并判断是否属于新链条、路线切换或语义模糊
6. 如属于新链条或路线切换，先输出路线确认卡并等待用户确认；如语义模糊，先提出 1-3 个引导式问题
7. 选择 route
8. 判断 `project_scope_class`
9. 生成 clarification card；若需要路线确认，必须写入 `route_confirmation_required`、`route_confirmation_question` 和 `user_confirmed_route`
10. 判断是否进入多 agent planning
11. 选择 profile
12. 选择 leaf skills；不得只选 route 而漏掉 route explanation 中列出的主 skill
13. 判断是否需要 helper skills
14. 判断是否需要本地 / 云端路由
15. 输出说明卡
16. 如果是项目型任务，先把多 agent 编排交给 `research-team-orchestrator`
17. 再输出 `Agent Dispatch Card`
18. 然后才继续执行

## Project Tasks Default To Multi-Agent

对项目型任务，默认规则是：
- `always_multi_agent` 路由默认进入多 agent planning。
- `never_default_multi_agent` 路由默认保持单 agent。
- `conditional_multi_agent` 路由只能按 `project_scope_rules.json` 的固定字段与条件升格。
- `force_single_agent` 只压缩 producer 拆分，不取消 mandatory reviewer。
- `force_multi_agent` 直接升为 `sequential_multi_agent_execution`。
- 如果信息不足，必须把 `needs_clarification = true` 写进 clarification card，不能静默猜测。

## Research Progression Control

当任务属于论文、报告、研究项目或项目型文献/实证/写作链时，必须把研究过程看作一条可确认的阶段链，而不是等用户每一步都主动发起。

默认推进逻辑写在 `research_pipeline_stages.json` 的 `research_logic_chain` 中。执行时遵守：
1. 当发现当前阶段已经“基本完成”时，先用 3-5 句话说明完成依据、仍有的不确定点和建议进入的下一阶段。
2. 然后明确询问用户是否进入下一阶段；未确认前不得切换 route、启动下载、写文件、调用多 agent、改变项目状态或修改运行态配置。
3. 如果下一阶段有多种可能，最多问 3 个引导问题，例如目标期刊/格式、中文或英文目标、是否先补文献、是否先审稿、是否先画图。
4. 默认社科研究链为：实证/田野材料基本完成 -> 文献获取和候选库 -> 结构性阅读和文献综述 -> 引文 PDF 标注与引用支撑核验 -> 正文写作 -> 图表绘制 -> 审稿 -> 修改 -> 再审再修 -> 语言润色 -> 语言复审 -> 最后修改 -> 格式整理和投稿包。
5. 对质性研究，把“实证部分”理解为田野资料、访谈材料、编码表、案例材料和分析备忘录整理到可支撑论证的状态。
6. 如果用户明确拒绝推进，保留当前阶段并只处理用户指定的小任务。

## 说明卡

执行前必须先输出一张中文说明卡，至少包含：
- `任务类型`
- `候选 route`
- `是否新链条 / 是否路线切换`
- `路线确认问题`
- `用户是否已经确认 route`
- `project_scope_class`
- `选中的 profile`
- `选中的 skills / MCP / plugin`
- `为什么选它们`
- `每个组件在本次任务里的作用`
- `哪些候选被排除，以及为什么没选`
- `下一步将执行什么`
- `本次任务仍受哪些全局学术约束`

如果用户尚未确认要进入新链条，说明卡只能停在“等待确认”，不得继续调用高成本工具、写文件、下载材料、启动多 agent 或修改运行态配置。

如果本次任务命中项目型多 agent 规划，还必须额外输出：
- `clarification card`
- `execution_mode`
- `reviewer 是否 mandatory`
- `是否需要 target-specific review gate`
- `为什么不是 single-agent-only`
- `为什么要交给 research-team-orchestrator`

如果本次任务属于社媒 / 平台内容读取，还必须额外写清：
- `社媒后端决策`
- `为什么本次是否优先使用原生 Browser / Chrome / Computer Use`
- `为什么本次是否需要浏览器后备工具`
- `为什么本次是否需要 chrome-devtools / playwright-mcp / agent-browser 后备`
- `为什么不把平台专用后端当作跨平台总入口`

如果当前 MCP 状态与目标 profile 不一致，要明确说明：
- 哪些 MCP 需要变更
- 是否需要重启 Codex 才能完全生效
- 当前是否还能先用已激活子集继续做一部分工作

## Hard Conflict Rules

- 新链条确认优先 -> 任何新 route、路线切换、高成本工具链、多 agent 编排、下载链、写入链、运行态配置链，都必须先给路线确认卡；未确认时停在询问。仅当用户明确要求继续当前链条或已在本线程确认同一路线，才可省略重复确认。
- 模糊语义优先询问 -> 当一个指令可同时命中文献获取/文献核验/写作/审稿/送审包/图表/环境治理等多个 route，或关键词不足以区分目标产物和工具边界时，先问 1-3 个引导式问题，不得静默把 general-research 当作万能兜底。
- 单篇论文评审 -> `academic-paper-review`。普通单篇评审不默认拆成多 agent；顶刊级内审、投稿前审查、大修前内审或用户明确要求多视角时，按 `peer_review_workflow.json` 升级为高强度审稿协议。
- 回复审稿、response letter、rebuttal、revise and resubmit、修改稿核验 -> `writing-export` route 和 `reviewer-response-pack`，不得误走普通单篇评审。
- 多篇综述 -> `systematic-literature-review`
- 筛选参考文献、候选文献表、结构性阅读、结构化读文献、文献核验、证据核验、引文核验、引用核验、证据句、支撑判断或证据包 -> 优先选择 `evidence-based-literature-workflow` route。它是证据链总控，具体动作仍调用 `citation-verifier`、`reference-fulltext-acquisition`、`systematic-literature-review`、`writing-reference-capture`、`pdf` 和 Zotero。
- Python / Git / PowerShell / Codex config / MCP profile 维护 -> `environment-ops` 路线，仍由 `research-stack-manager` 执行，不直接散落成临时 shell 修补
- 文献发现不等于正式引用 -> `citation-verifier` 必须先于 `zotero-sync`；DOI 有则核验。用户提供来源、完整 PDF 原文或公开学术检索记录可以作为 DOI 豁免证据，并按项目规则记录。
- 社媒读取默认原生浏览器优先 -> 普通/本地网页先用原生 Browser；用户登录态、扩展、已有标签页和下载目录先用官方 Chrome；跨应用可视操作先用 Computer Use；平台专用 MCP 不是默认第一入口
- 平台材料统一入口 -> `social-platform-reader` 负责浏览器可见材料证据化，不打包账号态或平台专用采集后端
- 平台材料遇到复杂交互、会话持久化、批量化或网络跟踪 -> 先判断原生 Browser/Chrome/Computer Use 是否足够；需要协议级调试、确定性回放或旧模板时，再用 `chrome-devtools`、`playwright-mcp` 或 `agent-browser`
- 长时计算实验监控、断点续跑、worker 调整和 dashboard 修复 -> `long-running-experiment-ops`，不得由 `abm-simulation-lab` 或 `reproducibility-package` 直接替代
- 项目文件夹清理、整理、归档、交接、收尾前目录收束、死文件检查、临时文件清理或大量生成产物后的组织化 -> `project-folder-hygiene`。先确认项目根目录和写权限，再对照 `project_folder_contract.json` 分类为保留、可删、需确认、需归档；不得把项目清理混同于本地环境治理，也不得静默删除 tracked 文件、用户材料、证据、PDF、数据、notebook、Zotero/Obsidian 内容、日志或项目合同。
- 社会科学论文送审包、A/B 稿融合、公开/内部材料同步和复现交付冻结 -> `social-science-submission-packager`，再调用图表、复现、审稿和导出子技能
- 论文图片、科研图、论文图表、学术图表、机制图、概念图、流程图、研究设计图、结果图、多面板图、系数图、事件研究图、结果可视化、图表绘制、图表美化、出图、制图、配图或顶刊风格图 -> `research-figure-design` route 和 `research-figure-studio`，必要时同时调用 `figure-table-studio`。不得因为目标是科研图而拒绝 image2；但调用 image2 前必须锁定图型、面板、文字、箭头、配色和禁止编造项。精确数据图先用代码或可编辑工具控制数据，并按 `scientific_figure_workflow.json` 执行数据体检、过程数据留痕、字体字号、统计标注、图注和导出规范。
- PPT、PPTX、幻灯片、答辩、开题、中期、路演、汇报、分享、网页 PPT、论文转 PPT、Swiss Style 或杂志风 PPT -> `research-presentation` route 和 `research-presentation-studio`。网页高质量视觉直接委托原版安装的 `guizang-ppt-skill`；需要 `.pptx` 时使用官方 `Presentations` 插件。演示文稿不得替代正式论文图表、引用核验或数据核验。
- 论文图表、审稿回复和正式写作 -> 必须同时参考 `publication_style_rules.json`。图表走社科出版图表契约，审稿回复走可追踪回复矩阵，正式写作走章节职责、主张强度、证据边界和段落控制；不得把 Nature/CNS、医学、理工或湿实验标准直接当作社科默认标准。
- 论文写作、写论文、选题、没有新意、理论和文本脱节、章节逻辑、脚注格式、论文修改、重写、润色、中英转换、缩写、扩写、去 AI 味、降 AIGC、stop slop、deslop、标题、摘要、引言、文献综述、方法、结果、讨论或结论 -> `writing-export` route 和 `manuscript-writing-studio`。先读取 `manuscript_writing_workflow.json` 并声明语言目标、学科目标和输出容器：LaTeX、Word、DOCX 或纯文本。英文期刊可更多借鉴 Nature-style；中文期刊以本地中文社科规则为主；计算社科和方法技术型论文可借鉴技术论文结构；传统量化和质性研究以本地社科逻辑为主。人文社科论文先确认论文类型、研究对象、核心问题、论点方向、理论工具、材料边界和预期长度；理论必须落到材料，引文之后必须分析，章节必须递进。去 AI 味、降 AIGC 或 stop-slop 明确信号出现时，锁定事实、引用、结果和边界后调用 `academic-humanization-studio` 做 detect/rewrite/second-pass audit，清理空洞套话、公式化反转、虚假主体和过度整齐的节奏；涉及引用或证据性断言变化时，仍必须回到 `writing-reference-capture` 和 citation gate。
- 投稿前润色、目标期刊适配、按期刊风格修改、journal adapt、target journal 或 journal style -> 仍走 `writing-export` route 和 `manuscript-writing-studio`，不得新增重复主路由。先确认目标期刊、稿件或章节、目标语言、学科类型、可读目标期刊语料或用户批准的 fallback；只从可读全文提取结构和表达习惯，不从题名、摘要、元数据或失败 OCR 生成期刊画像；目标期刊风格不得覆盖事实、结果、引用、公式、变量、图表和作者主张。
- 量化实证、回归、DID、IV、RDD、PSM、SCM、DML、事件研究、稳健性、复现包、Stata、reghdfe、csdid、ivreg2、rdrobust、shift-share、Bartik、三重差分、弱工具变量或 AER/AEJ 风格实证论文 -> `empirical-quant` route 和 `quant-analysis`。必须读取 `empirical_quant_workflow.json`，先声明任务是描述、相关、预测还是因果；涉及因果、影响、机制、政策效果或处理效应时，先通过 `causal_identification_checked`，不得把模型运行、显著性或语言润色替代识别策略、诊断和稳健性。AER/经济学/Stata 只是条件增强，不是所有社科任务的默认；Stata 输出必须可追溯到 do-file、日志和表图输出路径。
- 换会议、改投别家、转投、重投、投稿格式迁移或目标模板迁移 -> `social-science-submission-package` route 和 `social-science-submission-packager`。先建立目标要求清单，区分机械格式迁移和实质改稿；不得只替换模板后宣称 ready。
- 审稿工作流 -> 必须参考 `peer_review_workflow.json`。外部仓库的优点只作为模式吸收：专项问题账本、领域化 reviewer card、full-text reading gate、独立 subtle logic flaw audit、reviewer independence、response tracker 和 action mapping；不得整包安装外部审稿系统，不得让 reviewer 直接改主产物。
- 项目收尾复盘、对话流总结、技能演化判断和 Obsidian 沉淀 -> `project-retrospective-evolver -> research-stack-manager / obsidian-research-sync`
- `local-cloud-router` 是 helper，不是用户主入口
- `skill-vetter` 只在第三方组件取舍时触发
- CNKI 批量下载到 Zotero -> 先走 `reference-fulltext-acquisition` 下的授权下载子链：用户真实 Chrome 登录态、扩展、已有标签页、下载目录或可视下载按钮能由官方 Chrome/Computer Use 处理时，优先用原生能力；需要指定项目下载目录、批量断点续跑、候选 gate、验证码 checkpoint 或可复现编排时，再用 `envctl cnki-zotero find/fetch/browser-download` 和可控 Chrome/CDP。`cnki-mcp` 只在实时冒烟测试通过后作为临时候选传感器。`envctl cnki-zotero ingest-plan` 生成导入计划，Zotero 写入走官方 Zotero 插件或本地 connector，并必须显式执行。项目任务必须下载到项目自己的 `outputs/inbox/cnki-downloads`；不得保存 cookies，不得绕过登录、验证码或访问权限。遇到滑块或安全验证时写入 `captcha_checkpoint`，用户在可见浏览器手动完成验证后，从报告里的 `resume_candidates` 继续。
- CNKI “作者 + 单位”任务 -> 下载前必须核验作者单位。不得用作者检索排序结果直接代表指定单位作者，也不得用全文混合检索替代作者单位过滤。
- Google Scholar -> 做候选发现、引文线索和公开学术检索证据。优先 `google-scholar-mcp`，备用 `paper-search-mcp`；不要把浏览器 Scholar 页面作为高频自动化入口。正式引用仍走 citation gate 和 Zotero；Google Scholar 记录本身可以作为 DOI 豁免证据，但不能替代作者、年份、题名和来源核验。
- 参考文献全文 PDF 获取 -> 统一走 `reference-fulltext-acquisition`。CNKI、Google Scholar、OpenAlex、Semantic Scholar、浏览器和 Zotero 都只是该流程调用的工具层，不得各自直接接管全文获取。

## Evidence-Based Literature Workflow

当用户要求“筛选参考文献”“生成候选文献表”“开始结构性阅读”“结构化阅读”“文献核验”“证据核验”“引文核验”“引用核验”“正文引用是否支撑”“标注证据句”或“输出证据包”时：
1. 选择 `evidence-based-literature-workflow` route 和 skill。
2. 如果用户已有实证/实验结果、论文框架、题目、摘要或选题来源文献，先围绕理论基础、研究现状、方法或主要变量建立候选文献表。
3. 默认先筛约 50 篇：中文约 20 篇、英文约 30 篇，优先高被引正式文献；正式纳入默认必须有 SCI、SSCI 或 CSSCI 来源证据。
4. 构成选题的来源文献默认进入候选池，并先查它们引用的文献和引用它们的文献；若来源文献没有 SCI/SSCI/CSSCI 证据，先放入背景或人工复核清单，除非用户明确批准豁免。
5. 先按题目、摘要、关键词、期刊或来源、被引信号和与本文关系筛选，再尝试获取候选文献 PDF；不能获取的单独列清单。
6. 先建候选池和元数据核验表，再取得并校验全文 PDF；不要直接从搜索结果写综述。
7. 写作前必须形成结构性阅读表；正文引用核验必须使用 cited source 的正文完整句作为证据。
8. 如果任务只剩单点 DOI 查验、单纯 PDF 下载或纯导出，再降级到对应子 skill。

## Empirical Quant Workflow

当用户要求量化研究、实证分析、回归、面板模型、DID、IV、RDD、PSM、SCM、DML、事件研究、稳健性、异质性、机制、复现包、AER/AEJ 风格实证论文，或需要把模型结果写成论文段落时：

1. 选择 `empirical-quant` route 和 `quant-analysis` skill。
2. 先读取 `empirical_quant_workflow.json`，不要只靠一个简短量化 skill 判断。
3. 先确认任务性质：描述、相关、预测或因果；如果语义模糊，必须问用户是否要使用因果表述。
4. 先锁定研究问题、分析单位、样本、变量、估计目标、处理或解释变量、控制变量、时间窗口、聚类层级和数据路径。
5. 如果涉及因果表述，必须选择设计家族并完成 `causal_identification_checked`：估计目标、识别假设、处理/分配机制、诊断计划、红线检查、稳健性矩阵和因果表述边界。
6. 外部 AER/StatsPAI/Full Empirical Analysis 的优点只作为本地合同吸收：识别优先、现代 DID/IV/RDD/shift-share/SCM 诊断、Stata do-file 生态、稳健性矩阵、复现包纪律和结果解释边界。不得把外部 DSL 或自动包当作无需审计的黑箱。
7. 如果用户要求“降 AIGC”“去 AI 味”“deslop”或“stop slop”，只允许在结论、结果、变量、估计值、引用和局限已经锁定后调用 `academic-humanization-studio` 做表层审计；不得为了像人工写作而改变事实、数据、模型输出或引用，也不得承诺检测绕过。
8. 量化图表进入 `figure-table-studio`；正式写作进入 `manuscript-writing-studio`；投稿和复现包进入 `social-science-submission-packager` 或 `reproducibility-package`。

## Peer Review Workflow

当用户要求审稿、顶刊级内审、投稿前审查、大修前内审、回复审稿、返修核验或送审包总审时：
1. 先读取 `peer_review_workflow.json`，选择一个明确模式：`standard_single_review`、`top_journal_internal_review`、`revision_response_review`、`submission_package_review` 或 `domain_calibrated_review`。
2. 普通单篇评审走 `standard_single_review`，不默认真实拆成多 agent；它仍必须输出已读边界、问题账本、细微逻辑漏洞审计和综合判断。
3. 顶刊级内审、投稿前审查、图表复现审计或用户明确要求多 reviewer 时，升级为 `top_journal_internal_review`，可以使用 subagent，但 reviewer 必须直接读主材料，不能只读主线程总结。
4. 有审稿意见、response letter、rebuttal 或 revise and resubmit 时，优先走 `revision_response_review` 和 `reviewer-response-pack`，逐条保留审稿意见、稳定编号、动作映射、真实修改位置和缺失作者信息。
5. 送审包、投稿包、定稿冻结或复现包核验走 `submission_package_review` 和 `social-science-submission-packager`，不得只做文字润色后宣称 ready。
6. 所有模式都受 `peer_review_protocol_checked` gate 约束；缺少 `logs/quality-gates/peer-review-report.json` 或关键 check 未通过时，不得把审稿链标成 pass。
7. 整篇审稿或投稿前内审要区分致命问题、可修复问题和表层问题；评分或推荐必须有明确依据，不能用固定严苛模板替代具体判断。
8. reviewer 不得直接覆盖主稿、图表、数据、代码或参考文献；如需修改，转入写作或项目执行链并保留人工检查点。

## Environment Ops

当任务属于 Python、Git、PowerShell、Codex 配置、MCP profile、agent-browser 或 Jupyter 环境维护时：
1. 先读取 `routing_table.json`、`conflict_matrix.json`、`settings.toml` 和目标 profile。
2. 先运行或参考 `scan_research_stack.py` 与 `validate_research_stack.py`。
3. 比较 `profiles/*.toml`、`config.toml`、`.codex/skills`、插件源目录和 catalog。
4. 说明配置漂移，再执行最小必要变更。
5. 修改运行态 `.codex` 后，如果需要重启 Codex，必须明确说明。

## Subagent Delegation

当任务可以拆分时，优先把上下文重的工作交给子 agent 或并行 agent：

1. 给每个 agent 写清楚任务、范围、项目根目录、可读材料、禁止写入范围、可用 skill/MCP/plugin、必须迭代到什么程度、验收方式和回报格式。
2. 子 agent 的输出必须是可整合报告：发现、证据、操作记录、失败点、风险、建议下一步；不要只给一句结论。
3. 主 agent 不把所有原始检索、长文阅读、文件盘点和重复测试塞进主上下文；主上下文只保留路线、关键证据、决策和下一步。
4. 主 agent 必须审查子 agent 报告之间的冲突，必要时继续分派二轮任务。
5. 涉及删除、覆盖、运行态配置、凭据、隐私材料和正式引用的关键动作，必须由主 agent 复核并按全局约束执行。

## Writing Tasks

当选中的路线属于写作、导出、回复审稿或修改稿时：
1. 先触发 `manuscript-writing-studio` 判断任务是起草、重写、润色、中英转换还是定稿检查。
2. 先声明语言目标和学科目标：英文期刊可更积极借鉴 Nature-style；中文期刊以本地中文社科规则为主；计算社科/方法技术型文章可借鉴技术论文的 pipeline 和复现表达；传统量化和质性研究以本地社科逻辑为主。
3. 如果是中英转换、缩写、扩写、去 AI 味、降 AIGC 或逻辑检查，先声明输出容器和修改幅度：LaTeX 输出保留命令并转义特殊字符；Word/纯文本不得带 Markdown 或错误转义；微调不能删除事实、变量、结果、引用、边界和不确定性。去模板化任务先用 `academic-humanization-studio` 生成 locked-items ledger、issue ledger、修改日志和二次复查，不把检测分数作为通过标准。
4. 如果用户要求投稿前润色、目标期刊适配或按期刊风格修改，先触发 `target_journal_adaptation` 模式：优先用 5 到 8 篇可读目标期刊近作生成风格卡和期刊画像；没有可读语料时只能做保守润色并标明限制。目标期刊画像只能校准结构、语气、段落顺序和表达强度，不能改事实、结果、引用和证据边界。
5. 如果写作会新增、删除、重排或改变引用性断言，再触发 `writing-reference-capture`。
6. 识别这次写作里实际用到的论文。
7. 只保留引用证据可核验且真实性可确认的条目；DOI 有则核验。无 DOI 时，只有用户提供来源、完整 PDF 原文或公开学术检索记录可审计，才可进入正式写作链。
8. 优先使用 Zotero 本地 connector 直写。
9. 如果存在现成项目 collection，就直接复用。
10. 如果不存在现成 collection，则按规则：
   - 允许降级时回退到 library root
   - 不允许降级时明确返回阻塞
11. 在正式导出前，必须检查 `writing_quality_checked` gate，并以 `logs/quality-gates/writing-quality-report.json` 作为 canonical 报告：
   - `style_calibration`
   - `argument_chain_closure`
   - `citation_alignment`
   - `empty_phrase_scan`
   - `section_logic_reader_flow`
   - `direct_argument_progression_checked`
   - `four_sentence_storyline_checked`
   - `method_transition_continuity_checked`
   - `language_target_declared`
   - `discipline_style_declared`
   - `claim_strength_and_boundary`
   - `contribution_posture_checked`
   - `section_job_checked`
   - `results_discussion_boundary`
   - `polishing_failure_mode_diagnosed`
   - `title_abstract_searchability_checked`
   - `sentence_paragraph_control`
   - `rhythm_variety_checked`
   - `reader_facing_terms_checked`
   - `format_container_preserved`
   - `minimal_delta_or_rewrite_scope_declared`
   - `humanized_surface_without_claim_change`
   - `data_bound_results_analysis`
   - `target_journal_style_profile_checked`
   - `venue_migration_checklist`
12. 如果写作质量 gate 未通过，不得把状态写成 `pass`，必须停留在 `revise` 或 `block`。
13. 完成 Zotero / Obsidian 同步和写作质量检查后，再进入：
   - `research-docx-export`
   - `reviewer-response-pack`
   - `latex-paper-conversion`

## Reference Fulltext Acquisition

当用户要求“补齐全文 PDF”“下载参考文献原文”“从参考文献表收集 PDF”“Google Scholar 右侧 PDF”“CNKI 批量下载论文”或“整理已取得/缺失全文清单”时：
1. 选择 `reference-fulltext-acquisition` route 和 skill。
2. 先建立 `reference_download_status.csv`，不要直接开始下载。
3. 先核验 DOI 与元数据；没有 DOI 时记录 DOI 豁免依据。英文或国际文献先用 OpenAlex / Crossref / Unpaywall / Semantic Scholar 批量尝试开放全文，没有取得可校验 PDF 时默认进入 Google Scholar 逐篇精确题名检索，优先右侧 `[PDF] domain`；CNKI 走授权下载，用户原件走 PDF 校验。
4. 下载文件默认进入项目输出区；CNKI 专项仍用 `<project_root>\outputs\inbox\cnki-downloads`。
5. PDF 通过文件头、页数、题名/DOI/元数据校验后，才写入“已取得”。
6. 结束时必须输出已取得清单、缺失清单、PDF 校验报告和必要的 Zotero 导入计划。
7. 正式写作引用仍回到 `citation-verifier -> zotero-sync -> writing-reference-capture`；用户提供来源、完整 PDF 原文或公开学术检索记录可作为 DOI 豁免证据；证据材料里出现 DOI 时仍必须核验。

## Research Figure Design

当用户要求“画论文图”“科研绘图”“顶刊风格图”“机制图”“概念框架图”“流程图”“研究设计图”“多面板图”“结果图”“用 image2 画科研图”或明显想把图用于论文、报告、答辩、审稿、投稿时：
1. 选择 `research-figure-design` route 和 `research-figure-studio`。
2. 先判断图型：经验结果图、机制图、概念框架图、流程图、研究设计图、网络图、文本分析图、ABM/仿真图或多面板证据图。
3. 先形成 figure brief：图的用途、论文主张、数据或概念依据、面板计划、全部文字标签、连接线含义、风格预设、配色、输出格式和风险检查。
4. 正式科研图默认使用 `social_science_nature_red_blue_rainbow`，真实数据图默认使用 `nature_empirical_red_blue_rainbow`，投稿审稿图默认使用 `minimal_review_ready_red_blue`，研究汇报图默认使用 `presentation_premium_red_blue_rainbow`。这些预设来自 `figure_style_presets.json`；不得只写“Nature 风格”“顶刊风格”或“高级一点”。
5. 默认审美不是简陋黑白图，而是白底、高留白、细线条、红蓝主轴彩虹色系；红蓝表达主要对比，青色、橙色、琥珀色、靛蓝等彩虹色只用于分组、梯度、地图和多系列图。灰度可读只是审稿安全检查。
6. 对 Excel、CSV、模型输出或真实数据图，先读取 `scientific_figure_workflow.json`：正式图默认先做数据体检，保留 process_data，按中英文字体 fallback、字号、图幅、DPI、统计标注和图注规则执行。
7. 不得因为科研图或论文图而拒绝 image2。机制图、概念图、流程图、研究设计图和非数值科研插图可以用 image2；精确数据图、回归图、事件研究图和系数图先用代码或可编辑工具控制数据。
8. 调用 image2 前必须锁定结构和文字，并写入预设要求：红蓝主轴 Nature-style 彩虹色系、高级社科期刊图、白底、高留白、无图名、无长图注、无元素重叠、文字按给定内容拼写、不得编造经验数据。
9. 图像输出后必须检查文字可读性、箭头关系、面板结构、元素重叠、灰度可读性、数据真实性、字体字号和图注证据链；图名、长图注、数据来源、样本说明、模型说明和脚本路径放在正文或交付说明，不放在图片内部。未通过则修图，不得把状态写成完成。
10. 如果是投稿包或完整论文图表组，`social-science-submission-packager` 仍是总控，`research-figure-studio` 和 `figure-table-studio` 是图表子链。

## Research Presentation

当用户要求“做 PPT”“做幻灯片”“答辩汇报”“开题/中期汇报”“路演”“网页 PPT”“论文转 PPT”“Swiss Style”“杂志风 PPT”或明显要做演示文稿时：
1. 选择 `research-presentation` route 和 `research-presentation-studio`。
2. 先确认输出格式：HTML web deck、PPTX，还是两者都要；如果用户已经明确，就直接记录假设。
3. 默认按 guizang-ppt-skill 的两套视觉系统做：人文叙事和行业观察用“电子杂志 × 电子墨水”；数据、方法、工具链和计算社科汇报用“瑞士国际主义”。
4. 生成前先做 slide manifest：页码、页面目的、版式、图片槽位、证据来源、输出格式和风险边界。
5. HTML web deck 使用 `$CODEX_HOME/skills/guizang-ppt-skill` 原版 skill 的模板、版式、主题、截图和配图规则；瑞士风必须运行它自带的 `validate-swiss-deck.mjs`。
6. PPTX 使用官方 `Presentations` 插件，但仍遵守同一套视觉、版式、图片和证据边界。
7. 用户截图需要保真时，先按截图适配规则处理，不默认重画；需要生成配图时可以用 image2，但必须先锁定比例、文字语言和禁止编造项。
8. 如果演示文稿里包含正式论文图表，图表本身仍要回到 `research-figure-studio` 或 `figure-table-studio`；如果涉及正式引用，仍回到 `writing-reference-capture` 和 citation gate。

## CNKI To Zotero Controlled Ingest

当用户要求“知网批量下载”“CNKI 文献进 Zotero”或提到浏览器批量下载脚本时：
1. 先说明能力边界：这是 `reference-fulltext-acquisition` 下面的 CNKI 授权下载子链。真实 Chrome 登录态、扩展、已有标签页、浏览器下载和可视点击优先使用官方 Chrome 插件和 Computer Use；需要项目下载目录控制、批量断点续跑、候选 gate、验证码 checkpoint 或可复现编排时，再使用 `envctl cnki-zotero` 和可控 Chrome/CDP。`cnki-mcp` 只在实时冒烟测试通过后作为临时候选传感器。Zotero 写入走官方 Zotero 插件或本地 connector，并必须显式执行。
2. 使用合同：`<VELA_RUNTIME_ROOT>/skills/catalog/cnki_zotero_workflow.json`。
3. 项目任务默认下载收件箱：`<项目根目录>\outputs\inbox\cnki-downloads`。该目录在项目 git ignored 输出区内。环境级收件箱只用于环境冒烟测试或无项目上下文维护。
4. 先检查运行依赖和可控 Chrome/CDP，区分“缺依赖”和“Chrome 端口未启动”：

```powershell
python -m skills.scripts.envctl cnki-zotero status --check-cdp --cdp 9333 --project-root "C:\path\to\project"
```

`missing-python-dependency:websocket-client` 表示当前 Python 环境缺少直连 CDP 依赖；`cdp-endpoint-unreachable` 表示依赖存在但专用可控 Chrome 尚未启动或端口不对。不能用开放可见检索替代正式 CNKI/CSSCI 候选 gate。

5. 如需准备收件箱，运行：

```powershell
python -m skills.scripts.envctl cnki-zotero status --project-root "C:\path\to\project" --ensure-inbox
```

6. 如果用户限定作者单位，先做候选 gate：候选必须带有高级检索作者+单位证据、详情页作者单位、CNKI 导出元数据，或项目人工核验清单。证据不足时停止，不进入下载。
7. 用户在 Chrome 中登录 CNKI 后，优先让 Codex 使用官方 Chrome 插件或 Computer Use 操作这个已登录 Chrome。只有需要受控下载目录、批量恢复或 CDP 级调试时，才使用 `browser-probe`、`browser-download`、agent-browser 或直接 Chrome DevTools Protocol：

```powershell
python -m skills.scripts.envctl cnki-zotero browser-probe --project-root "C:\path\to\project"
python -m skills.scripts.envctl cnki-zotero browser-download --input candidates.json --author "作者" --affiliation "机构" --project-root "C:\path\to\project" --output auto
```

8. 如果需要由环境直接完成“检索 -> 候选核验 -> 批量下载”，日常入口使用 `fetch`。检索字段用 `--field`，可为 `author`、`subject`、`keyword`、`title`、`affiliation`、`fulltext`、`doi`；排序用 `--sort`，可为 `cited`、`latest`、`relevance`、`download`、`composite`。示例：

```powershell
python -m skills.scripts.envctl cnki-zotero fetch --query "工程控制论" --field subject --sort latest --limit 10 --project-root "C:\path\to\project" --cdp 9333
python -m skills.scripts.envctl cnki-zotero fetch --author "陈云松" --affiliation "南京大学" --field author --sort cited --pages 2 --limit 10 --project-root "C:\path\to\project" --cdp 9333
```

9. 只做候选发现、不下载全文时，使用 `find`，再让用户或后续 gate 审查候选 JSON。
10. 如果官方 Chrome 插件或普通 Chrome 因默认资料目录限制无法提供可控项目下载目录，启动专用 CNKI 可控窗口：`powershell -ExecutionPolicy Bypass -File skills\scripts\open-cnki-controlled-chrome.ps1`。用户只需在该窗口登录 CNKI 和处理验证码；随后用 `browser-download --direct-cdp --cdp 9333` 或 `fetch --cdp 9333` 下载到项目收件箱。
11. 如果报告出现 `captcha_checkpoint`，不要从头重跑。用户手动完成 CNKI 验证后，把上一份报告作为输入继续：

```powershell
python -m skills.scripts.envctl cnki-zotero browser-download --input "C:\path\to\project\outputs\reports\cnki-zotero\YYYY-MM-DD.json" --project-root "C:\path\to\project" --direct-cdp --cdp 9333 --output auto
```

12. 如果原生 Chrome/Computer Use 和可控浏览器都不可用，才退回用户已安装的批量下载脚本；下载目标仍必须是项目收件箱。Codex 不保存 cookies 到仓库，不自动拖动验证码，不绕过访问限制。
13. 下载后运行：

```powershell
python -m skills.scripts.envctl cnki-zotero ingest-plan --project-root "C:\path\to\project"
```

14. 对 PDF，按报告中的 Zotero 导入计划使用官方 Zotero 插件或本地 connector 从文件添加附件；对有 DOI 的条目优先补充 DOI 元数据；对 CAJ 保持人工复核或用户批准的转换路径。
15. 写入 Zotero 后用官方 Zotero 插件或本地 connector 刷新/搜索确认标题或 DOI。

这个链路只把下载文件作为本地证据和附件处理。正式参考文献仍需 `citation-verifier -> zotero-sync -> writing-reference-capture`；用户提供来源、完整 PDF 原文或公开学术检索记录可作为 DOI 豁免证据；证据材料里出现 DOI 时仍必须核验，并记录基础元数据。

## Output Contract

说明卡之后，继续给出：
1. 本次选中的 route
2. 本次选中的 leaf skills
3. 本次建议启用的 profile
4. 现在立刻执行的第一步动作

如果进入项目型多 agent 规划，还必须继续给出：
5. `Agent Dispatch Card` 的最小字段：
   - `run_id`
   - `route_id`
   - `route_confirmation_required`
   - `route_confirmation_question`
   - `user_confirmed_route`
   - `execution_mode`
   - `agents`
   - `agent_context_packet`
   - `allowed_skills_mcp`
   - `agent_output_path`
   - `review_agents`
   - `handoff_log`
   - `gate_log`
6. 说明 canonical 文件落点：
   - `.codex/dispatch/<run_id>.yaml`
   - `.codex/context-packets/<run_id>/<agent_id>.md`
   - `outputs/agent-runs/<run_id>/<agent_id>/`
   - `logs/agent-handoffs/<run_id>.md`
   - `logs/quality-gates/<run_id>.md`

默认由 `research-team-orchestrator` 负责把这些字段写成可校验的 dispatch artifact，而不是在对话里停留在口头分工。

不要把技能选择权重新抛回给用户，除非用户明确要求手动覆盖。
