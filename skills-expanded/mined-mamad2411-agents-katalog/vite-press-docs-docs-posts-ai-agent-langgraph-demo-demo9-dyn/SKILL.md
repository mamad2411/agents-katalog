# demo9：动态系统提示词（system_prompt）

> GitHub 源码：[demo9-dynamic-system-prompt](https://github.com/fengnovo/langchain-learn/tree/main/ai-agent-langgraph-demo/demo9-dynamic-system-prompt)
通过提供系统提示来确定 Agent 处理任务的方式。本示例是 Python 课件「系统消息
system_prompt」的 TypeScript 版：根据调用时传入的 `context`（用户角色）动态生成
系统提示词。

- `contextSchema`：定义上下文结构（对应 Python 的 `class Context(TypedDict)`）；
- `wrapModelCall` 中间件：LangChain.js v1 没有 `dynamic_prompt` 装饰器，等价写法是
  在中间件里覆盖 `systemPrompt` 后再调用 `handler`；
- `invoke(input, { context })`：每次调用时明确指定上下文。

## 1. 环境变量

复用项目根目录 `.env` 的默认模型配置：

```dotenv
OPENAI_API_KEY=你的API_KEY
OPENAI_BASE_URL=https://你的OpenAI兼容接口/v1
MODEL=模型名称
```

## 2. 运行

在 `ai-agent-langgraph-demo` 目录执行：

```bash
pnpm demo9
```

执行类型检查：

```bash
pnpm typecheck:demo9
```

## 3. Python 与 TypeScript API 对照

| 功能 | Python | TypeScript |
| --- | --- | --- |
| 定义上下文 | `class Context(TypedDict): user_role: str` | `z.object({ userRole: ... })` |
| 动态提示词中间件 | `@dynamic_prompt` 装饰器 | `createMiddleware({ wrapModelCall })` |
| 读取上下文 | `request.runtime.context.get("user_role", "user")` | `request.runtime.context.userRole`（zod `default` 兜底） |
| 覆盖系统提示词 | `return f"{base_prompt} ..."` | `handler({ ...request, systemPrompt: ... })` |
| 创建 Agent | `create_agent(..., context_schema=Context)` | `createAgent({ ..., contextSchema })` |
| 调用时传上下文 | `agent.invoke({...}, context={"user_role": "expert"})` | `agent.invoke({ messages }, { context: { userRole: 'expert' } })` |

## 4. 工作原理

1. `contextSchema` 用 zod 定义 `userRole` 字段，默认值 `user`；
2. `userRolePrompt` 中间件在每次模型请求前读取 `request.runtime.context.userRole`：
   `expert` → 详细技术答复；`beginner` → 简单解释、避免行话；其他 → 基础提示词；
3. Demo 用同一个问题分别以 `expert` 和 `beginner` 角色调用，
   观察同一 Agent 在不同 context 下回答风格的变化。

---

[← Demo 8：动态模型 Agent](./demo8-dynamic-model) · [返回系列总览](./) · [Demo 10：结构化输出 →](./demo10-structured-output)
