---
name: cultivation-world-simulator-api
description: Use when 用户提供一个正在运行的 cultivation-world-simulator 部署地址，并希望你通过 external control API v1 的 HTTP 或 WebSocket 接口查询世界状态、事件、详情、元数据、存档、设置，或在明确授权下执行受控写操作。
---

# cultivation-world-simulator external control API v1

## 核心规则

- 只有在用户给出模拟器部署地址后才开始调用 API。
- 先把地址规范化为 `base_url`：补 `http://`，并去掉末尾 `/`。
- 默认先调用 `GET /api/v1/query/runtime/status`，再决定后续查询或写操作。
- 外接稳定契约以 `/api/v1/query/*` 和 `/api/v1/command/*` 为准，不要再依赖旧 `/api/*` 兼容层。
- 唯一例外是应用设置真源：`/api/settings*` 与 `/api/settings/llm*` 仍保留旧路径，不属于 v1 `ok/data` 包装。
- 默认优先 HTTP；只有用户明确要求“实时看”“持续监听”“盯住新事件”时才连接 `WS /ws`。
- 默认优先只读接口；只有在用户明确要求修改状态时，才使用下文列出的白名单写接口。
- 历史事件统一走 `GET /api/v1/query/events`；`GET /api/v1/query/world/state` 只看当前快照，不能代替事件历史查询。
- 如果用户给的是名字，不是 ID，必须先做名称解析，再发正式查询。
- 名称匹配到多个候选时不要猜，直接把候选列表返回给用户确认。
- `goldfinger` 现在是正式实体；相关说明字段以 `desc`、`story_prompt`、`effect_desc`、`mechanism_type` 为准，不要再假设存在 `display_text` 或 `enabled`。
- v1 成功响应统一解包 `{"ok": true, "data": ...}`；v1 失败响应优先读取 HTTP 错误体里的 `detail.code`、`detail.message`、`detail.details`。

## 终端中的默认调用方式

在 Windows / Codex 终端里，优先使用 PowerShell 的 `Invoke-RestMethod`。

对 `/api/v1/*` 使用自动解包的封装；对 `/api/settings*` 使用 raw 封装。

```powershell
$base = 'http://127.0.0.1:8002'.TrimEnd('/')

function Invoke-Cws([string]$method, [string]$path, $body = $null, [switch]$RawResponse) {
    $params = @{
        Method = $method
        Uri    = ($base + $path)
    }

    if ($null -ne $body) {
        $params.ContentType = 'application/json'
        $params.Body = $body | ConvertTo-Json -Depth 8
    }

    $resp = Invoke-RestMethod @params

    if (
        -not $RawResponse `
        -and $resp `
        -and $resp.ok -eq $true `
        -and ($resp.PSObject.Properties.Name -contains 'data')
    ) {
        return $resp.data
    }

    return $resp
}

function Get-Cws([string]$path) {
    Invoke-Cws 'GET' $path
}

function Send-Cws([string]$method, [string]$path, $body = $null) {
    Invoke-Cws $method $path $body
}

function Get-CwsRaw([string]$path) {
    Invoke-Cws 'GET' $path $null -RawResponse
}

