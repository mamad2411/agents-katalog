---
name: mcp-builder
description: 创建高质量 MCP（模型上下文协议）服务器的指南，使 LLM 能够通过精心设计的工具与外部服务交互。在构建 MCP 服务器以集成外部 API 或服务时使用，无论是使用 Python (FastMCP) 还是 Node/TypeScript (MCP SDK)。
license: Complete terms in LICENSE.txt
---

# MCP 服务器开发指南

## 概述

要创建能够使 LLM 有效地与外部服务交互的高质量 MCP（模型上下文协议）服务器，请使用此技能。MCP 服务器提供的工具允许 LLM 访问外部服务和 API。MCP 服务器的质量取决于它能在多大程度上使 LLM 利用提供的工具完成现实世界的任务。

---

# 流程

## 🚀 高级工作流

创建高质量的 MCP 服务器涉及四个主要阶段：

### 第 1 阶段：深度研究与规划

#### 1.1 理解以代理为中心的设计原则

在深入实施之前，通过回顾以下原则来了解如何为 AI 代理设计工具：

**为工作流构建，而不仅仅是 API 端点：**
- 不要简单地包装现有的 API 端点 - 构建深思熟虑的、高影响力的工作流工具
- 合并相关操作（例如，`schedule_event` 既检查可用性又创建事件）
- 专注于能完成完整任务的工具，而不仅仅是单独的 API 调用
- 考虑代理实际上需要完成什么工作流

**针对有限的上下文进行优化：**
- 代理有受限的上下文窗口 - 让每一个 token 都有价值
- 返回高信号信息，而不是详尽的数据转储
- 提供“简洁”与“详细”的响应格式选项
- 默认使用人类可读的标识符而非技术代码（名称优于 ID）
- 将代理的上下文预算视为稀缺资源

**设计可操作的错误消息：**
- 错误消息应引导代理采用正确的使用模式
- 建议具体的后续步骤：“尝试使用 filter='active_only' 来减少结果”
- 使错误具有教育意义，而不仅仅是诊断性的
- 通过清晰的反馈帮助代理学习正确的工具使用方法

**遵循自然的任务细分：**
- 工具名称应反映人类思考任务的方式
- 使用一致的前缀对相关工具进行分组以提高可发现性
- 围绕自然工作流设计工具，而不仅仅是 API 结构

**使用评估驱动开发：**
- 尽早创建现实的评估场景
- 让代理反馈驱动工具改进
- 快速原型设计并根据实际代理表现进行迭代

#### 1.3 研究 MCP 协议文档

**获取最新的 MCP 协议文档：**

使用 WebFetch 加载：`https://modelcontextprotocol.io/llms-full.txt`

这份综合文档包含完整的 MCP 规范和指南。

#### 1.4 研究框架文档

**加载并阅读以下参考文件：**

- **MCP 最佳实践**: [📋 查看最佳实践](./reference/mcp_best_practices.md) - 所有 MCP 服务器的核心指南

**对于 Python 实现，还需加载：**
- **Python SDK 文档**: 使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python 实现指南](./reference/python_mcp_server.md) - Python 特定的最佳实践和示例

**对于 Node/TypeScript 实现，还需加载：**
- **TypeScript SDK 文档**: 使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript 实现指南](./reference/node_mcp_server.md) - Node/TypeScript 特定的最佳实践和示例

#### 1.5 详尽研究 API 文档

要集成服务，请阅读 **所有** 可用的 API 文档：
- 官方 API 参考文档
- 身份验证和授权要求
- 速率限制和分页模式
- 错误响应和状态代码
- 可用端点及其参数
- 数据模型和架构

**为了收集全面的信息，请根据需要使用网络搜索和 WebFetch 工具。**

#### 1.6 创建全面的实施计划

根据您的研究，创建一个详细计划，其中包括：

**工具选择：**
- 列出要实施的最有价值的端点/操作
- 优先考虑能够实现最常见和最重要用例的工具
- 考虑哪些工具协同工作以实现复杂的工作流

**共享实用程序和助手：**
- 识别常见的 API 请求模式
- 规划分页助手
- 设计过滤和格式化实用程序
- 规划错误处理策略

