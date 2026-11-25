---
name: bytefaas
description: Query ByteFaaS (FaaS platform) service details, cluster lists, code revisions, and online revisions by PSM, service ID, or region. Use whenever the user asks about FaaS services, serverless functions, ByteFaaS deployments, FaaS cluster status, function code versions, or mentions ByteFaaS. Also trigger when the user wants to check a FaaS service's configuration, look up which clusters a FaaS function is deployed to, check the current online version of a FaaS function, or debug FaaS-related deployment issues.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# ByteFaaS 服务查询

> **何时使用**: 查询 ByteFaaS 平台的服务信息、集群列表、代码版本、在线版本等。适用于需要了解 FaaS 服务部署状态、集群配置或版本信息的场景。

## 使用方法

```bash
gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "<action>", ...}'
```

## 支持的 Action

| Action                     | 描述                    | 必填参数                        | 可选参数                                                                              |
|----------------------------|-----------------------|-----------------------------|-----------------------------------------------------------------------------------|
| `get_service`              | 按 PSM + env 获取服务详情    | psm, env                    | —                                                                                 |
| `list_services`            | 分页/条件查询服务列表           | —                           | search, name, psm, env, owner, search_type, search_fields, sort_by, limit, offset |
| `list_clusters`            | 按 PSM + region 查询集群列表 | psm, region                 | env                                                                               |
| `list_clusters_by_service` | 按 service_id 分页查集群    | service_id                  | limit, offset                                                                     |
| `get_code_revision`        | 查询代码版本详情              | service_id                  | revision_number（默认 `$latest`）                                                     |
| `get_online_revision`      | 查询集群当前在线版本            | service_id, region, cluster | format                                                                            |

## 输入参数说明

### 通用参数

| 参数      | 类型     | 描述                                                                           |
|---------|--------|------------------------------------------------------------------------------|
| action  | string | 必填，要执行的操作                                                                    |
| vregion | string | VRegion（`code.byted.org/gopkg/env` 标准常量），用于认证和 API 路由。默认 `Singapore-Central` |

### 查询参数

| 参数              | 类型     | 描述                                      |
|-----------------|--------|-----------------------------------------|
| psm             | string | 服务 PSM                                  |
| env             | string | 环境名称（如 `prod`, `ppe`, `boe_feature`）    |
| service_id      | string | 服务 ID                                   |
| region          | string | 集群真实 region 值，用于集群和在线版本查询；例如 `cn-north`、`us-ttp`、`us-ttp2`、`eu-ttp`、`eu-ttp2`、`us-east-red`，不要写成 `usttp` / `euttp` 这种区域组名字 |
| cluster         | string | 集群名称，用于在线版本查询                           |
| revision_number | string | 代码版本号（如 `$latest`），默认 `$latest`         |
| search          | string | 前缀搜索关键字（用于 list_services）               |
| name            | string | 服务名称精确匹配                                |
| owner           | string | 服务 owner，按 username 过滤。⚠️ **优先级低于 `search_type`**：若同时传了 `search_type=own/admin/subscribe`，后端会先按调用者身份裁剪结果集，`owner` 字段会被忽略。查他人服务请不要传 `search_type`，或显式传 `search_type=all` |
| search_type     | string | 搜索类型（**基于当前登录身份**）：`all` 全部、`admin` 我管理的、`own` 我拥有的、`subscribe` 我订阅的。⚠️ **优先级高于 `owner`**：一旦传入，后端就按调用者身份过滤，同时传的 `owner` 会失效。要查他人 owner 的服务，只需要传 `owner`，不要再传 `search_type=own` |
| search_fields   | string | 搜索字段：`cluster_id`, `id`, `name`, `psm`  |
| sort_by         | string | 排序字段                                    |
| limit           | int    | 分页大小，默认 20                              |
| offset          | int    | 分页偏移量，默认 0                              |
| format          | bool   | 是否格式化在线版本输出                             |

### `vregion` 和 `region` 的区别

- `vregion` 是认证和路由用的 VRegion，例如 `US-TTP`、`EU-TTP`、`US-EastRed`。
- `region` 是接口里的真实集群 region，例如 `us-ttp`、`us-ttp2`、`eu-ttp`、`eu-ttp2`、`us-east-red`、`cn-north`。
- 不要把区域组名直接当作 `region` 传入：`usttp` / `euttp` 不是合法的 `region` 值，通常会查不到数据。
- 可以简单记成：`USTTP/EUTTP` 这类是你选 `vregion` 时看的，`us-ttp/us-east-red` 这类才是你查 cluster / online revision 时传的 `region`。

### vregion 可选值

