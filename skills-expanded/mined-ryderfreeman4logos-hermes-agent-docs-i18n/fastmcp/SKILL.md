---
name: fastmcp
description: Build, test, and deploy Python MCP servers.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [MCP, FastMCP, Python, Tools, Resources, Prompts, Deployment]
    homepage: https://gofastmcp.com
    related_skills: [hermes-agent, mcporter]
prerequisites:
  commands: [python]
---

# FastMCP

使用 FastMCP 用 Python 构建 MCP 服务器，在本地进行验证，将其安装到 MCP 客户端中，进而作为 HTTP 接口进行部署。

## 适用场景

当需要执行以下任务时，可使用此技能：

- 用 Python 创建新的 MCP 服务器
- 将 API、数据库、CLI 或文件处理流程封装为 MCP 工具
- 除了工具之外还需提供资源或提示词
- 在将服务器接入 Hermes 或其他客户端之前，使用 FastMCP CLI 进行初步测试
- 将服务器安装到 Claude Code、Claude Desktop、Cursor 或类似的 MCP 客户端中
- 准备用于 HTTP 部署的 FastMCP 服务器代码仓库

如果服务器已存在且仅需连接到 Hermes，则应使用 `native-mcp`。若目标是临时通过 CLI 访问现有的 MCP 服务器而非从头构建，则应使用 `mcporter`。

## 先决条件

首先在工作环境中安装 FastMCP：

```bash
pip install fastmcp
fastmcp version
```

对于 API 模板，如果尚未安装 `httpx`，请先进行安装：

```bash
pip install httpx
```

## 包含的文件

### 模板

- `templates/api_wrapper.py` - 支持身份验证头的 REST API 封装工具
- `templates/database_server.py` - 只读 SQLite 查询服务器
- `templates/file_processor.py` - 文本文件检测与搜索服务器

### 脚本

- `scripts/scaffold_fastmcp.py` - 复制示例模板并替换服务器名称占位符

### 参考资料

- `references/fastmcp-cli.md` - FastMCP CLI 工作流程、安装要求及部署检查项

## 工作流程

### 1. 选择最精简的可行服务器架构

首先确定最小的实用功能范围：

- API 封装工具：从 1-3 个高价值接口开始，而非整个 API
- 数据库服务器：仅提供只读查询功能及受限的查询路径
- 文件处理工具：通过明确的路径参数实现确定性操作
- 提示词/资源模块：仅在客户端需要可复用的提示词模板或可检索文档时再添加

相比功能繁多但工具定义模糊的大型服务器，更推荐选择结构精简、具备清晰名称、文档说明及数据结构的服务器。

### 2. 基于模板快速搭建

可直接复制模板，或使用搭建辅助脚本：

```bash
python ~/.hermes/skills/mcp/fastmcp/scripts/scaffold_fastmcp.py \
  --template api_wrapper \
  --name "Acme API" \
  --output ./acme_server.py
```

可用模板：


需完整翻译输入内容，不得提前终止。

```bash
python ~/.hermes/skills/mcp/fastmcp/scripts/scaffold_fastmcp.py --list
```

如果选择手动复制，请将 `__SERVER_NAME__` 替换为实际的服务器名称。

### 3. 先实现工具功能

在添加资源或提示词之前，先从 `@mcp.tool` 函数开始构建。

工具设计的规则如下：

- 为每个工具起一个以动词构成的具体名称
- 将文档字符串编写成面向用户的工具描述
- 确保参数清晰且带有类型标注
- 尽可能返回结构化且符合 JSON 格式的数据
- 及早验证可能存在风险的输入
- 在初始版本中，默认采用只读模式

优秀的工具示例：

- `get_customer`
- `search_tickets`
- `describe_table`
- `summarize_text_file`

较差的工具示例：

- `run`
- `process`
- `do_thing`

### 4. 仅在有必要时添加资源与提示词

当客户端需要获取诸如架构定义、政策文档或生成的报告等稳定的只读内容时，再添加 `@mcp.resource`。

当服务器需要为某种已知工作流程提供可重复使用的提示词模板时，再添加 `@mcp.prompt`。

切勿将每份文档都转化为提示词。建议采用以下方式：

- 使用工具来执行操作
- 使用资源来检索数据或文档
- 使用提示词来提供可重复使用的大语言模型指令

### 5. 在集成到任何系统之前先测试服务器

可使用 FastMCP CLI 进行本地验证：

```bash
fastmcp inspect acme_server.py:mcp
fastmcp list acme_server.py --json
fastmcp call acme_server.py search_resources query=router limit=5 --json
```

为实现高效的迭代式调试，请在本地运行该服务器：

```bash
fastmcp run acme_server.py:mcp
```

