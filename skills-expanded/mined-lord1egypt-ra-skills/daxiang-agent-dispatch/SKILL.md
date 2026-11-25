# Agent Dispatch Skill

**版本**: v1.0
**创建日期**: 2026-03-26
**作?*: 象腿 (main agent)
**用?*: 根据routing规则自动调度specialist agents

---

## 🎯 核心功能

Agent Dispatch是main agent的核心协调skill，负责：
1. **意图识别**: 分析用户请求，提取关键特?2. **路由匹配**: 根据routing规则选择最合适的agent
3. **任务调度**: 使用sessions_spawn调度specialist agent
4. **结果整合**: 合并agent执行结果，形成连贯回?5. **容错处理**: 失败时自动重试或fallback到main

---

## 📋 Routing规则

### 规则优先?
```yaml
routing:
  # P1: 编程和技术实?  - pattern: "(代码|编程|debug|开发|API|技术实现|github|pr|git|仓库|分支)"
    target: "coder"
    priority: 1
    description: "编程、代码调试、API开发、GitHub操作"

  # P2: 深度研究和知识提?  - pattern: "(搜索|研究|文档|资料|深度分析|知识提取|学习|调研|总结)"
    target: "danao"
    priority: 2
    description: "深度思考、知识提取、研究分?

  # P3: 内容创作
  - pattern: "(写作|翻译|文案|内容创作|公众号|视频脚本|小红书|抖音|文章|博客)"
    target: "writer"
    priority: 3
    description: "文案写作、内容创作、多平台内容"

  # P4: 架构和设?  - pattern: "(创意|产品设计|方案设计|架构设计|系统设计|技术方?"
    target: "engineer"
    priority: 4
    description: "系统架构、技术方案、产品设?

  # P5: 日常协作和管?  - pattern: "(飞书|文档|日程|任务管理|日常协作|提醒|会议)"
    target: "manager"
    priority: 5
    description: "飞书协作、日程管理、任务提?

  # P99: 默认fallback
  - pattern: ".*"
    target: "self"
    priority: 99
    description: "main agent自己处理"
```

### 路由匹配逻辑

1. **优先级匹?*: 按priority顺序从低到高匹配
2. **正则表达?*: pattern使用正则表达式匹配用户输?3. **首次命中**: 匹配到第一个rule即停止，返回target
4. **默认兜底**: 如果都不匹配，fallback?self"

---

## 🔄 调度流程

### 步骤1: 意图识别

```python
def identify_intent(user_input):
    """
    识别用户意图，提取关键特?
    Returns:
        dict: {
            "keywords": ["关键?", "关键?"],
            "task_type": "coding|research|writing|design|management|general",
            "complexity": "simple|medium|complex",
            "requires_parallel": false
        }
    """
    # 关键词提?    keywords = extract_keywords(user_input)

    # 任务类型判断
    task_type = classify_task(user_input)

    # 复杂度评?    complexity = assess_complexity(user_input)

    # 是否需要并行处?    requires_parallel = check_parallel_requirements(user_input)

    return {
        "keywords": keywords,
        "task_type": task_type,
        "complexity": complexity,
        "requires_parallel": requires_parallel
    }
```

### 步骤2: 路由匹配

```python
def match_route(intent):
    """
    根据intent匹配routing规则

    Returns:
        dict: {
            "target": "coder|danao|writer|engineer|manager|self",
            "priority": 1-99,
            "confidence": 0.0-1.0
        }
    """
    for rule in routing_rules:
        pattern = rule["pattern"]
        if re.search(pattern, intent["user_input"]):
            return {
                "target": rule["target"],
                "priority": rule["priority"],
                "confidence": calculate_confidence(intent, rule)
            }

    # 默认fallback到self
    return {"target": "self", "priority": 99, "confidence": 0.5}
```

### 步骤3: 任务调度

```python
def dispatch_task(route, intent, user_input):
    """
    调度任务到目标agent

    Args:
        route: 路由结果
        intent: 意图识别结果
        user_input: 用户原始输入

    Returns:
        dict: {
            "success": true/false,
            "result": "agent执行结果",
            "metadata": {
                "agent": "coder",
                "execution_time": 123.45,
                "retry_count": 0
            }
        }
    """
    target = route["target"]

    # 如果是self，直接处?    if target == "self":
        return handle_self(user_input)

    # 调度到specialist agent
    return spawn_agent(target, user_input, intent)
```

