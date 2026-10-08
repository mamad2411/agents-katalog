# P17 New-AI 任务 — 连续指令上下文 + Skill 优先调用深度分析

> 分支: `feature/p17-context-and-skill`  
> 基于当前 HEAD

你负责 2 个需要深度分析和修复的任务。

---

## N1: 连续指令上下文断裂分析与修复

### 问题

截图6显示用户连续发出两条指令：
1. "@research_agent 分析视频的评论和弹幕吧"（01:54）
2. "@research_agent 分析视频的评论和弹幕吧"（01:57，重复发送）

但第二条指令无法工作——agent 没有再次调用 B站工具。

### 需要排查的问题

#### 1. 上下文传递完整性

每次 agent loop 运行都会构建完整的 prompt stack。需要确认：

- `context_compiler.py` 在构建 context 时，是否包含了**所有历史消息**，特别是上一轮 agent 的工具调用结果？
- 第二次运行的 system prompt + user messages 中，是否包含了第一次运行的搜索结果？
- 如果第一次运行使用了 `bilibili_analyze_video` 工具并返回了结果，第二次运行的 messages 列表中是否能看到这些结果？

排查路径：
```
context_compiler.py → compile() → _conversation_section() → 检查历史消息是否完整
prompt_stack.py → build_agent_loop_prompt_stack() → 检查 messages 组装
agent_loop.py → run() → 检查传入的 system_prompt + user_prompt 是否完整
```

#### 2. 工具可用性问题

当用户第二次发送相同指令时，可能因为以下原因导致工具不可用：

a. **`bilibili_analyze_video` 工具是否在第二次运行中可用？**
   - 检查 `tool_definitions.py` 中 `get_agent_tools()` 的逻辑
   - `bilibili_analyze_video` 需要 `bvid` 参数，第二次运行的 LLM 是否知道之前获取的 bvid？

b. **工具列表是否根据 agent 类型筛选？**
   - 如果 RESEARCH agent 运行使用的工具列表不包含 `bilibili_analyze_video`，就无法调用
   - 检查 `skill_registry.py` 和 `runtime.py` 中工具分配逻辑

c. **Phase machine 是否切换了阶段导致工具集变化？**

#### 3. Agent Loop 的消息历史构建

检查 `runtime.py` 中 `_execute_existing_run()` 方法：
- 它如何构建 `messages` 列表？
- 是否包含前一次 run 的工具调用结果？
- 是否有消息窗口截断导致第一次运行的关键上下文丢失？

相关代码路径：
```
runtime.py → _execute_existing_run() → 获取 messages
           → agent_runtime_kernel.prepare_turn() → 构建 messages
           → context_compiler.compile() → 构建上下文
           → prompt_stack.build_agent_loop_prompt_stack() → 构建最终 prompt
           → agent_loop.run() → 执行
```

#### 4. 关键信息：前一轮 tool 结果在消息中的表示

Agent Loop 执行工具后，工具结果以什么形式存储在 messages 中？

检查：
- `agent_loop.py` 工具调用后如何将结果追加到 messages
- 这些 messages 是否由 `store.save_message()` 持久化
- 还是仅在单次 run 的 agent_loop 内部存在，run 结束后丢失

如果工具结果**只在单次 run 内部存在**，则第二次 run 看不到第一次的工具结果——这就是根因。

#### 5. 可能的解决方案

如果确认是上下文丢失：

**方案 A**: 在 run 完成后，将关键工具调用结果摘要保存为 assistant message 的一部分
- `agent_loop.py` → `AgentLoopResult.content` 已经包含最终回答
- 但中间的工具调用输入/输出可能没有被保存
- 需要在 `runtime.py` 的 run 完成后，将 skill_calls 的摘要附加到 output message

**方案 B**: 在第二次 run 的 context 中注入前一次 run 的工具调用摘要
- `context_compiler.py` 可以从 `run.skill_calls` 或 `run.trace_events` 中提取工具调用记录
- 在 system prompt 或 user context 中添加 "上一轮工具调用结果" 部分

**方案 C**: 利用 RuntimeMemory 或 RuntimeEvidence 保存中间研究结果
- 检查 `runtime_evidence.py` 和 `runtime_memory.py` 是否已经做了这个

---

## N2: Skill 请求优先调用机制

### 问题

截图2和4显示：
- 用户在输入框中附加了 Skill 请求（如 "B站搜索 搜索词:逗比的雀巢"）
- 发送后 agent 开始处理，但不一定优先调用用户请求的 Skill

截图4更明显：
- 用户明确发送了 "Skill: B站搜索" + "@research_agent 你能直接通过BV1G3411h7Te 这个BV号..."
- 但系统显示 "执行了 2 个操作" → "先顺手补齐商业目标..." + "本轮继续由 research_agent 执行"
- 没有看到 B站搜索被优先执行

