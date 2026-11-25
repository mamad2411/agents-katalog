---
name: haoxu-agent
description: 通过 haoxu CLI 查询号续账号、稿件、存稿任务、发表任务、分组/标签/代理 IP/稿件分类/员工，支持公众号远端草稿箱与发表记录查询，以及账号元数据写操作（号主/备注、移组、设标签、分组/标签 CRUD）、代理写操作（代理库 CRUD/绑定/检测/Excel 导入、异步 Job）、统计刷新/账号检测/未读刷新（0.6.0）、稿件路径/链接导入（0.7.0）、存稿/发表写操作（0.8.0）、单篇稿件设封面（0.9.0）、公众号面板远端写（1.0.0）、远端草稿箱发表 from-drafts / from-first-drafts（1.1.0）与单篇设原文链接（1.2.0）。Use when the user asks to query or update HaoXu data, list accounts/manuscripts/draft tasks/publish tasks/groups/tags/ip-proxies/categories/employees, query WeChat MP drafts/published posts, delete/sync MP drafts, update MP published private, list/upload/delete MP images, patch account owner/remarks, move groups, set tags, manage proxies, bind proxy, test proxy, import proxies, detect account proxy, refresh account metrics, detect account, refresh unread, import manuscripts from paths or links, set manuscript cover, set manuscript source url, create/start/cancel/delete draft tasks, create/start publish tasks from batch draft, create publish tasks from drafts or first drafts, or mentions haoxu CLI / Agent Bridge.
---

# 号续 Agent（查询 + 账号元数据写 + 代理写 + 统计刷新）

用 Shell 执行全局命令 `haoxu`，经本机 Agent Bridge 查询或更新号续数据。**0.4.0** 起允许账号元数据与分组/标签写操作；**0.5.0** 起允许代理库写、账号绑定代理、**代理检测**与 Excel 导入（异步 Job）；**0.6.0** 起允许统计刷新、**账号检测**（非代理检测）与未读刷新；**0.7.0** 起允许本机路径（含 zip）与公众号链接导入稿件；**0.8.0** 起允许存稿 create/start/cancel/delete 与发表 from-batch-draft / start / start-batch / start-all-pending；**0.9.0** 起允许单篇稿件设封面（本机路径 / URL / 清除）；**1.0.0** 起允许公众号面板远端写（删草稿、草稿另存、已发表改私密、素材库 list/上传/删图）；**1.1.0** 起允许从远端草稿箱创建发表（`from-drafts` 默认只建、须 `--start` 开跑；`from-first-drafts` 创建后自动开跑）；**1.2.0** 起允许单篇稿件设原文链接（`--url` / `--clear`）。**不支持飞书导入**、批量设封面/原文链接 API、删发表任务、发表任务 UPDATE 等。

适用于任何能跑终端的 Agent（Cursor、Claude Code、Codex、WorkBuddy、QoderWork、QClaw、OpenClaw、Trae 等），不限单一产品。

**Announce at start:** 「我在用 haoxu-agent skill 查询/更新号续数据。」

## 前置条件

| 条件 | 说明 |
|------|------|
| 号续运行 | 桌面端已启动并保持运行 |
| Agent Bridge 已开启 | 主账号或子账号均可：设置 → Agent Bridge → 启用，状态为「运行中」（开关与 API Key 本机共用） |
| 桌面端版本 | 需含对应 Bridge 能力：账号元数据写 **0.4.0**；代理写与 Job **0.5.0**；统计刷新/账号检测/未读 **0.6.0**；稿件路径/链接导入 **0.7.0**；存稿/发表写 **0.8.0**；单篇设封面 **0.9.0**；公众号面板远端写 **1.0.0**；远端草稿箱发表 **1.1.0**；设原文链接 **1.2.0**（与 `@haoxu/cli` / `@haoxu/mcp` 同版本配套） |
| API Key | 在号续内生成；用 `haoxu auth set-key` 写入本机 |
| CLI 可用 | 已安装：`npm i -g @haoxu/cli@1.2.0`（或 `npx @haoxu/cli@1.2.0`） |
| 本 Skill | 推荐：`npx skills add montisan/skills --skill haoxu-agent -y -g`（见文末「安装本 Skill」） |

首次配置：

```bash
haoxu auth set-key
haoxu auth status --json
```

配置写入 `~/.haoxu/config.json`。默认 Bridge：`http://127.0.0.1:19321`。完整小白教程：仓库 `Desktop/docs/agent/haoxu-agent-guide.md` §1–§2。

## 通用约定（所有命令）

| 约定 | 说明 |
|------|------|
| `--json` | **强烈建议始终加上**：机器可读；Agent 解析优先用 JSON |
| `--page` / `--page-size` | 列表分页；省略则用 Bridge 默认。部分远端接口 `pageSize` **上限 20** |
| 多选 ID | CLI 用逗号分隔（`--group a,b`）；MCP/HTTP 用数组或逗号，视字段而定 |
| `--confirm` / `confirm: true` | **删除类**必填，否则 `400 VALIDATION_ERROR` |
| 本机绝对路径 | 稿件导入、设封面、素材上传等：路径须绝对路径，且**号续与 Agent 同机**可读 |
| `haoxu auth status` | 检查 `enabled`、登录用户；`readonly: false` 表示本阶段写能力已开放（勿因旧文档误判「只能读」） |
| 写后进度 | 存稿/发表 `start` **无 Job**：用 `draft-tasks get` / `publish-tasks get` 轮询 `status`；批量检测/导入返回 `jobId` → `jobs get` |

