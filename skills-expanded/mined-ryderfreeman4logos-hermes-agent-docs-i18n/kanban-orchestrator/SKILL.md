---
name: kanban-orchestrator
description: Decomposition playbook + anti-temptation rules for an orchestrator profile routing work through Kanban. The "don't do the work yourself" rule and the basic lifecycle are auto-injected into every kanban worker's system prompt; this skill is the deeper playbook when you're specifically playing the orchestrator role.
version: 3.0.0
platforms: [linux, macos, windows]
environments: [kanban]
metadata:
  hermes:
    tags: [kanban, multi-agent, orchestration, routing]
    related_skills: [kanban-worker]
---

# 看板编排器 —— 分解任务指南

> **核心工作流程生命周期**（包括 `kanban_create` 分发模式以及“分解而非直接执行”的原则）会通过 `KANBAN_GUIDANCE` 系统提示块自动注入到每一个看板流程中。对于那些以任务路由为主要职责的编排者而言，这项技能就是更深入的任务处理指南。

## 配置文件由用户自行设定 —— 无固定列表

Hermes 的部署方式多种多样。有些用户只使用一个能处理所有任务的配置文件；有些则使用多个工作节点（如 `docker-worker`、`cron-worker`）；还有些用户会组建自己命名的专业团队。**系统并未预设任何默认的专业团队列表**——编排者技能并不知道该机器上存在哪些配置文件。

在开始分发任务之前，必须确保分解后的任务对应实际存在的配置文件。调度器会自动拒绝处理未知的负责人名称——它不会自动更正、不会给出建议，也不会尝试备用方案。因此，在只有 `docker-worker` 的环境中，被分配给 `researcher` 的任务卡将永远处于“待处理”状态。

**步骤 0：在规划之前先查询可用配置文件。**

可使用以下命令之一：

- `hermes profile list` —— 显示该机器上已配置的所有配置文件列表。如果有终端工具，可直接通过该工具执行；否则请让用户手动输入。
- `kanban_list(assignee="<某名称>")` —— 对单个名称进行验证。如果负责人不存在，该命令会返回空列表而非错误信息，因此仅适用于你已经考虑过的名称。
- **直接询问用户。** 当任务需要多个专业人员处理时，开头问一句“您已配置了哪些配置文件？”是个不错的方式。

将查询结果缓存起来，以便在后续对话中重复使用。每次都重新查询会浪费工具调用次数。

## 何时使用看板（而非直接执行任务）

出现以下任一情况时，应创建看板任务：

1. **需要多名专业人员协作。** 比如研究、分析、写作这三项工作分别需要不同的配置文件。
2. **任务需在系统崩溃或重启后仍能继续。** 适用于那些长期运行、周期性重复或至关重要的任务。
3. **用户可能希望随时介入干预。** 需要在每个步骤都有人类参与监督。
4. **多个子任务可以并行执行。** 通过分发加快处理速度。
5. **需要后续审核或迭代。** 审核人员配置文件可循环处理起草人的输出结果。
6. **需要保留操作审计记录。** 看板中的任务行会永久保存在 SQLite 数据库中。

如果以上情况均不满足——即只是简单的单次推理任务——则应直接使用 `delegate_task` 命令或直接向用户回复。

## 抵制诱惑的规则

你的职责描述是“负责路由，而非直接执行”。以下规则旨在确保这一点：

- **切勿亲自执行任务。** 你的受限工具集通常甚至不包含用于实现任务的终端、文件操作、代码编写或网页访问功能。如果你发现自己想“快速自己解决”，请立即停止，为合适的专业人员创建任务。
- **对于任何具体任务，都必须创建看板任务并分配给相应人员。** 每次都是如此。
- **在创建任务卡之前，先拆分多条独立的工作流。** 用户的提示中可能包含多个独立的工作环节。应先提取这些独立环节，再为每个环节创建一张任务卡，而非将无关任务捆绑到同一张任务卡中。
- **让独立的任务流并行运行。** 如果两张任务卡互不依赖对方的输出结果，就不要将它们关联起来，这样调度器才能分别分发。仅对真正存在数据依赖关系的任务卡进行关联。
- **切勿将依赖性任务创建为独立的“待处理”任务卡。** 如果一张任务卡必须等待另一张任务卡的完成，应在最初的 `kanban_create` 调用中传入 `parents=[...]` 参数。不要先创建后再手动关联，也不要在任务描述中仅用文字说明“等待 T1 完成”。
- **如果现有配置文件中没有合适的专业人员，应询问用户是新建配置文件还是使用现有配置文件。** 严禁自行编造配置文件名称——调度器会自动忽略未知的负责人。
- **分解、路由、汇总 —— 这就是全部工作内容。**

