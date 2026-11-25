---
name: diagnosis-onu-optical-power
description: 跨厂商 ONU/ONT 光功率诊断。只解释 rx/tx Evidence；取证命令见厂商 Skill。不改配置。门限来自 SoT 或厂商手册，本库不写死 dBm。
---

# ONU / ONT 光功率（跨厂商诊断）

## 定位

**Diagnosis** 层：解释已采集的 `optical.rx_power` / `optical.tx_power`。取证走厂商 Skill，不要在此发明 CLI。

| 会话 | 取证 |
|------|------|
| `allinpol.huawei.olt` | `08-huawei-olt-ont-status`（`display ont optical-info` 等须本机 `?`，多为 DISCOVERY） |
| `allinpol.zte.olt` | `22-zte-c600-ont-correlation`；光功率命令本库多为 DISCOVERY，禁止套华为语法 |

成熟度：`experimental`。与 `query_onu_optical_power`（只读查询）分工：本 Skill 做判断。

## 目标

给出光路假设（过弱 / 过强 / 不可读 / 正常相对门限）与下一步只读取证。不授权 WRITE / 复位 ONU / PERSIST。

## 何时使用

用户说光衰、光功率异常、Rx 过低、过载，且目标是 OLT 上的 ONU/ONT。先查询再诊断：无数字时不要猜。

## 前置条件

Fingerprint 已核对；已有 ONU/ONT 标识。默认 READ。

## 解释层

```text
有无 rx/tx 数值？
  → 无：证据不足，按厂商 Skill DISCOVERY 取光功率
  → 有，且 alarm.los：先按掉线/LOS 处理（diagnosis-onu-flapping），不要只谈衰耗
  → 有：与 SoT 或该 ONU 型号手册门限比较
      → 低于下限：光路衰耗 / 连接 / 分路 / 距离
      → 高于上限：过载（过近、错模块）
      → 在门限内：光功率不是首发故障，转状态/业务层
```

本库 **不** 把「例如 -8～-27 dBm」标成已确认门限。任何数字区间均为 **推断**，必须被手册或局方 SoT 替换。

Evidence：`optical.rx_power`、`optical.tx_power`、`onu.status`、`alarm.los`。

## 禁止事项

- 不要用华为光功率命令套中兴会话。
- 不要因光功率差就 `ont reset` / 删 ONU。
- 不要把推断门限写成已确认。

## 配置保存（PERSIST）

不适用。本 Skill 不改运行配置。
