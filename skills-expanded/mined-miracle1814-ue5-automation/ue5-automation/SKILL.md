# UE5.1 自动化工具 — 使用手册

> **Skill 名称：** `ue5-automation`  
>
> ### ⚡ 30 秒路由（先读这里，再跳章节）
> | 你的处境 | 直接跳 |
> |---|---|
> | 第一次给项目装这个工具 | `docs/QUICKSTART.md`（人类用户 10 分钟上手指南） |
> | 要**读懂**一个蓝图 | §3.1 分析模式 |
> | 要**从零建**蓝图 | §3.2 → §3.7（整图写入是写图主路径，先 search 后 apply） |
> | 蓝图**编译报错** | §3.6 修复 SOP（诊断 → 按错误修 → 收敛看 `compiled`） |
> | 要改**已有**蓝图 | §3.5 增量修改（大改用 apply_graph，小改动逐节点工具） |
> | 要**验证结果**（截图/运行时） | §3.8 视觉自检 SOP |
> | **每个多步任务必做** | §3.9 任务上报（`task_begin` → 干活 → `task_end`） |
> | 用户说"撤回/不要了" | §3.9 末段 任务级撤销（`agent_undo_status` → `agent_undo`） |
> | 要证明**行为真的生效** | §3.10 行为验证（`verify_behavior`：读运行时属性 + 截图） |
> | 要批量搬资产 / 撤销资产 | §3.11 资产治理（`batch_asset_ops` / `rollback_task_assets`） |
> | 改 DataTable / 大图读省 token | §3.12 DataTable + `fields` 字段裁剪 |
> | 要 CI 可消费的验收证据 | §3.13 场景化验收（`verify_scenario` + JUnit） |
> | 多 Agent 抢同一资产 / 重试防重复写 | §3.14 会话锁 + 幂等键 + 回执 |
> | 撞到已知坑 | `docs/pitfalls.md`（P01–P19 蓝图陷阱 + B1–B19 构建/真机实录） |
>
> ### 🧰 工具目录（v4.8 修正：默认全量 31）
> `tools/list` **默认返回全部 34 个工具**（能力完整、可发现性优先）：
> 蓝图读写/整图写入/编译诊断/截图/PIE/日志/材质/UMG/资产/任务/撤销等。
>
> 为什么改了：v4.3 曾按「4 天调用日志里 31 个只用了 12 个」把默认目录收窄到 16 ——
> 这是统计错误（样本小、场景偏，只能说明未测到，不能说明无价值）。
>
> **按需收窄（可选）**：`UE5_MCP_PROFILE=core` → 18 个核心；
> `UE5_MCP_PROFILE=gateway` → 12 个入口（读/查/写/编译/截图/验证/任务收尾）。
> 旧变量 `UE5_MCP_CORE_TOOLS=1` / `UE5_MCP_GATEWAY=1` 仍兼容。默认仍全量。
>
> 无论目录怎么显示，`ue5_execute_command` 都可透传 **101 条白名单命令**——
> 目录控制的是「发现成本」，不是「能力边界」。
  
> **版本：** v1.14（多 Agent 锁/幂等 + 场景安全 + AnimBP 只读 · v6.5） · v1.13（安全硬化 · v6.4） · v1.6（工具目录恢复全量 · v4.8） · v1.5（管理端视觉刷新 · v4.7） · v1.4（结构化编译诊断 · v4.6） · v1.3（任务级撤销 + 5.8 自启修复 · v4.5） · v1.2（保存闭环 + 死循环保护 + 高危确认 · T-20261025-VERIFY · 双引擎真机验证与发布收敛：UE 5.1.1 + 5.8.2 全主路径实测通过；任务日志 `task_begin/step/end`（白名单 78→84、MCP 工具 27→31）+ 管理端 v3 任务指挥台；GT 队列直呼替代 C++ 跳板（5.8 UFUNCTION 拒非 GT）；投影矩阵轴重映射修复（真值对照 <1e-3）；5.1/5.8 中文编译错误行双变体提取；`debug_reflect` 反射探针；发布验证记录见 `docs/VERIFICATION-RELEASE-3.9.md`）
> **分层阅读（v4.6）：** 本文件只保留「速查 + 硬规则」；详细走查在
> `docs/reference/`（modes / graph-apply / compile-fix / visual-check /
> task-reporting / cpp-api / version-history）。历史版本记录见
> [reference/version-history.md](docs/reference/version-history.md)。


---

## 一、技能概述

### 1.1 一句话定位

**面向 UE5.1 的多智能体自动化管线** — 读取蓝图、自动编写蓝图、日志报错诊断、项目架构评估，四合一开发辅助工具。

### 1.2 四类场景

| 场景 | 你只需要 | 你会得到 |
|:---|:---|:---|
| **🔍 蓝图资产梳理** | 给一个蓝图路径 | 完整分析报告：变量清单、节点拓扑、Mermaid 流程图、引用资产、关联蓝图、优化建议 |
| **🏗️ 快速搭建原型** | 用自然语言描述功能 | 自动创建蓝图骨架（资产 + 变量 + 组件 + 接口），编译验证通过 |
| **🩺 报错排查** | 贴一段 UE 日志 | 根因定位 + 修复方案 + 可自动修复项直接修复 |
| **📐 架构评审** | 给项目根目录 | 全项目扫描 → 架构评估报告 + 按严重程度排序的问题清单 |

