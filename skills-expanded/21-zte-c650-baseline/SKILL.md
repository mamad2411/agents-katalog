---
name: 21-zte-c650-baseline
description: 以只读方式确认 ZTE ZXA10 C 系列 OLT 的 fingerprint 与可脱敏 GPON 基线；已观测锚点为 C650 release V1.1.2，其他 C 系列机型须先 DISCOVERY。
---

# ZTE ZXA10 C 系列基线（参考 C650）

## 目标

在不修改 OLT 的前提下确认型号、软件、硬件、GPON 与传输。
导航适用于 ZXA10 C300 / C320 / C600 / C650 等；字面已确认 CLI 与 release 仍以 C650 / V1.1.2 为锚点，跨机型不得假定逐命令等价。

## 前置条件

- 目标、协议与凭据已由 Source of Truth 确认。
- 现行范围为 `READ` 或 `DISCOVERY`。
- 查询前先校验 host key 与会话身份。

## 已确认命令

- [已确认] `show software`（`ZXA10 C650`，软件 `V1.1.2`）。
- [已确认] `show hostname`、`show card`、`show equipment`（基线）。
- [已确认] `show interface brief`、`show vlan summary`（传输）。
- [已确认] `show gpon profile tcont`、`show gpon onu profile vlan`。
- [已确认] `show gpon onu state`（状态，必须脱敏）。

## 安全发现

参数化查询前使用 `show ?` 与上下文帮助。`gpon_olt-`、`gpon_onu-`、`vport-`、`xgei-` 等引用必须来自 CLI 或 Source of Truth，禁止靠假设或扫描。

## 安全规则

- 原始响应保存在仓库外；发布前移除 ONU 序列号、LOID、用户数据、IP、密钥与电路描述。
- 在已观测上下文中 `show version` 被拒绝；改用 `show software`。
- 不要执行 `configure`、创建/删除、`commit`、`write`、`save`、reload 或 reset。持有凭据不等于获得写权限。
- 开通光猫见 `31-zte-olt-ont-one-click`；PnP/开局见 `32-zte-olt-onu-pnp`（均须另行 WRITE 授权）。

## 来源

- 已观测 CLI：ZXA10 C650 / V1.1.2。
- 设备 CLI 优先于通用文档。
