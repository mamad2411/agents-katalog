---
name: codegraph
description: 当需要搜索符号定义、追踪双向调用链、分析变更影响、选取受影响测试、理解陌生模块时，用预索引的代码知识图谱一次调用替代多轮 grep/glob/read_file，工具调用减少 60%+、token 消耗降低 50%+
---

# CodeGraph — 代码知识图谱辅助

## 核心原则

CodeGraph 预索引了项目的符号关系和调用图，一次 CLI 调用即可替代多轮 grep/glob/read_file 操作。当项目根目录存在 `.codegraph` 文件夹时，**优先使用 codegraph 命令**获取代码上下文，显著减少工具调用次数和 token 消耗。

**五大能力**：①任务上下文（context）②符号搜索（query）③双向调用链（callers/callees）④符号驱动变更影响（impact）⑤diff 驱动测试选择（affected）。凡属这五类的结构问题一律 codegraph，不要去动 cbm（cbm 只保留架构概览/复杂度排行/commit 影响半径三个场景）。

## 前置条件

项目已初始化并完成索引（`codegraph status` 显示 Files > 0）。如未初始化，**分两步**执行：

```bash
# 第一步：初始化（只需一次，创建 .codegraph 配置目录）
codegraph init

# 第二步：索引源码（扫描解析所有代码文件）
codegraph index
```

**⚠️ 常见错误：**
- ✅ `codegraph init --index` — 一步完成初始化+初始索引（0.9.x 的 `--index` 会在初始化后接着跑索引）
- ❌ `codegraph index <path>` — index 不需要路径参数，在项目目录下直接执行即可
- ❌ 初始化后未索引就直接用 `context`/`query` — 会报错或返回空结果，必须先 `index`

验证索引状态：
```bash
codegraph status   # 确认 Files > 0
```

## 五大能力（完整参数）

### 1. `context` — 任务级智能上下文（首选）

开始任何编码任务前，先用 `context` 获取整体上下文，一次调用返回入口点、相关符号和代码片段。

```bash
# 为一个任务描述构建上下文，返回相关符号和代码
codegraph context "实现用户登录的 JWT 认证" --max-nodes 20

# 控制代码块数量；--no-code 只要符号清单不要源码片段（更省 token）
codegraph context "优化数据库查询性能" --max-nodes 15 --max-code 5
codegraph context "梳理导出逻辑" --no-code

# JSON 输出便于程序解析；-p 指定其他项目路径
codegraph context "重构缓存层" --format json -p /path/to/other/repo
```

| 参数 | 说明 |
|---|---|
| `-n, --max-nodes <n>` | 最多返回符号节点数（默认 50） |
| `-c, --max-code <n>` | 最多代码块数（默认 10） |
| `--no-code` | 排除代码块，只要符号级上下文 |
| `-f, --format <fmt>` | `markdown`（默认）或 `json` |
| `-p, --path <path>` | 项目路径（默认当前目录） |

**何时使用：** 接到任务后、动手写代码前的第一步。替代 Explore 子代理的多轮文件扫描。

### 2. `query` — 按名称搜索符号

精确定位函数、类、类型、接口等符号定义。

```bash
# 搜索名为 HandleLogin 的符号
codegraph query HandleLogin

# 限定符号类型 + 扩大结果数
codegraph query "User" --kind class --limit 10

# JSON 输出，便于解析
codegraph query "ParseToken" --json
```

| 参数 | 说明 |
|---|---|
| `-l, --limit <n>` | 最多结果数（默认 10） |
| `-k, --kind <kind>` | 按节点类型过滤（function/class/method/type/interface/variable 等） |
| `-j, --json` | JSON 输出 |
| `-p, --path <path>` | 项目路径 |

**何时使用：** 需要找到某个函数/类/类型的定义位置时，替代 `grep "func HandleLogin"`。

### 3. `callers` / `callees` — 双向调用链

一对互补命令：向上找谁调用了我，向下找我调用了谁。框架感知：查询 controller 的 callers 会暴露关联的 URL 路由。

```bash
# 谁调用了 HandleLogin（上游）
codegraph callers HandleLogin --limit 20

# HandleLogin 内部调用了什么（下游）
codegraph callees "ProcessOrder" --limit 15

# JSON 输出
codegraph callers "UserService.Create" --json
```

| 参数 | 两个命令一致 |
|---|---|
| `-l, --limit <n>` | 最多结果数（默认 20） |
| `-j, --json` | JSON 输出 |
| `-p, --path <path>` | 项目路径 |

**何时使用：** 修改函数签名前先 `callers` 确认调用方；理解复杂函数内部流程或评估下游影响用 `callees`。

