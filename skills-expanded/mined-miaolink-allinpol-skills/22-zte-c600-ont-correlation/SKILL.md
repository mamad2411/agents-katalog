---
name: 22-zte-c600-ont-correlation
description: 仅在 READ/DISCOVERY 下关联 ZTE ZXA10 C 系列（C300/C320/C600/C650 等）的 GPON SN、ONU、T-CONT、GEM、vport、service-port 与 VLAN。已观测锚点为 C650；按序列号前缀（含 TPLG）调查 ONU 时使用，不预设厂商或型号。
---

# ZTE ZXA10 C 系列 ONU 关联

## 已确认范围

导航适用于 ZXA10 C300 / C320 / C600 / C650 等。唯一字面已观测 CLI 上下文为 `ZXA10 C650` + `ZTE ZXA10 Software V1.1.2`；其他机型须先确认 fingerprint，再按 DISCOVERY 校验语法，不视为已证实兼容。

本 Skill 仅为 `READ`/`DISCOVERY`。不授权开通、创建 ONU/模板/VLAN/GEM/T-CONT/service-port、`configure`、`commit`、`write`、`save`、reload 或 reset。

## 关联流程

1. 用 `show software` 确认 fingerprint。
2. 用 `show gpon onu state` 列出状态，并取得 CLI 自身确认的 `gpon_olt-` 引用。
3. 查询 `show gpon onu baseinfo <gpon_olt-confirmada>`，在 GPON SN 中定位请求的前缀。完整序列号仅保存在版本库外。
4. 对每个授权引用，用 `show gpon onu detail-info <gpon_onu-confirmada>` 关联状态与属性。
5. 对同一已确认 PON 查询：

   ```cli
   show gpon onu tcont <gpon_olt-confirmada>
   show gpon onu gemport <gpon_olt-confirmada>
   show gpon onu vport <gpon_olt-confirmada>
   ```

6. 关联业务对象：

   ```cli
   show service-port interface <gpon_onu-confirmada>
   ```

7. 当传输接口已由 Source of Truth 或 CLI 确认时，查询 VLAN 关联：

   ```cli
   show vlan port <xgei-confirmada>
   ```

引用或语法不被接受时，用 `show ?` 作为 `DISCOVERY`。不要猜测 PON、ONU、vport 或接口。

## 前缀 TPLG

`TPLG` 是 **GPON SN 发现指纹**，不是厂商/型号/芯片确认。记录为：

```text
GPON SN prefix: TPLG
厂商/型号: 未知；采集未确认
```

没有 OLT 给出的显式识别前，不要给 ONU 指派厂商，也不要把该前缀提升为兼容性规则。

## 解读

- 将 T-CONT、GEM、vport、service-port、VLAN 视为不同对象，仅关联同一 PON/ONU 上下文的引用。
- 区分 `working`、`OffLine`、`LOS`、`DyingGasp` 等管理/工作状态。频繁掉线的解释层见 `diagnosis-onu-flapping`；本 Skill 只负责中兴取证。
- 仅当响应真正暴露字段时，才记录 DBA、OMCI、OMCC 加密、line/service profile。
- 已接受查询与已观测结果用 `[已确认]`；帮助与前缀用 `[DISCOVERY]`；字面拒绝用 `[错误]`；未见为命令的逻辑序列用 `[推断]`。

## 限制与脱敏

- 不要假定 T-CONT/GEM/VLAN/OMCI/service-port 模式对 C600/C650、其他 release 或其他环境普遍成立。
- 不要版本化完整序列号、LOID、密码、IP、电路描述、用户标识、ONU 数量或原始配置。
- 不要把观测关系在**无 WRITE 授权**时直接转成开通命令。开通编排见 `31-zte-olt-ont-one-click`（字段模板 · DISCOVERY）。
