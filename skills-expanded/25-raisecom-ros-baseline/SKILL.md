---
name: 25-raisecom-ros-baseline
description: 在 READ/DISCOVERY 下确认瑞斯康达 ROS/ROAP 设备 fingerprint；使用 ALLinPOL 原生会话配置 allinpol.raisecom.ros 或 allinpol.raisecom.roap 取证，不假定具体型号已确认。
---

# Raisecom ROS 基线

## 目标

在不修改设备的前提下确认 Raisecom 平台（ROS 或 ROAP）身份与可脱敏概览。

## 前置条件

- Source of Truth 已给出目标与凭据机制；按产品线选择 `allinpol.raisecom.ros` 或 `allinpol.raisecom.roap`（见 [VENDOR-ACCESS.md](../../VENDOR-ACCESS.md)）。
- 现行范围为 `READ` 或 `DISCOVERY`。

## DISCOVERY 命令

须在目标上验证：

- `show version` / `show system`
- `show interface`
- `show vlan`
- 上下文 `?`

模块：[fingerprint-and-cli-discovery](../../docs/raisecom/ros/cli/fingerprint-and-cli-discovery.md)

## 安全规则

- 先确认 ROS vs ROAP，再选命令集。
- 光接入（ONU/PON）相关语法仅在 CLI 证明存在后使用。
- 无授权禁止保存配置与重启；不记录密钥与 ONU 序列号。

## 来源

- 会话：ALLinPOL 原生配置 `allinpol.raisecom.ros` / `allinpol.raisecom.roap`。
- CLI 证据：待目标会话取证；当前无已确认锚点。
