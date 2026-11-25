---
name: diagnosis-onu-offline
description: 跨厂商 ONU/ONT 不在线诊断。区分未注册、从未上线、当前 offline；取证走厂商 Skill。不改配置。
---

# ONU / ONT 不在线（跨厂商诊断）

## 定位

**Diagnosis** 层。反复上下线走 `diagnosis-onu-flapping`。光功率数值走 `diagnosis-onu-optical-power`。LOS/掉电告警走 `diagnosis-onu-los`。

| 会话 | 取证 |
|------|------|
| `allinpol.huawei.olt` | `08-huawei-olt-ont-status`、`06-huawei-olt-ont-autofind`、`14-huawei-olt-troubleshooting` |
| `allinpol.zte.olt` | `22-zte-c600-ont-correlation`、`21-zte-c650-baseline` |

成熟度：`experimental`。

## 解释层

```text
OLT 上是否已有该 ONU/ONT 注册？
  → 否：未注册。查 autofind / 未发现列表；不要先建 service-port
  → 是，status 从未 online：注册在、光路或供电未通；转 LOS/光功率
  → 是，当前 offline：取 los / dying_gasp / rx；再决定是光路、掉电还是局端
```

Evidence：`onu.status`、位置字段。缺 status 则证据不足。

## 禁止事项

- 不要把「不在线」直接当成授权 `ont add` / PnP / reset。
- 不要混用华为与中兴 CLI。

## 配置保存（PERSIST）

不适用。
