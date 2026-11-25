---
name: tce
description: Query TCE service deployments, cluster details, Pod information, and deployment tickets. Use whenever the user mentions TCE, wants to check service deployment status, view Pod information or Pod list, check cluster details or instances, verify user permissions on a service, troubleshoot deployment or service issues, or query deployment tickets. Also trigger when the user asks about a service's clusters, Pod states, or deployment operations.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# TCE 服务部署查询

查询 TCE 服务的部署信息，包括服务搜索、服务详情、集群配置、Pod 实例状态等。

> **何时使用**: 查看 TCE 服务部署状态、集群配置、Pod 实例信息，或按 PSM 搜索服务。

## 使用方法

```bash
gdpa-cli run tce --session-id "$SESSION_ID" --input '{"action": "<action>", ...}'
```

## 支持的 Action

| Action | 描述 | 必填参数 | 可选参数 |
|--------|------|----------|----------|
| `list_services` | 搜索/列出 TCE 服务 | `psm` | `page`, `page_size`, `vregion` |
| `get_service_detail` | 获取服务详情 | `service_id` | `vregion` |
| `list_service_clusters` | 获取服务的集群列表 | `service_id` | `page`, `page_size`, `vregion` |
| `list_cluster_instances` | 获取集群的 Pod 实例列表 | `cluster_id` | `vregion` |
| `get_pod_readiness_msg` | 获取 Pod 就绪检查信息 | `pod_names` | `vregion` |

## Input Schema

```json
{
  "type": "object",
  "required": ["action"],
  "properties": {
    "action": {
      "type": "string",
      "enum": ["list_services", "get_service_detail", "list_service_clusters", "list_cluster_instances", "get_pod_readiness_msg"],
      "description": "操作类型"
    },
    "psm": {
      "type": "string",
      "description": "服务 PSM 名称（list_services 时必填）"
    },
    "service_id": {
      "type": "integer",
      "description": "TCE 服务 ID（get_service_detail / list_service_clusters 时必填）"
    },
    "cluster_id": {
      "type": "integer",
      "description": "TCE 集群 ID（list_cluster_instances 时必填）"
    },
    "pod_names": {
      "type": "string",
      "description": "Pod 名称，多个用逗号分隔（get_pod_readiness_msg 时必填）"
    },
    "page": {
      "type": "integer",
      "default": 1,
      "description": "分页页码"
    },
    "page_size": {
      "type": "integer",
      "default": 20,
      "description": "每页条数"
    },
    "vregion": {
      "type": "string",
      "default": "China-BOE",
      "description": "目标区域。别名：'sg'→Singapore-Central, 'us'→US-East, 'cn'→China-North, 'boe'→China-BOE, 'ttp'→US-TTP"
    }
  }
}
```

## 典型工作流

```
1. list_services     → 通过 PSM 搜索服务，获取 service_id
2. get_service_detail → 查看服务详情（部署状态、SCM 版本、Owner 等）
3. list_service_clusters → 查看集群列表（VRegion、资源配额、副本数等）
4. list_cluster_instances → 查看具体 Pod 状态（IP、CPU/内存使用率、容器状态等）
5. get_pod_readiness_msg → 查看 Pod 就绪检查结果（容器环境、服务启动、端口、组件等）
```

---

## Action 详细说明

### 1. 搜索服务 (list_services)

通过 PSM 名称搜索 TCE 服务。

```bash
gdpa-cli run tce --session-id "$SESSION_ID" --input '{
  "action": "list_services",
  "psm": "tiktok.example.service",
  "vregion": "sg"
}'
```

**响应示例：**

```json
{
  "success": true,
  "action": "list_services",
  "data": {
    "services": [
      {
        "id": 315389,
        "psm": "tiktok.example.service",
        "name": "example-service",
        "status": "Running",
        "status_display": "运行中"
      }
    ],
    "total": 1,
    "query_vregion": "Singapore-Central"
  }
}
```

### 2. 查看服务详情 (get_service_detail)

获取服务的完整信息，包括部署状态、SCM 版本、Owner 等。

```bash
gdpa-cli run tce --session-id "$SESSION_ID" --input '{
  "action": "get_service_detail",
  "service_id": 315389,
  "vregion": "sg"
}'
```

**响应示例：**

```json
{
  "success": true,
  "action": "get_service_detail",
  "data": {
    "id": 315389,
    "psm": "tiktok.example.service",
    "status": "Running",
    "auth": {
      "owner_name": "user1",
      "owners": ["user1", "user2"]
    },
    "build": {
      "language": "go",
      "tech_stack": "gdp",
      "scm_repos": [{"name": "example-repo", "path": "code.byted.org/tiktok/example"}]
    },
    "runtime": {
      "image_version": "1.0.0.213",
      "cluster_ids": [1650885]
    },
    "query_vregion": "Singapore-Central"
  }
}
```

### 3. 查看服务集群 (list_service_clusters)

获取服务下的集群列表，包含集群状态、资源配额、副本数等。

```bash
gdpa-cli run tce --session-id "$SESSION_ID" --input '{
  "action": "list_service_clusters",
  "service_id": 315389,
  "vregion": "sg"
}'
```

**响应示例：**

```json
{
  "success": true,
  "action": "list_service_clusters",
  "data": {
    "clusters": [
      {
        "id": 1650885,
        "name": "default",
        "status": "Running",
        "resource": {
          "vregion": "Singapore-Central",
          "zone": "sg1",
          "cpu": 4,
          "mem": 8192,
          "cpu_usage": 35.2,
          "mem_usage": 60.1
        },
        "runtime": {
          "image_version": "1.0.0.213",
          "dc_info": [{"idc": "sg1", "replicas": 3, "current_count": 3}]
        }
      }
    ],
    "total": 1,
    "query_vregion": "Singapore-Central"
  }
}
```

