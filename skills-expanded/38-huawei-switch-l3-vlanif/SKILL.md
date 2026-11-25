---
name: 38-huawei-switch-l3-vlanif
description: 华为 VRP VLANIF/SVI、三层口与静态路由 DISCOVERY；勿与 OLT vlanif 管理口混淆。
---

# 华为 VRP VLANIF 与三层

## 适用范围

适用于华为 **VRP 园区/汇聚交换机**（常见 S5700/S6700/S8700、CloudEngine 等）。**不是** SmartAX OLT（MA5600/MA5800/EA5800）。OLT 用 `allinpol.huawei.olt`。V200 与 V300（commit 风格）语法不同；本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.huawei.switch`。

## DISCOVERY 只读

```cli
display ip interface brief
display ip routing-table
display interface Vlanif ${VLAN}
```

## DISCOVERY 写（须 WRITE；地址来自 SoT）

```cli
system-view
interface Vlanif ${VLAN}
ip address ${IP} ${MASK}
quit
ip route-static ${PREFIX} ${MASK} ${NEXTHOP}
```

管理 VLAN/默认路由属 HIGH-IMPACT。
## 配置保存（可选）

**禁止**每次改配后自动 save/write/commit。仅当用户明确要求落盘时执行；先本机 ?。


## 来源

- 公开 VRP 命令参考与园区交换机运维速查结构化为场景，非官方手册替代。
- 本库无已观测 release 锚点；设备 CLI 优先。

