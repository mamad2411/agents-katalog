---
name: kb-edge-device
description: CVE/PoC 知识库 · 边界设备与远程运维：PAN-OS(2024-3400)、Ivanti(2023-46805+2024-21887)、Pulse 文件读(2019-11510)、Citrix 路径穿越(2019-19781)、FortiOS 管理面绕过(2022-40684)/穿越(2018-13379)/2FA 绕过(2020-12812)、F5 iControl(2022-1388/2021-22986)/TMUI(2020-5902)。每条都有对应 PoC；公开资料整理，verified=false。
verified: false
sources: 公开资料整理（CVE 公告 / 公开分析 / 业务逻辑类；出处见各条参考）
---

# 边界设备 / VPN / 负载均衡（16 条）
> 条目为公开资料整理（出处见文末「参考」），`利用步骤` 属待验证假设；出报告前按目标版本自验并把 `verified` 置为 true。

这类目标的价值不在单机权限，而在**会话与凭据**：SSL VPN 的内存里活着所有人的令牌，ADC 的配置里躺着后端地址与证书，防火墙的管理面往往直通内网核心。

## 条目

| 文件 | 漏洞 | 严重度 | 入口 |
|---|---|---|---|
| `cve-2018-13379-fortinet-fortios.md` | FortiOS SSL VPN 路径穿越（凭据读取） | critical | - |
| `cve-2019-11510-pulse-secure-file-read.md` | Pulse Secure 任意文件读取（凭据与会话） | critical | /dana-na/../dana/html5acc/guacamole/ 穿越 |
| `cve-2019-19781-citrix-path-traversal.md` | Citrix ADC 路径穿越 → 模板注入 RCE | critical | - |
| `cve-2020-12812-fortios-2fa-case-bypass.md` | FortiOS SSL VPN 双因素绕过（用户名大小写） | high | 改用户名大小写跳过 2FA |
| `cve-2020-5902-f5-tmui.md` | F5 BIG-IP TMUI 未授权 RCE（..;/ 路径穿越） | critical | /tmui/login.jsp/..;/tmui/locallb/workspace/tmshCmd.jsp |
| `cve-2021-22986-f5-icontrol.md` | F5 iControl REST 未授权 RCE（2021 变体） | critical | POST /mgmt/tm/util/bash 带假 token |
| `cve-2022-1388-f5-icontrol.md` | F5 BIG-IP iControl REST 认证绕过 → 命令执行 | critical | - |
| `cve-2022-40684-fortios-auth-bypass.md` | FortiOS / FortiProxy 管理面认证绕过（假 Forwarded 头） | critical | Forwarded: for="127.0.0.1" 冒充本地 |
| `cve-2023-35078-ivanti-epmm-auth-bypass.md` | Ivanti EPMM 认证绕过（CVE-2023-35078） | critical | /mifs/aad/api/v2/admins/users 未授权 |
| `cve-2023-46805-2024-21887-ivanti.md` | Ivanti Connect Secure 认证绕过 + 命令注入（串联） | critical | - |
| `cve-2023-48788-forticlient-ems-sqli.md` | FortiClient EMS SQL 注入 → 未认证 RCE（CVE-2023-48788） | critical | /api/v1/fortitray/installer 的 multipart 字段注入 |
| `cve-2024-0012-panos-auth-bypass.md` | PAN-OS 管理面认证绕过 → root RCE（CVE-2024-0012 + CVE-2024-9474） | critical | /php/ztp_gate.php?PanGPSRunning=true 绕过认证 → 用 /php/utils.php 提权 |
| `cve-2024-0204-goanywhere-auth-bypass.md` | GoAnywhere MFT 认证绕过 → 新建管理员（CVE-2024-0204） | critical | /goanywhere/images/..;/wizard/InitialAccountSetup.xhtml |
| `cve-2024-24919-checkpoint-quantum.md` | Check Point Quantum 安全网关任意文件读（CVE-2024-24919） | critical | POST /clients/MyCRL 的 a 参数读任意文件 |
| `cve-2024-3400-panos-globalprotect.md` | PAN-OS GlobalProtect 命令注入 | critical | - |
| `cve-2024-47575-fortimanager-fortijump.md` | FortiManager 未认证 RCE（FortiJump，CVE-2024-47575） | critical | FGFM（541）协议未认证注册 → 下发脚本 |

## 用这一页的方法

1. **先认设备再打洞**：登录页特征 + 版本接口，别把 PAN-OS 的 PoC 打到 FortiGate 上。
2. 设备类目标优先做**只读取证**（配置导出、会话表），破坏性利用（改策略、删证书）放最后。
3. 打之前确认是否在生产链路：VPN/ADC 一旦崩，整条业务断。选低峰窗口，先在不影响的节点验。
4. 拿到设备后第一件事：导配置（含本地账号与哈希）、抓 `sslvpn_websession` / `SESSID` 表，用来横向到内网。
