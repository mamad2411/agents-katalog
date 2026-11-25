---
name: agentscope-tutorial
description: AgentScope 2.0 多智能体框架完整教程。提供 Agent 创建、Toolkit 工具系统、Model 模型集成、Context 上下文管理、Middleware 中间件、Permission 权限系统、Plan 任务规划、Agent Team 多智能体协作、Workspace 沙箱隔离的使用指南和代码示例。当需要使用 AgentScope 2.0 构建智能体应用时参考。
license: MIT
compatibility: Requires Python 3.11+, agentscope pip package. Internet access for API queries.
allowed-tools: Bash Read Write Edit Glob Grep
metadata:
  user-invocable: "true"
---

# AgentScope 2.0 框架教程

AgentScope 2.0 是面向生产环境的多智能体框架，以**安全、高效、灵活、完整**为核心理念，覆盖从开发 SDK 到分布式部署的全栈能力。

## 安装

```bash
# 推荐使用 uv 包管理
uv pip install agentscope

# 或从源码安装
git clone -b main https://github.com/agentscope-ai/agentscope
cd agentscope
uv pip install -e .

# 验证安装
python -c "import agentscope; print(agentscope.__version__)"
```

---

## 1. 快速开始：第一个 Agent

```python
import asyncio
import os
from agentscope.agent import Agent
from agentscope.credential import DashScopeCredential
from agentscope.event import EventType
from agentscope.message import UserMsg
from agentscope.model import DashScopeChatModel
from agentscope.tool import Toolkit, Bash, Read, Write, Edit


async def main() -> None:
    agent = Agent(
        name="Friday",
        system_prompt="You are a helpful assistant named Friday.",
        model=DashScopeChatModel(
            credential=DashScopeCredential(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
            ),
            model="qwen-plus",
        ),
        toolkit=Toolkit(tools=[Bash(), Read(), Write(), Edit()]),
    )

    user_msg = UserMsg(name="user", content="Hello, who are you?")

    # 方式 1: 阻塞式获取最终回复
    reply_msg = await agent.reply(user_msg)
    # reply_msg 是 AssistantMsg，content 是 block 列表

    # 方式 2: 流式获取增量事件
    async for event in agent.reply_stream(user_msg):
        match event.type:
            case EventType.TEXT_BLOCK_DELTA:
                # 流式文本增量 → 追加到 UI/stdout
                pass
            case EventType.TOOL_CALL_START:
                # Agent 即将调用工具
                pass
            case _:
                # 其他事件: thinking blocks, tool results, reply end...
                pass


asyncio.run(main())
```

---

## 2. Agent 核心

### 2.1 创建 Agent

`Agent(...)` 构造函数参数：

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | `str` | Agent 标识符，用于消息和日志 |
| `system_prompt` | `str` | 基础系统提示词 |
| `model` | `ChatModelBase` | 推理 LLM |
| `toolkit` | `Toolkit \| None` | 管理工具、MCP 客户端、技能及工具组 |
| `state` | `AgentState \| None` | 持有上下文、权限及会话状态 |
| `offloader` | `Offloader \| None` | 卸载压缩上下文/工具结果至磁盘 |
| `middlewares` | `list[MiddlewareBase] \| None` | 生命周期注入逻辑 |
| `model_config` | `ModelConfig` | 重试次数与降级模型配置 |
| `context_config` | `ContextConfig` | 上下文压缩阈值与工具结果限制 |
| `react_config` | `ReActConfig` | 最大迭代次数与拒绝处理策略 |

### 2.2 Agent 方法

| 方法 | 说明 |
|------|------|
| `reply(inputs)` | 执行推理-行动循环，返回最终 Msg |
| `reply_stream(inputs)` | 同上，但实时 yield AgentEvent |
| `observe(msgs)` | 向上下文注入消息而不触发推理 |
| `compress_context(config)` | 手动触发上下文压缩 |

### 2.3 输入类型

`inputs` 支持：
- `Msg` 列表 — 开启新回复
- `UserConfirmResultEvent` / `ExternalExecutionResultEvent` — 恢复暂停状态（人机协作）
- `None` — 无新输入继续执行

---

## 3. Model 模型集成

### 3.1 支持的模型提供商

