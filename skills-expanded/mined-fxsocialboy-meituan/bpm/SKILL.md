---
name: bpm
description: Manage BPM (流程平台) workflow tickets — update status, get detail, list records, cancel, and list process logs. Use whenever the user mentions BPM, 流程平台, workflow tickets (工单), wants to check ticket status, approve or advance a ticket, query ticket lists by creator/assignee/tenant, cancel a ticket, or view process logs. Also trigger when the user provides a BPM workflow ID and wants to look up its detail, or needs to manage approval workflows on bpm.bytedance.net.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# BPM 流程平台工单管理

管理 BPM（流程平台）工单：变更工单状态、获取工单详情、查询工单列表、取消工单、查询流程日志。

## When to Use

- 查看 BPM 工单详情（按 workflow_id）
- 查询工单列表（按租户、创建人、处理人、状态等筛选）
- 推进工单状态流转（审批通过/拒绝/下一步）
- 取消（强制关闭）未完成的工单
- 查看工单的流程运行日志

## Command Format

```bash
gdpa-cli run bpm --session-id "$SESSION_ID" --input '<json_params>'
```

## Actions

### 1. get_detail — 获取工单详情

根据 workflow_id 查询工单详情。

```bash
gdpa-cli run bpm --session-id "$SESSION_ID" --input '{"action": "get_detail", "workflow_id": "879450"}'
```

### 2. list_records — 查询工单列表

在当前用户可见范围内搜索工单列表，支持多种筛选条件。

```bash
# 查询未完成的工单
gdpa-cli run bpm --session-id "$SESSION_ID" --input '{"action": "list_records", "finished": ["0"], "page_size": "5"}'

# 按租户查询（I18N 环境）
gdpa-cli run bpm --session-id "$SESSION_ID" --input '{"action": "list_records", "target_system": "DH_test1", "vregion": "sg"}'

# 按创建人查询
gdpa-cli run bpm --session-id "$SESSION_ID" --input '{"action": "list_records", "creator": "donghao.blueone", "finished": ["0", "1"]}'
```

### 3. list_logs — 查询流程日志列表

根据工单 ID 获取流程运行日志。

```bash
gdpa-cli run bpm --session-id "$SESSION_ID" --input '{"action": "list_logs", "workflow_id": "879450"}'
```

### 4. get_op_keys — 获取可用操作列表

查询工单当前状态下可执行的操作（如通过、拒绝、修改审批人），用于在 `update_status` 前确认可用的 `op_key`。

```bash
gdpa-cli run bpm --session-id "$SESSION_ID" --input '{"action": "get_op_keys", "workflow_id": "8403208", "vregion": "sg"}'
```

### 5. update_status — 变更工单状态节点

推进工单状态流转（审批通过、拒绝、下一步等）。

```bash
gdpa-cli run bpm --session-id "$SESSION_ID" --input '{"action": "update_status", "workflow_id": "879450", "status": "pending1", "op_key": "next"}'
```

### 6. cancel — 取消工单

强制关闭一个未完成的工单，操作人需为租户管理员或工单创建者。

```bash
gdpa-cli run bpm --session-id "$SESSION_ID" --input '{"action": "cancel", "workflow_id": "879450"}'
```

## VRegion 区域映射

| VRegion | Aliases | 办公网 URL | 生产网 URL | JWT |
|---------|---------|-----------|-----------|-----|
| `China-North` | `cn`, `china` | `bpm.bytedance.net` | `bpm.bytedance.net` | CN |
| `China-BOE` | `boe`, `cn-boe` | `bpm-boe.bytedance.net` | `bpm-boe.bytedance.net` | CN |
| `US-BOE` | `boei18n`, `boe-i18n` | `bpm-boe-i18n.bytedance.net` | `bpm-boe-i18n.bytedance.net` | CN |
| `Singapore-Central` | `sg`, `singapore` | `bpm-i18n.tiktok-row.net` | `bpm-i18n.bytedance.net` | I18N |
| `US-East` | `us`, `i18n` | `bpm-i18n.tiktok-row.net` | `bpm-i18n.bytedance.net` | I18N |
| `US-TTP` | `ttp`, `usttp` | `bpm.tiktok-us.net` | `bpm-tx.tiktokd.net` | TTP-US |
| `US-TTP2` | `ttp2`, `usttp2` | `bpm.tiktok-us.net` | `bpm-tx.tiktokd.net` | TTP-US |
| `EU-TTP` | `euttp` | `bpm-eu.tiktok-eu.net` | `bpm-eu.tiktoke.org` | I18N |
| `EU-TTP2` | `euttp2` | `bpm-eu.tiktok-eu.net` | `bpm-eu.tiktoke.org` | I18N |