### 1.3 谁在背后工作

```
用户 ──→ maintainer（总调度） ──→ 判定模式 ──→ 分派任务
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         dev（引擎交互）  vision（截图识别）  docs-writer（报告输出）
         Python/Bridge    图像/OCR后备    文档/格式化
```

---

## 二、前置依赖

### 2.1 你必须具备的环境

| 依赖项 | 版本/说明 | 检查方式 |
|:---|:---|:---|
| **Unreal Engine** | **5.1.x 开箱即用**（随包 DLL 实测 5.1.1）；5.2–5.5 需重编译 bridge；5.6+ 未验证 | `python scripts\check_ue_version.py`（30 秒只读自检） |
| **UE Python 插件** | `Python Editor Script Plugin` 已启用 | UE 菜单 → Edit → Plugins → 搜索 "Python" → 确认已勾选 |
| **Remote Execution** | `Editor Preferences → Python → Enable Remote Execution` 已勾选 | 不依赖固定端口，使用 UDP 多播自动发现 |
| **ue_send.py** | Agent 与 UE 的通信脚本 | 放在 workspace/scripts/ 或通过 `UE_SEND_PATH` 指定 |
| **C++ Bridge 插件** | 解锁蓝图节点级操作（✅ 已就绪 · 双引擎 DLL（5.1 1,048,576 B / 5.8 901,632 B，2026-10-25 编译）· 源码头文件提供编辑器级 UFUNCTION） | 现已可用；`bridge/BlueprintPythonBridge/` 完整包（DLL+头文件+uplugin），5.8 预编译见 `bridge/prebuilt-5.8/` |

### 2.2 Bridge 通信架构（混合通道）

