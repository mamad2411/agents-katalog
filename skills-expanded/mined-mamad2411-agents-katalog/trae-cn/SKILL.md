---
name: trae-cn
description: Trae CN AI IDE integration. Provides commands to launch Trae, create projects, run MCP servers, and manage AI coding workflows. Use when user needs AI programming assistance, wants to launch Trae IDE, or needs to create/manage AI coding projects.
---

# Trae CN AI IDE 集成

Trae 是字节跳动推出的 AI 原生集成开发环境（AI IDE），与 AI 深度集成，提供智能问答、代码自动补全以及基于 Agent 的 AI 自动编程能力。

## 快速开始

### 启动 Trae IDE

```bash
# 使用 Homebrew 启动
brew services start trae-cn

# 或者直接启动应用
open -a "Trae"
```

### Trae SOLO 模式

Trae 的 SOLO 模式能够理解开发者需求，自动执行编程任务：

```bash
# 进入项目目录后启动 Solo 模式
cd your-project
trae solo --task "帮我优化这个函数的性能"
```

## 主要功能

### 1. AI 编程助手

- **智能问答**: 直接在 IDE 中询问 AI
- **代码生成**: 描述需求，自动生成代码
- **代码解释**: 选中代码，AI 解释逻辑
- **单元测试**: 自动生成测试用例
- **智能修复**: AI 自动修复 bug

### 2. MCP 集成 (Model Context Protocol)

MCP 是一种让 AI 工具能够理解和访问外部知识库或服务的协议。

#### 配置 MCP Server

在 Trae 中配置 MCP：

1. 打开 Trae IDE
2. 进入设置 → MCP
3. 添加 MCP Server 配置

#### 内置 MCP Server

Trae 内置了常用 MCP Server：

- **文件系统**: 文件读写操作
- **数据库**: 数据库查询
- **API 调用**: HTTP 请求
- **网页自动化**: Playwright 集成

#### 自定义 MCP Server

```bash
# 安装 MCP Server
npm install -g @modelcontextprotocol/server-filesystem

# 配置到 Trae
trae config add-mcp @modelcontextprotocol/server-filesystem
```

### 3. Agent 模式

使用 Agent 模式让 AI 自动完成复杂任务：

```bash
# 启动 Agent
trae agent --task "创建一个 React 组件，包含表单验证功能"

# 带上下文
trae agent --task "分析这个项目的架构" --context ./project
```

## 常用命令

### 项目管理

```bash
# 创建新项目
trae create --template react my-project

# 打开项目
trae open ./my-project

# 克隆并打开项目
trae clone https://github.com/user/repo.git
```

### 代码操作

```bash
# 代码生成
trae generate --prompt "创建一个用户登录组件"

# 代码重构
trae refactor --file ./src/App.tsx --task "将类组件改为函数组件"

# 代码审查
trae review --file ./src/utils.ts
```

### AI 对话

```bash
# 启动对话
trae chat

# 带系统提示
trae chat --system "你是一个 Python 专家"

# 引用代码对话
trae chat --file ./script.py "解释这段代码"
```

### MCP 操作

```bash
# 列出已配置的 MCP Server
trae mcp list

# 添加 MCP Server
trae mcp add filesystem -- npx @modelcontextprotocol/server-filesystem ./projects

# 移除 MCP Server
trae mcp remove filesystem
```

## 与 OpenClaw 集成

### 使用 Trae MCP Server

在 OpenClaw 中可以通过 MCP 协议调用 Trae：

```python
# Python 示例：使用 Trae MCP Server
import requests

# 调用 Trae MCP 文件系统操作
response = requests.post(
    "http://localhost:3000/mcp/file",
    json={
        "action": "read",
        "path": "./src/App.tsx"
    }
)
```

### OpenClaw Trae Skill

使用 OpenClaw 的 trae-cn Skill：

```bash
# 在 OpenClaw 中使用
@trae-cn help

# 创建项目
@trae-cn create-project --name my-app --template react

# 运行代码生成
@trae-cn generate --prompt "创建一个登录表单"
```

## 配置选项

### 环境变量

```bash
# API Key 配置
export TRAE_API_KEY="your-api-key"

# 模型选择
export TRAE_MODEL="deepseek-v3"  # 默认
# 或 claude-sonnet, gpt-4

# MCP Server 默认路径
export TRAE_MCP_PATH="./mcp-servers"
```

### 配置文件

Trae 配置文件位于 `~/.trae/config.json`:

```json
{
  "model": {
    "provider": "deepseek",
    "model": "deepseek-v3",
    "temperature": 0.7
  },
  "mcp": {
    "enabled": true,
    "servers": ["filesystem", "database"]
  },
  "theme": "dark",
  "shortcuts": {
    "chat": "cmd+shift+l",
    "generate": "cmd+shift+g"
  }
}
```

## 使用场景

### 场景 1：快速原型开发

```bash
# 1. 创建项目
trae create --template nextjs my-saas

# 2. 进入项目
cd my-saas

# 3. 启动开发
trae dev

# 4. AI 生成代码
trae generate --prompt "创建一个用户仪表盘页面"
```

### 场景 2：代码审查与优化

```bash
# 1. 打开项目
trae open ./my-project

# 2. AI 审查代码
trae review --file ./src/critical.ts

# 3. AI 优化
trae refactor --file ./src/critical.ts --task "性能优化"
```

### 场景 3：集成外部工具

```bash
# 1. 配置 MCP Server
trae mcp add weather -- npx @modelcontextprotocol/server-weather

# 2. 在对话中使用
trae chat "北京今天天气怎么样？"
```

### 场景 4：团队协作

```bash
# 1. 克隆项目
trae clone https://github.com/team/project.git

# 2. 设置上下文
trae context set ./project-docs

# 3. AI 理解项目
trae chat "根据项目文档，帮我生成 API 文档"
```

## 常见问题

**Q: Trae 和 VS Code 有什么区别？**
A: Trae 是原生 AI IDE，与 AI 深度集成，支持 Agent 模式和 MCP 协议，比 VS Code 有更强的 AI 能力。

**Q: Trae 支持哪些编程语言？**
A: 支持所有主流语言，包括 Python、JavaScript/TypeScript、Go、Rust、Java、C++ 等。

**Q: 如何配置自定义 MCP Server？**
A: 参考官方文档：https://docs.trae.com.cn/ide/model-context-protocol

**Q: Trae 免费吗？**
A: Trae 提供免费版和专业版，免费版包含基础 AI 功能，专业版提供更多高级功能。

**Q: 如何切换 AI 模型？**
A: 在设置中配置或使用环境变量 `TRAE_MODEL`

## 参考链接

- 官网: https://www.trae.com.cn
- 文档: https://docs.trae.com.cn
- GitHub: https://github.com/trae-ai
- 下载: https://www.trae.com.cn/download
