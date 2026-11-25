---
name: detecting-golden-ticket-attacks
description: >-
  通过分析 Windows 安全事件日志中的异常 TGT 使用模式，检测 Kerberos 黄金票据（Golden Ticket）攻击。从 EVTX 文件中解析事件 ID 4624、4672 和 4768，识别具有异常生命周期的票据、域 SID 不匹配，以及非管理员账户无对应组成员身份变更却获得管理员级别权限的特权提升序列。
domain: cybersecurity
subdomain: security-operations
tags: [detecting, golden, ticket, attacks]
version: "1.0"
author: mahipal
license: Apache-2.0
---

## 使用说明

1. 安装依赖：`pip install python-evtx lxml`
2. 从域控制器收集 Windows Security EVTX 日志。
3. 解析事件 ID：
   - 4768：Kerberos TGT 请求（认证服务请求）
   - 4624：登录事件（查找使用 NTLM 或 Kerberos 的 LogonType 3）
   - 4672：特殊权限分配（管理员登录指标）
4. 检测黄金票据指标：
   - 有效期超过 10 小时的 TGT（默认最大值为 10 小时）
   - 非 Domain Admins 成员账户触发事件 4672
   - 无对应 4768 TGT 请求的登录事件
   - 票据数据中的域 SID 不一致
5. 生成带有时间线重建的检测报告。

```bash
python scripts/agent.py --evtx-file /path/to/Security.evtx --output golden_ticket_report.json
```

## 示例

### 检测异常权限分配
标准用户账户触发事件 4672 并获得 SeDebugPrivilege、SeTcbPrivilege 或 SeBackupPrivilege，表明可能存在黄金票据使用。

### 无对应 AS-REQ 的 TGT
使用 Kerberos 认证的登录事件（4624）但域控制器上没有匹配的 4768（TGT 请求），说明可能是伪造的 TGT。
