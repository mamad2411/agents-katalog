---
name: agent-engine
description: 长运行自主编码 Agent 引擎。用于指导项目的自动化开发，实现多会话跨上下文窗口的持续开发。实现两阶段 Agent 架构：Initializer Agent（初始化环境）和 Coding Agent（增量开发）。当用户需要构建复杂的、需要多会话完成的项目时，当用户提到需要自主编码、长运行 agent、多会话开发、增量开发时，必须使用此 skill。此 skill 提供完整的工作流程，包括环境初始化、功能列表管理、增量进度追踪、Git 提交规范和端到端测试。
---

# Agent Engine

长运行自主编码 Agent 引擎，用于指导项目的自动化开发。

## 核心理念

长运行 Agent 的核心挑战是：它们必须以离散会话工作，每个新会话开始时没有之前的记忆。由于上下文窗口有限，且大多数复杂项目无法在单个窗口内完成，Agent 需要一种方式来弥合编码会话之间的差距。

**解决方案：两阶段 Agent 架构**

1. **Initializer Agent**（初始化 Agent）：第一个会话使用专门的 prompt 设置初始环境
2. **Coding Agent**（编码 Agent）：每个后续会话被要求做增量进度，同时为下一个会话留下清晰的产物

可以参考 reference 文件夹中的示例 prompt 和产物：
- [initializer-prompt.md](./references/initializer-prompt.md)：Initializer Agent 的示例 prompt
- [agent-progress.md](./references/agent-progress.md)：增量开发过程中的进度日志示例
- [feature_list.json](./references/feature_list.json)：功能列表的示例
- [init.sh](./references/init.sh)：开发服务器启动脚本示例
- [coding-agent-prompt.md](./references/coding-agent-prompt.md)：Coding Agent 的示例 prompt

## 触发场景

当用户有以下需求时，必须使用此 skill：

- 需要构建复杂的、多会话完成的项目
- 需要实现长运行自主编码
- 需要增量开发工作流
- 需要多会话跨上下文窗口的持续开发
- 需要功能级别的进度追踪
- 需要端到端自动化测试
- 用户明确提及需要使用这个 skill

## 核心组件

### 1. init.sh - 开发服务器启动脚本

初始化 Agent 应该创建一个 `init.sh` 脚本，用于启动开发服务器：

```bash
#!/bin/bash
# 启动开发服务器
cd /path/to/project
npm install
npm run dev
```

或者是 Python 项目：

```bash
#!/bin/bash
# 启动开发服务器
cd /path/to/project
source venv/bin/activate # 或者使用 uv/conda 等
pip install -r requirements.txt
python app.py
```

具体可见 [init.sh](./references/init.sh) 示例。

### 2. agent-progress.md - 进度日志

记录每个会话完成的工作：

```
## Session History

### Session 1 (2025-01-15)
- Initialized project structure
- Set up feature list with 50 features
- Created init.sh script
- Basic project scaffold complete

### Session 2 (2025-01-16)
- Implemented user authentication
- Added login/logout functionality
- Created user dashboard page
- Fixed session persistence bug

### Session 3 (2025-01-17)
- Started work on messaging feature
- ...
```

具体可见 [agent-progress.md](./references/agent-progress.md) 示例。

### 3. feature_list.json - 功能列表

这是最关键的组件。初始化 Agent 应该创建一个结构化的 JSON 文件，列出所有需要实现的功能：

```json
{
  "features": [
    {
      "id": "1",
      "category": "functional",
      "description": "User can open a new chat, type in a query, press enter, and see an AI response",
      "steps": [
        "Navigate to main interface",
        "Click the 'New Chat' button",
        "Verify a new conversation is created",
        "Check that chat area shows welcome state",
        "Verify conversation appears in sidebar"
      ],
      "passes": false,
      "priority": "high"
    },
    {
      "id": "2", 
      "category": "functional",
      "description": "Theme toggle switches between light and dark mode",
      "steps": [
        "Click theme toggle button",
        "Verify CSS variables change",
        "Verify persistence across page reload"
      ],
      "passes": false,
      "priority": "medium"
    }
  ]
}
```

**重要规则**：
- 所有功能初始标记为 `"passes": false`
- Coding Agent 只能通过更改 `passes` 字段来更新状态
- 禁止删除或编辑测试，因为这可能导致功能缺失或 bug
- 使用 JSON 格式，因为模型不太可能不当更改 JSON 文件

具体可见 [feature_list.json](./references/feature_list.json) 示例。

## 工作流程

### 阶段 1：初始化（Initializer Agent）

第一个会话执行以下任务：

1. **分析需求**：理解用户的初始 prompt，扩展为完整的功能列表
2. **创建 feature_list.json**：
   - 将需求分解为具体的、可测试的功能
   - 每个功能包含步骤说明
   - 所有功能初始标记为 failing
3. **创建 init.sh**：
   - 安装依赖的命令
   - 启动开发服务器的命令