## 任务分解指南

### 步骤 1 —— 明确目标

如果目标不够清晰，需提出澄清性问题。提问成本很低，但若分配错误的任务团队则会造成严重后果。

### 步骤 2 —— 绘制任务流程图

在创建任何内容之前，先在回复用户时口头描述出任务流程图。将每一个具体的工作环节都视为潜在的任务卡：

1. 从用户需求中提取出不同的工作环节。
2. 将每个环节对应到步骤 0 中确定的配置文件中。如果某个环节无法匹配现有配置文件，则询问用户应使用哪个或新建哪个配置文件。
3. 判断每个环节是独立的，还是受其他环节的制约。
4. 将独立的环节作为没有父级关联的并行任务卡创建出来。
5. 为需要依赖其他环节结果的合成、审核或整合类任务创建任务卡，并为其设置指向对应环节的父级关联。如果某个子任务的父级任务尚未完成，它将初始状态设为“待处理”；只有当所有父级任务都完成后，调度器才会将其状态提升为“待处理”。

以下是一些需要分解为多个任务的提示示例（使用占位符配置文件名称——请替换为用户实际使用的配置文件）：

- “开发一个应用程序” → 一张任务卡分配给负责产品/界面设计的配置文件，一到两张任务卡分配给负责实现的工程配置文件；如果用户有审核人员配置文件，还可再添加一张用于后续审核的任务卡。
- “解决阻塞问题并检查模型变体” → 一张用于修复阻塞问题的实现任务卡，以及一张用于验证配置/源代码的探索/研究任务卡。最终的审核任务卡可以同时依赖这两张任务卡的结果。
- “研究相关文档并开始实现” → 文档研究任务卡可以与代码库探索任务卡并行执行；实现任务仅在确实需要这些研究成果时才会启动。
- “分析此截图并查找相关代码” → 一张任务卡分配给具备图像识别能力的配置文件用于视觉分析，另一张任务卡则负责在代码库中搜索。

“此外”、“最后”或“以及”这类词语并不自动意味着存在依赖关系。它们通常只是表示“在汇报之前请确保这些内容都已处理完毕”。只有当一张任务卡必须等待另一张任务卡的输出结果才能开始时，才需要建立关联。

在创建任务卡之前，先将流程图展示给用户，让他们进行修正——包括确定每个环节应对应哪个实际的配置文件名称。

### 步骤 3 —— 创建任务并建立关联

使用步骤 0 中确定的配置文件名称。下面的示例使用了 `<profile-A>`、`<profile-B>`、`<profile-C>` 等占位符——请替换为用户实际使用的配置文件名称。

```python
t1 = kanban_create(
    title="research: Postgres cost vs current",
    assignee="<profile-A>",  # whichever profile handles research on this setup
    body="Compare estimated infrastructure costs, migration costs, and ongoing ops costs over a 3-year window. Sources: AWS/GCP pricing, team time estimates, current Postgres bills from peers.",
    tenant=os.environ.get("HERMES_TENANT"),
)["task_id"]

t2 = kanban_create(
    title="research: Postgres performance vs current",
    assignee="<profile-A>",  # same profile, run in parallel
    body="Compare query latency, throughput, and scaling characteristics at our expected data volume (~500GB, 10k QPS peak). Sources: benchmark papers, public case studies, pgbench results if easy.",
)["task_id"]

t3 = kanban_create(
    title="synthesize migration recommendation",
    assignee="<profile-B>",  # whichever profile does synthesis/analysis
    body="Read the findings from T1 (cost) and T2 (performance). Produce a 1-page recommendation with explicit trade-offs and a go/no-go call.",
    parents=[t1, t2],
)["task_id"]

t4 = kanban_create(
    title="draft decision memo",
    assignee="<profile-C>",  # whichever profile drafts user-facing prose
    body="Turn the analyst's recommendation into a 2-page memo for the CTO. Match the tone of previous decision memos in the team's knowledge base.",
    parents=[t3],
)["task_id"]
```

