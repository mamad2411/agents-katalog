---
name: AI Bridge
description: AI 多模型桥接模块，支持并发查询多个 AI 提供商（OpenAI, Claude, Gemini, Z-IMAGE, ModelScope, NVIDIA 等），返回文本、Base64 图片、或 HTML img 标签。
---

# AI Bridge 操作手册

## 功能概览

AI Bridge 模块提供统一的 AI 模型查询入口，支持：

- **聊天模型**：文本对话、代码生成、数据分析
- **生图模型**：图片生成、视频生成、异步轮询
- **多提供商**：OpenAI, Anthropic, Google, Z-IMAGE, ModelScope, NVIDIA 等
- **自动路由**：根据用户意图自动分类聊天/生图
- **并发查询**：支持同时查询多个提供商并返回最优结果

## 注册工具

| 工具名 | 功能 | 入口文件 |
|--------|------|----------|
| `list_ais_models` | 列出所有已加载的 AI 模型配置及其元数据 | scripts/list_models.py |
| `query_ais` | 统一入口，LLM 通过自然语言判断调用聊天/生图模型 | scripts/query_ais.py |

## 配置文件格式

配置文件位于 `configs/` 目录，支持两种格式：

### curl 命令格式
```
curl https://api.example.com/chat/completions \
  -H "Authorization: Bearer sk-xxx" \
  -d '{"model": "gpt-4", "messages": [...]}'
```

### Python 脚本格式
```python
base_url = "https://api.example.com/chat/completions"
api_key = "Bearer sk-xxx"
model = "gpt-4"
payload = {"messages": [...]}
```

## 元数据配置

`configs/model_metadata.json` 包含模型元数据：
- `name`: 显示名称
- `category`: 分类（language/vision/audio/unknown）
- `context_length`: 上下文长度
- `supports_streaming`: 是否支持流式输出
- `supports_function_calling`: 是否支持函数调用
- `supports_vision`: 是否支持视觉
- `supports_image`: 是否支持图片生成
- `supports_video`: 是否支持视频生成

## 异步平台支持

- **ModelScope**：异步图像生成，提交+轮询模式（最大重试 30 次）
- **NVIDIA NIM**：异步推理，支持超时控制

## 错误处理

| 错误类型 | 返回格式 |
|----------|----------|
| 配置未找到 | `{"status": "error", "message": "未检测到有效的 AI 配置"}` |
| HTTP 错误 | `{"type": "text", "content": "[name_http_error] 401 - Unauthorized"}` |
| 超时 | `{"type": "text", "content": "[name_timeout] 请求超时"}` |
| 空内容 | `{"type": "text", "content": "[name_empty] 返回空内容"}` |
| 解析失败 | `{"type": "text", "content": "[name_parse_error] ...", "mimetype": "text/plain"}` |

## 使用示例

```python
# 查询聊天模型
result = await query_ais(prompt="帮我写一段 Python 代码")

# 查询生图模型
result = await query_ais(prompt="画一只可爱的猫咪")

# 列出可用模型
models = await list_ais_models()
```

## 内部模块

| 模块 | 功能 |
|------|------|
| `scripts/config.py` | 目录探测与路径解析 |
| `scripts/metadata.py` | 元数据加载与自动同步 |
| `scripts/parser.py` | TXT 配置解析 |
| `scripts/network.py` | HTTP 请求/轮询/发送 |
| `scripts/route.py` | 配置路由分类 |
| `scripts/query_chat_ais.py` | 聊天模型内部查询 |
| `scripts/query_image_ais.py` | 生图模型内部查询 |
