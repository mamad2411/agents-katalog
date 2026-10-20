---
name: decc-desrpc
description: Query and manage DECC DES-RPC Callee Channels, data rules, and Caller Channel configurations for cross-region RPC routing. Use whenever the user asks about DES-RPC channels, cross-region RPC routing, caller/callee channel configuration, DECC platform settings, or wants to check how RPC traffic routes between services across regions (sites/VGeos). Also trigger when the user mentions DECC, DES-RPC, needs to understand caller-to-callee routing relationships, wants to create a new DES-RPC channel, wants to create data rules (RPC methods / HTTP paths) under a channel, wants to create/update/submit data versions, or wants to do field-level "打标" (DES annotation) on an RPC method before audit.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# DECC DES-RPC Skill

操作 DECC 平台的 DES-RPC 通道、数据规则、版本与字段打标。用 caller / callee / method / VRegion
等业务元信息查询，无需记忆内部 ID。

## When to Use

- 查询 DES-RPC 通道（Caller Channel / Callee Channel）
- 查看通道下的数据规则（RPC Methods / HTTP Paths）
- 检查跨区域 Caller → Callee 路由
- 给 RPC 方法做 DES 打标并提交审核（**核心场景**）
- 查 Texas/TikTok Catalog 名字 → code 映射，或自检 reviewer 拒绝模板（`fetch_meta`）
- 写操作（`create_*` / `update_*` / `parse_idl` / `tag_fields` / `submit_*`）调用前都需向用户明确确认

## 核心概念

| 概念 | 说明 | 参数 |
|---|---|---|
| **Caller Channel** | 调用方（发起 RPC）的通道 | `caller` |
| **Callee Channel** | 被调用方通道 | `callee` / `channel` |
| **Method** | RPC 方法或 HTTP Path（数据规则名） | `method` / `data_name` |
| **Site** | 部署站点（ROW-TT / EU / US / ...） | `caller_site` / `callee_site` |
| **VGeo** | 虚拟地理区域 | `vgeo` |
| **Scenario** | 跨境传输场景，决定 direction_pairs mesh | `scenario` |

DES-RPC `scenario` 取值：

| 值 | 含义 | 自动 direction_pairs |
|---|---|---|
| `2` | Texas 跨境 | `ROW <> US` |
| `3` | EU 跨境 | `EU <> ROW` |
| `4` | CN-RoW 跨境 | `CN <> ROW-TT` |
| `5` | TT-NonTT 跨境 | `NonTT <> ROW-TT` |
| `9` | TT_TTP 三方 | `EU / US / ROW-TT` 全互通（6 方向） |
| `13` | BOE-i18n RoW | `BOE <> i18n` |

> 同一个 method 可以在不同 scenario 下各挂一条 data rule，分别走各自方向。

## Command Format

```bash
gdpa-cli run decc-desrpc --input '<json>'
```

## ⚠️ Pre-submit Review Protocol（务必遵守）

`submit_data_version` 触发的 **DES 审核单（Audit Ticket）** 通常 **1–2 周以上**才能跑完，
被打回需要新建草稿重打、重提，代价很高。所以代码层强制了**两阶段确认**：

1. **第一次调用** `submit_data_version`（不传 `confirmed` 或 `confirmed: false`）
   → Skill 不会真的提交；它会拉取版本详情 + json_schema，返回结构化 **`preview`**：
   - `data_id` / `version` / `scenario`
   - `channel` / `method`
   - `description` / `reason` / `explanation`（reviewer 第一眼看的文本）
   - `direction_pairs`（包括来源是 `saved_extra` 还是 `derived_from_scenario`）
   - `schema_summary`：叶子字段总数、各项打标完成率、缺 description / catalog / reason 的字段清单
   - `next_command`：直接可拷贝的"加 confirmed:true"复用命令

2. **必须把整个 `preview` 完整呈现给用户**（不要总结、不要省略字段路径），并以
   "确认提交吗？需要看到 `yes / 提交 / submit` 之类明确同意，再继续"的形式询问。

3. 用户**显式同意**后，再次调用同一 `data_id` + `version` + `scenario`，加 `confirmed: true`。
   只有这一次才会真正调用 DECC 的 `SubmitDataVersion`。

