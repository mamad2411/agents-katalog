---
name: 07-huawei-olt-ont-provisioning
description: 在 华为 OLT（参考 R018） 上按 SN 开通 ONT，使用已校验的 line/service profiles，并先诊断 DBA 兼容性。
---

# ONT 开通

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

为台架 EG8145X6-10 添加正确的 GPON 链路，并将 ONT 授权与后续 WAN 配置分开。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

Autofind 与 SN 已确认；已查询 profiles 100；DBA 兼容；ONT-ID 空闲；回滚已准备。

## 已确认命令

- [已确认][破坏性] 源会话：`ont add ${PON_PORT} ${ONT_ID} sn-auth ${ONT_SERIAL} omci ont-lineprofile-id ${LINE_PROFILE_ID} ont-srvprofile-id ${SERVICE_PROFILE_ID} desc "${ONT_DESCRIPTION}"`。在目标设备上重新发现各参数值。

## 发现类命令

- [DISCOVERY] `ont add ?`；`ont add ${PON_PORT} ?`；`ont add ${PON_PORT} ${ONT_ID} sn-auth ?`；`ont add ${PON_PORT} ${ONT_ID} sn-auth ${ONT_SERIAL} ?`；`ont add ${PON_PORT} ${ONT_ID} sn-auth ${ONT_SERIAL} omci ?`。

## 语法

在 GPON 0/1 上下文：port 0、ONT-ID 0、sn-auth、OMCI 与各 profile ID。

## 示例

观测输出：`Number of ONTs that can be added: 1, success: 1`；PortID 0，ONTID 0。

## 预期结果

ONT 0 已添加，随后在 `display ont info summary 0/1/0` 中为 online。这不证明 WAN PPPoE 已创建或已认证。

## 已知错误

[错误] `Failure: The maximum bandwidth of the referenced DBA profile exceeds the limitation`。

## 诊断

排查 DBA Max、能力/ont-type、line profile、T-CONT、GEM 与引用关系。不要盲目改 Max。

## 依赖

Autofind；DBA；line profile；service profile；PON。route/PPPoE 配置属于后续步骤 `20-huawei-olt-ont-wan-pppoe`。

## 风险

错误的 SN/端口/profile 可能中断或占用其他 ONT 的业务。

## 回滚

仅在查清依赖后规划删除 ONT 与 service-port；delete 语法须先发现。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不要保存密码；不要把生产 SN 当作可执行示例；非必要不要修改在线 ONT。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