function Send-CwsRaw([string]$method, [string]$path, $body = $null) {
    Invoke-Cws $method $path $body -RawResponse
}
```

最常用的最小调用：

```powershell
$runtime = Get-Cws '/api/v1/query/runtime/status'
$avatars = Get-Cws '/api/v1/query/meta/avatar-list'
$events = Get-Cws '/api/v1/query/events?limit=20'
$state = Get-Cws '/api/v1/query/world/state'
$settings = Get-CwsRaw '/api/settings'
```

### 什么时候必须用 `Get-CwsRaw` / `Send-CwsRaw`

看到下面两类接口时，不要走 `Get-Cws` / `Send-Cws`：

1. `'/api/settings'`、`'/api/settings/llm'`、`'/api/settings/llm/status'`、`'/api/settings/llm/test'`
2. 任何不在 `'/api/v1/query/*'` 或 `'/api/v1/command/*'` 命名空间里的保留设置接口

原因：

- 它们仍然是旧路径
- 它们默认返回 raw JSON
- 它们不是统一的 `{"ok": true, "data": ...}` 包装

最容易错的写法：

```powershell
$settings = Get-Cws '/api/settings'
```

应改为：

```powershell
$settings = Get-CwsRaw '/api/settings'
$llmStatus = Get-CwsRaw '/api/settings/llm/status'
$testResp = Send-CwsRaw 'POST' '/api/settings/llm/test' $body
```

## 启动前固定检查

先调用：

```powershell
$runtime = Get-Cws '/api/v1/query/runtime/status'
```

按 `status` 分支处理：

- `ready`：世界已可用，可以继续绝大多数业务查询与经用户授权的写操作。
- `idle`：当前没有运行中的世界。不要继续查询人物、事件、宗门、区域详情等世界依赖接口；可以继续查看 `GET /api/v1/query/saves`、`GET /api/settings`、`GET /api/settings/llm`、`GET /api/settings/llm/status`，或在用户要求时调用开局/读档相关接口。
- `pending` / `in_progress`：初始化过程中默认先回报进度；如用户想看初始化中的地图或快照，可以尝试 `GET /api/v1/query/world/map` 与 `GET /api/v1/query/world/state`，但要明确说明这是初始化阶段的部分信息，不保证完整。
- `error`：初始化失败。直接返回 `error`；如果 `llm_check_failed=true`，同时带上 `llm_error_message`。不要继续执行世界依赖查询。

`/api/v1/query/runtime/status` 的关键字段：

- `status`
- `phase`
- `phase_name`
- `progress`
- `elapsed_seconds`
- `error`
- `version`
- `llm_check_failed`
- `llm_error_message`
- `is_paused`

## 名称解析

### 人物名 -> `avatar_id`

固定流程：

1. `GET /api/v1/query/meta/avatar-list`
2. 先精确匹配 `name`
3. 精确匹配不到时，再做包含匹配
4. 命中 1 个候选就继续
5. 命中多个候选时，返回候选列表让用户确认

`/api/v1/query/meta/avatar-list` 常用字段：

- `id`
- `name`
- `sect_name`
- `realm`
- `gender`
- `age`

如果重名或近似名过多，按下面模板确认：

```text
找到多个候选，请确认要查哪一个：
1. id=a1 | name=张三 | sect_name=青云宗 | realm=筑基 | age=37
2. id=a2 | name=张三 | sect_name=散修 | realm=炼气 | age=18
```

### 宗门名 -> `sect_id`

固定流程：

1. 优先 `GET /api/v1/query/sects/territories`
2. 需要补充区域上下文时再查 `GET /api/v1/query/world/map`
3. 用 `sects[].id` / `sects[].name` 或地图区域里的 `sect_id` / `sect_name` 命中目标

### 区域名 -> `region_id`

固定流程：

1. `GET /api/v1/query/world/map`
2. 在 `regions[]` 里按 `name` 或 `id` 查找
3. 再调用 `GET /api/v1/query/detail?type=region&id=...`

## 只读接口与关键参数

### 基础状态与元数据

| 接口 | 方法 | 用途 |
|---|---|---|
| `/api/v1/query/runtime/status` | `GET` | 判断世界是否可查、查看初始化进度 |
| `/api/v1/query/system/current-run` | `GET` | 当前开局配置快照 |
| `/api/v1/query/meta/avatar-list` | `GET` | 人物名解析到 `avatar_id` |
| `/api/v1/query/meta/avatars` | `GET` | 头像素材库，常用于头像更新前取可用 `pic_id` |
| `/api/v1/query/meta/game-data` | `GET` | 角色创建所需的宗门、人格、境界、装备等元数据 |
| `/api/v1/query/meta/avatar-adjust-options` | `GET` | 角色调整面板全量选项，包含 `goldfingers` |
| `/api/v1/query/meta/phenomena` | `GET` | 可切换天象列表 |

### 世界查询

| 接口 | 方法 | 关键参数 | 用途 |
|---|---|---|---|
| `/api/v1/query/events` | `GET` | `avatar_id`、`avatar_id_1`、`avatar_id_2`、`sect_id`、`major_scope`、`cursor`、`limit` | 历史事件查询 |
| `/api/v1/query/detail` | `GET` | `type=avatar\|sect\|region`、`id` | 角色 / 宗门 / 区域详情 |
| `/api/v1/query/world/state` | `GET` | 无 | 当前世界快照 |
| `/api/v1/query/world/map` | `GET` | 无 | 地图、区域、宗门映射 |
| `/api/v1/query/sects/territories` | `GET` | 无 | 宗门列表与领地 |
| `/api/v1/query/sect-relations` | `GET` | 无 | 宗门关系 |
| `/api/v1/query/rankings` | `GET` | 无 | 榜单 |
| `/api/v1/query/mortals/overview` | `GET` | 无 | 凡人系统总览 |
| `/api/v1/query/dynasty/overview` | `GET` | 无 | 王朝总览 |
| `/api/v1/query/dynasty/detail` | `GET` | 无 | 王朝详情 |
| `/api/v1/query/saves` | `GET` | 无 | 存档列表，包含 `language`、`avatar_count`、`alive_count`、`dead_count`、`custom_name`、`event_count`、`playthrough_id`、`is_auto_save` 等元数据 |

### 应用设置例外接口

这些接口仍保留旧路径，且默认返回 raw JSON，不是 `ok/data` 包装：

| 接口 | 方法 | 用途 |
|---|---|---|
| `/api/settings` | `GET` | 应用设置 |
| `/api/settings/llm` | `GET` | LLM 配置视图 |
| `/api/settings/llm/status` | `GET` | LLM 是否已配置 |

### `GET /api/v1/query/events` 参数规则

- 单人物事件：只传 `avatar_id`
- 双人共同经历：必须同时传 `avatar_id_1` 和 `avatar_id_2`
- 宗门事件：传 `sect_id`
- 事件类型：`major_scope` 只允许 `all`、`major`、`minor`
- 分页：检查 `events`、`next_cursor`、`has_more`
- `limit` 默认是 `100`；如果只是回答“最近事件”，常用 `20` 或 `50`

### `GET /api/v1/query/detail` 参数规则

- 角色详情：`/api/v1/query/detail?type=avatar&id=<avatar_id>`
- 宗门详情：`/api/v1/query/detail?type=sect&id=<sect_id>`
- 区域详情：`/api/v1/query/detail?type=region&id=<region_id>`

### Avatar detail 里的 `goldfinger`

`GET /api/v1/query/detail?type=avatar&id=...` 返回的角色详情现在可能包含 `goldfinger`，常见字段包括：

- `id`
- `name`
- `desc`
- `key`
- `rarity`
- `color`
- `effect_desc`
- `story_prompt`
- `mechanism_type`
- `state`
- `source_of_truth`
- `state_source_of_truth`

如果用户问某角色的外挂、外挂效果、外挂故事提示，不要忽略这部分。

### 常见 v1 错误结构

v1 公共 API 失败时，优先读取 HTTP 错误体中的：

- `detail.code`
- `detail.message`
- `detail.details`

常见错误码包括：

- `WORLD_NOT_READY`
- `EVENTS_NOT_READY`
- `TARGET_NOT_FOUND`
- `UNSUPPORTED_DETAIL_TYPE`

## 白名单写接口

只有在用户明确要求修改状态时，才使用这些接口。默认仍优先只读。

### 角色与内容操作

| 接口 | 方法 | 何时使用 |
|---|---|---|
| `/api/v1/command/avatar/set-long-term-objective` | `POST` | 用户明确要求给角色设置长期目标 |
| `/api/v1/command/avatar/clear-long-term-objective` | `POST` | 用户明确要求清空长期目标 |
| `/api/v1/command/avatar/create` | `POST` | 用户明确要求创建角色 |
| `/api/v1/command/avatar/delete` | `POST` | 用户明确要求删除角色 |
| `/api/v1/command/avatar/update-portrait` | `POST` | 用户明确要求修改角色头像 |
| `/api/v1/command/avatar/update-adjustment` | `POST` | 用户明确要求修改角色功法、武器、辅助、人格或 `goldfinger` |
| `/api/v1/command/avatar/generate-custom-content` | `POST` | 用户明确要求让 AI 先生成自定义内容草稿 |
| `/api/v1/command/avatar/create-custom-content` | `POST` | 用户明确要求把草稿落成正式自定义内容 |

### 世界与系统操作

| 接口 | 方法 | 何时使用 |
|---|---|---|
| `/api/v1/command/world/set-phenomenon` | `POST` | 用户明确要求切换当前天象 |
| `/api/v1/command/game/start` | `POST` | 用户明确要求开始新开局 |
| `/api/v1/command/game/load` | `POST` | 用户明确要求读档 |
| `/api/v1/command/game/save` | `POST` | 用户明确要求手动存档 |
| `/api/settings/llm/test` | `POST` | 用户明确要求测试 LLM 连接 |
| `/api/settings/llm` | `PUT` | 用户明确要求更新 LLM 配置 |
| `/api/settings` | `PATCH` | 用户明确要求修改应用设置 |

以下接口虽然存在，但更偏控制/清理操作；除非用户明确要求，否则不要主动调用：

- `DELETE /api/v1/command/events/cleanup`
- `POST /api/v1/command/game/pause`
- `POST /api/v1/command/game/resume`
- `POST /api/v1/command/game/reset`
- `POST /api/v1/command/game/reinit`
- `POST /api/v1/command/game/delete-save`
- `POST /api/v1/command/system/shutdown`
- `POST /api/settings/reset`

## 关键写操作规则

- `avatar/create` 请求体不包含 `goldfinger` 字段。手动创建角色后，如果还要给角色外挂，应继续调用 `POST /api/v1/command/avatar/update-adjustment`，并传 `category='goldfinger'`。
- `avatar/update-adjustment` 的 `category` 允许：`technique`、`weapon`、`auxiliary`、`personas`、`goldfinger`。
- `avatar/generate-custom-content` / `avatar/create-custom-content` 的 `category` 允许：`technique`、`weapon`、`auxiliary`、`goldfinger`。
- `avatar/set-long-term-objective` 的请求体字段名是 `content`，不要自行改成 `objective` 或其他别名。
- `game/delete-save` 的请求体关键字段是 `filename`。
- `events/cleanup` 走 `DELETE`，常用查询参数是 `keep_major` 与 `before_month_stamp`，不是旧版 `POST` 清理接口。
- 自定义 `goldfinger` 草稿/实体应以 `desc`、`story_prompt`、`effect_desc`、`mechanism_type` 为准，不要再构造 `display_text` 或 `enabled`。
- 自定义内容里的 `effects` 必须使用后端认可的 canonical effect key；不要凭空编造字段名。

## 常用查询与操作配方

### 1. 查某人物最近事件

```powershell
$avatars = (Get-Cws '/api/v1/query/meta/avatar-list').avatars
$avatar = $avatars | Where-Object { $_.name -eq '张三' } | Select-Object -First 1
$events = Get-Cws "/api/v1/query/events?avatar_id=$($avatar.id)&limit=20"
$events
```

### 2. 查两个人共同经历

```powershell
$avatars = (Get-Cws '/api/v1/query/meta/avatar-list').avatars
$a1 = $avatars | Where-Object { $_.name -eq '张三' } | Select-Object -First 1
$a2 = $avatars | Where-Object { $_.name -eq '李四' } | Select-Object -First 1
$events = Get-Cws "/api/v1/query/events?avatar_id_1=$($a1.id)&avatar_id_2=$($a2.id)&limit=50"
$events
```

### 3. 查角色详情里的外挂

```powershell
$avatars = (Get-Cws '/api/v1/query/meta/avatar-list').avatars
$avatar = $avatars | Where-Object { $_.name -eq '韩立' } | Select-Object -First 1
$detail = Get-Cws "/api/v1/query/detail?type=avatar&id=$($avatar.id)"
$detail.goldfinger
```

### 4. 给角色设置 `goldfinger`

```powershell
$avatars = (Get-Cws '/api/v1/query/meta/avatar-list').avatars
$avatar = $avatars | Where-Object { $_.name -eq '韩立' } | Select-Object -First 1