`parents=[...]` 可用于控制任务升级流程——只有当所有父任务都标记为“已完成”时，子任务才会从“待处理”状态自动升级为“就绪”状态。无需人工协调，调度器与依赖关系引擎会自动处理这一过程。

如果任务图存在依赖关系，请先创建父任务卡片，记录返回的编号，然后在创建子任务卡片时，于其 `kanban_create` 调用中将该编号加入 `parents` 列表中。避免同时创建所有卡片后再进行关联操作，否则调度器可能会在子任务的输入数据尚未准备就绪时便将其标记为完成状态。

### 第 4 步——完成你自己的任务

如果你本身就是以任务形式被生成的（例如某个规划者配置了任务 `T0: "调查 Postgres 迁移问题"`），请在完成任务后注明你所完成的操作内容作为总结：

```python
kanban_complete(
    summary="decomposed into T1-T4: 2 research lanes in parallel, 1 synthesis on their outputs, 1 prose draft on the recommendation",
    metadata={
        "task_graph": {
            "T1": {"assignee": "<profile-A>", "parents": []},
            "T2": {"assignee": "<profile-A>", "parents": []},
            "T3": {"assignee": "<profile-B>", "parents": ["T1", "T2"]},
            "T4": {"assignee": "<profile-C>", "parents": ["T3"]},
        },
    },
)
```

### 第5步 — 向用户反馈结果

用通俗的语言告诉他们你完成了哪些工作，并明确说明使用了哪些配置文件：

> 我已排队处理4项任务：
> - **T1**（`<profile-A>`）：成本对比
> - **T2**（`<profile-A>`）：性能对比，与T1同步执行
> - **T3**（`<profile-B>`）：综合T1和T2的结果并给出推荐方案
> - **T4**（`<profile-C>`）：将T3的结果整理成给技术主管的备忘录
>
> 调度器会立即开始处理T1和T2。T3会在两者完成后启动。当T4处理完毕时，你会收到系统通知。可通过控制面板或命令 `hermes kanban tail <id>` 实时跟踪任务进度。

## 常见架构模式

**辐射式 + 收集式（研究 → 综合）**：多个无父节点的研究型任务卡片，以及一个以所有这些卡片为父节点的综合任务卡片。

**并行执行 + 验证**：一个执行型卡片负责完成具体操作，同时另一个探索/研究型卡片负责验证配置、文档或代码映射关系。审核型卡片可以依赖这两类卡片。切勿仅因为用户在同一句话中提到了两者，就让执行型卡片自行处理无关的验证工作。

**带关卡的流水线**：`规划者 → 执行者 → 审核者`。每个阶段的 `parents=[上一个任务]`。审核者可决定阻塞或完成任务；若审核者阻塞，操作员需提供反馈后解除阻塞并重新启动任务。

**同配置文件队列**：多个任务均分配给同一配置文件，彼此之间没有依赖关系。调度器会按顺序串行处理——该配置文件会按照优先级依次处理这些任务，并在自己的内存中积累处理经验。

**人工干预机制**：任何任务都可以通过 `kanban_block()` 方法暂停等待输入。收到 `/unblock` 指令后，调度器会重新启动任务。所有上下文信息都会保留在评论线程中。

## 常见误区

**编造并不存在的配置文件名称**。调度器会默默放弃创建未知的负责人——相关任务卡片将永远处于“待处理”状态。务必从第0步的发现结果中选择配置文件；如有疑问，应向用户确认。

**将独立的任务合并到同一张卡片中**。如果用户需要两个独立的结果，应分别创建两张卡片。例如，“修复障碍问题并检查模型变体”并非一个单一的修复任务；应为修复工作创建执行/工程师型卡片，为变体检查创建探索/研究型卡片，之后可根据需要对这两项任务设置审核关卡。

**因表述问题造成过度关联**。如果“最后检查X”涉及的是静态配置、文档或代码来源的查找，那么它仍可能与执行任务并行。只有当该检查依赖于执行结果时，才应在执行完成后再进行关联。

**忽略任务间的依赖关系**。如果任务图显示为 `研究 → 执行 → 审核`，则不能将所有任务都作为独立的待处理卡片创建。必须设置父节点关联，确保执行和审核任务不会在所需输入尚未准备就绪时就开始运行。