```
┌──────────────────────────────────────────────────────────┐
│            Agent 侧                │     UE5 侧           │
│                                    │                      │
│  ┌─ 读通道 ──────────────────────────────────────────┐  │
│  │ ue5_runner.py read/health                          │  │
│  │   → ue_send.py ── UDP 多播发现 ──▶ Remote Execution│  │
│  │     (不阻塞 GameThread, 适合读取/查询)              │  │
│  └────────────────────────────────────────────────────┘  │
│                                    │                      │
│  ┌─ 写通道 ──────────────────────────────────────────┐  │
│  │ ue5_runner.py build/connect                        │  │
│  │   → HTTP POST ────────────────▶ ue5_bridge.py      │  │
│  │     (FastAPI :8889, 后台运行, 不卡 GameThread)      │  │
│  │     → unreal Python API + BlueprintPythonBridge    │  │
│  │     (创建资产 / 添加节点 / 连线 / 编译)             │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

> **混合通道说明：** 
> - **读/健康检查** → `ue_send` (UDP) 直发 Python 命令，轻量快速，不启动服务。
> - **写/创建/连线** → `ue5_bridge` HTTP 服务 (端口 8889)。`ue5_runner.py build` 自动检测并远程启动 bridge（通过 `ensure_http_bridge()`），无需手动启动。
> - **为什么分通道：** ue_send 基于 `remote_execution`，写操作可能阻塞 GameThread 导致 UE 卡顿。HTTP bridge 在后台线程运行，写入操作通过 tick worker 异步调度，不影响编辑器响应。

### 2.3 C++ Bridge API 清单（UFUNCTION 全量 · 详见 reference）

桥的 C++ 入口覆盖节点/引脚/变量/组件/蓝图生命周期/截图/事务/结构化诊断。
**日常不需要背这张表**：Python 命令层（101 条白名单）已封装可读错误；
要确认某个 API 在本机 DLL 是否可用，直接查 `/diag` 的 `all_methods`。

完整清单（签名 + 用途）见 [reference/cpp-api.md](docs/reference/cpp-api.md)。

### 2.4 安全说明

**混合通道安全策略：**
- **读通道 (ue_send)**：走 UE `PythonScriptPlugin` 的 Remote Execution —— UDP 多播，同网段无鉴权。**v6.1 起默认关闭**；确认网络可信后设 `UE5_ALLOW_REMOTE_EXEC=1` 才启用。日常读请走 HTTP 桥 `read_*`（127.0.0.1 + token）。
- **日志读取 (v6.4)**：`logs_read.log_file` 只允许项目日志 / `Saved/Logs` / 系统临时目录；
  越界路径拒绝（防任意文件读取）。场景 JUnit 输出同样有目录白名单。
- **写通道 (HTTP bridge)**：仅监听 `127.0.0.1:8889`，不对外暴露。需 `X-Skill-Token` 头认证 —— **token 无"默认值 test123"**：bridge 首次启动时随机生成并落盘 `%APPDATA%\ue5_bridge\token`（环境变量 `UE5_BRIDGE_TOKEN` 可覆盖，env 优先于文件；`UE5_BRIDGE_TOKEN_FILE`
可指定自定义 token 文件路径，测试/多实例隔离用）；调用方经 `ue5_runner` 自动读取，手动调用时读该文件。CORS 仅允许本地来源。
- **⚠️ T-20260727-C03 · Mermaid 渲染安全**：`mermaid_render.py` 的 L2 在线渲染（`allow_external=True`）会将 Mermaid 代码通过 HTTPS GET 发送到第三方服务 `mermaid.ink`。若代码含项目敏感信息（蓝图函数名、类名、架构细节），存在数据外泄风险。**生产环境建议只使用 L1 (mmdc) 本地渲染**，确保 `allow_external=False`（默认值，已安全）。

> **Agent 侧注意：** Python 调用示例：
> ```python
> from ue5_runner import UE5Runner
> runner = UE5Runner()
> 
> # 读取（走 ue_send）
> runner.read("/Game/Blueprints/BP_Test")
> runner.health()
> 
> # 创建/连线（走 HTTP bridge，自动检测并启动）
> runner.build({...})      # 蓝图创建 + 变量 + 事件 + 函数 + 连线 + 编译
> runner.connect(...)       # 引脚连线
> ```

### 2.5 部署清单（首次使用）

> 🚀 **新机器/新宿主机首选 `scripts/init.py` 薄执行器初始化**（默认 dry-run 只读；产出**建议稿**须人工确认才生效）：
> - 第 1 步 探测预览：`python scripts/init.py`（dry-run 只读，不落盘）
> - 第 2 步 落盘建议稿：`python scripts/init.py --apply`
>   - 自动能力探测（list_agents API → agent.json → 系统提示词三级链）
>   - 自动定位 UE 引擎/项目 + 校验 Bridge 插件源（deploy.py 复用）
>   - 产出 `output/role_assignments.yaml`（角色分配）+ `output/init_report.md`（health 自检）
>   - 自动语义分配 → `status: proposed`（**建议稿，未生效**）
> - 第 3 步 **人工确认门**（建议稿生效为 confirmed 二选一）：
>   - `python scripts/init.py --apply --assign <agent_id>=<role> ...`（显式指派核心角色）
>   - 或手编 `output/role_assignments.yaml` 后 `python scripts/init.py --reconcile --apply`
> - ℹ️ single_agent 环境（≤1 enabled agent）确定性指派宿主 `all_in_one` → 自动 confirmed，无需人工通道
> - 非破坏：不删文件、不建自启服务；详细见 DEPLOY.md「新机器初始化」章节

| 步骤 | 操作 | 负责人 |
|:---|:---|:---|
| 0 | 初始化：`python scripts/init.py`（dry-run 预览）→ `python scripts/init.py --apply` 落盘建议稿（proposed）→ 人工确认门：`--assign` 或手编 yaml 后 `--reconcile --apply` 生效（confirmed） | maintainer自动执行 |
| 1 | 确认 UE 已安装（**随包桥 DLL 仅实测 5.1.x**；其他版本先跑 `python scripts/check_ue_version.py` 并见 `UE_VERSION_GUIDE.md`），`Python Editor Script Plugin` 已启用 | 你 |
| 2 | 确认 `Editor Preferences → Python → Enable Remote Execution` 已勾选 | 你 |
| 3 | 连通性测试：`python scripts/ue5_runner.py health` | maintainer自动执行 |
| 4 | 部署 Bridge 插件：init 报告 verify=通过时可 `--apply` 自动部署；否则按 DEPLOY.md 手动拷贝/编译 | 你/maintainer |
| 5 | 重启 UE5 编辑器，验证插件已加载（Edit → Plugins → 搜索 "BlueprintPythonBridge"） | 你 |

---

## 三、四种模式入口

### 3.1 分析模式 — 读懂一个蓝图

`read_blueprint{level:"L1"|"L2"|"full"}` → 概览/节点/连线。**先 L1 再 L2**，
不要一上来拉全图（token 成本）。完整走查见
[reference/modes.md](docs/reference/modes.md)。

### 3.2 创建模式 — 搭一个蓝图骨架

`build_blueprint{bp_name, pkg, parent, vars, comps, interfaces, compile_after}`
→ 资产 + 变量/组件 + 初始事件；**写逻辑走 §3.7**（不要逐节点搭）。
详见 [reference/modes.md](docs/reference/modes.md)。

### 3.3 诊断模式 — 查一个报错

`compile_and_diagnose` → 读 `errors`（`node_guid` 优先）→ 按 §3.6 修。
只读命令不会改蓝图。详见 [reference/modes.md](docs/reference/modes.md)。

### 3.4 优化模式 — 评估整个项目

`list_assets` + 复杂度/风险盘点 → 报告。完整流程见
[reference/modes.md](docs/reference/modes.md)。

### 3.5 增量修改模式 — 编辑已有蓝图

手术式改图：`set_pin_default_value` / `connect_pins` / `disconnect_pin` /
`delete_node`；**大改仍用 §3.7 整图写入**。完整命令与示例见
[reference/modes.md](docs/reference/modes.md)。

### 3.6 编译修复 SOP（agent 必须遵守）

**循环**：`compile_and_diagnose` → 按 `errors` 定位（`node_guid` 优先）→ 修 →
再编译。**收敛只看 `compiled`**（`errors` 非空 ≠ 没修好）。

- v4.6 优先 `structured:true`：`errors_scope=compiler_results_log`、
  `may_be_stale=false`、`node_guid` 来自 token（权威）。
  `structured:false` = 旧 DLL 回退日志正则，行为同 v4.5。
- 同一错误连续 2 轮修不好 → 停下来说明（别烧轮次）；编译类守卫放宽到 5 次。
- 报错文本 ≠ 根因：先看 `pitfall_ref`/`fix_hint`（命中已知坑时），再自己判断；
  未命中是 `CompileError.Unclassified`，不编造分类。
- 改完 `save_asset`（或让 `task_end` 自动保存）。

错误 JSON 字段、完整示例、错误码见
[reference/compile-fix.md](docs/reference/compile-fix.md)。

### 3.7 整图声明式写入 — 写图主路径（agent 必须遵守）

**"Never build a graph one node at a time"**：逻辑搭建用 `apply_graph` 一次写整张图；
逐节点工具只做手术式微调。

**SOP**：`search_blueprint_nodes`（拿签名）→ 写 GraphSpec → `apply_graph`
→ 看 `verified` → 编译失败走 §3.6。

**GraphSpec 要点**：

- 节点 `{id, kind: event|function|flow|variable_get|variable_set, target, class?, pos?}`
- 连线 `{"from":"id.pin","to":"id.pin"}`（id 不含点）
- 默认值 `{"id.pin":"value"}`（**对象**，不是数组）
- 目标图非空必须显式 `replace=true`（先 read 再决定；MCP 层需 `confirm=true`）

完整字段、全部 kind 示例、布局与回滚语义见
[reference/graph-apply.md](docs/reference/graph-apply.md)。

### 3.8 视觉自检 SOP — 截图反馈闭环

改完**看得到的东西**（关卡/UMG/材质表现）才截图；纯逻辑改动用编译 + 读回即可。

1. `capture_viewport`（编辑器机位）或 `capture_pie`（PIE 画面）；
2. 需要标注时 `project_actors_to_screen`（与截图同机位同源）；
3. 落盘 `<项目>/Saved/Screenshots/ue5-automation/`，面板「画面」页同源；
4. PIE 未运行/窗口最小化 → fail-loud（绝不返回白图）。

机位参数、超时语义、标注规则见
[reference/visual-check.md](docs/reference/visual-check.md)。

### 3.9 任务上报 SOP（每个多步任务必做）

`task_begin`（goal + user_request + understanding/approach/steps）→ 干活 →
`task_end`（status + summary + lessons + deliverables + how_to_verify）。

- 关键工具调用（编译/整图写入/截图）自动记进度与证据，**不必逐步 task_step**；
  手动上报用于标记步骤完成/失败、写关键结论、附证据。
- `success` 需证据：全程无编译/写入/截图 → 面板标「未验证」（agent 自述）。
- `task_end` 自动保存本任务触碰过的资产（`auto_save`），并封口悬挂步骤。
- 同一时刻只能有一个任务；失败重试标同一 `step_id`；完成后必须 `task_end`。
- 用户说"撤回/不要了" → `agent_undo_status` → `agent_undo{count}`；
  遇用户操作会提前停，如实转述 `stopped_reason`；资产创建/删除不在撤销栈。

完整字段、证据配对写法、撤销边界见
[reference/task-reporting.md](docs/reference/task-reporting.md)。

> 账本记录太多/有测试噪声：`python scripts/task_cleanup.py`（默认 dry-run 预览）→
> `--apply`（先备份 `tasks-backup-<时间>/`，重写并重新编号；重启编辑器生效）。

### 3.10 行为验证 SOP — 证明"行为真的生效"（v4.9）

编译通过只证明图合法；要证明行为，必须读**运行时**状态。`verify_behavior`
把"读属性 → 比对 → 截图"合成一次调用：

```json
{"command": "verify_behavior", "params": {
  "actor_name": "BP_Door_1", "property_name": "state",
  "expected": "Open", "match": "exact",
  "world": "pie", "capture": true}}