要在本地测试 HTTP 传输功能：

```bash
fastmcp run acme_server.py:mcp --transport http --host 127.0.0.1 --port 8000
fastmcp list http://127.0.0.1:8000/mcp --json
fastmcp call http://127.0.0.1:8000/mcp search_resources query=router --json
```

在确认服务器正常运行之前，务必针对每款新工具至少执行一次真实的 `fastmcp call` 操作。

### 6. 本地验证通过后安装到客户端中

FastMCP 可将服务器注册到支持 MCP 的客户端中：

```bash
fastmcp install claude-code acme_server.py
fastmcp install claude-desktop acme_server.py
fastmcp install cursor acme_server.py -e .
```

可使用 `fastmcp discover` 命令来查看机器上已配置的命名 MCP 服务器。

若目标是与 Hermes 集成，可选择以下任一方式：

- 在 `~/.hermes/config.yaml` 文件中通过 `native-mcp` 技能配置服务器，或
- 在开发阶段继续使用 FastMCP CLI 命令，直至接口稳定为止

### 7. 当本地契约稳定后进行部署

对于托管式服务，FastMCP 文档中有最直接的部署指南，即 Prefect Horizon。在部署之前：

```bash
fastmcp inspect acme_server.py:mcp
```

请确保该代码仓库中包含以下内容：

- 包含 FastMCP 服务器对象的 Python 文件  
- `requirements.txt` 或 `pyproject.toml` 文件  
- 部署所需的环境变量相关文档  

对于常规的 HTTP 托管场景，建议先在本地验证 HTTP 传输功能，之后再将服务部署到任何能够开放服务器端口的 Python 兼容平台上。

## 常见实现模式

### API 封装模式

适用于将 REST 或 HTTP API 转换为 MCP 工具的场景。

推荐的初始功能模块包括：

- 一个读取路径  
- 一个列表/搜索路径  
- 可选的健康检查功能  

实现注意事项：

- 将认证信息存储在环境变量中，而非硬编码  
- 将请求处理逻辑集中到同一个辅助函数中  
- 以简洁的方式反馈 API 错误信息  
- 在返回数据前对格式不一致的上游数据进行标准化处理  

可从 `templates/api_wrapper.py` 文件开始实现。

### 数据库模式

适用于需要提供安全的数据查询与查看功能的场景。

推荐的初始功能模块包括：

- `list_tables`  
- `describe_table`  
- 一个带限制条件的读取查询工具  

实现注意事项：

- 默认仅允许读取数据库数据  
- 在早期版本中拒绝非 `SELECT` 类型的 SQL 查询  
- 限制返回的记录数量  
- 同时返回数据行和列名  

可从 `templates/database_server.py` 文件开始实现。

### 文件处理模式

适用于需要按需检查或转换文件的服务器场景。

推荐的初始功能模块包括：

- 概要总结文件内容  
- 在文件内进行搜索  
- 提取确定的元数据  

实现注意事项：

- 接受显式的文件路径  
- 检查是否存在缺失的文件以及编码错误  
- 限制预览数量和结果数量  
- 除非确实需要特定的外部工具，否则避免调用shell命令  

请从 `templates/file_processor.py` 文件开始。  

## 质量检查标准  

在将FastMCP服务器交付使用之前，请确认以下所有事项：  

- 服务器能够正常导入  
- `fastmcp inspect <file.py:mcp>` 命令执行成功  
- `fastmcp list <server spec> --json` 命令执行成功  
- 每个新工具都至少包含一个真实的 `fastmcp call` 调用  
- 所有环境变量都有明确的文档说明  
- 工具的接口设计简洁，无需猜测即可理解  

## 故障排除  

### FastMCP命令缺失  

在当前激活的环境中安装相应包：

```bash
pip install fastmcp
fastmcp version
```

### `fastmcp inspect` 命令执行失败

请检查以下内容：

- 文件导入时不会引发导致程序崩溃的副作用；
- `<file.py:object>` 中的 FastMCP 实例名称是否正确；
- 模板中指定的可选依赖项是否已安装。

### 工具在 Python 环境下可正常运行，但通过 CLI 无法使用

请执行以下操作：

```bash
fastmcp list server.py --json
fastmcp call server.py your_tool_name --json
```

这通常是由于名称不匹配、缺少必需参数，或是返回值不可序列化所导致的。

### Hermes 无法识别已部署的服务器

虽然服务器构建部分可能是正确的，但 Hermes 的配置可能存在问题。请加载 `native-mcp` 技能，并在 `~/.hermes/config.yaml` 中配置服务器，之后重新启动 Hermes。

## 参考资料

如需了解 CLI 详情、目标安装以及部署检查的相关内容，请参阅 `references/fastmcp-cli.md`。
