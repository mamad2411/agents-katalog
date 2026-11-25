---
name: mebular-memory
description: 通过 Mebular MCP 使用跨设备、离线可用的图式长期记忆：先查后写、类型化节点、时效与关系、隐私红线。
whenToUse: 需要记住或复用用户偏好/事实/会话/技能，跨会话或跨设备共享 Agent 记忆，或按语义/关系检索既有记忆时。
---

# Mebular Memory

Mebular 是一个本地优先的分布式图记忆层。通过 MCP 工具读写记忆，行为规约见 `MEMORY_POLICY.md`。

它是**叠加**基建：与既有 memory provider **共存、不接管**（不替代、不改造；不双写同一事实）——分工与导入口径见 `MEMORY_POLICY.md` §8。

## 何时使用

- 用户透露稳定偏好、事实或约束，且未来会复用时。
- 需要回顾历史会话、任务过程或既有技能时。
- 需要按语义（同义不同词）或关系检索既有记忆时。

## 工具（13 个）

| 工具 | 用途 |
|------|------|
| `memory_write` / `memory_write_batch` | 写入一/多条记忆（fact / preference / episode / observation / skill） |
| `memory_query` | 语义（配置向量索引）/关键词召回，可按类型与过滤 |
| `memory_search` | 关键词检索，可选一跳关系 |
| `memory_profile` | 用户偏好与属性画像 |
| `memory_skills` | 技能列表（按分类/关键词/标签） |
| `memory_history` | 会话历史 |
| `memory_graph` | 从某节点遍历关系图 |
| `memory_import` | 经适配器导入异构来源（kv / markdown / …） |
| `memory_status` | 设备/网络/计数/状态哈希/开关 |
| `memory_sync` | 连接对端并等待一次同步（需 network.enabled） |
| `memory_delete` | 删除记忆（写墓碑，随图同步；删除后默认不再召回）。**何时用**：内容已过时/错误/不该共享，且希望各端一起不再召回；不可逆（对端旧快照无法强制回收）。需 `memory.admin`。 |
| `memory_archive` | 归档 / 解除归档记忆（`metadata.archivedAt`，随图同步、可逆）。**何时用**：内容暂时不该参与召回但**将来可能有用**（先归档而非删除）；`archived: false` 解除。需 `memory.write`。 |

查询类工具（`memory_query` / `memory_search` / `memory_profile` / `memory_skills` / `memory_history` / `memory_graph`）默认**不返回已归档**；需要时传 `includeArchived: true`（已删除的墓碑始终不召回）。

## 工作流

1. **先查后写**：写入前用 `memory_query`/`memory_search` 查重。
2. **选对类型**：稳定事实→`fact`；用户偏好→`preference`；会话/任务过程→`episode`；可复用步骤→`skill`；观察→`observation`。
3. **标注时效**：有有效期的用 `metadata.expiresAt`；过期事实不当现状。
4. **表达关系**：`metadata.relatedTo` 精确关联已存在节点。
5. **诚实回答**：召回为空就如实说明，不要臆造记忆。

完整行为规约见 `MEMORY_POLICY.md`。

## 接入

本 Skill 目录附各客户端 MCP 接入片段（见 `mcp/`）；`scripts/install.mjs` 可将本 Skill（含 `mcp/` 片段）安装到常见 Skill 目录。

支持的文件夹式 Skill 客户端（`--global` 只写**已检测到**的客户端）：OpenCode/OpenChamber `~/.config/opencode/skills`、Hermes `~/.hermes/skills`、Claude Code `~/.claude/skills`、Cursor `~/.cursor/skills`、DeepSeek Harness `~/.agents/skills`；Claude Desktop 无文件夹式自动目录（用 zip/UI 上传）。

**会话里没有 Mebular 工具时的第一步**（每次会话）：

1. **先看 App/守护是否已在跑**：读 `HOME_DIR="${MEBULAR_HOME:-$HOME/.mebular}"` 下的 `runtime.json`，用其中的 `host`/`port` 请求 `/healthz`；200 → 已在跑，直接接入，**不要因为 `command -v mebular` 失败就再装一套 CLI**。
2. **home 不存在时**先按 SETUP §3/§5（从 App 主界面新建/加入），**不要跑 `status`**（它会在默认 home 自举身份材料，见 §0.2）。
3. 没有 runtime/healthz 且 home 已存在：CLI 可用 → `MEBULAR_HOME="$HOME_DIR" mebular status` 看 `storeLock`；未跑按 [`SETUP.md`](./SETUP.md) §0.3 拉起。没有 CLI → 按 SETUP §2 安装。
4. 生成当前客户端的接入片段：`mebular print-config --client <opencode|claude|cursor|dsh|generic>`
   （远程形态追加 `--url https://<host>/mcp`），合入客户端 MCP 配置（先备份）并**重载客户端**。
5. 用 `memory_status` 验证工具面可用；失败排查见 [`SETUP.md`](./SETUP.md) §0.4。

完整剧本（幂等判定 / 拉起 / 接入 / 红线）见 [`SETUP.md`](./SETUP.md) §0「会话内接入」。

## 部署 / 加入 / 邀请

**部署一台新机器、加入别人的 Mebular、生成邀请（二维码 + 令牌）**：见 [`SETUP.md`](./SETUP.md)
——面向 Agent 的可执行剧本（前置检查 → 安装 CLI（钉 SHA）→ `fleet quickstart` / `fleet join --qr` →
`mebular doctor --net` 自检 → 失败恢复 → 安全红线）。