不要为了"省一步"自己默认 `confirmed: true`。代码层守卫和文档守卫都存在的目的是：
**human-in-the-loop 提单不可绕过**。

## ⚠️ 打标硬规则（务必遵守，违反即返工）

**核心立场是 IDL-driven**：每个字段的 5 项标注必须有可追溯的依据，agent 不要自由发挥。
来源按优先级分三档——**有 IDL 注解就抠注解；注解缺失就基于 IDL 设计背景与仓库上下文
推断（并记录推断依据）；都没有就回去补 IDL，不要凭字段名瞎猜**。

| 字段 | ✅ 第一优先：IDL 注解 | 🟡 第二优先：IDL 设计背景 / 仓库上下文 | ❌ 反模式（禁止） |
|---|---|---|---|
| **`description`**（字段语义） | field 上方 `// 英文注释` → `(field.desc = "...")` → 最近祖先的 comment | struct 设计目的（从 `// @doc` / 设计文档 / PR 描述）、相邻字段语义、调用方代码用法、字段命名约定 | 凭字段名硬猜并写一段无依据的通用话术 |
| **`catalog`**（Texas Data Catalog） | struct 级 `compliance.message.field_default.texas`；字段级 `compliance.field.texas`；名字 → code 用 `fetch_meta` 查 | 同 struct 内已有注解字段的语义类比；用 `fetch_meta query=...` 按字段语义对应到 catalog name 后取 code | 凭"字段名看起来像什么"猜 catalog code，忽略 struct 上写得清清楚楚的注解 |
| **`reason`**（互通原因） | method/struct 上方 `// @sync_reason: ...` | method 的业务用途（从仓库 README / commit message / 调用链推断），写成"X 服务部署在 A，需要调用 B 服务的 Y 数据用于 Z" | 套话（"Required for cross-region X in Y mesh"），把审批单号塞进 reason |
| **`entity`**（TikTok Data Catalog） | 业务侧选定（IDL 暂无对应注解）；按 scenario 默认表查 `fetch_meta {catalog_type: "row_tt"}` | 同 channel 内同业务方向已通过的 data version 复用 | 跟着 catalog 漂移；瞎填 |

> **走第二档时的纪律**：把推断依据写进版本的 `explanation` 里（"description 来自 struct
> 设计文档 §2.3 / 调用方 X.go:42 的使用方式"），让审核员能复核。**第二档不是"自由发挥"
> 的开闸**——它要求你能给出可验证的引用，agent 也要能解释自己是怎么得出这个值的。
> 如果连第二档的依据都凑不出来，就回去补 IDL 注解，再来打标。

> **⚠️ 全局 catalog/entity/description 不会覆盖已有值**。
> 如果版本是 `create_data_version upstream_version=1` 继承来的（上一版打标已存在），
> 全局参数只对**空字段**生效，旧 `tag` 纹丝不动。**修正打标必须用 `field_overrides`
> 逐路径写**，否则你看到的是"我改了但 schema 还是老的"。
>
> **⚠️ map/list 容器里的 value struct 不会继承父 struct 的 catalog**。
> 如果某个字段是 `map<string, ValueStruct>` 或 `list<ValueStruct>`，且 `ValueStruct`
> 在 IDL 里有自己的 `compliance.message.field_default.texas`，那 ValueStruct 的
> 叶子字段在打标时**只会拿到顶层 `catalog` 全局默认值**（错的），审核会被打回。
>
> 两种写法都可以正确处理（任选其一）：
>
> **写法 A（推荐）：用 `/*` 前缀 override 一次性下沉**
> 路径以 `/*` 结尾时，规则会应用到该路径下的**所有后代叶子**，效果等价于给
> ValueStruct 整棵子树设了"struct 级 catalog 默认"。具体某个叶子若需要不同的值，
> 再用精确路径 override 覆盖即可（精确 > 前缀 > 全局）。
>
> ```jsonc
> // IDL: map<string, BuyerInfo> buyer_info  (BuyerInfo 注解 'User Data|Account Basic Info' → 1.5.1)
> "field_overrides": {
>   "_response.buyer_info{*}/*":         {"catalog": "1.5.1"},                                  // 整个子树
>   "_response.buyer_info{*}.user_id":   {"description": "Buyer TikTok user id"},               // 叶子级 description
>   "_response.buyer_info{*}.country":   {"description": "Buyer registered country (ISO-2)"}
> }
> ```
>
> **写法 B：每个叶子单独写**（路径多时啰嗦，但显式）
>
> ```jsonc
> "field_overrides": {
>   "_response.buyer_info{*}.user_id":    {"description": "...", "catalog": "1.5.1"},
>   "_response.buyer_info{*}.created_at": {"description": "...", "catalog": "1.5.1"},
>   "_response.buyer_info{*}.country":    {"description": "...", "catalog": "1.5.1"}
> }
> ```