**输入/输出设计：**
- 定义输入验证模型（Python 用 Pydantic，TypeScript 用 Zod）
- 设计一致的响应格式（例如，JSON 或 Markdown），以及可配置的详细级别（例如，详细或简洁）
- 规划大规模使用（成千上万的用户/资源）
- 实施字符限制和截断策略（例如，25,000 个 token）

**错误处理策略：**
- 规划优雅的故障模式
- 设计清晰、可操作、LLM 友好的自然语言错误消息，提示进一步的操作
- 考虑速率限制和超时场景
- 处理身份验证和授权错误

---

### 第 2 阶段：实施

有了全面的计划后，开始按照特定语言的最佳实践进行实施。

#### 2.1 设置项目结构

**对于 Python：**
- 创建单个 `.py` 文件，或者如果复杂则组织成模块（参见 [🐍 Python 指南](./reference/python_mcp_server.md)）
- 使用 MCP Python SDK 进行工具注册
- 定义 Pydantic 模型用于输入验证

**对于 Node/TypeScript：**
- 创建正确的项目结构（参见 [⚡ TypeScript 指南](./reference/node_mcp_server.md)）
- 设置 `package.json` 和 `tsconfig.json`
- 使用 MCP TypeScript SDK
- 定义 Zod 模式用于输入验证

#### 2.2 首先实施核心基础设施

**要开始实施，请在实施工具之前创建共享实用程序：**
- API 请求助手函数
- 错误处理实用程序
- 响应格式化函数（JSON 和 Markdown）
- 分页助手
- 身份验证/令牌管理

#### 2.3 系统地实施工具

对于计划中的每个工具：

**定义输入架构：**
- 使用 Pydantic (Python) 或 Zod (TypeScript) 进行验证
- 包含适当的约束（最小/最大长度、正则表达式模式、最小/最大值、范围）
- 提供清晰、描述性的字段说明
- 在字段说明中包含各种示例

**编写全面的文档字符串/描述：**
- 一句话总结工具的作用
- 详细解释目的和功能
- 带有示例的显式参数类型
- 完整的返回类型架构
- 使用示例（何时使用，何时不使用）
- 错误处理文档，概述在特定错误下如何继续

**实施工具逻辑：**
- 使用共享实用程序以避免代码重复
- 对所有 I/O 使用 async/await 模式
- 实施正确的错误处理
- 支持多种响应格式（JSON 和 Markdown）
- 遵守分页参数
- 检查字符限制并适当截断

**添加工具注解：**
- `readOnlyHint`: true (对于只读操作)
- `destructiveHint`: false (对于非破坏性操作)
- `idempotentHint`: true (如果重复调用具有相同的效果)
- `openWorldHint`: true (如果与外部系统交互)

#### 2.4 遵循特定语言的最佳实践

**此时，加载相应的语言指南：**

**对于 Python：加载 [🐍 Python 实现指南](./reference/python_mcp_server.md) 并确保以下几点：**
- 使用带有正确工具注册的 MCP Python SDK
- 使用带有 `model_config` 的 Pydantic v2 模型
- 全程使用类型提示
- 对所有 I/O 操作使用 async/await
- 正确的导入组织
- 模块级常量 (CHARACTER_LIMIT, API_BASE_URL)

**对于 Node/TypeScript：加载 [⚡ TypeScript 实现指南](./reference/node_mcp_server.md) 并确保以下几点：**
- 正确使用 `server.registerTool`
- 使用带有 `.strict()` 的 Zod 模式
- 启用 TypeScript 严格模式
- 无 `any` 类型 - 使用正确的类型
- 显式的 Promise<T> 返回类型
- 配置构建过程 (`npm run build`)

---

### 第 3 阶段：审查和完善

初步实施后：

#### 3.1 代码质量审查

为了确保质量，请审查代码的以下方面：
- **DRY 原则**: 工具之间无重复代码
- **可组合性**: 共享逻辑提取到函数中
- **一致性**: 类似的操作返回类似的格式
- **错误处理**: 所有外部调用都有错误处理
- **类型安全**: 全面的类型覆盖（Python 类型提示，TypeScript 类型）
- **文档**: 每个工具都有全面的文档字符串/描述

#### 3.2 测试和构建

**重要：** MCP 服务器是长时间运行的进程，通过 stdio/stdin 或 sse/http 等待请求。直接在主进程中运行它们（例如 `python server.py` 或 `node dist/index.js`）将导致您的进程无限期挂起。

