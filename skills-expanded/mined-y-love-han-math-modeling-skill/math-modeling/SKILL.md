---
name: math-modeling
description: "Execute and audit complete mathematical modeling competition workflows with the evidence-first mmflow runtime as the single source of truth, plus adaptive data analysis, model selection, validation, publication, presentation, privacy, reproducibility, and compliance templates. Use for 数学建模、数模、赛题、CUMCM、MCM/ICM、GMCM、MathorCup、APMCM、深圳杯 or any contest task involving problem selection, data analysis, model construction, validation, paper writing, review, packaging, defense preparation, auditing, or workflow recovery."
---

# 数学建模自主全流程整合版

## 1. 任务定位

使用本 Skill 完成从赛题读取到本地交付的完整数学建模竞赛流程。以证据链、可复现性、题型适配、论文一致性、合规性和可审查性为首要目标；以高水平竞赛作品为质量方向，但不承诺原创性、评委接受度、奖项或任何外部检测结果。

将 `scripts/mmflow.py` 作为唯一事实入口。状态、事件账本、Registry、Lineage、stage_epoch、门禁、回退、受控执行、复现、审查关闭、隐私扫描、打包和发布标签都必须由它计算或登记。Markdown、文件名、关键词、文件大小、截图和模型自报均不能单独证明阶段完成。

把本 Skill 安装目录与具体比赛项目根目录严格分开。所有题目文件、数据、代码、实验、稿件和交付包写入用户授权的项目根目录；不要把比赛产物写入本 Skill 目录，不要把 `.mmflow` 事件或状态当作普通文本手工修改。

## 2. 不可逾越的规则

1. 读取题目原文、全部可用附件、补充说明和适用的当届官方规则；当届一手规则优先于往届经验和本 Skill 的通用建议。
2. 区分题目事实、数据事实、外部文献、数学推导、模型输出、实验观察、专业判断、假设和建议；为关键内容登记来源与适用范围。
3. 禁止编造数据、引用、运行、数值、图表、统计显著性、定理条件、最优性、复现事实、许可或外部工具结果。
4. 禁止把调试、demo、fixture、旧尝试、归档、未核验来源或陈旧证据用于论文生产主张。
5. 禁止直接写入 `PASSED`、`COMPLETE`、发布标签、门禁结果或审查关闭状态；只能调用受控命令，请程序判定。
6. 禁止用未来阶段证据、回退前旧 epoch 证据、来源阶段未通过的证据或与当前项目无血缘的产物过门禁。
7. 禁止删除失败尝试、矛盾结果、审查 finding 或日志来美化过程；修复必须产生新 attempt、execution、证据或关闭记录。
8. 禁止为了固定页数、图表数量、三维图数量、算法数量、检验名称、引用数量或创新数量注水；适用的官方格式和真实信息需求优先。
9. 禁止将复杂度、术语数量或模型数量当作质量；先排除泄漏、单位错误、不可识别、不匹配、不可复现和约束违规。
10. 门禁失败时修复最上游根因或回退，不得改阈值、扩大容差、替换规则或将 `ERROR`、`BLOCKED`、未知状态解释成通过。
11. 记录简洁的决策摘要、备选方案、证据、风险和撤销条件；不要求暴露隐藏推理过程。
12. 未获明确授权时，不执行外部提交、上传、付费、受限登录、发送消息、披露参赛者身份或改变任务范围外系统。

## 3. 启动、恢复与主循环

在每次进入任务或切换会话时执行以下循环：

