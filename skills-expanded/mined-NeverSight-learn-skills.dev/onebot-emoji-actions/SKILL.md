---
name: onebot-emoji-actions
description: 在 OpenClaw OneBot / NapCat 插件里实现、接入和调试表情相关能力，覆盖标准消息段（face、poke、rps、dice、image）以及 NapCat 扩展（mface、消息贴表情、自定义表情）。
---

# OneBot 表情动作

这个 skill 关注“怎么在插件里真正接上表情能力”，包括消息段、provider 扩展和当前仓库里的落点。

## 先判断能力层

- 标准 OneBot v11：读 `standard.md`
- NapCat 私有扩展：读 `napcat.md`
- 如果需求是“让角色更会用表情”，同时配合 `onebot-emoji-style`

## 当前仓库里的关键接入点

- `src/connection.ts`：低层发送、`sendOneBotAction(...)`
- `src/send.ts`：上层主动发送 helper
- `src/handlers/process-inbound.ts`：回复捕获、消息段组装
- `src/message.ts`：入站消息语义提取
- `src/service.ts`：通知事件接入，例如 `poke`
- `src/channel.ts`：channel capability 声明

## 推荐接入顺序

1. 先做标准 `face` 的发送与接收
2. 再把入站 `face` 保留成文本语义，避免模型丢上下文
3. 再做 `poke` / `rps` / `dice`
4. 最后再单独做 NapCat 的 `mface`、消息贴表情、自定义表情

## 发送策略

- 标准消息段：构造 `OneBotMessageSegment[]`，再走 `sendGroupMsg` / `sendPrivateMsg`
- 私有 provider API：直接走 `sendOneBotAction(...)`
- 如果模型要参与决策，优先让模型输出中间标记，再由插件做后处理

## 中间标记建议

- `[[face:123]]`
- `[[rps]]`
- `[[dice]]`
- `[[poke:type=126,id=2003]]`
- `[[mface:package=1,id=abc,key=xyz,summary=贴贴]]`
- `[[emoji-like:message=12345,emoji=128,set=true]]`

## Guardrails

- 不要假设所有 OneBot 后端都支持 `mface`
- 没有本地映射表时，不要瞎猜 `face.id`
- 不要让 transcript / prompt 里只保留平台码，最好保留一份文字语义
- 只有真的实现“给消息贴表情”后，才考虑调整 `reactions` capability

## 需要细节时再读

- 标准消息段：`standard.md`
- NapCat 扩展：`napcat.md`
