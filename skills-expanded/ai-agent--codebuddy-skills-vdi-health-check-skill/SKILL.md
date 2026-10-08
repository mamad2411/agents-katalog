# VDI 健康检查 Skill

通过 MCP Server 调用 VDI 系统健康检查接口，查询系统各项监控状态。

## 使用场景

- 查询 VDI 系统 CPU、内存、存储、网络等健康状态
- 排查系统异常，定位故障原因
- 定期巡检，生成健康报告

## 工作原理

此 Skill 调用本地 MCP Server (`vdi-checkhealthy`)，由 MCP Server 通过 HTTP Digest Auth 访问 VDI API。

## 前置条件

1. 确保 MCP Server 已注册到 OpenClaw：
   ```bash
   openclaw mcp add vdi-checkhealthy \
     /Users/kirito/repos/ai-agent/python-study/mcp_servers/venv/bin/python3 \
     /Users/kirito/repos/ai-agent/python-study/mcp_servers/vdi_checkhealthy_server.py
   ```
   或者在 openclaw 配置文件中添加：
   ```json
    "vdi-checkhealthy": {
        "url": "http://127.0.0.1:8765/mcp"
      }
   ```

2. 确保 VDI API 可访问：`http://172.53.3.107:8083`

## 工具

### check_healthy

检查 VDI 系统各项健康状态。

**参数：**
- `items` (可选): 指定检查项，如不指定则检查全部 24 项
- `raw` (可选): `true` 返回原始 JSON，`false` 返回格式化报告（默认）

**调用示例：**
```
检查全部健康状态
```
```
只检查 CPU 和内存状态
items: ["cpuStatus", "memStatus"]
```
```
获取原始 JSON 数据
raw: true
```

**返回格式（格式化模式）：**
```
==================================================
VDI 系统健康检查报告
==================================================

🔴 异常 (2 项)
  • CPU 资源超配状态: ❌ 异常
    原因: 部分主机 CPU 资源超配比例大于 200%

🟡 警告 (1 项)
  • 存储空间状态: ⚠️ 警告
    原因: 存储使用率超过 80%

🟢 正常 (21 项)
  • 内存资源超配状态: ✅ 正常
  • ...

--------------------------------------------------
总计: 24 项 | 🟢 正常 21 | 🟡 警告 1 | 🔴 异常 2
```

**状态码说明：**
- `✅ 正常` (status=1): 检查项正常
- `⚠️ 警告` (status=2): 存在潜在问题
- `❌ 异常` (status=3): 严重问题需要处理

### list_items

列出所有可用的健康检查项及其说明。

**参数：** 无

## 检查项说明

| 键值 | 中文名称 | 说明 |
|-----|---------|------|
| cpuStatus | CPU 资源超配状态 | CPU 超配比例是否合理 |
| memStatus | 内存资源超配状态 | 内存超配比例是否合理 |
| memHwCheck | 内存硬件检查 | 内存硬件是否正常 |
| storeStatus | 存储资源超配状态 | 存储超配比例是否合理 |
| storageSpace | 存储空间状态 | 存储使用率 |
| netProcess | 网络进程状态 | 网络相关进程是否运行 |
| ntpStatus | NTP 时间同步状态 | 时间同步是否正常 |
| hostStatus | 主机状态 | 宿主机状态 |
| drsStatus | DRS 状态 | 动态资源调度状态 |
| warnConfigStatus | 告警配置状态 | 告警配置是否正确 |
| wsServeComponentStatus | ws 服务组件状态 | ws 服务组件健康状态 |
| clServeComponentStatus | cl 服务组件状态 | cl 服务组件健康状态 |
| xnServeComponentStatus | xn 服务组件状态 | xn 服务组件健康状态 |
| ypServeComponentStatus | yp 服务组件状态 | yp 服务组件健康状态 |
| hostResourceStatus | 主机资源状态 | 主机资源使用情况 |
| emergencyAlertStatus | 应急告警状态 | 应急告警是否正常 |
| redisStatus | Redis 状态 | Redis 服务状态 |
| licenseCheck | License 检查 | License 是否有效 |
| domainStatus | 域名状态 | 域名解析状态 |
| cvmBackupStatus | CVM 备份状态 | 云虚拟机备份状态 |
| imageStorageStatus | 镜像存储状态 | 镜像存储状态 |
| terminalStorageStatus | 终端存储状态 | 终端存储状态 |
| uploadStorageStatus | 上传存储状态 | 上传存储空间状态 |
| cloudDeskStatus | 云桌面状态 | 云桌面运行状态 |
| clientStatus | 客户端状态 | 客户端连接状态 |

## 故障排查

**问题：返回"无法连接到服务器"**
- 检查 IP 和端口是否正确：`http://172.53.3.107:8083`
- 检查网络是否可达

**问题：返回"认证失败"**
- 检查账号密码是否正确
- 确认 Digest Auth 认证方式是否正确

**问题：MCP Server 未注册**
- 按照前置条件中的命令重新注册
- 重启 OpenClaw Gateway
