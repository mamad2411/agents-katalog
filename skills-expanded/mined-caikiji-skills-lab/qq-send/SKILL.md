---
name: qq-send
description: 当用户要求通过 QQ 发送消息、文件或图片（如"用 QQ 发给 XX 这份报告""QQ 通知我任务完成""把截图 QQ 给某人"）或需要捕获 QQ 目标用户 openid 时使用。执行本技能目录 scripts/qq_send.py 一次性 CLI：text 发文本、file 发本地文件或 URL、image 发图片、listen 捕获 openid、status 查状态。群聊/频道消息、QQ 机器人开发不触发。
---

# QQ 消息发送

运行入口（优先 uv，失败退化 python 直跑，`<SKILL_DIR>` 指本技能所在目录）：

```bash
uv run --project "<SKILL_DIR>" python "<SKILL_DIR>/scripts/qq_send.py" <子命令> [参数]
python "<SKILL_DIR>/scripts/qq_send.py" <子命令> [参数]  # uv 不可用且已装 requests、websocket-client 时
```

## 流程

1. 确定收件人 openid：读 `~/.config/qq-send/openid.json`；缓存缺失或收件人与缓存不符时，运行 `listen`（默认等 120 秒，可 `--timeout` 调整），并提示用户用目标 QQ 给机器人发一条私聊。
2. 确认凭据：运行 `status` 检查配置就绪；缺 appid/client_secret 时提示用户填 `~/.config/qq-send/config.json` 或环境变量 `QQ_BOT_APPID` / `QQ_BOT_SECRET`，等用户完成后再继续。
3. 发送：
   - 文本：`text --content "内容"`
   - 本地文件：`file --path <绝对路径> --content "说明"`（路径必须存在，≤200MB）
   - 网络文件：`file --url <公网URL> --name <文件名>`
   - 图片：`image --path <绝对路径>`
   - 可用 `--openid` 显式指定收件人，缺省用缓存。
4. 校验：退出码 0 且输出含"发送成功"为成功；退出码非 0 读 stderr 错误原文，不自行重试。

## 输出规范

- 成功：一句话报告（内容类型+收件人），其余细节省略。
- 失败：报告退出码与错误原文，附下一步建议（缺 openid → 先 listen；凭据缺失 → 填 config）。

## 边界

- 仅 C2C 单聊；群聊/频道不支持。
- 文本单条受官方 4000 字节上限约束：中文约 1300 字、英文约 4000 字符，超限拆多条或写文件走 file。
- 配置与缓存固定读写 `~/.config/qq-send/`，与当前工作目录无关；各子命令完整帮助见 `-h`。
- 官方 API 文档：<https://bot.qq.com/wiki/develop/api-v2/server-inter/message/overview.html>

