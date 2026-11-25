---
name: 33-huawei-switch-baseline
description: 华为 VRP 交换机 fingerprint 与只读基线；会话 allinpol.huawei.switch；非 OLT。
---

# 华为 VRP 交换机基线

## 适用范围

适用于华为 **VRP 园区/汇聚交换机**（常见 S5700/S6700/S8700、CloudEngine 等）。**不是** SmartAX OLT（MA5600/MA5800/EA5800）。OLT 用 `allinpol.huawei.olt`。V200 与 V300（commit 风格）语法不同；本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.huawei.switch`。

## 目标

只读确认型号、VRP 版本、板卡/端口概览，再进入 VLAN/聚合等场景。

## 前置条件

READ/DISCOVERY；SoT 已给出目标。勿把 OLT `display ont` 用到交换机。

## DISCOVERY 命令

```cli
display version
display device
display elabel brief
display interface brief
display vlan
display current-configuration | include sysname
?
```

模块：`docs/huawei/switch/cli/fingerprint-and-cli-discovery.md`

## 禁止

无 WRITE 时禁止 `system-view` 改配、`save`、`reboot`。不记录完整配置与密钥。

## 来源

- 公开 VRP 命令参考与园区交换机运维速查结构化为场景，非官方手册替代。
- 本库无已观测 release 锚点；设备 CLI 优先。