**Announce 后先跑：** `haoxu auth status --json`（确认 Bridge 通、已登录、`readonly` 为 `false`）。

## 能力边界

**允许（读）：** 查询账号与统计、稿件、存稿任务、发表任务、分组、标签、代理 IP、稿件分类、员工（主账号）、**公众号远端草稿箱与发表记录**。

**允许（写，0.4.0）：** 账号 `owner` / `remark1` / `remark2`、移组、设标签；分组与标签实体 CRUD。

**允许（写，0.5.0）：** 代理库 CRUD / 批量创建 / 移组 / 入库 test；账号绑定代理；无库连通性 test；单账号与批量「**代理检测**」（`proxy-detect`，非账号检测）；Excel 导入（异步 Job）。

**允许（写，0.6.0）：** 单账号与批量统计刷新、**账号检测**（`detect`，非 `proxy-detect`）、未读刷新。查统计仍用 `accounts list|get`，勿把 refresh 当查询接口。

**允许（写，0.7.0）：** 本机**绝对路径**（含 zip/docx/html/md/txt 等）与**公众号文章链接**导入稿件（同步返回 `{ imported, errors }`）。号续与 Agent **须同机**，路径须号续进程可读；Bridge 不弹文件对话框。**不支持飞书**、base64 上传或分类 CRUD。

**允许（写，0.8.0）：** 存稿任务 create/start/cancel/delete（create 可选 `--content-mode article|note`、`--start` / `start: true`；**默认 article 图文**；贴图用 `note`）；发表任务 from-batch-draft create、单条 start、start-batch、start-all-pending（create 可选定时 `schedule` 与 `--start`）。启动后**无 Job**，须轮询 `draft-tasks get` / `publish-tasks get` 查看 `status` 直至终态。

**允许（写，0.9.0）：** 单篇稿件设封面（`--file` 本机绝对路径 / `--url` HTTP(S) / `--clear` 清除；三选一互斥）。`--file` 须号续与 Agent **同机**可读；成功返回 `{ coverUrl: string | null }`。批量设封面由 Agent 循环调用，无专用批量 API。

**允许（写，1.2.0）：** 单篇稿件设原文链接（`--url` HTTP(S) / `--clear` 清除；二选一互斥）。成功返回 `{ sourceUrl: string | null }`。链接导入**不**自动填原文链接。批量由 Agent 循环调用，无专用批量 API。

**允许（写，1.0.0）：** 公众号面板远端写——删远端草稿（`mp-drafts-delete`，须 `--confirm`）；草稿另存到其他账号（`mp-drafts-sync`，全同步可能较久，可选 `--upload-material`）；已发表设/取消仅自己可见（`mp-published-private`，`--items` / `--items-file`）；素材库 list / 本机路径上传 / 删图（`mp-images`、`mp-images-upload`、`mp-images-delete`，上传路径须**绝对路径**且号续与 Agent **同机**；删图须 `--confirm` 与 `--group-ids`）。

**允许（写，1.1.0）：** 从远端草稿箱创建发表——指定草稿（`publish-tasks from-drafts`，`--drafts` / `--drafts-file`，可选定时与 `--start`）；各账号首条草稿（`publish-tasks from-first-drafts`，`--draft-type article|sticker`，**创建后自动开跑**）。可先 `accounts mp-drafts` 查 `platformDraftId`。

**禁止（不在范围）：** 飞书导入、删发表任务、发表任务 UPDATE、员工增删改、账号增删、批量设封面 API 等。

**删除须确认：** 删除分组/标签/代理节点/存稿任务/远端草稿/素材图必须 `--confirm`（CLI）或 `confirm: true`（MCP），否则 `400 VALIDATION_ERROR`。

**异步 Job：** Excel 导入、批量代理检测、批量统计刷新/账号检测/未读刷新返回 `jobId`；用 `haoxu jobs get <id>` 轮询。Job 存于号续进程内存，完成后约 **1 小时** TTL 自动清理；**号续退出或重启后 Job 不可恢复**（旧 jobId → 404）。

## 写操作权限（与 UI/IPC 一致）

| 操作 | 主账号 | 员工（可见账号） | 员工（不可见账号） |
|------|--------|------------------|-------------------|
| `PATCH` `owner` / `remark1` / `remark2` | ✅ | ✅（仅这三字段） | `404 NOT_FOUND` |
| `move-group` | ✅ | `403 FORBIDDEN` | `404` 若不可见，否则 `403` |
| `set-tags`（账号打标） | ✅（须会员标签额度） | ✅ 可见账号 + 会员额度 | `404` |
| 分组 create/update/delete | ✅ | `403` | — |
| 标签 create/update/delete | ✅（须会员额度） | ✅（须会员额度） | — |

