---
name: 40-huawei-switch-loop-stp
description: 华为 VRP 环路/STP/MSTP/SEP 只读诊断；清 MAC 或改 STP 须单独授权。
---

# 华为 VRP 环路与 STP

## 适用范围

适用于华为 **VRP 园区/汇聚交换机**（常见 S5700/S6700/S8700、CloudEngine 等）。**不是** SmartAX OLT（MA5600/MA5800/EA5800）。OLT 用 `allinpol.huawei.olt`。V200 与 V300（commit 风格）语法不同；本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.huawei.switch`。

## 症状

广播风暴、CPU 高、MAC 漂移、间歇丢包。

## DISCOVERY 只读

```cli
display stp brief
display stp
display mac-address flapping
display cpu-usage
```

SEP/ERPS/RRPP 等以本机 `?` 发现，勿套用未证实协议名。

## 禁止默认执行

`reset mac-address`、改 STP 优先级、关 STP：须 HIGH-IMPACT 授权与窗口。

## 来源

- 公开 VRP 命令参考与园区交换机运维速查结构化为场景，非官方手册替代。
- 本库无已观测 release 锚点；设备 CLI 优先。

