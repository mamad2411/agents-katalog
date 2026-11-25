---
name: network-device-access
description: 使用 Source of Truth 已确认参数（含授权 .env 本地凭据），对接清单中的网络设备准备、认证并校验安全会话；不扩大任务允许的命令范围。
---

# 网络设备安全接入

## 目标

建立已认证会话并校验到正确设备。连接是基础运维能力；读/测/写/持久化/破坏性动作的授权由现行提示/任务另行决定。

## 何时使用

在依赖 CLI、SSH、Telnet、API、SNMP 或其他设备管理通道的任何 skill 之前使用。

## 原则

- 本 Skill 定义接入**语义与护栏**（目标来自 SoT、认证不等于 WRITE）。具体用 SSH、Telnet、NETCONF、API 还是 MCP，由 Agent / Adapter 决定；本仓库不实现连接器。
- 不要从本 skill 推断目标、IP、主机名、凭据或拓扑。
- 认证不等于授权变更。
- 项目允许时，可用 `.env`/`.env.*` 作为本地授权的参数/凭据来源。
- 密钥只留在内存，且永不进入 Git、日志、Issues、PRs、报告或回复。

## 参数

在 Source of Truth 或授权环境中解析：

- `${DEVICE_NAME}`：规范名称；
- `${DEVICE_HOST}`：已确认的别名、DNS 或管理地址；
- `${DEVICE_VENDOR}` 与 `${DEVICE_MODEL}`；
- `${DEVICE_VERSION}`（若已知）；
- `${ACCESS_PROTOCOL}`：SSH、Telnet、API、SNMP 或其他授权方式；
- `${USERNAME_VAR}`、`${PASSWORD_VAR}`、`${TOKEN_VAR}` 或其他密钥引用（若适用）；
- `${JUMP_HOST}`（拓扑需要跳板时）；
- `${OPERATION_SCOPE}`：按任务为 `READ`、`DISCOVERY`、`TEST`、`WRITE`、`PERSIST` 或 `HIGH-IMPACT`。

## 目标解析

顺序：

1. 运维规范名称/别名；
2. 已批准的 SSH/DNS 配置；
3. Source of Truth 已确认的管理地址；
4. 本地环境中的授权连接参数。

别名解析失败时，若已有确认地址，不应放弃任务。禁止网络扫描或猜测地址。

## `.env` 使用

项目允许时：

1. 在工作区/安全本地定位 `.env`；
2. 只读会话所需变量；
3. 不做 dump、无差别 `cat`、带密钥展开的 debug 或回显凭据；
4. 不全局导出多余变量；
5. 仅在必要进程/会话中使用取值；
6. 永不把文件或取值复制进仓库；
7. 只记录“使用了授权的本地凭据源（已脱敏）”。

凭据存在不改变 `${OPERATION_SCOPE}`。

## 流程

1. **解析身份：** 确认 `${DEVICE_NAME}`、厂商/型号与主机。
2. **解析授权：** 划分现行范围。
3. **加载凭据：** 仅从授权机制取所需值。
4. **连接：** 按约定协议开会话，需要时经跳板。
5. **校验目标：** 在执行主任务前核对提示符、banner、版本或其他安全标识。按厂商选择 ALLinPOL 原生会话配置 ID（见 [VENDOR-ACCESS.md](../../VENDOR-ACCESS.md)），再进入对应 fingerprint 模块。
6. **应用护栏：** 加载厂商/型号专项 skill，只执行与范围兼容的命令。
7. **结束/脱敏：** 不持久化密钥，只记录脱敏证据。

## 运维操作类别

### READ / DISCOVERY

任务只读时允许：查询、状态、计数器、`show`、`display`、上下文帮助与安全语法发现。

### WRITE

仅当提示/任务授权变更时可用。写入前要求与风险相称的预检、已校验语法、影响、回滚、中止准则与事后验证。

### PERSIST

当平台区分 running 与 startup/持久化时，全局持久化是独立动作。不要仅因已授权变更就假定可持久化。

### HIGH-IMPACT

Reload/reset、删除、改管理面、路由、AAA、防火墙、生产 ACL/NAT 或有实质风险的动作，需要显式授权与安全方案。

## 接入失败

出现以下情况时中断自动重试：

- 凭据被拒；
- 用户/IP 锁定；
- 非预期 host key；
- banner/提示符/型号/身份不一致；
- 跳板与预期不符；
- 行为暗示目标错误。

无密钥地记录失败；仅在没有其他已定义授权来源时，才请求修正接入机制。

## 预期结果

交付已校验会话，或脱敏接入诊断，包含：`target_validated`、`protocol`、`scope`、`credential_source_sanitized`、`jump_path_sanitized`、`warnings`。

## 安全规则

- 永不打印密钥。
- 永不提交 `.env*`。
- 永不拿可用凭据去扩大提示范围。
- 永不把别名失败变成网络扫描。
- 在确认范围与平台专项 skill 之前，永不执行可变命令。