1. 确定并验证项目根目录；确认本 Skill 根目录和比赛项目根目录不是同一目录。
2. 运行 `python <skill-root>/scripts/mmflow.py doctor --project <project-root> --json`，读取能力、依赖、路径和隔离等级。目录级受控执行不是操作系统沙箱；不得把它描述为阻止网络、项目外文件访问或子进程逃逸的强隔离。
3. 若项目尚未初始化，先清点材料，再运行 `init`；若存在旧契约，先运行 `migrate --dry-run`，确认迁移计划后才迁移；已初始化项目运行 `resume`。
4. 运行 `status --project <project-root> --json` 和 `next --project <project-root> --json`，只执行程序返回的唯一活动阶段或下一合法阶段。
5. 按 `next` 给出的资源路由读取当前阶段所需参考，不一次加载全部长文档；若需要深度方法或冲刺节奏，再读取两个扩展参考的相关小节。
6. 完成当前阶段的专业工作，登记输入、决策、候选、实验计划、风险和撤销条件。
7. 用 `register-*` 登记真实的输入、artifact、split、result、claim、formula、citation、figure、finding 和 evidence；execution 只能由 `run` 命令受控产生（没有 register-execution，手工登记会被拒绝）。确保含 `created_stage`、`stage_epoch`、账本序号和血缘。
8. 所有进入论文或交付包的计算使用 `run --class production`，从新 attempt 或空目录执行，并绑定代码、配置、输入、环境和输出。
9. 运行 `gate <stage> --project <project-root> --json`，同时读取结构化报告和人类可读报告；修复最上游失败原因。
10. 门禁通过后运行 `advance`；上游决定变化时运行 `rollback`，让程序传播陈旧状态并递增 `stage_epoch`，不得手工跳阶段。
11. 长阶段或上下文切换前运行 `checkpoint`；恢复会话先运行 `resume`、`status` 和 `next`，不凭记忆继续写稿。
12. 需要弃用根因实体时运行 `invalidate --id <entity_id> --reason <reason>`；不要直接改 Registry 单个实体的状态。
13. 阶段收尾和交付前运行 `audit`，逐项读取 integrity、lineage、evidence、scientific-bindings、publication、compliance、review、delivery 和 release-status 分域。工作流未 COMPLETE 时 release-status 分域预期为 FAIL（标签 NOT_READY）、聚合退出码为 3，这是设计行为而非完整性故障；此时只需确认其余分域为 PASS 即可继续当前阶段，不得据此回退。
14. 直到 P11 通过并由状态机返回 `COMPLETE`，或形成合法 `BLOCKED` 报告；发布前运行 `release-status`，只接受程序计算的标签。

## 4. P0–P11 主路由

| 阶段 | 目标 | 主要参考 |
|---|---|---|
| P0 | 启动、能力、赛事识别、当届规则 | `references/workflow-contract.md`、`references/competition-compliance.md` |
| P1 | 材料清点、附件完整性、选题决策 | `references/problem-formalization.md`、`references/data-and-literature-governance.md` |
| P2 | 需求矩阵、问题契约、歧义、依赖 DAG | `references/problem-formalization.md` |
| P3 | 数据、文献、质量、划分、泄漏治理 | `references/data-and-literature-governance.md` |
| P4 | 基线、候选模型、假设、实验、冻结计划 | `references/model-selection.md`、`references/validation-by-model-type.md` |
| P5 | 建模、算法、求解、结构化结果 | `references/model-selection.md`、`references/evidence-and-claims.md` |
| P6 | 题型适配验证、稳健性、不确定性、反证 | `references/validation-by-model-type.md` |
| P7 | 逐问答案、结果选择、主张登记 | `references/evidence-and-claims.md` |
| P8 | 论文、图表、表格、引用、支撑材料 | `references/paper-and-visuals.md`、`references/competition-compliance.md` |
| P9 | 空目录隔离复现、结果比较、漂移处理 | `references/evidence-and-claims.md`、`references/review-recovery-and-defense.md` |
| P10 | 多角色对抗审查、finding 关闭、质量审计 | `references/review-recovery-and-defense.md`、`references/competition-compliance.md` |
| P11 | 隐私扫描、打包、校验和、答辩材料 | `references/competition-compliance.md`、`references/review-recovery-and-defense.md` |

没有选题、附件数据或答辩环节时，登记带证据的 `NOT_APPLICABLE`，不要用自然语言跳过阶段。状态机可能使用 `NOT_STARTED`、`ACTIVE`、`GATE_FAILED`、`PASSED`、`INVALIDATED`、`BLOCKED`、`INTEGRITY_FAILURE` 和 `COMPLETE`；任何时刻最多一个主阶段为 `ACTIVE`。

## 5. 各阶段执行要点

### P0：启动与规则

- 创建唯一 `run_id` 和策略锁，确认账本、Registry、项目路径和写入锁可用。
- 核验 Python、表格、PDF、LaTeX 能力并登记缺失项及其影响；doctor 默认零外部流量，网络连通性用 `--probe-network` 显式探测，独立审查能力由用户在 P0/P10 如实申报。
- 从主办方一手来源核验当届页数、匿名、命名、附件、支撑材料、AI 使用披露、答辩和提交要求。
- 将未核实冲突登记为红线；不要用往届规则补齐。

### P1：材料与选题

- 对题目、附件、说明、数据字典和补充文件计算哈希，记录读取状态、编码、损坏、扫描页和隐藏内容。
- 多题赛事按价值、数据、可验证性、计算可行性、差异化空间和风险形成可追溯比较；单题赛事登记选题不适用。
- 缺附件时先判断是否有公开且许可清晰的替代来源；关键材料仍不可得才阻塞。

### P2：形式化

- 把显性和隐含要求绑定到赛题来源位置；为每问建立 Problem Contract。
- 明确任务、输入、输出、变量、约束、单位、时空尺度、评价指标、claim 类型、外推边界和小问依赖。
- 对关键歧义建立可检验解释分支；区分预测、因果、优化、理论、仿真和综合评价标签。