## 端到端"打标" Workflow（IDL-driven）

```
0. 读 IDL（.thrift / .proto）
   └─ 提取每个 field 的 // 英文注释 / (field.desc = "...") / compliance.* / @sync_reason
   └─ 在内存里组装出 field_path → {description, catalog?, reason?} 映射

1. list_data channel=<channel>
   └─ data 不存在 → create_data（自动 LoadIDL，scenario 必填）
   └─ data 存在但 latestVersionState != draft → create_data_version

2. parse_idl                    # 仅生成 json_schema 结构，**不打标**
3. tag_fields                   # 用第 0 步算出来的 field_overrides 一次性写满
   ├─ catalog: <struct 级默认 catalog code>     # 来自 compliance.message.field_default.texas
   ├─ entity:  <业务选定的 TikTok catalog code> # 用 fetch_meta 查可选项
   ├─ reason:  <@sync_reason>                   # method 上没有时 fallback 到 file 顶部
   └─ field_overrides: 字段级精准下发（path → description/catalog/...）

4. update_data_version          # 设版本级 description / reason / explanation / direction_pairs
5. submit_data_version          # ① 不带 confirmed → 返回 preview
                                # ② 用户审阅 → 加 confirmed:true
```

> **如果 IDL 注解不全**（按优先级处理，不要直接跳到瞎猜）：
> 1. **首选**：patch IDL 把缺失的 `// 注释` / `compliance.*` / `@sync_reason` 补齐再来打标。
>    业务方维护一次 IDL，下游所有打标链路都自动得到正确 description / catalog / reason。
> 2. **次选**（IDL 短期内无法修改、或字段语义已经在别处定义清楚）：基于 **IDL 设计背景 +
>    仓库上下文** 推断，并把推断依据写进 `explanation`。可参考的来源：
>    - struct/method 所在的 `.thrift` / `.proto` 文件顶部的设计说明、`README.md`、相邻
>      已有 compliance 注解的字段；
>    - 业务仓库里 **该字段的写入侧 / 读取侧代码**（grep 字段名，看 setter/getter 怎么用）；
>    - 设计文档、PR/MR 描述、commit message 里说明该 RPC 的用途；
>    - 同 channel 中同业务方向 **已审核通过** 的相似 data version（用 `list_data` 找）；
>    - `fetch_meta` 拿到的 catalog enumeration——按字段实际语义找最贴近的 catalog name，再取它的 code。
> 3. **底线**：如果两档都给不出可引用的依据，**回去补 IDL，不要让 agent 用"看起来合理"
>    的兜底值占位**。审核员看到 description/catalog 与字段语义对不上、又没有 explanation
>    解释推断依据，会直接拒。

> Step 2/3 也可以让 `update_data_version` 配合 `auto_create_if_no_draft: true` 处理 draft 缺失。

## Actions（按使用顺序）

### list_channels — 查通道列表

```bash
gdpa-cli run decc-desrpc --input '{"action": "list_channels", "name": "desrpc.test", "vgeo": "ROW-TT"}'
```

### list_data — 查通道下的数据规则

```bash
gdpa-cli run decc-desrpc --input '{"action": "list_data", "channel": "desrpc.test.http_server"}'
```

返回带 `latest_version_states.<vgeo>.latestVersionState`，决定下一步是否要 create_data_version。