```python
# DashScope (通义千问)
from agentscope.model import DashScopeChatModel
from agentscope.credential import DashScopeCredential

model = DashScopeChatModel(
    credential=DashScopeCredential(api_key="your-key"),
    model="qwen-plus",
)

# OpenAI 兼容 (DeepSeek 等)
from agentscope.model import OpenAIChatModel
from agentscope.credential import OpenAICredential

model = OpenAIChatModel(
    credential=OpenAICredential(api_key="your-key"),
    client_kwargs={"base_url": "https://api.deepseek.com/"},
    model="deepseek-chat",
)
```

### 3.2 本项目的 DeepSeek 封装

项目 `LLM/model.py` 已提供 DeepSeek 封装：

```python
from LLM.model import DeepSeek

model = DeepSeek(Ver="Flash", think=True, temperature=0.7)
# Ver 可选: "Flash" | "Pro" | "chat"
# think=True 启用思考模式
```

---

## 4. Toolkit 工具系统

### 4.1 内置工具

| 工具 | 类别 | 说明 |
|------|------|------|
| `Bash` | 基础 | Shell 命令执行，含多层安全拦截 |
| `Read` | 基础 | 文件读取（强制读前写规则） |
| `Write` | 基础 | 文件写入 |
| `Edit` | 基础 | 文件精确编辑 |
| `Glob` | 基础 | 文件模式匹配 |
| `Grep` | 基础 | 内容搜索 |
| `TaskCreate` | 计划 | 创建任务 |
| `TaskGet` | 计划 | 查询单个任务 |
| `TaskList` | 计划 | 列出所有任务 |
| `TaskUpdate` | 计划 | 更新任务状态 |
| `reset_tools` | 元工具 | 运行时动态管理工具组 |

### 4.2 基础注册

```python
from agentscope.tool import Toolkit, Bash, Read, Write, Edit

toolkit = Toolkit(
    tools=[Bash(), Read(), Write(), Edit()],
)
```

### 4.3 创建自定义工具

继承 `ToolBase`：

```python
from agentscope.tool import ToolBase, ToolChunk
from agentscope.permission import (
    PermissionContext, PermissionDecision, PermissionBehavior,
)
from agentscope.message import TextBlock

class WebSearch(ToolBase):
    name = "WebSearch"
    description = "Search the web for information."
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query."},
        },
        "required": ["query"],
    }
    is_concurrency_safe = True
    is_read_only = True

    async def check_permissions(
        self, tool_input: dict, context: PermissionContext,
    ) -> PermissionDecision:
        return PermissionDecision(
            behavior=PermissionBehavior.ALLOW,
            message="Web search is read-only.",
        )

    async def call(self, query: str) -> ToolChunk:
        results = await do_search(query)
        return ToolChunk(content=[TextBlock(text=results)])
```

或使用 `FunctionTool` 快速包装 Python 函数：

```python
from agentscope.tool import FunctionTool

def get_weather(city: str, unit: str = "celsius") -> str:
    """Get the current weather for a city.

    Args:
        city: The city name to look up.
        unit: Temperature unit, "celsius" or "fahrenheit".
    """
    return f"The weather in {city} is 22°{unit[0].upper()}"

toolkit = Toolkit(tools=[FunctionTool(get_weather)])
```

### 4.4 工具组动态管理

```python
from agentscope.tool import Toolkit, ToolGroup

toolkit = Toolkit(
    tools=[Bash(), Read(), Write(), Edit()],
    tool_groups=[
        ToolGroup(
            name="database",
            description="Tools for database operations.",
            instructions="Always wrap mutations in a transaction.",
            tools=[db_query_tool, db_migrate_tool],
        ),
    ],
)
```

当存在非基础工具组时，`reset_tools` 元工具自动注册。Agent 调用它传入目标组名即可运行时切换工具集，按需节省上下文。

### 4.5 外部执行工具 (Human-in-the-loop)

```python
class HumanApproval(ToolBase):
    name = "HumanApproval"
    description = "Request human approval for a sensitive operation."
    input_schema = {
        "type": "object",
        "properties": {
            "action": {"type": "string", "description": "Action requiring approval."},
            "reason": {"type": "string", "description": "Why this needs approval."},
        },
        "required": ["action", "reason"],
    }
    is_concurrency_safe = True
    is_external_tool = True  # 关键：标记为外部工具

    async def check_permissions(self, tool_input, context):
        return PermissionDecision(
            behavior=PermissionBehavior.ALLOW,
        )
```

