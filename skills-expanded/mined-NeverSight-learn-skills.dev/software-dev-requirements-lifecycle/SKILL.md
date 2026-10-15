---
name: software-dev-requirements-lifecycle
description: >-
  引导长期软件产品在需求频繁变更下建立「文档真源 + 变更闭环」：需求接收与归类、用户故事与验收、排期与承诺、
  ADR/变更台账、实现闭合与发版说明，以及用户帮助中心的目录与导航。适用于任意技术栈；要求使用者在项目根维护
  AGENTS.md（或等价文档地图）声明路径与优先级。在用户讨论立项、排期、PRD、路线图、需求变更、研发流程、
  文档如何配合编码、帮助文档信息架构时使用。多步执行前须先与用户确认拟办步骤及可选/高风险环节。
  收到 PDF 或 Office（DOCX/PPTX/XLSX 等）需求材料时，可配合本仓库 mineru-office-to-markdown 技能在本地转为 Markdown 后再做 Intake；若无 MinerU 须先说明成本并征得用户同意再引导安装。
  与具体云厂商或某一内部工具无绑定。
---

# 软件开发与需求管理生命周期（通用）

面向**任意业务项目仓库**：把零散需求与口头约定，收敛为可追溯的书面基线，使人类与 AI 代理能共享同一套「真源」与更新节奏。

## 与 Baklib / 本仓库的关系

