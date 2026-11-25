---
name: 24-ruijie-rgos-baseline
description: 在 READ/DISCOVERY 下确认锐捷 RGOS 设备 fingerprint；使用 ALLinPOL 原生会话配置 allinpol.ruijie.rgos，以 show 类只读查询取证，不假定具体型号已确认。
---

# Ruijie RGOS 基线

## 目标

在不修改设备的前提下确认 RGOS 平台身份、版本与可脱敏接口/VLAN 概览。

## 前置条件

- Source of Truth 已给出目标与凭据机制；会话配置 ID：`allinpol.ruijie.rgos`（见 [VENDOR-ACCESS.md](../../VENDOR-ACCESS.md)）。
- 现行范围为 `READ` 或 `DISCOVERY`。

## DISCOVERY 命令

须在目标上验证：

- `show version`
- `show inventory`
- `show interfaces status` / `show ip interface brief`
- `show vlan`
- 上下文 `?`

模块：[fingerprint-and-cli-discovery](../../docs/ruijie/rgos/cli/fingerprint-and-cli-discovery.md)

## 安全规则

- 无授权禁止 `configure` / `write` / `reload`。
- 不记录密钥与完整 running-config。
- 产品线不同则命令子集不同；拒绝时改 DISCOVERY，勿推断写命令。

## 来源

- 会话：ALLinPOL 原生配置 `allinpol.ruijie.rgos`。
- CLI 证据：待目标会话取证；当前无已确认锚点。