会员不足写标签 → `403 FORBIDDEN`（如「请开通会员后再添加标签」）。

## 代理写操作权限（0.5.0，与 UI/IPC 一致）

| 操作 | 主账号 | 员工 |
|------|--------|------|
| 代理 create / batch-create | ✅ | ✅（分组须授权） |
| 代理 update | ✅ | 见 IPC（备注始终可；改 groupId 禁；其它字段须会员额度且节点在授权组） |
| 代理 delete / move-group | ✅ | ❌ `403` |
| 入库节点 test | ✅ | ✅ 且节点可见；不可见 → `404` |
| bind-proxy | ✅ | ✅ 账号可见 + managed 规则 |
| `proxy test`（无库） | ✅ | ✅ |
| 单账号 / 批量 proxy detect | ✅ | ✅ 仅可见账号 |
| Excel import | ✅ | ✅（同 IPC 导入权限） |
| 统计刷新 / 账号 detect / 未读 | ✅ | ✅ 可见账号 | 不可见 → `404` |
| import-paths / import-links | ✅ | ✅（对齐 IPC：会话 owner = userId） | — |
| set-cover | ✅ | ✅（对齐稿件导入：会话 owner = userId） | — |
| set-source-url | ✅ | ✅（对齐 set-cover） | — |

## 安装 CLI

```bash
npm install -g @haoxu/cli@1.2.0
haoxu --help
```

## 常用命令（请加 `--json`）

### 基础查询

```bash
haoxu auth status --json
haoxu accounts list --json
haoxu accounts get <账号ID> --json
haoxu manuscripts list --json
haoxu manuscripts get <稿件ID> --json --include content
haoxu draft-tasks list --json
haoxu draft-tasks get <任务ID> --json
haoxu publish-tasks list --json
haoxu publish-tasks get <任务ID> --json
```

### 新增域（0.2.0）

```bash
haoxu groups list --json
haoxu groups get <分组ID> --json
haoxu tags list --json
haoxu tags get <标签ID> --json
haoxu ip-proxies list --json
haoxu ip-proxies get <代理ID> --json
haoxu categories list --json
haoxu categories get <分类ID> --json
haoxu employees list --json    # 仅主账号
haoxu employees get <员工ID> --json
```

### 账号元数据写操作（0.4.0）

```bash
# 修改号主/备注（至少传 --owner / --remark1 / --remark2 之一）
haoxu accounts patch <id> --owner 张三 --json
haoxu accounts patch <id> --remark1 备注A --remark2 备注B --json

# 移组：--group 为分组 ID，或哨兵 ungrouped（移出分组）
haoxu accounts move-group <id> --group <groupId|ungrouped> --json

# 设标签：全量替换；逗号分隔 ID；--tags 传空字符串可清空
haoxu accounts set-tags <id> --tags t1,t2 --json

# 分组 CRUD（delete 须 --confirm）
haoxu groups create --name 新分组 [--description 说明] [--color '#1fc372'] [--sort 0] --json
haoxu groups update <id> [--name 改名] [--description ...] [--color ...] [--sort n] --json
haoxu groups delete <id> --confirm --json

# 标签 CRUD（delete 须 --confirm；创建/更新受会员额度限制）
haoxu tags create --name 新标签 [--color ...] [--sort n] --json
haoxu tags update <id> [--name 改名] [--color ...] [--sort n] --json
haoxu tags delete <id> --confirm --json
```

| 命令 | Flag / 参数 | 说明 |
|------|-------------|------|
| `accounts patch` | `--owner` / `--remark1` / `--remark2` | 字符串；至少一项；未传字段不改 |
| `accounts move-group` | `--group` | 分组 ID 或 `ungrouped`（必填） |
| `accounts set-tags` | `--tags` | 逗号分隔标签 ID；全量替换；可为空 |
| `groups create` | `--name`（必填）、`--description`、`--color`、`--sort` | 与 UI 分组字段对齐 |
| `groups\|tags delete` | `--confirm` | 必填 |

### 代理写操作（0.5.0）