### 步骤4: 结果整合

```python
def integrate_results(dispatch_result):
    """
    整合agent执行结果

    Returns:
        str: 格式化的用户回复
    """
    if not dispatch_result["success"]:
        return handle_failure(dispatch_result)

    result = dispatch_result["result"]
    metadata = dispatch_result["metadata"]

    # 透明化：告知用户哪个agent处理?    agent_name = metadata["agent"]
    execution_time = metadata["execution_time"]

    response = f"【{agent_name}】已处理完成（耗时{execution_time:.2f}秒）\n\n"
    response += result

    return response
```

### 步骤5: 容错处理

```python
def handle_failure(dispatch_result, retry_count=0):
    """
    处理agent执行失败

    Args:
        dispatch_result: 失败的调度结?        retry_count: 当前重试次数

    Returns:
        str: 错误处理结果
    """
    MAX_RETRY = 3

    if retry_count < MAX_RETRY:
        # 自动重试
        log(f"Agent执行失败，正在重?({retry_count + 1}/{MAX_RETRY})")
        return dispatch_task(dispatch_result["route"], retry_count + 1)

    # 超过最大重试次数，fallback到self
    log(f"Agent执行失败，fallback到main agent")
    return handle_self(dispatch_result["user_input"])
```

---

## 🛠?实现细节

### sessions_spawn参数配置

```yaml
# Coder Agent
coder:
  runtime: "acp"
  agentId: "codex"
  mode: "run"
  timeout: 300

# Danao Agent
danao:
  runtime: "subagent"
  agentId: "danao"
  mode: "session"
  timeout: 600

# Writer Agent
writer:
  runtime: "subagent"
  agentId: "writer"
  mode: "session"
  timeout: 600

# Engineer Agent
engineer:
  runtime: "subagent"
  agentId: "engineer"
  mode: "session"
  timeout: 600

# Manager Agent
manager:
  runtime: "subagent"
  agentId: "manager"
  mode: "session"
  timeout: 300
```

### 并行任务处理

```python
def parallel_dispatch(tasks):
    """
    并行调度多个独立任务

    Args:
        tasks: [
            {"route": route1, "intent": intent1, "user_input": input1},
            {"route": route2, "intent": intent2, "user_input": input2}
        ]

    Returns:
        list: [result1, result2]
    """
    MAX_PARALLEL = 2

    # 限制并行数量
    tasks = tasks[:MAX_PARALLEL]

    # 并行执行
    results = []
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as executor:
        futures = [
            executor.submit(dispatch_task, task["route"], task["intent"], task["user_input"])
            for task in tasks
        ]

        for future in as_completed(futures):
            results.append(future.result())

    return results
```

---

## 📊 性能监控

### 关键指标

```yaml
metrics:
  - name: "dispatch_success_rate"
    description: "调度成功?
    target: "> 95%"

  - name: "avg_dispatch_time"
    description: "平均调度耗时"
    target: "< 5s"

  - name: "retry_rate"
    description: "重试?
    target: "< 10%"

  - name: "fallback_rate"
    description: "fallback到self的比?
    target: "< 5%"

  - name: "parallel_speedup"
    description: "并行加速比"
    target: "> 1.3x"
```

### 日志记录

```python
def log_dispatch(route, intent, result):
    """
    记录调度日志

    Format:
    [2026-03-26 12:00:00] [DISPATCH] target=coder, priority=1, confidence=0.95, success=true, time=3.45s
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "DISPATCH",
        "target": route["target"],
        "priority": route["priority"],
        "confidence": route["confidence"],
        "success": result["success"],
        "execution_time": result["metadata"]["execution_time"],
        "retry_count": result["metadata"]["retry_count"]
    }

    write_log(log_entry)
```

---

## 🎓 使用示例

### 示例1: 编程任务

```python
# 用户输入
user_input = "帮我debug这段代码，报错了"

# 意图识别
intent = identify_intent(user_input)
# => {"task_type": "coding", "complexity": "medium"}

# 路由匹配
route = match_route(intent)
# => {"target": "coder", "priority": 1, "confidence": 0.95}

# 任务调度
result = dispatch_task(route, intent, user_input)

# 结果整合
response = integrate_results(result)
# => "【Coder】已处理完成（耗时3.45秒）\n\n代码问题已修?.."
```

### 示例2: 内容创作

