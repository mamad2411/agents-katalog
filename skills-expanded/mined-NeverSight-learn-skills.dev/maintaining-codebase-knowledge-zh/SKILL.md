---
name: maintaining-codebase-knowledge-zh
description: 当接手不熟悉的仓库、为请求的功能或 Bug 深化项目知识、将任务范围内的企业或对话证据与实现关联、在代码变更后刷新知识、完成前检查文档影响，或向开发工作流提供可靠的仓库上下文时使用。
---

# 维护代码库知识

建立一条可靠路径，让开发请求能够找到相关代码、行为、约束和测试。本 Skill 维护项目知识，不负责设计或实现改动。

## 始终遵守的规则

- 每项声明都要使用能够支持它的证据。需求不能证明已经实现；代码也不能证明预期行为。
- 分别记录支持状态、置信度、就绪度、持久化方式和文档深度。
- 每个持久事实只有一个规范文档所有者。其他位置只链接。
- 区分业务能力、跨能力流程和实现单元。
- 文档只描述当前状态。历史留在 Git、已接受的决策、规格或计划中。
- 只重写带托管标记的文档或区块。保留用户编写的内容。
- 不生成空章节。

## 需要读取的参考文档

写入项目知识前，先读 `references/knowledge-model.md`。

以下情况还要读取：

- 对话、企业系统、CI、事故或受治理的证据会影响任务时，读取 `references/external-context.md`。
- 其他工作流将使用项目知识进行设计、实现、调试、评审、验证或交付时，读取 `references/development-workflow-integration.md`。

## 选择一种模式

| 模式 | 使用时机 |
|---|---|
| Bootstrap | 仓库不熟悉，或没有可靠的知识索引 |
| Deepen | 功能、Bug 或维护任务需要更深入的知识 |
| Refresh | 稳定实现已经变化，或需要检查文档影响 |

不要把首次发现和代码修改混在一起。每种模式都可以读取已授权证据并运行安全检查，但不得修改生产代码、泄露秘密、变更外部系统或接管开发工作流状态。

## 每种模式开始前

1. 解析唯一的目标仓库根目录。报告绝对路径和选择依据，并在整个运行中保持不变。
2. 按 `references/knowledge-model.md` 选择一个根指令桥接文件，然后读取适用的项目指令。
3. 直接检查 `<target-repository-root>/docs/project-knowledge/index.md`。如果存在，先读索引，再选择其他项目文件。
4. 说明目标、范围、选定能力、排除项和可观察的成功条件。
5. 检查当前对话和附件。存在重要证据时，加载外部上下文参考文档。
6. 记录 revision，以及会影响证据含义的环境或外部来源信息。
7. 明确可能改变计划的歧义。

索引处理必须严格：

- Bootstrap 可以从缺失索引开始，并创建索引。
- Deepen 和 Refresh 必须使用已有且可读的索引，否则停止并建议 Bootstrap。
- 索引不可读时，所有模式都停止。
- 不得借用其他 worktree、Skill 安装目录或记忆中的索引。

每次成功运行后，只能有一个选定的根指令桥接文件指向当前索引。仅当两个受支持的指令文件都不存在时，才创建 `AGENTS.md`。写入前验证完整托管区块；发生冲突时，不要通过切换文件绕过。

## Bootstrap

### 目标

建立有选择、有证据支撑的知识基线，为后续任务提供路由。不要尝试覆盖所有未来能力。

### 步骤

1. 检查适用的指令、manifest、入口、文档、测试、CI、部署和迁移。按照知识模型评估架构关注点与交付义务来源。
2. 扫描任务和产品线索，例如 TODO/FIXME、待办类文件、规格、示例、接口、schema、配置、废弃代码和测试缺口。
3. 选择一到五个高价值能力。为每个能力追踪一条有代表性的“调用方到结果”路径及其测试。
4. 创建最小托管集合：每个选定能力一个能力文档，每个重要的已知意图一个台账条目。
5. 只有当两个或更多能力所有者存在可复用的顺序、交接、事务、重试、回滚或副作用时，才创建 flow。局部顺序留在能力文档中。
6. 模拟两到三个任务交接。对于没有权威意图的新请求，只验证它能路由到 Deepen；对于已有意图，说明现有证据足以进入设计还是实现。
7. 渲染并验证选定的指令桥接文件。

### 停止条件

- 选定能力已经描述有证据支持的当前行为；
- 每个选定的重要意图都有唯一入口；
- 每个持久事实只有一个文字所有者；
- 指令桥接文件通过选择、标记、内容和预算检查。

## Deepen

### 目标

不重新执行 Bootstrap，只把一个具体任务补充到可以安全进入下一阶段的深度。

### 步骤

1. 从请求或对应的 intent 条目开始。新请求或未路由请求都是合法输入。
2. 按知识模型检查下一阶段所需知识。如果已有路由足够，返回 `checked-unchanged`。
3. 只读取当前任务需要的来源和实现路径。
4. 追踪“调用方到结果”路径。按需记录符号、所有权和生命周期、状态变化、算法分支与终止、数据或并发行为、失败路径、不变量、测试、公共契约变化和交付义务。使用限定范围且可复现的证据，不复制实现正文。
5. 公共或集成边界发生变化时，追踪：
   `原始输入 -> 运行时归一化值 -> 消费者可见值`。
   核对所有适用的运行时、类型或 schema、文档、示例和测试。语义不一致时记录为缺口。