$catalog = Get-Cws '/api/v1/query/meta/avatar-adjust-options'
$goldfinger = $catalog.goldfingers | Where-Object { $_.name -eq '气运之子' } | Select-Object -First 1

$body = @{
    avatar_id = $avatar.id
    category = 'goldfinger'
    target_id = [int]$goldfinger.id
}

Send-Cws 'POST' '/api/v1/command/avatar/update-adjustment' $body
```

### 5. 先生成再创建自定义 `goldfinger`

```powershell
$draftResp = Send-Cws 'POST' '/api/v1/command/avatar/generate-custom-content' @{
    category = 'goldfinger'
    user_prompt = '做一个偏奇遇和悟性的外挂，名字叫天命推演'
}

$createResp = Send-Cws 'POST' '/api/v1/command/avatar/create-custom-content' @{
    category = 'goldfinger'
    draft = $draftResp.draft
}

$createResp.item
```

### 6. 创建角色

```powershell
$meta = Get-Cws '/api/v1/query/meta/game-data'
$sect = $meta.sects | Where-Object { $_.name -eq '青云宗' } | Select-Object -First 1
$persona = $meta.personas | Where-Object { $_.name -eq '扮猪吃老虎' } | Select-Object -First 1

$body = @{
    surname = '韩'
    given_name = '立'
    gender = '男'
    age = 19
    level = 5
    sect_id = $sect.id
    persona_ids = @($persona.id)
}

