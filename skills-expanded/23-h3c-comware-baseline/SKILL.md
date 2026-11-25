---
name: 23-h3c-comware-baseline
description: 在 READ/DISCOVERY 下确认 H3C Comware 设备 fingerprint；使用 ALLinPOL 原生会话配置 allinpol.h3c.comware，以 display 类只读查询取证，不假定具体型号已确认。
---

# H3C Comware 基线

## 目标

在不修改设备的前提下确认 Comware 平台身份、版本与可脱敏接口/VLAN 概览。

## 前置条件

- Source of Truth 已给出目标与凭据机制；会话配置 ID：`allinpol.h3c.comware`（见 [VENDOR-ACCESS.md](../../VENDOR-ACCESS.md)）。
- 现行范围为 `READ` 或 `DISCOVERY`。
- 会话建立后先校验 host key / 提示符。

## DISCOVERY 命令

下列命令为本库推荐起点，**须在目标上验证**后方可提升证据级别：

- `display version`
- `display device` / `display device manuinfo`
- `display interface brief`
- `display vlan brief`
- 上下文 `?`

模块：[fingerprint-and-cli-discovery](../../docs/h3c/comware/cli/fingerprint-and-cli-discovery.md)

## 安全规则

- 禁止 `system-view` 下的配置变更、`save`、`reboot`（无 WRITE/HIGH-IMPACT 授权时）。
- 不把完整配置或密钥写入仓库/日志。
- Comware V5/V7/V9 等语法差异大；版本不符即停止硬套。

## 来源

- 会话：ALLinPOL 原生配置 `allinpol.h3c.comware`。
- CLI 证据：待目标会话取证；当前无已确认锚点。