### list_data_versions — 查版本列表

```bash
# 通过 channel + data_name 自动解析 data_id
gdpa-cli run decc-desrpc --input '{"action": "list_data_versions", "channel": "desrpc.stability.thrift_server", "data_name": "GetItemV3"}'

# 通过 data_id 直接查
gdpa-cli run decc-desrpc --input '{"action": "list_data_versions", "data_id": "7628400000000000001"}'
```

返回字段含 `version` / `states` / `description` / `reason` / `direction_pairs`。
不需要文本字段时可加 `enrich: false` 跳过 N 次详情请求加速。

> 认证：`/openapi/data_version/list` 个人 JWT 没权限，Skill 内部自动改用 service-account
> Bearer Token（与 `parse_idl` 复用）。enrich 阶段使用个人 JWT，无需额外配置。

### query_caller_channel — 查 Caller Channel 配置

```bash
# 仅指定 callee，列出所有 caller
gdpa-cli run decc-desrpc --input '{"action": "query_caller_channel", "callee": "desrpc.test.http_server"}'

# 完整筛选
gdpa-cli run decc-desrpc --input '{"action": "query_caller_channel", "caller": "desrpc.test.client", "callee": "desrpc.test.http_server", "method": "PUT:/hotsoon/item/path/_like/", "caller_site": "ROW-TT", "callee_site": "EU"}'
```

### create_channel ⚠️ 写

调用前向用户确认。会通过 psm-info 验证 PSM：
- PSM 存在 → `channel_type` 可选
- PSM 不存在 → 必须传 `channel_type`（2=RPC_PSM, 3=HTTP_PSM, 4=HTTP_DOMAIN）
- DOMAIN（4）→ 还要 `psm_list`

`scenario` 必填（除非用户明确说"先不声明场景"，可传 `skip_scenario: true`）。

```bash
gdpa-cli run decc-desrpc --input '{
  "action": "create_channel",
  "name": "desrpc.myteam.myservice",
  "description": "My service channel",
  "owners": ["your.username"],
  "scenario": [9]
}'
```

### create_data ⚠️ 写

在指定 channel 下创建 data rule（RPC method / HTTP path）。会自动 LoadIDL 并附带初始 DataVersion。

`scenario` 选择规则：
- channel 只有 1 个 scenario → 自动继承
- channel 有多个 scenario → 必须显式指定其一

```bash
gdpa-cli run decc-desrpc --input '{
  "action": "create_data",
  "channel": "desrpc.myteam.myservice",
  "data_name": "Echo",
  "owners": ["your.username"],
  "scenario": 9
}'
```

### create_data_version ⚠️ 写

```bash
gdpa-cli run decc-desrpc --input '{"action": "create_data_version", "channel": "desrpc.myteam.myservice", "data_name": "Echo"}'
# 基于已有版本 inherit
gdpa-cli run decc-desrpc --input '{"action": "create_data_version", "data_id": "...", "upstream_version": 1}'
```

### update_data_version ⚠️ 写

只能更新 draft（state=2）状态的版本。Agent 会先 fetch detail 检查：
- latest 是 draft → 直接更新
- 否则报错；可传 `auto_create_if_no_draft: true` 让 agent 自动建草稿再更新

```bash
gdpa-cli run decc-desrpc --input '{
  "action": "update_data_version",
  "channel": "desrpc.myteam.myservice",
  "data_name": "Echo",
  "version": 1,
  "description": "...",
  "reason": "...",
  "direction_pairs": [{"source_vgeo": "ROW-TT", "target_vgeo": "EU"}]
}'
```

### load_idl — 从 BAM 拉 IDL

```bash
gdpa-cli run decc-desrpc --input '{"action": "load_idl", "channel": "desrpc.stability.thrift_server", "data_name": "GetItemV3"}'
```

> BAM 找不到 IDL → 先与业务方确认**是否要在 BAM 上新建 IDL 版本**，新建后再回来。

### parse_idl ⚠️ 写

把 IDL 写入草稿版本，生成 `json_schema` 结构。**只生成结构，不打标**。