Send-Cws 'POST' '/api/v1/command/avatar/create' $body
```

### 7. 更新头像

```powershell
$avatars = (Get-Cws '/api/v1/query/meta/avatar-list').avatars
$avatar = $avatars | Where-Object { $_.name -eq '韩立' } | Select-Object -First 1
$assetMeta = Get-Cws '/api/v1/query/meta/avatars'

$body = @{
    avatar_id = $avatar.id
    pic_id = 12
}

Send-Cws 'POST' '/api/v1/command/avatar/update-portrait' $body
```

### 8. 切换天象

```powershell
$phenomena = (Get-Cws '/api/v1/query/meta/phenomena').phenomena
$target = $phenomena | Where-Object { $_.name -eq '血月' } | Select-Object -First 1

Send-Cws 'POST' '/api/v1/command/world/set-phenomenon' @{
    id = [int]$target.id
}
```

### 9. 读档

```powershell
$saves = (Get-Cws '/api/v1/query/saves').saves
$target = $saves | Sort-Object save_time -Descending | Select-Object -First 1

Send-Cws 'POST' '/api/v1/command/game/load' @{
    filename = $target.filename
}
```

### 10. 测试 LLM 连接

```powershell
$body = @{
    base_url = 'https://api.openai.com/v1'
    api_key = 'sk-...'
    model_name = 'gpt-5.2'
    fast_model_name = 'gpt-5.2'
    mode = 'openai'
    max_concurrent_requests = 4
    api_format = 'openai'
}

