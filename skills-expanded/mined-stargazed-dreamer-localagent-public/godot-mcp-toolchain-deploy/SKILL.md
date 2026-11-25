---
name: godot-mcp-toolchain-deploy
description: 把 Godot AI 工具链（gdflow.py + gdmcp CLI + Godot-MCP-Native 补丁版 + godot-multi-manager）接入一个 Godot 4.x 项目，让 Agent 能通过 MCP 操纵编辑器。当用户说「部署 Godot MCP」「接入 godot-ai-toolkit」「让 AI 能操作 Godot 场景」「gdflow init 报错」时使用。
agent_created: true
task_type: daily.godot_mcp_toolchain_deploy
---

# Godot MCP 工具链部署

工具链源：`<projects_parent>\GameProject\godot-ai-toolkit`（22M，含离线缓存，可整目录拷贝）。
引擎（本机唯一）：`<projects_parent>\GameProject\godot-4.7.2\Godot_v4.7.2-stable_win64.exe`。

```
AI Agent ──► gdflow.py（单文件零依赖）──► gdmcp CLI ──► Godot-MCP-Native 插件（编辑器内开 MCP 服务）
                    ↑
        godot-multi-manager（:17890，编排多实例、自动分配 MCP 端口）
```

## 部署 5 步

### 1. 拷贝工具链到目标工作区

```bash
cp -r <projects_parent>/GameProject/godot-ai-toolkit <工作区>/_toolchain/
```
不要动 `dev_toolkit_v3.zip` 之类的打包副本（godot-ai-toolkit 无此问题，但别拷 `_toolchain` 外的旧副本）。

### 2. 先起 manager，再 init（顺序不能反）

```bash
cd <toolkit>/manager && node server.mjs      # 后台常驻，Web UI :17890
```

**必须先把 Godot 路径喂给 manager**，否则第 3 步会在最后一步 `projstart` 处报
`HTTP Error 400`（urllib 只显示 "Bad Request"，真实原因在响应体里，看不到）：

```bash
# 正斜杠可以被接受
curl -s -X POST http://127.0.0.1:17890/api/settings \
  -H "Content-Type: application/json" -d '{"godotPath":"F:/path/to/Godot_v4.7.2-stable_win64.exe"}'
```
⛔ **Git Bash 的 curl 会把 JSON 里的反斜杠吃掉** → manager 回「请求体不是合法 JSON」。
要用原生反斜杠路径就停掉 manager、直接改 `manager/data/config.json` 的 `settings.godotPath` 再重启。

### 3. init

```bash
cd <toolkit>
python gdflow.py --project "<工程绝对路径>" --godot "<Godot.exe 绝对路径>" init
```

⛔ **`--godot` / `--port` / `--manager` 是全局参数，必须写在子命令 `init` 之前**。
写成 `gdflow.py --project P init --godot G` 会报 `unrecognized arguments`。

init 会做：备份 project.godot → 铺 `addons/godot_mcp/` → 铺 `.gdmcp/bin/gdmcp.exe` →
铺埋点 `scripts/debug_ring.gd` → 改 project.godot（启用插件 + 注册 autoload）→
注册到 manager → 分配 MCP 端口（portBase 19080 起）→ 拉起 headless 实例。

### 4. 验收

```bash
python gdflow.py --project "<工程绝对路径>" doctor     # 七项全 [OK]
curl -s -X POST http://127.0.0.1:19080/mcp -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}'
```
期望返回 `serverInfo.name = godot-native-mcp`。端口从 `curl http://127.0.0.1:17890/api/state` 的
`projects[].port` 读，不要硬编码。

### 5. 注册到 IDE 的 MCP 配置

`~/.workbuddy/mcp.json`（WorkBuddy）加一项：

```json
"godot": { "type": "streamableHttp", "url": "http://127.0.0.1:19080/mcp" }
```

⚠ 写入后**不会自动生效**——需用户到连接器管理页右上角自定义连接器入口，对新服务器点「信任」。
（注意：仓库若自带 `addons/godot_ai` 插件，它自动配置写的是 `~/.codebuddy/mcp.json`，另一套路径。）

## 常用命令

| 用途 | 命令 |
|---|---|
| 跑 / 停 | `gdflow run` / `gdflow stop`（stop 会清僵尸进程） |
| 验证 | `gdflow check` / `validate` / `smoke` / `selftest` |
| 属性读写 | `gdflow setprop` / `getprop` |
| 调试 | `gdflow dump` / `shot` / `call` |
| 资产导入 | `gdflow import`（停实例 → headless 导入 → 起实例） |
| 安全改配置 | `gdflow projstop` → 改 → `gdflow projstart`；`gdflow guard` 做快照 |

## 必知坑（完整版见 `<toolkit>/docs/pitfalls.md`）

1. **物理回调里切场景 → 游戏进程挂死**（帧冻结、无报错、debugger 桥还活着）→ 一律 `call_deferred()`
2. **属性设值返回 success ≠ 生效** → 读回验证是铁律；Vector2/Color 用 JSON 对象格式，不用 `"(x,y)"`
3. **编辑器开着直接改 project.godot 会被回写覆盖**（实测踩过 3 次）→ 先 `projstop`
4. `stop` 只断会话会留僵尸游戏进程 → 用 `gdflow stop`
5. manager 跑在会被回收的终端里 → 用 DETACHED / 独立后台进程
6. 新 PNG 需要导入元数据才能进 SpriteFrames/TileSet；测试资产用 `GradientTexture2D` 可零导入
7. AnimationLibrary 的 `.tres` 不落数据 → 动画内嵌到 `.tscn` 的 sub_resource

### autoload 与 headless 测试（GDScript 通用，不只本工具链）

8. **autoload 名与 `class_name` 同名 → `Class "X" hides an autoload singleton`**，脚本加载失败。
   去掉 `class_name` 又会让别的脚本报 `Cannot find member "x" in base "res://autoload/x.gd"`。
   → 命名规则：autoload 用业务名，class_name 加角色后缀（`Signals`/`SignalBus`）。
   **常量不要做 autoload**，做成静态类（`class_name GameConsts` + 纯 const）三种模式都能访问。
9. **`--script` headless 模式下 autoload 不注入全局标识符**（节点在 root 下但编译器不认）。
   直接写 `Signals.xxx` 连编译都过不去 → 用 `root.get_node_or_null("Signals") as SignalBus`。
   autoload 之间也不要用全局名互相访问（同样会编译失败，症状是"脚本挂载为 null"，极难定位）。
10. **测试逻辑不能写在 `_initialize()`**：覆写它会导致 autoload 不被创建，
    且 `super._initialize()` 报 "parent class' virtual function hasn't been defined"。
    → 写在 `_process()` 里，用 `_done` 标志跑一次。
11. 新建脚本后 `class_name` 不会立即进全局类缓存 → 先跑一次 `gdflow import` 再跑测试，
    否则报 `Identifier "X" not declared`。

## 实测记录

2026-10-03 部署到 `<data_drive>:/<apps_root>\spotlight`（Godot 4.7.2 + 空工程 `game/`）：
doctor 七项全 OK，MCP 端口 19080，30 个工具（create_node / update_node_property /
read_script / run_project / get_editor_logs / execute_editor_script …）。
