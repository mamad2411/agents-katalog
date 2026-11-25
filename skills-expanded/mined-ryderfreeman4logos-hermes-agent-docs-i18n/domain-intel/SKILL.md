---
name: domain-intel
description: Passive recon of subdomains, SSL certs, WHOIS, and DNS.
version: 1.0.0
author: FurkanL0, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Domains, OSINT, DNS, Research]
    related_skills: []
---

# 域名情报——被动式开源情报收集

仅使用 Python 标准库即可实现被动式域名侦察。
**无需任何依赖，也不需要 API 密钥。可在 Linux、macOS 和 Windows 系统上运行。**

## 辅助脚本

该功能包含 `scripts/domain_intel.py` —— 一款用于执行所有域名情报操作的完整命令行工具。

```bash
# Subdomain discovery via Certificate Transparency logs
python SKILL_DIR/scripts/domain_intel.py subdomains example.com

# SSL certificate inspection (expiry, cipher, SANs, issuer)
python SKILL_DIR/scripts/domain_intel.py ssl example.com

# WHOIS lookup (registrar, dates, name servers — 100+ TLDs)
python SKILL_DIR/scripts/domain_intel.py whois example.com

# DNS records (A, AAAA, MX, NS, TXT, CNAME)
python SKILL_DIR/scripts/domain_intel.py dns example.com

# Domain availability check (passive: DNS + WHOIS + SSL signals)
python SKILL_DIR/scripts/domain_intel.py available coolstartup.io

# Bulk analysis — multiple domains, multiple checks in parallel
python SKILL_DIR/scripts/domain_intel.py bulk example.com github.com google.com
python SKILL_DIR/scripts/domain_intel.py bulk example.com github.com --checks ssl,dns
```

`SKILL_DIR` 是包含该 SKILL.md 文件的目录。所有输出均为结构化的 JSON 格式。

## 可用命令

| 命令 | 功能说明 | 数据来源 |
|---------|-----------|-----------|
| `subdomains` | 从证书日志中查找子域名 | crt.sh（HTTPS） |
| `ssl` | 检查 TLS 证书的详细信息 | 直接连接目标服务器的 TCP:443 端口 |
| `whois` | 查看注册信息、注册商及相关日期 | WHOIS 服务器（TCP:43） |
| `dns` | 查询 A、AAAA、MX、NS、TXT、CNAME 记录 | 系统 DNS + Google DoH |
| `available` | 检查域名是否已注册 | DNS、WHOIS 及 SSL 信号 |
| `bulk` | 对多个域名同时执行多项检测 | 上述所有数据源 |

## 何时使用本技能与内置工具

- 针对基础设施相关问题（如子域名、SSL 证书、WHOIS、DNS 记录及域名可用性），请**使用本技能**；
- 若需了解某个域名或公司的基本信息，建议**使用 `web_search`** 进行搜索；
- 如需获取网页的实际内容，可**使用 `web_extract`**；
- 对于简单的“该 URL 是否可访问”检测，可直接**使用 `terminal` 结合 `curl -I` 命令**。

| 任务 | 更佳工具 | 原因 |
|------|-----------|------|
| “example.com是做什么的？” | `web_extract` | 能获取页面内容，而非DNS/WHOIS数据 |
| “查找某家公司的信息” | `web_search` | 适用于通用信息检索，而非特定域名查询 |
| “这个网站安全吗？” | `web_search` | 声誉检测需要网页上下文支持 |
| “检查某个URL是否可访问” | 配合`curl -I`的`terminal` | 简单的HTTP状态检测 |
| “查找X的所有子域名” | **该技能** | 仅此方式能为该需求提供被动信息来源 |
| “SSL证书何时过期？” | **该技能** | 内置工具无法检测TLS相关信息 |
| “谁注册了这个域名？” | **该技能** | WHOIS数据无法通过网页搜索获取 |
| “coolstartup.io是否可用？” | **该技能** | 通过DNS、WHOIS及SSL信息进行被动可用性检测 |

## 平台兼容性

基于纯Python标准库（`socket`、`ssl`、`urllib`、`json`、`concurrent.futures`），在Linux、macOS和Windows系统上均可完美运行，无需额外依赖。

- **crt.sh查询**使用HTTPS协议（端口443）——可在大多数防火墙后正常工作
- **WHOIS查询**使用TCP端口43——在严格限制的网络环境中可能会被屏蔽
- **DNS查询**通过Google DoH（HTTPS）来获取MX/NS/TXT记录——更易穿透防火墙
- **SSL检测**会连接到目标端口的443端口——这是唯一的“主动”操作

## 数据来源

所有查询均为**被动式**——不进行端口扫描，也不执行漏洞检测：

- **crt.sh** — 证书透明度日志（用于子域名检测，仅支持 HTTPS）
- **WHOIS 服务器** — 直接通过 TCP 连接到 100 多家权威顶级域名注册商
- **Google DNS-over-HTTPS** — 支持 MX、NS、TXT、CNAME 域名解析（兼容防火墙设置）
- **系统 DNS** — 用于 A/AAAA 记录解析
- **SSL 检查** 是唯一会主动执行的操作（通过 TCP 连接到目标地址的 443 端口）

## 备注

- WHOIS 查询使用 TCP 43 端口——在限制严格的网络环境中可能会被屏蔽
- 部分 WHOIS 服务器会根据 GDPR 法规隐藏注册人信息——需向用户说明这一点
- 对于非常热门的域名（拥有数千份证书），crt.sh 的响应速度可能会较慢——请用户做好相应预期
- 可用性检查基于启发式方法（通过 3 个被动信号判断），并不像注册商 API 那样具有权威性

---

*由 [@FurkanL0](https://github.com/FurkanL0) 提供*
