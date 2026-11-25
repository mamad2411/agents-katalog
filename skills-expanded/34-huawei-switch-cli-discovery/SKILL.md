---
name: 34-huawei-switch-cli-discovery
description: 在华为 VRP 交换机上用 ? 发现语法；区分 V200 save 与 V300 commit；禁止臆造写命令。
---

# 华为 VRP 交换机 CLI 发现

## 适用范围

适用于华为 **VRP 园区/汇聚交换机**（常见 S5700/S6700/S8700、CloudEngine 等）。**不是** SmartAX OLT（MA5600/MA5800/EA5800）。OLT 用 `allinpol.huawei.olt`。V200 与 V300（commit 风格）语法不同；本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.huawei.switch`。

## 流程

1. 确认视图：用户视图 `< >` vs 系统视图 `[ ]`
2. 每步一个 token：`display ?`、`interface ?`、`vlan ?`
3. 被拒则停，改帮助，不试写命令
4. 记录原文；未成功执行不得标 `[已确认]`

## 方言提示

- 园区 V200：`system-view` / `save`
- 部分 CE/V300：候选配置 + `commit`（与 OLT profile `commit` 不是同一对象）
- 接口名 `GigabitEthernet` / `XGigabitEthernet` / `10GE` 以本机为准

## 来源

- 公开 VRP 命令参考与园区交换机运维速查结构化为场景，非官方手册替代。
- 本库无已观测 release 锚点；设备 CLI 优先。

