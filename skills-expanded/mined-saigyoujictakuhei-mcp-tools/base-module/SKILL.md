---
name: Base Module
description: MCP Server 基础架构模块，提供工具注册装饰器、LRU 缓存机制和自动 Schema 推断
---

# Base 模块操作手册

## 功能概览
Base 模块是 KazeMiMiRin MCP Server 的基础设施层，提供：
- **@tool 装饰器**：将普通 Python 函数注册为 MCP 工具
- **ToolRegistry**：单例工具注册表，集中管理所有工具元数据
- **@cache 装饰器**：LRU 缓存机制（TTL + 最大容量限制）
- **自动 Schema 推断**：从函数签名自动生成 JSON Schema

## 使用方式

### 注册 MCP 工具
```python
from Lib.base.scripts.base import tool

@tool(
    name="my_tool",
    description="我的工具描述",
    schema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "参数1"},
            "param2": {"type": "integer", "description": "参数2"}
        },
        "required": ["param1"]
    }
)
def my_tool(param1: str, param2: int = 10):
    return f"结果: {param1}, {param2}"
```

### 使用缓存装饰器
```python
from Lib.base.scripts.base import cache

@cache(ttl=3600, max_size=5000)
def expensive_function(data):
    # 耗时操作
    return result
```

### 工具注册表操作
```python
from Lib.base.scripts.base import ToolRegistry

# 获取所有注册工具
all_tools = ToolRegistry.get_all()

# 获取特定工具
tool_def = ToolRegistry.get("tool_name")
```

## 缓存机制
- **TTL**: 默认 3600 秒（1 小时）
- **最大容量**: 默认 500 条
- **淘汰策略**: LRU（淘汰最久未使用的条目）
- **缓存键**: 函数名 + JSON 序列化的参数

## 自动 Schema 推断
- 支持类型：int, float, str, bool, list, dict
- 自动识别必填参数（无默认值的参数）
- 跳过 self/cls 参数

## 模块依赖
- 标准库：`inspect`, `json`, `time`, `collections.OrderedDict`, `dataclasses`
- 无外部依赖

## 注意事项
1. @tool 装饰器必须在函数定义时立即使用
2. 缓存键使用 JSON 序列化，确保可变对象的稳定性
3. ToolRegistry 是单例类，所有模块共享同一注册表
4. clear_cache() 会清除所有缓存条目
