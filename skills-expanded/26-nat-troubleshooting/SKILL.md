---
name: 26-nat-troubleshooting
description: 在 ASR1001-X 上追踪 NAT/PAT/CGNAT 失败，并用会话、翻译、计数器与回程做时间关联。
---

# NAT 与 CGNAT 排障

## 目标

判断用户为何不翻译、不打到上游或收不到回程。

## 前置条件

先使用 `network-device-access`。确认 ASR1001-X、IOS XE release、特权、Source of Truth，以及初始 READ-ONLY 范围。

## 候选命令

- [已确认 @ IOS XE 17.09.03a] `show ip nat translations`
- [已确认 @ IOS XE 17.09.03a] `show ip nat statistics`
- [推断] `show ip nat pool`
- [推断] `show access-lists <ACL>`
- [已确认 @ IOS XE 17.09.03a] `show ip route <SUBSCRIBER_IP>`
- [推断] `show ip cef <SUBSCRIBER_IP>`

## 步骤

按下列链路推进：

`客户端 → PPPoE/IPoE → 路由/FIB → ACL 分类 → NAT binding → pool → 翻译 → outside/上游 → 回程`。

每层登记证据，并在第一处客观失败处停止。

## 强制时间关联

在用户受控流量期间：

1. 采集 NAT statistics/translations 与会话计数器；
2. 在已知短间隔内产生流量；
3. 再次采集；
4. 比较增量。

解读：

- 流量到达 BNG，但翻译仍为零 → 分类/binding/pool 缺失或不正确；
- 翻译增长，但有 `in-to-out` drops 或 pool/端口失败 → 容量/pool/分类；
- 翻译增长且下行计数器增加 → 至 BNG 的 NAT/回程正常；再校验客户端/DNS/HTTP；
- 仅有既有静态 PAT 不能证明在网用户动态 NAT。

## 公网 pool 检查清单

任何纠正前证明：

- 授权的 IPv4/块；
- 回程路由；
- 候选 IP 在配置、NAT、ARP、特定路由或相关路由协议中无既有消费者；
- inside/outside 正确；
- ACL 限于目标前缀；
- 须保留的既有 NAT/PAT。

勿从 loopback 或管理 PAT 推断地址可用。

## 预期结果

客观回答：

`报文是否到达 BNG？是否创建翻译？是否打到上游？是否有回程？` — 每项为 `是`、`否` 或 `未确认`，并附证据。

## 风险

翻译数据可能识别在网用户；版本化前须脱敏。`clear`、改 CGN 模式或大范围改 ACL/pool 属于 HIGH-IMPACT。

## 回滚

无自动 clear。纠正只能移除本次创建的 binding/pool/ACL，按逆序，并在检查依赖之后。

## 持久化

勿把 `write memory`/save 当作纠正的隐式步骤。持久化须在 running-config 校验后的单独门禁。

## 安全规则

遵循 SHOW → 分析 → 校验 → 提案 → 确认 → 变更 → 校验 → 记录。真实网络数据留在 Source of Truth。

## 禁止事项

勿全局清理翻译；勿在未分析其他前缀时复用宽 ACL；勿为方便复用管理公网 IPv4；勿在验收前保存。

## 依赖

与 `14-nat-cgnat`、`24-pppoe-troubleshooting`、`30-safe-change`、`31-production-checklist`、`32-pppoe-up-no-navigation` 配合使用。

## 来源

- Cisco ASR1001-X / IOS XE；以真实 CLI 为准。
- 在 IOS XE 17.09.03a 上验证的运维证据，不含客户专属数据。