### 4. 查看 Pod 实例 (list_cluster_instances)

获取集群下的 Pod 实例列表，包含 Pod IP、CPU/内存使用率、容器状态等。

```bash
gdpa-cli run tce --session-id "$SESSION_ID" --input '{
  "action": "list_cluster_instances",
  "cluster_id": 1650885,
  "vregion": "sg"
}'
```

**响应示例：**

```json
{
  "success": true,
  "action": "list_cluster_instances",
  "data": {
    "instance_groups": [
      {
        "desc": "sg1 deployment",
        "idc": "sg1",
        "cpu_usage_pct": 35.2,
        "mem_usage_pct": 60.1,
        "pods": [
          {
            "pod_name": "example-service-xxx-yyy",
            "pod_ip": "10.0.0.1",
            "pod_status": "Running",
            "vregion": "Singapore-Central",
            "containers": [
              {
                "name": "main",
                "status": "Running",
                "cpu_usage_pct": 35.2,
                "mem_usage_pct": 60.1
              }
            ]
          }
        ],
        "pod_count": 1
      }
    ],
    "total_groups": 1,
    "query_vregion": "Singapore-Central"
  }
}
```

### 5. 查看 Pod 就绪检查信息 (get_pod_readiness_msg)

获取指定 Pod 的就绪检查结果，包括容器环境检查、服务启动检查、端口检查、第三方组件检查等。适用于排查 Pod 启动失败原因。

```bash
gdpa-cli run tce --session-id "$SESSION_ID" --input '{
  "action": "get_pod_readiness_msg",
  "pod_names": "dp-bf5f17ca5b-94b8d4b8d-x8d84",
  "vregion": "sg"
}'
```

**响应示例：**

```json
{
  "success": true,
  "action": "get_pod_readiness_msg",
  "data": {
    "pods": [
      {
        "pod_name": "dp-bf5f17ca5b-94b8d4b8d-x8d84",
        "format": true,
        "check_list": [
          {"name": "容器环境检查", "stage": 0, "status": "passed"},
          {
            "name": "服务启动检查",
            "stage": 1,
            "status": "failed",
            "msg": "业务进程发生panic...",
            "oncall": "tce_platform oncall",
            "doc_link": "https://cloud.bytedance.net/docs/...",
            "doc_title": "业务服务进程启动失败"
          },
          {"name": "服务端口检查", "stage": 2, "status": "failed", "msg": "服务配置的端口未正常监听..."},
          {"name": "第三方组件检查", "stage": 3, "status": "failed", "msg": "bytemesh 尚未Ready..."},
          {"name": "其他检查", "stage": 4, "status": "pending"}
        ]
      }
    ],
    "total": 1
  }
}
```

**check_list 状态说明：**

| status | 含义 |
|--------|------|
| `passed` | 检查通过 |
| `failed` | 检查失败，`msg` 字段包含详细错误信息 |
| `pending` | 检查尚未执行（前序检查未通过时后续检查可能为 pending） |

## VRegion 映射

| VRegion | 别名 | 说明 | 网关 |
|---------|------|------|------|
| `China-BOE` | `boe` | CN BOE 环境（默认） | cloud-boe.bytedance.net |
| `US-BOE` | `usboe`, `boei18n` | 国际 BOE 环境 | cloud-boe.bytedance.net |
| `China-North` | `cn` | CN 生产环境 | cloud.bytedance.net |
| `China-East` | `chinaeast` | CN 华东 | cloud.bytedance.net |
| `Singapore-Central` | `sg` | 新加坡 | bc-sg-gw.tiktok-row.net |
| `US-East` | `us` | 美东 | bc-sg-gw.tiktok-row.net |
| `US-TTP` | `ttp`, `usttp` | 美国合规区 | cloud.tiktok-us.net |
| `US-TTP2` | `usttp2` | 美国合规区 2 | cloud.tiktok-us.net |
| `EU-TTP2` | `euttp2` | 欧洲合规区 | bc-iedt-gw.tiktok-eu.net |
| `US-EastRed` | `useastred` | 美东 Red | bc-iedt-gw.tiktok-eu.net |

## ⚠️ service_id / cluster_id 适用范围

**不同 VRegion 的 service_id 和 cluster_id 互不通用**。在 China-BOE 查到的 service_id 不能用于 Singapore-Central 的查询。每次跨 VRegion 查询时，必须先用 `list_services` 在该 VRegion 下重新获取 service_id。

所有返回结果均包含 `query_vregion` 字段，标明当前结果所属 VRegion。

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `action parameter is required` | 缺少 action | 指定 action 参数 |
| `psm parameter is required` | list_services 缺少搜索关键字 | 添加 `psm` 参数 |
| `service_id parameter is required` | 缺少服务 ID | 先用 `list_services` 获取 service_id |
| `cluster_id parameter is required` | 缺少集群 ID | 先用 `list_service_clusters` 获取 cluster_id |
| `pod_names parameter is required` | 缺少 Pod 名称 | 先用 `list_cluster_instances` 获取 pod_name |
| `authentication failed` | JWT 获取失败 | 运行 `gdpa-cli login` 先登录 |
| `unsupported vregion` | VRegion 不支持 | 检查 VRegion 拼写，参考上方映射表 |

## 注意事项

- **默认 VRegion** 为 `China-BOE`（BOE 测试环境），查询生产环境请显式指定 `vregion`
- 只读查询，不支持修改服务配置
- 需要先通过 `gdpa-cli login` 登录获取认证凭据