**测试服务器的安全方法：**
- 使用评估工具（参见第 4 阶段） - 推荐方法
- 在 tmux 中运行服务器以使其保持在主进程之外
- 测试时使用超时：`timeout 5s python server.py`

**对于 Python：**
- 验证 Python 语法：`python -m py_compile your_server.py`
- 通过查看文件检查导入是否正确工作
- 手动测试：在 tmux 中运行服务器，然后在主进程中使用评估工具进行测试
- 或者直接使用评估工具（它管理 stdio 传输的服务器）

**对于 Node/TypeScript：**
- 运行 `npm run build` 并确保无错误完成
- 验证 dist/index.js 已创建
- 手动测试：在 tmux 中运行服务器，然后在主进程中使用评估工具进行测试
- 或者直接使用评估工具（它管理 stdio 传输的服务器）

#### 3.3 使用质量检查表

要验证实施质量，从特定语言指南中加载相应的检查表：
- Python: 参见 [🐍 Python 指南](./reference/python_mcp_server.md) 中的“质量检查表”
- Node/TypeScript: 参见 [⚡ TypeScript 指南](./reference/node_mcp_server.md) 中的“质量检查表”

---

### 第 4 阶段：创建评估

实施 MCP 服务器后，创建全面的评估以测试其有效性。

**加载 [✅ 评估指南](./reference/evaluation.md) 获取完整的评估指南。**

#### 4.1 理解评估目的

评估测试 LLM 是否可以有效地使用您的 MCP 服务器来回答现实的、复杂的问题。

#### 4.2 创建 10 个评估问题

要创建有效的评估，请遵循评估指南中概述的流程：

1. **工具检查**: 列出可用工具并了解其功能
2. **内容探索**: 使用只读操作探索可用数据
3. **问题生成**: 创建 10 个复杂的、现实
4. **答案验证**: 自己解决每个问题以验证答案

#### 4.3 评估要求

每个问题必须是：
- **独立的**: 不依赖于其他问题
- **只读的**: 仅需要非破坏性操作
- **复杂的**: 需要多次工具调用和深度探索
- **现实的**: 基于人类关心的真实用例
- **可验证的**: 具有可以通过字符串比较验证的单一明确答案
- **稳定的**: 答案不会随时间改变

#### 4.4 输出格式

创建一个具有此结构的 XML 文件：

```xml
<evaluation>
  <qa_pair>
    <question>查找关于以动物代号命名的 AI 模型发布的讨论。一个模型需要特定的安全指定，格式为 ASL-X。对于以斑点野猫命名的模型，确定的数字 X 是多少？</question>
    <answer>3</answer>
  </qa_pair>
<!-- 更多 qa_pairs... -->
</evaluation>
```

---

# 参考文件

## 📚 文档库

在开发过程中根据需要加载这些资源：

### 核心 MCP 文档（首先加载）
- **MCP 协议**: 从 `https://modelcontextprotocol.io/llms-full.txt` 获取 - 完整的 MCP 规范
- [📋 MCP 最佳实践](./reference/mcp_best_practices.md) - 通用 MCP 指南，包括：
  - 服务器和工具命名约定
  - 响应格式指南（JSON 与 Markdown）
  - 分页最佳实践
  - 字符限制和截断策略
  - 工具开发指南
  - 安全和错误处理标准

### SDK 文档（在第 1/2 阶段加载）
- **Python SDK**: 从 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 获取
- **TypeScript SDK**: 从 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 获取

### 特定语言实施指南（在第 2 阶段加载）
- [🐍 Python 实现指南](./reference/python_mcp_server.md) - 完整的 Python/FastMCP 指南，包含：
  - 服务器初始化模式
  - Pydantic 模型示例
  - 使用 `@mcp.tool` 进行工具注册
  - 完整的工作示例
  - 质量检查表

- [⚡ TypeScript 实现指南](./reference/node_mcp_server.md) - 完整的 TypeScript 指南，包含：
  - 项目结构
  - Zod 模式模式
  - 使用 `server.registerTool` 进行工具注册
  - 完整的工作示例
  - 质量检查表

### 评估指南（在第 4 阶段加载）
- [✅ 评估指南](./reference/evaluation.md) - 完整的评估创建指南，包含：
  - 问题创建指南
  - 答案验证策略
  - XML 格式规范
  - 示例问题和答案
  - 使用提供的脚本运行评估
