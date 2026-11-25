---
name: 48-zte-switch-troubleshooting
description: 中兴交换机上联/VLAN/聚合排障；对接 ZTE OLT 时交叉 OLT 上联配置。
---

# 中兴 ZXR10 交换机排障

## 适用范围

适用于中兴 **ZXR10 交换机**（常见 5960/8900E/9900 等 **ROSNG**）。**不是** ZXA10 OLT。OLT 用 `allinpol.zte.olt`。老款 2900E 等可能是 `set vlan` 方言，与 ROSNG 的 `switchport` **不可混用**。本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.zte.switch`。

## 分层

1. 物理/光：Skill 44
2. VLAN/trunk 列表：Skill 45
3. smartgroup/LACP：Skill 46
4. `show mac` 是否在预期口
5. 对端 OLT：核对 OLT 口 `switchport vlan … tag` 与本端一致
6. 三层：Skill 47

默认不 `write`。

## 来源

- 公开 ZXR10 命令参考与字段 ROSNG 上联（smartgroup/xgei）结构。
- 本库无已观测 release 锚点；设备 CLI 优先。

