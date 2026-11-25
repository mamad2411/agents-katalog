---
name: 14-nat-cgnat
description: 在 Cisco ASR1001-X 上解读、规划并校验传统 NAT、PAT 与宽带 CGNAT，含公网块、容量、回滚与持久化的显式门禁。
---

# NAT 与 CGNAT

## 目标

在可追溯、有容量约束并保留既有服务的前提下，翻译在网用户流量。

## 前置条件

先使用 `network-device-access`。识别 ASR1001-X、IOS XE release、特权与 Source of Truth。从 READ-ONLY 开始，并采集脱敏基线：NAT、接口、路由、pool、ACL 与会话。

## 候选命令

- [已确认 @ IOS XE 17.09.03a] `show ip nat translations`
- [已确认 @ IOS XE 17.09.03a] `show ip nat statistics`
- [推断] `show ip nat pool`
- [推断] `show access-lists`
- [DISCOVERY 变更前强制] `ip nat ?`
- [DISCOVERY 变更前强制] `ip nat pool ?`
- [DISCOVERY 变更前强制] `ip nat inside source ?`

## 强制规划

在提议 Dynamic PAT/CGNAT 之前，分别确认：

1. 在网用户真实私网前缀；
2. `inside` 接口/模板；
3. `outside` 接口与默认/上游；
4. 负责人/上游授权的公网 IPv4/块；
5. 该块的回程路由；
6. 候选公网 IP 无既有消费者；
7. 服务专用 ACL，无正当理由勿复用更宽分类；
8. 适用的容量/许可/资源；
9. 须保留的静态 PAT/NAT；
10. 目标 release 字面接受的语法。

切勿仅因公网 IPv4 出现在 loopback、能 ping 或参与管理 PAT，就推断其可用于 CGNAT。

## Dynamic Port Address CGN 候选模型

仅在 discovery 与授权之后，下列格式可作为候选：

```text
ip access-list standard <SUBSCRIBER_ONLY_ACL>
 permit <SUBSCRIBER_PREFIX> <WILDCARD>
ip nat pool <PUBLIC_POOL> <FIRST_PUBLIC_IP> <LAST_PUBLIC_IP> netmask <MASK>
ip nat inside source list <SUBSCRIBER_ONLY_ACL> pool <PUBLIC_POOL> overload
```

以上命令均为 `[HIGH-IMPACT] [破坏性]`。同一变更中勿混用 interface overload、pool overload、BPA 或其他方法，除非另开新计划。

## 时间校验

在受控流量前后采集 `show ip nat statistics` 与 `show ip nat translations`。证明：

- 为预期用户创建翻译；
- 双向计数器增长；
- 无 pool/mapping/端口分配失败或 drops；
- 既有翻译/PAT 得以保留。

## 预期结果

变更小、可审计、可回退，且不必要地改动 PPPoE、路由、接口、`mode cgn` 或管理服务。

## 回滚

仅移除本次创建的 binding，再移除 pool，最后移除 ACL；移除前确认各对象无其他消费者。勿将 `clear ip nat translation *`、reload 或全局删除作为常规回滚。

## 持久化

持久化 running-config 是单独门禁。`write memory`、`copy running-config startup-config` 或等价操作需要显式授权与事后功能验证。save 后确认 startup-config。

## 安全规则

遵循 SHOW → 分析 → 校验 → 提案 → 确认 → 变更 → 校验 → 授权持久化 → 持久化 → 记录。脱敏凭据与在网用户数据。真实网络数据属于 Source of Truth。

## 禁止事项

勿编造公网块；勿凭推断复用管理 IP；勿在无专项计划时于事故中改动 `mode cgn`；勿全局清理翻译；勿在验收前保存。

## 依赖

与 `26-nat-troubleshooting`、`30-safe-change`、`31-production-checklist`、`32-pppoe-up-no-navigation` 配合使用。

## 来源

- Cisco ASR1001-X / IOS XE；以真实 CLI 为准。
- Cisco 文档化的 IOS XE Dynamic Port Address CGN 流程。
- 在 IOS XE 17.09.03a 上验证的运维证据，不含客户专属数据。
