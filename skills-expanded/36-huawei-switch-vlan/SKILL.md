---
name: 36-huawei-switch-vlan
description: 华为 VRP 交换机 VLAN、access/trunk/QinQ（dot1q-tunnel）规划与 DISCOVERY 配置；对接 OLT 上联场景。
---

# 华为 VRP VLAN / Trunk / QinQ

## 适用范围

适用于华为 **VRP 园区/汇聚交换机**（常见 S5700/S6700/S8700、CloudEngine 等）。**不是** SmartAX OLT（MA5600/MA5800/EA5800）。OLT 用 `allinpol.huawei.olt`。V200 与 V300（commit 风格）语法不同；本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.huawei.switch`。

## 场景

- 接入口 access + PVID
- 上联/级联 trunk 放行 VLAN 列表（常对接 OLT `port vlan`）
- 园区/城域 QinQ：`dot1q-tunnel` 或灵活 QinQ（版本差异大，必须 `?`）

## DISCOVERY 只读

```cli
display vlan
display port vlan
display current-configuration interface ${IF}
```

## DISCOVERY 写（须 WRITE + 参数来自 SoT）

```cli
system-view
vlan batch ${VLAN_LIST}
interface ${IF}
port link-type access
port default vlan ${PVID}
# 或
port link-type trunk
port trunk allow-pass vlan ${VLAN_LIST}
# QinQ 候选（本机确认）
port link-type dot1q-tunnel
port default vlan ${SVLAN}
```

禁止把示例 VLAN 当生产事实。先对端放行再改本端。
## 配置保存（可选）

**禁止**每次改配后自动 save/write/commit。仅当用户明确要求落盘时执行；先本机 ?。


## 来源

- 公开 VRP 命令参考与园区交换机运维速查结构化为场景，非官方手册替代。
- 本库无已观测 release 锚点；设备 CLI 优先。

