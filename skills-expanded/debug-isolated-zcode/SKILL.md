---
name: debug-isolated-zcode
description: 隔离 ZCode lab 的搭建、启动与故障诊断：lab/patch 工具用法、八层排查法与 K1-K31 踩坑索引。触发于 lab 搭建或启动异常、补丁 apply/restore/升级、插件不加载或 Stop 不触发、开关不生效、网关握手与 probeHost、MCP start_session 拒绝、侧栏面板与评论链路。
---

# 调试隔离 ZCode 环境

隔离 ZCode 环境 = 复制的运行包 + 独立数据根 + 进程级环境变量集。lab 内验证 Desktop/CLI/补丁/插件行为；日常安装、`~/.zcode` 与日常网关保持不动（日常安装自身的故障见 zcode-guide 系列）。

## 速查

| 项 | 值 |
| --- | --- |
| lab 工具 | `suian-zcode-common/local-only/lab.mjs`：setup / check / launch / report / teardown |
| 补丁工具 | `suian-zcode-common/local-only/patch.mjs`：status / prepare / apply / restore |
| 单一数据源 | `lab-env.mjs`（目录树、env 集、包字节身份）、`patch-env.mjs`（锚点、开关约定、退出码） |
| 宿主插件发现根 | `<lab>/storage/cli/plugins`（由 `ZCODE_STORAGE_DIR` 派生；cache + installed_plugins.json + data/） |
| 插件启用门槛 | `home/.zcode/cli/config.json` 的 `plugins.enabledPlugins[id]===true` |
| 网关 | lab 独用 17331 + 独立 config；日常 17329 常驻 relay，两套互不影响 |
| 网关健康 | `curl http://127.0.0.1:<lab端口>/health`；就绪看 `desktop_connected` / `desktop_ready` |
| 状态锚点 | `run-state.json`：主进程 PID、全部隔离 env、代理端口；读前剥 UTF-8 BOM |
| 日志 | lab 内 `logs/desktop.{out,err}.log`；流程日志在 worktree `.scratch/logs/`（不入库） |
| CDP | `launch --remote-debugging-port <port>`，目标列表 `/json/list` |
| 启动约定 | 始终传隔离 `--user-data-dir`；`--workspace` 渲染为 Desktop 的 `--open-workspace`；启动前按副本 exe 路径拒绝已有进程（即使无 run-state） |
| 受控模型 | 回环 OpenAI 兼容端点（本轮 18081）；调用锚点只记类型与长度 |
| 面板入口 | 侧栏"查看所有插件"→`个人`→插件卡片"打开"（推荐位依赖远端配置） |

## 排查方法论：八层收缩

按层走，**找到原因的那层停下**并记录证据；八层都干净时回到假设。

1. **进程层**：按 run-state 的 PID 与 exe 路径过滤进程（日常 Desktop 同名）。判据：主进程存活状态与子进程数明确。
2. **载体层**：确认页面由真实 Host 加载，并分清操作目标是 page / webview / iframe（K26）。判据：目标类型与页面内容对得上。
3. **日志层**：`desktop.err.log` 找**首次**错误条目与完整堆栈；`desktop.out.log` 看 `[main]`/`[host]` 生命周期、`rpc:call`、`[provider-config]`。判据：能指出首个异常条目。
4. **网络层**：按 PID 查 TCP 连接（回环 = 本地链路；外部 443 = 官方或 TUN 残留），对照 `/health` 两字段。判据：连接分类与就绪状态各有结论。
5. **配置层**：插件需同时满足发现根、安装记录、`enabledPlugins=true` 三项。判据：三项逐项确认，或用最小探针证明已加载（K19）。
6. **环境层**：`lab.mjs check` 核对实际解析路径，重点 `ZCODE_DATA_BASE_DIR` 语义（K4）与独立进程 HOME 注入（K15）。判据：check 全项通过或列出越界项。
7. **时序层**：开关、标志、provider 配置的求值时机 vs 创建时机（K5、K28）。判据：每个求值点都晚于其输入的创建点。
8. **归属层**：会话、策略、安装记录、恢复副本、评论状态只落 lab；源文件、恢复副本、评论是三份独立回执（K29）。判据：每份回执都有落点证据。

Windows 副本仍会自动注册当前用户的 `zcode:` 协议和右键菜单，数据目录隔离不覆盖这些注册。严格隔离需独立 Windows 用户或虚拟环境；同用户运行须事先备份并核对恢复（见 K13 的证据链接）。

"设置了变量"不等于"实际生效"——以 check 输出与日志中的实际路径为判据。

当前补丁为 v3：最终 WS 地址的两个 env 入口均受 URL 回环校验；setup 的完整还原同时恢复网关 relay 模式。旧 v2 证据保留历史口径，当前摘要、升级与负向原生验证见[开发集成总验收](../../../suian-zcode-app-mcp/docs/local-only/09-development-acceptance.md)。

## 坑索引

按症状查编号，详录见 [references/known-pitfalls.md](references/known-pitfalls.md)。

| 症状 | 坑 |
| --- | --- |
| 停在欢迎页 / 登录门禁 | K1、K28 |
| 复用凭据后解密失败 / 副本登录缓存被清除 | K31 |
| 进程启动即退出 | K10、K12 |
| 进程存活但无主窗口 | K13 |
| 远控不启动、`desktop_connected:false` | K5、K9 |
| 插件不加载 / Hook 不触发 | K19 |
| 找不到插件面板入口 | K25 |
| `start_session` 被拒（无可用 provider） | K18、K28 |
| 轮次失败、受控服务零调用 | K20、K28 |
| `probeHost` 报 Invalid workspace attachment | K17 |
| 网关健康检查失败 / 连不上 | K7、K15、K24 |
| 空闲后附着报协议错误、terminal-owner-ended | K30 |
| 网络证据判读（TUN 假象、官方连接判定） | K6 |
| 会话库 `unable to open database file` | K16 |
| 启动器静默失败 / JSON 解析错 | K2、K11 |
| 注入后 `node --check` 报语法错 | K10 |
| CDP 目标错乱、截图失败 | K11、K26 |
| 工具调用卡在审批 | K27 |
| 评论状态不可用 / 正文丢失 | K29 |
| 命名没发生 / 无 Stop 记录（失败轮） | K21 |
| title 安装报快捷方式失败 / 协议键被改 | K22 |
| 新实例转交给旧进程 / 重启无效 | K3、K23 |
| 环境变量"设了但没生效" | K4、K5、K15 |
| teardown 后配置丢失 / 残留 | K23 |
| 要在 lab 里跑 setup 端到端 runner | K14 |
| 子代理疑似失联 | K8 |

## 维护约定

每票收尾把新踩的坑按 K 编号追加到 `references/known-pitfalls.md`（症状 / 根因 / 解法 / 来源），并修正既有条目的待确认标注。只收"可复现动作 + 可指认证据"；工具行为以 `lab-env.mjs` / `patch-env.mjs` 源码为准。

本技能位于仓库 `.agents/skills/` 入库共享（ZCode 以 worktree 根的 `.agents/skills` 为兼容发现路径，同名时 `.zcode/skills` 优先）。
