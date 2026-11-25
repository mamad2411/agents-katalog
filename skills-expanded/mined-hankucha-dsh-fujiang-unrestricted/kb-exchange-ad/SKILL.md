---
name: kb-exchange-ad
description: CVE/PoC 知识库 · Exchange 与 Windows/AD：ProxyLogon(2021-26855)、ProxyShell(2021-34473)、ProxyNotShell(2022-41040)、ViewState(2020-0688)、Zerologon(2020-1472)、noPac(2021-42287)、AD CS ESC、PrintNightmare(2021-34527)、MS17-010、Follina(2022-30190)。每条都有对应 PoC；公开资料整理，verified=false。
verified: false
sources: 公开资料整理（CVE 公告 / 公开分析 / 业务逻辑类；出处见各条参考）
---

# Exchange / Windows / AD（14 条）
> 条目为公开资料整理（出处见文末「参考」），`利用步骤` 属待验证假设；出报告前按目标版本自验并把 `verified` 置为 true。

两条主线：
1. **不需凭据的外场入口**（Exchange 代理漏洞、MS17-010、Zerologon）——优先做最小影响验证。
2. **有凭据后的域内提权**（noPac、AD CS、Kerberoast、DCSync）——从普通域用户到域管。

## 条目

| 文件 | 漏洞 | 严重度 | 入口 |
|---|---|---|---|
| `adcs-esc1-esc8.md` | AD CS 证书滥用（ESC1 / ESC8 等） | critical | - |
| `cve-2017-0144-eternalblue.md` | EternalBlue（MS17-010 SMBv1 远程溢出） | critical | - |
| `cve-2020-0688-exchange-viewstate.md` | Exchange ViewState 反序列化（静态 machineKey） | critical | web.config 静态 machineKey + ysoserial.net 载荷 |
| `cve-2020-1472-zerologon.md` | Zerologon（Netlogon 密钥置零 → 域控接管） | critical | - |
| `cve-2021-26855-proxylogon.md` | Exchange ProxyLogon（SSRF + 任意文件写入 → RCE） | critical | - |
| `cve-2021-34473-proxyshell.md` | Exchange ProxyShell（三个洞串联 → RCE） | critical | - |
| `cve-2021-34527-printnightmare.md` | PrintNightmare（打印后台服务任意 DLL 加载） | critical | - |
| `cve-2021-42287-nopac.md` | noPac（sAMAccountName 伪装 + 无 PAC 票据 → 域管） | critical | - |
| `cve-2021-42321-exchange-deser.md` | Exchange 认证后反序列化 RCE（CVE-2021-42321） | critical | EWS 请求体里的 .NET 序列化 blob |
| `cve-2022-30190-follina.md` | MSDT 协议远程代码执行（Follina） | critical | 文档里引用 ms-msdt:/id PCWDiagnostic |
| `cve-2022-41040-proxynotshell.md` | Exchange ProxyNotShell（SSRF + PowerShell 远程） | critical | autodiscover 的 @ 绕过 + /powershell 端点 |
| `cve-2024-21410-exchange-ntlm-relay.md` | Exchange EWS NTLM 中继提权（CVE-2024-21410） | critical | /ews/exchange.asmx 允许 NTLM 中继 |
| `cve-2024-21413-outlook-monikerlink.md` | Outlook MonikerLink 绕过与 NTLM 泄露（CVE-2024-21413） | critical | file:// 后加 ! 绕过 Protected View |
| `cve-2024-45519-zimbra-postjournal.md` | Zimbra postjournal 未授权命令执行（CVE-2024-45519） | critical | 向 postjournal 发含 base64 命令的 SMTP 收件人 |

## 用这一页的方法

- 先分清「拿机器」和「拿域」：机器权限只给你一个立足点，域权限才给全森林。
- Exchange 的洞打完必须**清 webshell 与提权后门**（`/owa/auth/*.aspx`、`/aspnet_client/`），否则下一次扫描还会命中。
- 域内操作一律先看日志与告警条件（4768/4769/4624/7045），再决定用哪种票据形态。