### 4. `impact` — 符号驱动的变更影响分析

修改代码前评估波及范围：遍历 callers 和 callees 双向闭包，给出完整影响半径。

```bash
# 分析修改 UserRepo.Find 的影响范围，遍历 3 层
codegraph impact "UserRepo.Find" --depth 3

# JSON 输出
codegraph impact "Config.Load" --depth 2 --json
```

| 参数 | 说明 |
|---|---|
| `-d, --depth <n>` | 闭包遍历深度（默认 2） |
| `-j, --json` | JSON 输出 |
| `-p, --path <path>` | 项目路径 |

**何时使用：** 重构前评估风险；修改公共接口前确认波及。⚠️ 它是**符号驱动**的——拿到的是一串 git diff 想知道影响时，那是 cbm `detect_changes` 的场景。

### 5. `affected` — diff 驱动的受影响测试选择

给定改动的源文件，反向找出应当重跑的测试文件。改完代码决定"跑哪些测试"时用，替代全量测试或凭感觉挑。

```bash
# 直接传文件
codegraph affected src/auth/login.ts src/auth/session.ts

# 从 stdin 批量读（配合 git diff 天然衔接）
git diff --name-only HEAD~1 | codegraph affected --stdin

# 自定义测试文件 glob；-q 只要纯净路径列表（好接脚本）
codegraph affected --filter "e2e/*.spec.ts" -q src/auth/login.ts
```

| 参数 | 说明 |
|---|---|
| `--stdin` | 从 stdin 读文件清单（每行一个），与 `git diff --name-only` 管道衔接 |
| `-d, --depth <n>` | 依赖遍历深度（默认 5） |
| `-f, --filter <glob>` | 自定义测试文件匹配规则 |
| `-q, --quiet` | 只输出路径，无装饰 |
| `-j, --json` | JSON 输出 |
| `-p, --path <path>` | 项目路径 |

**何时使用：** 提交前/PR 前决定最小测试集；CI 里做变更驱动的测试分层。

## 运维辅助命令（非分析能力）

```bash
codegraph files --filter "*.go" --max-depth 2   # 索引的文件结构概览，替代多层 list_directory
codegraph sync [path]                            # 手动增量同步（通常自动，防抖 2s）
codegraph status                                 # 索引状态与统计（Files > 0 才可用）
codegraph unlock [path]                          # 清理阻塞索引的残留锁文件
codegraph serve                                  # 作为 MCP server 常驻（AI 助手接入）
codegraph install / uninstall                    # 安装/移除各客户端的 MCP 接入
```

`files` 适合快速了解模块划分；`context/query` 结果看着过时或不完整时先 `sync` 再查。

## 典型工作流示例

### 场景：修改一个 API 端点的处理函数

```
第一步：获取任务上下文
  codegraph context "修改 /api/users 端点增加分页功能"

第二步：定位目标符号
  codegraph query "GetUsers" --kind function

第三步：了解谁在调用（确认路由绑定）
  codegraph callers GetUsers

第四步：了解内部调用链（确认数据层依赖）
  codegraph callees GetUsers

第五步：评估变更影响
  codegraph impact GetUsers --depth 2

第六步：改完后选出需要重跑的测试
  git diff --name-only | codegraph affected --stdin

→ 至此编码与验证范围都已明确，无需额外的 grep/read_file
```

### 场景：理解一个不熟悉的模块

```
第一步：整体上下文
  codegraph context "理解 auth 模块的认证流程"

第二步：浏览文件结构
  codegraph files --filter "*.go" --max-depth 3

第三步：追踪核心符号的调用链
  codegraph callers AuthService.Validate
  codegraph callees AuthService.Validate
```

## 与现有工具的优先级

| 场景 | 优先使用 | 而非 |
|---|---|---|
| 开始编码任务前 | `codegraph context` | Explore 子代理 |
| 查找函数/类定义 | `codegraph query` | `grep_search` |
| 追踪调用关系 | `codegraph callers/callees` | 手动 grep + read_file |
| 评估符号变更风险 | `codegraph impact` | 猜测 + 试错 |
| 改动后选测试 | `codegraph affected` | 全量跑测试 |
| 查看项目结构 | `codegraph files` | 多层 `list_directory` |
| 架构概览/复杂度排行/commit 影响半径 | **cbm**（另一 skill） | codegraph 无此能力 |

**注意：** 当 codegraph 返回不足时（如搜索非符号内容、查看具体实现逻辑），仍使用 `read_file` 读取完整源码。codegraph 提供的是符号级视图，不是源码全文。