```

- `world: "pie"`（默认）要求 PIE/Simulate 在跑；没跑会 fail-loud 并提示先 `pie_start`
  （5.1 用 `mode:"simulate"`；5.8 可用 `mode:"pie"`）；
- `match`: `exact`（默认，数值支持 `tolerance`）| `contains`（子串，忽略大小写）；
- 返回 `verified` 是唯一判据；`actual` / `expected` / `screenshot` 是证据；
- 断言失败 → `success=false` + `_fail_loud`（MCP `isError` 可见），不要无视；
- 截图失败**不**翻转 `verified`，只进 `warnings`（证据失败 ≠ 行为失败）。

**SOP**：`pie_start` → 触发行为（按键/移动/交互）→ `verify_behavior` →
`verified=false` 时按 §3.6 修图/改逻辑 → 重跑。**不要**用"编译通过 + 截图没报错"
替代属性断言——那只是"看起来对"。

> 查属性名：先 `get_actor_properties{property_name:""}` 列候选；
> 查不到就说明该状态没有可读属性，改用日志/计数器断言。

### 3.11 资产治理 SOP — 批量搬迁与任务级资产回滚（v5.0）

**批量重命名/搬迁**：`batch_asset_ops{items:[{from,to}], dry_run:true}`
先看预检计划（源是否存在/目标是否冲突）；确认后 `dry_run:false, confirm:true`。
目标已存在**不覆盖**；上限 50 条；成功以回读为准（目标存在且源消失）。

**任务级资产回滚**：`task_assets` 看账本 → `rollback_task_assets{confirm:true}`。

- 删除本任务**新建**的资产（蓝图/材质/UMG 创建自动记账）；
- 从删除前快照恢复本任务**删除**的资产（`delete_asset` 前自动备份）；
- 只动账本内资产；修改类资产请用 `agent_undo`（事务回滚）；
- 恢复是**文件级**：返回 `reload_required:true` 时，需重启编辑器或
  Content Browser 右键 Rescan（两引擎 Python 均未暴露 reload_asset）；
- 有失败项 → `success=false` + `_fail_loud`，不要谎报已恢复。

### 3.12 DataTable 与读结果裁剪（v6.0）

**DataTable**：

- `datatable_read{asset_path, limit, include_csv}` → 行名 + 行结构 + CSV
  （5.1 无 CSV 导出接口 → `csv_supported=false`，只给行名）；
- `datatable_write_csv{asset_path, csv, confirm:true}` → 覆盖行 + 保存 + 回读行名；
  CSV 必须与行结构匹配（表头用字段名）；
- `datatable_create{asset_path, row_struct}` → 新建表（行结构如
  `/Script/GameplayTags.GameplayTagTableRow`），用于脚手架/验证。

**读结果裁剪**：`read_blueprint` / `read_nodes` / `read_connections` 支持
`fields: ["title","guid","pos"]` —— 大图只取需要的字段，显著省 token。
顶层元数据（asset/world/errors）保留，不会把结构裁没。

**类能力探针**：`class_probe{names:[...]}` 只读检查 unreal 类/工厂/方法是否存在，
排查"这个引擎版本有没有这个 API"时先用它，别猜。

### 3.13 场景化验收 SOP（v6.2 · 独家）

`verify_scenario` 把「起 PIE → 等待 → 断言属性 → 日志匹配 → 截图 → 停 PIE」编成一条
可重复的场景，产出 **JUnit XML**（CI 可直接消费），面板「运行状况 → 验收场景」可见。

```json
{"command": "verify_scenario", "params": {
  "name": "door_opens",
  "start_pie": true, "pie_mode": "simulate",
  "steps": [
    {"type": "wait", "seconds": 0.5},
    {"type": "assert", "actor_name": "BP_Door_1", "property_name": "state",
     "expected": "Open", "match": "exact"},
    {"type": "log_contains", "pattern": "Portal entered", "timeout": 5},
    {"type": "screenshot", "out_path": "door_scenario.png"}
  ]}}