Send-CwsRaw 'POST' '/api/settings/llm/test' $body
```

## WebSocket 实时监听

只有用户明确要求“实时看事件”“持续监听”“盯住新事件”时才连接 `/ws`。

HTTP 地址转 WebSocket 地址：

- `http://127.0.0.1:8002` -> `ws://127.0.0.1:8002/ws`
- `https://demo.example.com` -> `wss://demo.example.com/ws`

默认监听脚本：

```powershell
$wsBase = ($base -replace '^http://', 'ws://' -replace '^https://', 'wss://')
$wsUrl = "$wsBase/ws"

$ws = [System.Net.WebSockets.ClientWebSocket]::new()
$ct = [Threading.CancellationToken]::None
$ws.ConnectAsync([Uri]$wsUrl, $ct).GetAwaiter().GetResult()

$buffer = New-Object byte[] 65536
$deadline = (Get-Date).AddSeconds(20)

while ((Get-Date) -lt $deadline) {
    $segment = [ArraySegment[byte]]::new($buffer)
    $result = $ws.ReceiveAsync($segment, $ct).GetAwaiter().GetResult()

    if ($result.MessageType -eq [System.Net.WebSockets.WebSocketMessageType]::Close) {
        break
    }

    $msg = [Text.Encoding]::UTF8.GetString($buffer, 0, $result.Count) | ConvertFrom-Json

    if ($msg.type -eq 'llm_config_required') {
        $msg
        break
    }

    if ($msg.type -eq 'tick' -and $msg.events -and $msg.events.Count -gt 0) {
        $msg
    }
}

$ws.Dispose()
```

