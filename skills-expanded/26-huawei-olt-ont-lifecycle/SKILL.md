---
name: 26-huawei-olt-ont-lifecycle
description: 按先业务后注册顺序做 ONT 删户、复位与出厂恢复预检；语法须本机 DISCOVERY。
---

# ONT 生命周期（删户 / 复位）

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507；来自历史 API 工程的命令标为 [版本不同]/[DISCOVERY]，不可未经校验直接套用。

## 目标

安全完成 ONT 去开通与复位，避免残留 service-port 或误删在用对象。

## 何时使用

移机、销户、更换 SN、卡死复位、授权清理僵尸 ONT。

## 前置条件

显式 WRITE 授权；已采集 F/S/P、ONT-ID、SN、service-port 索引；文本备份。

## 已确认命令

- [已确认] `display ont info summary <F/S/P>`
- [已确认] `display service-port all`（或按端口过滤的本机等价查询）

## 发现类命令（API 工程常用，本库须先 ?）

- [DISCOVERY][破坏性] `undo service-port port <F/S/P> ont <ONTID>`（确认 y）
- [DISCOVERY][破坏性] `undo service-port <INDEX>`
- [DISCOVERY][破坏性] `interface gpon <F/S>` → `ont delete <P> <ONTID>`
- [DISCOVERY][破坏性] `ont reset <P> <ONTID>` / `ont reset graceful ...`
- [DISCOVERY][破坏性] `ont factory-setting-restore ...`（高风险，默认禁止）
- [DISCOVERY] 按 SN 定位：`display ont info by-sn <SN>`（API skill.md）

## 删户顺序（强制）

1. 读：ONT 状态 + service-port 列表
2. 删：全部相关 service-port
3. 删：ONT 注册
4. 读：复核无残留；必要时再查 autofind

## 已知错误

- `Failure: The ONT ID has already existed` → 先 by-sn 定位旧位置再迁
- `Failure: The ONT does not exist` → 核对 F/S/P/ONT-ID
- `No service virtual port can be operated` → 先列 service-port

## 依赖

10-service-port；08-ont-status；17-rollback；18-cleanup。

## 风险

颠倒顺序会导致业务残留或删错口；factory-restore 可抹终端侧配置。

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