```bash
# 创建 / 更新 / 删除（删除须 --confirm）
haoxu ip-proxies create --host 1.2.3.4 --port 1080 --type socks5 --label 节点A --json
haoxu ip-proxies update <id> --label 改名 --json
haoxu ip-proxies delete <id> --confirm --json

# 批量创建（JSON 文件含 items 数组）
haoxu ip-proxies batch-create --file ./proxies.json --json

# 移组
haoxu ip-proxies move-group --ids id1,id2 --group <groupId|ungrouped> --json

# 入库节点连通性 test（失败仍 200，状态写入 DTO）
haoxu ip-proxies test <id> --json

# Excel 导入（异步，返回 jobId）
haoxu ip-proxies import --file ./proxies.xlsx --group <groupId> --json
haoxu jobs get <jobId> --json

# 账号绑定代理
# --mode direct：直连（不绑库内代理）
# --mode managed：须 --ip-proxy-id；可选 --identity-reuse
# --mode custom：须 --payload-file（自定义代理 JSON，字段对齐 UI）
haoxu accounts bind-proxy --accounts a1,a2 --mode managed --ip-proxy-id <id> --json
haoxu accounts bind-proxy --accounts a1 --mode direct --json
haoxu accounts bind-proxy --accounts a1 --mode custom --payload-file ./proxy.json --json

# 单账号代理检测（对齐 UI「代理检测」；≠ accounts detect）
haoxu accounts proxy-detect <accountId> --json

# 批量代理检测（异步返回 jobId；--poll 自动轮询，间隔 1s，超时 120s）
haoxu accounts proxy-detect-batch --accounts a1,a2 --poll --json

# 无库连通性 test（不入库）
haoxu proxy test --host 1.2.3.4 --port 1080 --type socks5 [--username u] [--password p] --json
```

| 命令 | Flag | 说明 |
|------|------|------|
| `ip-proxies create` | `--host` `--port` `--type` | 必填；`type`: `socks5` \| `https` \| `http` |
| | `--label` `--region` `--username` `--password` `--group` | 可选 |
| `ip-proxies batch-create` | `--file` | JSON 文件，根对象含 `items` 数组 |
| `ip-proxies move-group` | `--ids` `--group` | 代理 ID 列表；目标分组或 `ungrouped` |
| `ip-proxies import` | `--file` `--group` | Excel；异步 → `jobId` |
| `accounts bind-proxy` | `--accounts` `--mode` | 必填；mode 见上 |
| | `--ip-proxy-id` / `--identity-reuse` / `--payload-file` | 依 mode |
| `proxy-detect-batch` | `--accounts` `--poll` | `--poll` 可选 |

### 统计刷新 / 账号检测 / 未读（0.6.0）

查统计仍用 `accounts list|get`；下列为触发刷新/检测的写操作。**账号检测**（`detect`）≠ **代理检测**（`proxy-detect`）。

```bash
# 单账号统计刷新（返回更新后的账号 DTO）
haoxu accounts refresh-metrics <id> [--no-force] --json

# 批量统计刷新（异步；省略 --accounts 则处理全部可见可刷新账号）
haoxu accounts refresh-metrics-batch [--accounts a1,a2] [--poll] [--json]

# 单账号检测（公众号有效性等）
haoxu accounts detect <id> [--no-force] --json

# 批量账号检测（异步）
haoxu accounts detect-batch [--accounts a1,a2] [--poll] [--json]

# 单账号未读刷新
haoxu accounts refresh-unread <id> [--no-force] --json

# 批量未读刷新（异步）
haoxu accounts refresh-unread-batch [--accounts a1,a2] [--poll] [--json]
```

默认 `force: true`；传 `--no-force` 时仅刷新符合自动策略的账号。批量 `--poll` 间隔 1s，超时 120s。

### 稿件导入（0.7.0）

路径须为**本机绝对路径**（如 `/Users/me/article.zip`）；号续与 Agent 同机，Bridge 直接读盘。**不支持飞书**。

```bash
# --paths：逗号分隔绝对路径（docx/html/md/txt/zip 等）
# --category：可选，已存在分类 ID（categories list）
# --strip-duplicate-title：可选，去重标题策略
haoxu manuscripts import-paths --paths /abs/a.docx,/abs/b.zip [--category <id>] [--strip-duplicate-title] --json

# --urls：逗号分隔公众号文章链接
haoxu manuscripts import-links --urls https://mp.weixin.qq.com/s/xxx,https://mp.weixin.qq.com/s/yyy [--category <id>] --json
```

同步返回 `{ imported, errors }`；部分失败仍 exit 0。不做分类 CRUD。

| Flag | 说明 |
|------|------|
| `--paths` / `--urls` | 必填（二选一命令）；逗号分隔 |
| `--category` | 可选分类 ID |
| `--strip-duplicate-title` | 仅 import-paths |

### 单篇稿件设封面（0.9.0）

`--file` / `--url` / `--clear` **三选一互斥**；`--file` 须绝对路径且同机可读。成功 `{ coverUrl: string | null }`（clear 时为 `null`）。无批量 API，循环调用即可。

```bash
haoxu manuscripts set-cover <稿件ID> --file /abs/cover.jpg --json
haoxu manuscripts set-cover <稿件ID> --url https://example.com/cover.png --json
haoxu manuscripts set-cover <稿件ID> --clear --json
```

### 单篇稿件设原文链接（1.2.0）

`--url` / `--clear` **二选一互斥**。成功 `{ sourceUrl: string | null }`。无批量 API；链接导入不自动写入。

```bash
haoxu manuscripts set-source-url <稿件ID> --url https://example.com/article --json
haoxu manuscripts set-source-url <稿件ID> --clear --json
haoxu manuscripts list --source-url unset --json
```

### 存稿 / 发表写操作（0.8.0 + 1.1.0 from-drafts）

