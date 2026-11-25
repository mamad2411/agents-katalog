---
name: 28-huawei-olt-tr069
description: 规划 TR069 server profile 与 ONT ACS 绑定；写操作须本机 DISCOVERY 确认语法。
---

# TR069 ACS 模板与 ONT 绑定

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507；来自历史 API 工程的命令标为 [版本不同]/[DISCOVERY]，不可未经校验直接套用。

## 目标

为 HGU 远程管理准备 ACS 模板，并在 ONT 上绑定管理 VLAN/DHCP/TR069。

## 何时使用

HGU 开户需 TR069、ACS URL 变更、排障无法上报 ACS。

## 前置条件

WRITE 授权；ACS URL/账号来自 SoT；lineprofile 是否启用 tr069-management 已核查。

## 已确认命令

（本库 R018 会话尚未固化 TR069 写命令为已确认。）

## 发现类命令（API 工程）

- [DISCOVERY] `ont tr069-server-profile add profile-id <ID> profile-name "<NAME>" url <URL> ...`
- [DISCOVERY] `ont tr069-server-profile delete ...` / `display` 等价查询
- [DISCOVERY] lineprofile 内 `tr069-management enable`
- [DISCOVERY][破坏性] `ont ipconfig <P> <ONTID> dhcp vlan <VLAN> priority 0`
- [DISCOVERY][破坏性] `ont tr069-server-config <P> <ONTID> profile-id <ID>`
- [DISCOVERY] `undo ont tr069-server-config ...`；`undo ont ipconfig ...`
- [DISCOVERY] `display ont wan-info ...` 验证管理 WAN

## 顺序

1. 读 profiles / ONT 状态
2. 建或确认 TR069 profile
3. 确认 lineprofile 允许 TR069
4. 绑定 ONT ipconfig + tr069-server-config
5. 读 wan-info / ACS 侧是否上线

## 依赖

04-line-profile；07-provisioning；20-ont-wan-pppoe（业务 WAN 与管理 WAN 分离）。

## 风险

错误管理 VLAN 可导致终端失管；勿把 ACS 密码写入仓库。

## 安全规则

优先 display；为每条命令分级；对 [破坏性] 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不得把 [版本不同] 升为 [已确认]；不得跳过 service-port 清理直接删 ONT；非授权不得 factory-restore。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 交叉验证：仓库 HUAWEI-OLT-API-CROSSWALK.md 与历史 API skill.md / 能力脚本。
- 一手证据：MA5800V100R018 / SPH507 会话（已确认子集）。
- 设备 CLI 优先于文档。