```bash
gdpa-cli run decc-desrpc --input '{"action": "parse_idl", "channel": "desrpc.stability.thrift_server", "data_name": "GetItemV3"}'
```

> 认证：`/openapi/schema/idl/parse` 个人 JWT 没权限，Skill 内部 hardcode 了 service-account
> Bearer Token。失效时改 `agent.go` 的 `serviceAccountBearerToken` 常量。

### tag_fields ⚠️ 写 — DES 真正意义上的"打标"

> `parse_idl` 只生成 schema、**不会自动加任何标签**。审核单上 Description / Texas / TikTok
> Catalog 全空，根因就是缺这一步。

每个叶子字段 5 项标签（默认**同时应用 request + response**）：

| UI | 写入 | 取值来源（**一律从 IDL 读，不要自己编**） |
|---|---|---|
| Sync | `des.sync` | `mode: all_yes` 默认 `"YES"`；个别字段不同步用 `field_overrides[path].sync: "NO"` |
| **Texas Data Catalog** | `des.tag` | IDL `compliance.message.field_default.texas`（struct 级默认）+ `compliance.field.texas`（字段级覆盖）；名字 → code 用 `fetch_meta {catalog_type: "texas", query: "..."}` 查 |
| **TikTok Data Catalog** | `des.entity` | 业务侧选定，按 scenario 默认表（IDL 暂无对应注解）；用 `fetch_meta {catalog_type: "row_tt"}` 看可选项 |
| **Reason** | `des.reason` | IDL method/struct 上方 `// @sync_reason: ...` |
| **Description** | **`node.description`**（与 `des` 同级，**不是** `des.description`） | IDL field 上方 `// 英文注释` → `(field.desc = "...")` → 最近祖先 comment（fallback） |

> ⚠️ **位置坑**：DECC submit 校验 `node.description`；写到 `des.description` 仍会报
> `description is empty in _request.properties.<field>`。
>
> ⚠️ **语义坑**：`description` ≠ `reason`。description 是"字段是什么"，reason 是"为什么互通"。
> 不要把 reason 文案塞 description（"Required for cross-region..." 是 reason，不是 description）。
>
> ⚠️ **覆盖坑**：基于 `upstream_version=N` 继承的版本，全局 `catalog`/`entity`/`description`
> **不会覆盖**已有值。修正打标必须 `field_overrides` 逐路径写（哪怕全部一样的值，也要每条都写一遍）。

#### Payload 形态（IDL-driven）

每一项都对应到 IDL 注解：全局参数取 struct 级默认，`field_overrides` 取字段级 `// 注释`
和 `compliance.field.*` 覆盖。

```bash
# 假设 IDL 上有：
#   struct Req {
#     option (compliance.message.field_default.texas) = '<struct-level-catalog-name>';
#     // <field-level English comment>
#     1: string <leaf_field>  (compliance.field.texas = '<field-level-catalog-name>');
#     ...
#   }
#   // @sync_reason: <one-line cross-vgeo justification>
#   service S { Resp Method(1: Req); }

gdpa-cli run decc-desrpc --input '{
  "action":   "tag_fields",
  "data_id":  "<data-id>",
  "mode":     "all_yes",
  "catalog":  "<struct-level catalog code, from fetch_meta query=...>",
  "entity":   "<TikTok catalog code, from fetch_meta catalog_type=row_tt|...>",
  "reason":   "<copy of @sync_reason text>",
  "field_overrides": {
    "_request.<leaf>":             {"description": "<leaf English comment>", "catalog": "<field-level catalog code>"},
    "_request.<nested>.<leaf>":    {"description": "<leaf English comment>"}
  }
}'
```

#### `field_overrides` 路径语法

精确路径会**只命中一个节点**，前缀路径用 `/*` 后缀**命中整棵子树的所有叶子**：

