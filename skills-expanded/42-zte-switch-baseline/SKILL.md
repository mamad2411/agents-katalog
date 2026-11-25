---
name: 42-zte-switch-baseline
description: 中兴 ZXR10 交换机 fingerprint；优先 ROSNG show；非 ZXA10 OLT。会话 allinpol.zte.switch。
---

# 中兴 ZXR10 交换机基线

## 适用范围

适用于中兴 **ZXR10 交换机**（常见 5960/8900E/9900 等 **ROSNG**）。**不是** ZXA10 OLT。OLT 用 `allinpol.zte.olt`。老款 2900E 等可能是 `set vlan` 方言，与 ROSNG 的 `switchport` **不可混用**。本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.zte.switch`。

## DISCOVERY 命令（ROSNG 起点）

```cli
show version
show hardware
show interface brief
show vlan
show running-config | include hostname
?
```

若大量 `set ` 命令风格，可能是 2900E 方言：停，按本机帮助重建命令表。

模块：`docs/zte/zxr10/cli/fingerprint-and-cli-discovery.md`

## 来源

- 公开 ZXR10 命令参考与字段 ROSNG 上联（smartgroup/xgei）结构。
- 本库无已观测 release 锚点；设备 CLI 优先。