### P3：数据与文献

- 保留原始数据只读副本，登记来源、许可、时间、字段、单位、版本和哈希；记录清洗、派生、连接、筛选和划分血缘。
- 在正确的数据边界内拟合会学习分布的预处理；按时间、主体、群组、空间和重复测量结构设计 split。
- 区分错误值、异常值和稀有真实值，报告处理对结果的影响；文献逐条核验元数据、支持位置、版本和撤稿状态。
- 无数据题登记公开数据、文献数据、机理参数或仿真生成协议，不能把合成数据写成真实观测。

### P4：模型与实验设计

- 先定义与题型匹配的最低合理基线，再形成少量结构不同、可证伪的候选。
- 按合法性与题目匹配、证据支持、任务表现和简约性选择；不能用固定总分掩盖硬约束或识别问题。
- 在查看最终测试结果前冻结指标、split、基线、验证、选择规则、随机性、容差和停止条件。
- 若启用 `adaptive`、`evidence-first`、`deep-insight`、`competition-sprint`、`presentation-ready` 或 `special-prize`（证据要求最严）profile，在 P4 登记适用理由、未启用项和降级条件；profile 只能增加审查，不能降低核心门禁。

### P5：实现与求解

- 先运行基线，再实现候选和主模型；每次执行使用新 attempt、execution、输入闭包和输出目录。
- 结构化记录指标、数组、单位、场景、样本量、定位、随机种子、求解状态、可行性和已知解对照。
- 保留不收敛、效果变差和失败执行；可行解不等于全局最优，按算法类型报告正确性证据。

### P6：验证与反证

- 按 Problem Contract 的 traits、claim_types 和 model_families 选择适配验证：时间回测、群组隔离、校准、因果识别、优化界、收敛、守恒、边界、退化、零模型、敏感性、不确定性或仿真误差。
- 核对验证方法前提、单位、评价方向、数据依赖和实际效应；主动寻找能推翻模型或改变建议的场景。
- 不支持的主张删除、降级或回退；不要用更多图表掩盖失败。

### P7：结论与主张

- 每项赛题要求映射到明确答案、证据和论文位置；每个数字使用 `result_id`，每个核心结论使用 `claim_id`。
- 派生比例、差值和排名由绑定结果重新计算；区分计算、观察、推断、理论、外部、建议和限制主张。
- 只把证据充分的实质贡献写入摘要和结论；矛盾结果保留并解释、降级或触发回退。

### P8：论文与图表

- 从 Registry 生成数字、表格和图形，使用 `MMResult`、`MMClaim` 或等价显式绑定；扫描未绑定科学数字。
- 每张图登记必要问题、源结果、claim、图注和解释动作；二维、表格或文字能充分表达时不要强行使用三维。
- 检查摘要、符号、公式、小问衔接、图注、引用、贡献措辞、渲染一致性和当届格式；不以接近页数上限为目标。
- 稿件与 Registry 双向覆盖：有效 citation、figure、formula 和 claim 必须互相可定位，修改绑定后重新运行受影响门禁。

### P9：隔离复现

- 在新空 attempt 目录从冻结输入、代码、配置和环境闭包重跑核心结果；不要复用缓存、临时输出或原工作目录。
- 按冻结策略比较结构化结果、浮点容差、随机统计性质、图源数据和 PDF 结构；环境漂移必须属于预登记允许差异。
- 不能复现时失效根因 execution、传播后代陈旧状态并回退最早根因阶段；不得事后扩大容差。

### P10：对抗审查

- 分别执行赛题、数学数值、数据统计、复现和论文合规审查；每个角色提交独立结构化 `review_report`。
- 每个 finding 登记严重度、位置、影响实体、回退阶段、重跑范围和关闭证据；CRITICAL/MAJOR 必须清零，MODERATE 修复或降级关闭；关闭一律使用 `close-finding` 命令并附关闭证据文件。
- 关闭 finding 必须引用更晚的修复证据和通过门禁；真正独立审查不可用时披露独立性限制，不能声称盲审已完成。

### P11：交付

- 用 delivery manifest 显式列出 PDF、代码、配置、数据说明、复现说明和支撑材料；archive path 不得泄露项目内部绝对路径。
- 运行 `scan-privacy`，检查匿名、PII、EXIF、PDF 元数据、秘密、绝对路径、嵌套压缩包、许可和 smoke command。
- 只打包显式允许文件，不打包 `.mmflow`、归档、夹具、内部审查记录或身份信息；新包必须在新目录安全解压并核验。
- 最终包字节变化后重新执行 P11；赛事需要答辩时生成并登记答辩材料，不需要时登记规则化不适用。

