---
name: herdr-chat
description: 子 agent 与主控在 Herdr 内双向通信的协议说明。当你在 herdr 管理的 pane 里作为子 agent（claude/codex）工作时必须遵守：向主控发消息用 herdr pane run 反向注入、消息前缀带 [名称] 标识、简短对话走 pane、长文写 .temp/msg/ 文件。主控方向的消息通过 agent prompt 到达，直接回复即可。要求 HERDR_ENV=1，依赖 herdr skill。
---

# Herdr Chat

本 skill 说明子 agent 与主控（用户侧）的双向通信协议。主控消息从 `agent prompt` 到达，你正常回复；主动联系主控用下面两种通道。

## 主动发消息给主控

通道一：简短对话，注入主 pane：

```bash
herdr pane run <主控pane-id> "[<你的agent名>] 消息内容"
```

通道二：长文或多段落，写文件后告知路径：

```bash
mkdir -p .temp/msg
# 完整内容写入 .temp/msg/<你的agent名>.md
herdr pane run <主控pane-id> "[<你的agent名>] 长文已写入 .temp/msg/<你的agent名>.md"
```

## 消息格式

- 前缀固定 `[发送方名称] `：主控侧是 `[主控]`，你这边是 `[<你的agent名>]`；
- 主 pane 同时跑着用户与主控，前缀让所有读屏者一眼分清发送方；
- 一条消息一件事，避免多条意图混在一条 pane 注入里；
- 禁止把命令提示符、shell 状态、屏幕内容等噪声注入主 pane。

## 边界

- 你的 `$HERDR_PANE_ID` 是自己的工作区，**不等于**主控 pane id；主控 pane id 由主控在派活简报里告知，未告知就不得猜测/探测，直接问（用通道一）。
- `pane run` 是 shell 注入：消息文本必须以 `[` 开头且不含换行拆分，斜杠开头的文本加 `MSYS_NO_PATHCONV=1` 前缀。
- 主 pane 峰值时刻（用户在操作时）减少注入频率，重要消息等主控空闲再发。
- 只读写自己的 `.temp/msg/<你的agent名>.md`；主控的 `.temp/msg/<主控>.md` 只读不写。