复杂存稿配置优先 `--payload-file`（JSON 对齐 create body，可含 `start`；**payload 覆盖同名 CLI flags**）。启动后 fire-and-forget，**须轮询 GET** 直至终态。

```bash
# 创建存稿（可选 --start；默认 contentMode=article 图文）
# 贴图模式：--content-mode note（亦接受 sticker 别名）；或 payload 内 "contentMode":"note"
haoxu draft-tasks create --account <账号ID> --manuscripts m1,m2 [--content-mode article|note] [--payload-file ./draft.json] [--start] --json
haoxu draft-tasks create --account <账号ID> --manuscripts m1 --content-mode note --start --json
haoxu draft-tasks start <任务ID> --json
haoxu draft-tasks cancel <任务ID> --json
haoxu draft-tasks delete <任务ID> --confirm --json   # 删除须 --confirm
haoxu draft-tasks get <任务ID> --json                # 轮询 status

# 从已完成存稿创建发表（可选定时 + --start）
haoxu publish-tasks from-batch-draft --tasks d1,d2 \
  [--schedule-date <label> --schedule-hour <h> --schedule-minute <m>] [--start] --json

# 从远端草稿箱指定草稿创建发表（1.1.0）
# drafts 元素：{ accountId, platformDraftId, draftTitle }；--drafts 与 --drafts-file 互斥
# 默认只建任务；须 --start 才入队执行
haoxu publish-tasks from-drafts --drafts '[{"accountId":"a1","platformDraftId":"d1","draftTitle":"标题"}]' [--start] --json
haoxu publish-tasks from-drafts --drafts-file ./drafts.json \
  [--schedule-date 今天 --schedule-hour 8 --schedule-minute 0] [--start] --json

# 各账号远端草稿箱「首条」创建发表（1.1.0；创建后自动开跑，无 --start / 无 schedule）
# --draft-type: article=图文，sticker=贴图（对齐 UI 今日首条）
haoxu publish-tasks from-first-drafts --accounts a1,a2 --draft-type article --json

haoxu publish-tasks start <任务ID> --json
haoxu publish-tasks start-batch --ids p1,p2 --json
haoxu publish-tasks start-all-pending --json
haoxu publish-tasks get <任务ID> --json              # 轮询 status
```

| 命令 | Flag | 说明 |
|------|------|------|
| `draft-tasks create` | `--account` `--manuscripts` | 必填；稿件 ID 逗号分隔 |
| | `--content-mode` | 可选；`article`（默认图文）\| `note`（贴图；亦接受 `sticker`→note） |
| | `--payload-file` | 可选；完整 create body JSON，**覆盖**同名 flags（含 `contentMode`） |
| | `--start` | 可选；`true` 时创建后立即启动 |
| `draft-tasks delete` | `--confirm` | 必填 |
| `from-batch-draft` | `--tasks` | 存稿任务 ID 列表 |
| | `--schedule-date` `--schedule-hour` `--schedule-minute` | 须**三者同时**才定时；否则立即模式 |
| | `--start` | 可选；默认只建不跑 |
| `from-drafts` | `--drafts` \| `--drafts-file` | 互斥；JSON 数组非空 |
| | schedule 三件套、`--start` | 同 from-batch-draft |
| `from-first-drafts` | `--accounts` `--draft-type` | 必填；`article` \| `sticker`；**自动开跑** |
| `start-batch` | `--ids` | 发表任务 ID 列表 |

员工仅可操作**可见账号**下任务；不可见 → `404 NOT_FOUND`。账号离线/非公众号不可存稿 → `503 ACCOUNT_NOT_READY`。

响应 DTO **不含 password**；创建/更新代理请求体可含 password。

### 公众号远端草稿箱 / 已发表 / 素材库（读 0.3.0 + 写 1.0.0）

实时查询/操作微信公众平台，**非**号续本地任务表。须**目标账号在线**且已登录公众平台。草稿另存为**全同步**，可能较久。

```bash
# —— 读 ——
haoxu accounts list --quick-filter online --json          # 先找在线账号
haoxu accounts mp-drafts <账号ID> --q 关键词 --json
haoxu accounts mp-drafts <账号ID> --content-type note --json   # 贴图草稿
haoxu accounts mp-published <账号ID> --date-preset today --json
haoxu accounts mp-published <账号ID> --from 2026-07-01 --to 2026-07-17 --json
haoxu accounts mp-images <账号ID> [--group <id>] [--page n] [--page-size n] --json

# —— 写 ——
haoxu accounts mp-drafts-delete <账号ID> <draftId> --confirm --json
# --targets：另存目标账号 ID；--upload-material：同步时上传到目标素材库
haoxu accounts mp-drafts-sync <账号ID> <draftId> --targets id1,id2 [--upload-material] --json
# privateType: 1=仅自己可见，0=取消；--items 与 --items-file 互斥
haoxu accounts mp-published-private <账号ID> --items '[{"appmsgid":123,"itemidx":1,"privateType":1}]' --json
haoxu accounts mp-published-private <账号ID> --items-file ./private.json --json
haoxu accounts mp-images-upload <账号ID> --file /abs/image.jpg --json   # 须绝对路径、同机
# --ids 与 --group-ids 等长对应；须 --confirm
haoxu accounts mp-images-delete <账号ID> --ids 1,2 --group-ids 0,0 --confirm --json
```