默认 VRegion 为 `China-North`。CLI 环境（办公网）自动选择办公网 URL。

## Input Schema

```json
{
  "type": "object",
  "required": ["action"],
  "properties": {
    "action": {
      "type": "string",
      "enum": ["get_detail", "list_records", "list_logs", "get_op_keys", "update_status", "cancel"],
      "description": "操作类型"
    },
    "workflow_id": {
      "type": "string",
      "description": "工单 ID（update_status / get_detail / cancel / list_logs 必填）"
    },
    "vregion": {
      "type": "string",
      "enum": ["China-North", "China-BOE", "US-BOE", "Singapore-Central", "US-East", "US-TTP", "US-TTP2", "EU-TTP", "EU-TTP2"],
      "default": "China-North",
      "description": "VRegion，决定 BPM 域名和 JWT 类型。支持别名：cn, boe, sg, us, ttp, euttp 等"
    },
    "status": {
      "type": "string",
      "description": "[update_status] 目标状态节点 key"
    },
    "op_key": {
      "type": "string",
      "description": "[update_status] 触发操作 key（如 'next'），下一步有多个操作时必传"
    },
    "current_status": {
      "type": "string",
      "description": "[update_status] 当前状态 key，用于并发校验"
    },
    "op_data": {
      "type": "object",
      "description": "[update_status] 操作参数"
    },
    "merge": {
      "type": "boolean",
      "description": "[update_status] 为 true 时将 op_data 合并到工单上下文"
    },
    "target_system": {
      "type": "string",
      "description": "[list_records] 租户名"
    },
    "workflow_config_id": {
      "type": "array",
      "items": { "type": "string" },
      "description": "[list_records] 流程配置 ID"
    },
    "finished": {
      "type": "array",
      "items": { "type": "string" },
      "description": "[list_records] 完成状态：0 未完成、1 已完成、2 强制关闭"
    },
    "creator": {
      "type": "string",
      "description": "[list_records] 创建人"
    },
    "assignee": {
      "type": "string",
      "description": "[list_records] 主处理人"
    },
    "multi_assignee": {
      "type": "string",
      "description": "[list_records] 按主处理人/当前处理人查询"
    },
    "search": {
      "type": "string",
      "description": "[list_records] 按环境变量搜索，格式 '\"key\":\"val\"'"
    },
    "workflow_key": {
      "type": "string",
      "description": "[list_records] 流程配置 key/name"
    },
    "start": {
      "type": "string",
      "description": "[list_records] 创建时间范围起始"
    },
    "end": {
      "type": "string",
      "description": "[list_records] 创建时间范围终止"
    },
    "page": {
      "type": "string",
      "default": "1",
      "description": "页码（list_records / list_logs）"
    },
    "page_size": {
      "type": "string",
      "default": "10",
      "description": "单页大小，最大 999（list_records / list_logs）"
    },
    "jwt": {
      "type": "string",
      "description": "个人 JWT，覆盖自动获取"
    },
    "target_addr": {
      "type": "string",
      "description": "完整根 URL（含 scheme），覆盖 vregion 映射"
    }
  }
}
```

## Output Schema

### get_detail

