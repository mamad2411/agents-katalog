---
name: 05-huawei-olt-service-profile
description: 在 华为 OLT（参考 R018） 上查询与配置 ONT service profiles GPON 及以太网口 VLAN，使用已验证语法。
---

# 华为 OLT Service Profile

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

通过 service profile 将 VLAN 100 应用到 ONT 的 ETH 1–4，并区分该映射与尚未发现的路由 WAN profile。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

VLAN 100 已存在；profile ID 空闲；确认 ONT 物理能力。

## 已确认命令

- [已确认] `display ont-srvprofile gpon all`
- [已确认] `display current-configuration | include ont-srvprofile`
- [已确认][破坏性] `ont-srvprofile gpon profile-id 100 profile-name "SRV-OMCI-VLAN-100"`
- [已确认][破坏性] `port vlan eth 1 translation 100 user-vlan 100`（对 2、3、4 重复）

## 发现类命令

- [DISCOVERY] `ont-port ?`；`ont-port eth ?`；`port ?`；`port vlan ?`；`port vlan eth ?`；`port vlan eth 1-4 ?`。

## 语法

已确认写法为逐端口配置。Discovery `port vlan eth 1-4 100 ?` 曾显示 `<cr>`、`TLS`、`priority`、`prival`，但尚未确认为可执行动作。

## 示例

将 ETH 1–4 各自配置为 translation 100/user-vlan 100，并查询该 profile。

## 预期结果

Profile 100 显示四个 ETH 口均在 VLAN 100。这只确认以太网映射，不确认 WAN route、PPPoE、NAT 或 DHCP。

## 已知错误

[错误] `port vlan eth 1-4 vlanid100` 被拒绝。

## 诊断

回到 service profile 上下文，用 `?` 发现下一 token。

## 依赖

VLAN 100、具备四口 ETH 的 ONT、ONT 绑定。涉及 route/PPPoE 时，另加载 `20-huawei-olt-ont-wan-pppoe`。

## 风险

错误映射可能导致 LAN 隔离或业务混杂。

## 回滚

记录变更前映射，并在变更窗口前用 `?` 取得删除/回退语法。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不要假定 1-4 范围语法与逐端口配置相同，也不要假定仅凭本 service profile 就能把 ONT 变成路由器。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
