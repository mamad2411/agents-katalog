---
name: project-analyzer
description: 基于深度代码分析生成项目架构白皮书（whitepaper），覆盖架构、核心模块、执行流程、质量评估、构建部署与二次开发指南。当用户需要整体理解一个仓库、生成项目文档或架构分析时使用。
---

# Deep Project Analysis

本 skill 系统性地分析整个仓库，综合产出一份"项目架构深度分析"文档。它结合了模块级深度理解（借鉴 `code-reader` 的 ABC 验证回路思想）与高层架构综合，以及工程实践（构建、测试、部署）分析。

最终产出以"架构与模块深度解析"为主（约 60%），辅以实用的工程与运维指引。

## 1. 团队角色

本工作流使用专门的智能体角色，在综合成稿前分别收集不同类型的信息：

- **Agent A (Tech Writer / 模块专家)**：模块理解引擎。**默认通过调用 `codegraph` skill 获取符号级上下文**（入口点、调用链、数据结构），必要时辅以 `read_file` 读取关键源码，确保理解准确。若需更强的事实校验，可套用 `code-reader` 的 ABC 闭卷验证回路（见第 6 节）。
- **Agent B (DevOps Engineer)**：基础设施专家。扫描配置文件（Makefile、Dockerfile、CI/CD 流水线、`package.json` 等），提取构建、测试、部署实践。
- **Agent C (Chief Architect)**：综合者。读取所有模块分析结果与 DevOps 报告，撰写最终项目架构深度分析文档，确保叙述连贯、架构准确。

**REQUIRED SUB-SKILL：** Phase 2 默认使用 `codegraph` skill 作为模块理解引擎；如需"仅凭文档即可被新人理解"的强校验，可启用 `code-reader` 风格的 ABC 验证回路。

## 2. 用法

```bash
/project-analyzer <source> <output-dir>
```

- **source**：本地路径（如 `./path/to/repo`）或 GitHub URL
- **output-dir**：最终白皮书与中间分析文件的输出目录

## 3. 完整流程

你必须按以下阶段顺序执行，以生成最终文档。

### 3.1 Phase 1：准备与扫描

本阶段处理目标源码的解析与准备。

1. 解析目标仓库（URL 则克隆，本地则校验存在）。
2. 扫描目录结构，识别：
   - **代码模块**：包含核心业务逻辑的目录（`src/`、`lib/` 等）。
   - **基础设施文件**：构建脚本、Dockerfile、CI/CD 工作流、配置文件。
3. 生成模块间的初始依赖图。

### 3.2 Phase 2：深度模块理解（via `codegraph`）

本阶段将代码理解的重活委派给 `codegraph` skill（或等效的深度阅读）。

对每个识别出的核心模块：
- 优先调用 `codegraph context "<模块描述>"` 获取入口点、符号与代码片段。
- 用 `codegraph callers/callees/impact` 追踪调用链与影响范围。
- 对 codegraph 返回不足的部分，使用 `read_file` 读取完整源码补全。
- 收集每个模块的"能力 / 数据结构 / 状态流 / 修改指引"笔记。
  _注：本阶段聚焦代码、逻辑与数据结构本身。_

### 3.3 Phase 3：基础设施分析（DevOps Engineer）

本阶段从配置文件提取工程实践。

派发 DevOps Engineer 角色（使用 `references/devops-engineer-prompt.md`）。

- **输入**：所有识别出的基础设施文件（如 `Makefile`、`Dockerfile`、`.github/workflows/`、`pom.xml`）。
- **输出**：覆盖构建步骤、测试策略、部署拓扑的结构化报告。

### 3.4 Phase 4：架构综合（Chief Architect）

本阶段生成最终的项目架构深度分析文档。

严格**读取并遵循** `references/chief-architect-prompt.md` 派发 Chief Architect 角色。

- **输入**：Phase 2 生成的模块文档、Phase 3 的基础设施报告，以及初始目录扫描。
- **项目名**：必须从实际仓库提取项目名（如仓库目录名、`package.json`、`go.mod`），替换输出文件名中所有 `{project-name}` 占位符。
- **约束**：
  - Architect 必须大约 60% 的篇幅与深度分配给系统架构与核心模块，剩余 40% 分配给项目概述、场景与工程实践。
  - **图示**：必须按 Chief Architect prompt 要求输出架构图、流程图、时序图的 Mermaid 语法。
- **输出**：写入 `<output-dir>` 的 `<actual-project-name>-deep-dive.md`，文档严格遵循以下 7 章大纲：
  1. 项目全局摘要 (Project Executive Summary)
  2. 系统架构分析 (System Architecture Analysis)
  3. 核心模块代码深度解析 (Core Modules Deep Dive)
  4. 核心功能执行流程分析 (Core Function Execution Flow)
  5. 质量与性能评估 (Quality & Performance Assessment)
  6. 项目构建与部署 (Project Build & Deployment)
  7. 二次开发指南 (Extension & Contribution Guide)

### 3.5 Phase 5：用户验收与评审

将生成的 `<actual-project-name>-deep-dive.md` 呈现给用户。

> "项目架构深度分析已生成。请审阅 `<actual-project-name>-deep-dive.md`。如需深入某个具体模块细节或调整任意章节的权重，请告诉我。"

## 4. 关键规则

执行期间严格遵守以下规则：

- **只读源码**：绝不修改源仓库。
- **内容权重**：确保 Chief Architect 严格遵守架构/模块与工程实践之间 60/40 的比例。
- **文档格式**：最终产出必须遵循专业技术写作规范（层级编号、无双语标题、术语一致）。

## 5. 可选增强：ABC 闭卷验证回路

当需要**确保生成的知识文档本身"仅凭该文档即可被新人准确理解"**时（例如为陌生模块生成 skill 文档），可启用借鉴自 `code-reader` 的 ABC 验证回路：

- **A (Tech Writer)**：深度阅读模块源码，撰写 SKILL.md 文档。
- **B (QA Engineer)**：仅读源码（不读文档），针对文档应覆盖的关键事实生成 5–8 道验证题（含答案要点 `required_facts`）。
- **C (Junior Dev)**：仅读 A 产出的文档（闭卷，不读源码），逐一作答。
- **评估**：主智能体比对 C 的答案与 B 的 `required_facts`，全部覆盖才算通过；任一未覆盖则把失败题目与答案要点回填给 A 重生成。
- **硬性规则**：必须循环直到 100% 通过或满 3 轮。3 轮后仍有问题则呈现给用户判断，不得静默放过。

该回路适用于"知识沉淀/文档自洽性"场景，普通项目分析（Phase 2）可直接用 `codegraph` 获取上下文，不必强制走完整 ABC 循环。