```python
# 用户输入
user_input = "写一篇关于AI工具推荐的小红书文案"

# 意图识别
intent = identify_intent(user_input)
# => {"task_type": "writing", "complexity": "medium"}

# 路由匹配
route = match_route(intent)
# => {"target": "writer", "priority": 3, "confidence": 0.92}

# 任务调度
result = dispatch_task(route, intent, user_input)

# 结果整合
response = integrate_results(result)
# => "【Writer】已处理完成（耗时15.23秒）\n\n小红书文案已生成..."
```

### 示例3: 并行任务

```python
# 用户输入
user_input1 = "查询今天的AI新闻"
user_input2 = "检查Gateway状?

# 意图识别
intent1 = identify_intent(user_input1)
intent2 = identify_intent(user_input2)

# 路由匹配
route1 = match_route(intent1)  # => {"target": "danao", ...}
route2 = match_route(intent2)  # => {"target": "manager", ...}

# 并行调度
tasks = [
    {"route": route1, "intent": intent1, "user_input": user_input1},
    {"route": route2, "intent": intent2, "user_input": user_input2}
]
results = parallel_dispatch(tasks)

# 结果整合
response = integrate_parallel_results(results)
# => "【Danao】AI新闻已查询（耗时2.15秒）\n【Manager】Gateway状态正常（耗时1.23秒）"
```

---

## ⚙️ 配置文件

### agent-dispatch-config.json

```json
{
  "version": "1.0",
  "routing": [
    {
      "pattern": "(代码|编程|debug|开发|API|技术实现|github|pr|git|仓库|分支)",
      "target": "coder",
      "priority": 1,
      "description": "编程、代码调试、API开发、GitHub操作",
      "enabled": true
    },
    {
      "pattern": "(搜索|研究|文档|资料|深度分析|知识提取|学习|调研|总结)",
      "target": "danao",
      "priority": 2,
      "description": "深度思考、知识提取、研究分?,
      "enabled": true
    },
    {
      "pattern": "(写作|翻译|文案|内容创作|公众号|视频脚本|小红书|抖音|文章|博客)",
      "target": "writer",
      "priority": 3,
      "description": "文案写作、内容创作、多平台内容",
      "enabled": true
    },
    {
      "pattern": "(创意|产品设计|方案设计|架构设计|系统设计|技术方?",
      "target": "engineer",
      "priority": 4,
      "description": "系统架构、技术方案、产品设?,
      "enabled": true
    },
    {
      "pattern": "(飞书|文档|日程|任务管理|日常协作|提醒|会议)",
      "target": "manager",
      "priority": 5,
      "description": "飞书协作、日程管理、任务提?,
      "enabled": true
    },
    {
      "pattern": ".*",
      "target": "self",
      "priority": 99,
      "description": "main agent自己处理",
      "enabled": true
    }
  ],
  "config": {
    "max_parallel_tasks": 2,
    "task_timeout": 300,
    "retry_attempts": 3,
    "fallback_to_self": true,
    "enable_logging": true
  },
  "agents": {
    "coder": {
      "runtime": "acp",
      "agentId": "codex",
      "mode": "run",
      "timeout": 300
    },
    "danao": {
      "runtime": "subagent",
      "agentId": "danao",
      "mode": "session",
      "timeout": 600
    },
    "writer": {
      "runtime": "subagent",
      "agentId": "writer",
      "mode": "session",
      "timeout": 600
    },
    "engineer": {
      "runtime": "subagent",
      "agentId": "engineer",
      "mode": "session",
      "timeout": 600
    },
    "manager": {
      "runtime": "subagent",
      "agentId": "manager",
      "mode": "session",
      "timeout": 300
    }
  }
}
```

---

## 🚀 未来优化

### 短期 (1-2?
- [ ] 添加机器学习模型提升意图识别准确?- [ ] 实现动态routing规则（基于历史数据优化）
- [ ] 添加agent性能评分，自动选择最优agent

### 中期 (1个月)
- [ ] 实现agent负载均衡
- [ ] 添加任务队列管理
- [ ] 实现跨agent知识共享

### 长期 (3个月)
- [ ] 引入强化学习优化routing策略
- [ ] 实现自适应并行度调?- [ ] 构建agent性能预测模型

---

*Skill版本: v1.0*
*最后更? 2026-03-26*
*维护? 象腿 (main agent)*
