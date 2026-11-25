---
name: repotalk
description: Analyze code repository structure, locate code details, trace dependencies and call chains across packages and functions, and search code semantically using natural language. Use whenever the user wants to understand how code works in a repo, trace a function's callers or callees, search for code by meaning, look up ByteDance internal infrastructure component usage (Hertz, Kitex, Redis, MySQL, etc.), analyze repository architecture, or get RPC call info for a PSM. Also trigger when the user asks "how does X work" or "where is X implemented" about a remote codebase, or mentions Repotalk.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Repotalk 代码仓库查询

> **何时使用**: 当需要查询代码仓库的功能结构、代码细节、服务信息时调用此 SKILL。

一个用于查询代码仓库的 **功能结构**、**代码细节**、**服务信息** 的工具集。

## 使用方法

```bash
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "<action>", ...}'
```

## 支持的 Action

| Action | 描述 | 必填参数 | 可选参数 |
|--------|------|----------|----------|
| `get_repos_detail` | 获取指定仓库详细信息，包括仓库的概览、包（package）列表、服务API列表（仅对HTTP/RPC服务类型有效） | repo_names | |
| `get_packages_detail` | 精确获取指定包（package）的功能、流程及包内的文件列表 | repo_name, package_ids | |
| `get_files_detail` | 获取指定路径文件的 ast 信息或配置文件、IDL 文件等 | repo_name, file_path | |
| `get_nodes_detail` | 精确获取指定 函数（FUNC）、类型（TYPE）、变量（VAR） 的详细信息及关系 | repo_name, node_ids | need_related_codes |
| `search_nodes` | 执行语义化的代码搜索，允许使用自然语言在指定仓库中查询 | question, repo_names | package_ids |
| `get_service_apis` | 获取指定仓库API接口的功能描述、处理流程及参数信息 | repo_name, api_names | |
| `get_rpcinfo` | 获取向目标 psm 的目标 method 发起 RPC 调用的方式和相关信息 | psm | method |
| `infra_search` | 获取字节跳动（公司）内部基础设施和基础组件的用法 | component, question | |
| `get_asset_file` | 获取仓库内的 asset，包括 readme、idl 文件、配置文件等 | repo_name, file_paths | |

## 输入参数

| 参数 | 类型 | 描述 |
|------|------|------|
| action | string | 必填，要执行的操作 |
| repo_names | string | 仓库名称（多个用逗号分隔） |
| repo_name | string | 仓库名称 |
| package_ids | string | 包 ID 列表，格式: `发行模块?命名空间` |
| file_path | string | 文件路径（相对于仓库根目录） |
| node_ids | string | 节点 ID 列表，格式: `${go_module_name}?${package_name}#${name}` |
| api_names | string | API 名称列表 |
| psm | string | PSM 名称 |
| method | string | 可选，方法名 |
| component | string | 组件名称（如 Hertz、Kitex、Redis、MySQL 等） |
| file_paths | string | 文件路径列表（多个用逗号分隔） |
| need_related_codes | boolean | 可选，是否返回相关节点的代码 |
| question | string | 可选，查询问题（建议使用中文） |
| branch | string | 可选，分支名 |

## 标准操作流程

### 1. 仓库概览
使用 `get_repos_detail` 获取仓库的详细信息，包括：
- 仓库概述
- 仓库中的包列表
- 仓库中的服务接口列表（可选，仅 HTTP/RPC 服务仓库有）

### 2. 问题分析
结合用户问题和上下文，分析出可能和问题相关的 **关键词** 或者 **可能的代码片段**。

### 3. 代码定位
结合步骤 2 中的分析，按照 **包 → 文件 → 节点** 逐级定位目标节点（函数、类型或变量）：

1. **定位包**: 基于 `get_repos_detail` 返回的包列表选取目标包，并通过 `get_packages_detail` 确认
2. **定位文件**: 基于 `get_packages_detail` 返回的文件列表选取目标文件，并通过 `get_files_detail` 确认
3. **定位节点**: 基于 `get_files_detail` 返回的节点列表选取目标节点，并通过 `get_nodes_detail` 确认
4. **关系确认**: 通过 `get_nodes_detail` 获取节点与其它节点的相互关系，包括：
   - **dependencies**: 依赖了哪些节点
   - **references**: 被哪些节点引用
   - **inherits**: 继承关系
   - **implements**: 实现关系
   - **groups**: 分组信息
   
   最终确定目标节点是否满足需要。如果需要确认 **多级间接关系** 的节点，可以递归调用 `get_nodes_detail` 获取间接目标节点的信息。

### 4. 问题反思
回答用户问题前，尽量弄清楚产生问题的 **完整的代码调用链路** 和 **上下文作用关系**。

如果步骤 3 返回的结果无法解释清楚运行机制或不满足用户需求，可以尝试调整 **关键词** 或 **选取列表**，重新进行步骤 3 直到能够准确回答用户问题。

## 输出格式

```json
{
  "success": true,
  "action": "get_repos_detail",
  "data": { ... }
}
```

## 示例

