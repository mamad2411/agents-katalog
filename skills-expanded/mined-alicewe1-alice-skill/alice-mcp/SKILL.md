---
name: alice-mcp
description: MCP 热启动网关（不写客户端 config，agent 经网关直接调用 MCP 工具；自检/添加/移除/热开关/目录包装/工具目录发现）。触发词：mcp自检/添加mcp/移除mcp/mcp管理/mcp工具/包装工具目录。
x-alice-class: assist
x-alice-domain: routing-skill-engineering
---

# alice-mcp — MCP 热启动网关（agent 层调用，零客户端配置）

> 架构（硬性理解）：
> - MCP server **不写入任何客户端 config**（codex/dsh/claude/workbuddy/pi 一律不写）。
> - `mcp_gateway.py` 按 registry 直接 spawn server 进程（stdio JSON-RPC），取工具目录、
>   转发调用，结果以普通命令输出喂给 agent —— **即加即用，无需重启客户端**。
> - 热开关：registry `disabled=true/false` 即时生效（gateway 每次调用现读）。
> - 兼容回退：`--client-sync` 可选把 registry 编译进当前客户端配置（默认不用）。

## 脚本与入口

| 命令 | 作用 |
|:--|:--|
| `mcp_manager.py --check` | 环境自检：registry / mcpRoot / server 健康与生效提示 |
| `mcp_manager.py --add <名> --cmd X --args "..." [--cwd D] [--env K=V]` | 添加 stdio server（**即加即用**） |
| `mcp_manager.py --add <名> --url U [--headers "K=V"]` | 添加 http server |
| `mcp_manager.py --remove <名>` | 移除 |
| `mcp_manager.py --disable <名>` / `--enable <名>` | **热关/热开**（即时生效） |
| `mcp_manager.py --test <名>` | server 进程握手验证 |
| `mcp_manager.py --wrap <目录> [--name S]` | 目录内可执行文件 → 一个 MCP server（每文件一个 `run_<名>` 工具） |
| `mcp_gateway.py list` | **agent 工具目录发现入口**（所有启用 server 的工具清单） |
| `mcp_gateway.py list <server> --json` | 单 server 工具目录（JSON） |
| `mcp_gateway.py call <server> <tool> '{"k":"v"}'` | 调用工具（stdout 即结果） |
| `mcp_gateway.py ping [server]` | 批量握手存活 |
| `mcp_gateway.py start/stop/status` | 常驻池预热/关闭/状态 |

脚本位置：`<技能根>/aliceskill/scripts/`。退出码 0/2/3/4。

## AI 执行流程

### 工具发现（每个任务开始时，动态）

```bash
python "<技能根>/aliceskill/scripts/mcp_gateway.py" list
```

- 输出形如 `mcp__<server>__<tool>  — 描述`；**以这条命令的实时输出为准**，不凭记忆假设有哪些 server。
- 调用：

```bash
python "<技能根>/aliceskill/scripts/mcp_gateway.py" call <server> <tool> '{"参数": "值"}' --timeout 300
```

### 添加（吸收）MCP

1. 问清四件事：名字、stdio（本地命令）还是 http（远程 URL）、**归属分类**（crack/reverse/pentest/game/ai/assist，可多选——决定出现在哪些路由页）、一句话说明。
2. stdio：`--add <名> --cmd <命令> --args "<参数>" --cwd <工作目录> --classes <类,类> --desc "<说明>"`（相对参数自动转绝对；`--classes` 决定该 server 出现在哪些路由页）。
3. http：`--add <名> --url <URL> --headers "Authorization=Bearer xxx" --classes <类,类>`。**网关双传输**：stdio（本地进程）与 Streamable HTTP（远程 MCP，如 github `https://api.githubcopilot.com/mcp/`）都已实现——registry 里有 `url` 自动走 HTTP，无 `url` 走 stdio；认证失败报 `HTTP 401/400` 并指向检查 headers。
4. 从 GitHub 装：先验证仓库真是 MCP server（package.json bin / pyproject 入口 / Dockerfile / 现成 http URL），验证不过不入库；装完走第 2/3 步。
5. **即加即用**：加完 `mcp_gateway.py list` 立即可见，无需重启客户端、无需写 config。
6. **归类落到路由页**：`--classes` 写入 registry 后重跑 `rebuild_menu.py`，该 server 自动出现在对应六类路由页的「可用 MCP 工具（按需使用，不全部加载）」段——例如 IDA 类 server 归 `reverse,crack` 就同时出现在逆和破两页。改归属 = 重新 `--add` 同名条目再重建。