设置 `is_external_tool = True` 后，调用时触发 `RequireExternalExecutionEvent`，由外部系统（如人工审批）异步返回结果。

---

## 5. Context 上下文管理

上下文是 Agent 的工作记忆。AgentScope 的三层组装结构：

1. **System Prompt**: 基础系统提示 + Toolkit 技能说明 + `on_system_prompt` 中间件
2. **Summary**: 仅在压缩后出现，旧消息的结构化摘要
3. **Context**: 最近的未压缩消息

### 5.1 配置上下文压缩

```python
from agentscope.agent import Agent, ContextConfig

agent = Agent(
    name="my_agent",
    system_prompt="...",
    model=model,
    toolkit=toolkit,
    context_config=ContextConfig(
        trigger_ratio=0.8,         # token 使用超过 80% 时触发压缩
        reserve_ratio=0.1,         # 压缩后保留最近 10% 的消息
        tool_result_limit=3000,    # 单个工具结果最大 token
    ),
)
```

### 5.2 压缩流程

1. 计数 token
2. 检查阈值 → 触发压缩
3. 拆分消息（保持工具调用/结果对完整）
4. 生成结构化摘要（task_overview, current_state, important_discoveries, next_steps, context_to_preserve）
5. 更新状态

### 5.3 手动压缩

```python
await agent.compress_context()
# 或覆盖配置
await agent.compress_context(context_config=ContextConfig(trigger_ratio=0.5))
```

### 5.4 上下文卸载 (Offloader)

将丢弃内容写入外部存储，Agent 后续可通过文件工具读取：

```python
from agentscope.workspace import LocalWorkspace

workspace = LocalWorkspace(workdir="/tmp/agent_workspace")
await workspace.initialize()

agent = Agent(
    name="my_agent",
    system_prompt="...",
    model=model,
    toolkit=toolkit,
    offloader=workspace,  # 卸载到本地工作区
)
```

---

## 6. Plan 任务规划系统

四个内置工具让 Agent 通过工具调用来维护显式的、结构化的任务列表：

| 工具 | 操作 | 只读 |
|------|------|------|
| `TaskCreate` | 追加新任务 | 否 |
| `TaskGet` | 按 ID 获取任务详情 | 是 |
| `TaskList` | 列出所有任务及状态 | 是 |
| `TaskUpdate` | 更新状态/字段/依赖边 | 否 |

### 6.1 装备规划工具

```python
from agentscope.tool import Toolkit, TaskCreate, TaskGet, TaskList, TaskUpdate

toolkit = Toolkit(
    tools=[TaskCreate(), TaskGet(), TaskList(), TaskUpdate()],
)

agent = Agent(
    name="planner",
    system_prompt="You are a planning assistant.",
    model=model,
    toolkit=toolkit,
)
```

### 6.2 任务状态流转

```
pending → in_progress → completed
                ↘ deleted (任何时候可硬删除)
```

### 6.3 任务依赖

```python
# 让任务 2 依赖任务 1
await TaskUpdate()(
    task_id="2",
    add_blocked_by=["1"],
    _agent_state=agent.state,
)
# 结果: task "2".blocked_by == ["1"] 且 task "1".blocks == ["2"]
```

### 6.4 编程式预置任务

```python
from agentscope.state import Task

agent.state.tasks_context.tasks.extend([
    Task(
        id="1",
        subject="Fetch project requirements",
        description="Read README.md in the repo root.",
    ),
    Task(
        id="2",
        subject="Draft an implementation plan",
        description="Produce a step-by-step plan.",
        blocked_by=["1"],
    ),
])
# 保持反向边一致：
agent.state.tasks_context.tasks[0].blocks.append("2")
```

---

## 7. Middleware 中间件系统

### 7.1 生命周期钩子