## 6. 证据登记与血缘纪律

### 输入和数据

- `register-input` 只登记实际读取、可定位、带哈希和来源的题目、规则、数据或文献输入；只看到文件名而未读取内容时登记读取失败或待核验状态。
- 对每个数据集记录来源、许可、抓取/下载时间、版本、字段、单位、编码、缺失处理、去重策略和原始哈希。派生数据必须引用父数据和转换脚本，不允许只写“清洗后数据”。
- 每个 split 记录源数据集、划分类型、选择器或索引哈希、分组/时间边界、泄漏边界、预处理拟合范围和指纹。execution 与 result 引用真实 split 实体，不把字符串当作划分证据。
- 外部数据和文献使用前检查许可、版本和可访问性；不能分发的私有或受限数据不进入最终包，除非当届规则和许可明确允许，并在 manifest 中声明。

### 执行和结果

- production execution 必须绑定 source artifacts、代码哈希、配置哈希、输入哈希、环境闭包、随机种子、命令、工作目录、退出码和输出清单。
- result 必须包含 result_id、execution_id、指标定义、方向、数值或数组、单位、样本量、场景、split、随机性说明和文件定位。日志可以辅助诊断，不能替代结构化结果。
- 任何用于论文的数字都通过 result_id 引用；比例、差值、排序、排名和汇总值由绑定结果重新计算，禁止凭手抄数字保持“看起来一致”。
- artifact_class 一经登记不可从 demo、exploratory、fixture、external 或 unattested 改成 production。生产结果必须在冻结后从空 attempt 重新执行。

### 公式、图表、引用和主张

- formula 登记公式文本、变量定义、假设、推导来源、适用范围和稿件位置；数学符号改动后重新检查受影响 claim 和结果。
- figure 登记源结果、生成脚本、输入哈希、图注、单位、颜色含义、输出哈希和稿件位置。装饰图、重复图、无数据支撑的三维图不进入生产论文。
- citation 登记完整书目信息、核验方式、支持位置、版本/撤稿状态和被支撑 claim；未核验或无法访问的引用不能写成已确认事实。
- claim 登记类型、文字、支持的 result/formula/citation/evidence、适用范围、限制、反证和稿件位置。发现支撑不足时降低 claim、补证据或删除 claim。

### 失效传播

输入、代码、配置、split、execution 或关键假设变化时，让 `mmflow` 沿 Lineage DAG 传播 `STALE` 或 `INVALID`，再运行 `next` 得到最小重跑范围。不要只更新最终图或论文，绕过上游失效会使交付不可审计。
深度证据（定理、候选放弃、公式合法性、消融、反直觉、统一框架、机理解释、负面结果、论文深度审查、特等奖评估）在内容中引用的 `source_entity_ids`、`supported_claim_ids`、`alternative_evidence_ids` 是政策声明的血缘依赖；登记时 `supports` 必须与这些引用完全一致，被引用实体失效时深度记录一并失效。登记 `NOT_APPLICABLE` 的深度决定必须给出结构化 `not_applicable_detail`（判定依据、对质量判断的影响、是否需要替代验证），不能只写一句理由就跳过。

## 7. 受控 runner 与模板调用协议

1. 先用 `integrate_templates.py check` 验证 manifest；模板条目必须有唯一 id、相对安全路径、阶段、输入、输出、依赖、质量 profile 和 evidence_types。
2. 根据当前阶段和问题契约选择模板；先读取其入口、输入格式、输出格式、可选依赖和已知限制，不要把模板中的示例结果当成项目结果。
3. 复制模板时用 `copy <template-id> <destination> --root <skill-root> --project-root <project-root> --json`；项目根目录必须存在，目标不得已存在，不得写入 `.mmflow`，不得越出项目根目录。
4. 模板只提供骨架、检查器或可复用函数；必须补充题目特定实现、数据绑定、配置和测试。`production_eligible` 也不等于自动产生 evidence，仍需 production runner 和 Registry 登记。
5. 运行分析模板输出 EDA、敏感性、统计检验或极端测试报告时，记录真实输入、依赖版本、随机性、失败情况和输出哈希；没有适用性时登记 `NOT_APPLICABLE`，不要机械运行。
6. 运行论文模板前确认 P7、P8 绑定已通过；运行 PPT 模板前确认已登记的图表和结构化结果可供消费；运行 quality 模板后把结果当作风险信号，不作为外部检测证明。
7. 目标项目已有文件时，先创建新 attempt 或新文件名，再由状态机决定是否替换；模板工具不会覆盖已有文件，任何替换都必须保留原哈希和决策记录。

## 8. 模型选择、验证与失败诊断

### 选择顺序

