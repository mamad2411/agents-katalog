---
name: wecom-alert-reader
description: 企业微信（WeCom）Windows 本地聊天记录只读解密与查询。从运行中的 WXWork.exe 进程内存提取 wxSQLite3 密钥，把本地加密库解密成只读明文快照，再查询会话、按群读取消息历史、全文搜索（典型用途：读取告警群/风控群最新消息）。触发词：企微告警、读企微消息、企微聊天记录、wecom 解密、wxwork 快照。绝不发送企业微信消息，绝不操作企微客户端，聊天内容不离开本机。
---

# wecom-alert-reader：企业微信本地数据只读读取（Windows）

## 原理

企微 5.x（Windows）本地库使用 wxSQLite3 AES-128-CBC 分页加密：

- **全局 raw key**：16 字节，解密所有库（各库仅「盐」= 每库文件前 16 字节不同）
- **每页派生**：页钥 = `MD5(raw_key + 页号(小端32位) + "sAlT")`，IV = MD5(伪随机种子序列)——与 SQLite3MultipleCiphers 的 wxSQLite3 方案一致（公开算法）
- **密钥来源**：客户端运行时必须把 raw key 常驻进程内存 → 用 Windows API（`OpenProcess` / `VirtualQueryEx` / `ReadProcessMemory`，全部只读）扫描 WXWork.exe 内存提取，候选钥必须先解密目标库第一页、验证出合法 SQLite 头与 B-tree 页类型才算数

实现 vendored 自 [wangk-ask/wecom-reader](https://github.com/wangk-ask/wecom-reader)（MIT），
含两处本地补丁（见下方「本地补丁记录」）。算法参考同样可见 SQLite3MultipleCiphers
公开文档与 yichen-wecom-local-vault（macOS 侧）skill 的公开说明。

## 强制边界（违反任何一条即停止）

1. 只读：不修改、不删除、不写回企微任何原始文件；只对快照查询。
2. 绝不发送企业微信消息，绝不点击/启动/退出/操控企微客户端。
3. 快照、密钥、导出文件只留本机私有目录；raw key 不进入聊天、日志、报告或记忆。
4. 聊天内容属于用户与企业：摘要/查询结果只给本机用户本人；使用者自行确认企业数据
   政策允许（参见 references/risks.md 的风险备忘——包括腾讯 DMCA 下架先例）。
5. 提 key 需要 WXWork.exe 正在运行；失败报告「未捕获」，不重试超过 2 次。
6. 不解密媒体文件正文（图片/语音/文件只出占位信息）。

## 依赖

- Windows 10/11，Python ≥ 3.10
- `pip install pycryptodomex click flask`
- WXWork.exe 正在运行（提 key 时）

## 快速开始

```bash
cd skills/wecom-alert-reader/scripts

# 1. 提取密钥 + 解密所有库（WXWork.exe 运行中）
python -m wecom_reader.cli --db-dir "D:\WXWork\WXWork\<account_id>\Data" init

# 2. 查看状态（哪些库解密成功、各含哪些表）
python -m wecom_reader.cli --db-dir "D:\WXWork\WXWork\<account_id>\Data" status

# 3. 列会话 / 读消息 / 搜索 / 查联系人
python -m wecom_reader.cli --db-dir "D:\WXWork\WXWork\<account_id>\Data" sessions --limit 30
python -m wecom_reader.cli --db-dir "D:\WXWork\WXWork\<account_id>\Data" messages R:<群ID> --limit 20
python -m wecom_reader.cli --db-dir "D:\WXWork\WXWork\<account_id>\Data" search "关键词"
python -m wecom_reader.cli --db-dir "D:\WXWork\WXWork\<account_id>\Data" contacts --keyword "名字"

# 4. 本地 Web UI（127.0.0.1:8765）
python -m wecom_reader.web --db-dir "D:\WXWork\WXWork\<account_id>\Data"
```

`<account_id>` = 企微数据目录下的账号目录名（形如 `1688xxxxxxxxxxxxx` 的数字串），
通常在 `%USERPROFILE%\Documents\WXWork\<account_id>\Data` 或自定义数据目录
（如 `D:\WXWork\WXWork\<account_id>\Data`）。判定标准：目录内同时存在
`message.db`、`session.db`、`user.db` 且文件头不是明文 `SQLite format 3`。

## 会话 ID 格式

| 前缀 | 类型 |
|---|---|
| `R:<数字>` | 群聊 |
| `S:<数字>_<数字>` | 单聊 |
| `M:<数字>` | 微信联系人 |
| `O:<数字>` | 应用/公众号 |
| `Y:<数字>` | 系统会话 |

## 故障排查

- `No such option '--db-dir'`：--db-dir 是主组选项，写在子命令（init/status/…）**前面**。
- `Failed to extract`：确认 WXWork.exe 在运行（`tasklist /FI "IMAGENAME eq WXWork.exe"`）；
  同用户进程一般无需管理员；失败可重试一次（密钥只在客户端实际读写库时才会被扫到）。
- 企微升级后：先 `status` 看 tables 是否可读；内存布局变化可能需要更新扫描特征。
- 部分库没解出来：工具会对未匹配盐做交叉验证（用已知钥试解其他库）。

## 本地补丁记录（相对上游的改动，保持可追溯）

1. **2026-10-16 · crypto/key_extract.py**：修复交叉验证分支在迭代 `key_map.values()`
   时向 `key_map` 插入新键的 RuntimeError（原实现在部分库未匹配时必崩）。改为先收集
   再写回。
2. **2026-10-16 · web.py**：修复本地 Web UI 存储型 XSS——`escapeHtml` 补单引号转义；
   会话条目移除内联 onclick（群名可逃逸 JS 字符串），改为 data-* 属性 + 事件委托。
3. 快照输出位置由使用者以 `--decrypted-dir` 指定（建议放在私有目录，勿放进会被打包
   或同步的位置）。

## 验证基线

2026-10-15 于 Windows 11 + WXWork 5.0.11.6018 实测：18 个本地数据库全部解密成功
（message/session/user/file/calendar/crm 等 0 失败），群消息（发送者/分钟级时间戳/正文）
完整还原。两处补丁后重跑基线一致。
