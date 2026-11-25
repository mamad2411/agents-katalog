---
name: 43-zte-switch-cli-discovery
description: 中兴交换机 CLI 发现：ROSNG switchport vs 老款 set 方言；禁止跨方言硬套。
---

# 中兴交换机 CLI 发现

## 适用范围

适用于中兴 **ZXR10 交换机**（常见 5960/8900E/9900 等 **ROSNG**）。**不是** ZXA10 OLT。OLT 用 `allinpol.zte.olt`。老款 2900E 等可能是 `set vlan` 方言，与 ROSNG 的 `switchport` **不可混用**。本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.zte.switch`。

## 流程

1. `show ?` / `configure ?`
2. 接口前缀：`gei_` / `xgei_` / `smartgroup` / `vlan` 以本机为准
3. 出现 `set vlan` / `set lacp` → 按老款手册 DISCOVERY，不要套 ROSNG `switchport`

## 来源

- 公开 ZXR10 命令参考与字段 ROSNG 上联（smartgroup/xgei）结构。
- 本库无已观测 release 锚点；设备 CLI 优先。