| 路径写法 | 含义 | 典型用途 |
|---|---|---|
| `_request.user_id` | 精确：仅 `user_id` 字段 | 单字段微调 |
| `_response.items[].name` | 精确：list 元素中的 `name` | list 里某个具体叶子 |
| `_response.tags{*}.value` | 精确：map value 里的 `value` 字段 | map 里某个具体叶子 |
| `_response.buyer_info{*}/*` | **前缀**：map value 子树下所有叶子 | map<K, ValueStruct> 整体下沉 catalog |
| `_response.items[]/*` | **前缀**：list 元素子树下所有叶子 | list<ValueStruct> 整体下沉 catalog |
| `_response.user_profile/*` | **前缀**：嵌套 struct 下所有叶子 | 子 struct 整体下沉 catalog |

优先级：**精确 override > 更具体的前缀 override > 更短的前缀 override > 全局参数**。
全局参数对**已经有 tag 的字段不会覆盖**，前缀 override 会。

> 推荐用法：先用 `_response.<container>/*` 把整棵子树的 `catalog` / `entity` 设成
> ValueStruct 的 IDL struct 级默认值，再对个别例外叶子用精确路径 override。

打标规范全文（IDL 注解抽取规则、Non-US User Data 额外项、字段路径写法、跳过规则、
常见 reviewer 拒绝模板等）见 **[references/des-tagging-spec.md](references/des-tagging-spec.md)** —
实际打标前**至少扫一遍**。

### fetch_meta — 查打标枚举（Texas / TikTok Catalog / 拒绝模板）

包装 DECC 平台的 `/openapi/meta/detail` 接口。解决两个常见痛点：

1. IDL `compliance.*` 注解里写的是 catalog 的英文名，平台提交需要的是 code，需要做 name → code 翻译
2. submit 前想自检 description / reason 是否会触发常见 reviewer 拒绝模板

```bash
# 按业务名查 Texas Data Catalog code（最常用）
gdpa-cli run decc-desrpc --input '{"action": "fetch_meta", "catalog_type": "texas", "query": "engineering operational"}'
# → [{"tag":"6.1","name":"Engineering Operational Data","path":"Engineering Data > ..."}]

# 看 TikTok Catalog (entity) 的 row_tt 表（scenario=9 用）
gdpa-cli run decc-desrpc --input '{"action": "fetch_meta", "catalog_type": "row_tt"}'
# → [{"label":"5","name":"Engineering Data"}, {"label":"6","name":"Company Data"}, ...]

# Submit 前自检常见拒绝模板
gdpa-cli run decc-desrpc --input '{"action": "fetch_meta", "include": "rejection_templates", "query": "description"}'
# → ["Field description lacks detail", "Detection UV lacks explaination", ...]

# 不带任何过滤拉全表（输出会比较大）
gdpa-cli run decc-desrpc --input '{"action": "fetch_meta"}'
```

参数：
- `catalog_type`：`all`（默认） / `texas` / `row_tt` / `row_nontt` / `nontt`
- `query`：substring 过滤（case-insensitive，匹配 name + tag/code + path + description）
- `include`：默认带回 `rejection_templates`；只想要 catalog 时传 `include: "catalogs_only"`

### submit_data_version ⚠️ 写 + 两阶段确认

**第一次（无 `confirmed`）→ 返回 preview，不提交**：

```bash
gdpa-cli run decc-desrpc --input '{
  "action": "submit_data_version",
  "data_id": "<data-id>",
  "version": <version>
}'
```

返回的 `preview` 含 `schema_summary`，能直接看出还缺哪些字段。把 preview **原样**给用户审阅。

**用户显式同意后第二次（加 `confirmed: true`）→ 真正提交审核单**：

```bash
gdpa-cli run decc-desrpc --input '{
  "action": "submit_data_version",
  "data_id": "<data-id>",
  "version": <version>,
  "scenario": <scenario>,
  "confirmed": true
}'
```

> RPC 方法 IDL 前置依赖：DES-RPC 数据规则 submit 前必须有 IDL，否则报 `empty properties`。
> 见 workflow 中的 `load_idl` → `parse_idl` 步骤。