- 本技能**不依赖** Baklib MCP 或 Baklib 产品；放在 [baklib-tools/skills](https://github.com/baklib-tools/skills) 是为与社区其他 Agent Skills **一并发布**。
- 使用者将本技能安装到自己的编辑器/Agent 所要求的技能目录后，按本文与 [`reference.md`](reference.md)、[`references/`](references/) 在**各自项目**中落地文档结构即可。安装方式见 **[README.md](README.md)**。

## 何时启用

- 讨论立项、里程碑、排期、优先级、技术债与功能债的平衡。
- 客户或内部不断提出新需求/改需求，需要归类、记录、并与实现、测试对齐。
- 需要约定 **PRD、设计、计划、变更记录、CHANGELOG、用户帮助中心** 的分工与命名。
- 要避免「口头已改、文档未改、代码按旧理解写」的三方分裂。
- 用户以 **PDF** 或 **Office** 附件提供 PRD、变更说明、需求摘录时，需先得到**可读文本**（见下文「PDF / Office 需求材料」）再继续归类与 Intake。

## PDF / Office 需求材料

用户给出的是 **PDF、DOCX、PPTX、XLSX** 等二进制或可打印稿，而非仓库内 Markdown 时：

1. **优先策略**：按 **[`mineru-office-to-markdown`](https://github.com/baklib-tools/skills/blob/main/skills/mineru-office-to-markdown/SKILL.md)** 技能，在**用户本机终端**用 MinerU 转为 Markdown（或抽取正文），再基于转换结果做需求接收、摘录与互链。该技能说明安装、CLI 参数与目录批量注意事项；代理**不在此仓库内代跑** MinerU，由用户或代理逐步指导用户在**其工作区**执行命令。
2. **技能是否已安装**：若使用者已通过 `npx skills add … --skill mineru-office-to-markdown`（或手动复制）安装该技能，代理可直接**激活该技能**的说明来组织转换步骤；若未安装且需要走 MinerU 路径，先告知可安装该技能以便对齐官方参数与边界，**是否安装由用户决定**。
3. **未安装 MinerU / 环境未就绪**：先**简要说明**本地需 Python、磁盘空间与首次拉取模型等成本（详见 `mineru-office-to-markdown`），询问用户是否愿意安装与跑通；**未获确认前**不要假定用户会安装，也不要替用户做「已能转换」的承诺。用户可改为：自行安装后重试、粘贴正文、由 Office 另存/导出为文本或 Markdown、或先转 PDF 再走 MinerU。
4. **格式边界**：老版 **`.doc`** 通常需先另存为 **DOCX** 或 **PDF** 再转换（见 `mineru-office-to-markdown`）；许可证与商用范围以 MinerU 官方为准。

## 核心原则

1. **当前基线 + 历史可追溯**：维护「当前有效」的 PRD/计划等；变更用**追加式**台账或 ADR，而非只覆盖不留痕（Git 历史不够给业务方读时，仍要有可读摘要）。
2. **先对齐真源，再改代码**：实现前更新对应文档或变更记录；冲突时以项目根 **`AGENTS.md`（或等价物）** 中声明的优先级为准。
3. **书面承诺与闲聊分离**：进入「已承诺」排期前，条目须有可验收描述；未澄清项留在 Backlog，勿混入当前里程碑。

## 生命周期（简图）

```text
信号 → 记录与归类 → 澄清与验收标准 → 排期与承诺 → 实现与测试 → 文档闭合与发版说明 → 用户帮助更新（若对终端用户可见）
  ↑__________________________ 需求变更时回到「记录与归类」，并追加变更记录 __________________________|
```

## 文档类型与职责（速查）

| 类型 | 典型内容 | 备注 |
|------|----------|------|
| 文档地图 / 优先级 | 各类文档路径、冲突时听谁的 | 项目根 `AGENTS.md` 或 `docs/README.md` + 专章 |
| PRD / 产品需求 | 目标用户、范围、优先级、**Out of scope**、用户故事与验收 | 当前有效的一份（或分卷但索引要统一） |
| 产品设计 | 信息架构、关键流程、交互原则 | 可与 PRD 分文件或同文件分章 |
| 开发计划 | 里程碑、依赖、勾选状态、风险与假设 | 与对外承诺日期绑定时写明假设条件 |
| 变更台账 | 变更单：原因、旧/新条款、影响、确认 | `docs/changes/` 等，**追加为主** |
| ADR / 决策 | 重大分叉、易反悔决定 | `docs/decisions/` 等 |
| 对外 CHANGELOG | 版本维度的新增/修复/破坏性变更 | 仓库根常见 |
| 对内日志（可选） | 日记式进展与卡点 | 如 `docs/journal/YYYY-MM.md` |
| 用户帮助 | 终端用户任务导向、导航清晰 | 见 `references/help-center-information-architecture.md` |

完整目录与命名建议见 **[references/document-map-and-paths.md](references/document-map-and-paths.md)**。

## 工作流确认门（代理必读）

本技能涉及**多步编排**（读真源 → Intake → 影响判断 → 排期与文档更新等）。代理在动手前须遵守下列确认规则，与仓库级 [AGENTS.md](https://github.com/baklib-tools/skills/blob/main/AGENTS.md) 对工作流类技能的约定一致。

1. **先列步骤，再执行**：收到任务后，用**简短编号**列出**拟执行的步骤**（可对照下文「Agent 执行步骤」裁剪），勿默认跳过某步或一口气跑完全流水线。
2. **对下列类型逐项征得用户明确同意**后再执行（用户说「只做其中几步」时，严格按约定范围执行）：
   - 代写或修改可能被理解为**对外承诺**的表述（排期日期、交付范围、合同/商务口径等）；
   - **批量**创建、重命名或重构仓库内多份文档（非用户点名的单文件小改）；
   - 任何**写入当前 Git 仓库以外**的系统（工单、IM、项目管理 API、在线文档站、产品内帮助后台等）——本技能默认只协助编辑**当前工作区仓库内**的 Markdown/约定文档；
   - 可能产生**额外成本或依赖人工评审链**的操作（计费工具、需审批的发布通道等）；
   - **首次在本机安装、配置 MinerU**（或为其准备 Python 虚拟环境、拉取模型）以处理 PDF/Office——须先说明磁盘/时间与网络成本，征得同意后再分步指导；用户不同意则改用粘贴正文、导出文本等路径。
3. **未确认前**：不得替用户做「已承诺」类结论；不得默认用户需要完整生命周期（从立项到帮助中心改版全做）；不得擅自连接或调用未获授权的对外服务。

## Agent 执行步骤（建议顺序）

1. **读项目文档地图**：打开项目根 `AGENTS.md`（或 `CONTRIBUTING` / `docs/README.md` 中声明的真源表），确认 PRD、计划、变更、帮助文档的路径。
2. **对每条新输入做 Intake**：若材料为 **PDF / Office**，先按上文「PDF / Office 需求材料」与 **[`mineru-office-to-markdown`](https://github.com/baklib-tools/skills/blob/main/skills/mineru-office-to-markdown/SKILL.md)** 处理或征得用户关于转换方式的同意，再提炼：一句话目标、类型（缺陷/增强/新能力/技术债/合规）、依赖与风险、验收标准（可测）；见 **[references/templates.md](references/templates.md)**。
3. **判断变更影响**：是否动范围/日期/验收；若是，追加变更记录或 ADR，并更新「当前基线」对应章节。
4. **排期**：区分已承诺轨道与 Backlog；大需求切片为可独立验收的增量。
5. **实现闭合**：勾选计划项；对外变更写 CHANGELOG；终端可见行为同步更新帮助文档入口与相关 how-to。
6. **检查清单**（摘要）：
   - [ ] 真源文档已更新，无与代码/测试相矛盾的陈旧表述（除非刻意保留并标注 deprecated）。
   - [ ] 用户故事或变更单使用稳定 ID（如 `US-042`）便于互链。
   - [ ] 若存在帮助中心，新/改功能已在 `help` 首页或子索引中可发现（无孤岛页）。

## 能力边界（不做什么）

- 不替用户承诺具体交付日期或合同条款；只协助**结构化记录与一致性**。
- 不绑定某一项目管理工具（Jira/Linear 等）；ID 与流程由团队自选。
- 不在未获授权时向外部系统写入；本技能以**仓库内文档**为主。

## 延伸阅读（本技能内）

| 文件 | 内容 |
|------|------|
| [reference.md](reference.md) | **单文件索引**：PRD 目录建议、术语表示例、分册导航、帮助骨架摘要 |
| [references/agents-document-map-template.md](references/agents-document-map-template.md) | 新项目可粘贴的 `AGENTS.md` 最小文档地图与工作流 |
| [references/document-map-and-paths.md](references/document-map-and-paths.md) | 仓库内 `docs/` 建议布局、文件命名 |
| [references/templates.md](references/templates.md) | 用户故事、GWT、变更单、how-to 骨架、Definition of Done |
| [references/help-center-information-architecture.md](references/help-center-information-architecture.md) | 帮助文档分层、首页导航、单篇结构 |
| [README.md](README.md) | **安装**：`npx skills add`、复制到 `~/.cursor/skills/` 等、私有仓库 |
| [`mineru-office-to-markdown`](https://github.com/baklib-tools/skills/blob/main/skills/mineru-office-to-markdown/SKILL.md)（同仓库技能） | PDF / Office → 本地 Markdown；与本技能衔接时需确认是否已安装 MinerU |
