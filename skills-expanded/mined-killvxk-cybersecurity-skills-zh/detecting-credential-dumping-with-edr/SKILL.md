---
name: detecting-credential-dumping-with-edr
description: 使用 EDR 遥测和 Sysmon 日志检测操作系统凭据转储技术，包括 LSASS 访问、SAM 提取和 DCSync。
domain: cybersecurity
subdomain: threat-hunting
tags: [threat-hunting, mitre-attack, credential-dumping, edr, lsass, t1003, proactive-detection]
version: "1.0"
author: mahipal
license: Apache-2.0
---

# 使用 EDR 检测凭据转储

## 适用场景

- 在受攻击环境中主动狩猎后渗透凭据盗取活动时
- 在 EDR 告警中检测到可疑 LSASS 进程访问后
- 调查潜在 Active Directory 入侵时
- 事件响应（Incident Response）期间确定凭据暴露范围时
- 主动跨终端狩猎 T1003 子技术时

## 前置条件

- 具备进程访问监控的 EDR 平台（CrowdStrike、MDE、SentinelOne）
- 已为 LSASS 配置事件 ID 10（进程访问）的 Sysmon
- 启用命令行审计的 Windows 安全事件日志 4688
- Active Directory 事件转发用于 DCSync 检测（事件 ID 4662）
- SAM 注册表访问的 Windows 安全事件日志 4656/4663

## 工作流程

1. **识别凭据转储向量**：映射与您环境相关的 T1003 子技术（LSASS 内存、SAM、NTDS、DCSync、/etc/passwd、缓存凭据）。
2. **查询 LSASS 访问事件**：搜索目标镜像为 lsass.exe 且具有可疑 GrantedAccess 掩码（0x1010、0x1038、0x1FFFFF）的 Sysmon 事件 ID 10。
3. **分析进程上下文**：检查访问 LSASS 的源进程——合法安全工具与未知或可疑二进制文件。
4. **狩猎 SAM/NTDS 访问**：查询针对 SAM/SECURITY/SYSTEM 注册表 hive 的 reg.exe 保存操作以及 ntdsutil/vssadmin 卷影副本访问。
5. **检测 DCSync 活动**：监控来自非域控制器源的 DS-Replication-Get-Changes 请求（事件 ID 4662）。
6. **与网络活动关联**：将凭据转储与后续横向移动（Lateral Movement）或身份验证异常交叉关联。
7. **评估影响并报告**：确定哪些凭据可能已暴露，并建议密码重置和遏制措施。

## 核心概念

| 概念 | 描述 |
|------|------|
| T1003 | 操作系统凭据转储（OS Credential Dumping）——父技术 |
| T1003.001 | LSASS 内存——从 LSASS 进程转储凭据 |
| T1003.002 | 安全账户管理器（SAM）——提取本地密码哈希 |
| T1003.003 | NTDS——从域控制器提取 AD 数据库 |
| T1003.004 | LSA Secrets——访问存储的服务凭据 |
| T1003.005 | 缓存的域凭据（DCC2） |
| T1003.006 | DCSync——通过 DRSUAPI 复制 AD 凭据 |
| LSASS | 本地安全授权子系统服务（Local Security Authority Subsystem Service） |
| GrantedAccess | 表示进程请求访问权限的位掩码 |
| Minidump | comsvcs.dll 等工具使用的内存转储技术 |

## 工具与系统

| 工具 | 用途 |
|------|------|
| CrowdStrike Falcon | LSASS 访问检测和进程树分析 |
| Microsoft Defender for Endpoint | 凭据访问事件的高级狩猎 |
| Sysmon | 进程访问监控（事件 ID 10） |
| Velociraptor | LSASS 分析的终端工件收集 |
| Elastic Security | 凭据转储指标的关联分析 |
| Splunk | 凭据访问事件分析的 SPL 查询 |
| Volatility | LSASS 凭据提取的内存取证 |

## 常见场景

1. **Mimikatz LSASS 转储**：攻击者运行 `sekurlsa::logonpasswords`，导致直接 LSASS 内存读取，GrantedAccess 为 0x1010。
2. **Comsvcs.dll MiniDump**：进程使用 `rundll32.exe comsvcs.dll MiniDump [LSASS PID]` 创建 LSASS 内存转储文件。
3. **ProcDump LSASS**：攻击者使用 Microsoft 签名的 procdump.exe 带 `-ma lsass.exe` 参数转储 LSASS 内存。
4. **SAM 注册表导出**：攻击者运行 `reg save HKLM\SAM sam.bak` 提取本地密码哈希。
5. **DCSync 复制**：拥有复制目录更改权限的受攻击账户从工作站执行 DCSync。
6. **NTDS 卷影副本**：攻击者使用 `vssadmin create shadow /for=C:` 然后从卷影副本复制 ntds.dit。

## 输出格式

```
Hunt ID: TH-CRED-DUMP-[DATE]-[SEQ]
Technique: T1003.[子技术]
Source Process: [访问 LSASS/SAM/NTDS 的进程]
Target: [lsass.exe / SAM / NTDS.dit / DC 复制]
Host: [主机名]
User: [账户上下文]
GrantedAccess: [访问掩码（如适用）]
Timestamp: [UTC]
Risk Level: [Critical/High/Medium/Low]
Evidence: [日志条目、进程树、网络活动]
Recommended Action: [密码重置范围、遏制步骤]
```