### 需要排查

#### 1. Skill 请求的后端处理流程

```
前端: skillRequests = [{ skillId: "bilibili_search", args: { query: "逗比的雀巢" } }]
      ↓
POST /api/projects/:id/mentions（payload 包含 skillRequests）
      ↓
runtime.py → run() → 接收 skill_requests
      ↓
runtime.py → _start_run() → 如何处理 skill_requests？
      ↓
agent_runtime_kernel.py → prepare_turn() → skill_requests 传递到哪里？
      ↓
agent_loop.py → run() → LLM 是否知道需要优先调用这个 skill？
```

#### 2. 检查 skill_requests 在 runtime 中的处理

文件: `runtime.py`

搜索 `skill_requests` 关键词，确认：
- `_start_run()` 或 `_execute_existing_run()` 中是否实际执行了 skill_requests
- 还是只是将它们作为参数传递，期望 LLM 自己决定是否调用

#### 3. 检查 skill_runner.py 中的预执行逻辑

搜索 `skill_runner.py` 中是否有 "预执行 skill" 的逻辑（在 agent loop 之前先执行用户请求的 skills，然后将结果注入上下文）。

### 可能的修复方案

#### 方案 A（推荐）: Agent Loop 入口强制首轮执行 Skill

在 `agent_loop.py` 的 `_run_internal()` 方法中，在正式循环开始前：

1. 检查是否有 `skill_requests`
2. 如果有，在第一轮直接执行这些 skills
3. 将结果注入到 messages 中
4. 然后正常进入 LLM 循环

```python
def _run_internal(self, *, skill_requests=None, ...):
    # ★ 预执行用户请求的 Skills
    if skill_requests:
        for req in skill_requests:
            tool_name = req.skill_id
            tool_args = dict(req.args)
            tool_result, skill_call, success = self._execute_tool(
                project_id=project_id,
                agent=agent,
                prompt=prompt,
                tool_name=tool_name,
                tool_args=tool_args,
                spill_cache=spill_cache,
            )
            if skill_call:
                result.skill_calls.append(skill_call)
            # 将结果加入 messages 作为上下文
            messages.append({"role": "system", "content": f"[用户请求的 {tool_name} 结果]:\n{tool_result}"})
    
    # 然后正常进入循环...
```

#### 方案 B: 增强 System Prompt

在 `prompt_stack.py` 中，如果检测到 skill_requests，添加明确指令：

```
"【必须优先处理的 Skill 请求】\n"
f"用户已在消息中请求执行以下 Skill: {skill_names}\n"
f"参数: {skill_args}\n"
"你必须在第一轮工具调用中优先执行这些请求的 Skill。"
```

#### 方案 C: 检查现有的 Skill 预执行逻辑

如果 `runtime.py` 已经有预执行逻辑但结果没有被正确注入上下文，
修复注入路径而不是重写。

### 排查路径

```bash
# 1. 查找 skill_requests 在 runtime 中的所有引用
grep -n "skill_requests" apps/api/src/brand_strategy_api/runtime.py

# 2. 查找 skill_requests 在 agent_loop 中的所有引用
grep -n "skill_requests" apps/api/src/brand_strategy_api/agent_loop.py

# 3. 查找 skill_runner 中的预执行逻辑
grep -n "pre_execute\|skill_request\|forced" apps/api/src/brand_strategy_api/skill_runner.py

# 4. 检查 agent_runtime_kernel 中的处理
grep -n "skill_requests" apps/api/src/brand_strategy_api/agent_runtime_kernel.py
```

---

## 执行顺序

1. **N2** (Skill 优先调用) — 先排查 + 修复 Skill 请求被忽略的问题
2. **N1** (连续指令) — 排查上下文断裂，可能和 N2 有交集

## 关键文件列表

后端（需要深入阅读）：
- `apps/api/src/brand_strategy_api/runtime.py` — 主运行时
- `apps/api/src/brand_strategy_api/agent_loop.py` — Agent Loop 核心
- `apps/api/src/brand_strategy_api/agent_runtime_kernel.py` — 运行时内核
- `apps/api/src/brand_strategy_api/context_compiler.py` — 上下文编译
- `apps/api/src/brand_strategy_api/prompt_stack.py` — 提示栈构建
- `apps/api/src/brand_strategy_api/skill_runner.py` — Skill 执行器
- `apps/api/src/brand_strategy_api/tool_definitions.py` — 工具定义
- `apps/api/src/brand_strategy_api/run_guard.py` — 运行队列

前端（参考）：
- `apps/web/components/workbench-shell-client.tsx` — 前端主控
- `apps/web/components/chat-thread.tsx` — 聊天线程
