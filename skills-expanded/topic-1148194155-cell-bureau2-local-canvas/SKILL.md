---
name: local-canvas
description: 可视化 AI 工作流画布 — 通过 REST API 和 WebSocket 管理节点、连线、工作流执行和 AI 对话。
---

# Local Canvas

Local Canvas 是一个可视化 AI 工作流画布应用，支持通过拖拽节点构建 AI 工作流、管理模型/技能/知识库、执行工作流并实时查看日志。

## 快速开始

### 启动服务

```powershell
# 启动后端 + 前端
.\scripts\start.ps1

# 不自动打开浏览器
.\scripts\start.ps1 -NoBrowser

# 停止所有服务
.\scripts\stop.ps1
```

启动后：
- 前端界面: http://localhost:5173
- 后端 API: http://localhost:3001/api
- WebSocket: ws://localhost:3001/ws
- 健康检查: http://localhost:3001/api/health

### 停止服务

```powershell
.\scripts\stop.ps1
# 强制终止所有相关 node 进程
.\scripts\stop.ps1 -Force
```

## API 端点参考

所有 API 统一基路径 `http://localhost:3001/api`，请求体为 JSON，响应格式为 `{ success: boolean, data?: any, error?: string }`。
认证通过 Header `X-User-Id: 1`（单用户模式）。

### 健康检查

```
GET /api/health
→ { "status": "ok", "timestamp": "..." }
```

### Skills（技能）

```
GET /api/skills
→ 获取所有可用 Skill 列表（含已发现的 SKILL.md 技能）
```

### Models（模型）

```
GET  /api/models          → 列出所有已配置模型（含在线状态）
POST /api/models          → 添加新模型
  Body: { name, adapter_type: "openai|ollama|anthropic|builtin", config: { endpoint, apiKey, model } }
DELETE /api/models/:id    → 删除模型
```

### API 端点管理

```
GET  /api/apis            → 列出所有 API 端点
POST /api/apis            → 添加 API 端点
  Body: { name, url, method, headers?, description? }
DELETE /api/apis/:id      → 删除 API 端点
```

### 知识库

```
GET  /api/knowledge           → 列出所有知识库
POST /api/knowledge           → 创建知识库
  Body: { name, folder_path }
POST /api/knowledge/:id/index → 触发索引重建
  Body: { model_id }
DELETE /api/knowledge/:id     → 删除知识库
```

### API Keys

```
GET  /api/apikeys         → 列出已保存的 Key（不返回实际值）
POST /api/apikeys         → 保存 API Key（加密存储）
  Body: { name, api_key }
DELETE /api/apikeys/:id   → 删除 API Key
```

### 工作流

```
GET    /api/workflows       → 列出所有工作流（摘要）
GET    /api/workflows/:id   → 加载完整工作流（含 nodes/edges）
POST   /api/workflows       → 保存新工作流
  Body: { name, nodes, edges }
PUT    /api/workflows/:id   → 更新工作流
  Body: { name?, nodes?, edges? }
DELETE /api/workflows/:id   → 删除工作流
POST   /api/workflows/run   → 执行工作流
  Body: { workflow_id } 或 { nodes, edges, options? }
  Response: { execution_id }
```

### 执行状态

```
GET /api/executions/:id/status
→ { status: "running|completed|failed", logs: [...], output_files: [...] }
```

### AI 对话

```
POST /api/ai/chat
  Body: {
    message: "用户消息",
    history?: [{ role, content }],
    canvas_state?: { nodes, edges },
    model_id?: number
  }
  Response: {
    reply: "AI 回复",
    actions?: [{ type: "add_node"|"add_edge"|"update_config"|"run_workflow"|"clear_canvas", payload }]
  }
```

### 内置模型状态

```
GET /api/builtin/status
→ 本地内置模型（GGUF）的加载状态
```

## WebSocket

连接 `ws://localhost:3001/ws`

**前端 → 后端:**
```json
{ "type": "subscribe", "execution_id": "uuid-xxx" }
```

**后端 → 前端:**
```json
{ "type": "log", "data": { "level": "info|warn|error|debug", "message": "...", "timestamp": "..." } }
{ "type": "complete", "result": { ... } }
{ "type": "error", "error": "错误信息" }
```

## AI 助手操作指南

### 可以通过 API 完成的操作

| 操作 | 方式 |
|------|------|
| 创建/读取/更新/删除工作流 | `POST/GET/PUT/DELETE /api/workflows` |
| 执行工作流 | `POST /api/workflows/run` |
| 查询执行状态 | `GET /api/executions/:id/status` |
| AI 对话（含画布上下文） | `POST /api/ai/chat` |
| 管理模型 | `GET/POST/DELETE /api/models` |
| 管理 API 端点 | `GET/POST/DELETE /api/apis` |
| 管理知识库 | `GET/POST/DELETE /api/knowledge` |
| 管理 API Keys | `GET/POST/DELETE /api/apikeys` |
| 浏览可用技能 | `GET /api/skills` |
| 订阅执行日志 | WebSocket `subscribe` |

### 需要用户手动完成的操作

以下操作需通过前端 UI（http://localhost:5173）完成，AI 应指导用户操作：

- **拖拽排列节点** — 节点在画布上的位置通过 UI 拖拽调整，API 仅保存 position 数据
- **编辑节点配置** — 双击节点编辑参数（模型选择、prompt 内容等）
- **连线操作** — 在 UI 中从节点拖拽手柄到目标节点建立连接
- **文件上传/附件** — 将文件拖入画布或通过 UI 上传
- **可视化调试** — 执行过程中查看节点高亮和日志流

### 工作流节点类型

| type | 说明 |
|------|------|
| `skill` | AI 技能节点（调用已注册 skill） |
| `llm` | 大模型对话节点 |
| `input` | 用户输入节点 |
| `output` | 结果输出节点 |
| `api` | API 调用节点 |
| `knowledge` | 知识库检索节点 |
| `code` | 自定义代码节点 |
| `condition` | 条件分支节点 |

## 文件结构

```
local-canvas/
├── .codex-plugin/plugin.json   # 插件清单
├── .app.json                    # Codex App 配置
├── skills/                      # AI 可读的 SKILL.md
├── scripts/
│   ├── start.ps1                # 启动脚本
│   ├── stop.ps1                 # 停止脚本
│   ├── src/                     # 后端代码 (Express + SQLite + WebSocket)
│   ├── renderer/                # 前端代码 (React + Vite + React Flow)
│   ├── models/                  # 本地模型文件 (GGUF)
│   └── node_modules/            # 后端依赖
└── assets/                      # 资源文件
```
