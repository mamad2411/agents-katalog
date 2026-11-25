---
name: antigravity-remote
description: 管理 antigravity远程-mogu 插件：微信 / QQ / 飞书 机器人的扫码绑定、会话绑定、远程发消息与文件回传、故障排查。
---

# antigravity远程-mogu

把手机 IM 变成 Antigravity 的遥控器：面板扫码绑定机器人 → 手机发消息 → 桌面会话执行 → 思考/工具过程实时流式回推 → 产出文件直接发回聊天。

## 何时用这个技能

- 用户说"绑定微信 / QQ / 飞书机器人""扫码接入""手机上看进度""把文件发到我微信"
- 需要排查：机器人离线、扫码过期、消息没进 Antigravity、回复没回传

## 快速检查

```bash
# 守护进程健康（含 Antigravity 连接、各机器人状态）
curl -s http://127.0.0.1:8791/api/health | node -e "process.stdin.pipe(process.stdout)"

# 当前绑定
curl -s http://127.0.0.1:8791/api/bots
```

## 常见问题

| 现象 | 处理 |
|---|---|
| 面板打不开 / 侧栏空白 | 看 `~/.gemini/memory/antigravity-remote/logs/hub.log`；确认 sidecar 在跑 |
| 微信提示"需要重新扫码"（errcode -14） | 面板点「重新扫码」，不要删配置 |
| 消息发出去了但没回复 | 检查是否绑定了会话；`/status` 看运行状态；确认 Antigravity 窗口在 |
| 回复里带"思考了 N 秒" | 不该出现：说明走的是旧版 DOM 抓取，检查是否加载了 legacy 代码 |
| 群里不响应 | 默认要求 @机器人；面板里可切换群聊策略 |

## 约束

- 不要在没有用户确认的情况下把机器人切到"所有人可用"。
- 群聊默认只响应 @机器人 的消息。
- 凭据只在 `~/.gemini/memory/antigravity-remote/secrets.json`，API 返回时一律脱敏。
