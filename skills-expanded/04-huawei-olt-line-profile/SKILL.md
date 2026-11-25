---
name: 04-huawei-olt-line-profile
description: 在 华为 OLT（参考 R018） 上查询与管理 ONT line profiles GPON，关联 DBA、T-CONT 与 GEM，并校验依赖。
---

# 华为 OLT Line Profile

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

保持可核验链路：line profile → T-CONT → DBA → GEM → GEM mapping VLAN/flow。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

DBA 已存在且兼容；掌握 ONT/profile 绑定清单。

## 已确认命令

- [已确认] `display ont-lineprofile gpon all`
- [已确认] `display ont-lineprofile gpon profile-id 0`（也可用于 1、2、3）
- [已确认][破坏性] `ont-lineprofile gpon profile-id 100 profile-name "LINE-OMCI-VLAN-100"`
- [已确认][破坏性] `tcont 0 dba-profile-id 200`
- [已确认][破坏性] `tcont 0 dba-profile-id 201`
- [已确认][破坏性] 参考 MA5800V100R018/SPH507：`gem mapping 1 1 vlan 100`，随后 `commit`。

## 发现类命令

- [DISCOVERY] `ont-lineprofile gpon profile-id ?`；[DISCOVERY] `tcont 0 ?`；[DISCOVERY] `gem ?`；[DISCOVERY] `gem mapping ?`；[DISCOVERY] `undo gem mapping ?`。

## 语法

先进入 profile 上下文再配置 `tcont`。在 `mapping-mode VLAN` 下，仅有 GEM 不够：profile 必须显示 GEM 与 VLAN/flow 的显式关联。在观测到的 R018 上，命令树为 `gem mapping <GEM_ID> <MAPPING_INDEX> vlan <SERVICE_VLAN>`；任何变更前，在目标设备上重新发现索引、类型与 VLAN。

## 示例

参数化 profile：Qos PQ、Mapping VLAN、T-CONT → DBA、GEM ETH 与 `gem mapping <GEM_ID> <MAPPING_INDEX> vlan <SERVICE_VLAN>`。

```text
ont-lineprofile gpon profile-id <LINE_PROFILE_ID>
gem mapping <GEM_ID> <MAPPING_INDEX> vlan <SERVICE_VLAN>
commit
```

参数化回滚，变更窗口前须在目标 release 用 `?` 校验：

```text
ont-lineprofile gpon profile-id <LINE_PROFILE_ID>
undo gem mapping <GEM_ID> <MAPPING_INDEX>
commit
```

## 预期结果

查询 profile 可见 T-CONT、GEM；在 VLAN mapping 模式下，mapping 与 VLAN/flow 以及 service-port 引用的 GEM 一致。

## 已知错误

[错误] `Failure: The line profile does not exist`；添加 ONT 时可能出现 Max DBA 相关错误。

## 诊断

列出 profiles；核对引用的 DBA、T-CONT、GEM、mapping、`binding times` 与 service-port。若出现 ONT online + service-port UP/零流量 + BNG 无 PPPoE PADI，须先查 GEM mapping，再查后续层。

## 依赖

DBA 201；GEM 1；ONT 0/1/0。

## 风险

修改已绑定 profile 可能影响多台 ONT。`commit` 前确认 `binding times`、mapping 索引空闲/正确、脱敏快照、中止条件、备用访问与具体回滚。`commit` 仅在 profile 上下文生效；全局 `save` 是另一动作，未经显式授权切勿执行。

## 回滚

先捕获变更前 detail；优先新建 profile 并受控重新绑定。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

未经分析不要删除默认 0（`line-profile_default_0`，含 T-CONT 0→DBA2 与 T-CONT1→DBA0）。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