```

- 步骤上限 50；`verified` = 全部 assert/log/command 通过；失败即 `_fail_loud`；
- **必须在 HTTP 线程单独调用**（内部有等待/轮询）——放进 `editor_batch` 会报错；
- 5.1 用 `pie_mode:"simulate"`；5.8 可用 `"pie"`；
- JUnit 默认写到项目 `Saved/ue5-automation/scenarios/`，也可传 `junit_path`。
- **v6.5 安全**：`action` 写法与 `type` 等价；新增 `command` / `pie_start` /
  `pie_stop` 步骤；`delete_asset` / `agent_undo` / `batch_asset_ops` /
  `apply_graph{replace}` 等高危命令默认拒绝，需顶层 `allow_destructive=true`
  或步骤级 `allow_destructive=true`；场景内禁止递归 `verify_scenario` 和
  `editor_batch`；总超时 `timeout_s` 默认 300s（上限 1800s）。

推荐链：`apply_graph` → `compile_and_diagnose` → `verify_scenario` → `task_end`
→（需要时）`agent_undo` / `rollback_task_assets`。

### 3.14 变更回执与资产锁（v6.3）

**变更回执**：每次写操作（写图/建资产/删除/保存/批量/DataTable 等）的结果里带
`receipt`：

```json
{"id":"a1b2c3d4e5","command":"save_asset",
 "asset":"/Game/Blueprint/BP_X",
 "before":{"exists":true,"size":12345,"sha1":"…"},
 "after":{"exists":true,"size":12400,"sha1":"…"},
 "saved":true,"success":true,"verified":true}
```

- `saved=false` 表示文件指纹没变（可能只在内存，`task_end` 会自动保存）；
- 回执随任务账本持久化，面板「交付物」区显示最近 12 条（before → after 短指纹）；
- 它是“这次写入到底改了没有”的硬证据，不替代 `verified`（读回）。

**资产锁（多 Agent）**：同一资产同一时刻只允许一个任务写。

- owner = 当前 task_id；没有任务时为 `adhoc`，**单命令租约**（命令结束即释放）；
- 任务持有的锁在 `task_end` 释放（异常也释放）；TTL 默认 300s
  （`UE5_ASSET_LOCK_TTL` 可调）；
- 冲突返回 `category="asset_locked"`，带 owner 与剩余秒数——不要重试同资产，
  等对方收尾或换资产。面板「运行状况 → 资产锁」可见当前锁。

**显式会话锁（v6.5，多 Agent 无任务场景）**：

```json
{"command":"session_lock_acquire",
 "params":{"owner":"agentA","assets":["/Game/BP_X"],"ttl":600}}
{"command":"session_lock_status","params":{}}
{"command":"session_lock_release","params":{"owner":"agentA"}}
```

- 任务锁和会话锁**互相可见**：任务写会检查会话锁，会话抢锁也会检查任务锁；
- `force=true` 只抢占其他**会话**锁，不能抢任务锁（任务锁等 `task_end`）；
- 上限：全局 1024、单 owner 256、单次 200 资产、路径 512 字符；
- 面板 `locks` 带 `scope: task|session`。

**幂等键（v6.5）**：写命令可加 `idempotency_key`（顶层或 params 均可）：

```json
{"command":"apply_graph",
 "params":{"bp_path":"/Game/BP_X","graph_spec":{...}},
 "idempotency_key":"agentA-001"}