#### `accounts mp-drafts`（读）

| Flag | 取值 |
|------|------|
| `--q` | 关键词（透传微信草稿搜索） |
| `--content-type` | `article`（默认）\| `note` |
| `--page` / `--page-size` | 分页（pageSize 上限 20） |

#### `accounts mp-published`（读）

| Flag | 取值 |
|------|------|
| `--q` | 关键词 |
| `--date-preset` | `today` \| `yesterday` \| `last_7_days` |
| `--from` / `--to` | `YYYY-MM-DD`，须成对；与 `--date-preset` **互斥** |
| `--page` / `--page-size` | 分页（pageSize 上限 20） |

**`scanExhausted`：** 带日期条件时 Bridge **有界跨页扫描**（最多 10 页）。若 `scanExhausted: true`，区间结果**可能不完整**——应缩小日期范围或告知用户。自然日按**号续桌面端本地时区**。

#### 写操作参数

| 命令 | Flag | 说明 |
|------|------|------|
| `mp-drafts-delete` | `--confirm` | 必填 |
| `mp-drafts-sync` | `--targets` | 必填；目标账号 ID 逗号分隔 |
| | `--upload-material` | 可选；默认 false |
| `mp-published-private` | `--items` \| `--items-file` | 互斥；元素含 `appmsgid`、`itemidx`、`privateType`（0\|1） |
| `mp-images` | `--group` `--page` `--page-size` | 可选；pageSize 上限 20 |
| `mp-images-upload` | `--file` | 必填；本机**绝对路径** |
| `mp-images-delete` | `--ids` `--group-ids` `--confirm` | 均必填；两列表等长对应 |

## 列表过滤（英文码，与 UI 对齐）

多选 ID 用**逗号分隔**（CLI 用 `--group a,b`；HTTP 用 `groupId=a,b`）。省略或空 = 不限。

### 账号 `accounts list`

| Flag | 取值 |
|------|------|
| `--group` | 分组 id；哨兵 `ungrouped`（未分组） |
| `--tag` | 标签 id；哨兵 `untagged`（未打标） |
| `--type` | `all` \| `official` \| `mini_program` |
| `--quick-filter` | `all` \| `online` \| `offline` \| `renewedToday` \| `notRenewedToday` \| `needsAttention` \| `withIp` \| `direct` |
| `--remark` | 备注筛选项字面值（逗号多选） |
| `--q` | 搜索 name/wxid/owner/remark |

```bash
haoxu accounts list --quick-filter online --group g1,g2 --json
haoxu accounts list --tag untagged --quick-filter needsAttention --json
```

### 稿件 `manuscripts list`

| Flag | 取值 |
|------|------|
| `--category` | 分类 id；哨兵 `uncategorized` |
| `--assigned` | `all` \| `assigned` \| `unassigned` |
| `--saved` | `all` \| `saved` \| `unsaved` |
| `--cover` | `all` \| `set` \| `unset` |
| `--source-url` | `all` \| `set` \| `unset` |
| `--q` | 搜索 title / sourceFileName |

```bash
haoxu manuscripts list --assigned unassigned --cover unset --source-url unset --json
```

### 存稿任务 `draft-tasks list`

| Flag | 取值 |
|------|------|
| `--status` | `all` \| `pending` \| `running` \| `completed` \| `failed`（`completed` **含** `partial_completed`） |
| `--content-type` | `all` \| `article` \| `note` |
| `--completed` | `all` \| `today` \| `yesterday` \| `last_3_days` |
| `--publish` | `all` \| `published` \| `unpublished` |
| `--q` | 搜索账号名 |

```bash
haoxu draft-tasks list --status completed --completed today --json
```

### 发表任务 `publish-tasks list`

| Flag | 取值 |
|------|------|
| `--status` | `all` \| `pending` \| `running` \| `failed` \| `published` \| `scheduled`（`scheduled` = UI「已定时」） |
| `--q` | 搜索账号名 |

```bash
haoxu publish-tasks list --status scheduled --json
```

### 代理 IP `ip-proxies list`

| Flag | 取值 |
|------|------|
| `--status` | `all` \| `healthy` \| `slow` \| `failed` |
| `--group` | 分组 id（逗号多选）；哨兵 `ungrouped` |
| `--q` | 搜索 label/host/username/remark/绑定账号名 |

## 员工列表权限

- **仅主账号（owner）**可查询 `employees list|get`
- 员工子账号调用 → Bridge 返回 **403 FORBIDDEN**
- 未登录号续 → **503 APP_NOT_READY**

## 退出码

`0` 成功 | `1` 业务/参数 | `2` 鉴权 | `3` 连接失败

## 错误排查