| VRegion                | 说明              |
|------------------------|-----------------|
| `US-BOE`               | 国际 BOE 测试环境     |
| `China-BOE`            | 中国 BOE 测试环境     |
| `China-North`          | 中国北方            |
| `China-East`           | 中国华东            |
| `China-Pay`            | 中国支付            |
| `China-Pay2`           | 中国支付二期          |
| `ID-Compliance`        | 印尼合规区           |
| `ID-Compliance2`       | 印尼合规区二期         |
| `MY-Compliance`        | 马来合规区           |
| `Singapore-Central`    | 新加坡（默认值）        |
| `US-East`              | 美东              |
| `US-West`              | 美西              |
| `Singapore-Compliance` | 新加坡合规区          |
| `US-TTP`               | 美国合规区（USTTP）    |
| `US-TTP2`              | 美国合规区二期（USTTP2） |
| `EU-TTP`               | 欧洲合规区（EUTTP）    |
| `EU-TTP2`              | 欧洲合规区二期（EUTTP2） |
| `US-Compliance`        | 美国合规区           |
| `EU-Compliance`        | 欧洲合规区           |
| `EU-Compliance2`       | 欧洲合规区二期         |
| `US-EastRed`           | 美东红区（useast2a）  |

### 业务常用区域组与推荐 vregion

> 当业务只说粗粒度区域（如 `cn`、`boe`、`i18n`、`usttp`、`euttp`）时，可优先按下表选择 `vregion`，而不是盲目遍历全部区域。

| 业务常说的区域组 | 推荐优先尝试的 `vregion` |
|------------------|--------------------------|
| `cn`             | `China-North` / `China-East` / `China-Pay` / `China-Pay2` |
| `boe`            | `China-BOE` |
| `boe-i18n`       | `US-BOE` |
| `usttp`          | `US-TTP` / `US-TTP2` |
| `euttp`          | `EU-TTP` / `EU-TTP2` / `US-EastRed` |
| `i18n`           | `Singapore-Central` / `US-East` / `US-West` |

### 查询建议

- 已知 `psm + env` 时，优先使用 `get_service`，比 `list_services` 更可靠。
- 用户只说 `i18n` / `cn` / `boe` / `usttp` / `euttp` 时，优先在对应组内选择 `vregion`，不要跨组乱试。
- 查 `list_clusters` / `get_online_revision` 时，`region` 要传真实集群 region，而不是区域组名；例如传 `us-ttp` / `us-ttp2` / `eu-ttp` / `eu-ttp2` / `us-east-red`，不要传 `usttp` / `euttp`。
- 网络超时不等于“服务不存在”；只有请求成功但返回空结果时，才可认为该 `vregion` 下未命中。

## 输出格式

所有输出遵循统一结构：

```json
{
  "success": true,
  "action": "get_service",
  "data": {
    ...
  }
}
```

### get_service 输出

```json
{
  "success": true,
  "action": "get_service",
  "data": {
    "code": 0,
    "service": {
      "service_id": "xxx",
      "name": "my-function",
      "psm": "tiktok.example.faas",
      "owner": "user1",
      "language": "golang",
      "runtime": "go1.18",
      "env_name": "prod",
      "description": "My FaaS function",
      "admins": "user1,user2",
      "deploy_method": "code",
      "clusters": [
        ...
      ]
    }
  }
}
```

### list_services 输出

```json
{
  "success": true,
  "action": "list_services",
  "data": {
    "code": 0,
    "services": [
      ...
    ],
    "total": 5
  }
}
```

### list_clusters 输出

```json
{
  "success": true,
  "action": "list_clusters",
  "data": {
    "code": 0,
    "psm": "tiktok.example.faas",
    "region": "cn-north",
    "clusters": [
      {
        "cluster": "faas-xxx",
        "region": "cn-north",
        "status": "Active",
        "runtime": "go1.18",
        "handler": "handler.Handler",
        "code_revision_number": "3"
      }
    ],
    "total": 1
  }
}
```

### get_code_revision 输出

```json
{
  "success": true,
  "action": "get_code_revision",
  "data": {
    "code": 0,
    "revision": {
      "id": "xxx",
      "number": "3",
      "service_id": "xxx",
      "runtime": "go1.18",
      "handler": "handler.Handler",
      "source": "code",
      "created_at": "2024-01-01T00:00:00Z",
      "created_by": "user1"
    }
  }
}
```

### get_online_revision 输出

```json
{
  "success": true,
  "action": "get_online_revision",
  "data": {
    "code": 0,
    "service_id": "xxx",
    "revisions": [
      {
        "code_revision_id": "xxx",
        "cluster": "faas-xxx",
        "traffic_value": "100",
        "images": [
          "image:tag"
        ]
      }
    ],
    "total": 1
  }
}
```

## 示例