6. 异步操作可能以不同顺序开始和结束时，分别记录调用顺序、完成顺序和外部可见顺序。如果顺序会影响行为，使用可控制的对抗测试接缝。
7. 将意图与当前支持状态分开。发现冲突时报告冲突，不凭假设解决。
8. 创建新能力前，先深化已有能力。能力过宽时，先列出内部区域。只有证据表明存在独立结果、契约、生命周期、不变量、变化轴或长期独立工作时，才拆分。
9. 更新 intent 条目、可选的任务契约差异，以及最小的 capability/flow 集合。只有创建或拆分规范 capability/flow 时，才调整索引或架构映射。

### 停止条件

路由 `index -> intent 条目 -> capability 或 flow` 已经给出任务的核心验收、入口和结果、相关机制、不变量、测试、交付义务、缺失证据及人工决策。边界可能变化时还要包含放置证据。就绪度只能反映这些证据实际支持的阶段。

## Refresh

### 目标

实现稳定后，让托管知识重新与代码保持一致。

### 步骤

1. 检查 diff、受影响测试、运行路径、任务证据和相关快照。
2. 将每项变化映射到其规范所有者。
3. 替换过时状态。把任务契约差异中的稳定行为归入 capability 或 flow，然后删除已被取代的任务细节。
4. 只有规划安全性变化时才更新就绪度。局部缺口留在 capability，跨能力风险留在 `risks.md`。
5. 没有持久知识变化时，返回 `checked-unchanged`。
6. 修改指令桥接文件前先验证它。

在重新进行完成验证前运行 Refresh。Refresh 本身不能证明实现正确。

## 结果契约

每次运行都以下列内容结束：

```text
Mode and goal: <模式、范围、成功条件>
Target repository root: <绝对路径和解析依据>
Knowledge entrypoint:
  Path: <绝对路径>
  Status: read | created | missing | unreadable
Project instruction bridge:
  Path: <绝对路径>
  Selection basis: existing AGENTS.md | existing CLAUDE.md | created AGENTS.md
  Discovery: native | platform-dependent | shadowed
  Managed block budget: <解码后的字符数>/800
  Status: written | unchanged | unresolved
Evidence snapshot: <revision、命令、环境、来源版本/时间>
Context evidence:
  Considered: <项目或 none>
  Persisted: <规范路径和提炼后的声明，或 none>
  Rejected or session-only: <项目、原因，或 none>
  Conflicts or unavailable: <项目或 none>
Knowledge changes:
  Updated: <路径或 none>
  Removed as stale: <声明、路径，或 none>
  Checked unchanged: <路径或 none>
Planning:
  Readiness: ready-for-design | ready-for-implementation | needs-deepen | needs-decision | blocked | none (没有选定的重要意图)
  Read first: <index、intent 条目、capability 或 flow>
  Unresolved decisions: <问题或 none>
  Recommended next action: <一项行动>
  Task contract coverage:
    Status: assessed | none (不是重要任务的 Deepen)
    仅在 assessed 时包含以下四行，否则省略：
      Core acceptance: defined | missing
      Public contract delta: resolved | not-material | missing
      Risk hardening: classified | none-observed | missing
      Delivery obligations: linked | none-applicable | missing
Placement evidence (放置位置或边界相关时)：
  Matching capability or flow: <规范链接或 none>
  Primary and supporting implementation units: <单元和链接，或 unknown>
  Existing extension seam: <有证据支持的接缝，或 none observed>
  Boundary pressure: <观察到的压力，或 none observed>
  Design decision still required: <问题或 none>
Deepening evidence (Deepen 模式)：
  Knowledge route: <intent existing|created|updated; capability/flow matched|expanded|created|split>
  Sufficiency before Deepen: sufficient | insufficient; <缺少的维度或 none>
  Key implementation symbols: <符号和规范章节，或 none>
  State machine or algorithm map: <规范章节或 none>
  Scoped evidence snapshot: <revision 加脏文件哈希，或选定文件哈希>
  Capability structure: <展开区域；split|keep-together|candidate-only|unchanged；证据依据>
```

## 常见错误

| 错误 | 修正方式 |
|---|---|
| 把 TODO 或用户描述当成实现事实 | 分别验证意图和当前支持状态。 |
| 在多个文档中复制同一状态 | 只存一次，其他位置链接到所有者。 |
| 在当前状态文档中保留变更前后历史 | 替换过时内容，历史交给历史记录。 |
| 把一个智能体缺少的本地工具写成项目债务 | 除非能复现为项目约束，否则只写入运行结果。 |
| 结构化重写没有标记的文档 | 只做必要的局部修改，或报告冲突。 |
| 把 capability 当成代码模块 | 分别映射 capability、flow 和实现单元。 |
| 因任务未路由而重新 Bootstrap | 执行任务级 Deepen。 |
| 因 capability 规模大而拆分 | 必须先有稳定的所有权或边界证据。 |
| 只列路径，不解释机制 | 补充任务相关符号、行为、不变量、测试和限定证据。 |
| 使用没有阶段含义的 `ready` | 明确下一个安全阶段。 |
| 把每个边界情况都升级为需求 | 区分核心验收与风险加固。 |