**重新分配任务 vs. 创建新任务**。如果审核者以“需要修改”为由阻塞任务，应从审核者的任务中创建一个**新任务**，而非简单地重复执行同一任务。新任务仍会分配给原来的执行者配置文件。

**关联参数的顺序**：使用 `kanban_link(parent_id=..., child_id=...)` —— 先指定父节点，再指定子节点。顺序错误会导致错误的任务被降级为“待办”状态。

**若任务结构取决于中间结果，不要预先创建整个任务图**。如果T3的任务结构依赖于T1和T2的查找结果，可将T3设为一个“综合分析结果”的任务，其第一步就是读取父节点传递的信息并规划后续步骤。协调器也可以负责创建更多的协调器任务。

**租户继承机制**。如果在环境变量中设置了 `HERMES_TENANT`，则应在每次调用 `kanban_create` 时传入 `tenant=os.environ.get("HERMES_TENANT")`，以确保子任务保持在同一个命名空间中。

## 目标模式卡片（持久型工作进程）

默认情况下，被调度的工作者只能执行其卡片中的任务**一次**：完成工作后，它会调用 `kanban_complete`/`kanban_block` 方法，然后退出。对于那些单次处理无法完成的工作，可通过设置 `goal_mode=True` 将该工作者置于类似Ralph框架的目标循环中——这一机制与 `/goal` 命令所使用的引擎相同。

```python
kanban_create(
    title="Translate the full docs site to French",
    body="Acceptance: every page translated, no English left, links intact.",
    assignee="<translator-profile>",
    goal_mode=True,        # judge re-checks the card after each turn
    goal_max_turns=15,     # optional budget (default 20)
)["task_id"]
```

**运行机制：**  
- 在每个工作节点处理完成后，辅助评估器会依据卡片的**标题与内容**（视为验收标准）来评判该工作节点的响应质量。  
- 若任务未完成但预算尚未耗尽，工作节点将在**同一会话中继续处理**（保留全部上下文，不会重新启动）。  
- 若工作节点主动调用 `kanban_complete`/`kanban_block`，则循环终止，进入正常生命周期流程。  
- 若预算耗尽且任务仍未完成，该卡片将被**标记为待人工审核状态**（即“粘性状态”），而不会悄无声息地退出。

**适用场景：** 长期、多步骤，或需要“持续处理直至满足某条件”的卡片任务。**不推荐用于：** 简单的一次性任务（如单个字符串的翻译、快速查询）——因为额外的评估开销并不值得，且调度器现有的重试与断路机制已足以应对工作节点的临时故障。

请将卡片内容编写为**明确的验收标准**——评估质量完全取决于目标描述的质量。“翻译 README”这样的描述远不如“将 README 的每个部分都翻译成法语，确保不再出现任何英文句子”那样具体清晰。

## 恢复卡住的工作节点  

当某个工作节点配置频繁崩溃、产生幻觉，或因自身错误被阻塞（常见原因包括：使用错误模型、缺失所需技能、凭证失效）时，看板界面会通过 ⚠ 标记提示该任务，并在侧边栏中打开**恢复**功能模块。提供三种主要操作方式：  

1. **回收**（命令：`hermes kanban reclaim <task_id>`）——立即终止当前正在运行的工作节点，并将任务状态重置为“准备就绪”。现有的任务占用有效期约为 15 分钟，这是最快速的解决途径。  
2. **重新分配**（命令：`hermes kanban reassign <task_id> <new-profile> --reassign`）——将任务切换到另一个工作节点配置（需为当前系统已有的配置），由调度器安排新的工作节点来处理该任务。  
3. **更换模型**——由于节点配置存储在磁盘上，界面会提供可直接复制的命令 `hermes -p <profile> model`，您可在终端中编辑该配置，之后通过“回收”操作使用新模型重新尝试。

当某个工作节点的 `kanban_complete(created_cards=[...])` 宣布中包含不存在或并非由其配置生成的卡片编号时（系统会阻止任务完成），或者其自由文本总结中出现了无法解析的 `t_<hex>` 编号时，系统会发出幻觉警告（仅为提示性说明，不会阻塞流程）。这两种情况都会生成审计事件，即便执行了恢复操作，这些记录仍会保留，便于后续调试。