对候选模型采用词典序判断：先检查题目匹配、合法性、识别条件和泄漏风险，再看证据支持、可解释性、验证可行性、性能和计算成本。不得用单一综合分数抵消硬约束或把复杂度当作优点。

### 基线和候选

- baseline 需足够简单、可解释、可复算，并与主模型共享题目边界、数据边界、split 和评价指标。
- 候选模型数量以解决不确定性为限；每个候选说明假设、预期优势、代价、失效条件和最小区分实验。
- 只有在冻结规则允许的情况下比较最终测试表现；若看过结果后更改指标、split、模型选择或容差，登记为探索性或修订计划，不伪装成确认性分析。

### 失败诊断树

按以下顺序定位问题：

1. 输入：路径、编码、缺失、重复、单位、版本、权限和哈希是否正确。
2. 实现：索引、维度、广播、边界、约束、随机种子、文件输出和异常处理是否正确。
3. 数值：初始化、尺度、收敛、可行性、精度、溢出和停止条件是否合理。
4. 模型：假设是否可识别、机制是否匹配、参数是否有数据支持、外推是否越界。
5. 评价：指标方向、对照组、统计前提、实际效应和题目要求是否一致。

每一层都保留诊断证据和排除理由；修复失败后创建新的 execution，不把“最终运行成功”写成所有中间尝试都成功。

### 验证选择

- 时间结构优先使用时间回测或滚动评估；主体、群组、空间和重复测量结构优先按相应单位隔离。
- 概率结果检查校准、覆盖率或概率评分；因果主张登记 estimand、识别假设和敏感性，条件不足时只能写关联。
- 精确优化报告可行性、求解状态、界和 gap；启发式或随机算法报告种子、预算、稳定性和正确性对照。
- ODE/PDE 检查量纲、初边值条件、离散化、收敛、稳定性和适用守恒；仿真分别报告程序验证与模型验证。
- 综合评价检查指标方向、权重来源、敏感性、支配关系和排名反转；不确定性区分参数、抽样、测量、结构、情景和求解来源。

## 9. 原版优势的可验证整合映射

两个原版中有价值的“深度、反偷懒、表达和冲刺”能力均保留，但统一落到阶段、受控执行、Registry 证据和审查闭环；关键词、文件存在或自报分数本身不能替代证据。以下映射是可按题目启用的质量路径，不是对每道题强加同一套形式。

| 原版优势 | 整合版执行落点 | 可核验证据或审查 | 适用性与降级 |
|---|---|---|---|
| 统一数学框架、问题间耦合和跨问题迁移 | P2 建立依赖 DAG，P6/P7 检验跨问接口与机制 | `cross_problem_framework_record`、Problem Contract、Claim/Result binding | 只有存在真实共享变量、机制或决策接口时启用；否则登记 `NOT_APPLICABLE` 和替代证据 |
| 反直觉发现、矛盾敏感和异常追问 | P3 记录冲突与异常，P6 做反证和反套路候选，P7 量化其决策含义 | `counterintuitive_finding_record`、`counterevidence_report`、finding closure | 反直觉不是凭空制造；未被数据/推导支持时保留为失败候选或限制 |
| 定理匹配、理论深化和公式合法性 | P4 冻结适用条件，P5 推导和独立核验，P6 做边界/特例/数值检查 | `theorem_application_record`、`formula_validity_record`、formula binding | 定理条件不满足时降级为启发式或关联结论，不以定理名称充当深度 |
| 基线优先、候选淘汰和反套路设计 | P4 先基线，再比较少量结构不同候选并记录放弃理由 | `candidate_rejection_record`、`frozen_analysis_plan`、production results | 候选数量由不确定性决定；不使用固定算法数量或事后改规则 |
| 两轮自批判、审稿人视角和失败恢复 | P4/P6 保留第一轮风险、修复动作、第二轮复核；P10 以 finding/closure 固化 | `negative_result_record`、`review_findings`、`paper_depth_review` | 自批判写决策摘要和证据，不要求暴露隐藏思维；失败执行不得删除 |
| 消融、假设松弛、敏感性、Sobol/蒙特卡洛和 What-if | P5/P6 按不确定性来源选择实验，记录停止条件、误差和实际信息增量 | `innovation_ablation_record`、`validation_adapter_report`、`counterevidence_report` | 样本量和扰动范围由误差与预算决定；不机械复制固定次数或固定场景 |
| 负面结果、无效尝试和矛盾结果保留 | P5/P6 保留失败 execution，P7/P8 将其写入限制、回退依据或反证讨论 | `negative_result_record`、Lineage、claim limitations | “没有显著改善”也是结果；不能为了美化作品删除或改写成成功 |
| 机制解释、三层结果解读和数学美学 | P7/P8 连接数值事实、数学结构、数据机制、决策意义与统一符号叙事 | `mechanism_explanation_record`、`paper_depth_review`、formula/figure bindings | 数学美学属于专业判断；由结构简洁、符号一致、推导衔接和可读性支持，不是程序保证 |
| CP1–CP6 深度检查、阶段自检和反偷懒 | 在 P1–P8 使用阶段决策摘要、反证记录、审查 finding 和证据依赖承载实质检查 | 阶段 evidence、`review_findings`、P8/P10 门禁 | CP 标签只是工作提示，不能单靠关键词或字数通过；不把隐藏推理写成伪证据 |
| 高级视觉、3D 双视角、图表多样性和第一印象图 | P8 先登记问题、sidecar、源结果、Claim、图注和风险，再做实际尺寸渲染审计 | `figure_registry`、figure sidecar、`paper-and-visuals.md` | 只有真实三维语义和信息增量才使用 3D；不以固定页数、图数、算法数替代论证 |
| 三审三校、交叉引用、附录代码闭包和答辩准备 | P8/P9/P10/P11 做稿件双向覆盖、源闭包、渲染复核、审查关闭和答辩材料 | `manuscript_source`、`reproduction_report`、`review_report`、delivery manifest | 轮次、材料和语言由赛事规则及风险决定；不适用环节用有理由的 `NOT_APPLICABLE` |
| CP/冲刺时间管理、里程碑、断点和恢复 | `checkpoint`、`resume`、`next`、单活动阶段和最小重跑范围组成可恢复节奏 | ledger、stage epoch、checkpoint payload、workflow snapshot | 时间不足先保住题目响应、合法基线、核心验证、复现和合规，再削减装饰性增强 |
| 国赛/美赛/其他赛事适配、英文表达与 AI/查重代理 | P0 核验当届规则，P8/P11 按赛事适配器选择格式、语言、匿名和披露 | `competition_rules`、`compliance_report`、quality review reports | 代理检查只报告风险和范围，不能等同外部 AI 检测、查重或原创性结论 |

