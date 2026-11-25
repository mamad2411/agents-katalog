---
name: diagnosis-service-vlan
description: 跨厂商业务 VLAN / QinQ / GEM mapping 不通诊断。只解释 L2 连续性 Evidence；取证走厂商 Skill。不改 VLAN、不上联、不自动 save。
---

# 业务 VLAN 不通（跨厂商诊断）

## 定位

**Diagnosis** 层：判断业务 VLAN 在哪一跳断开。取证走厂商 Skill，不要在此发明 CLI。

反复掉线、光功率、LOS 不是本 Skill 的主路径。

| 会话 | 取证 |
|------|------|
| `allinpol.huawei.olt` | `09-huawei-olt-gem-tcont`、`10-huawei-olt-service-port`、`11-huawei-olt-vlan`、`12-huawei-olt-uplink` |
| `allinpol.zte.olt` | `22-zte-c600-ont-correlation`、`32-zte-olt-onu-pnp` 中的 QinQ/上联段落（只读） |
| `allinpol.huawei.switch` | `36-huawei-switch-vlan`（对端 trunk 是否放行同一 VLAN） |
| `allinpol.zte.switch` | `45-zte-switch-vlan` |

成熟度：`experimental`。

## 解释层

```text
ONU/ONT 在线且光路正常？
  → 否：先走 offline / los / optical / flapping
GEM / vport 是否映射到业务 VLAN（或 QinQ 内外层）？
  → 否：mapping 缺失或 VLAN 与 SoT 不一致（华为 mapping-mode VLAN 下尤其如此）
service-port / 业务流是否存在且 UP、计数是否增长？
  → 流 down / 无计数：先查 VLAN/mapping，不要先改 AAA
PON 口是否放行该 VLAN？
上联 / smartgroup / Eth-Trunk 是否放行同一 VLAN？
对端交换机 trunk 是否放行同一 VLAN？
  → 任一层未知：证据不足，按上表 Skill 只读取证
```

Evidence 字段（能填则填，不能填就写未知）：业务 VLAN、内层/外层（QinQ）、GEM mapping 是否存在、service-port 状态、PON VLAN、上联 VLAN。

## 禁止事项

- 不要为「通业务」自动改上联 trunk（HIGH-IMPACT，须单独授权）。
- 不要把华为 `port vlan` / `gem mapping` 套到中兴或交换机会话。
- 不要动管理 VLAN。
- 不要自动 `save` / `write`。

## 配置保存（PERSIST）

不适用。本 Skill 不改运行配置。
