---
name: project-docs-product
description: Clarify business requirements; create, revise, or review PRDs; and deliver clickable HTML prototypes when requested. Work from spoken descriptions, meeting notes, business materials, or changes to existing systems. Use project-docs-overview for documentation of the current project.
---

# Project Docs Product

Turn business questions into reviewable product requirements, PRD revisions, or requirement reviews, with clickable HTML prototypes when requested. Work from conversations, meeting notes, business materials, and existing systems while keeping business decisions, source evidence, and acceptance criteria traceable.

[中文文档 / Chinese documentation](.bundle/README.zh-CN.md)

若当前 Skill 目录下存在 `.bundle` 且其 `../../` 不是本集合的 Git 检出，先读取 `.bundle/skills/project-docs-product/GUIDE.md` 并以该目录为 Skill 真实目录；其中的共享脚本、资料和其他 Skill 均来自同一快照。通过 `npx skills update <已安装的本集合 Skill 名称>` 更新此类安装，按实际作用域加 `-g` 或 `-p`；不运行快照内依赖 Git 检出的更新命令。 帮助产品与业务人员把问题变成可评审、可交接的需求。按[读者与用途约定](.bundle/references/audience.md)组织结果，保留同一正式 PRD、版本、规则与 FR/AC，读者摘要引用主文，不改既定业务约束。按 [产品工作流](references/workflow.md) 组合 Superpowers `brainstorming`、Matt Pocock `grilling` 和 `domain-modeling`；先确定当前阶段，只加载该阶段需要的能力，不能同时运行两个访谈主持流程。

先按[工作流的任务路径](references/workflow.md#按需选择阶段)区分评审、整理/修订与探索，只加载当前阶段需要的资源。先解析本 Skill 的真实目录，脚本位于 `../../scripts/`。只在调用上游能力前按[依赖与适配](references/dependencies.md)核查所需能力；缺失不自行安装或伪称已运行。完整探索须具备相应依赖，不以整理路径绕过；安装和全套诊断另行处理。

生成、修订及评审均按[生成前澄清与未决分类](references/workflow.md#生成前澄清与未决分类)：关键业务歧义先问，明确事项不重复问；写作中发现歧义也回到澄清。业务未决、技术待核实和待批准分开，不能未询问就用草稿或一串“待确认”代替澄清；明确暂缓的讨论草稿例外按工作流处理。

## 交付选择

先读[资料条件与产品质量](references/input-and-quality.md)，按源码、截图/设计、文档/口述或新产品资料开始；无源码仍交付完整业务规格，分别说明证据与交付用途。读取已有文档时先按工作流核对读取完整性：正文、表格、评论标注及回复共同构成来源，未读到的部分明确留缺口。不能把正文读取成功当作来源完整，也不能为通过校验改编号或移除可点击来源链接。

- PRD评审：按[PRD评审](references/workflow.md#prd评审)交付问题、结论和必要澄清，不自动重写PRD或套用生成交付要求。
- 原型：用户要求出原型，或将原型范围限定为仅验证某个交互（例如比较两个操作后的状态反馈），先读[原型交付规范](references/prototype.md)。后者走局部交互验证，关键状态未定时先澄清，列出未覆盖范围。完整原型默认覆盖本期完整用户任务，先写流程覆盖表，再交付共享模拟数据的可编辑 HTML、旅程验收和截图。
- 普通需求：默认用[面向读者的 PRD 模板](assets/prd-reader-template.md)交付 `prd.md`。先按[写作与修订基线](references/workflow.md#写作与修订基线)确定主干：复杂业务先讲背景、问题与场景处理，再推导页面、数据和接口变化；简单增量用短变更说明，按[阅读与变更约定](references/reading-and-change.md)裁剪。不要让 FR、AC 或追踪元数据主导正文；另交付 HTML 阅读版时复用同一业务主文，静态说明页使用 Overview 的 explainer。详细验收、既有编号和源码证据按阅读约定拆出并链接，不靠折叠附录隐藏冗长。涉及计算或数据变化时按需补可复算数据示例表，不为无计算需求凑表。
- 已有系统改造：先读[增量设计与业务闭环](references/brownfield-delivery.md)，按 Overview 取证核实现有页面、组件和端到端对象链；在原页面上标新增变化，集中列变更清单，复杂业务仍以场景处理为主干；仅沿本次数据及职责边界核对准备、固定、保存和使用，不把外围系统风险自动变成需求。源码是现状依据，不替业务作决策；无页面基线仍画目标任务，明确未核实的原页面边界。
- 业务图：使用 [Diagram](.bundle/skills/project-docs-diagram/GUIDE.md) 的非源码原生通道，以 PRD 和业务资料为依据。
- 可选 PDLC 协作：读取 [交接约定](references/pdlc.md)；缺失不阻塞独立交付，安装不等于支持接管，普通 PRD 不自动进入研发。

未指定目录时，在被分析仓库外创建本次需求交付目录。统一使用业务语言；术语表只放定义，规则、决策和未决问题放 PRD，重要 ADR 按上游条件按需创建。不要把示例或原型模拟值当作真实业务事实。

## 检查与交付

按[阅读与变更约定](references/reading-and-change.md)选择轻量单文件或主文/追踪拆分，以及必要页面图和业务图；先验收范围与读者能否看懂变化，再核完整性。正文不能靠附件拼出规则，也不能为模板扩写。

修订前与交付前执行[需求保留与恢复走读](references/workflow.md#需求保留与恢复走读)，逐项核对原始诉求及有效关联约定，并从异常反馈走到可执行下一步；记录实际缺口，不以“已检查”代替。

生成或修订PRD时，按[结构声明模板](assets/prd-template.md)保留实际需求的三级 FR 标题、所属四级 AC 标题及状态、依据、原型字段；文档状态值单独写“草稿”“待确认”或“已确认”，说明另写，不复制空章节。重新读取成品，运行 `python3 <本集合>/scripts/validate_product_doc.py --file <交付目录>/prd.md`；外置追踪时显式追加 `--tracking <交付目录>/prd-traceability.md`（须同目录、版本一致且主文有链接）；用户已要求原型或本轮需联动核验已有原型时，追加 `--prototype <交付目录>/prototype.html`。原型缺失须报告未交付，不能因文件未生成省略核验；使用bundle检查时同时传 `--require-prototype`。核对来源、已决事项、正常/边界/异常验收，以及修改前后的关联内容。校验失败时按错误修正本次生成的声明并重新校验，无法完成须如实报告。校验只证明结构、标识与资源关联，业务含义和浏览器交互另行验证；仅评审不为适配校验器补写或改写原稿。

按[交付回复与验收汇总](references/reading-and-change.md#正文与交付回复)先说明变化、待决定事项与下一步，提供实际成品及证据；定稿或大改按需要给要点覆盖。产品确认和授权边界统一按[工作流](references/workflow.md#验证与交付)，不同检查结果不能互相代替。
