---
name: 44-zte-switch-interface
description: 中兴 ZXR10 端口/光属性只读巡检；shutdown 须 WRITE。
---

# 中兴 ZXR10 端口与光口

## 适用范围

适用于中兴 **ZXR10 交换机**（常见 5960/8900E/9900 等 **ROSNG**）。**不是** ZXA10 OLT。OLT 用 `allinpol.zte.olt`。老款 2900E 等可能是 `set vlan` 方言，与 ROSNG 的 `switchport` **不可混用**。本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.zte.switch`。

## DISCOVERY 只读

```cli
show interface brief
show interface ${IF}
show optical-info ${IF}
show lldp neighbors
```

光命令名以 `?` 为准。字段 OLT 上联常见 `xgei_` + `phy-attribute` / `hybrid-attribute fiber`（交换机侧等价须本机确认）。

## WRITE

```cli
configure terminal
interface ${IF}
shutdown
no shutdown
```

## 配置保存（可选）

**禁止**每次改配后自动 save/write/commit。仅当用户明确要求落盘时执行；先本机 ?。


## 来源

- 公开 ZXR10 命令参考与字段 ROSNG 上联（smartgroup/xgei）结构。
- 本库无已观测 release 锚点；设备 CLI 优先。

