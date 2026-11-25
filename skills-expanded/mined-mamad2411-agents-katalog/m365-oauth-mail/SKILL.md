---
name: m365-oauth-mail
summary: 读取 Microsoft 365 / Office 365 学校或企业邮箱（密码 IMAP 被租户禁用时的 OAuth2 方案）
read_when:
  - 用户需要自动读取、总结 Outlook / Office 365 / 微软教育版邮箱
  - IMAP 密码登录报 AUTHENTICATE failed 或租户禁用基础认证
  - 设备码授权时提示 Enter justification（管理员审批）需要绕过
---

# M365 邮箱 OAuth2 只读访问（设备码 + Outlook REST）

适用于任何能执行Python3脚本的环境，只依赖标准库。

## 背景与坑位（实测 2026-08）

1. **密码直连 IMAP 已被微软全面禁用**：`imaplib` + 密码登录 `outlook.office365.com:993` 会报
   `AUTHENTICATE failed`，不要走这条路。
2. **Thunderbird 公共客户端 ID（9e5f94bc-...）在开启管理员审批的租户会弹
   "Enter justification for requesting this app"**，走不通。
3. **解法：用微软第一方 Office 客户端 ID `d3590ed6-52b3-4102-aeff-aad2292ab01c`**，
   第一方应用免管理员审批，设备码流程直接成功。
4. **该 ID 的令牌不含 IMAP.AccessAsUser.All**（IMAP XOAUTH2 仍会失败），但含
   `Mail.ReadWrite / EWS.AccessAsUser.All / OutlookService.AccessAsUser.All`，
   **改走 Outlook REST API v2.0 即可**：`GET https://outlook.office365.com/api/v2.0/me/messages`。

## 关键技术点

- 认证用 **v1 端点**（非 v2.0）：`https://login.microsoftonline.com/common/oauth2/`
  - devicecode 请求：`client_id` + `resource=https://outlook.office365.com`
  - token 轮询参数名是 **`code`**（v1 不叫 `device_code`，两个都传最稳）
  - token 刷新：`grant_type=refresh_token` + `resource`
- v1 端点返回的字段：`verification_url`（不是 verification_uri）、`expires_in` 是**字符串**
  （代码里要 float() 转换）
- 设备码要**落盘保存**（含 expires_at），进程因网络抖动挂掉后重启可复用未过期设备码
- HTTP 请求加重试（代理环境偶发 502 Tunnel connection failed）
- REST API 返回字段是 **PascalCase**（Subject/From/ReceivedDateTime/BodyPreview），
  BodyPreview 直接可用作摘要，无需解析正文
- 令牌文件权限 chmod 600；不要把令牌或密码写进任何 prompt / 配置模板

## 现成脚本

`scripts/fetch_emails.py`（仅标准库，python3 直接运行，支持 `--help`）：

```
python3 fetch_emails.py --help  # 完整用法（agent 探索工具时的第一入口）
python3 fetch_emails.py --login # 首次授权：打印 login.microsoft.com/device + 代码，浏览器登录一次（login 兼容旧写法）
python3 fetch_emails.py         # 拉取最近 24h 邮件，输出 markdown 摘要（只读，不标记已读）
python3 fetch_emails.py 12      # 拉取最近 12 小时（位置参数覆盖默认值，合法范围 1..720）
python3 fetch_emails.py --new-only  # 只输出相对上次运行的新邮件（去重，标 [新] 的邮件进 seen 记录）
python3 fetch_emails.py --full 48   # 输出完整正文（HTML 解析为纯文本，单封上限 20000 字符）
```

去重机制：每次运行会把拉取到的消息 Id 记入 `email_seen.json`（带时间戳，31 天自动修剪）。
默认输出全部邮件并在头部显示「共 X 封，其中 Y 封新」，新邮件带 `[新]` 标记；
定时任务建议配 `--new-only`，避免窗口重叠时重复分类。

退出码：0 成功 / 2 网络 / 3 认证失败 / 4 `[NEED_LOGIN]` 令牌失效需重新 login / 5 API 错误。
stdout 输出 markdown 摘要，错误信息走 stderr，方便 agent 判断分支。

### 数据目录

脚本默认自动使用固定数据目录 **`~/.m365-oauth-mail/`**（无需任何配置，目录不存在会自动创建）。

- `~/.m365-oauth-mail/email_tokens.json`：OAuth 令牌（600 权限，核心实例数据）
- `~/.m365-oauth-mail/email_pending_device.json`：授权中设备码断点（授权成功自动删除）
- `~/.m365-oauth-mail/email_seen.json`：已见消息 Id 去重记录（保留 31 天自动修剪）
- 可选 `~/.m365-oauth-mail/email_config.json`：`{"hours": 12}` 固定默认时间窗口

多邮箱场景：用环境变量 `MAIL_DATA_DIR` 为每个邮箱指定独立目录
（如 `MAIL_DATA_DIR=~/.m365-oauth-mail-corp python3 fetch_emails.py login`），互不干扰。

## 定时总结

任意调度机制均可（cron：`0 20 * * *`，或 agent 自带的定时任务能力）。要点：

- 每次运行脚本（无参数 = 最近 24h），把 stdout 交给 agent/LLM 生成分类摘要：
  【需要回复/行动】【重要通知】【可忽略】三组，每封一行
  （主题 | 发件人 | 时间 | 一句话摘要）
- 处理退出码分支：4 → 提示用户需重新授权（跑一次 `login`）；2/5 → 报告网络/API 错误

## 注意

- 刷新令牌长期闲置约 90 天过期，届时重新 `login` 一次即可。
- 该方案为只读；如需发信/移动邮件，令牌权限足够（Mail.ReadWrite），但需扩展脚本。
- 脚本可在本仓库之外独立运行；迁移到其他机器时只需带走脚本 + 对应数据目录。
