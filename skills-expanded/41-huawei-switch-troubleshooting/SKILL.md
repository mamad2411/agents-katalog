---
name: 41-huawei-switch-troubleshooting
description: 华为 VRP 交换机上联/VLAN/聚合不通的分层排障；对接华为 OLT 上联时交叉 11/12 Skill。
---

# 华为 VRP 交换机排障

## 适用范围

适用于华为 **VRP 园区/汇聚交换机**（常见 S5700/S6700/S8700、CloudEngine 等）。**不是** SmartAX OLT（MA5600/MA5800/EA5800）。OLT 用 `allinpol.huawei.olt`。V200 与 V300（commit 风格）语法不同；本库无指定型号已确认锚点，一律 `[DISCOVERY]`。会话：`allinpol.huawei.switch`。

## 分层（先读后写）

1. 物理/光：Skill 35
2. VLAN/PVID/trunk 列表：Skill 36
3. Eth-Trunk 成员 Up 数：Skill 37
4. MAC 是否学在预期口：Skill 39
5. 若对端是华为 OLT：OLT 侧 `display port vlan`（Skill 11/12），两边 VLAN 必须一致
6. 三层才查 VLANIF/路由：Skill 38

## 决策

未知或否 → 停在该层。不授权则不做 `save`。

## 来源

- 公开 VRP 命令参考与园区交换机运维速查结构化为场景，非官方手册替代。
- 本库无已观测 release 锚点；设备 CLI 优先。

