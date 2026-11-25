---
name: 24-pppoe-troubleshooting
description: 在 ASR1001-X BNG 上从 ONT 到 Internet 隔离 PPPoE 首层失败，含会话已 UP 且已获 IP 的情况。
---

# PPPoE 排障

## 目标

精确定位 PPPoE 会话失败点，勿将 `UP` 等同于可上网。

## 前置条件

先使用 `network-device-access`。识别 ASR1001-X、IOS XE release、特权、范围与 Source of Truth。从 READ-ONLY 开始。

## 候选命令

- [已确认 @ IOS XE 17.09.03a] `show pppoe session all`
- [推断] `show pppoe session summary`
- [推断] `show users`
- [推断] `show aaa sessions`
- [推断] `show interfaces <VIRTUAL_ACCESS>`
- [推断] `show policy-map interface <VIRTUAL_ACCESS>`
- [已确认 @ IOS XE 17.09.03a] `show ip route <SUBSCRIBER_IP>`
- [已确认 @ IOS XE 17.09.03a] `show ip nat statistics`
- [已确认 @ IOS XE 17.09.03a] `show ip nat translations`

## 步骤

按下列链路推进：

`ONT → VLAN/uplink → PADI → PADO → PADR → PADS → LCP → Authentication → AAA/RADIUS → IPCP/IP assignment → Virtual-Access → 路由/FIB → service-policy/ACL → NAT/CGNAT → 上游 → 回程 → DNS/HTTP/HTTPS`。

在第一处客观失败处停止。

## PPPoE UP 规则

若会话 UP 且已有 IP：

1. 确认用户 `/32` 或等价路由；
2. 在真实流量期间观察 Virtual-Access RX/TX 计数器；
3. 若 IP 为 RFC6598/RFC1918，证明动态 NAT/CGNAT 翻译；
4. 区分动态 NAT 与管理用静态 PAT；
5. 确认上游与回程；
6. 有客户端终端时，校验 DNS、HTTP/HTTPS 与 MTU/MSS。

RX 增长但无动态翻译，应调查 NAT 分类/binding/pool，而非据此改 PPPoE。

## 时间关联

在短测试窗口前后采集计数器。报告增量与时间。单独的静态配置不能证明转发。

## 预期结果

证据足以将每层标为 `已确认`、`失败` 或 `未确认`；仅在有会话、路由与计数器支撑时给出根因。

## 风险

`clear pppoe`、复位会话或改动 Virtual-Template 会影响客户，不属于标准诊断。

## 回滚

诊断本身不改动设备。纠正走专用 skill 与 `30-safe-change`。

## 安全规则

遵循 SHOW → 分析 → 校验 → 提案 → 确认 → 变更 → 校验 → 记录。脱敏 PPPoE 用户名、凭据与个人数据。真实网络数据属于 Source of Truth。

## 禁止事项

勿为“测试”而拆会话；勿在计数器已到达 BNG 时假定问题在 OLT；勿在测通 IP 前归咎 DNS；勿在验收前持久化配置。

## 依赖

会话 UP 但无法上网时，使用 `14-nat-cgnat`、`26-nat-troubleshooting`、`29-isp-troubleshooting` 与 `32-pppoe-up-no-navigation`。

## 来源

- Cisco ASR1001-X / IOS XE；以真实 CLI 为准。
- 在 IOS XE 17.09.03a 验证的运营证据，不含客户专属数据。
