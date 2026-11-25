---
name: telegram-dm
description: Telegram 私信/DM 自动化技能。基于 Python + Telethon 在本地直接完成 Telegram 用户账号登录、会话持久化、目标清单处理、分批私信群发与结果汇总，不依赖 gomtm 端点。适用于 Telegram 私信营销、批量发送消息、手机号登录、2FA 登录、会话导出、受众列表脚本化处理等场景。
---

# Telegram 私信群发（Python）

## 核心原则

- 仅依赖 Python 客户端库，不调用 gomtm server、mtgate 或其他项目端点。
- 优先复用本技能目录下的脚本，不临时重写一套新的登录或群发逻辑。
- 首轮演示以本地 session 文件为主，避免在聊天中暴露 `string_session`。
- 当前示例优先支持 `username` / `@username` / `https://t.me/<username>` 目标格式；手机号导入联系人不放在第一版脚本里，避免静默修改联系人列表。

## 先决条件

1. 准备 Telegram 官方 API 凭据：登录 `https://my.telegram.org` 创建应用，拿到 `api_id` 和 `api_hash`。
2. 准备 Python 3.10+ 环境。
3. 安装依赖：

```bash
/usr/bin/python3 -m pip install --user -r .agent/skills/telegram-dm/scripts/requirements.txt
```

也可以通过环境变量传递敏感参数：

```bash
export TG_API_ID="123456"
export TG_API_HASH="0123456789abcdef0123456789abcdef"
export TG_PHONE="+8613800138000"
```

## 标准工作流

1. 首次登录：运行 `scripts/login_telethon.py`，完成手机号 + 验证码 + 可选 2FA 密码登录。
2. 检查输出：确认脚本返回 `session_file` 与当前登录账号信息。
3. 准备目标：按 `scripts/example_targets.txt` 的格式整理目标清单。
4. 准备消息：直接用 `--message` 传入，或使用 `--message-file` 指向文本文件。
5. 试运行：先执行 `scripts/batch_send_telethon.py --dry-run` 验证 session 与目标是否可解析。
6. 正式发送：设置合理的 `--batch-size`、`--min-delay`、`--max-delay`、`--batch-delay` 后执行发送。
7. 查看结果：按需写出 `--report-json-out`，复盘成功数、失败数与失败原因。

## 登录流程细则

- 首次登录必须提供国际格式手机号，如 `+8613800138000`。
- Telegram 验证码通常优先发到已登录的 Telegram 客户端，其次才可能是短信。
- 若账号开启两步验证，登录脚本会继续提示输入 2FA 密码。
- 登录成功后默认持久化为本地 `.session` 文件；如需迁移到别的机器，可用 `--string-session-out` 导出字符串会话到本地文件。
- 验证码输错、过期、切换账号或 session 损坏时，重新执行登录脚本，不要手改 `.session` 文件。
- 严禁把 `string_session`、`.session` 文件、`api_hash` 贴到聊天窗口、Issue、日志或公开仓库。

## 脚本清单

- `scripts/requirements.txt`：当前示例依赖。
- `scripts/login_telethon.py`：交互式手机号登录，保存 session，并可选导出 `string_session`。
- `scripts/batch_send_telethon.py`：按目标文件分批发送或试跑校验。
- `scripts/example_targets.txt`：目标列表示例。
- `scripts/example_message.txt`：消息文案示例。

## 常用命令

首次登录：

```bash
/usr/bin/python3 .agent/skills/telegram-dm/scripts/login_telethon.py \
  --api-id "$TG_API_ID" \
  --api-hash "$TG_API_HASH" \
  --phone "$TG_PHONE" \
  --session-name marketing-demo
```

若需要导出 `string_session`：

```bash
/usr/bin/python3 .agent/skills/telegram-dm/scripts/login_telethon.py \
  --api-id "$TG_API_ID" \
  --api-hash "$TG_API_HASH" \
  --phone "$TG_PHONE" \
  --session-name marketing-demo \
  --string-session-out ~/.telegram-dm/marketing-demo.json
```

试运行校验目标：

```bash
/usr/bin/python3 .agent/skills/telegram-dm/scripts/batch_send_telethon.py \
  --api-id "$TG_API_ID" \
  --api-hash "$TG_API_HASH" \
  --session-name marketing-demo \
  --targets-file .agent/skills/telegram-dm/scripts/example_targets.txt \
  --message-file .agent/skills/telegram-dm/scripts/example_message.txt \
  --dry-run
```

正式发送并写出报告：

```bash
/usr/bin/python3 .agent/skills/telegram-dm/scripts/batch_send_telethon.py \
  --api-id "$TG_API_ID" \
  --api-hash "$TG_API_HASH" \
  --session-name marketing-demo \
  --targets-file ./targets.txt \
  --message-file ./message.txt \
  --batch-size 10 \
  --min-delay 8 \
  --max-delay 18 \
  --batch-delay 600 \
  --report-json-out ./telegram-send-report.json
```

## 发送策略

- 新账号先从 5 到 10 个目标试跑，不要一上来全量发送。
- 消息间隔建议至少 5 到 15 秒，批次间隔建议至少 5 到 15 分钟。
- 出现 `PeerFlood` 时立即停止，不要硬重试。
- 出现 `FloodWait` 时按服务端返回的等待秒数暂停；等待时间过长时直接终止本轮任务更安全。
- 先用 `--dry-run` 检查目标解析，再进入正式发送。

## 故障排查

| 问题 | 常见原因 | 处理方式 |
| --- | --- | --- |
| `ApiIdInvalidError` / `ApiHashInvalidError` | API 凭据错误 | 重新核对 `api_id` / `api_hash` |
| `PhoneCodeInvalidError` | 验证码输错 | 重新执行登录脚本并重新输入验证码 |
| `SessionPasswordNeededError` | 账号开启 2FA | 按提示输入 Telegram 两步验证密码 |
| `FloodWaitError` | 操作过快 | 按返回秒数等待，必要时结束任务 |
| `PeerFloodError` | 账号被 Telegram 风控 | 立即停止发送，等待账号恢复 |
| `UsernameNotOccupiedError` / `UsernameInvalidError` | 目标用户名无效 | 修正目标清单后重试 |
| `Session is not authorized` | session 失效或未登录 | 重新执行 `login_telethon.py` |

## 输出要求

- 给用户汇报时，优先说明：登录是否完成、session 存储位置、目标数量、试跑结果、正式发送结果。
- 不要在回复中直接回显完整 `api_hash`、`string_session` 或 `.session` 文件内容。
