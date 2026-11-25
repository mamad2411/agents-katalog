---
name: skill-creator-new
description: 适配本低代码平台的技能 (Skill) 开发全量指南。包含创作原则、SOP 编写哲学、以及多调度模式 (Workflow/Package/Code) 的技术规范。
---

# 技能开发者指南 (Skill Creator for Low-Code Agent)

本指南指导开发者如何为本平台创建高效的 AI 技能。

## 1. 关于技能 (About Skills)

技能 (Skill) 是自包含的模块化能力包，用于扩展智能体的能力边界。它们是为特定任务量身定制的“专家 SOP”，将**过程性知识 (Procedural Knowledge)** 注入 AI。

### 1.1 技能提供的内容 (What Skills Provide)

1. **专项工作流 (Workflows)**：如数据聚合、合规审核等多步处理程序。
2. **工具集成 (Integrations)**：与 MongoDB、钉钉、外部 API 等底层能力的标准交互。
3. **领域专业知识 (Domain Expertise)**：平台特定的 Schema 定义、业务规则、数据转换模板。
4. **资源合集 (Bundled Resources)**：辅助脚本、参考文档以及处理复杂重复任务所需的静态资产。

---

## 2. 核心原则 (Core Principles)

### 2.1 精简是金 (Concise is Key)

上下文窗口是公共资源。

- **默认假设**：AI 已经足够聪明。只添加它确实不知道的背景。
- **实践**：优先使用具体的输入输出示例。挑战每一段话：“如果删掉它，AI 还能正常工作吗？”

### 2.2 设定合适的自由度 (Set Appropriate Degrees of Freedom)

- **高自由度 (PACKAGE_SKILL)**：适用于依赖推理、决策且输入多变的场景。
- **中自由度 (脚本控制)**：适用于有首选模式但允许一定波动的场景。
- **低自由度 (WORKFLOW)**：适用于容错率为零的关键序列（如数据库写入或审批流）。

### 2.3 技能剖析 (Anatomy of a Skill)

每个文件夹技能都由一个必选的 `SKILL.md` 和可选的资源目录组成：

```text
skill-name/
├── SKILL.md (必须)        # 包含元数据 (YAML) 和 Markdown 指令
├── scripts/ (可选)        # 确定性脚本。AI 通过 read_skill_resource 读取并执行
├── references/ (可选)     # 领域知识文档
└── sub-task/ (可选)       # 子文件夹内若含 SKILL.md，将自动成为“私有子技能”
```

### 2.4 不应包含的内容 (What to Not Include)

不要包含 `README.md`、`INSTALL_GUIDE.md` 等非执行相关文件。保持包体纯净以节省同步开销。

### 2.5 渐进式披露设计原则 (Progressive Disclosure)

本平台支持三层加载系统：

1. **Metadata (YAML)**: 用于路由决策。
2. **SOP Body (SKILL.md)**: 触发后作为 `SkillAgent` 的系统提示词补充。
3. **Resources (Files)**: 仅在 AI 调用内置工具 `read_skill_resource` 时惰性加载。

---

## 3. 技术标准与规格 (Technical Specification)

### 3.1 YAML 元数据详解

```yaml
---
name: my_skill_id # 唯一标识符。英文字母/数字/下划线
description: '场景描述...' # 极其重要：它是 Agent 的语义索引工具触发词
parameters: # 定义工具输入 (将自动转换为 Zod 校验)
  type: object
  properties:
    query: { type: string, description: '搜索词' }
    limit: { type: integer, default: 20 }
  required: [query]
requires: # 依赖注入
  tools:
    - 'system:executeMongoQuery' # 引用内置系统工具
    - 'pkg:another_skill' # 引用其他全局安装的 Package 技能
    - 'doc:24位ObjectId' # 引用某个 SOP 文档作为工具
    - 'mcp:server_id:tool_name' # 引用 MCP 服务工具
hideResult: true # 启用后，Agent 只看到任务摘要，结果直推给用户
---
```

### 3.2 依赖解析优先级

当 AI 在 `SkillAgent` 沙盒内调用工具时，解析顺序如下：

1. **私有子技能 (Private Sub-skills)**：当前技能文件夹内的子文件夹（含 `SKILL.md`）。
2. **全局注册表 (Global Registry)**：包括已安装的 Package、发布的 Workflow、系统内置工具、MCP 工具、SOP 文档。

### 3.3 运行环境限制

- **递归深度限制**：系统硬限制 `MAX_SKILL_DEPTH = 5`。若超过此深度，调用将产生错误。
- **沙盒边界**：AI 只能通过 `list_skill_resources` 和 `read_skill_resource` 访问自身文件夹及其子文件夹内的文件。

### 3.4 内建沙箱工具 (Built-in Sandbox Tools)
所有进入 `SkillAgent` 沙盒环境的 AI 将自动获得以下两个隐式工具（无需在 YAML 中定义）：

1.  **`list_skill_resources`**: `Object` (无参数)。
    - **作用**: 列出当前技能包目录下 `references/` 和 `scripts/` 文件夹内的所有文件名。
    - **逻辑**: 当 AI 需要深入了解特定领域（如 DB Schema、第三方 API）时，应首先通过此工具寻找可用文件。

2.  **`read_skill_resource`**: `filename: String` (必须)。
    - **逻辑**: **读并严格执行 (Read and Follow)**。
    - **要求**: AI 读取内容后，必须立即将其中的指令集、规则或 SOP 步骤纳入正在执行的任务决策。该工具不仅是“数据源”，更是“指令源”。

3.  **`write_skill_resource`**:
    - **参数**: `filename: String`, `content: String`, `append: Boolean (default: true)`。
    - **作用**: 用于记录自进化历史、修正定义的 Schema 或故障诊断日志。
    - **核心规范**: AI 发现代码层面的真相与文档不符时，必须使用此工具将更正后的知识 **追加 (Append)** 写入到 `references/evolution.md`。

---

## 4. 技能创建流程 (Skill Creation Process)

### 4.1 步骤 1：实例理解

分析用户请求，梳理步骤。

### 4.2 步骤 2：内容规划

判断哪些部分写在 SOP 里，哪些放进 `references/`。

### 4.3 步骤 3：初始化放置

在 `server/skills/` 创建文件夹。系统会自动将其同步到数据库中。

### 4.4 步骤 4：编辑与模式应用

- **模式 1：SOP 模式**：通过 `SKILL.md` 的 Markdown 部分指导 AI 工作。
- **模式 2：混合模式**：在 YAML 中引入 `system:executeMongoQuery` 来赋予 AI 查库能力。

---

## 5. 发布与迭代 (Publishing & Iteration)

- **可见性范围 (Scope)**:
  - **SYSTEM**: 位于 `server/skills` 下，系统全局可见。
  - **ORGANIZATION**: 在 UI 发布的 Workflow，组织内可见。
  - **APP**: 仅限当前应用关联的 Workflow。
- **同步与 Reconciliation**: 系统每次启动或通过管理界面触发同步时，会自动将文件系统的 YAML 元数据更新到数据库。

---
