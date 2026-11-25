---
name: diagnosis-onu-los
description: 跨厂商 ONU/ONT 的 LOS、LOF、Dying Gasp 解释。只根据告警 Evidence 分支；取证走厂商 Skill。不改配置。
---

# ONU / ONT LOS / LOF / Dying Gasp（跨厂商诊断）

## 定位

**Diagnosis** 层：解释 `alarm.los`、`alarm.lof`、`alarm.dying_gasp`。反复闪断仍以 `diagnosis-onu-flapping` 为主路径。

| 会话 | 取证 |
|------|------|
| `allinpol.huawei.olt` | `08-huawei-olt-ont-status`、`14-huawei-olt-troubleshooting` |
| `allinpol.zte.olt` | `22-zte-c600-ont-correlation`（状态字面如 `LOS`、`DyingGasp` 以 CLI 为准） |

成熟度：`experimental`。

## 解释层

```text
dying_gasp 为真？
  → 优先供电/断电，而不是先改 ODN
los 为真且无 dying_gasp？
  → 光路中断（连接、分路、断纤、ONT 未加电但无 gasp 字段）
lof 为真、los 为假？
  → 帧失步/光质量；再取光功率（diagnosis-onu-optical-power）
三者皆未知？
  → 证据不足，按厂商 Skill 读状态/告警，不要猜
```

字段来自 `schema/evidence.schema.yaml`。厂商 CLI 的状态字符串须原样记录，再映射到这些字段。

## 禁止事项

- 不要因 LOS 立即 `ont delete` 或 reset。
- 不要把华为 `display` 用到中兴会话。

## 配置保存（PERSIST）

不适用。
