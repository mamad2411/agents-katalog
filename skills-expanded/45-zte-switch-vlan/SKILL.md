---
name: 45-zte-switch-vlan
description: 中兴 ZXR10 VLAN、access/trunk/QinQ 与对接 OLT 上联 VLAN 列表；ROSNG switchport 语法。
---

# 中兴 ZXR10 VLAN / Trunk / QinQ

## 适用范围

适用于中兴 **ZXR10 交换机**（常见 5960/8900E/9900 等 **ROSNG**）。**不是** ZXA10 OLT。OLT 用 `allinpol.zte.olt`。老款 2900E 等可能是 `set vlan` 方言，与 ROSNG 的 `switchport` **不可混用**。本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.zte.switch`。

## DISCOVERY 只读

```cli
show vlan
show vlan brief
show running-config interface ${IF}
```

## DISCOVERY 写（ROSNG 字段常见结构）

```cli
configure terminal
vlan ${VLAN}
exit
interface ${IF}
switchport mode access
switchport access vlan ${PVID}
# 或
switchport mode trunk
switchport vlan ${VLAN_LIST} tag
```

QinQ/svlan 以本机 `?` 为准。对接 ZTE OLT 时与 OLT `switchport vlan … tag` 列表对齐。
## 配置保存（可选）

**禁止**每次改配后自动 save/write/commit。仅当用户明确要求落盘时执行；先本机 ?。


## 来源

- 公开 ZXR10 命令参考与字段 ROSNG 上联（smartgroup/xgei）结构。
- 本库无已观测 release 锚点；设备 CLI 优先。