```

- 10 分钟内同 key + 同 command/params → 重放上次成功结果，带
  `idempotent_replay:true`；不会重复写；
- key 被复用到不同命令/参数 → `category="idempotency_conflict"`，换 key；
- 失败结果不缓存；>256KB 结果不缓存。

**回执查询**：`receipt_list{limit:20}` 返回最近写回执（倒序，上限 200），
字段含 `receipt_id` / `before` / `after` / `saved` / `idempotent_replay`。

**AnimBP 只读（v6.5）**：`animbp_probe{asset_path}` 看类/父类/骨骼/能力；
`animbp_read{asset_path,include_nodes,limit}` 枚举图/节点。读不到就
`_fail_loud`；**写入通道未开放**（需真实 AnimBP 资产验证后再开）。

---

---

## 四、输出物说明

### 4.1 报告文件清单

| 模式 | 输出文件 | 包含内容 |
|:---|:---|:---|
| 🔍 分析模式 | `📊 {safe_name}_analysis_{timestamp}.md` | 7 章：基本信息卡片 → 变量清单 → 节点拓扑 → Mermaid 流程图 → 引用资产 → 关联蓝图 → 优化建议（与 blueprint_reader.py:1069 实际命名一致） |
| 🏗️ 创建模式 | `🏗️ {蓝图名}_创建方案.md` | 方案概述 → Step-by-step 分解 → 预估产出 → 待确认项 |
| 🩺 诊断模式 | `🩺 诊断报告_{关联蓝图}.md` | 日志摘要 → 根因分析 → 修复方案（含优先级） → 操作步骤 |
| 📐 优化模式 | `📐 {项目名}_架构报告.md` | 整体结构 → 架构指标 → 问题清单（按严重程度） → 优化路线图 |
| ✏️ 增量修改模式 | `logs/blueprint_editor.jsonl` | 事务日志（每行 JSONL：操作类型/蓝图路径/参数/结果/耗时） + 即时 CLI 输出 |

### 4.2 流程图标准

所有报告中的 Mermaid 流程图统一使用 **emoji+中文标注标准**，详见 `templates/mermaid_tags.md` v1.0。

> 快速查阅标签：`🚀入口` `🔀分支` `🔄循环` `🏃移动` `🎯转换` `📦变量` `⚡性能热点` `❓未识别`

**mermaid l2_online 测试（开发端验证命令 · 需真实 UE 环境 + 源码仓库）：**

`run_tests.bat`（开发端测试启动器，**不随发布包**）`online` / `e2e` 模式**不含** mermaid 在线用例（`test_6_l2_online` 标记 `ue_online`）。开发侧需要验证 L2 在线渲染（`allow_external=True` → mermaid.ink）时，先 `cd` 到本 skill 根目录（`ue5-automation/`），再单独跑：

```cmd
cd <skill 源码根目录>  :: 开发端源码仓库内的 ue5-automation 根目录（发布包内无 tests\，本命令仅开发端可跑）
python -m pytest tests\test_mermaid_render_audit.py::test_6_l2_online -v --ue-online --timeout=90
```

> ⚠️ L2 在线渲染会向第三方 `mermaid.ink` 发送 Mermaid 代码，含项目敏感信息时慎用（见 §2.4 Mermaid 渲染安全）；默认 L1 (mmdc) 本地渲染。

### 4.3 报告语言约定

- **中文为主**，技术术语保留英文（如 CastTo、BeginPlay）
- 节点标签：`{emoji} {中文动词+对象}`，如 `⚔️ ApplyDamage 25`
- 问题分级：🔴阻断 → 🟡警告 → 🟢建议
- 不确定处标注 `⚠️ 待确认`，不强行下结论

---

## 五、边界与限制

### 5.1 版本能力矩阵

| 功能 | v0.1 | v0.2（SKILL-06 就绪） | v0.3（完整体） | v0.4（混合通道） | v0.7（增量修改） | v0.9（CPP-APIS） |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| 读取蓝图基本信息+变量 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 读取蓝图节点+连线 | ❌ | ✅ 59 API | ✅ | ✅ | ✅ | ✅ |
| 创建蓝图骨架（资产+变量+组件） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 自动连线节点 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 创建自定义事件/函数图 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 蓝图续写（在已有蓝图中添加节点） | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **修改节点参数（SetPinDefaultValue）** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **按标识连线（connect_pins_by_id）** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **断开连线（disconnect_pin / BreakPins）** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **删除节点（delete_node / RemoveNode）** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **事务快照 + 回滚** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **组件添加+属性设置（AddComponent→SetComponentProperty）** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **程序化读取变量（ReadVariables · 假阳性消除）** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| 诊断错误模式 | 15+ | 40+ | 40+ | 40+ | 40+ | 40+ |
| 架构统计+热力图 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 循环依赖检测 | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| 继承深度 / 接口分析 | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| 混合通道（读写分离） | — | — | — | ✅ | ✅ | ✅ |

> 注：当前 SKILL.md 版本为 v0.14；v0.10 / v0.11 未新增 Bridge API，能力面与 v0.9 列一致。表中「诊断错误模式」列的 `15+` / `40+` 为**早期预估口径**——截至 v0.13，`config\error_patterns.json` **实装 19 条**（PTN-001~019 · 与 `docs\pitfalls.md` P01–P19 同源），实际可用模式数以实装为准。

### 5.2 已知限制

| 限制 | 影响 | 缓解方式 |
|:---|:---|:---|
| 蓝图节点读取依赖 C++ Bridge | v0.1 无法生成节点拓扑和连线 | ✅ v0.2 已解决（Bridge API 覆盖 · 随包 DLL 提供编辑器级 UFUNCTION） |
| 蓝图创建不支持节点连线 | 创建后需手动连线 | ✅ v0.2 已解决（ConnectPins API） |
| 大型项目扫描可能超时 | 200+ 蓝图项目扫描 > 5 分钟 | 增量扫描（仅扫变更文件）；后台异步+进度推送 |
| 截图识别准确率非 100% | 复杂节点图可能误识别 | 输出标注识别置信度；低置信节点标记 `❓` |
| 模式 E 仅支持已有蓝图的节点级增量修改 | 不做整图重建、不能替代模式 B 从零创建 | 整图重建 / 新建蓝图 → 模式 B（§3.2 创建模式）；结构分析 → 模式 A |
| 模式 E 不支持「从已有蓝图复制节点逻辑」 | 无法把 A 蓝图节点组整体复制到 B 蓝图 | Bridge API（59 项）无复制/克隆接口（§2.3 / §5.1 能力矩阵无此能力）；需手动重建或改走模式 B |

### 5.3 不支持的场景

- ❌ UE4.x 项目（API 差异较大）
- ❌ 非 UE 引擎项目
- ❌ C++ 源码级操作（仅蓝图层面）
- ❌ 运行时/已打包游戏的操作（仅编辑器环境）

---

## 六、FAQ

### Q1：为什么创建蓝图后节点没有连线？
> **A：** v0.2 已通过 C++ Bridge（Bridge API）支持自动连线。`ConnectPins` API 可以连接任意两个引脚。如果连线失败，请确认 Bridge 插件已正确安装并加载。

### Q2：分析模式为什么看不到节点详情？
> **A：** v0.2 已解决。现在通过 C++ Bridge（`ListNodes` / `GetPinInfos` / `GetNodeConnections` 等 59 API）可直接读取节点、引脚、连线拓扑，不再需要截图识别降级方案。

### Q3：端口 8889 被占用了怎么办？
> **A：** HTTP bridge 默认监听 `127.0.0.1:8889`，仅用于写操作（build/connect）。如果端口被占用：
> 1. 在 UE Python Console 中启动时指定其他端口：`ue5_bridge.start(port=8890)`
> 2. Agent 侧调用时传 `--bridge-port 8890` 参数
> 3. 或者通过环境变量 `UE5_BRIDGE_PORT=8890` 设置
> 
> 读操作（health/read）走 ue_send，不受端口影响。

### Q4：支持 UE5.3 / 5.4 吗？
> **A：** 随包 DLL 只实测 UE 5.1.x，**5.2–5.5 需自行重编译 bridge**（架构可行、未逐版本实测），5.6+ 未验证。不要假设高版本直接可用 —— 按 `UE_VERSION_GUIDE.md` 路径 B/C 操作，或先跑 `python scripts\check_ue_version.py` 自检。遇到不兼容问题请贴报错日志进入诊断模式。

### Q5：分析一个蓝图要多久？
> **A：** L1 级（基本信息+变量）约 5-10 秒。L2/L3 级（节点+连线）视蓝图复杂度而定，简单蓝图 < 30 秒，200+ 节点的大蓝图可能需要 1-2 分钟。

### Q6：创建蓝图时出错了能回滚吗？
> **A：** 创建模式在执行前会出方案让你确认，确认后才会动手。如果执行中出错（如编译失败），**创建的资产不会被自动删除**（避免误删已有资产），会提示你手动处理并存留诊断报告。

### Q7：诊断模式会自动修改我的蓝图吗？
> **A：** 默认 `auto_fix=true` 会自动修复可安全修复的问题（如引用替换、接口补全）。如果你希望**只看诊断不动手**，请在触发时说明"只诊断不修复"或设置 `auto_fix=false`。

### Q8：我能自己照着流程手动搭建吗？
> **A：** 可以。创建模式的方案输出就是一份完整的操作清单，包含每个 Step 的具体操作（在哪右键 → 选什么菜单 → 填什么参数），你可以照着在 UE 编辑器中手动完成。

---

## 七、故障排查

### 7.1 通信失败（HTTP 超时 / Connection Refused）

| 排查步骤 | 操作 |
|:---|:---|
| 1 | 确认 UE5 编辑器已打开，Bridge 已在 Python Console 中启动（`import ue5_bridge; ue5_bridge.start()`） |
| 2 | 确认 Remote Execution 已开启：`Config/DefaultEngine.ini` → `[PythonScriptPlugin]` → `bRemoteExecution=true`（面板：Edit → Project Settings → Plugins → Python → ☑ Enable Remote Execution） |
| 3 | 自检（/health 需鉴权，浏览器裸访问只会 403，不代表 bridge 挂了）：`python scripts\ue5_runner.py health`；或 `curl -H "X-Skill-Token: <token>" http://127.0.0.1:8889/health`（token 见 §2.4） |
| 4 | 若无法访问 → 检查 fastapi/uvicorn 是否已安装到 UE5 的 Python 环境（见 DEPLOY.md §七 步骤 8） |
| 5 | 若端口已被占用 → `netstat -ano | findstr 8889` 查看占用进程 |