| 钩子 | 类型 | 触发时机 |
|------|------|----------|
| `on_reply` | Onion | 包裹一次完整回复（所有 ReAct 轮次） |
| `on_reasoning` | Onion | 包裹单轮推理（输入组装 → 模型调用 → 解码） |
| `on_acting` | Onion | 包裹单次工具调用执行 |
| `on_model_call` | Onion | 包裹底层 ChatModel API 调用 |
| `on_compress_context` | Onion | 上下文压缩决策时触发 |
| `on_system_prompt` | Transformer | 每次组装系统提示词时触发 |
| `list_tools` | Tool source | 贡献额外工具（显式调用） |

钩子嵌套结构：

```
on_reply
  └── 每个 ReAct 轮次
        ├── on_compress_context
        ├── on_reasoning
        │     ├── on_system_prompt
        │     └── on_model_call
        └── on_acting
```

### 7.2 创建中间件

```python
from agentscope.middleware import MiddlewareBase
import time

class TimingMiddleware(MiddlewareBase):
    async def on_model_call(self, agent, input_kwargs, next_handler):
        start = time.time()
        result = await next_handler()
        elapsed = time.time() - start
        print(f"[timing] {agent.name} → {elapsed:.2f}s")
        return result

# 装备
agent = Agent(
    name="assistant",
    system_prompt="...",
    model=model,
    toolkit=toolkit,
    middlewares=[TimingMiddleware()],
)
```

### 7.3 实用中间件示例

**速率限制：**

```python
import asyncio, time
from agentscope.middleware import MiddlewareBase

class RateLimitMiddleware(MiddlewareBase):
    def __init__(self, min_interval: float = 1.0):
        self._last_call = 0.0
        self._min_interval = min_interval

    async def on_model_call(self, agent, input_kwargs, next_handler):
        wait = self._min_interval - (time.time() - self._last_call)
        if wait > 0:
            await asyncio.sleep(wait)
        self._last_call = time.time()
        return await next_handler()
```

**动态系统提示词：**

```python
from datetime import datetime
from agentscope.middleware import MiddlewareBase

class DynamicContextMiddleware(MiddlewareBase):
    def __init__(self, context_fn):
        self._context_fn = context_fn

    async def on_system_prompt(self, agent, current_prompt):
        context = self._context_fn()
        return f"{current_prompt}\n\n## Current Context\n{context}"

agent = Agent(
    middlewares=[
        DynamicContextMiddleware(lambda: f"Time: {datetime.now().isoformat()}"),
    ],
)
```

**模型降级回退：**

```python
class ModelFallbackMiddleware(MiddlewareBase):
    def __init__(self, fallback_model):
        self._fallback = fallback_model

    async def on_model_call(self, agent, input_kwargs, next_handler):
        try:
            return await next_handler()
        except Exception as e:
            print(f"Primary model failed: {e}, switching to fallback")
            return await next_handler(current_model=self._fallback)
```

### 7.4 Onion 执行顺序

```python
middlewares = [mw1, mw2]
# 调用: mw1 pre → mw2 pre → 内部逻辑 → mw2 post → mw1 post
# 流式: mw1_pre → mw2_pre → mw2_event → mw1_event → ... → mw2_post → mw1_post
```

Transformer（`on_system_prompt`）从左到右链式：`mw1 → mw2`

---

## 8. Permission 权限系统

### 8.1 五种权限模式

| 模式 | 行为 | 用例 |
|------|------|------|
| `DEFAULT` | 只读自动允许；修改操作需提示。安全 ASK 不可被允许规则覆盖 | **最安全**，推荐默认 |
| `ACCEPT_EDITS` | DEFAULT 全部 + 工作目录内编辑自动允许 | 活跃开发 |
| `EXPLORE` | 只读允许，拒绝所有修改 | 代码探索/规划 |
| `BYPASS` | 完全信任，安全 ASK 跳过，其他全部允许 | 沙箱/完全信任环境 |
| `DONT_ASK` | 无人值守版：只读 + 工作目录编辑自动允许，其余拒绝 | 无人值守自动化 |

### 8.2 配置权限