```json
{
  "success": true,
  "action": "get_detail",
  "base_url": "https://bpm.bytedance.net",
  "workflow_id": "879450",
  "data": {
    "id": 879450,
    "creator": "donghao.blueone",
    "assignee": "donghao.blueone",
    "status": "done",
    "status_name": "已完成",
    "workflow_config": 7461,
    "workflow_key": "workflow_config_O",
    "workflow_name": "多级审批流程",
    "target_system": "DH_test1",
    "finished": 1,
    "create_time": "2022-09-06T11:22:19+08:00",
    "update_time": "2022-09-06T11:22:32+08:00"
  }
}
```

### list_records

```json
{
  "success": true,
  "action": "list_records",
  "base_url": "https://bpm.bytedance.net",
  "data": [
    {
      "id": 879450,
      "creator": "donghao.blueone",
      "status": "approval3",
      "status_name": "固定负责人待审核",
      "workflow_name": "多级审批流程",
      "target_system": "DH_test1",
      "finished": 0
    }
  ],
  "page": {
    "total_items": 501,
    "current_page": 1,
    "total_page": 51,
    "page_size": 10
  }
}
```

### list_logs

```json
{
  "success": true,
  "action": "list_logs",
  "base_url": "https://bpm.bytedance.net",
  "workflow_id": "879450",
  "data": [
    {
      "id": 11424012,
      "creator": "donghao.blueone",
      "workflow": 879450,
      "tag": 1,
      "content": "同意: donghao.blueone 将流程状态从直属leader待审核变更为是否需要资源owner审核",
      "old_status": "直属leader待审核",
      "status": "是否需要资源owner审核",
      "create_time": "2022-09-24T18:24:05+08:00"
    }
  ],
  "page": {
    "total_items": 5,
    "current_page": 1,
    "total_page": 1,
    "page_size": 10
  }
}
```

### get_op_keys

```json
{
  "success": true,
  "action": "get_op_keys",
  "base_url": "https://bpm-i18n.tiktok-row.net",
  "workflow_id": "8403208",
  "data": [
    {
      "op_key": "approve",
      "op_name": "通过",
      "status": "resource_owner_approval_paas",
      "branch": "main",
      "button_type": "default",
      "type": "default",
      "current_status": "resource_owner_approval",
      "op_rule": "or"
    },
    {
      "op_key": "reject",
      "op_name": "拒绝",
      "status": "reject",
      "button_type": "default",
      "type": "default",
      "current_status": "resource_owner_approval",
      "op_rule": "or"
    }
  ]
}
```

### update_status / cancel

```json
{
  "success": true,
  "action": "update_status",
  "base_url": "https://bpm.bytedance.net",
  "workflow_id": "879450",
  "data": { "status": "pending1" }
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `action parameter is required` | 缺少 action | 添加 `action` 参数 |
| `workflow_id is required` | 缺少 workflow_id | 添加 `workflow_id` 参数 |
| `status is required for update_status` | update_status 缺少目标状态 | 添加 `status` 参数 |
| `invalid vregion` | 不支持的 vregion 值 | 参考 VRegion 区域映射表 |
| `auto JWT acquisition failed` | 自动获取 JWT 失败 | 运行 `gdpa-cli login` (CN: `login cn`, I18N: `login i18n`) |
| `permission denied` | 操作人无权限 | 确认为租户管理员或工单创建者 |
| `illegal next status` | 非法的后继状态 | 检查目标状态是否合法 |
| `Status has been changed` | 工单状态并发冲突 | 使用 `current_status` 校验后重试 |

## Notes

- 默认 VRegion 为 `China-North`，可通过 `vregion` 参数切换到 I18N / TTP / EU 环境
- JWT 根据 VRegion 自动选择类型（CN / I18N / TTP-US），无需手动传入
- 若自动获取 JWT 失败，运行 `gdpa-cli login cn`（CN 区域）或 `gdpa-cli login i18n`（国际区域）
- `target_addr` 可覆盖 VRegion 映射，用于自定义域名
- `finished` 字段含义：`0` 未完成、`1` 已完成、`2` 强制关闭
