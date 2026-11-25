---
name: 37-huawei-switch-eth-trunk
description: 华为 VRP Eth-Trunk/LACP 成员口、负载分担与对接 OLT/上联聚合的 DISCOVERY 流程。
---

# 华为 VRP Eth-Trunk / LACP

## 适用范围

适用于华为 **VRP 园区/汇聚交换机**（常见 S5700/S6700/S8700、CloudEngine 等）。**不是** SmartAX OLT（MA5600/MA5800/EA5800）。OLT 用 `allinpol.huawei.olt`。V200 与 V300（commit 风格）语法不同；本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.huawei.switch`。

## 场景

OLT 或核心侧 LACP 聚合；本端 Eth-Trunk 成员必须同速率/双工。

## DISCOVERY 只读

```cli
display eth-trunk
display eth-trunk ${ID}
display lacp statistics eth-trunk ${ID}
display interface brief | include Eth-Trunk
```

## DISCOVERY 写（HIGH-IMPACT，须明确授权）

```cli
system-view
interface Eth-Trunk ${ID}
mode lacp-static
interface ${MEMBER_IF}
eth-trunk ${ID}
```

`mode` 取值（lacp-static / manual 等）以本机 `?` 为准。改聚合可能中断上联。
## 配置保存（可选）

**禁止**每次改配后自动 save/write/commit。仅当用户明确要求落盘时执行；先本机 ?。


## 来源

- 公开 VRP 命令参考与园区交换机运维速查结构化为场景，非官方手册替代。
- 本库无已观测 release 锚点；设备 CLI 优先。

