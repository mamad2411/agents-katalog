---
name: diagnosis-pon-congestion
description: 跨厂商 PON/DBA/T-CONT 拥塞诊断。解释带宽与计数 Evidence；取证走 DBA/GEM/service-port Skill。不改 DBA、不自动 save。
---

# PON 拥塞（跨厂商诊断）

## 定位

**Diagnosis** 层。ONU 不在线/掉线/光功率不是本路径。业务 VLAN 不通走 `diagnosis-service-vlan`。

| 会话 | 取证 |
|------|------|
| `allinpol.huawei.olt` | `03-huawei-olt-dba`、`09-huawei-olt-gem-tcont`、`10-huawei-olt-service-port` |
| `allinpol.zte.olt` | `22-zte-c600-ont-correlation`（T-CONT/GEM/vport）；traffic profile 须 DISCOVERY |

成熟度：`experimental`。交换机会话不要用本 Skill 当主路径。

## 解释层

```text
ONU 在线且 mapping/VLAN 已通、但仍慢或无计数？
  → 先排除 VLAN/光路（见其它 Diagnosis）
DBA / traffic profile 是否被过多 T-CONT 引用，或 Max 与 ONT type 冲突？
  → 有字面错误：走错误库，勿盲目下调 Max
同一 PON 上是否大量 ONU 争用同一 T-CONT/DBA？
  → 是：拥塞假设；用计数器是否增长来验证，不要猜利用率数字
service-port 计数不涨：可能仍是 mapping，不是拥塞
字段不足：证据不足
```

本库 **不** 写死「PON 应低于 xx Mbps」。任何容量数字来自 SoT 或本机显示，标推断直至证实。

Evidence：DBA/profile 引用次数、T-CONT 关联、service-port 计数是否增长、相关字面错误。

## 禁止事项

- 不要为「加速」自动改 DBA Max 或删 T-CONT。
- 不要把华为 DBA CLI 套到中兴。
- 不要自动 `save`。

## 配置保存（PERSIST）

不适用。
