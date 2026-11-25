---
name: re-flow-capture
description: 网络抓包流程——编排网络层取证：明文 HTTP 用 Wireshark Follow TCP Stream、HTTPS 用 Fiddler/mitmproxy 加根证书、直连程序用 Proxifier 强制转发、证书校验与自定义协议用 Frida 在 API 层取明文。当用户要求"抓包、看程序发出什么请求、HTTPS 解密、协议分析"，或 re-flow-orchestrator 进入 CAPTURE 阶段时使用。触发词：抓包、网络请求、HTTPS、流量、Fiddler、Wireshark、证书校验、协议。
agent_created: true
x-alice-class: reverse
---# 抓包流程（re-flow-capture）

## 单一职责

只做一件事：**拿到目标程序网络通信的明文证据**。

## 触发条件

- 用户："抓包 / 看它发出什么请求 / HTTPS 能不能解密"
- re-flow-orchestrator 进入 CAPTURE 阶段
- re-flow-recon 报告显示存在联网验证或激活时联网

## 输入与输出

- **输入**：目标进程名或 exe 路径 + 侦察报告中的连接信息（域名 / IP / 端口 / 协议）
- **输出**：流量证据包——pcap 文件、明文请求响应日志、自定义协议时的字段结构说明；状态流转标记 `CAPTURE → UNPACK | BYPASS`

## 执行步骤（按序，遇阻再进下一级）

1. **明文 HTTP**：Wireshark 捕获，过滤 `ip.addr == 目标IP`，右键 Follow TCP Stream 看全文
2. **HTTPS**：Fiddler / mitmproxy 开系统代理 + 根证书导入受信任存储；.NET 与 WinINet 程序走系统证书链，可直接解密
3. **程序直连不走代理**：Proxifier 加规则"目标 exe → 转发 127.0.0.1:8888"
4. **TLS 断连或密文**：命中证书校验（pinning）—— Frida hook 校验回调强制通过（.NET 为 `ServerCertificateValidationCallback`）
5. **自定义二进制协议**：Frida hook `WSASend` / `WSARecv` / `send` / `recv`，dump **加密前、解密后**的明文 buffer
6. **归档**：证据写任务目录 `capture/`，每条请求标注触发动作（启动 / 点击激活 / 提交授权码）

## 关键要点

- VMP 等虚拟化保护下，网络验证逻辑静态不可见，**hook 点选在系统 API 层**（WinHTTP / WinINet / socket），这是虚拟化够不到的边界
- 抓包结论直接决定 BYPASS 阶段的 hook 目标：能伪造响应就无需碰程序

## 边界与上下游

- **前置**：re-flow-recon（提供连接信息）；re-tool-manifest（Wireshark/Fiddler/Frida 就位）
- **后继**：re-flow-unpack（需静态深入时）；或直接 BYPASS（伪造响应即可绕过时）
- **深度参考**：windows-license-crack 的 `references/vmprotect.md` 抓包章节