### 7.2 Python 插件不可用

| 排查步骤 | 操作 |
|:---|:---|
| 1 | UE → Edit → Plugins → 搜索 "Python" → 确认 `Python Editor Script Plugin` 已勾选 |
| 2 | 若未勾选 → 勾选后重启编辑器 |
| 3 | 若仍然不可用 → 检查 UE 安装目录 `Engine/Plugins/Experimental/PythonScriptPlugin` 是否存在 |

### 7.3 蓝图编译失败（创建模式）

| 错误现象 | 可能原因 | 解决 |
|:---|:---|:---|
| "Parent class not found" | 指定的父类不存在 | 确认父类路径是否正确 |
| "Variable type not recognized" | 变量类型拼写错误或类型不存在 | 检查类型名（如 `float` 非 `Float`） |
| "Interface not implemented" | 蓝图未实现接口的所有函数 | 在蓝图编辑器中手动补全接口函数 |

### 7.4 报告质量不满意

> 如果报告未达到预期，请在反馈中说明：① 哪部分不够详细 ② 需要什么额外的维度。docs-writer会调整模板和示例库。

---

## 八、相关文档

> 可复现检查：`python benchmark/run_offline.py`（离线）/ `python benchmark/live_smoke.py`（真机只读）
> 英文入口：根级 `README.en.md`；竞品/路线图类文档为内部资料，不随公开包分发。