启用 `deep-insight` 或 `special-prize` 时，先在 P4 登记适用理由、未启用项、替代证据和降级条件；策略文件中的证据类型必须与真实 Registry 记录、当前 stage epoch、血缘和生产执行一致。`special-prize` 的评分只由 policy 和真实证据重算，任何标签或分数都不是奖项预测。

## 10. 论文、图表、复现和审查输出

### 论文生成

论文结构围绕“问题—假设—数据—模型—求解—验证—结果—限制—建议”展开。每一节都回答其证据来源和读者需要做出的判断；不要用泛化的“效果很好”“模型稳定”“具有创新性”替代量化或条件化表述。

摘要至少包含题目背景、方法、关键结果、验证证据、实际含义和限制中适用的内容；若证据尚未支持某项内容，就减少主张而不是补写空话。论文中的计算结果、单位、舍入规则和符号要与 Registry 一致。

### 图表和可视化

- 图表先有问题再有形式：登记读者要观察的结构、源结果、主张、图注和限制。
- 用一致的单位、轴向、色标、误差说明和图例；对比图共享可比的尺度，不隐藏失败场景。
- 三维图仅在真实三维变量、曲面、空间、轨迹或前沿语义能增加信息时使用；不能用旋转角度、立体感或重复视角凑视觉复杂度。
- 对每张图检查源数据、生成脚本、文件哈希、稿件引用、分辨率、裁切、字体、色盲可读性和孤儿状态。

### P9 复现报告

复现报告逐项列出原 execution 与复现 execution 的输入、代码、依赖、环境、随机性、输出、容差、允许漂移、差异解释和结论。结构化结果不一致时标出第一个不一致节点并触发失效传播；不能用“图看起来相似”关闭复现问题。

### P10 审查报告

每个审查角色独立记录范围、检查项、通过条件、finding_id、reviewer_mode、证据位置和时间。审查报告只能审查已存在的稿件或结果，不能引用未来证据；修复 finding 后必须生成更晚的关闭证据，并重跑声明范围内的门禁。

### P11 交付报告

交付报告列出候选包和最终包哈希、manifest、成员路径、成员哈希、许可、匿名扫描、隐私扫描、解压测试、smoke command、复现入口、适用性豁免和未解决限制。包中不能出现项目内部绝对路径、身份信息、`.mmflow`、临时缓存、秘密或未许可数据。

## 11. 最终报告语言与阻塞协议

向用户汇报时分成四层：

1. 程序验证事实：阶段状态、事件、哈希、血缘、绑定、复现、隐私、许可、路径和规则检查。
2. 科学证据：数据、模型、推导和实验真正支持的结果，附适用范围和不确定性。
3. 专业判断：创新、领域意义、可读性、答辩强度和质量 profile 评价，明确证据和主观成分。
4. 外部边界：原创性归属、评委接受度、奖项、外部 AI/查重系统和官方最终决定。

