---
name: project-docs
description: Entry point for the Project Docs skill collection. Use when users name project-docs, install or upgrade the collection, coordinate work from business problems to release, or combine PRDs, interactive HTML prototypes, project overviews, API documentation, and technical diagrams.
---

# Project Docs

Choose a documentation workflow for your project, from business requirements and clickable prototypes to source-backed onboarding guides, API documentation, and technical diagrams. Use this entry point to combine skills or install and update the collection.

[中文文档 / Chinese documentation](.bundle/README.zh-CN.md)

若当前 Skill 目录下存在 `.bundle` 且其 `../../` 不是本集合的 Git 检出，先读取 `.bundle/skills/project-docs/GUIDE.md` 并以该目录为 Skill 真实目录；其中的共享脚本、资料和其他 Skill 均来自同一快照。通过 `npx skills update <已安装的本集合 Skill 名称>` 更新此类安装，按实际作用域加 `-g` 或 `-p`；不运行快照内依赖 Git 检出的更新命令。

根据任务目标、范围和交付物选择本集合的专用能力，再按读者组织结果。先解析当前 Skill 的真实目录；下表链接均相对该目录。读取选中能力的入口说明后，遵循其取证、生成和验证要求。

文档、图与交接资料按[读者与用途约定](.bundle/references/audience.md)组织：先选任务，再分别判断业务/技术知识与阅读目的；不把专家、普通读者或 HTML 格式等同某种固定写法。安装、升级与诊断无需读者分类。

用户要求更新本集合及依赖时，运行 `bash <真实Skill目录>/../../install.sh --update --host <宿主>`；根据当前实际宿主选 `codex`、`claude`、`zcode`、`dsh`、`gemini`、`grok`、`pi` 或 `opencode`，用户明确要求全部宿主时才用 `all`。只同步依赖时使用 `--update-deps`，仅更新 Skill 时加 `--no-engines`；诊断和卸载也使用同一个 `--host`。不要省略宿主参数后误用默认的 Codex、Claude Code 两端。五个子 Skill 随仓库更新，绘图 CLI 以集合锁定版本为最低基线，保留相同或更高稳定版本，无法识别版本时停止；显式 CLI 覆盖由外部管理。更新保护本地改动，不自动切分支或重置；失败时报告具体阶段，不宣称全部更新成功。普通文档生成不先联网升级，也不升级用户的其他全局 Skill。

安装及依赖同步会补齐 Product 必要的 `brainstorming`、`grilling`、`domain-modeling`，已有有效安装直接复用，不覆盖、不自动升级。`--no-engines` 仍检查并补齐必要 Skill；`--doctor` 只读检查，卸载保留第三方 Skill。可选前端、UI/UX、PDLC 等不默认安装，按任务需要及明确授权处理。

| 用户需要 | 读取的能力 | 交付物 |
|---|---|---|
| 从业务痛点到需求、设计研发、验收上线与效果跟踪，或已有需求跨阶段接续 | [project-docs-lifecycle](.bundle/skills/project-docs-lifecycle/GUIDE.md) | 同一身份的阶段交接、版本化追踪、实际工作及证据 |
| 业务需求梳理、PRD、产品评审，或可点击 HTML 界面原型 | [project-docs-product](.bundle/skills/project-docs-product/GUIDE.md) | 可追溯 PRD、按需交互 HTML 原型及评审记录 |
| Spring MVC、Feign 或 FastAPI 接口文档 | [project-docs-api](.bundle/skills/project-docs-api/GUIDE.md) | API Markdown、Postman Collection、cURL 示例 |
| 架构图、流程图、泳道图、时序图、ERD，或处理 Mermaid、PlantUML、draw.io、Archify 图源 | [project-docs-diagram](.bundle/skills/project-docs-diagram/GUIDE.md) | 可编辑图源、按需导出文件及验证回执 |
| 项目介绍、功能说明、架构总览文档或开发者上手手册 | [project-docs-overview](.bundle/skills/project-docs-overview/GUIDE.md) | 按对应模板生成、带来源的 Markdown；按需交付 explainer 交互 HTML |

“一页项目说明”“explainer”或项目介绍交互 HTML 选择 `project-docs-overview` 的一页说明模式；它可嵌入原生图，但不作为第十一种图型交给图形脚本。表单、弹窗、页面跳转或业务状态演示的“原型 HTML”选择 `project-docs-product`，不能用静态说明页替代。比较 PRD 与代码差异时由产品能力组织需求，Overview 核实现状；无代码的需求也可从产品能力开始。

“零基础图解”或 ELI5 解释页面交由 `project-docs-overview`，复用 explainer，覆盖概念、流程、规则、机制、问题因果、取舍、变更、培训及客户说明；按解释目标组织，不限技术主题。仅要求 ELI5 解释、通俗解释或给业务人员看时调整表达，不自动生成 HTML。仅画图仍走绘图能力。

用户已明确交付物时直接选择，无需再询问入口名称。仅要求画图时读取绘图能力；“架构总览文档”由文档能力组织正文，并读取绘图能力完成必需的系统全景图和核心流程图。保留用户指定的图型、引擎和导出格式。

按系统描述画概念／方案图也选择绘图能力，走现有原生图源通道，不要求先有仓库；根据当前代码画图仍须取证。混合请求区分已实现部分与拟议部分，不把描述当成源码事实。

组合请求按交付物衔接。例如“介绍项目，附 draw.io 架构图和接口文档”使用文档能力组织正文、绘图能力交付图片与图源、接口能力生成独立接口产物，最后在正文中关联。复用已核对的源码范围与证据，仍执行每项交付物各自要求的检查；不能用一项通过代替其他项通过。

没有指定输出位置时遵循专用能力的默认位置；组合产物放在同一交付目录及子目录，用相对链接关联。交付时列出实际完成的文件、验证结果与未完成项。普通文档生成不授权修改业务代码、发布到飞书或提交到目标仓库。生命周期请求已明确授权实现时，按对应范围推进代码与测试；实际发布和外部写入仍依用户指令、权限及项目规则执行。
