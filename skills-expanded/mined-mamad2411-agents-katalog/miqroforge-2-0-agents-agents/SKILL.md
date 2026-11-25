# LangGraph Agent Layer

**Hierarchy:** `agents/` — Phase 2 smart workflow orchestration agents.

## STRUCTURE
```
agents/
├── common/           # Shared: prompt_loader, eval_loop, session_logger
├── planner/          # Intent → semantic workflow (RAG node retrieval)
│   ├── state.py, generator.py, evaluator.py, graph.py
│   └── prompts/
├── yaml_coder/       # Semantic workflow → MF YAML
│   ├── state.py, generator.py, evaluator.py, graph.py
│   └── prompts/
├── node_generator/   # Dual-mode: Prefab (formal) + Ephemeral (temp)
│   ├── prefab/       #   Generator-Evaluator loop + ReAct + sandbox tools
│   ├── ephemeral/    #   Runtime script generation + Docker sandbox
│   ├── shared/       #   knowledge.py, memory.py, sandbox_base.py, manual_index.py
│   └── prompts/      #   .jinja2 templates
└── subagent/         # Explore SubAgent (software manual research)
    └── explore/
```

## WHERE TO LOOK
| Task | Location |
|------|----------|
| Add/modify planner | `agents/planner/` |
| Add/modify YAML coder | `agents/yaml_coder/` |
| Modify prefab generator | `agents/node_generator/prefab/` |
| Modify ephemeral generator | `agents/node_generator/ephemeral/` |
| Add shared tool | `agents/node_generator/shared/` |
| Explore subagent | `agents/subagent/explore/` |

## KEY PATTERNS
- **LangGraph TypedDict state** per agent (`AgentState` in each `state.py`)
- **Separate `graph.py`** per agent — no main graph (Phase 2 design: agents independent)
- **Generator-Evaluator loops** via `common/eval_loop.py`
- **Prompt templates** in `.jinja2` files (NOT inline in Python)
- **No `__main__`** — agents invoked via `api/routers/agents.py` only
- **No `import nodes/`** — agents see nodes via RAG vectorstore only

---

## Phase 2 里程碑（当前开发阶段）

| 里程碑 | 名称 | 状态 | 关键交付 |
|--------|------|------|----------|
| M1 | Agent 基础框架 | ✅ 完成 | LangGraph 图 + RAG 节点检索 + Planner Agent + YAML Coder Agent + Node Generator (Formal) |
| M2 | 临时节点运行时生成 | ✅ 完成 | MF YAML 声明式格式 + 运行时 Agent API 生成脚本 + 沙箱执行 + 视觉评估 + sweep/fan-in 并行 |
| M3 | AI 增强节点 | 🔲 暂停开发 | LLM Gateway Service + `llm_access` 执行类型 + 成本控制（待节点库充实后推进） |
| M4 | 正式节点生成 Agent | ✅ 完成 | Generator-Evaluator 模式 + 非量子/非AI增强正式节点的 Agent 辅助生成 |
| — | 多软件节点扩增 | ✅ 完成 | 新增 Gaussian (9)、Psi4 (9)、CP2K (4)、preprocessing (1) 共 23 个节点 + 4 个 test 节点 + Cirq 镜像；节点库从 4 增至 32 |

> **Phase 2 设计原则：各 Agent 独立可调用。**
> Phase 2 不实现主 Agent（Main Agent）和项目记忆——各 Agent 由前端或后端逐一调用即可。
> 主 Agent 编排与跨会话记忆推迟到 Phase 3 实现。

---

## Agent 设计约定

- 所有 Agent 使用 **LangGraph** 管理状态图，各 Agent 在自己的 `graph.py` 中定义独立的编译图
- Phase 2 无主图（Main Graph），各 Agent 独立可调用；主 Agent 编排推迟到 Phase 3
- Agent 状态对象（`AgentState`）使用 TypedDict 定义，字段变更需同步更新测试
- Prompt 模板统一存放在 `agents/<agent_name>/prompts/`，以 `.jinja2` 格式编写，**禁止在 Python 代码中内联长 Prompt**（jinja2 运行在宿主侧 FastAPI 环境，无镜像依赖问题）
- 工具函数必须有明确的 docstring 作为 LangChain 工具描述
- **Phase 2 各 Agent 独立可调用**：每个 Agent 在 `api/routers/agents.py` 中有对应端点，
  前端或后端可以直接按需调用单个 Agent，无需经过主 Agent 中转

### 渐进式信息披露（信息量大的 Agent）

对于 Planner Agent、Prefab Generator 等需要消化大量上下文的 Agent，采用分层信息披露策略：
尽量避免在第一轮就将全部节点的完整 Schema 塞入上下文；先让 Agent 缩小范围，再展开细节。

---

## RAG 节点检索约定

- `vectorstore/indexer.py` 负责将 `nodes/` 目录下所有节点的 Schema 文档化并索引
- 向量库优先使用 **ChromaDB**（本地开发），生产可替换为 FAISS
- 检索结果分两级：摘要级（节点名 + 一句话 + 端口列表）和详细级（完整 Schema JSON）
- Planner Agent 先使用摘要级检索缩小候选范围，再按需拉取详细级供 YAML Coder 使用

---

## FastAPI 约定（Agent 相关）

- 路由版本前缀：`/api/v1/`
- 所有请求/响应使用 `api/models/` 中的 Pydantic 模型（不得使用裸 dict）
- Argo 提交接口需在提交前做 MF YAML → Argo YAML 编译校验（含临时节点 wrapper 脚本生成），校验失败返回 400
- WebSocket 端点用于 Agent ↔ 前端实时交互（流式输出 Agent 思考过程和 Generator-Evaluator 迭代进度）

---

## 项目管理约定

前端首页为**项目画廊**（`/`），展示所有项目卡片。每个项目是独立的工作空间，包含自己的画布、运行记录、对话和快照。

- **路由**：`/` → 项目画廊，`/project/:projectId` → 画布编辑器
- **后端存储**：`userdata/projects/` 目录，每个项目一个子目录，`registry.json` 作为索引
- **前端状态隔离**：进入项目时调用 `setProjectId()` 和 `setSavedWorkflowsProjectId()` 切换 localStorage key，离开时清理
- **项目元数据**：`name`、`description`（备注）、`icon`（emoji）、时间戳
- **画布自动保存**：切换项目或卸载 CanvasLayout 时自动 `saveCanvas`；新项目首次加载时 `clearCanvas` 避免 localStorage 残留