## Input Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["action"],
  "properties": {
    "action": {
      "type": "string",
      "enum": ["list_channels", "list_data", "list_data_versions", "query_caller_channel", "create_channel", "create_data", "create_data_version", "update_data_version", "submit_data_version", "load_idl", "parse_idl", "tag_fields", "fetch_meta"]
    },
    "name":         { "type": "string", "description": "[list_channels] fuzzy filter. [create_channel] PSM/domain (required)" },
    "vgeo":         { "type": "string", "description": "[list_channels] e.g. 'ROW-TT'" },
    "channel":      { "type": "string", "description": "[list_data, *_data_version, load_idl, parse_idl, tag_fields] channel name" },
    "data_name":    { "type": "string", "description": "[create_data, *_data_version, load_idl, parse_idl] RPC method or HTTP path" },
    "data_id":      { "type": "string", "description": "Data rule ID; alternative to channel+data_name" },
    "version":      { "type": "integer", "description": "Version number (defaults to latest where applicable)" },
    "upstream_version": { "type": "integer", "description": "[create_data_version] base version to inherit from" },
    "description":  { "type": "string", "description": "[create_channel] English-only channel description. [create_data, update_data_version] version-level description. [tag_fields] default field-semantic Description; per-field semantics should go through field_overrides[<path>].description" },
    "reason":       { "type": "string", "description": "[create_data, update_data_version] change reason. [tag_fields] cross-vgeo interop reason; applied to all leaves on BOTH _request and _response (ASCII only)" },
    "explanation":  { "type": "string", "description": "[update_data_version] change explanation" },
    "direction_pairs": {
      "type": "array",
      "items": { "type": "object", "properties": { "source_vgeo": {"type": "string"}, "target_vgeo": {"type": "string"} } },
      "description": "[update_data_version] override extra.rpc.direction_pairs"
    },
    "caller":       { "type": "string", "description": "[query_caller_channel] caller channel name" },
    "callee":       { "type": "string", "description": "[query_caller_channel] callee channel name (usable alone)" },
    "method":       { "type": "string", "description": "[query_caller_channel] RPC method or HTTP path" },
    "caller_site":  { "type": "string", "description": "[query_caller_channel] e.g. 'ROW-TT'" },
    "callee_site":  { "type": "string", "description": "[query_caller_channel] e.g. 'EU'" },
    "scenario": {
      "oneOf": [{"type": "integer"}, {"type": "array", "items": {"type": "integer"}}],
      "description": "[create_channel] scenario list (required unless skip_scenario). [create_data] required when channel has multiple scenarios. [submit_data_version] auto-resolved from version detail; can be overridden. Values: 2=Texas, 3=EU, 4=CN-RoW, 5=TT-NonTT, 9=TT_TTP, 13=BOE-i18n RoW"
    },
    "channel_type": { "type": "integer", "enum": [2, 3, 4], "description": "[create_channel] 2=RPC_PSM, 3=HTTP_PSM, 4=HTTP_DOMAIN; required only if PSM not registered" },
    "owners":       { "type": "array", "items": {"type": "string"}, "description": "[create_channel, create_data] owner usernames" },
    "vgeo_list":    { "type": "array", "items": {"type": "string"}, "description": "[create_channel] vgeo list" },
    "psm_list":     { "type": "array", "items": {"type": "string"}, "description": "[create_channel] domain_psm_list (HTTP_DOMAIN only)" },
    "target_geo_list": { "type": "array", "items": {"type": "string"}, "description": "[create_channel] target geo list" },
    "skip_scenario": { "type": "boolean", "default": false, "description": "[create_channel] bypass scenario requirement (rare)" },
    "auto_create_if_no_draft": { "type": "boolean", "default": false, "description": "[update_data_version] auto-create draft when latest is not draft" },
    "is_serialized_data": { "type": "boolean", "default": false, "description": "[load_idl, parse_idl] usually false for RPC" },
    "endpoint_id":   { "type": "string", "description": "[parse_idl] BAM endpoint id (usually inferable)" },
    "endpoint_name": { "type": "string", "description": "[parse_idl] BAM endpoint name" },
    "endpoint_type": { "type": "string", "description": "[parse_idl] e.g. 'thrift', 'pb'" },
    "endpoint_region": { "type": "string", "description": "[parse_idl] BAM endpoint region (optional)" },
    "category":      { "type": "string", "description": "[parse_idl] DECC category (optional)" },
    "data_type":     { "type": "string", "description": "[parse_idl] DECC data type (optional)" },
    "is_template":          { "type": "boolean", "default": false, "description": "[parse_idl] pass-through" },
    "is_data_type_changed": { "type": "boolean", "default": false, "description": "[parse_idl] pass-through" },
    "has_ods":              { "type": "boolean", "default": false, "description": "[parse_idl] pass-through" },
    "has_nontt":            { "type": "boolean", "default": false, "description": "[parse_idl] pass-through" },
    "mode":     { "type": "string", "enum": ["all_yes", "all_no"], "default": "all_yes", "description": "[tag_fields] default `sync` for every leaf" },
    "catalog":  { "type": "string", "description": "[tag_fields] Texas Data Catalog code, applied to all leaves on BOTH _request and _response (ASCII only)" },
    "entity":   { "type": "string", "description": "[tag_fields] TikTok Data Catalog code, applied to all leaves on BOTH _request and _response (ASCII only)" },
    "field_overrides": {
      "type": "object",
      "description": "[tag_fields] per-field overrides. Keys are dotted field paths (e.g. '_response.item.p1'); values are objects with optional sync/catalog/entity/reason/description. Path syntax: `.` for struct member, `[]` for list element, `{*}` for any map key. Path ending with `/*` is a PREFIX override that applies to ALL descendant leaves of that path (e.g. `_response.buyer_info{*}/*` covers every leaf inside the map's ValueStruct) — this is the recommended way to push struct-level catalog defaults into map<K,V> / list<V> containers, since the global `catalog` parameter alone won't reach those inner leaves correctly. Precedence: exact override > more-specific prefix override > shorter prefix override > global parameters.",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "sync":        { "type": "string", "enum": ["YES", "NO"] },
          "catalog":     { "type": "string" },
          "entity":      { "type": "string" },
          "reason":      { "type": "string" },
          "description": { "type": "string" }
        }
      }
    },
    "confirmed": {
      "type": "boolean",
      "default": false,
      "description": "[submit_data_version] Two-phase confirmation guard. First call without this (or with false) returns a `preview` block and does NOT submit. Only after the human has reviewed the preview and explicitly approved should the caller re-issue the same request with `confirmed: true` to actually submit the audit ticket."
    },
    "enrich": {
      "type": "boolean",
      "default": true,
      "description": "[list_data_versions] when false, skip per-version GetDataVersionDetail enrichment for speed"
    },
    "vregion": {
      "type": "string",
      "enum": ["Singapore-Central", "US-East", "China-North", "China-BOE", "US-BOE"],
      "default": "Singapore-Central",
      "description": "VRegion for authentication. Aliases: 'sg', 'us', 'cn', 'boe', 'boei18n'"
    },
    "catalog_type": {
      "type": "string",
      "enum": ["all", "texas", "row_tt", "row_nontt", "nontt"],
      "default": "all",
      "description": "[fetch_meta] which catalog table to return. `texas` for Texas Data Catalog (the `catalog`/`tag` field in tag_fields). `row_tt`/`row_nontt`/`nontt` for TikTok Data Catalog (the `entity` field in tag_fields), pick by channel region."
    },
    "query": {
      "type": "string",
      "description": "[fetch_meta] case-insensitive substring filter against name + code/tag + path + description. E.g. `query: \"engineering operational\"` finds the Texas catalog code for 'Engineering Operational Data'."
    },
    "include": {
      "type": "string",
      "enum": ["rejection_templates", "catalogs_only", "all"],
      "default": "rejection_templates",
      "description": "[fetch_meta] whether to include reviewer rejection templates. Default returns both catalogs and rejection templates. Pass `catalogs_only` to skip the templates."
    }
  }
}
```

## 进一步阅读

- 字段打标完整规范（`description` 写作规则、Non-US User Data 额外项、跳过规则、字段路径写法）
  → **[references/des-tagging-spec.md](references/des-tagging-spec.md)**
- 各 action 的完整返回字段
  → **[references/output-schemas.md](references/output-schemas.md)**
- 报错速查与修复路径
  → **[references/errors.md](references/errors.md)**
