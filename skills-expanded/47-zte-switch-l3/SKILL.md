---
name: 47-zte-switch-l3
description: 中兴 ZXR10 三层 VLAN 接口与静态路由 DISCOVERY。
---

# 中兴 ZXR10 三层

## 适用范围

适用于中兴 **ZXR10 交换机**（常见 5960/8900E/9900 等 **ROSNG**）。**不是** ZXA10 OLT。OLT 用 `allinpol.zte.olt`。老款 2900E 等可能是 `set vlan` 方言，与 ROSNG 的 `switchport` **不可混用**。本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.zte.switch`。

## DISCOVERY 只读

```cli
show ip interface brief
show ip route
show interface vlan${VLAN}
```

## DISCOVERY 写

接口形式可能是 `interface vlan ${VLAN}` 或 `vlan-interface`，**先 `?`**。地址来自 SoT。管理路由 HIGH-IMPACT。
## 配置保存（可选）

**禁止**每次改配后自动 save/write/commit。仅当用户明确要求落盘时执行；先本机 ?。


## 来源

- 公开 ZXR10 命令参考与字段 ROSNG 上联（smartgroup/xgei）结构。
- 本库无已观测 release 锚点；设备 CLI 优先。