```bash
# 按 PSM + env 查询服务详情
# 已知 psm + env 时，优先用 get_service

gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "get_service", "psm": "tiktok.example.faas", "env": "prod"}'

# 搜索服务列表
gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "list_services", "search": "gdpa", "limit": 10}'

# 按 owner 查询他人的服务
# ⚠️ search_type 优先级高于 owner：一旦传 `own/admin/subscribe`，后端会按调用者身份裁剪，owner 就失效。
# 查他人服务时，要么只传 owner，要么同时传 search_type=all，切勿传 search_type=own + owner=<他人>。
gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "list_services", "owner": "user1"}'
gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "list_services", "owner": "user1", "search_type": "all"}'

# 查询当前登录账号自己的服务（不传 owner，只传 search_type=own）
gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "list_services", "search_type": "own"}'

# TTP 下按 psm 查询服务列表
# 注意：这里仍然只传 psm；skill 会在 TTP 下自动转换成 search=<psm> + search_type=all

gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "list_services", "psm": "oec.pay.billing_mock_reverse", "limit": 5, "vregion": "EU-TTP"}'

# 查询 PSM 在指定 region 的集群
# 注意：这里的 region 要写真实集群 region，不是 usttp/euttp 这种区域组名

gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "list_clusters", "psm": "tiktok.example.faas", "region": "cn-north"}'

# 查询 USTTP 集群列表示例

gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "list_clusters", "psm": "goofy_ssr.ttp2.134215", "region": "us-ttp2", "env": "prod", "vregion": "US-TTP2"}'

# 查询 EUTTP 集群列表示例

gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "list_clusters", "psm": "oec.ecom.atlas_gateway_l2l_eu_4489425gs", "region": "us-east-red", "env": "prod", "vregion": "EU-TTP"}'

# 按 service_id 分页查集群
gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "list_clusters_by_service", "service_id": "12345", "limit": 10}'

# 查询最新代码版本
gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "get_code_revision", "service_id": "12345"}'

# 查询指定版本号
gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "get_code_revision", "service_id": "12345", "revision_number": "3"}'

# 查询集群在线版本
# 注意：region 同样要写真实集群 region

gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "get_online_revision", "service_id": "12345", "region": "cn-north", "cluster": "faas-xxx"}'

# 查询 BOE 环境下的服务
gdpa-cli run bytefaas --session-id "$SESSION_ID" --input '{"action": "get_service", "psm": "tiktok.example.faas", "env": "boe_feature", "vregion": "China-BOE"}'
```

### 业务表达转查询参数示例

- “i18n 区域的 `bytedance.skill.autoperf_report`”
  - 若已知环境，优先：`{"action": "get_service", "psm": "bytedance.skill.autoperf_report", "env": "<env>", "vregion": "Singapore-Central"}`
  - 若未命中，**向用户报告未找到**，并建议可尝试的其他 VRegion（如 `US-East`、`US-West`），**等待用户确认后再重试**。绝不自动切换 VRegion。
- “cn 区域的 `bytedance.mcp.gdpa`”
  - 若已知环境，优先：`{"action": "get_service", "psm": "bytedance.mcp.gdpa", "env": "<env>", "vregion": "China-North"}`
  - 若未命中，**向用户报告未找到**，并建议可尝试的其他 VRegion（如 `China-East`、`China-Pay`、`China-Pay2`），**等待用户确认后再重试**。绝不自动切换 VRegion。
- “euttp 区域的某个服务”
  - 建议用户可能的查询 VRegion：`EU-TTP`、`EU-TTP2`、`US-EastRed`。若首次未命中，**报告结果后让用户决定是否换区重试**。

## 错误处理

| 错误                                 | 原因           | 解决方案                      |
|------------------------------------|--------------|---------------------------|
| `action parameter is required`     | 缺少 action 参数 | 添加 `action` 参数            |
| `psm parameter is required`        | 缺少 PSM       | 添加 `psm` 参数               |
| `service_id parameter is required` | 缺少服务 ID      | 添加 `service_id` 参数        |
| `authentication failed`            | JWT 获取失败     | 运行 `gdpa-cli login` 先登录   |
| API 返回 `code != 0`                 | 业务错误（如服务不存在） | 检查 PSM、service_id 等参数是否正确 |

## 注意事项

- 默认 VRegion 为 `Singapore-Central`（I18N 默认），查询国内服务需指定 `vregion: China-North` 或 `vregion: China-BOE`
- `list_services` 按 `psm` 查询时，Skill 会根据区域自动选择后端能识别的参数组合：
  - **TTP**（US-TTP/EU-TTP 等）：`search=<psm>` + `search_type=all`
  - **China-North（CN）**：原生 `psm` + `all=true`
  - **i18n / BOE**（Singapore-Central、US-East、US-BOE、China-BOE 等）：`search=<psm>` + `search_fields=psm` + `search_type=all`（i18n 网关会忽略原生 `psm` 字段，必须用关键字搜索）
- `get_code_revision` 的 `revision_number` 默认为 `$latest`；TTP 下未传 `revision_number` 时会自动走列表接口取最新版本
- 需要先通过 `gdpa-cli login` 登录获取认证凭据