```python
from agentscope.agent import Agent
from agentscope.state import AgentState
from agentscope.permission import (
    PermissionContext, PermissionMode, PermissionRule, PermissionBehavior
)

agent = Agent(
    name="my_agent",
    system_prompt="...",
    model=model,
    state=AgentState(
        permission_context=PermissionContext(
            mode=PermissionMode.DEFAULT,
            allow_rules={
                "Bash": [
                    PermissionRule(
                        tool_name="Bash", rule_content="npm run:*",
                        behavior=PermissionBehavior.ALLOW, source="userSettings",
                    ),
                ],
                "Write": [
                    PermissionRule(
                        tool_name="Write", rule_content="src/**",
                        behavior=PermissionBehavior.ALLOW, source="userSettings",
                    ),
                ],
            },
            deny_rules={
                "Bash": [
                    PermissionRule(
                        tool_name="Bash", rule_content="rm:*",
                        behavior=PermissionBehavior.DENY, source="userSettings",
                    ),
                ],
            },
        )
    ),
)
```

### 8.3 权限决策优先级（六步评估）

1. 拒绝规则 → DENY（最高优先级）
2. 询问规则 → ASK
3. 只读快速通道 → ALLOW
4. 工具 `check_permissions()` → ALLOW/DENY/安全 ASK/PASSTHROUGH
5. 允许规则 → ALLOW
6. 模式回退

### 8.4 常用模式

**只读探索：**
```python
agent.state.permission_context = PermissionContext(mode=PermissionMode.EXPLORE)
```

**无人值守自动化：**
```python
agent.state.permission_context = PermissionContext(
    mode=PermissionMode.DONT_ASK,
    allow_rules={...},
)
```

**运行时切换：**
```python
agent.state.permission_context.mode = PermissionMode.EXPLORE
```

---

## 9. Agent Team 多智能体协作

### 9.1 概念

| 概念 | 说明 |
|------|------|
| **Team** | 持久化智能体成员组 |
| **Leader** | 创建团队的会话，可添加/移除成员、解散团队 |
| **Worker** | 作为团队成员生成的会话，独立 ReAct 循环 |
| **Team message** | 成员间消息，以 `<team-message from="...">` 包裹 |

### 9.2 内置团队工具

| 工具 | 用途 |
|------|------|
| `TeamCreate` | 创建新团队 |
| `AgentCreate` | 在团队中生成工作者 |
| `TeamSay` | 向成员发送消息（或广播） |
| `TeamDelete` | 解散团队 |
| `AgentInvite` | 邀请已有智能体加入 |

### 9.3 自定义子智能体模板

```python
from agentscope.app import create_app, SubAgentTemplate
from agentscope.permission import PermissionContext, PermissionMode

app = create_app(
    storage=storage,
    message_bus=message_bus,
    workspace_manager=workspace_manager,
    sub_agent_templates=[
        SubAgentTemplate(
            type="explorer",
            description="Read-only agent for codebase exploration.",
            system_prompt_template="""You are {member_name}, an explorer \
in team '{team_name}' led by {leader_name}.

Team purpose: {team_description}
Your role: {member_description}

## Rules
- Complete the exploration tasks assigned by the leader.
- You are READ-ONLY — never modify, create, or delete anything.
- Report results back to {leader_name} using TeamSay.""",
            permission_context=PermissionContext(
                mode=PermissionMode.EXPLORE,
            ),
        ),
    ],
)
```

系统提示占位符：`{team_name}`, `{team_description}`, `{member_name}`, `{member_description}`, `{leader_name}`

### 9.4 协调模型

Agent Team 默认**分布式部署**。所有通信通过 Redis 消息总线中介：

1. 发送方通过消息总线将 `HintBlock` 推送到接收方收件箱
2. 入队唤醒信号
3. 唤醒调度器驱动接收方 `ChatService.run`
4. `InboxMiddleware` 清空收件箱，消息进入上下文

---

## 10. Workspace 沙箱隔离

### 10.1 四种实现

| 实现 | 后端 | 隔离级别 |
|------|------|----------|
| `LocalWorkspace` | 主机文件系统 | 无隔离 |
| `DockerWorkspace` | Docker 容器 | 进程级 |
| `E2BWorkspace` | E2B 云沙箱 | 云端 |
| `OpenSandboxWorkspace` | OpenSandbox | 沙箱级 |

### 10.2 LocalWorkspace

