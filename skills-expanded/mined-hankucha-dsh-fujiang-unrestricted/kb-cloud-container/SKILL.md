---
name: kb-cloud-container
description: CVE/PoC 知识库 · 云原生 / 虚拟化 / 中间件：runc(2024-21626)、cgroups(2022-0492)、Docker API 2375、Redis 未授权、Nacos(2021-29441)、vCenter 上传(2021-21972)、Workspace ONE SSTI(2022-22954)。每条都有对应 PoC；公开资料整理，verified=false。
verified: false
sources: 公开资料整理（CVE 公告 / 公开分析 / 业务逻辑类；出处见各条参考）
---

# 云 / 容器 / 中间件（14 条）
> 条目为公开资料整理（出处见文末「参考」），`利用步骤` 属待验证假设；出报告前按目标版本自验并把 `verified` 置为 true。

判据永远是"**这个服务能不能被直连**"。博彩/跑分那类站点特别常见的三件套：`bucket` 公开可列（证件照、充值凭证）、`3306/27017` 弱口令暴露、`Redis` 裸奔。它们比任何 CVE 都更值钱。

## 条目

| 文件 | 漏洞 | 严重度 | 入口 |
|---|---|---|---|
| `cve-2019-7238-nexus-rce.md` | Nexus Repository 未授权 RCE（CVE-2019-7238） | critical | POST /service/extdirect 的 EL 注入 |
| `cve-2019-9193-postgres.md` | PostgreSQL COPY PROGRAM 命令执行（CVE-2019-9193） | high | COPY ... TO PROGRAM |
| `cve-2021-21972-vcenter-upload.md` | vCenter Server 未授权上传 → RCE（vROPS 插件） | critical | POST /ui/vropspluginui/rest/services/uploadova |
| `cve-2021-29441-nacos.md` | Nacos 认证绕过（User-Agent 白名单） | critical | - |
| `cve-2021-43798-grafana-file-read.md` | Grafana 插件路径穿越任意文件读（CVE-2021-43798） | high | /public/plugins/<plugin>/../../../../etc/passwd |
| `cve-2022-0492-cgroup-release-agent.md` | cgroups release_agent 容器逃逸 | high | 挂 cgroup v1 写 release_agent |
| `cve-2022-22954-workspace-one-ssti.md` | VMware Workspace ONE Access 模板注入 RCE | critical | /catalog-portal/ui/oauth/verify?deviceUdid= |
| `cve-2023-27532-veeam-credential-dump.md` | Veeam Backup 凭据泄露（CVE-2023-27532） | high | 9401 Backup Service 回显配置库凭据 |
| `cve-2024-21626-runc-leaky-vessels.md` | runc 文件描述符泄露逃逸（Leaky Vessels） | critical | WORKDIR /proc/self/fd/N 拿到宿主 fd |
| `cve-2024-37085-esxi-auth-bypass.md` | VMware ESXi 认证绕过 → hypervisor 失守（CVE-2024-37085） | critical | AD 里新建 "ESX Admins" 组 → 自动获得 ESXi 管理权 |
| `cve-2024-40711-veeam-rce.md` | Veeam Backup 未认证 RCE（CVE-2024-40711） | critical | 9419 控制台凭据反序列化 |
| `docker-api-2375.md` | Docker Remote API 未授权（直接拿宿主） | critical | - |
| `mongodb-unauth.md` | MongoDB 未授权访问（直接拖库） | critical | mongod 无 auth 且对外开放 |
| `redis-unauth.md` | Redis 未授权（写文件 / 模块加载 / 主从复制） | critical | - |

## 用这一页的方法

- 从**前端资源**开始收集：JS 里的图片域名、`config.js` 的 `ossUrl`、下载链接的 `?Expires=` 签名 → 反推 bucket 名。
- 对象存储只列举、只取 1 个对象做证据；DB 只取 `select 1` 与一行样例，别拖库。
- 拿到 DB 后优先看"会员/订单/提现/代理"四张表，那是这类目标的全部价值。