报告必须逐项列出全部 `NOT_APPLICABLE` 决策及其判定依据和替代验证安排，供用户复核适用性判断；不隐藏、不合并、不省略。

阻塞时只请求最小缺失输入，并附安全替代、已完成产物、恢复命令和数据敏感性说明。不要把“需要用户选择风格”“模型还可以改进”“工具暂时不可用但有替代路径”当作阻塞；前两类应自主决策或登记限制，后一类先尝试安全替代。

## 12. 模板、脚本与扩展资源

### 运行时与校验

- 主事实入口：`scripts/mmflow.py`。
- 登记契约自省（只读、无需项目）：`schema [--evidence-type T]` 输出证据内容契约与实测必填字段；`adapters` 输出全部合法 trait/claim/model_family 的适配器机器名；`cookbook [--stage Pn]` 输出阶段必需证据集合与登记手册路径。登记前先自检，把 epoch 重建压到最少。
- 证据登记唯一操作手册：`references/evidence-registration-cookbook.md`（P0–P11 全阶段路由；载荷配方、代际纪律、链式注册顺序的唯一事实源）。
- 图表覆盖规划：`figures plan --contract <problem-contract.json>` 生成题目自适应图表计划，`figures verify --plan <plan.json> --figures <figures.json>`（后者为含图表 JSON 数组的文件，不是目录）核验完成度；P8 登记图表前先规划。
- 答辩材料数据源：`export-claims [--question Qx] [--output claims.json]` 导出 VALID claim 及支撑实体，供 `qa_cards.py` 与 `create_ppt.py --claims` 消费。
- 审查关闭入口：`close-finding --id <finding_id> --closure <closure.json> --reason <...> [--mode CLOSED|ACCEPTED_LIMITATION]`；CRITICAL/MAJOR finding 必须经此命令以真实关闭证据清零（P10）。
- 代际重建入口：`retire-artifact --id <entity_id> --reason <...>` 把上一代固定路径制品 STALE 并沿血缘传播，但不自动回退阶段；返回 `suggested_rollback_stage` 供显式 `rollback` 决策（跨 epoch 重生成不卡顿的关键动作）。
- 批量登记：`batch-register --file <entries.json>`（顶层 `{entries:[{kind,payload}]}`）；单条失败不影响其余条目，错误逐行回报。
- 整合版模板清单和安全复制入口：`scripts/integrate_templates.py`。
- Skill 结构、政策、模板隔离和交付卫生校验：`scripts/validate_skill.py`。
- 稳定测试入口：`python scripts/run_tests.py`（`--quick` 为快速契约子集，`--full` 为完整分组套件）。完整套件可用 `--group core|workflow|runner|delivery|figures-docs` 单独运行；命名分组只改变批次和进度记录，不放宽任何测试或门禁。入口自行固定 skill 根路径并禁用字节码缓存，测试缓存不进入交付目录。
- 干净交付闭环：`python scripts/clean_delivery.py --output <dir> [--tests quick|full|skip]`；在临时干净副本上依次执行发布复制、Skill 校验、manifest 检查、语法检查、分组测试和 ZIP 路径安全核验，产出哈希化发布报告，不写源目录。
- 运行模板前先执行 `python scripts/integrate_templates.py check --root <skill-root> --json`；查看可用模板用 `list`，查看单项用 `info <template-id>`。
- 复制模板时必须显式指定 `--project-root`；目标已存在、越出项目根目录或位于 `.mmflow` 时拒绝覆盖或复制。模板输出永远不是生产证据，必须经受控 runner 和 Registry 登记。

### 六类模板

- `templates/production/`：第一版 production 入口、结果契约、论文骨架和模型执行模板；只有这一层可声明 production eligible，仍需受控执行。
- `templates/analytics/`：数据预处理、EDA、问题骨架、敏感性、统计检验、极端场景和工具函数；按题型和依赖选择，不机械全部运行。
- `templates/visualization/`：生产图生成器基线（趋势、热力图、雷达图、Pareto、收敛、残差诊断、网络图、柱状、散点拟合、结果表、流程与模型示意、空间分布）与批量出图驱动 `generate_all.py`；经共享契约 `plotting_common.py` 产出 v2 sidecar，只有 production 输入可出图。
- `templates/publication/`：中英文论文骨架、美赛 AI Use Report 披露骨架（内容只由参赛者如实填写，AI 不代填）、摘要检查、一致性检查、`build_abstract.py` 摘要草稿生成（数值逐字取自 export-claims，未填槽位显式标记）和 Word 导出；输出需要绑定有效 Registry 证据。
- `templates/presentation/`：答辩 PPT 生成骨架与答辩问答卡片（`qa_cards.py`，从 claim 导出生成）；内容、数字和图表必须来自已登记生产结果。
- `templates/quality/`：AI 风格和查重代理检查；只能作为辅助风险信号，不能等同于外部 AI 检测或查重结论。
- `templates/examples/`：明确标记为 demo，不得支持最终主张，也不得通过复制或改名升级为 production。