| 文档 | 路径 | 说明 |
|:---|:---|:---|
| Mermaid 标签标准 | `templates/mermaid_tags.md` | 流程图 emoji+中文标注规范（24 标签+4 连线+5 色） |
| 分析报告模板 | `templates/analysis_report.md` | 7 章结构 + BP_EnemyController 示例 |
| 创建方案模板 | `templates/creation_plan.md` | 方案格式 + BP_PickupItem 示例 |
| 诊断报告模板 | `templates/diagnosis_report.md` | 诊断格式 + FInventoryItem 缺失示例 |
| 架构报告模板 | `templates/architecture_report.md` | 指标体系 + MyGame 项目示例 |
| 立项文档 | `./SKILL.md` | 完整技术架构、Agent 分工、模式用法（见本文件「一、技能概述」「二、前置依赖」「三、四种模式入口」等章节） |
| **增量修改引擎** | `scripts/blueprint_editor.py` | v0.7 新增：4 核心 API + freeze/execute/verify + 事务日志 |
| **Bridge 端点参考** | `scripts/ue5_bridge.py` | HTTP 端点清单（含 v0.7 新增 /disconnect /delete_node） |
| **已知陷阱清单** | `docs/pitfalls.md` | **19 个已知坑（P01–P19）**（ConnectPins 假阳性 / CDO 时序 / 线程安全 / **事件存在性误判漏建** / **同名节点定位** / **`/build` spec 字段名契约不一致** 等） |
| **质量门禁** | `docs/quality_gates.md` | 提交前质量门槛（⚠️ **仅源端 skill 目录，不随发布包分发**） |
| **预检清单** | `docs/preflight.md` | 运行前预检项（随包分发） |
| **v0.7 设计文档** | `output/UE-05-v07-blueprint_editor.md` | 增量修改模式的技术设计 + 测试计划（⚠️ **仅源端**，`output/` 不随发布包分发） |

---

> **手册版本 v2.0** | 角色分工疑问请对照 §1.3 或 init.py 生成的 role_assignments.yaml

## 附录 B：常见错误码

| 状态码 | 含义 | 最常见原因 | 解决 |
|:---|:---|:---|:---|
| **403** | Forbidden | 请求未带 `X-Skill-Token` 头，或令牌不匹配 | 读取 `%APPDATA%\ue5_bridge\token`（bridge 首启自动生成的随机 token），或两端统一设置 `UE5_BRIDGE_TOKEN`；**没有 test123 默认令牌**（见 §2.4） |
| **400** | Bad Request | 命令不在白名单 / 参数格式错误 | 检查命令拼写，参考「三、四种模式入口」各模式请求格式 |
| **500** | Internal Server Error | UE Python API 调用异常（如蓝图不存在、CDO 不可访问） | 查看 UE5 Python Console 输出的完整 traceback |
| **timeout** | 请求无响应 | UE5 编辑器未打开 / Bridge 未启动 / 端口被占用 | 走 §7.1 通信故障排查清单 |