| 现象 | 处理 |
|------|------|
| Connection refused / exit 3 | 启动号续并启用 Agent Bridge |
| 401 / exit 2 | `haoxu auth set-key` 或重新生成 Key |
| 误以为「只读不可写」 | 看 `haoxu auth status --json`：`readonly` 应为 `false`；并确认桌面端含写能力（≥ 配套 1.2.0 Bridge）。旧桌面端写路由缺失时会 `404 未找到资源` |
| 503 APP_NOT_READY | 在号续内完成登录 |
| 503 ACCOUNT_NOT_READY | 目标账号离线或未登录公众平台 |
| 401 REMOTE_UNAUTHORIZED | 微信侧 session 失效，在号续内重新登录该账号 |
| 502 UPSTREAM_ERROR | 微信接口异常，稍后重试 |
| 403 FORBIDDEN（employees / move-group / groups / 代理 delete·move-group） | 需主账号登录 |
| 403 FORBIDDEN（tags / 代理 update 额度） | 会员额度不足 |
| 404 NOT_FOUND（mp-* / 不可见账号·代理） | 资源不存在或员工不可见 |
| 400 VALIDATION_ERROR（delete） | 删除须 `--confirm` / `confirm: true` |
| 404 NOT_FOUND（jobs） | jobId 不存在、已 TTL 清理，或号续已重启 |
| `haoxu: command not found` | `npm install -g @haoxu/cli@1.2.0` |
| 未知命令 / 过滤无效 | 升级桌面端与 CLI 至 1.2.0 |
| 路径不可读 / 导入失败 | 确认绝对路径、号续与 Agent 同机、文件扩展名支持 |

## MCP（可选，1.2.0）

`npx -y @haoxu/mcp@1.2.0`，与 CLI 共用 API Key。

| 工具 | 说明 |
|------|------|
| `haoxu_status` | Bridge 与登录状态 |
| `haoxu_list_accounts` / `haoxu_get_account` | 账号（含过滤参数） |
| `haoxu_list_manuscripts` / `haoxu_get_manuscript` | 稿件 |
| `haoxu_list_draft_tasks` / `haoxu_get_draft_task` | 存稿任务 |
| `haoxu_list_publish_tasks` / `haoxu_get_publish_task` | 发表任务 |
| `haoxu_list_groups` / `haoxu_get_group` | 分组 |
| `haoxu_list_tags` / `haoxu_get_tag` | 标签 |
| `haoxu_list_ip_proxies` / `haoxu_get_ip_proxy` | 代理 IP |
| `haoxu_list_categories` / `haoxu_get_category` | 稿件分类 |
| `haoxu_list_employees` / `haoxu_get_employee` | 员工（主账号） |
| `haoxu_list_mp_drafts` | 公众号远端草稿箱（`accountId` + `q` / `contentType` / 分页） |
| `haoxu_list_mp_published` | 公众号远端发表记录（`accountId` + `q` / `datePreset` / `from`+`to` / 分页） |
| `haoxu_delete_mp_draft` | 删除远端草稿（须 `confirm: true`） |
| `haoxu_sync_mp_draft` | 草稿另存到其他账号（全同步，可能较久） |
| `haoxu_update_mp_published_private` | 已发表设/取消仅自己可见 |
| `haoxu_list_mp_images` | 素材库图片列表 |
| `haoxu_upload_mp_image` | 上传素材（`filePath` 须本机绝对路径、同机可读） |
| `haoxu_delete_mp_images` | 删除素材图（须 `confirm: true` 与 `groupIds`） |
| `haoxu_patch_account` | 修改号主/备注 |
| `haoxu_move_account_group` | 移组 |
| `haoxu_set_account_tags` | 设标签（全量替换） |
| `haoxu_create_group` / `haoxu_update_group` / `haoxu_delete_group` | 分组 CRUD（delete 须 `confirm: true`） |
| `haoxu_create_tag` / `haoxu_update_tag` / `haoxu_delete_tag` | 标签 CRUD（delete 须 `confirm: true`） |
| `haoxu_create_ip_proxy` / `haoxu_update_ip_proxy` / `haoxu_delete_ip_proxy` | 代理 CRUD（delete 须 `confirm: true`） |
| `haoxu_batch_create_ip_proxies` / `haoxu_move_ip_proxies` | 批量创建 / 移组 |
| `haoxu_test_ip_proxy` | 入库节点 test |
| `haoxu_import_ip_proxies` | Excel 导入（异步，返回 `jobId`） |
| `haoxu_bind_accounts_proxy` | 账号绑定代理 |
| `haoxu_detect_account_proxy` / `haoxu_detect_account_proxy_batch` | 单账号 / 批量**代理**检测（批量异步） |
| `haoxu_refresh_account_metrics` / `haoxu_refresh_account_metrics_batch` | 单账号 / 批量统计刷新（批量异步） |
| `haoxu_detect_account` / `haoxu_detect_account_batch` | 单账号 / 批量**账号**检测（非代理；批量异步） |
| `haoxu_refresh_account_unread` / `haoxu_refresh_account_unread_batch` | 单账号 / 批量未读刷新（批量异步） |
| `haoxu_test_proxy_connectivity` / `haoxu_proxy_lookup_exit_ip` | 无库 test / 查出口 IP |
| `haoxu_get_job` | 查询异步 Job 状态 |
| `haoxu_import_manuscripts_from_paths` | 本机绝对路径导入稿件（同步 `{ imported, errors }`） |
| `haoxu_import_manuscripts_from_links` | 公众号链接导入稿件（同步 `{ imported, errors }`） |
| `haoxu_set_manuscript_cover` | 单篇设封面（`source`: local/url/clear；local 时 `filePath` 须本机绝对路径、同机可读） |
| `haoxu_set_manuscript_source_url` | 单篇设原文链接（`source`: url/clear；url 时须 `url`） |
| `haoxu_create_batch_draft_task` | 创建存稿任务（可选 `start`） |
| `haoxu_start_batch_draft_task` | 启动存稿任务 |
| `haoxu_cancel_batch_draft_task` | 取消存稿任务 |
| `haoxu_delete_batch_draft_task` | 删除存稿任务（须 `confirm: true`） |
| `haoxu_create_publish_tasks_from_batch_draft` | 从存稿创建发表（可选 `schedule`、`start`） |
| `haoxu_create_publish_tasks_from_drafts` | 从远端草稿箱指定草稿创建发表（可选 `schedule`；默认只建，`start=true` 才开跑） |
| `haoxu_create_publish_tasks_from_first_drafts` | 从各账号首条远端草稿创建发表（创建后自动开跑） |
| `haoxu_start_publish_task` | 启动单条发表任务 |
| `haoxu_start_publish_tasks_batch` | 批量启动发表任务 |
| `haoxu_start_all_pending_publish_tasks` | 启动全部可见待执行发表任务 |