WebSocket 消费规则：

- 默认只处理 `type='tick'` 的消息
- 只提取 `events` 非空的 `tick`
- `tick` 重点字段：`year`、`month`、`events`、`avatars`、`phenomenon`、`active_domains`
- `type='llm_config_required'` 不是事件，直接把错误返回给用户并停止
- `type='toast'`、`type='game_reinitialized'` 属于系统提示，不要混进事件列表
- 默认只做短窗口监听并汇总结果；只有用户明确要求持续监听时才保持连接
- 需要保活时，可以向服务端发送文本 `ping`，期望收到 `{"type":"pong"}`

## 常见 API 误用

- 不要继续使用旧 `/api/*` 兼容层；外接公共接口应优先走 `/api/v1/query/*` 和 `/api/v1/command/*`
- 不要把人物名直接塞进 `avatar_id`；先查 `/api/v1/query/meta/avatar-list`
- 不要用 `/api/v1/query/world/state` 代替 `/api/v1/query/events`
- 不要分别查两个人的事件再手动拼共同经历；应直接用 `avatar_id_1 + avatar_id_2`
- 不要只看第一页就下结论；要检查 `has_more` 和 `next_cursor`
- 不要把规则写死成“非 `ready` 一律不能查”；初始化阶段至少应先看 `/api/v1/query/runtime/status`，必要时再读 `/api/v1/query/world/map` 或 `/api/v1/query/world/state`
- 不要在未获用户明确要求时调用写接口
- 不要把 `/api/settings*` 当成 v1 `ok/data` 包装接口；它们是保留的 raw 设置接口
- 不要把 `display_text`、`enabled` 当成新版 `goldfinger` 或自定义外挂的必备字段
- 不要假设 `avatar/create` 能直接指定外挂；要追加 `goldfinger` 请走 `/api/v1/command/avatar/update-adjustment`
- 不要把 `POST /api/settings/llm/test` 和 `PUT /api/settings/llm` 混为同一个接口

## 对用户回报时至少说明

- 命中的对象和 ID
- 实际调用的接口
- 关键查询参数或请求体关键字段
- 拿到的数据范围，例如“最近 20 条”或“已翻完全部分页”
- 如果执行了写操作，要明确说明这是根据用户要求触发的状态修改