### 扩展参考

- `references/extended-competition-playbook.md`：需要深度洞察、定理匹配、跨领域迁移、反套路候选、失败诊断、敏感性、论文叙事或答辩卡片时读取。
- `references/extended-sprint-protocol.md`：时间紧、需要逐问闭环、阶段里程碑、上下文断点、并行边界或恢复策略时读取。
- 扩展参考中的质量 profile、页数建议、图表建议、写作检查和代理指标均为可选增强；适用规则和题目证据优先。

## 13. 质量标签和能力边界

由 `mmflow release-status --project <project-root> --json` 计算标签，不接受调用方传入标签或自报分数：

- `NOT_READY`：存在红线、条件门禁失败、完整性错误、重大 finding 或必需测试失败。
- `REPRODUCIBLE`：证据链、隔离复现和合规门禁通过，但质量证据尚未齐全。
- `QUALITY_REVIEW_READY`：质量证据齐全，等待专业审查。
- `SPECIAL_PRIZE_CANDIDATE`：所有门禁、高质量证据、实质贡献和真正独立盲审均通过。
- `SPECIAL_PRIZE_CANDIDATE_LIMITED_REVIEW`：其他条件满足但独立审查能力受限，必须披露限制。

程序可以证明哈希、事件、状态、血缘、绑定、复现、隐私、路径、许可和规则检查。模型是否有领域意义、是否原创、表达是否优美、评委是否认可、是否获奖以及外部 AI/查重系统如何判断，仍属于证据支持的专业判断或外部决定，不能写成程序证明。

## 14. 阻塞、恢复与完成定义

仅在题目或关键附件不可访问、必需私有数据/账户/授权不可取得、一手规则冲突无法确认、身份信息只能由用户提供、未授权外部操作不可替代或允许资源无法形成可信答案时阻塞。阻塞报告必须说明 `missing_item`、`why_required`、`attempted_alternatives`、`minimum_request`、`safe_partial_outputs` 和 `resume_command`；模型失败、效果不佳、需要重写或需要更多实验不是阻塞理由。

只有状态机返回 `COMPLETE`，且最终报告明确区分以下四类内容时才交付：程序验证的事实；模型/数据/理论/实验支持的结论；专业判断的质量、创新和领域意义；本 Skill 无法保证的评委判断、奖项、原创性和外部检测结果。任一必要校验失败、重大 finding 未关闭或限制未披露，都保持 `NOT_READY`。

## 15. 直接参考路由

只按当前阶段读取以下一层直接参考：

- 工作流、事实边界、状态、门禁、账本和恢复：`references/workflow-contract.md`
- 各阶段证据登记配方、代际纪律与链式顺序：`references/evidence-registration-cookbook.md`
- 材料、选题、需求矩阵、Problem Contract 和歧义：`references/problem-formalization.md`
- 基线、候选模型、选择和冻结分析计划：`references/model-selection.md`
- 题型适配验证、不确定性、优化、ODE/PDE 和规则化不适用：`references/validation-by-model-type.md`
- 数据血缘、划分、泄漏、公开数据和文献：`references/data-and-literature-governance.md`
- Artifact、Execution、Result、Claim、Binding、Lineage 和失效传播：`references/evidence-and-claims.md`
- 当届规则、匿名、许可、隐私、打包和提交边界：`references/competition-compliance.md`
- 论文论证、摘要、公式、图表、三维图边界和渲染：`references/paper-and-visuals.md`
- 按问题与 evidence role 的图表覆盖、Python 基线、MATLAB 可选契约和 sidecar：`references/figure-coverage.md`
- 外部快照、短路径执行、缓存重定向、失败诊断和源树卫生：`references/isolation-runtime.md`
- v1→v2 plan/apply、备份、原子 staging、哈希报告和重新验证：`references/migration.md`
- 复现、审查角色、finding 生命周期、回退、盲审和答辩：`references/review-recovery-and-defense.md`
- 深度洞察、创新、定理、表达和质量增强：`references/extended-competition-playbook.md`
- 冲刺节奏、逐问闭环、断点、并行边界和恢复：`references/extended-sprint-protocol.md`

不要把参考文档作为更深层索引；不要一次加载全部长文档；不要让扩展模板或参考文本成为第二个事实源。