### MCP 写工具关键参数（与 CLI 对齐）

| 工具 | 关键参数 |
|------|----------|
| `haoxu_patch_account` | `id`；`owner` / `remark1` / `remark2` 至少一 |
| `haoxu_move_account_group` | `id`；`groupId` 或 `ungrouped` |
| `haoxu_set_account_tags` | `id`；`tagIds: string[]`（全量替换，可空） |
| `haoxu_*_delete_*` / `haoxu_delete_*` | 须 `confirm: true` |
| `haoxu_bind_accounts_proxy` | `accountIds`；`mode`: direct\|managed\|custom；managed 须 `ipProxyId` |
| `haoxu_set_manuscript_cover` | `id`；`source`: local\|url\|clear；local 须 `filePath` 绝对路径 |
| `haoxu_create_batch_draft_task` | 对齐存稿 create body；可选 `contentMode`: article\|note（默认 article；贴图用 note）；可选 `start: true` |
| `haoxu_create_publish_tasks_from_batch_draft` | `batchDraftTaskIds`；可选 `schedule`、`start` |
| `haoxu_create_publish_tasks_from_drafts` | `drafts: [{ accountId, platformDraftId, draftTitle }]`；可选 `schedule`、`start`（默认只建） |
| `haoxu_create_publish_tasks_from_first_drafts` | `accountIds`；`draftType`: article\|sticker（**自动开跑**） |
| `haoxu_sync_mp_draft` | `accountId`；`draftId`；`targetAccountIds`；可选 `uploadToMaterial` |
| `haoxu_update_mp_published_private` | `accountId`；`items: [{ appmsgid, itemidx, privateType }]` |
| `haoxu_upload_mp_image` | `accountId`；`filePath` 绝对路径 |
| `haoxu_delete_mp_images` | `accountId`；`imageIds`；`groupIds`；`confirm: true` |

MCP 参数名与 HTTP query/body 对齐（如 `quickFilter`、`groupId`、`assigned`、`completed`、`status`、`contentType`、`datePreset`）。异步工具返回 `jobId` → `haoxu_get_job`；存稿/发表 start 后用 `haoxu_get_draft_task` / `haoxu_get_publish_task` 轮询。

## 安装本 Skill / CLI / MCP

**推荐（全局 Skill）：**

```bash
npx skills add montisan/skills --skill haoxu-agent -y -g
npm install -g @haoxu/cli@1.2.0
# 可选 MCP：
npm install -g @haoxu/mcp@1.2.0
```

装完后请用户：号续 → 设置 → Agent Bridge → 启用 → 生成 Key → `haoxu auth set-key` → `haoxu auth status --json`。然后**重启当前 Agent / 开新对话**。

**Agent 代装：** 用户可把教程 `docs/agent/haoxu-agent-guide.md` §2 发给**任意**能执行终端的 Agent（含 WorkBuddy、QoderWork、QClaw、OpenClaw、Trae 等）；或由你直接执行上述命令后协助配置 Key。完整小白步骤见该教程 §1。

**备选（从 npm 包复制 Skill）：** 拷到当前产品要求的 skills 目录，例如：

```bash
mkdir -p ~/.claude/skills/haoxu-agent   # 或 .cursor/skills/haoxu-agent 等
cp "$(npm root -g)/@haoxu/cli/skills/haoxu-agent/SKILL.md" ~/.claude/skills/haoxu-agent/
```