```python
from agentscope.workspace import LocalWorkspace

workspace = LocalWorkspace(workdir="/data/my-workspace")
await workspace.initialize()

agent = Agent(
    name="coder",
    system_prompt="...",
    model=model,
    toolkit=Toolkit(
        tools=await workspace.list_tools(),
        mcps=await workspace.list_mcps(),
        skills_or_loaders=await workspace.list_skills(),
    ),
    offloader=workspace,
)
```

### 10.3 DockerWorkspace

```python
from agentscope.workspace import DockerWorkspace

workspace = DockerWorkspace(
    base_image="python:3.11-slim",
    workdir="/data/docker-workspaces/agent-1",
    node_version="20",
    extra_pip=["numpy", "pandas"],
)
await workspace.initialize()
```

### 10.4 目录布局

```
{workdir}/
├── .mcp           # MCP 客户端配置
├── data/          # 卸载的多模态负载 (SHA-256 去重)
├── skills/        # 技能子目录
│   └── .skills    # 名称/哈希索引
└── sessions/      # 每会话 context.jsonl + 工具结果
```

---

## 11. 完整示例：多 Agent 安全扫描系统

基于本项目架构的示例模式：

```python
import asyncio
from agentscope.agent import Agent
from agentscope.tool import Toolkit, Bash, Read, Write, Edit, Grep
from agentscope.permission import PermissionContext, PermissionMode
from agentscope.state import AgentState
from LLM.model import DeepSeek


async def main():
    # 模型
    model = DeepSeek(Ver="Flash", think=True)

    # === Brain: 战略层 ===
    brain = Agent(
        name="Brain",
        system_prompt="""你是一个网络安全战略分析师。
        接收用户任务，解析目标，制定攻击计划。
        将计划分解为明确的阶段步骤。""",
        model=model,
    )

    # === Orchestrator: 战术层 ===
    orchestrator = Agent(
        name="Orchestrator",
        system_prompt="""你是任务调度指挥官。
        根据当前任务状态决定下一步行动。
        所有 Agent 只产生结果，只有你可改变任务状态。""",
        model=model,
        toolkit=Toolkit(tools=[
            Bash(), Read(), Write(), Edit(), Grep(),
        ]),
    )

    # === Recon: 侦察 ===
    recon = Agent(
        name="Recon",
        system_prompt="""你是信息侦察专家。
        使用工具扫描目标：端口扫描、服务识别、Banner 获取。
        只负责收集信息，不决定下一步。""",
        model=model,
        toolkit=Toolkit(tools=[Bash(), Read()]),
        state=AgentState(
            permission_context=PermissionContext(
                mode=PermissionMode.ACCEPT_EDITS,
            )
        ),
    )

    # === Analysis: 漏洞分析 ===
    analysis = Agent(
        name="Analysis",
        system_prompt="""你是漏洞分析专家。
        根据侦察信息推理可能存在的漏洞和攻击路径。
        只返回分析结果，不执行攻击。""",
        model=model,
        toolkit=Toolkit(tools=[Read()]),
    )

    # 使用 observe 共享信息
    # orchestrator 调用 recon 后，analysis 观察结果
    # 然后 orchestrator 决策下一步

    await orchestrator.reply(UserMsg(content="渗透测试目标: 192.168.1.1"))


asyncio.run(main())
```

---

## 12. 常见问题

**Q: 如何安全中断 Agent？**  
A: 使用 `task.cancel()` 触发 `CancelledError`，上下文保持原子一致性，新消息可无缝恢复。

**Q: Agent 状态如何持久化？**  
A: 结合 `RedisStorage` 使用 `get_session` 加载 `AgentState`，推理后 `update_session_state` 保存。

**Q: 系统提示词有什么限制？**  
A: 保持简洁，避免单独超过上下文压缩阈值，否则 `compress_context` 抛出 `RuntimeError`。

**Q: 组件 vs 阻塞模式如何选择？**  
A: 交互式 UI 用 `reply_stream` 实时检测暂停事件；纯自动化脚本用 `reply`。

---

## 参考链接

- 官方文档: https://docs.agentscope.io/versions/2.0.5dev/en
- GitHub: https://github.com/agentscope-ai/agentscope
- 完整 API 索引: https://docs.agentscope.io/llms.txt