4. **创建 agent-progress.md**：
   - 记录初始化进度
5. **初始化 Git 仓库**：
   - 创建初始 commit
   - 显示添加了哪些文件
6. **验证环境**：
   - 运行 init.sh 启动服务器
   - 验证基本功能工作

具体步骤可见 [initializer-prompt.md](./references/initializer-prompt.md) 示例。

### 阶段 2：增量开发（Coding Agent）

每个后续会话遵循以下流程：

#### 开始时：获取 bearings

```
[Assistant] I'll start by getting my bearings and understanding the current state of the project.
[Tool Use] <bash - pwd>
[Tool Use] <read - agent-progress.md>
[Tool Use] <read - feature_list.json>
[Assistant] Let me check the git log to see recent work.
[Tool Use] <bash - git log --oneline -20>
[Assistant] Now let me check if there's an init.sh script to restart the servers.
<Starts the development server>
[Assistant] Excellent! Now let me navigate to the application and verify that some fundamental features are still working.
<Tests basic functionality>
```

具体步骤：

1. **运行 `pwd`**：确认工作目录
2. **读取 git logs 和 progress 文件**：了解最近的工作
3. **读取 feature list**：选择最高优先级的未完成功能
4. **启动开发服务器**：运行 `init.sh`
5. **基本功能验证测试**：确保应用没有被破坏
6. **选择一个功能开始工作**

#### 工作中：增量实现

1. **选择一个功能**：
   - 选择最高优先级且未通过的功能
   - 不要尝试一次实现多个功能

2. **实现功能**：
   - 按照 feature 中的步骤实现
   - 编写必要的代码

3. **端到端测试**：
   - 使用 Puppeteer MCP 或 Playwright 进行浏览器自动化测试
   - 模拟用户操作验证功能
   - 记录测试截图

4. **更新 feature 状态**：
   - 测试通过后，将 `passes` 改为 `true`
   - 记录测试结果

#### 结束时：留下干净的产物

1. **运行完整测试**：确保没有破坏现有功能
2. **更新 agent-progress.md**：
   ```
   ### Session N (YYYY-MM-DD)
   - Completed feature: [feature description]
   - Fixed bugs: [list of fixes]
   - Tests added: [test descriptions]
   ```
3. **Git 提交**：
   ```bash
   git add -A
   git commit -m "feat: implement [feature name]
   
   - Added [specific changes]
   - Fixed [bugs fixed]
   - Tests: [test results]"
   ```
4. **确保代码整洁**：
   - 没有 major bugs
   - 代码有序且有文档
   - 可以轻松开始新功能

## 常见失败模式及解决方案

| 问题 | 解决方案 |
|------|---------|
| Agent 过早宣布项目完成 | 设置 feature list 文件，每次只做一个功能 |
| Agent 留下有 bug 或未记录的进度 | 开始时读取 progress 和 git log，结束时写 commit 和 progress 更新 |
| Agent 过早标记功能为完成 | 自我验证所有功能，只有经过仔细测试后才标记为 passing |
| Agent 花时间弄清楚如何运行应用 | 创建 init.sh 脚本，会话开始时读取并运行 |

## 测试最佳实践

### 使用浏览器自动化

使用 Puppeteer MCP 或 Playwright 进行端到端测试：

1. **启动应用**：导航到本地开发服务器
2. **模拟用户操作**：
   - 点击按钮
   - 填写表单
   - 提交数据
3. **验证结果**：
   - 检查页面内容
   - 验证状态变化
   - 截图记录

### 测试优先级

1. **基本功能测试**：每次会话开始时运行
2. **新功能测试**：实现后立即测试
3. **回归测试**：确保没有破坏现有功能

## 输出格式

### 功能列表更新

```json
{
  "id": "feature-id",
  "description": "功能描述",
  "passes": true,
  "test_results": {
    "screenshot": "path/to/screenshot.png",
    "notes": "测试备注"
  }
}
```

### Progress 更新

``` Session N (YYYYmarkdown
###-MM-DD)
**Completed:**
- Feature: [name]
- Tests: [results]

**In Progress:**
- Feature: [name]

**Next:**
- Feature: [name]
```

## Git 提交规范

使用清晰的提交信息：

```
feat: add user authentication

- Implement login/logout functionality  
- Add session persistence
- Create user dashboard

Tests: All passing
```

## 进阶主题

### 多 Agent 架构

未来方向可能包括专门的 Agent：
- **Testing Agent**：专门负责测试
- **QA Agent**：专门负责质量保证
- **Code Cleanup Agent**：专门负责代码清理

### 跨领域泛化

这些实践可以应用于：
- 科学研究
- 金融建模
- 数据分析
- 其他长运行 Agent 任务

## 参考

- Anthropic 官方文章：[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Claude Quickstarts: [Autonomous Coding](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
- Claude Agent SDK: [Quickstart](https://platform.claude.com/docs/en/agent-sdk/quickstart)