### 使用中调用（优先级规则）

- 会话内盘点到与任务相关的 MCP 工具 → **优先调用**（经 gateway，输出即结果）。
- 调用失败/超时/无匹配 → **立即回退**本地命令与脚本继续执行，不停手、不追问、不要求用户装环境。
- **开工先汇报工作链路**：正式动手前向用户输出一行——`当前预使用 MCP 工具: xxx | xxx | xxx`（按需列出，无则写：无，走本地）+ `使用技能 N 个，取自: <模块id>.md | <模块id>.md | …`（N 个对应 `_modules/` 里的具体 SKILL.md 文件名，不是类名或领域名）；执行中新增取模块或启用新 MCP server 时同步更新。
- 模块 frontmatter `x-alice-mcp: <server名>` 仅作核对提示：gateway list 里有就用，没有就回退。

### 热开关（不使用时关闭）

```bash
mcp_manager.py --disable <名>    # 热关：gateway 立即拒绝该 server 调用
mcp_manager.py --enable <名>     # 热开：立即可调
```

- registry 每次调用现读，**无需重启任何东西**——这就是"要使用时申请、不使用时关闭"的实现。

### 目录包装（把任意工具目录变成 MCP）

```bash
mcp_manager.py --wrap <目录> --name <server名>
mcp_gateway.py list <server名>
mcp_gateway.py call <server名> run_<文件名> '{"argv": ["--help"], "timeout": 60}'
```

## MCP 工作目录（mcpRoot）——向用户解释用

首次 `--add` 时 manager 会问「MCP 工作目录」。向用户转述以下要点（不要让用户猜）：

- **它是什么**：一个存放 MCP 数据的文件夹。你添加的所有 MCP server 清单（`servers.json`）、`--wrap` 生成的包装 server 都存在这里；gateway 每次调用都来这读配置。
- **怎么选**：直接用默认（`<客户端主目录>/mcp`，如 `~/.workbuddy-ai/mcp`）即可——跟客户端数据待在一起，备份/迁移顺手。别放 U 盘或网络盘（server 启动路径要稳定）。
- **确认方式**：回车确认默认，或指定目录后执行 `mcp_manager.py --set-root "<目录>"` 落盘（写入 `aliceskill/config/mcp_settings.json`，之后不再询问）。
- **换位置**：改/删 `mcp_settings.json` 后重新 `--set-root`；registry 里带旧绝对路径的 server 需重新 `--add`（用 `--test <名>` 逐个验证）。
- **换电脑**：发布包不含此目录的锁存信息（`mcp_settings.json` 不随包），新机首次使用重新问一次——这是设计行为。
## 常见故障

| 现象 | 处置 |
|:--|:--|
| `gateway list` 报 unavailable | `--ping <名>` 看握手错误；命令不存在 → 修 registry 路径 |
| 工具调用超时 | `--timeout` 加大；server 卡死用 `gateway stop --all` 清池 |
| mcpRoot 未锁存 | manager 会 exit 3 问用户；用户给目录后 `--set-root` 落盘 |
| codex 报 duplicate key（历史遗留） | 旧版曾写客户端 config 且逐键重复子表头；现架构已不写 config，`--client-sync` 写入器已修复为单子表头 |

## 与其它机制的关系

- **客户端原生 MCP**（dsh cordis / pi mcp.json）与本网关**互不干扰**：原生由客户端拉起、工具直接出现在会话；本网关由 agent 显式调用。同一 server 两边都配会重复，选一种。
- 提示词注入块（`inject_route_prompt.py`）只写「动态发现」规则，不含任何 server 清单。
