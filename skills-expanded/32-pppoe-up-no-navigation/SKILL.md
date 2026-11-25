---
name: 32-pppoe-up-no-navigation
description: 诊断已认证并获 IP 但无法上网的 PPPoE 用户，隔离 BNG、策略、NAT/CGNAT、上游与客户端之间的断点。
---

# PPPoE UP、已获 IP、无法上网

## 目标

当 PPPoE 会话 UP 且用户已获 IPv4 但无法访问 Internet 时，用证据确定首个失败点。

## 前置条件

先使用 `network-device-access`。确认设备、IOS XE release、特权、授权访问路径与 Source of Truth。从 READ-ONLY 开始。勿假定 PPPoE UP 等于完整转发。

## 强制流程

按层标记 `已确认`、`失败` 或 `未确认`：

`客户端/ONT → OLT/VLAN → BNG/Virtual-Access → 路由/FIB → ACL/policy → NAT/CGNAT → 上游 → 回程 → DNS/HTTP/HTTPS`。

在第一处客观失败处停止。

## 候选命令

- [已确认 @ IOS XE 17.09.03a] `show pppoe session all`
- [已确认 @ IOS XE 17.09.03a] `show ip route <SUBSCRIBER_IP>`
- [已确认 @ IOS XE 17.09.03a] `show ip nat statistics`
- [已确认 @ IOS XE 17.09.03a] `show ip nat translations`
- [推断] `show interfaces <VIRTUAL_ACCESS>`
- [推断] `show policy-map interface <VIRTUAL_ACCESS>`
- [推断] `show access-lists <ACL>`
- [推断] `show ip cef <SUBSCRIBER_IP>`
- [推断] `show ip route 0.0.0.0 0.0.0.0`

标为 `[已确认]` 的命令仍依赖模式与 release 上下文；以真实 CLI 为准。

## 强制时间关联

勿仅凭静态配置下结论。在用户产生流量时做前后采样：

1. 登记 PPPoE/Virtual-Access 与 NAT 计数器；
2. 有客户端访问时产生 ping/HTTPS；
3. 等待已知短间隔；
4. 再次采集；
5. 比较增量。

最低解读：

- PPPoE RX 增长且 NAT 不创建翻译 → 调查 CGNAT 分类/binding/pool；
- 翻译出现且 PPPoE TX 增长 → 回程已到 BNG；校验客户端/DNS/HTTP；
- PPPoE RX 不增长 → 回到 OLT/VLAN/转发；
- NAT 显示 drops/pool/端口失败 → 在查上游前先处理容量/分类。

## NAT/CGNAT

若用户使用 RFC6598 或 RFC1918，显式证明是否存在动态翻译。勿把管理静态 PAT 与在网用户动态 NAT 混淆。确认 `inside`、`outside`、专用 ACL、授权公网 pool、回程路由，以及公网 IP 无既有消费者。

切勿因公网 IP 出现在 loopback 或管理 PAT 就推断其可用于 CGNAT。

## 客户端测试

可用时按序校验：

1. 网关/BNG；
2. 已知公网 IPv4；
3. 显式 DNS；
4. HTTP/HTTPS；
5. traceroute；
6. MTU/MSS/PMTUD。

ASR 上数据面通过不能替代客户端上网确认；终端不可用时明确记录限制。

## 根因标准

仅当会话、路由、计数器与失败层相关时才标 `已确认`。避免在未证明流量到达 BNG 且未产生翻译/回程时说“好像是 NAT”。

## 纠正变更

任何创建/改动 ACL、pool、NAT binding、接口、路由或 policy 均为 `[HIGH-IMPACT] [破坏性]`，需单独门禁。Change Plan 须含：

- 脱敏基线；
- 精确私网块；
- 授权公网块；
- inside/outside；
- 经 CLI 校验的语法；
- 影响与容量；
- 保留既有 NAT/PAT；
- 变更后校验；
- 专项回滚。

## 持久化

`write memory`、`copy running-config startup-config` 或等价操作是单独的持久化变更。仅在校验 running-config 并获显式授权后持久化。之后将 startup-config 与已批准行比对。

## 回滚

仅移除本次变更创建的对象，按 binding → pool → ACL 逆序，并在确认无其他消费者之后。勿将 `clear ip nat translation *`、reload 或全局删除作为标准回滚。

## 安全与文档

脱敏凭据、community、密钥、PPPoE 用户名与个人数据。客户真实地址、主机名、拓扑与取值属于 Source of Truth，绝不写入本 skill。

## 依赖

与下列配合：

- `11-pppoe-bng`；
- `14-nat-cgnat`；
- `24-pppoe-troubleshooting`；
- `26-nat-troubleshooting`；
- `30-safe-change`；
- `31-production-checklist`。

## 预期结果

报告须能回答：“PPPoE 已 UP 且已获 IP；报文停在哪一层、何证据证明、需要何种纠正、还缺哪道门禁？”
