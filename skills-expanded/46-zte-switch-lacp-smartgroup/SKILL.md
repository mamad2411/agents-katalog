---
name: 46-zte-switch-lacp-smartgroup
description: 中兴 ZXR10 LACP/smartgroup 聚合；与 ZTE OLT smartgroup 上联场景对齐。
---

# 中兴 ZXR10 LACP / smartgroup

## 适用范围

适用于中兴 **ZXR10 交换机**（常见 5960/8900E/9900 等 **ROSNG**）。**不是** ZXA10 OLT。OLT 用 `allinpol.zte.olt`。老款 2900E 等可能是 `set vlan` 方言，与 ROSNG 的 `switchport` **不可混用**。本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.zte.switch`。

## 场景

对端 ZTE OLT 常用 `interface smartgroup` + `smartgroup mode 802.3ad`。交换机侧须同模式、同 VLAN trunk。

## DISCOVERY 只读

```cli
show lacp
show smartgroup
show interface smartgroup${ID}
```

## DISCOVERY 写（HIGH-IMPACT）

```cli
configure terminal
interface smartgroup${ID}
smartgroup mode 802.3ad
smartgroup load-balance ${ALGO}
switchport mode trunk
switchport vlan ${VLAN_LIST} tag
interface ${MEMBER_IF}
smartgroup ${ID} mode active
```

算法/接口名本机确认。改聚合可能中断上联。
## 配置保存（可选）

**禁止**每次改配后自动 save/write/commit。仅当用户明确要求落盘时执行；先本机 ?。


## 来源

- 公开 ZXR10 命令参考与字段 ROSNG 上联（smartgroup/xgei）结构。
- 本库无已观测 release 锚点；设备 CLI 优先。

