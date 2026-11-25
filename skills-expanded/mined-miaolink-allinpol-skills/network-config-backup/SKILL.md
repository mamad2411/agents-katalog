---
name: network-config-backup
description: 对清单中的网络设备采集、脱敏、校验、命名、对比并文档化文本配置备份。用于变更前后、定期采集、回滚准备，或在纳入版本前校验文件。
---

# 安全配置备份

## 原则

- 以 Source of Truth 清单为身份、厂商与型号的权威。
- 切勿从本 skill 推断真实设备或取值。
- 所有目标与取值保持参数化。
- 默认只读。将持久化、导出到服务器、写入与改配归为可变操作。
- 无显式授权、已知影响与回滚时，禁止可变命令。
- 切勿覆盖已有备份；切勿把密钥记入 Git、日志、Issues 或 PR。

## 必填参数

接入设备前在 Source of Truth 中解析：

- `${DEVICE_NAME}`：规范名称；
- `${DEVICE_CATEGORY}`：`olt`、`routers`、`switches`、`radios`、`servers` 或 `other`；
- `${DEVICE_VENDOR}` 与 `${DEVICE_MODEL}`；
- `${DEVICE_HOST}`：授权地址（勿复制到公开证据）；
- `${BACKUP_DATE}`：`DD-MM-AAAA`；
- `${BACKUP_PHASE}`：空、`pre`、`pos` 或已批准序列；
- `${BACKUP_ROOT}`：Source of Truth 备份根目录；
- `${READ_TIMEOUT_SECONDS}`：采集超时；
- `${PAGINATION_MODE}`：经已校验语法禁用分页，或受控手动翻页；
- `${EXPECTED_END_MARKER}`：该平台已校验的结束提示符/标记。

若身份、厂商或型号未确认，仅做安全观察并记录 `待校验`。不要用任意名称创建备份。

## 流程

1. **观察：** 确认目标、会话、提示符、日期、只读访问与目标目录空间。
2. **选择流程：** 完整阅读厂商/型号 skill、[命令分级](references/command-classification.md) 与[分平台命令](references/vendor-commands.md)。
3. **预检：** 填写 [readiness 清单](references/preflight-checklist.md)，确认目标路径不存在，并定义超时、分页与结束标记。
4. **采集：** 执行已确认或经 CLI 发现的展示命令。采集中不要隐含执行 `save`、`write`、`copy`、export、reload 或等价操作。
5. **仓库外保留原始：** 若含密钥，原始输出仅放在受保护存储。
6. **脱敏：** 生成拟纳入版本的副本，遮蔽凭据、哈希、密钥、community、token 及 Source of Truth 政策禁止的数据。
7. **校验：** 核对完整性、身份、名称、日期、内容、脱敏、未覆盖，以及[输出契约](references/output-contract.md)。
8. **对比：** 与上一份备份对照，标出意外差异。
9. **记录：** 记录命令、时间、结果、限制、旧/新文件，不含密钥。
10. **事后检查：** 确认会话仍只读，且设备状态未变。

## 路径与名称

使用：

```text
${BACKUP_ROOT}/${DEVICE_CATEGORY}/${DEVICE_NAME}/${DEVICE_NAME}-${BACKUP_DATE}.txt
```

与一次变更绑定的两次采集追加 `-pre`/`-pos`。同日独立采集用 `-01`、`-02`…。主文件不要用 `latest.txt`、Unix 时间戳或泛名。

静态校验可用的合成示例：`OLT-LAB-01-12-08-2026.txt`、`OLT-LAB-01-12-08-2026-pre.txt`、`OLT-LAB-01-12-08-2026-pos.txt`、`OLT-LAB-01-12-08-2026-01.txt`。它们不代表真实设备。

## 超时、分页与截断

- 采集前设定 `${READ_TIMEOUT_SECONDS}`；切勿无限等待。
- 仅用该平台已分级且上下文已校验的命令禁用分页；否则手动翻页，勿发送可能被当成命令的文本。
- 若残留分页提示、超时、断连、缓冲上限、错误信息或缺少 `${EXPECTED_END_MARKER}`，则采集无效。
- 不要静默拼接部分结果。原因消除后用新文件重采。

## 脱敏

至少检查：

- 密码与 secrets（含哈希与密文）；
- SSH 密钥、证书与密码学材料；
- SNMP community；
- RADIUS/TACACS+/BGP/PPP secrets；
- URL 内嵌 token/凭据；
- 版本化备份不需要的个人用户/标识。

使用明确标记如 `<REDACTED_SECRET>`。当地址、VLAN、接口属于授权 Source of Truth 的必要部分时，不要替换它们。若脱敏后失去运维价值，则不要纳入版本，改走批准的受保护存储。

## 校验与对比

- 确认文件非空、身份与日期匹配、结束标记存在、无密钥泄漏迹象。
- 与上一备份对比时，区分预期变更与意外差异；意外差异阻断版本化直至解释清楚。

## 失败与回滚

- 采集失败：保留诊断、不覆盖旧备份、不提交部分文件。
- 脱敏失败：不版本化，原始仅留受保护存储。
- 本流程默认不改设备；若误发可变命令，立即中止并转平台 rollback skill。

## 安全规则

- 永不在证据中打印密钥。
- 永不覆盖现有备份文件。
- 永不把原始含密配置提交到 Git。
- 永不把备份流程当作改配窗口。
