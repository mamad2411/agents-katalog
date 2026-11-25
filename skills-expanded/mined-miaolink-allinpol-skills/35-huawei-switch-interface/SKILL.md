---
name: 35-huawei-switch-interface
description: 华为 VRP 交换机端口/光模块只读巡检与授权下的 shutdown 变更；默认不 save。
---

# 华为 VRP 端口与光模块

## 适用范围

适用于华为 **VRP 园区/汇聚交换机**（常见 S5700/S6700/S8700、CloudEngine 等）。**不是** SmartAX OLT（MA5600/MA5800/EA5800）。OLT 用 `allinpol.huawei.olt`。V200 与 V300（commit 风格）语法不同；本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.huawei.switch`。

## 何时使用

端口 Down、光衰、双工不匹配、接 OLT 上联口排障。跨厂商解释层见 `diagnosis-ethernet-fault`（意图 `端口down` / `以太网故障`）。STP 专项仍可用意图 `loop`。

## DISCOVERY 只读

```cli
display interface brief
display interface ${IF}
display transceiver verbose interface ${IF}
display optical-module diagnose interface ${IF}
display lldp neighbor
```

后两条以本机 `?` 为准，名称因版本而异。

## 授权 WRITE（最小）

```cli
system-view
interface ${IF}
shutdown
undo shutdown
```

先确认对端与业务窗口。
## 配置保存（可选）

**禁止**每次改配后自动 save/write/commit。仅当用户明确要求落盘时执行；先本机 ?。


## 来源

- 公开 VRP 命令参考与园区交换机运维速查结构化为场景，非官方手册替代。
- 本库无已观测 release 锚点；设备 CLI 优先。

