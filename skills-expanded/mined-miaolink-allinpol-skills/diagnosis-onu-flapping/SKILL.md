---
name: diagnosis-onu-flapping
description: 跨厂商 ONU/ONT 频繁掉线诊断。只解释 Evidence（LOS、光功率、Dying Gasp、flap）；取证命令见当前会话的厂商 Skill。不改配置。
---

# ONU / ONT 频繁掉线（跨厂商诊断）

## 定位

本 Skill 是 **Diagnosis** 层：根据已采集的结构化证据下结论。单次不在线走 `diagnosis-onu-offline`；告警字面 LOS/Dying Gasp 走 `diagnosis-onu-los`。

**如何取证** 属于厂商 Skill，不要在本文件里发明 CLI。

| 会话 | 取证 |
|------|------|
| `allinpol.huawei.olt` | `08-huawei-olt-ont-status`、`14-huawei-olt-troubleshooting`、`huawei-olt-decision-tree` |
| `allinpol.zte.olt` | `22-zte-c600-ont-correlation`、`21-zte-c650-baseline` |

术语：华为侧常用 **ONT**，中兴侧常用 **ONU**。见 `ontology/terms.yaml`。

成熟度：`experimental`。结论必须能指向 Evidence 字段；缺字段时只输出「证据不足」，不要猜光衰或供电。

## 目标

给出首发假设（光路 / 供电 / 设备 / 局端）和下一步**只读**取证，不授权 WRITE / PERSIST。

## 何时使用

用户说掉线、反复 offline、flapping，且目标是 OLT 上的 ONU/ONT。交换机会话不要用本 Skill 当主路径。

## 前置条件

1. `network-device-access` 与 fingerprint 已核对。
2. 已有 ONU/ONT 标识（F/S/P + ID，或厂商确认的接口名）。不得扫描发现。
3. 默认 READ / DISCOVERY。

## 解释层（与厂商无关）

按顺序问，**停下在第一个被证据支持的分支**：

```text
ONU/ONT flapping
  → LOS / 光路中断？
  → 光功率越限或不可读？
  → Dying Gasp / 供电掉电？
  → 短周期反复注册或状态翻转（flap）？
  → 局端告警或板卡/PON 异常？
  → 证据不足，扩大只读取证
```

映射到 Evidence 字段（`schema/evidence.schema.yaml`）：

| 问题 | 应具备字段 |
|------|------------|
| LOS | `alarm.los` |
| 光功率 | `optical.rx_power` / `optical.tx_power`，以及 `onu.status` |
| 供电 | `alarm.dying_gasp` |
| 频繁翻转 | `history.flap_count` 或等价计数；没有计数就写未知 |
| 在线身份 | `onu.status`、`onu` 位置字段 |

## 厂商取证（只指向，不替代）

华为 OLT：状态与光功率走 `08`（`display ont info` / `display ont optical-info` 等以目标 CLI 与 DISCOVERY 为准）。分层排障走 `14`。

中兴 OLT：状态与关联走 `22`（`show gpon onu state` / `detail-info` 等）。光功率命令本库多为 DISCOVERY，先 `?`，不要套华为 `display ont optical-info`。

## 预期结果

一条首发假设、已引用的 Evidence 字段、缺失字段列表、下一步厂商只读命令（来自上表 Skill）。

## 禁止事项

- 不要在未取证时下发重置 ONU、删 ONU、改 DBA 或 `save`/`write`。
- 不要把华为命令用在中兴会话，反之亦然。
- 不要把推断标成已确认。
- 不要记录真实 SN、客户名或管理地址。

## 配置保存（PERSIST）

不适用。本 Skill 不改运行配置。
