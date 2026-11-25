---
name: diagnosis-ethernet-fault
description: 跨厂商以太网/端口故障诊断。解释链路、错包、STP 阻塞与光模块 Evidence；取证走厂商 Skill。不改配置、不自动 save。
---

# 以太网 / 端口故障（跨厂商诊断）

## 定位

**Diagnosis** 层。业务 VLAN 不通走 `diagnosis-service-vlan`。PON 上 ONU 问题走 ONU 诊断系列。

| 会话 | 取证 |
|------|------|
| `allinpol.huawei.switch` | `35-huawei-switch-interface`、`40-huawei-switch-loop-stp`、`39-huawei-switch-mac-arp-lldp` |
| `allinpol.zte.switch` | `44-zte-switch-interface`、`48-zte-switch-troubleshooting` |
| `allinpol.cisco.iosxe` | `03-interface-diagnostics`、`04-optical-diagnostics` |
| `allinpol.huawei.olt` | `12-huawei-olt-uplink`（上联以太网侧） |
| `allinpol.zte.olt` | `32` 上联段落只读；端口方言须 DISCOVERY |

成熟度：`experimental`。环路专项规划仍可用意图 `loop`（交换机 STP Skill）。

## 解释层

```text
接口是否存在且 shutdown / admin down？
  → 是：管理关闭，先核对授权与窗口，不要当光路故障
协议 down / no link？
  → 查对端、介质、光模块 rx/tx（门限来自 SoT/手册）
错包 / CRC / flap 计数增长？
  → 物理层或双工不匹配
STP / 环路防护是否把端口 blocking？
  → 是：先拓扑与根桥，不要先 undo shutdown 对端
MAC/LLDP 是否看到预期邻居？
  → 否：链路通但接错设备或 VLAN
任一层未知：证据不足，按上表只读取证
```

Evidence：`interface.admin_status`、`interface.protocol_status`、错包计数、STP 状态、光模块 rx/tx（若有）。

## 禁止事项

- 不要为排障自动 `shutdown` / 改 STP / 改上联聚合。
- 不要把 VRP `display interface` 套到中兴 ROSNG 或 Cisco。
- 不要自动 `save` / `write`。

## 配置保存（PERSIST）

不适用。