```bash
# 获取仓库详细信息
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "get_repos_detail", "repo_names": "github.com/cloudwego/kitex"}'

# 获取包详细信息
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "get_packages_detail", "repo_name": "github.com/cloudwego/kitex", "package_ids": "github.com/cloudwego/kitex?github.com/cloudwego/kitex/pkg/generic"}'

# 获取文件详细信息
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "get_files_detail", "repo_name": "github.com/cloudwego/kitex", "file_path": "pkg/generic/generic.go"}'

# 获取节点详细信息及关系（依赖、引用等）
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "get_nodes_detail", "repo_name": "github.com/cloudwego/kitex", "node_ids": "github.com/cloudwego/kitex?github.com/cloudwego/kitex/pkg/generic#Closer.Close"}'

# 获取节点详细信息，包含相关节点代码
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "get_nodes_detail", "repo_name": "github.com/cloudwego/kitex", "node_ids": "github.com/cloudwego/kitex?github.com/cloudwego/kitex/pkg/generic#Closer.Close", "need_related_codes": "true"}'

# 语义化代码搜索
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "search_nodes", "question": "鉴权中间件在哪里", "repo_names": "github.com/cloudwego/kitex"}'

# 语义化代码搜索，指定包范围
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "search_nodes", "question": "泛化调用的实现", "repo_names": "github.com/cloudwego/kitex", "package_ids": "github.com/cloudwego/kitex?github.com/cloudwego/kitex/pkg/generic"}'

# 获取服务 API 接口信息
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "get_service_apis", "repo_name": "github.com/cloudwego/kitex", "api_names": "GetUser"}'

# 获取 RPC 调用信息
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "get_rpcinfo", "psm": "a.b.c"}'

# 获取指定方法的 RPC 调用信息
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "get_rpcinfo", "psm": "a.b.c", "method": "Echo"}'

# 查询字节跳动内部组件用法（提问方式为 component + 用法，不能组合使用）
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "infra_search", "component": "Hertz", "question": "反向代理如何使用"}'

# 查询 Kitex 框架用法
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "infra_search", "component": "Kitex", "question": "如何配置超时"}'

# 获取仓库 asset 文件（readme、idl、配置文件等）
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "get_asset_file", "repo_name": "github.com/cloudwego/kitex", "file_paths": "README.md"}'

# 获取多个 asset 文件
gdpa-cli run repotalk --session-id "$SESSION_ID" --input '{"action": "get_asset_file", "repo_name": "github.com/cloudwego/kitex", "file_paths": "README.md,go.mod"}'
```

## 注意事项

### 通用
- `question` 参数中**关键字尽量使用中文**，代码使用原始代码
- `package_id` 格式为 `发行模块?命名空间`，例如：`github.com/cloudwego/kitex?github.com/cloudwego/kitex/pkg/generic`
- `node_id` 格式为 `发行模块?命名空间#符号名`，例如：`github.com/cloudwego/kitex?github.com/cloudwego/kitex/pkg/generic#Closer.Close`
- 对于结构体方法，name 为 `${结构体名称}.${方法名}`
- **尽量使用 `get_nodes_detail` 确认节点的依赖（Dependencies）和引用（References）关系**
- **鼓励递归调用 `get_nodes_detail` 确保清楚间接关系的代码节点**
- 当缺少信息时，可以通过 `get_repos_detail` -> `get_packages_detail` -> `get_files_detail`/`get_nodes_detail` 的方式逐级获取

### get_files_detail
- 应该通过 `get_repos_detail` -> `get_packages_detail` -> `get_files_detail` 的路径去寻找文件，除非明确知道文件名称
- 当请求多个文件时，如果只要一个文件存在，就会返回该文件的信息
- 当所有文件不存在时，会返回所有的文件列表

### get_rpcinfo
- 将 psm 中的 `.` 替换为 `_`（下面用 `${psm_}` 代替）
- 新增 import：`code.byted.org/overpass/${psm_}/rpc/${psm_}`
- 发起调用代码：`resp, err := ${psm_}.RawCall.${method}(ctx, req)`
- 示例：向 `a.b.c` 服务请求 `Echo` 方法：`resp, err := a_b_c.RawCall.Echo(ctx, req)`，import 为 `import a_b_c "code.byted.org/overpass/a_b_c/rpc/a_b_c"`
- 结构体类型定义为 `${package}:${type}`，`*` 前缀表示指针类型
- 枚举类型定义为 `${package}:${type}=${value}`

### infra_search
- 提问方式应为 `${component} + ${用法}`，如：`Hertz 反向代理如何使用`
- **注意不能组合使用**，如 `Hertz 中如何使用 MySQL` 是不正确的

### get_asset_file
- 不会返回代码文件，如需获取代码文件使用 `get_files_detail`
- 如果传递的文件不存在，会返回所有可获取的文件列表

### 认证
- JWT Token 会**自动获取**（默认使用 CN 区域），无需手动传入
- 首次使用需要先执行 `gdp login` 登录

### 环境要求
- 需要安装 `gdp` 工具（用于自动获取 JWT Token，未安装时会自动安装）
