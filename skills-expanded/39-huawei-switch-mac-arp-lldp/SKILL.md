---
name: 39-huawei-switch-mac-arp-lldp
description: 华为 VRP MAC/ARP/LLDP 只读关联，定位环路、错接、对端设备。
---

# 华为 VRP MAC / ARP / LLDP

## 适用范围

适用于华为 **VRP 园区/汇聚交换机**（常见 S5700/S6700/S8700、CloudEngine 等）。**不是** SmartAX OLT（MA5600/MA5800/EA5800）。OLT 用 `allinpol.huawei.olt`。V200 与 V300（commit 风格）语法不同；本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.huawei.switch`。

## DISCOVERY

```cli
display mac-address
display mac-address ${MAC}
display arp
display lldp neighbor
display lldp neighbor ${IF}
```

用于：用户 MAC 在哪口、网关 ARP、对端是否为 OLT/核心。勿把完整表写入公开仓库。

## 来源

- 公开 VRP 命令参考与园区交换机运维速查结构化为场景，非官方手册替代。
- 本库无已观测 release 锚点；设备 CLI 优先。

