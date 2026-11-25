---
name: 10-huawei-olt-service-port
description: 在 华为 OLT（参考 R018） 上创建并校验 GPON service-port，将 ONT/GEM 通过 tag translation 接到业务 VLAN。
---

# 华为 OLT Service-Port

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

将 GEM 1 的 VLAN 100 交付到 OLT 的 L2 域。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

ONT online；GEM 1 已存在；在 mapping VLAN 模式下，GEM mapping 与 VLAN/flow 兼容；VLAN 100 已在 PON 与上联；索引 1000 空闲。

## 已确认命令

- [已确认][破坏性] `service-port 1000 vlan 100 gpon 0/1/0 ont 0 gemport 1 multi-service user-vlan 100 tag-transform translate`
- [已确认] `display service-port 1000`
- [已确认] `display service-port all`

## 发现类命令

- [DISCOVERY] 在适配到其他 release/流程之前，先用 `service-port ?`。
- [DISCOVERY] `display service-port port <F/S/P> ont <ONTID>`（按 ONT 列流）。
- [DISCOVERY][破坏性] `undo service-port <INDEX>` / 按端口+ONT 的 undo 变体 — 删户顺序见 `26-huawei-olt-ont-lifecycle`。

## 语法

索引、VLAN、F/S/P、ONT、GEM、multi-service 模式、user-vlan 与 translate。

## 示例

结果：index 1000，VLAN 100，gpon 0/1/0，ONT 0，GEM 1，admin enable，state up。

## 预期结果

service-port 为 `up`，参数与方案一致，计数器与测试流量相符。仅 `up` 而无字节/报文，不能证明转发。

## 已知错误

[错误] `Failure: No service virtual port can be operated`。

## 诊断

列出 service-port；核对索引、ONT、GEM、VLAN、PON 状态与计数器。若 ONT online、service-port `up`/零流量且 BNG 无 PADI/PADR，在变更 VLAN、WAN 或 AAA 之前，回到 line profile 的 GEM mapping。

## 依赖

ONT → GEM → service-port → VLAN → 上联。

## 风险

错误的索引或 VLAN 可能串接客户/租户。

## 回滚

先抓取 display；发现删除语法，并在删除前取得显式确认。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

在 GEM/ONT/VLAN 就绪之前不要创建；不要自动删除。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
